from __future__ import annotations

import json
import time

import requests

from .common import redact, write_json


class ProviderError(RuntimeError):
    pass

class ResponsesClient:
    """Small Responses API client; no assumed upstream model identity or prices."""
    def __init__(self, settings):
        self.settings = settings
        self.session = requests.Session()
        self.session.headers.update({"Authorization": "Bearer " + settings.api_key,
                                     "Content-Type": "application/json"})

    def models(self):
        if not self.settings.api_key or not self.settings.base_url:
            raise ProviderError("API credentials or base URL absent")
        try:
            response = self.session.get(self.settings.base_url.rstrip("/") + "/models", timeout=30)
            if response.status_code != 200:
                raise ProviderError(f"Model discovery HTTP {response.status_code}")
            return response.json()
        except requests.RequestException as exc:
            raise ProviderError(redact(str(exc), [self.settings.api_key])) from None

    def respond(self, model, input_items, log_dir, tools=None, tool_choice=None, max_tokens=None, timeout=None):
        cfg = self.settings
        call_timeout = max(1, min(cfg.llm_timeout, timeout or cfg.llm_timeout))
        if not cfg.api_key or not cfg.base_url:
            raise ProviderError("API credentials or base URL absent")
        payload = {"model": model, "input": input_items, "store": False, "stream": True,
                   "max_output_tokens": max_tokens or cfg.max_output_tokens,
                   "reasoning": {"effort": cfg.reasoning_effort}}
        if tools:
            payload["tools"] = tools
        if tool_choice:
            payload["tool_choice"] = tool_choice
        # The request contains prompts only; Authorization is never serialized.
        write_json(log_dir / "request.json", payload)
        started = time.monotonic()
        events, terminal = [], None
        try:
            with self.session.post(cfg.base_url.rstrip("/") + "/responses", json=payload,
                                   stream=True, timeout=(min(20, call_timeout), call_timeout)) as response:
                if response.status_code != 200:
                    msg = redact(response.text[:1200], [cfg.api_key])
                    raise ProviderError(f"Responses HTTP {response.status_code}: {msg}")
                if "text/event-stream" not in response.headers.get("Content-Type", ""):
                    terminal = response.json()
                else:
                    response.encoding = "utf-8"
                    for line in response.iter_lines(decode_unicode=True):
                        if time.monotonic() - started > call_timeout:
                            raise ProviderError("Responses stream exceeded deadline")
                        if not line or not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        if data == "[DONE]":
                            continue
                        event = json.loads(data)
                        events.append(event)
                        if event.get("type") == "response.completed":
                            terminal = event["response"]
                        elif event.get("type") in ("response.failed", "error"):
                            raise ProviderError(redact(json.dumps(event), [cfg.api_key])[:1200])
            if terminal is None or terminal.get("status") not in (None, "completed"):
                raise ProviderError("Missing completed Responses event or truncated output")
        except (requests.RequestException, ValueError) as exc:
            raise ProviderError(redact(f"{type(exc).__name__}: {exc}", [cfg.api_key])) from None
        finally:
            # Keep tool/usage protocol evidence; omit hidden reasoning summaries.
            clean = [e for e in events if "reasoning" not in e.get("type", "")]
            write_json(log_dir / "events.json", json.loads(redact(json.dumps(clean), [cfg.api_key])))
        safe_terminal = json.loads(redact(json.dumps(terminal), [cfg.api_key]))
        write_json(log_dir / "response.json", safe_terminal)
        output = terminal.get("output", [])
        text = "".join(c.get("text", "") for item in output if item.get("type") == "message"
                       for c in item.get("content", []) if c.get("type") == "output_text")
        return {"text": text, "output": output, "usage": terminal.get("usage"),
                "elapsed_seconds": time.monotonic() - started, "reported_model": terminal.get("model"),
                "cost": None}

def parse_candidate(text):
    from .compiler import normalize_candidate
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return normalize_candidate(json.loads(text))
