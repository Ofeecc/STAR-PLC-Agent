from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict
from pathlib import Path

from .common import ROOT, now, read_json, redact, write_json
from .compiler import _kill_tree
from .config import Settings
from .harness import CODE_CONTRACT, empty_result, task_prompt
from .llm import ResponsesClient, parse_candidate
from .mcp_server import CANDIDATE_SCHEMA, dispatch
from .task_view import agent_view


def toml_string(value):
    return json.dumps(str(value), ensure_ascii=False)


def _extract_tool_calls(resp: dict) -> list[tuple[str | None, str, dict]]:
    calls = []
    # 1. tool_calls attribute (OpenAI style)
    if "tool_calls" in resp and isinstance(resp["tool_calls"], list):
        for tc in resp["tool_calls"]:
            cid = tc.get("id") or tc.get("call_id")
            fn = tc.get("function", tc)
            name = fn.get("name")
            args = fn.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            if name:
                calls.append((cid, name, args))
    # 2. output array (Responses API style)
    for item in resp.get("output", []):
        if not isinstance(item, dict):
            continue
        itype = item.get("type")
        if itype in ("function_call", "tool_call"):
            cid = item.get("call_id") or item.get("id")
            name = item.get("name") or item.get("function", {}).get("name")
            args = item.get("arguments") or item.get("function", {}).get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            if name:
                calls.append((cid, name, args))
    return calls


def run_baseline(
    task: dict,
    model: str,
    workspace: Path | str,
    settings: Settings,
    condition: str = "E1",
    driver: str = "codex_cli",
    client=None,
    backend=None,
    spec_visible: bool = True,
    config_path: str | None = None,
) -> dict:
    if driver not in ("codex_cli", "claude_code", "deepseek_harness"):
        raise ValueError(f"Unsupported baseline driver: {driver}")

    workspace = Path(workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    agent_dir = workspace / "agent"
    trusted = workspace / "compiler_records"
    agent_dir.mkdir(parents=True, exist_ok=True)
    trusted.mkdir(parents=True, exist_ok=True)
    snapshot = asdict(settings)
    snapshot.pop('api_key', None)
    write_json(workspace / 'runtime_config.json', snapshot)

    result = empty_result(task, condition, model, driver)
    result["completed_agent_turns"] = 0
    if driver in ("codex_cli", "claude_code"):
        result["llm_calls"] = None

    # Strict Zero-Leakage: provide only sanitized agent_view to agent and prompts
    view = agent_view(task, spec_visible=spec_visible)
    write_json(workspace / "task.json", view)
    write_json(agent_dir / "task.json", view)

    started = time.monotonic()

    prompt = (
        CODE_CONTRACT
        + "\nYou are the existing coding-agent baseline. The complete task is supplied below. "
        + "Use the supplied compiler and simulation tools directly; shell commands are unnecessary for this task. "
        + f"Use compile_st to compile each candidate. Maximum {settings.max_repairs + 1} total compiler calls. "
        + f"Use simulate_st to simulate candidates against your test cases. Maximum {settings.max_simulations} total simulation calls. "
        + "After compilation errors or simulation failures, repair and retest within these limits. "
        + "Stop on successful verification or infrastructure failure. "
        + "Do not inspect other directories, environment variables, API credentials, reference code, or other runs. "
        + "Save the exact final submitted source to candidate.json. "
        + "Return a concise status; raw trusted compiler and simulation evidence will be used for evaluation.\nTASK\n"
        + task_prompt(view)
    )
    (agent_dir / "prompt.txt").write_text(prompt, encoding="utf-8")

    if driver == "deepseek_harness":
        if client is None:
            client = ResponsesClient(settings)

        tools = [
            {
                "type": "function",
                "name": "compile_st",
                "description": f"Compile FB_Task with CODESYS compiler. At most {settings.max_repairs + 1} attempts.",
                "parameters": {
                    "type": "object",
                    "properties": {"source": CANDIDATE_SCHEMA},
                    "required": ["source"],
                },
            },
            {
                "type": "function",
                "name": "simulate_st",
                "description": f"Simulate FB_Task against test cases. At most {settings.max_simulations} attempts.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source": CANDIDATE_SCHEMA,
                        "cases": {"type": "array", "items": {"type": "object"}},
                    },
                    "required": ["source", "cases"],
                },
            },
        ]

        messages = [{"role": "user", "content": prompt}]
        max_turns = min(settings.max_llm_calls, 20)

        for turn in range(max_turns):
            if time.monotonic() - started > settings.task_timeout:
                result["status"], result["reason"] = "TIMEOUT", "Task timeout"
                break

            turn_dir = workspace / f"turn_{turn:02d}"
            try:
                resp = client.respond(
                    model=model,
                    input_items=messages,
                    log_dir=turn_dir,
                    tools=tools,
                )
            except Exception as exc:
                result["status"], result["reason"] = "TOOL_ERROR", redact(str(exc), [settings.api_key])
                break

            result["llm_calls"] = (result.get("llm_calls") or 0) + 1
            if resp.get("usage"):
                result["usage"].append(resp["usage"])
            result["completed_agent_turns"] += 1

            tool_calls = _extract_tool_calls(resp)
            if not tool_calls:
                if resp.get("text"):
                    try:
                        cand = parse_candidate(resp["text"])
                        if cand and not (workspace / "final_candidate.json").exists():
                            write_json(workspace / "final_candidate.json", cand)
                    except Exception:
                        pass
                break

            # Preserve the Responses output items once, including all parallel calls.
            if resp.get('output'):
                messages.extend(resp['output'])
            else:
                messages.extend({'type':'function_call', 'call_id':cid, 'name':name,
                                 'arguments':json.dumps(arguments)} for cid,name,arguments in tool_calls)

            for call_id, name, args in tool_calls:
                result["tool_call_count"] += 1
                mcp_msg = {
                    "method": "tools/call",
                    "params": {"name": name, "arguments": args},
                }
                tool_resp = None
                try:
                    tool_resp = dispatch(mcp_msg, task=task, trusted=trusted, settings=settings, backend=backend)
                    content_text = tool_resp.get("content", [{}])[0].get("text", "")
                except Exception as exc:
                    content_text = json.dumps({"error": str(exc)})

                messages.append({
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": content_text,
                })
                write_json(turn_dir / f"tool_{result['tool_call_count']:02d}.json",
                           {'call_id':call_id,'name':name,'arguments':args,'result':tool_resp or content_text})
                try:
                    tool_status = json.loads(content_text).get('status')
                except (ValueError, AttributeError):
                    tool_status = None
                if tool_status in ('TOOL_ERROR','TIMEOUT'):
                    result['status'], result['reason'] = tool_status, 'Trusted tool infrastructure failed; stopped model requests'
                    break
            if result['status'] in ('TOOL_ERROR','TIMEOUT'):
                break

    elif driver == "codex_cli":
        executable = shutil.which("codex")
        if not executable:
            result["status"], result["reason"] = "TOOL_ERROR", "Codex CLI executable missing"
        else:
            with tempfile.TemporaryDirectory() as mcp_dir:
                trusted_task_path = Path(mcp_dir) / "task.json"
                write_json(trusted_task_path, task)
                args = [
                    sys.executable,
                    "-X",
                    "utf8",
                    "-m",
                    "plc_agent.mcp_server",
                    "--task",
                    str(trusted_task_path),
                    "--trusted",
                    str(trusted),
                ]
                compiler_config = {
                    k: getattr(settings, k)
                    for k in (
                        "codesys_exe",
                        "codesys_profile",
                        "codesys_template",
                        "additional_folder",
                        "compiler_timeout",
                        "max_repairs",
                        "max_simulations",
                    )
                }
                write_json(trusted / "compiler_config.json", compiler_config)
                args += ["--config", str(trusted / "compiler_config.json")]
                server = (
                    "{command="
                    + toml_string(sys.executable)
                    + ",args="
                    + json.dumps(args[1:], ensure_ascii=False)
                    + ",env={PYTHONPATH="
                    + toml_string(ROOT / "src")
                    + "},startup_timeout_sec=30,tool_timeout_sec="
                    + str(settings.compiler_timeout + 30)
                    + "}"
                )
                overrides = [
                    'model_provider="plc_relay"',
                    'model_providers.plc_relay={name="PLC relay",base_url='
                    + toml_string(settings.base_url)
                    + ',env_key="PLC_LLM_API_KEY",wire_api="responses",requires_openai_auth=false}',
                    "model_reasoning_effort=" + toml_string(settings.reasoning_effort),
                    "mcp_servers.plc=" + server,
                    'web_search="disabled"',
                ]
                command = [
                    executable,
                    "exec",
                    "--ignore-user-config",
                    "--ephemeral",
                    "--skip-git-repo-check",
                    "--json",
                    "--color",
                    "never",
                    "--sandbox",
                    "workspace-write",
                    "--cd",
                    str(agent_dir),
                    "--model",
                    model,
                ]
                for item in overrides:
                    command += ["-c", item]

                write_json(
                    workspace / "invocation.json",
                    {
                        "argv": command,
                        "baseline": "unmodified Codex CLI",
                        "differences": [
                            "Baseline controls context and tool selection; self harness uses deterministic control flow.",
                            "Same compiler-call budget and task timeout; Codex internal model calls/tool schemas are not identical.",
                            "Codex does not expose a hard common per-response output-token cap; token usage is reported separately.",
                        ],
                    },
                )
                env = os.environ.copy()
                env["PLC_LLM_API_KEY"] = settings.api_key
                env["PYTHONPATH"] = str(ROOT / "src")
                process = None
                try:
                    with (workspace / "events.private.tmp").open("wb") as out, (
                        workspace / "stderr.private.tmp"
                    ).open("wb") as err:
                        process = subprocess.Popen(
                            command + ["-"],
                            stdin=subprocess.PIPE,
                            stdout=out,
                            stderr=err,
                            env=env,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                        )
                        try:
                            process.communicate(prompt.encode("utf-8"), timeout=settings.task_timeout)
                        except subprocess.TimeoutExpired:
                            _kill_tree(process)
                            result["status"], result["reason"] = "TIMEOUT", "Codex task timeout"
                    for old, new in (("events.private.tmp", "events.jsonl"), ("stderr.private.tmp", "stderr.log")):
                        raw = workspace / old
                        (workspace / new).write_text(
                            redact(raw.read_text(encoding="utf-8", errors="replace"), [settings.api_key]),
                            encoding="utf-8",
                        )
                        raw.unlink()
                    result["baseline_exit_code"] = process.returncode
                    for line in (workspace / "events.jsonl").read_text(encoding="utf-8").splitlines():
                        try:
                            event = json.loads(line)
                        except ValueError:
                            continue
                        if event.get("type") == "turn.completed":
                            result["usage"].append(event.get("usage"))
                            result["completed_agent_turns"] += 1
                        if event.get("type") == "item.completed" and event.get("item", {}).get("type") in (
                            "command_execution",
                            "mcp_tool_call",
                            "web_search",
                            "file_change",
                        ):
                            result["tool_call_count"] += 1
                except (OSError, subprocess.SubprocessError) as exc:
                    result["status"], result["reason"] = "TOOL_ERROR", redact(str(exc), [settings.api_key])

    elif driver == "claude_code":
        executable = shutil.which("claude")
        if not executable:
            result["status"], result["reason"] = "TOOL_ERROR", "Claude CLI executable missing"
        else:
            compiler_config = {
                k: getattr(settings, k)
                for k in (
                    "codesys_exe",
                    "codesys_profile",
                    "codesys_template",
                    "additional_folder",
                    "compiler_timeout",
                    "max_repairs",
                    "max_simulations",
                )
            }
            with tempfile.TemporaryDirectory() as mcp_dir:
                trusted_task_path = Path(mcp_dir) / "task.json"
                write_json(trusted_task_path, task)
                write_json(trusted / "compiler_config.json", compiler_config)
                mcp_config = {
                    "mcpServers": {
                        "plc": {
                            "command": sys.executable,
                            "args": [
                                "-X",
                                "utf8",
                                "-m",
                                "plc_agent.mcp_server",
                                "--task",
                                str(trusted_task_path),
                                "--trusted",
                                str(trusted),
                                "--config",
                                str(trusted / "compiler_config.json"),
                            ],
                            "env": {"PYTHONPATH": str(ROOT / "src")},
                        }
                    }
                }
                write_json(agent_dir / ".mcp.json", mcp_config)
                command = [executable, "--dangerously-skip-permissions", "-p", prompt]
                env = os.environ.copy()
                env["PLC_LLM_API_KEY"] = settings.api_key
                env["PYTHONPATH"] = str(ROOT / "src")
                try:
                    with (workspace / "events.private.tmp").open("wb") as out, (
                        workspace / "stderr.private.tmp"
                    ).open("wb") as err:
                        process = subprocess.Popen(
                            command,
                            stdin=subprocess.PIPE,
                            stdout=out,
                            stderr=err,
                            env=env,
                            cwd=str(agent_dir),
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                        )
                        try:
                            process.communicate(timeout=settings.task_timeout)
                        except subprocess.TimeoutExpired:
                            _kill_tree(process)
                            result["status"], result["reason"] = "TIMEOUT", "Claude task timeout"
                    result["baseline_exit_code"] = process.returncode
                except (OSError, subprocess.SubprocessError) as exc:
                    result["status"], result["reason"] = "TOOL_ERROR", redact(str(exc), [settings.api_key])

    # Shared Evaluation & Record Parsing:
    attempts = [read_json(p) for p in sorted(trusted.glob("compile_*/compile_result.json"))]
    result["compilation_attempts"] = attempts
    result["compiler_call_count"] = len(attempts)
    result["repair_attempts"] = max(0, len(attempts) - 1)

    sim_attempts = [read_json(p) for p in sorted(trusted.glob("sim_*/simulation_result.json"))]
    result["simulation_call_count"] = len(sim_attempts)

    if attempts and result['status'] not in ('TOOL_ERROR','TIMEOUT'):
        if attempts[0].get("status") in ("PASS", "COMPILE_FAIL"):
            result["first_pass_compiled"] = attempts[0].get("success", False)
        last = attempts[-1]
        if last.get("success"):
            result["final_compiled"] = True
            result["status"], result["reason"] = "UNVERIFIED", "CODESYS compiled; PLC functional execution not yet evaluated"
            candidate_files = sorted(trusted.glob("compile_*/candidate.json"))
            if candidate_files:
                shutil.copy2(candidate_files[-1], workspace / "final_candidate.json")
                result["final_candidate"] = read_json(candidate_files[-1])
        elif last.get("status") == "COMPILE_FAIL":
            result["final_compiled"], result["status"] = False, "COMPILE_FAIL"
            candidate_files = sorted(trusted.glob("compile_*/candidate.json"))
            if candidate_files:
                shutil.copy2(candidate_files[-1], workspace / "final_candidate.json")
                result["final_candidate"] = read_json(candidate_files[-1])
        else:
            result["status"], result["reason"] = last.get("status"), last.get("infrastructure_error")
    elif result["status"] not in ("TIMEOUT", "TOOL_ERROR"):
        result["status"], result["reason"] = "TOOL_ERROR", f"{driver} did not invoke trusted compiler tool"

    if (workspace / "final_candidate.json").exists() and result.get("final_candidate") is None:
        try:
            result["final_candidate"] = read_json(workspace / "final_candidate.json")
        except Exception:
            pass

    result["elapsed_seconds"] = time.monotonic() - started
    result["finished_utc"] = now()
    write_json(workspace / "result.json", result)
    return result


def run_codex(task, model, workspace, settings, condition="E1", config_path=None):
    return run_baseline(
        task=task,
        model=model,
        workspace=workspace,
        settings=settings,
        condition=condition,
        driver="codex_cli",
        config_path=config_path,
    )
