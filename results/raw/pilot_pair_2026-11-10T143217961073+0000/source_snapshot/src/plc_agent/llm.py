from __future__ import annotations

import json
import time
from pathlib import Path

import requests

from .common import digest, now, redact, write_json


class ProviderError(RuntimeError):
    pass

class ResponsesClient:
    """Small Responses API client; no assumed upstream model identity or prices."""
    def __init__(self, settings):
        self.settings = settings
        self.request_count = 0
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
        log_dir = Path(log_dir)
        def safe(value):
            return json.loads(redact(json.dumps(value, ensure_ascii=False), [cfg.api_key]))
        def journal(event, **fields):
            log_dir.parent.mkdir(parents=True, exist_ok=True)
            entry = safe({'utc':now(), 'event':event, 'call_dir':log_dir.name, **fields})
            with (log_dir.parent / 'model_calls.jsonl').open('a',encoding='utf-8') as stream:
                stream.write(json.dumps(entry,ensure_ascii=False)+'\n')
        # Every request retains its complete application-provided context and tool schemas.
        # UTF-8 bytes are a conservative proxy, not the provider's tokenizer/count.
        input_bound = len(json.dumps({'input':input_items,'tools':tools or []},ensure_ascii=False).encode('utf-8')) + 256
        context = {'reasoning_effort_requested':cfg.reasoning_effort,
                   'local_context_budget':cfg.context_window_tokens,
                   'input_token_upper_bound':input_bound,
                   'count_method':'UTF8_BYTES_PLUS_256_CONSERVATIVE_PROXY_NOT_PROVIDER_TOKENIZER',
                   'output_tokens_reserved':payload['max_output_tokens'],
                   'input_sha256':digest(input_items), 'history_truncated':False}
        write_json(log_dir / 'request.json', safe(payload))
        write_json(log_dir / 'context.json', safe(context))
        if input_bound + payload['max_output_tokens'] > cfg.context_window_tokens:
            journal('context_budget_rejected', **context)
            raise ProviderError('Local context budget exceeded; no request sent and no history truncated')
        if self.request_count >= cfg.max_llm_calls:
            journal('request_budget_rejected', maximum=cfg.max_llm_calls)
            raise ProviderError('Per-experiment model request budget exhausted')
        started = time.monotonic()
        events, terminal = [], None
        self.request_count += 1
        journal('request_started', model=model, request_number=self.request_count, **context)
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
                        if event.get("type") in ("response.completed", "response.incomplete", "response.failed"):
                            terminal = event["response"]
                        if event.get("type") in ("response.failed", "error"):
                            raise ProviderError(redact(json.dumps(event), [cfg.api_key])[:1200])
            if terminal is None:
                raise ProviderError("Missing terminal Responses event")
            if terminal.get("status") not in (None, "completed"):
                raise ProviderError('Responses ' + str(terminal.get('status')) + ': ' + json.dumps(terminal.get('incomplete_details') or terminal.get('error')))
        except ProviderError as exc:
            write_json(log_dir / 'error.json', safe({'error':str(exc)}))
            journal('request_failed', error=str(exc), elapsed_seconds=time.monotonic()-started,
                    usage=(terminal or {}).get('usage'), response_status=(terminal or {}).get('status'))
            raise
        except (requests.RequestException, ValueError) as exc:
            write_json(log_dir / 'error.json', safe({'error':str(exc)}))
            journal('request_failed', error=str(exc), elapsed_seconds=time.monotonic()-started)
            raise ProviderError(redact(f"{type(exc).__name__}: {exc}", [cfg.api_key])) from None
        finally:
            # Retain the protocol the provider actually exposes, including visible summaries.
            write_json(log_dir / "events.json", safe(events))
            if terminal is not None:
                write_json(log_dir / 'response.json', safe(terminal))
        journal('request_completed', elapsed_seconds=time.monotonic()-started,
                usage=terminal.get('usage'), reported_model=terminal.get('model'))
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
