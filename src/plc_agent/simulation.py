"""Actual CODESYS IDE simulation for fixed untimed scalar scan traces.

Each test gets a separate fresh FB instance. An editable PLC_PRG sequencer
assigns fixed inputs, invokes the generated FB exactly once per task scan,
and copies actual sampled inputs and outputs to typed trace arrays. Expected
outputs never appear in the generated test program.
"""
from __future__ import annotations
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import uuid
from .common import ROOT, digest, now, read_json, write_json
from .compiler import codesys_command, _kill_tree, normalize_candidate, stage_ascii_workspace, sync_ascii_artifacts

SCALAR_TYPES = {"BOOL", "BYTE", "WORD", "DWORD", "LWORD", "SINT", "INT", "DINT", "LINT",
                "USINT", "UINT", "UDINT", "ULINT", "REAL", "LREAL"}
INTEGER_TYPES = SCALAR_TYPES - {"BOOL", "REAL", "LREAL"}

def supported_type(type_name):
    value = type_name.strip().upper()
    return value in SCALAR_TYPES or bool(re.fullmatch(r"STRING\([1-9][0-9]*\)", value))

def eligibility(task):
    reasons = []
    for field in task["interface"]:
        if field["direction"] == "IN_OUT":
            reasons.append("Caller-owned IN_OUT/composite storage needs a separate verified adapter")
        if not supported_type(field["type"]):
            reasons.append("Unsupported automatic monitoring type: " + field["type"])
    if any("dt_ms" in step for case in task["tests"] for step in case["steps"]):
        reasons.append("Physical elapsed-time tests require a separately validated clock adapter")
    return sorted(set(reasons))

def st_literal(value, type_name):
    typ = type_name.strip().upper()
    if typ == "BOOL":
        if not isinstance(value, bool):
            raise ValueError("BOOL input requires a JSON Boolean")
        return "TRUE" if value else "FALSE"
    if typ in INTEGER_TYPES:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("Integer input requires a JSON integer")
        return typ + "#" + str(value)
    if typ in ("REAL", "LREAL"):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
            raise ValueError("Real input must be finite")
        text = repr(float(value))
        return typ + "#" + text
    if typ.startswith("STRING("):
        if not isinstance(value, str):
            raise ValueError("STRING input requires a string")
        escaped = value.replace("$", "$$").replace("'", "$'").replace("\r", "$R").replace("\n", "$N")
        return "'" + escaped + "'"
    raise ValueError("Unsupported test input type")

def build_program(task):
    reasons = eligibility(task)
    if reasons:
        raise ValueError("; ".join(reasons))
    fields = task["interface"]
    for field in fields:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", field["name"]):
            raise ValueError("Unexpected IEC field identifier")
    inputs = [v for v in fields if v["direction"] == "INPUT"]
    outputs = [v for v in fields if v["direction"] == "OUTPUT"]
    count = sum(len(case["steps"]) for case in task["tests"])
    if count <= 0:
        raise ValueError("No fixed test steps")
    declarations = ["PROGRAM PLC_PRG", "VAR", " BenchStep : UDINT := 0;", " BenchCalls : UDINT := 0;", " BenchDone : BOOL := FALSE;"]
    declarations += [f" BenchUut{i} : FB_Task;" for i, _ in enumerate(task["tests"])]
    declarations += [f" TraceIn{i} : ARRAY[0..{count - 1}] OF {field['type']};" for i, field in enumerate(inputs)]
    declarations += [f" TraceOut{i} : ARRAY[0..{count - 1}] OF {field['type']};" for i, field in enumerate(outputs)]
    declarations.append("END_VAR")
    body = ["IF NOT BenchDone THEN", " CASE BenchStep OF"]
    steps = []
    step_index = 0
    for case_index, case in enumerate(task["tests"]):
        instance = "BenchUut" + str(case_index)
        for case_step, step in enumerate(case["steps"]):
            body.append(f" {step_index}:")
            for field in inputs:
                body.append(f"  {instance}.{field['name']} := {st_literal(step['inputs'][field['name']], field['type'])};")
            for i, field in enumerate(inputs):
                body.append(f"  TraceIn{i}[{step_index}] := {instance}.{field['name']};")
            body.append(f"  {instance}();")
            for i, field in enumerate(outputs):
                body.append(f"  TraceOut{i}[{step_index}] := {instance}.{field['name']};")
            body.append("  BenchCalls := BenchCalls + 1;")
            steps.append({"index": step_index, "case_id": case["id"], "case_step": case_step})
            step_index += 1
    body += [" END_CASE;", " BenchStep := BenchStep + 1;", f" IF BenchStep >= {count} THEN BenchDone := TRUE; END_IF;", "END_IF;"]
    return {"declaration": "\n".join(declarations), "implementation": "\n".join(body),
            "step_count": count, "steps": steps, "inputs": inputs, "outputs": outputs}

def run_functional(task, candidate, source_hash, workspace, settings):
    """Return real simulation trace/evidence. Unsupported tasks remain UNVERIFIED."""
    workspace = Path(workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    result = {"status": "UNVERIFIED", "actual_simulation": False, "execution_verified": False,
              "backend": "CODESYS_SIMULATION", "task_id": task["id"], "source_sha256": source_hash,
              "physical_connection_allowed": False, "trace_path": None, "reason": None}
    reasons = eligibility(task)
    if reasons:
        result["reason"] = "; ".join(reasons)
        write_json(workspace / "simulation_result.json", result)
        return result
    candidate = normalize_candidate(candidate)
    if digest(candidate) != source_hash:
        raise ValueError("Functional candidate source hash mismatch")
    missing = settings.compiler_ready()
    if missing:
        result["status"], result["reason"] = "TOOL_ERROR", "Missing compiler configuration: " + ", ".join(missing)
        write_json(workspace / "simulation_result.json", result)
        return result
    program = build_program(task)
    token = uuid.uuid4().hex
    script_path = ROOT / "codesys/scripts/run_tests.py"
    template_path = Path(settings.codesys_template)
    exec_ws, staged_script, staged_template = stage_ascii_workspace(
        workspace, script_path, template_path, settings.get_ascii_work_root()
    )
    project = exec_ws / "simulation.project"
    shutil.copy2(staged_template, project)
    request = {"request_id": token, "mode": "IDE_SIMULATION_ONLY", "no_physical_connection": True,
               "workspace": str(exec_ws), "project": str(project), "template": str(staged_template),
               "task_id": task["id"], "task_sha256": digest(task), "source_sha256": source_hash,
               "candidate": candidate, "program": program,
               "result_path": str(exec_ws / "simulation_evidence.json")}
    write_json(exec_ws / "request.json", request)
    write_json(exec_ws / "candidate.json", candidate)
    (exec_ws / "test_program.st").write_text(program["declaration"] + "\n\n" + program["implementation"] + "\nEND_PROGRAM\n", encoding="utf-8")
    if exec_ws != workspace:
        write_json(workspace / "request.json", request)
        write_json(workspace / "candidate.json", candidate)
        (workspace / "test_program.st").write_text(program["declaration"] + "\n\n" + program["implementation"] + "\nEND_PROGRAM\n", encoding="utf-8")
    command = [settings.codesys_exe, "--profile=" + settings.codesys_profile,
               "--runscript=" + str(staged_script), "--noUI", "--culture=en"]
    if settings.additional_folder:
        command.append("--additionalfolder=" + settings.additional_folder)
    write_json(exec_ws / "invocation.json", {"argv": command, "template_sha256": hashlib.sha256(Path(settings.codesys_template).read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(staged_script.read_bytes()).hexdigest(), "program_sha256": digest(program)})
    env = os.environ.copy()
    env["PLC_CODESYS_TEST_REQUEST"] = str(exec_ws / "request.json")
    for key in ("PLC_LLM_API_KEY", "OPENAI_API_KEY", "PLC_API_CONFIG"):
        env.pop(key, None)
    try:
        lock_path = ROOT / ".local/compiler.lock"
        lock_path.parent.mkdir(exist_ok=True)
        with lock_path.open("a+b") as lock:
            if os.name == "nt":
                import msvcrt
                if lock.tell() == 0:
                    lock.write(b"0"); lock.flush()
                lock.seek(0)
                deadline = time.monotonic() + 900
                while True:
                    try:
                        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                        break
                    except OSError:
                        if time.monotonic() >= deadline:
                            raise TimeoutError("Shared CODESYS lock wait exceeded 900 seconds")
                        time.sleep(0.25)
            with (exec_ws / "stdout.log").open("wb") as out, (exec_ws / "stderr.log").open("wb") as err:
                proc = subprocess.Popen(codesys_command(command), env=env, stdout=out, stderr=err,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
                try:
                    result["process_exit_code"] = proc.wait(timeout=max(180, settings.compiler_timeout))
                except subprocess.TimeoutExpired:
                    _kill_tree(proc)
                    result["status"], result["reason"] = "TIMEOUT", "CODESYS simulation process timeout"
            if result["status"] != "TIMEOUT":
                evidence = read_json(exec_ws / "simulation_evidence.json")
                if evidence.get("request_id") != token or evidence.get("source_sha256") != source_hash or evidence.get("physical_connection_allowed") is not False:
                    raise ValueError("Unrelated simulation evidence")
                result.update({k: evidence.get(k) for k in ("status", "actual_simulation", "execution_verified", "infrastructure_error")})
                if result["process_exit_code"] != 0:
                    result["status"], result["reason"] = "TOOL_ERROR", "Simulation IDE process exited abnormally"
                elif evidence.get("execution_verified"):
                    rows = evidence["observations"]
                    if len(rows) != program["step_count"]:
                        raise ValueError("Missing observed scan rows")
                    cases = {case["id"]: [] for case in task["tests"]}
                    for meta, row in zip(program["steps"], rows):
                        cases[meta["case_id"]].append({"inputs": row["inputs"], "outputs": row["outputs"]})
                    trace = {"task_id": task["id"], "task_sha256": digest(task), "source_sha256": source_hash,
                             "backend": "CODESYS_SIMULATION", "operator": "automated CODESYS IDE simulation scan sequencer",
                             "acquisition": "automated CODESYS IDE simulation with native scan sequencer",
                             "observed_utc": now(), "evidence_files": ["simulation_evidence.json", "test_program.st", "request.json"], "cases": cases,
                             "scan_control": "One FB invocation per real simulator task scan; separate freshly initialized instance per fixed test"}
                    write_json(workspace / "trace.json", trace)
                    if exec_ws != workspace:
                        sync_ascii_artifacts(exec_ws, workspace)
                    from .functional import evaluate_trace
                    evaluated = evaluate_trace(task, source_hash, trace, evidence_root=workspace)
                    result["status"] = evaluated["status"]
                    result["functional"] = evaluated
                    result["trace_path"] = str(workspace / "trace.json")
    except (OSError, ValueError, KeyError) as exc:
        result["status"], result["reason"] = "TOOL_ERROR", f"{type(exc).__name__}: {exc}"
    finally:
        if exec_ws != workspace:
            sync_ascii_artifacts(exec_ws, workspace)
    result["elapsed_seconds"] = time.monotonic() - started
    result["finished_utc"] = now()
    write_json(workspace / "simulation_result.json", result)
    return result
