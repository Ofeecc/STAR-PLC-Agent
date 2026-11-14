"""Budgeted local Responses transport for an otherwise unmodified Codex CLI.

Logs exactly the CLI's requests and provider responses; it does not plan, edit
code, choose tools, or repair candidates. The real API credential stays here.
"""
from __future__ import annotations

import json
import secrets
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import requests

from .common import digest, now, redact, write_json


class CodexTransport:
    def __init__(self, settings, model, log_dir):
        self.settings, self.model, self.log_dir = settings, model, Path(log_dir)
        self.token = secrets.token_urlsafe(32)
        self.request_count, self.total_tokens, self.usage = 0, 0, []
        self.started = time.monotonic()
        self.session = requests.Session()
        owner = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                # Codex queries its provider's model catalogue before starting
                # a run. Keep that lookup local and deterministic: the actual
                # requested model is still sent through the authenticated POST
                # relay below, so this does not make an extra upstream call.
                if self.path.split("?", 1)[0].rstrip("/") != "/v1/models":
                    return self.error(404, "Only the local model catalogue is enabled")
                # Codex's model manager expects a `models` catalogue (rather
                # than the OpenAI `/v1/models` `data` shape). An empty catalogue
                # is sufficient here: the caller already selected the exact
                # configured model ID and unknown IDs use Codex fallback
                # metadata, while the actual request still goes through the
                # authenticated Responses relay.
                body = json.dumps({"models": []}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def error(self, code, message):
                body = json.dumps({"error": {"message": message, "type": "local_budget_or_transport"}}).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_POST(self):
                if self.headers.get("Authorization") != "Bearer " + owner.token:
                    return self.error(401, "Invalid local transport credential")
                if self.path.split("?")[0].rstrip("/") != "/v1/responses":
                    return self.error(404, "Only the Responses endpoint is enabled")
                try:
                    length = int(self.headers.get("Content-Length", "0"))
                    if length < 1 or length > 8_000_000:
                        return self.error(413, "Invalid request size")
                    payload = json.loads(self.rfile.read(length))
                    context = owner.prepare(payload)
                except (ValueError, TypeError) as exc:
                    owner.journal("request_rejected", reason=str(exc))
                    return self.error(429, str(exc))
                call_dir = owner.log_dir / f"request_{owner.request_count:03d}"
                owner.request_count += 1
                write_json(call_dir / "request.json", owner.safe(payload))
                write_json(call_dir / "context.json", context)
                owner.journal("request_started", request_number=owner.request_count, input_sha256=context["input_sha256"])
                raw = bytearray()
                sent_headers = False
                try:
                    remaining = max(1, owner.settings.task_timeout - (time.monotonic() - owner.started))
                    with owner.session.post(owner.settings.base_url.rstrip("/") + "/responses", json=payload,
                                            headers={"Authorization": "Bearer " + owner.settings.api_key,
                                                     "Content-Type": "application/json", "Accept": "text/event-stream"},
                                            stream=True, timeout=(20, min(owner.settings.llm_timeout, remaining))) as upstream:
                        self.send_response(upstream.status_code)
                        self.send_header("Content-Type", upstream.headers.get("Content-Type", "text/event-stream"))
                        self.send_header("Connection", "close")
                        self.end_headers()
                        sent_headers = True
                        for chunk in upstream.iter_content(chunk_size=1024):
                            if chunk:
                                raw.extend(chunk)
                                self.wfile.write(chunk)
                                self.wfile.flush()
                        self.close_connection = True
                except (requests.RequestException, OSError) as exc:
                    owner.journal("transport_error", reason=redact(str(exc), (owner.settings.api_key, owner.token)))
                    if not sent_headers:
                        self.error(502, "Upstream transport failed; see retained transport journal")
                finally:
                    owner.record_response(call_dir, raw, context)

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.base_url = f"http://127.0.0.1:{self.server.server_port}/v1"

    def safe(self, value):
        return json.loads(redact(json.dumps(value, ensure_ascii=False), (self.settings.api_key, self.token)))

    def journal(self, event, **fields):
        self.log_dir.mkdir(parents=True, exist_ok=True)
        with (self.log_dir / "model_calls.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(self.safe({"utc": now(), "event": event, **fields}), ensure_ascii=False) + "\n")

    def prepare(self, payload):
        cfg = self.settings
        if payload.get("model") != self.model:
            raise ValueError("CLI requested a different model")
        if cfg.max_llm_calls and self.request_count >= cfg.max_llm_calls:
            raise ValueError("Per-task request safety limit reached")
        if time.monotonic() - self.started >= cfg.task_timeout:
            raise ValueError("Task timeout reached")
        # Transport-level safety caps are recorded explicitly as a protocol difference.
        payload["max_output_tokens"] = min(int(payload.get("max_output_tokens") or cfg.max_output_tokens), cfg.max_output_tokens)
        payload["reasoning"] = dict(payload.get("reasoning") or {}, effort=cfg.reasoning_effort)
        payload["store"], payload["stream"] = False, True
        upper = len(json.dumps(payload, ensure_ascii=False).encode("utf-8")) + 256
        reserve = upper + payload["max_output_tokens"]
        if reserve > cfg.context_window_tokens:
            raise ValueError("Local context safety limit reached; no history truncated")
        if cfg.max_total_tokens and self.total_tokens + reserve > cfg.max_total_tokens:
            raise ValueError("Per-task total token safety limit reached")
        return {"reasoning_effort_requested": cfg.reasoning_effort,
                "local_context_budget": cfg.context_window_tokens, "input_token_upper_bound": upper,
                "output_tokens_reserved": payload["max_output_tokens"], "input_sha256": digest(payload),
                "count_method": "UTF8_BYTES_PLUS_256_CONSERVATIVE_PROXY_NOT_PROVIDER_TOKENIZER", "history_truncated": False}

    def record_response(self, call_dir, raw, context):
        terminal = None
        decoded = bytes(raw).decode("utf-8", errors="replace")
        Path(call_dir).mkdir(parents=True, exist_ok=True)
        (Path(call_dir) / "response.sse").write_text(redact(decoded, (self.settings.api_key, self.token)), encoding="utf-8")
        for line in decoded.splitlines():
            if not line.startswith("data:"):
                continue
            try:
                item = json.loads(line[5:].strip())
            except ValueError:
                continue
            if item.get("type") in ("response.completed", "response.incomplete", "response.failed"):
                terminal = item.get("response", {})
        usage = (terminal or {}).get("usage")
        if usage:
            self.usage.append(usage)
            consumed = int(usage.get("total_tokens") or (int(usage.get("input_tokens", 0)) + int(usage.get("output_tokens", 0))))
        else:
            consumed = context["input_token_upper_bound"] + context["output_tokens_reserved"]
        self.total_tokens += consumed
        write_json(Path(call_dir) / "response.json", self.safe({"response": terminal, "usage": usage,
                   "accounted_tokens": consumed, "usage_accounting": "PROVIDER" if usage else "CONSERVATIVE_RESERVE_USAGE_MISSING"}))
        self.journal("request_finished", usage=usage, accounted_tokens=consumed)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.server.shutdown()
        self.server.server_close()
        self.session.close()
        self.thread.join(timeout=2)
