"""One tiny, real tool-use compatibility run per selected relay model.

No compiler and no benchmark tasks are used. Requires --run; existing records
are reused rather than silently spending another API call. Credentials remain
in process memory/environment and are redacted before any log is written.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import tomllib
import uuid

from plc_agent.common import ROOT, now, read_json, redact, write_json
from plc_agent.compiler import _kill_tree
from plc_agent.config import Settings

MODELS = ("deepseek-v4.1-flash", "kimi-k3.1-pro")


def toml_string(value):
    return json.dumps(str(value), ensure_ascii=False)


def event_items(events):
    return [event.get("item", {}) for event in events if event.get("type") == "item.completed"]


def probe(executable, settings, model):
    folder = ROOT / "results/raw/codex_compatibility" / model
    summary_path = folder / "summary.json"
    if summary_path.exists():
        return read_json(summary_path)
    folder.mkdir(parents=True, exist_ok=True)
    agent_dir = folder / "agent"
    agent_dir.mkdir(exist_ok=True)
    nonce = "PLC_CODEX_PROBE_" + uuid.uuid4().hex
    (agent_dir / "probe.txt").write_text(nonce + "\n", encoding="utf-8")
    provider = ('{name="PLC relay compatibility probe",base_url=' + toml_string(settings.base_url)
                + ',env_key="PLC_LLM_API_KEY",wire_api="responses",requires_openai_auth=false,'
                + 'request_max_retries=0,stream_max_retries=0,stream_idle_timeout_ms=60000}')
    overrides = ["model_provider=\"plc_probe\"", "model_providers.plc_probe=" + provider,
                 "model_reasoning_effort=\"low\"", "web_search=\"disabled\""]
    # Validate all generated TOML locally before invoking a paid model.
    for override in overrides:
        tomllib.loads(override)
    command = [executable, "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check",
               "--json", "--color", "never", "--sandbox", "read-only", "--cd", str(agent_dir),
               "--model", model]
    for override in overrides:
        command.extend(["-c", override])
    prompt = ("This is a tiny local-file tool compatibility probe. Use exactly one local shell tool command "
              "to read the UTF-8 file probe.txt in the current directory. Do not inspect any other file, "
              "environment variable, credential, or directory. Do not write files or use network/web tools. "
              "After reading, return only the exact file content and stop.")
    write_json(folder / "invocation.json", {"argv": command, "prompt": prompt, "reasoning_effort": "low",
                                           "task_timeout_seconds": 120, "retry_settings": "request=0, stream=0"})
    result = {"kind": "CODEX_TOOL_COMPATIBILITY_PROBE", "requested_model": model, "reported_model": None,
              "upstream_identity_verified": False, "started_utc": now(), "status": "NOT_RUN",
              "tool_execution_verified": False, "final_content_verified": False,
              "usage": [], "cli_exit_code": None, "elapsed_seconds": None,
              "raw_events": str(folder / "events.jsonl"), "reasoning_effort": "low",
              "actual_codesys_compilation": False, "benchmark_result": False}
    env = os.environ.copy()
    env["PLC_LLM_API_KEY"] = settings.api_key
    env.pop("OPENAI_API_KEY", None)
    env.pop("PLC_API_CONFIG", None)
    started = time.monotonic()
    stdout, stderr = b"", b""
    process = None
    try:
        process = subprocess.Popen(command + ["-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, env=env,
                                   creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        try:
            stdout, stderr = process.communicate(prompt.encode("utf-8"), timeout=120)
        except subprocess.TimeoutExpired:
            _kill_tree(process)
            stdout, stderr = process.communicate(timeout=15)
            result["status"], result["reason"] = "TIMEOUT", "Codex probe exceeded 120 seconds"
        result["cli_exit_code"] = process.returncode
        out = redact(stdout.decode("utf-8", errors="replace"), [settings.api_key])
        err = redact(stderr.decode("utf-8", errors="replace"), [settings.api_key])
        (folder / "events.jsonl").write_text(out, encoding="utf-8")
        (folder / "stderr.log").write_text(err, encoding="utf-8")
        events = []
        for line in out.splitlines():
            try:
                events.append(json.loads(line))
            except ValueError:
                continue
        items = event_items(events)
        commands = [item for item in items if item.get("type") == "command_execution"]
        result["completed_command_count"] = len(commands)
        result["policy_blocked_command_count"] = err.count("rejected: blocked by policy")
        result["model_metadata_fallback"] = "Model metadata for" in out or "fallback model metadata" in err
        result["tool_execution_verified"] = any(item.get("exit_code") == 0 and nonce in item.get("aggregated_output", "")
                                                   for item in commands)
        messages = [item.get("text", "") for item in items if item.get("type") == "agent_message"]
        result["final_content_verified"] = bool(messages) and messages[-1].strip() == nonce
        for event in events:
            if event.get("type") == "turn.completed":
                result["usage"].append(event.get("usage"))
            if isinstance(event.get("model"), str):
                result["reported_model"] = event["model"]
        result["responses_conversation_completed"] = any(event.get("type") == "turn.completed" for event in events)
        if result["status"] != "TIMEOUT":
            if process.returncode == 0 and result["tool_execution_verified"] and result["final_content_verified"]:
                result["status"] = "PASS"
                result["reason"] = "Actual Codex shell-tool execution and subsequent final reply verified"
            else:
                result["status"] = "TOOL_ERROR" if process.returncode else "UNVERIFIED"
                failures = [event for event in events if event.get("type") in ("error", "turn.failed")]
                if result["policy_blocked_command_count"]:
                    result["reason"] = ("Local command execution policy rejected tool commands before execution. "
                                         "The relay conversation completed, but an actual tool-result continuation remains unverified.")
                else:
                    result["reason"] = json.dumps(failures, ensure_ascii=False)[:1600] if failures else err[-1600:]
    except (OSError, subprocess.SubprocessError) as exc:
        result["status"], result["reason"] = "TOOL_ERROR", redact(str(exc), [settings.api_key])
    result["elapsed_seconds"] = time.monotonic() - started
    result["finished_utc"] = now()
    write_json(summary_path, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Authorize the two tiny model-backed CLI runs")
    args = parser.parse_args()
    if not args.run:
        parser.error("Use --run explicitly; this probe makes paid API calls")
    settings = Settings.load()
    if not settings.api_key or not settings.base_url:
        parser.error("Relay credentials/base URL not configured")
    executable = shutil.which("codex")
    if not executable:
        parser.error("Codex CLI missing")
    version = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=15).stdout.strip()
    results = []
    for model in MODELS:
        result = probe(executable, settings, model)
        results.append(result)
        print(json.dumps({"model": model, "status": result["status"],
                          "tool_execution_verified": result["tool_execution_verified"],
                          "elapsed_seconds": result["elapsed_seconds"]}), flush=True)
    summary = {"kind": "CODEX_COMPATIBILITY", "cli_version": version, "created_utc": now(),
               "models": results, "both_models_tool_compatible": all(r["status"] == "PASS" for r in results),
               "limitations": ["This is a read-file tool loop, not a CODESYS benchmark.",
                               "Relay route names and reported IDs do not authenticate upstream identity.",
                               "Responses protocol smoke and actual compiler-tool testing are separate checks.",
                               "Codex turn usage is reported; internal API request count is not exposed by these events."]}
    path = ROOT / "results/summary/codex_compatibility.json"
    write_json(path, summary)
    print(json.dumps({"summary": str(path), "both_models_tool_compatible": summary["both_models_tool_compatible"]}), flush=True)


if __name__ == "__main__":
    main()
