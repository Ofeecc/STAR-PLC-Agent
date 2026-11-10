from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import time
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .common import ROOT, digest, now, read_json, write_json
from .config import Settings


@dataclass
class CompileResult:
    status: str
    success: bool = False
    backend: str = "CODESYS"
    infrastructure_error: str | None = None
    diagnostics: list = field(default_factory=list)
    elapsed_seconds: float = 0
    source_sha256: str = ""
    request_id: str = ""
    project: str | None = None
    evidence: str | None = None
    process_exit_code: int | None = None

def normalize_candidate(source):
    if isinstance(source, str):
        # Full ST text is accepted for a single FB, split at the last END_VAR.
        import re
        source = re.sub(r"\s*END_FUNCTION_BLOCK\s*$", "", source, flags=re.I)
        ends = list(re.finditer(r"\bEND_VAR\b", source, flags=re.I))
        if not ends:
            raise ValueError("Full ST must include FB declaration and END_VAR")
        pos = ends[-1].end()
        source = {"declaration": source[:pos], "implementation": source[pos:].strip(), "supporting_objects": []}
    if not isinstance(source, dict) or not all(isinstance(source.get(k), str) for k in ("declaration", "implementation")):
        raise ValueError("Candidate needs string declaration and implementation")
    result = {k: source[k] for k in ("declaration", "implementation")}
    result["supporting_objects"] = source.get("supporting_objects", [])
    if not isinstance(result["supporting_objects"], list):
        raise ValueError("supporting_objects must be a list")
    return result

def _kill_tree(process):
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, timeout=15)
    else:
        process.kill()

def codesys_command(argv):
    """CODESYS parses raw Windows command line and requires quotes AFTER '='."""
    if os.name != "nt":
        return argv
    parts = [subprocess.list2cmdline([argv[0]])]
    for arg in argv[1:]:
        if arg.startswith("--") and "=" in arg:
            name, value = arg.split("=", 1)
            if any(c in value for c in ('"', '\n', '\r')):
                raise ValueError("Unsupported quote/newline in CODESYS argument")
            parts.append(name + '=\"' + value + '\"')
        else:
            parts.append(subprocess.list2cmdline([arg]))
    return " ".join(parts)

def verify_evidence(evidence, request):
    """Fail closed: exit code, empty/stale messages alone never prove compilation."""
    if evidence.get("request_id") != request["request_id"] or evidence.get("source_sha256") != request["source_sha256"]:
        raise ValueError("Stale or unrelated compiler evidence")
    if evidence.get("backend") != "CODESYS" or not evidence.get("finished"):
        raise ValueError("Incomplete compiler evidence")
    if evidence.get("infrastructure_error"):
        return "TOOL_ERROR", False
    if not evidence.get("rebuild_invoked") or type(evidence.get("error_count")) is not int or evidence["error_count"] < 0:
        raise ValueError("No reliable rebuild diagnostics")
    if evidence["error_count"]:
        return "COMPILE_FAIL", False
    if not evidence.get("compiled_pou_crc"):
        raise ValueError("FB_Task was not demonstrably compiled")
    return "PASS", True

@contextmanager
def compiler_lock(timeout=180):
    path = ROOT / ".local/compiler.lock"
    path.parent.mkdir(exist_ok=True)
    started = time.monotonic()
    with path.open("a+b") as lock:
        if lock.tell() == 0:
            lock.write(b"0"); lock.flush()
        if os.name == "nt":
            import msvcrt
            while True:
                try:
                    lock.seek(0)
                    msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    if time.monotonic() - started >= timeout:
                        raise TimeoutError("Compiler lock wait deadline exceeded")
                    time.sleep(0.1)
        try:
            yield time.monotonic() - started
        finally:
            if os.name == "nt":
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)

ASCII_SYNC_FILES = (
    "codesys_evidence.json",
    "simulation_evidence.json",
    "stdout.log",
    "stderr.log",
    "request.json",
)

def sync_ascii_artifacts(staged_ws: Path | str, target_ws: Path | str) -> None:
    staged = Path(staged_ws)
    target = Path(target_ws)
    if staged.resolve() == target.resolve():
        return
    target.mkdir(parents=True, exist_ok=True)
    for name in ASCII_SYNC_FILES:
        src = staged / name
        if src.is_file():
            shutil.copy2(src, target / name)

def stage_ascii_workspace(
    workspace: Path | str,
    script_path: Path | str,
    template_path: Path | str,
    ascii_root: str | Path | None = None,
) -> tuple[Path, Path, Path]:
    ws = Path(workspace)
    script = Path(script_path)
    template = Path(template_path)

    paths = (ws, script, template)
    needs_staging = any(
        not str(p).isascii() or not str(p.resolve()).isascii()
        for p in paths
    )
    if not needs_staging:
        return ws, script, template

    if ascii_root is not None:
        root = Path(ascii_root)
    else:
        root = Settings.load(load_api=False).get_ascii_work_root()

    if not str(root.resolve()).isascii():
        root = Path("C:/plc_work" if os.name == "nt" else "/tmp/plc_work")

    ws_hash = hashlib.sha256(str(ws.resolve()).encode("utf-8")).hexdigest()[:16]
    staged_ws = root / ws_hash
    staged_ws.mkdir(parents=True, exist_ok=True)

    staged_script = staged_ws / script.name
    staged_tpl = staged_ws / template.name

    if script.is_file() and script.resolve() != staged_script.resolve():
        shutil.copy2(script, staged_script)

    if template.is_file() and template.resolve() != staged_tpl.resolve():
        shutil.copy2(template, staged_tpl)

    return staged_ws, staged_script, staged_tpl

def _compile_st(task, source_code, workspace, settings=None):
    cfg = settings or Settings.load()
    candidate = normalize_candidate(source_code)
    workspace = Path(workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=False)
    source_hash = digest(candidate)
    write_json(workspace / "candidate.json", candidate)
    (workspace / "FB_Task.st").write_text(candidate["declaration"] + "\n\n" + candidate["implementation"] + "\nEND_FUNCTION_BLOCK\n", encoding="utf-8")
    request_id = uuid.uuid4().hex
    result = CompileResult("TOOL_ERROR", source_sha256=source_hash, request_id=request_id)
    started = time.monotonic()
    missing = cfg.compiler_ready()
    if missing:
        result.infrastructure_error = "Missing compiler configuration: " + ", ".join(missing)
    else:
        script_path = ROOT / "codesys/scripts/build.py"
        template_path = Path(cfg.codesys_template)
        exec_ws, staged_script, staged_template = stage_ascii_workspace(
            workspace, script_path, template_path, cfg.get_ascii_work_root()
        )
        project = exec_ws / "task.project"
        shutil.copy2(staged_template, project)
        result.project = str(project)
        request = {"request_id": request_id, "source_sha256": source_hash, "task_id": task["id"],
                   "project": str(project), "candidate": candidate,
                   "result_path": str(exec_ws / "codesys_evidence.json"), "started_utc": now()}
        write_json(exec_ws / "request.json", request)
        if exec_ws != workspace:
            write_json(workspace / "request.json", request)
            write_json(exec_ws / "candidate.json", candidate)
            (exec_ws / "FB_Task.st").write_text(candidate["declaration"] + "\n\n" + candidate["implementation"] + "\nEND_FUNCTION_BLOCK\n", encoding="utf-8")
        command = [cfg.codesys_exe, "--profile=" + cfg.codesys_profile,
                   "--runscript=" + str(staged_script), "--scriptargs:" + request_id, "--noUI", "--culture=en"]
        if cfg.additional_folder:
            command.append("--additionalfolder=" + cfg.additional_folder)
        env = os.environ.copy()
        env["PLC_CODESYS_REQUEST"] = str(exec_ws / "request.json")
        # Compiler does not need an API credential.
        for key in ("PLC_LLM_API_KEY", "OPENAI_API_KEY", "PLC_API_CONFIG"):
            env.pop(key, None)
        write_json(exec_ws / "invocation.json", {"argv": command, "template_sha256": hashlib.sha256(Path(cfg.codesys_template).read_bytes()).hexdigest()})
        try:
            # Global serial lock prevents concurrent IDE repository access.
            with compiler_lock(cfg.compiler_timeout):
                with (exec_ws / "stdout.log").open("wb") as out, (exec_ws / "stderr.log").open("wb") as err:
                    process = subprocess.Popen(codesys_command(command), stdout=out, stderr=err, env=env,
                                               creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
                    try:
                        result.process_exit_code = process.wait(timeout=cfg.compiler_timeout)
                    except subprocess.TimeoutExpired:
                        _kill_tree(process)
                        result.status = "TIMEOUT"
                        result.infrastructure_error = "CODESYS process timeout"
                if result.status != "TIMEOUT":
                    evidence_path = exec_ws / "codesys_evidence.json"
                    evidence = read_json(evidence_path)
                    if exec_ws != workspace:
                        sync_ascii_artifacts(exec_ws, workspace)
                    result.evidence = str(workspace / "codesys_evidence.json") if exec_ws != workspace else str(evidence_path)
                    result.status, result.success = verify_evidence(evidence, request)
                    result.diagnostics = evidence.get("diagnostics", [])
                    result.infrastructure_error = evidence.get("infrastructure_error")
                    if result.process_exit_code != 0:
                        result.status, result.success = "TOOL_ERROR", False
                        result.infrastructure_error = "CODESYS exited abnormally; see process logs"
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            result.infrastructure_error = f"Compiler infrastructure: {type(exc).__name__}: {exc}"
        finally:
            if exec_ws != workspace:
                sync_ascii_artifacts(exec_ws, workspace)
                if (workspace / "codesys_evidence.json").is_file():
                    result.evidence = str(workspace / "codesys_evidence.json")
    result.elapsed_seconds = time.monotonic() - started
    write_json(workspace / "compile_result.json", asdict(result))
    return result

def compile_st(task, source_code, workspace, settings=None):
    """Always classify local service I/O failures separately from generated-code errors."""
    started = time.monotonic()
    try:
        return _compile_st(task, source_code, workspace, settings)
    except OSError as exc:
        candidate = normalize_candidate(source_code)
        result = CompileResult("TOOL_ERROR", infrastructure_error=f"Local compiler infrastructure: {type(exc).__name__}: {exc}",
            source_sha256=digest(candidate), elapsed_seconds=time.monotonic() - started)
        try:
            write_json(Path(workspace) / "compile_result.json", asdict(result))
        except OSError:
            pass
        return result

def actionable_diagnostics(result, max_chars=6000):
    unique = []
    for d in result.diagnostics:
        if "error" in str(d.get("severity", "")).lower():
            text = str(d.get("text", ""))
            if text not in unique:
                unique.append(text)
    return "\n".join(unique)[:max_chars]
