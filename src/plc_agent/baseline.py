from __future__ import annotations
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from .common import ROOT, now, read_json, redact, write_json
from .compiler import _kill_tree
from .harness import CODE_CONTRACT, empty_result, task_prompt

def toml_string(value):
    return json.dumps(str(value), ensure_ascii=False)

def run_codex(task, model, workspace, settings, condition="E1", config_path=None):
    workspace = Path(workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=False)
    agent_dir, trusted = workspace / "agent", workspace / "compiler_records"
    agent_dir.mkdir(); trusted.mkdir()
    result = empty_result(task, condition, model, "codex_cli")
    result["llm_calls"] = None  # Codex turns contain an unexposed number of HTTP calls.
    result["completed_agent_turns"] = 0
    write_json(workspace / "task.json", task)
    write_json(agent_dir / "task.json", task)
    started = time.monotonic()
    executable = shutil.which("codex")
    if not executable:
        result["status"], result["reason"] = "TOOL_ERROR", "Codex CLI executable missing"
    else:
        args = [sys.executable, "-X", "utf8", "-m", "plc_agent.mcp_server", "--task", str(workspace / "task.json"),
                "--trusted", str(trusted)]
        # Freeze compiler configuration; MCP environment inheritance varies by CLI.
        compiler_config = {k: getattr(settings, k) for k in ("codesys_exe", "codesys_profile", "codesys_template",
            "additional_folder", "compiler_timeout", "max_repairs")}
        write_json(trusted / "compiler_config.json", compiler_config)
        args += ["--config", str(trusted / "compiler_config.json")]
        server = "{command=" + toml_string(sys.executable) + ",args=" + json.dumps(args[1:], ensure_ascii=False)
        server += ",env={PYTHONPATH=" + toml_string(ROOT / "src") + "},startup_timeout_sec=30,tool_timeout_sec=" + str(settings.compiler_timeout + 30) + "}"
        overrides = ["model_provider=\"plc_relay\"", "model_providers.plc_relay={name=\"PLC relay\",base_url="
            + toml_string(settings.base_url) + ",env_key=\"PLC_LLM_API_KEY\",wire_api=\"responses\",requires_openai_auth=false}",
            "model_reasoning_effort=" + toml_string(settings.reasoning_effort), "mcp_servers.plc=" + server,
            "web_search=\"disabled\""]
        command = [executable, "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check",
                   "--json", "--color", "never", "--sandbox", "workspace-write", "--cd", str(agent_dir), "--model", model]
        for item in overrides:
            command += ["-c", item]
        prompt = (CODE_CONTRACT + "\nYou are the existing Codex coding-agent baseline. The complete task is supplied below. "
            + "Use the supplied compiler MCP tool directly; shell commands are unnecessary for this task. "
            + f"Use the plc.compile_st MCP tool to compile each candidate. Maximum {settings.max_repairs + 1} total compiler calls. "
            + "After compilation errors, repair and recompile within this limit. Stop on successful compilation or infrastructure failure. "
            + "Do not inspect other directories, environment variables, API credentials, reference code, or other runs. "
            + "Save the exact final submitted source to candidate.json. Do not claim functional testing was performed. "
            + "Return a concise status; raw trusted compiler evidence will be used for evaluation.\nTASK\n" + task_prompt(task))
        (agent_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
        write_json(workspace / "invocation.json", {"argv": command, "baseline": "unmodified Codex CLI",
            "differences": ["Baseline controls context and tool selection; self harness uses deterministic control flow.",
                "Same compiler-call budget and task timeout; Codex internal model calls/tool schemas are not identical.",
                "Codex does not expose a hard common per-response output-token cap; token usage is reported separately."]})
        env = os.environ.copy()
        env["PLC_LLM_API_KEY"] = settings.api_key
        env["PYTHONPATH"] = str(ROOT / "src")
        process = None
        try:
            with (workspace / "events.private.tmp").open("wb") as out, (workspace / "stderr.private.tmp").open("wb") as err:
                process = subprocess.Popen(command + ["-"], stdin=subprocess.PIPE, stdout=out, stderr=err, env=env,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
                try:
                    process.communicate(prompt.encode("utf-8"), timeout=settings.task_timeout)
                except subprocess.TimeoutExpired:
                    _kill_tree(process)
                    result["status"], result["reason"] = "TIMEOUT", "Codex task timeout"
            for old, new in (("events.private.tmp", "events.jsonl"), ("stderr.private.tmp", "stderr.log")):
                raw = workspace / old
                (workspace / new).write_text(redact(raw.read_text(encoding="utf-8", errors="replace"), [settings.api_key]), encoding="utf-8")
                raw.unlink()
            attempts = [read_json(p) for p in sorted(trusted.glob("compile_*/compile_result.json"))]
            completion_timeout = result["status"] == "TIMEOUT"
            result["compilation_attempts"], result["compiler_call_count"] = attempts, len(attempts)
            result["repair_attempts"] = max(0, len(attempts) - 1)
            if attempts:
                if attempts[0]["status"] in ("PASS", "COMPILE_FAIL"):
                    result["first_pass_compiled"] = attempts[0]["success"]
                last = attempts[-1]
                if last["success"]:
                    result["final_compiled"] = True
                    result["status"], result["reason"] = "UNVERIFIED", "CODESYS compiled; PLC functional execution not yet evaluated"
                    # The last tool-submitted candidate, not an unchecked final answer, is evaluated.
                    shutil.copy2(sorted(trusted.glob("compile_*/candidate.json"))[-1], workspace / "final_candidate.json")
                elif last["status"] == "COMPILE_FAIL":
                    result["final_compiled"], result["status"] = False, "COMPILE_FAIL"
                else:
                    result["status"], result["reason"] = last["status"], last["infrastructure_error"]
            elif result["status"] != "TIMEOUT":
                result["status"], result["reason"] = "TOOL_ERROR", "Codex did not invoke trusted compiler tool"
            result["baseline_exit_code"] = process.returncode
            for line in (workspace / "events.jsonl").read_text(encoding="utf-8").splitlines():
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if event.get("type") == "turn.completed":
                    result["usage"].append(event.get("usage"))
                    result["completed_agent_turns"] += 1
                if event.get("type") == "item.completed" and event.get("item", {}).get("type") in ("command_execution", "mcp_tool_call", "web_search", "file_change"):
                    result["tool_call_count"] += 1
            if completion_timeout:
                result["status"], result["reason"] = "TIMEOUT", "Codex task timeout; compilation outcomes retained separately"
            if process.returncode not in (None, 0) and result["status"] != "TIMEOUT":
                result["status"], result["reason"] = "TOOL_ERROR", "Codex process exited abnormally; retained compilation outcomes separately"
        except (OSError, subprocess.SubprocessError) as exc:
            result["status"], result["reason"] = "TOOL_ERROR", redact(str(exc), [settings.api_key])
    result["elapsed_seconds"] = time.monotonic() - started
    result["finished_utc"] = now()
    write_json(workspace / "result.json", result)
    return result
