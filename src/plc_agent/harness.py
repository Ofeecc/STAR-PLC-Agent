from __future__ import annotations
import json
import time
from dataclasses import asdict, replace
from pathlib import Path
from .common import digest, now, write_json
from .compiler import compile_st, actionable_diagnostics
from .llm import ProviderError, parse_candidate

CODE_CONTRACT = """Return ONLY a JSON object with declaration, implementation, supporting_objects.
declaration is CODESYS FUNCTION_BLOCK FB_Task followed by all VAR sections; omit END_FUNCTION_BLOCK.
implementation is the ST body alone. supporting_objects is a list of helper DUT/POU objects, each with
name, kind (DUT/FUNCTION/FUNCTION_BLOCK), declaration, implementation; functions need return_type.
Keep exact task interface names/types and implement all behavior. Define referenced DUTs. No Markdown.
Do not change requirements or use reference answers. Standard library is available in the project.
The target is CODESYS 3.5 ST. Compilation is offline; do not contact physical equipment.
"""

def requirement_analysis(task):
    return {"pou_type": "FUNCTION_BLOCK", "pou_name": "FB_Task", "interface": task["interface"],
            "initial_conditions": task["initial_conditions"], "scan_semantics": task["scan_semantics"],
            "safety_priority": task["safety_priority"], "assumptions": task["assumptions"],
            "formal_properties": task["ltl"], "atomic_propositions": task["atomic_propositions"],
            "supporting_types": task.get("supporting_types", task.get("data_types", [])),
            "specification_version": task.get("specification_version", "1"),
            "specification_contract": task.get("specification_contract", {})}

def task_prompt(task):
    # Both frameworks receive the same source/spec/tests. No other task is visible.
    return json.dumps(task, ensure_ascii=False, indent=2)

def empty_result(task, condition, model, framework, reason=None):
    return {"schema_version": 1, "task_id": task["id"], "task_sha256": digest(task),
            "condition": condition, "framework": framework, "model": model,
            "status": "NOT_RUN", "reason": reason, "started_utc": now(), "finished_utc": None,
            "first_pass_compiled": None, "final_compiled": None, "repair_attempts": 0,
            "compilation_attempts": [], "compiler_call_count": 0, "tool_call_count": 0, "llm_calls": 0, "usage": [],
            "api_cost": None, "elapsed_seconds": 0, "functional": {"status": "NOT_RUN", "evidence": None,
                "planned_cases": len(task["tests"]), "evaluated_cases": 0, "passed_cases": 0,
                "evaluated_steps": 0, "passed_steps": 0}}

def run_harness(task, model, workspace, client, settings, condition="E3"):
    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=False)
    result = empty_result(task, condition, model, "self_harness")
    started = time.monotonic()
    write_json(workspace / "task.json", task)
    write_json(workspace / "analysis.json", requirement_analysis(task))
    snapshot = asdict(settings)
    snapshot.pop("api_key", None)
    write_json(workspace / "runtime_config.json", snapshot)
    prompt = task_prompt(task)
    current = None
    history = []
    try:
        for attempt in range(settings.max_repairs + 1):
            if time.monotonic() - started >= settings.task_timeout:
                result["status"], result["reason"] = "TIMEOUT", "Task deadline exhausted"
                break
            messages = [{"role": "developer", "content": CODE_CONTRACT},
                        {"role": "user", "content": "TASK AND SPECIFICATIONS\n" + prompt}]
            if current is not None:
                messages.append({"role": "user", "content": "Focused repair: preserve correct behavior and interface.\n"
                    + "Current code:\n" + json.dumps(current) + "\nCompiler errors:\n" + history[-1]["diagnostics"]
                    + "\nEarlier repair summaries:\n" + json.dumps(history[:-1])})
            remaining = max(1, settings.task_timeout - (time.monotonic() - started))
            reply = client.respond(model, messages, workspace / f"llm_{attempt:02d}", timeout=remaining)
            result["llm_calls"] += 1
            result["usage"].append(reply["usage"])
            # Malformed code is an agent-output failure, never a real compiler failure.
            current = parse_candidate(reply["text"])
            write_json(workspace / f"version_{attempt:02d}.json", current)
            remaining = settings.task_timeout - (time.monotonic() - started)
            if remaining <= 0:
                result["status"], result["reason"] = "TIMEOUT", "Task deadline expired after generation"
                break
            compile_settings = replace(settings, compiler_timeout=max(1, min(settings.compiler_timeout, int(remaining))))
            compiled = compile_st(task, current, workspace / f"compile_{attempt:02d}", compile_settings)
            result["tool_call_count"] += 1
            result["compiler_call_count"] += 1
            result["compilation_attempts"].append(asdict(compiled))
            result["repair_attempts"] = attempt
            if attempt == 0 and compiled.status in ("PASS", "COMPILE_FAIL"):
                result["first_pass_compiled"] = compiled.success
            if compiled.success:
                result["final_compiled"] = True
                result["status"] = "UNVERIFIED"
                result["reason"] = "CODESYS compiled; PLC functional execution remains to be evaluated"
                write_json(workspace / "final_candidate.json", current)
                break
            if compiled.status in ("TOOL_ERROR", "TIMEOUT"):
                result["status"], result["reason"] = compiled.status, compiled.infrastructure_error
                break
            result["status"], result["final_compiled"] = "COMPILE_FAIL", False
            history.append({"attempt": attempt, "diagnostics": actionable_diagnostics(compiled)})
    except ProviderError as exc:
        result["status"], result["reason"] = "TOOL_ERROR", str(exc)
    except OSError as exc:
        result["status"], result["reason"] = "TOOL_ERROR", "Local infrastructure: " + str(exc)
    except (ValueError, TypeError, KeyError) as exc:
        result["status"], result["reason"] = "UNVERIFIED", "Invalid model output: " + str(exc)
    finally:
        result["elapsed_seconds"] = time.monotonic() - started
        result["finished_utc"] = now()
        write_json(workspace / "result.json", result)
    return result
