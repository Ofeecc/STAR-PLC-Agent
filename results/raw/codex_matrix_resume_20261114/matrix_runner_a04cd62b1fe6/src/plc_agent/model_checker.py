"""Local NuSMV / nuXmv runner for explicitly encoded SMV models (not an ST translator)."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
from pathlib import Path

from .common import ROOT, now, write_json

SBMC_START_MARKER = "=== NUXMV_SBMC_PHASE ==="
LTL_RESULTS_MARKER = "=== NUXMV_LTL_RESULTS ==="
_SMT_FEATURE_RE = re.compile(
    r"\b(?:integer|real|array|toreal|toint|swconst|uwconst|floor)\b"
    r"|\b(?:unsigned|signed)\s+word\b"
    r"|0[us][dbho](?:1[6-9]|[2-9]\d|\d{3,})_"
)
_INFINITE_VAR_RE = re.compile(r":\s*(?:array\s+[^\n;]*?\bof\s+)?(?:integer|real)\b")


def _is_runnable_candidate(path: Path) -> bool:
    if not path.is_file():
        return False
    return os.name == "nt" or os.access(path, os.X_OK)


def _pick_checker_path(paths: list[Path]) -> Path:
    ranked = sorted(
        paths,
        key=lambda p: (0 if "usr/local/bin/nuxmv" in p.as_posix().lower() else 1, p.as_posix()),
    )
    return ranked[-1].resolve()


def _resolve_explicit_executable(configured: str, error_msg: str) -> Path:
    path = Path(configured)
    if path.is_file():
        return path.resolve()
    resolved = shutil.which(configured)
    if resolved and Path(resolved).is_file():
        return Path(resolved).resolve()
    raise ValueError(error_msg)


def _search_local_and_path(local_patterns: tuple[str, ...], path_cmds: tuple[str, ...], error_msg: str) -> Path:
    checkers_root = ROOT / ".local/model_checkers"
    for pattern in local_patterns:
        paths = [p for p in checkers_root.glob(pattern) if _is_runnable_candidate(p)]
        if paths:
            return _pick_checker_path(paths)

    for cmd in path_cmds:
        resolved = shutil.which(cmd)
        if resolved and Path(resolved).is_file():
            return Path(resolved).resolve()
    raise ValueError(error_msg)


def find_nusmv(executable: str | None = None) -> Path:
    """Locate local or PATH NuSMV (with nuXmv fallback if NuSMV is absent)."""
    configured = executable or os.environ.get("NUSMV_EXE")
    if configured:
        return _resolve_explicit_executable(configured, "NuSMV executable does not exist")

    patterns = ("**/NuSMV.exe", "**/nuXmv.exe") if os.name == "nt" else ("**/NuSMV", "**/nusmv", "**/nuXmv", "**/nuxmv")
    cmds = ("NuSMV.exe", "NuSMV", "nuXmv.exe", "nuXmv") if os.name == "nt" else ("NuSMV", "nusmv", "nuXmv", "nuxmv")
    return _search_local_and_path(patterns, cmds, "Install official NuSMV locally or set NUSMV_EXE")


def find_nuxmv(executable: str | None = None) -> Path:
    """Locate local or PATH nuXmv executable (preferring compat wrapper over raw usr/local/bin/nuXmv)."""
    configured = executable or os.environ.get("NUXMV_EXE")
    if not configured:
        env_nusmv = os.environ.get("NUSMV_EXE")
        if env_nusmv and "nuxmv" in Path(env_nusmv).name.lower():
            configured = env_nusmv
    if configured:
        return _resolve_explicit_executable(configured, "nuXmv executable does not exist")

    patterns = ("**/nuXmv.exe",) if os.name == "nt" else ("**/nuXmv", "**/nuxmv")
    cmds = ("nuXmv.exe", "nuXmv") if os.name == "nt" else ("nuXmv", "nuxmv")
    return _search_local_and_path(patterns, cmds, "Install nuXmv locally or set NUXMV_EXE")


def resolve_model_checker(
    executable: str | None = None, tool: str = "auto", needs_smt: bool = False
) -> tuple[str, Path]:
    """Resolve model checker tool label ('NuSMV' or 'nuXmv') and executable path."""
    if tool not in {"auto", "nusmv", "nuxmv"}:
        raise ValueError("tool must be one of 'auto', 'nusmv', 'nuxmv'")
    if executable:
        exe = find_nuxmv(executable) if tool == "nuxmv" else find_nusmv(executable)
        label = "nuXmv" if (tool == "nuxmv" or "nuxmv" in exe.name.lower()) else "NuSMV"
        return label, exe
    if tool == "nuxmv" or (tool == "auto" and needs_smt):
        return "nuXmv", find_nuxmv()
    if tool == "auto" and not os.environ.get("NUSMV_EXE") and os.environ.get("NUXMV_EXE"):
        return "nuXmv", find_nuxmv()
    exe = find_nusmv()
    return ("nuXmv" if "nuxmv" in exe.name.lower() else "NuSMV"), exe


def _needs_smt_engine(stripped: str) -> bool:
    return bool(_SMT_FEATURE_RE.search(stripped))


def _has_infinite_vars(stripped: str) -> bool:
    return bool(_INFINITE_VAR_RE.search(stripped))


def _build_nuxmv_smt_script(stripped: str, invar_count: int, ltl_count: int, bmc_bound: int) -> str:
    lines = [
        "set on_failure_script_quits 1",
        "read_model -i model.smv",
        "go_msat",
    ]
    if not _has_infinite_vars(stripped):
        lines.append("build_boolean_model")
    if invar_count > 0:
        lines.append("check_invar_ic3")
    if ltl_count > 0:
        lines.extend(
            [
                f"echo {SBMC_START_MARKER}",
                f"msat_check_ltlspec_sbmc_inc -k {bmc_bound}",
                f"echo {LTL_RESULTS_MARKER}",
                "check_ltlspec_ic3",
            ]
        )
    lines.append("quit")
    return "\n".join(lines) + "\n"


def parse_results(stdout: str, stderr: str, returncode: int, expected_count: int) -> dict:
    sbmc_false_exprs: set[str] = set()
    sbmc_match = re.search(
        rf"{re.escape(SBMC_START_MARKER)}(.*?){re.escape(LTL_RESULTS_MARKER)}",
        stdout,
        flags=re.S,
    )
    if sbmc_match:
        for fm in re.finditer(
            r"^--\s+(?:LTL\s+)?(?:specification|invariant)\s+(.+?)\s+is\s+false\s*$",
            sbmc_match.group(1),
            re.M | re.I,
        ):
            sbmc_false_exprs.add(fm.group(1).strip())

    verdict_stdout = re.sub(
        rf"{re.escape(SBMC_START_MARKER)}.*?{re.escape(LTL_RESULTS_MARKER)}\s*\n?",
        "",
        stdout,
        flags=re.S,
    )
    checks = []
    for m in re.finditer(
        r"^--\s+(?:LTL\s+)?(?:specification|invariant)\s+(.+?)\s+is\s+(true|false|unknown)\s*$",
        verdict_stdout,
        re.M | re.I,
    ):
        expr = m.group(1).strip()
        verdict = m.group(2).lower()
        if verdict == "true":
            checks.append({"expression": expr, "holds": True, "status": "PASS"})
        elif verdict == "false" or expr in sbmc_false_exprs:
            checks.append({"expression": expr, "holds": False, "status": "FAIL"})
        else:
            checks.append({"expression": expr, "holds": None, "status": "UNKNOWN"})

    unknown_count = sum(1 for c in checks if c["holds"] is None)
    failed = bool(
        returncode != 0
        or expected_count < 1
        or len(checks) != expected_count
        or re.search(
            r"(syntax error|aborting|cannot read|undefined|unknown command|^.*error:|^(?!.*\bwarning\b).*?(?:cannot assign value|range error))",
            stdout + "\n" + stderr,
            re.M | re.I,
        )
    )
    if failed:
        status = "TOOL_ERROR"
    elif any(c["holds"] is False for c in checks):
        status = "COUNTEREXAMPLE"
    elif unknown_count > 0:
        status = "INCONCLUSIVE"
    else:
        status = "MODEL_PROPERTIES_TRUE"
    return {
        "status": status,
        "property_results": checks,
        "expected_properties": expected_count,
        "checked_properties": len(checks),
        "unknown_properties": unknown_count,
        "returncode": returncode,
    }


def check_model(
    model: str | Path,
    out_dir: str | Path,
    executable: str | None = None,
    timeout: int = 60,
    tool: str = "auto",
    engine: str = "auto",
    bmc_bound: int = 25,
) -> dict:
    """Run NuSMV/nuXmv on an explicitly encoded SMV model and write a reproducible JSON artifact."""
    if not 1 <= timeout <= 600:
        raise ValueError("Timeout must be between 1 and 600 seconds")
    if engine not in {"auto", "bdd", "smt"}:
        raise ValueError("engine must be one of 'auto', 'bdd', 'smt'")
    if bmc_bound < 1:
        raise ValueError("bmc_bound must be >= 1")

    source = Path(model).read_bytes()
    text = source.decode("utf-8-sig")
    # Count declarations after removing SMV line comments; NuSMV/nuXmv parses the model itself.
    stripped = re.sub(r"--[^\n]*", "", text)
    invar_count = len(re.findall(r"\bINVARSPEC\b", stripped))
    ltl_count = len(re.findall(r"\bLTLSPEC\b", stripped))
    ctl_count = len(re.findall(r"\b(?:CTLSPEC|SPEC)\b", stripped))
    count = invar_count + ltl_count + ctl_count

    needs_smt = _needs_smt_engine(stripped)
    selected_engine = ("smt" if needs_smt else "bdd") if engine == "auto" else engine
    tool_name, exe = resolve_model_checker(executable, tool=tool, needs_smt=(selected_engine == "smt"))
    if selected_engine == "smt":
        if tool_name != "nuXmv":
            raise ValueError("SMT mode requires nuXmv (MathSAT); NuSMV only supports finite BDD mode")
        if ctl_count > 0:
            raise ValueError("CTL/SPEC properties are not supported in nuXmv SMT mode; use INVARSPEC or LTLSPEC")

    output = Path(out_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "model.smv").write_text(text, encoding="utf-8")
    if selected_engine == "smt":
        (output / "nuxmv.cmd").write_text(
            _build_nuxmv_smt_script(stripped, invar_count, ltl_count, bmc_bound),
            encoding="utf-8",
        )
        cmd = [str(exe), "-source", "nuxmv.cmd"]
    else:
        cmd = [str(exe), "model.smv"]

    timed_out = False
    try:
        proc = subprocess.run(cmd, cwd=output, capture_output=True, timeout=timeout)
        stdout = proc.stdout.decode("utf-8", errors="replace")
        stderr = proc.stderr.decode("utf-8", errors="replace")
        result = parse_results(stdout, stderr, proc.returncode, count)
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = (exc.stderr or b"").decode("utf-8", errors="replace")
        result = {"status": "TIMEOUT", "property_results": [], "expected_properties": count}
        timed_out = True
    (output / "stdout.txt").write_text(stdout, encoding="utf-8")
    (output / "stderr.txt").write_text(stderr, encoding="utf-8")
    result.update(
        {
            "tool": tool_name,
            "engine": selected_engine,
            "tool_exe_sha256": hashlib.sha256(exe.read_bytes()).hexdigest(),
            "model_sha256": hashlib.sha256(source).hexdigest(),
            "created_utc": now(),
            "scope": "EXPLICIT_SMV_MODEL_ONLY",
            "candidate_st_verified": False,
            "timed_out": timed_out,
            "stdout_path": "stdout.txt",
            "stderr_path": "stderr.txt",
        }
    )
    write_json(output / "model_check_result.json", result)
    return result
