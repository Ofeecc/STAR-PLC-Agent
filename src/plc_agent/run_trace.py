"""Discovery and execution-trace extraction for live and archived agent runs."""

from __future__ import annotations

import difflib
import json
import os
import re
from pathlib import Path, PurePosixPath
from typing import Any, Callable

from .backend import SimCaseFailure, SimResult
from .common import digest
from .st_verifier import _parse_observer_smv, discover_observer_smv, extract_observer_spec_id_map

_MARKERS = (
    "result.json",
    "runtime_config.json",
    "task_view.json",
    "execution.jsonl",
    "model_calls.jsonl",
    "plan.json",
    "turn_00",
    "fullflow_result.json",
)
_PILOT_IGNORED_DIRS = {"source_snapshot", "compile_00", "sim_00", "fixed_evaluation", "post_failure_fixed_evaluation"}
_VERSION_RE = re.compile(r"^version_(?:(cegar|sim)_)?(\d+)$")


def _read_json_safe(path: Path) -> Any:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _read_jsonl_safe(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except Exception:
            # Live runs may flush partial trailing lines; ignore incomplete lines safely.
            continue
        if isinstance(item, dict):
            rows.append(item)
    return rows


def _is_run_workspace(directory: Path) -> bool:
    if not directory.is_dir():
        return False
    return any((directory / marker).exists() for marker in _MARKERS)


def resolve_safe_run_dir(root: Path, run_rel: str) -> tuple[Path | None, int, str]:
    """Validate and resolve a relative run workspace inside experiments/ or results/raw/."""
    if not run_rel or not isinstance(run_rel, str):
        return None, 400, "Missing required query parameter: 'run'"
    cleaned = run_rel.strip().replace("\\", "/")
    if "\x00" in cleaned or cleaned.startswith("/") or re.match(r"^[A-Za-z]:", cleaned):
        return None, 400, f"Invalid run path: '{run_rel}'"
    parts = [p for p in PurePosixPath(cleaned).parts if p not in ("", ".")]
    if not parts or any(p == ".." for p in parts):
        return None, 403, f"Path traversal rejected: '{run_rel}'"

    exp_root = (root / "experiments").resolve()
    raw_root = (root / "results" / "raw").resolve()
    candidate = (root / Path(*parts)).resolve()

    if not (candidate.is_relative_to(exp_root) or candidate.is_relative_to(raw_root)):
        return None, 403, f"Run path outside allowed artifact roots: '{run_rel}'"
    if candidate in (exp_root, raw_root) or candidate.parent == raw_root:
        return None, 400, f"Path does not point to a task run workspace: '{run_rel}'"
    if not _is_run_workspace(candidate):
        return None, 404, f"Run workspace not found: '{run_rel}'"
    return candidate, 200, "OK"


def _detect_framework_kind(ws: Path, result: dict | None, runtime_cfg: dict | None) -> str:
    fw = ((result or {}).get("framework") or (runtime_cfg or {}).get("framework") or "").lower()
    if fw in ("star", "star_v2", "self_harness"):
        return "star"
    if fw in ("custom_tool_loop", "claude_code", "codex_cli", "baseline"):
        return "baseline"
    if any(
        (ws / p).exists() for p in ("plan.json", "dialect_cards.json", "llm_planner", "llm_code_00", "selftest.json")
    ):
        return "star"
    if any((ws / p).exists() for p in ("turn_00", "trusted", "agent")):
        return "baseline"
    if (ws / "fullflow_result.json").is_file():
        return "fullflow"
    return "star"


def _infer_task_id(ws: Path, result: dict | None) -> str:
    if result and result.get("task_id"):
        return str(result["task_id"])
    for fname in ("task_view.json", "task.json", "evaluation_task.json", "fullflow_result.json"):
        data = _read_json_safe(ws / fname)
        if isinstance(data, dict) and (data.get("id") or data.get("task_id")):
            return str(data.get("id") or data.get("task_id"))
    for part in (ws.parent.name, ws.name):
        match = re.match(r"^(PUB\d+|SELF\d+)", part)
        if match:
            return match.group(1)
    return ws.name


def _infer_condition_and_campaign(
    ws: Path, root: Path, source: str, result: dict | None, runtime_cfg: dict | None
) -> tuple[str, str, str]:
    condition = (result or {}).get("condition") or (runtime_cfg or {}).get("condition") or ""
    campaign = ""
    group = ""
    try:
        rel = ws.relative_to(root).parts
        if source == "experiments" and len(rel) >= 3:
            condition = condition or rel[1]
            campaign = rel[2]
            group = condition or rel[2]
        elif source == "fullflow" and len(rel) >= 4:
            campaign = rel[2]
            if len(rel) >= 5 and ws.name == "generation":
                group = rel[3]
            else:
                group = rel[2]
        elif source == "pilot" and len(rel) >= 3:
            campaign = rel[2]
            group = "pilot_pair"
    except Exception:
        pass
    return str(condition or ""), str(campaign or ""), str(group or "")


def _unwrap_result(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    inner = payload.get("result")
    if isinstance(inner, dict):
        return inner
    return payload if ("status" in payload or "functional" in payload or "property_results" in payload) else None


def _load_parent_fullflow_context(ws: Path) -> dict[str, Any]:
    """Load post-generation full-flow compile/functional/formal records when present."""
    target_dir = ws.parent if ws.name == "generation" else ws
    ff = _read_json_safe(target_dir / "fullflow_result.json")
    fn = _read_json_safe(target_dir / "functional.json")
    fm = _read_json_safe(target_dir / "formal.json")
    cp = _read_json_safe(target_dir / "compile.json")
    return {
        "base_dir": target_dir,
        "fullflow": ff if isinstance(ff, dict) else None,
        "functional": _unwrap_result(fn),
        "formal": _unwrap_result(fm),
        "compile": _unwrap_result(cp),
    }


def _latest_mtime(ws: Path) -> float:
    best = 0.0
    try:
        best = ws.stat().st_mtime
    except OSError:
        return best
    for child in ws.iterdir():
        try:
            st = child.stat()
            if st.st_mtime > best:
                best = st.st_mtime
        except OSError:
            continue
    return best


def _extract_token_summary(model_calls: list[dict[str, Any]], result: dict | None, ws: Path) -> dict[str, Any]:
    completed = [e for e in model_calls if e.get("event") == "request_completed"]
    started = [e for e in model_calls if e.get("event") == "request_started"]
    reused = [e for e in model_calls if e.get("event") == "request_reused"]

    usage_records: list[dict[str, Any]] = []
    for ev in completed:
        if isinstance(ev.get("usage"), dict):
            usage_records.append(ev["usage"])
    if not usage_records and isinstance((result or {}).get("usage"), list):
        usage_records = [u for u in result["usage"] if isinstance(u, dict)]
    if not usage_records:
        for resp_path in sorted(ws.glob("llm_*/response.json")) + sorted(ws.glob("turn_*/response.json")):
            resp = _read_json_safe(resp_path)
            if isinstance(resp, dict) and isinstance(resp.get("usage"), dict):
                usage_records.append(resp["usage"])

    def _sum_optional(getter: Callable[[dict], int | None]) -> int | None:
        vals = [v for u in usage_records if (v := getter(u)) is not None]
        return sum(vals) if vals else None

    elapsed_vals = [
        float(e["elapsed_seconds"]) for e in completed if isinstance(e.get("elapsed_seconds"), (int, float))
    ]
    return {
        "usage_available": bool(usage_records),
        "request_started_count": len(started),
        "request_completed_count": len(completed),
        "reused_count": len(reused),
        "input_tokens": _sum_optional(
            lambda u: u.get("input_tokens") if u.get("input_tokens") is not None else u.get("prompt_tokens")
        ),
        "output_tokens": _sum_optional(
            lambda u: u.get("output_tokens") if u.get("output_tokens") is not None else u.get("completion_tokens")
        ),
        "reasoning_tokens": _sum_optional(lambda u: (u.get("completion_tokens_details") or {}).get("reasoning_tokens")),
        "cached_tokens": _sum_optional(
            lambda u: (
                (u.get("input_tokens_details") or {}).get("cached_tokens")
                if (u.get("input_tokens_details") or {}).get("cached_tokens") is not None
                else (u.get("prompt_tokens_details") or {}).get("cached_tokens")
            )
        ),
        "total_tokens": _sum_optional(lambda u: u.get("total_tokens")),
        "llm_elapsed_seconds": round(sum(elapsed_vals), 3) if elapsed_vals else None,
    }


def _candidate_to_st(cand: dict[str, Any]) -> str:
    decl = str(cand.get("declaration") or "").rstrip()
    impl = str(cand.get("implementation") or "").rstrip()
    return f"{decl}\n\n{impl}".strip() if (decl or impl) else ""


def _version_sort_key(path: Path) -> tuple[int, int, str]:
    match = _VERSION_RE.match(path.stem)
    if match:
        kind = match.group(1)
        bucket = 2 if kind == "sim" else (1 if kind == "cegar" else 0)
        return (bucket, int(match.group(2)), path.name)
    return (3, 0, path.name)


def _extract_versions(ws: Path, framework_kind: str, *, include_diffs: bool = True) -> list[dict[str, Any]]:
    raw_entries: list[tuple[str, str, str, dict[str, Any], bool]] = []
    if framework_kind == "baseline":
        for p in sorted((ws / "trusted").glob("compile_*/candidate.json")):
            cand = _read_json_safe(p)
            if isinstance(cand, dict) and ("declaration" in cand or "implementation" in cand):
                comp_res = _read_json_safe(p.parent / "compile_result.json")
                compile_ok = comp_res.get("success") if isinstance(comp_res, dict) else None
                raw_entries.append((p.parent.name, p.parent.name, "compile_attempt", cand, compile_ok is False))
    elif framework_kind == "fullflow":
        cand = _read_json_safe(ws / "candidate.json")
        if isinstance(cand, dict) and ("declaration" in cand or "implementation" in cand):
            raw_entries.append(("candidate", "Final Candidate", "final", cand, False))
    else:
        for p in sorted(ws.glob("version_*.json"), key=_version_sort_key):
            cand = _read_json_safe(p)
            if not isinstance(cand, dict):
                continue
            m = _VERSION_RE.match(p.stem)
            if m and m.group(1) == "sim":
                suffix = m.group(2)
                comp_res = _read_json_safe(ws / f"compile_sim_{int(suffix):02d}" / "compile_result.json")
                compile_failed = isinstance(comp_res, dict) and comp_res.get("success") is False
                raw_entries.append((p.stem, f"Sim Repair {suffix}", "sim_repair", cand, compile_failed))
            elif m and m.group(1) == "cegar":
                suffix = m.group(2)
                comp_res = _read_json_safe(ws / f"compile_cegar_{int(suffix):02d}" / "compile_result.json")
                compile_failed = isinstance(comp_res, dict) and comp_res.get("success") is False
                raw_entries.append((p.stem, f"CEGAR Repair {suffix}", "cegar_repair", cand, compile_failed))
            else:
                num = int(m.group(2)) if m else 0
                stage = "initial" if num == 0 else "compile_repair"
                label = "v00 (Initial)" if num == 0 else f"v{num:02d} (Compile Repair)"
                raw_entries.append((p.stem, label, stage, cand, False))

    final_cand = _read_json_safe(ws / "final_candidate.json")
    final_sha = digest(final_cand) if isinstance(final_cand, dict) else None

    if isinstance(final_cand, dict):
        if not raw_entries or digest(raw_entries[-1][3]) != final_sha:
            raw_entries.append(("final_candidate", "Final Candidate", "final", final_cand, False))

    earliest_final_idx = None
    if final_sha:
        for idx, (_, _, _, cand, _) in enumerate(raw_entries):
            if digest(cand) == final_sha:
                earliest_final_idx = idx
                break

    versions: list[dict[str, Any]] = []
    prev_lines: list[str] | None = None
    for idx, (vid, label, stage, cand, compile_failed) in enumerate(raw_entries):
        full_st = _candidate_to_st(cand)
        lines = full_st.splitlines()
        diff_lines = (
            list(
                difflib.unified_diff(
                    prev_lines,
                    lines,
                    fromfile=raw_entries[idx - 1][0],
                    tofile=vid,
                    lineterm="",
                )
            )
            if (include_diffs and prev_lines is not None)
            else []
        )
        prev_lines = lines
        sha = digest(cand)
        rolled_back = bool(
            compile_failed
            or (stage != "final" and earliest_final_idx is not None and idx > earliest_final_idx and sha != final_sha)
        )
        versions.append(
            {
                "id": vid,
                "label": label,
                "stage": stage,
                "sha256": sha,
                "is_final": bool(final_sha and sha == final_sha),
                "rolled_back": rolled_back,
                "declaration": str(cand.get("declaration") or ""),
                "implementation": str(cand.get("implementation") or ""),
                "supporting_objects": cand.get("supporting_objects") or [],
                "full_st": full_st,
                "diff_from_prev": diff_lines,
            }
        )
    return versions


def _compile_attempts_from_ws(ws: Path, result: dict | None, framework_kind: str) -> list[dict[str, Any]]:
    if result and isinstance(result.get("compilation_attempts"), list) and result["compilation_attempts"]:
        return result["compilation_attempts"]
    pattern = (
        "trusted/compile_*/compile_result.json" if framework_kind == "baseline" else "compile_*/compile_result.json"
    )
    out = []
    for p in sorted(ws.glob(pattern)):
        data = _read_json_safe(p)
        if isinstance(data, dict):
            out.append(data)
    return out


def _sim_attempts_from_ws(ws: Path, framework_kind: str) -> list[dict[str, Any]]:
    pattern = "trusted/sim_*/simulation_result.json" if framework_kind == "baseline" else "sim_*/simulation_result.json"
    out = []
    for p in sorted(ws.glob(pattern)):
        data = _read_json_safe(p)
        if isinstance(data, dict):
            data["_dir"] = p.parent.name
            out.append(data)
    return out


def _call_state(call_dir: str, started: set[str], completed: set[str]) -> str:
    if call_dir in completed:
        return "DONE"
    if call_dir in started:
        return "RUNNING"
    return "PENDING"


def resolve_showcase_outcome(
    raw_status: str | None,
    *,
    compiled: bool | None,
    fixed_status: str | None,
    formal_status: str | None,
    fixed_evaluated: int | None = None,
    fixed_planned: int | None = None,
) -> tuple[str, str | None]:
    """Classify showcase status: Reason-1 PARTIAL (checks passed, spec ID unmapped) displays as PASS; keep Reason-2 PARTIAL."""
    st = str(raw_status or "UNKNOWN")
    if st != "PARTIAL":
        if formal_status == "UNSUPPORTED_ST" and st != "FAIL":
            return st, "reason2_unsupported_st"
        return st, None

    all_fixed_passed = fixed_status == "PASS" and (
        fixed_planned is None or (fixed_evaluated is not None and fixed_evaluated >= fixed_planned)
    )
    if compiled is True and all_fixed_passed and formal_status == "PASS":
        return "PASS", "reason1_checks_verified"
    if formal_status == "UNSUPPORTED_ST":
        return "PARTIAL", "reason2_unsupported_st"
    if fixed_status and fixed_status != "PASS":
        return "PARTIAL", "reason2_incomplete_fixed"
    return "PARTIAL", "reason2_incomplete"


def _enrich_verification_ids(ver_payload: dict[str, Any] | None, task: dict[str, Any] | None) -> dict[str, Any] | None:
    """Resolve legacy SMV_1..SMV_N IDs back to observer NAMEs / task['ltl'] IDs for historical formal.json display."""
    if not isinstance(ver_payload, dict) or not isinstance(task, dict):
        return ver_payload
    props = ver_payload.get("property_results")
    if not isinstance(props, list) or not props:
        return ver_payload
    if not any(isinstance(pr, dict) and str(pr.get("id") or "").startswith("SMV_") for pr in props):
        return ver_payload
    tid = str(task.get("id") or "")
    obs_path = discover_observer_smv(tid)
    if not obs_path or not obs_path.is_file():
        return ver_payload
    try:
        obs = _parse_observer_smv(obs_path.read_text(encoding="utf-8"))
        id_map = extract_observer_spec_id_map(obs.spec_stmts, task)
    except Exception:
        return ver_payload

    new_props = []
    for idx, pr in enumerate(props):
        if not isinstance(pr, dict):
            new_props.append(pr)
            continue
        item = dict(pr)
        cur_id = str(item.get("id") or "")
        if cur_id.startswith("SMV_") and idx < len(id_map):
            item["id"] = id_map[idx]
        new_props.append(item)
    out = dict(ver_payload)
    out["property_results"] = new_props
    return out


def _compact_verification_payload(ver: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(ver, dict):
        return None
    ces = []
    for ce in (ver.get("counterexamples") or [])[:2]:
        if isinstance(ce, dict):
            ces.append(
                {
                    "property": ce.get("property"),
                    "loop_start_step": ce.get("loop_start_step"),
                    "trace": (ce.get("trace") or [])[:16],
                }
            )
    return {
        "status": ver.get("status"),
        "tool": ver.get("tool"),
        "engine": ver.get("engine"),
        "modeling_scope": ver.get("modeling_scope"),
        "full_specification_verified": ver.get("full_specification_verified"),
        "specification_coverage": ver.get("specification_coverage"),
        "total_properties": ver.get("total_properties"),
        "passed_properties": ver.get("passed_properties"),
        "failed_properties": ver.get("failed_properties"),
        "unknown_properties": ver.get("unknown_properties"),
        "property_results": (ver.get("property_results") or [])[:40],
        "counterexamples": ces,
        "warnings": (ver.get("warnings") or [])[:15],
        "reason": ver.get("reason"),
    }


def _collect_verify_attempts(ws: Path) -> list[dict[str, Any]]:
    attempts = []
    for vdir in sorted(ws.glob("verify_*")):
        if not vdir.is_dir():
            continue
        vres = _read_json_safe(vdir / "verification_result.json")
        if isinstance(vres, dict):
            comp = _compact_verification_payload(vres)
            if comp is not None:
                comp["attempt"] = vdir.name
                attempts.append(comp)
    return attempts


def _build_star_stages(
    ws: Path,
    result: dict | None,
    runtime_cfg: dict | None,
    model_calls: list[dict[str, Any]],
    exec_events: list[dict[str, Any]],
    versions: list[dict[str, Any]],
    parent_ctx: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    is_live = result is None
    parent_ctx = parent_ctx or _load_parent_fullflow_context(ws)
    ablation = (result or runtime_cfg or {}).get("ablation")
    started_calls = {
        e.get("call_dir") for e in model_calls if e.get("event") == "request_started" and e.get("call_dir")
    }
    completed_calls = {
        e.get("call_dir")
        for e in model_calls
        if e.get("event") in ("request_completed", "request_reused") and e.get("call_dir")
    }
    plan = _read_json_safe(ws / "plan.json")
    dialect = _read_json_safe(ws / "dialect_cards.json")
    selftest = _read_json_safe(ws / "selftest.json")
    compile_attempts = _compile_attempts_from_ws(ws, result, "star")
    sim_attempts = _sim_attempts_from_ws(ws, "star")
    verify_attempts = _collect_verify_attempts(ws)
    rejected = (result or {}).get("selftest_rejected") or []
    rollback_count = sum(1 for v in versions if v.get("rolled_back"))

    # 1. Planner
    planner_call = _call_state("llm_planner", started_calls, completed_calls)
    if ablation == "no_planner":
        planner_status = "SKIPPED"
    elif isinstance(plan, dict):
        planner_status = "DONE"
    elif planner_call == "RUNNING" and is_live:
        planner_status = "RUNNING"
    elif planner_call in ("RUNNING", "DONE") and not is_live:
        planner_status = "FAIL"
    else:
        planner_status = "PENDING"
    state_machine = plan.get("state_machine", {}) if isinstance(plan, dict) else {}
    states = state_machine.get("states", []) if isinstance(state_machine, dict) else state_machine
    if not isinstance(states, list):
        states = []
    planner_stage = {
        "id": "planner",
        "label_en": "1. Planner",
        "label_zh": "1. 架构规划",
        "status": planner_status,
        "summary_en": f"{len(states)} states planned"
        if states
        else ("Skipped (ablation)" if ablation == "no_planner" else "State machine & timer decomposition"),
        "summary_zh": f"已规划 {len(states)} 个状态"
        if states
        else ("已跳过（消融）" if ablation == "no_planner" else "状态机与定时器分解"),
        "metrics": {"state_count": len(states)},
        "detail": plan if isinstance(plan, dict) else {},
    }

    # 2. Dialect Cards
    if ablation == "no_dialect":
        dialect_status = "SKIPPED"
    elif isinstance(dialect, list):
        dialect_status = "DONE"
    elif is_live and planner_status == "DONE":
        dialect_status = "RUNNING"
    else:
        dialect_status = "PENDING"
    cards = dialect if isinstance(dialect, list) else []
    dialect_stage = {
        "id": "dialect",
        "label_en": "2. Dialect Cards",
        "label_zh": "2. CODESYS 方言卡",
        "status": dialect_status,
        "summary_en": f"{len(cards)} ST dialect cards injected"
        if cards
        else ("Skipped (ablation)" if ablation == "no_dialect" else "CODESYS IEC 61131-3 guardrails"),
        "summary_zh": f"已注入 {len(cards)} 张方言卡"
        if cards
        else ("已跳过（消融）" if ablation == "no_dialect" else "CODESYS IEC 61131-3 规范卡"),
        "metrics": {"card_count": len(cards)},
        "detail": {
            "cards": [
                {"id": c.get("id"), "title": c.get("title"), "body": str(c.get("body") or "")[:400]}
                for c in cards
                if isinstance(c, dict)
            ]
        },
    }

    # 3. Coder & Compile Repair
    code_repair_active = any(
        c.startswith(("llm_code_", "llm_repair_")) and c not in completed_calls for c in started_calls
    )
    compile_started = sum(1 for e in exec_events if e.get("event") == "compile_started")
    compile_finished = sum(1 for e in exec_events if e.get("event") == "compile_finished")
    compile_running = compile_started > compile_finished
    final_compiled = (result or {}).get("final_compiled")
    if final_compiled is True:
        coder_status = "DONE"
    elif final_compiled is False:
        coder_status = "FAIL"
    elif compile_attempts and any(a.get("success") for a in compile_attempts):
        coder_status = "DONE"
    elif is_live and (code_repair_active or compile_running or (ws / "version_00.json").exists()):
        coder_status = "RUNNING"
    elif not is_live and (started_calls & {"llm_code_00"} or any(c.startswith("llm_repair_") for c in started_calls)):
        coder_status = "FAIL" if (result or {}).get("status") in ("COMPILE_FAIL", "TOOL_ERROR", "TIMEOUT") else "DONE"
    else:
        coder_status = "PENDING"
    coder_stage = {
        "id": "coder",
        "label_en": "3. Coder & Compile Repair",
        "label_zh": "3. ST 生成与编译修复",
        "status": coder_status,
        "summary_en": f"{len(compile_attempts)} compile(s), {(result or {}).get('repair_attempts', 0)} repair(s)",
        "summary_zh": f"编译 {len(compile_attempts)} 次，语法修复 {(result or {}).get('repair_attempts', 0)} 次",
        "metrics": {
            "compile_attempts": len(compile_attempts),
            "first_pass_compiled": (result or {}).get("first_pass_compiled"),
            "final_compiled": final_compiled,
            "repair_attempts": (result or {}).get("repair_attempts", 0),
        },
        "detail": {"compilation_attempts": compile_attempts},
    }

    # 4. Formal Verify & CEGAR
    cegar_active = any(c.startswith("llm_cegar_") and c not in completed_calls for c in started_calls)
    ver_res = (result or {}).get("verification") or (verify_attempts[-1] if verify_attempts else None)
    parent_formal = parent_ctx.get("formal") or ((parent_ctx.get("fullflow") or {}).get("formal"))
    effective_ver = parent_formal if isinstance(parent_formal, dict) else ver_res
    cegar_repairs = int((result or {}).get("cegar_repairs") or 0)
    if ablation in ("no_verify", "no_cegar"):
        verify_status = "SKIPPED"
    elif is_live and (cegar_active or (verify_attempts and coder_status == "DONE" and not selftest)):
        verify_status = "RUNNING"
    elif isinstance(effective_ver, dict) and effective_ver.get("status"):
        verify_status = str(effective_ver.get("status"))
    elif not is_live and final_compiled is False:
        verify_status = "SKIPPED"
    elif not is_live:
        verify_status = "NOT_RUN"
    else:
        verify_status = "PENDING"

    v_passed = (effective_ver or {}).get("passed_properties")
    v_total = (effective_ver or {}).get("total_properties")
    if isinstance(effective_ver, dict) and effective_ver.get("status") in ("PASS", "COUNTEREXAMPLE"):
        verify_sum_en = f"{v_passed}/{v_total} props · CEGAR ×{cegar_repairs}"
        verify_sum_zh = f"性质 {v_passed}/{v_total} 通过 · CEGAR ×{cegar_repairs}"
    elif verify_status in ("UNSUPPORTED_ST", "TOOL_ERROR", "TIMEOUT", "SKIPPED", "NOT_RUN"):
        verify_sum_en = f"{verify_status} · CEGAR ×{cegar_repairs}"
        verify_sum_zh = f"{verify_status} · CEGAR ×{cegar_repairs}"
    else:
        verify_sum_en = "ST->SMV translation & NuSMV/nuXmv CEGAR"
        verify_sum_zh = "ST->SMV 符号转换与反例引导修复"

    verify_stage = {
        "id": "verify",
        "label_en": "4. Formal Verify & CEGAR",
        "label_zh": "4. ST->SMV 形式验证与 CEGAR",
        "status": verify_status,
        "summary_en": verify_sum_en,
        "summary_zh": verify_sum_zh,
        "metrics": {
            "verification_calls": (result or {}).get("verification_call_count") or len(verify_attempts),
            "cegar_repairs": cegar_repairs,
            "passed_properties": v_passed,
            "total_properties": v_total,
            "failed_properties": (effective_ver or {}).get("failed_properties"),
            "tool": (effective_ver or {}).get("tool"),
            "engine": (effective_ver or {}).get("engine"),
            "full_specification_verified": (effective_ver or {}).get("full_specification_verified"),
        },
        "detail": {
            "in_harness": _compact_verification_payload(ver_res),
            "fullflow_formal": _compact_verification_payload(parent_formal),
            "attempts": verify_attempts,
        },
    }

    # 5. Self-Test Synth
    tester_call = _call_state("llm_tester", started_calls, completed_calls)
    st_cases = selftest if isinstance(selftest, list) else []
    if ablation == "no_selftest" or (not is_live and final_compiled is False):
        tester_status = "SKIPPED"
    elif is_live and tester_call == "RUNNING":
        tester_status = "RUNNING"
    elif isinstance(selftest, list):
        tester_status = "DONE"
    elif not is_live and tester_call == "RUNNING":
        tester_status = "FAIL"
    else:
        tester_status = "PENDING"
    tester_stage = {
        "id": "tester",
        "label_en": "5. Self-Test Synth",
        "label_zh": "5. 自测用例合成",
        "status": tester_status,
        "summary_en": f"{len(st_cases)} agent self-test cases"
        if st_cases
        else ("Skipped" if tester_status == "SKIPPED" else "Edge-case sequence synthesis"),
        "summary_zh": f"{len(st_cases)} 组Agent自测序列"
        if st_cases
        else ("已跳过" if tester_status == "SKIPPED" else "边界与边沿时序合成"),
        "metrics": {"selftest_cases": len(st_cases), "rejected_cases": len(rejected)},
        "detail": {"cases": st_cases, "rejected": rejected},
    }

    # 6. Sim & Monotonic Ratchet
    sim_repair_active = any(c.startswith("llm_sim_repair_") and c not in completed_calls for c in started_calls)
    sim_started = sum(1 for e in exec_events if e.get("event") in ("selftest_started", "fixed_evaluation_started"))
    sim_finished = sum(1 for e in exec_events if e.get("event") in ("selftest_finished", "fixed_evaluation_finished"))
    parent_func_res = parent_ctx.get("functional") or {}
    parent_func = parent_func_res.get("functional") if isinstance(parent_func_res.get("functional"), dict) else None
    result_func = (result or {}).get("functional") or {}
    func = (
        parent_func
        if parent_func and parent_func.get("evaluated_cases")
        else (result_func if result_func.get("evaluated_cases") else (parent_func or result_func))
    )
    run_status = (result or {}).get("status")
    if parent_func and parent_func.get("status"):
        ratchet_status = str(parent_func.get("status"))
        if ratchet_status == "TEST_FAIL":
            ratchet_status = "FAIL"
    elif run_status == "PASS":
        ratchet_status = "PASS"
    elif run_status in ("TEST_FAIL", "COMPILE_FAIL", "TOOL_ERROR", "TIMEOUT"):
        ratchet_status = "FAIL" if coder_status == "DONE" else "PENDING"
    elif run_status == "UNVERIFIED":
        ratchet_status = "UNVERIFIED"
    elif is_live and (sim_repair_active or sim_started > sim_finished or bool(sim_attempts) or rollback_count > 0):
        ratchet_status = "RUNNING"
    else:
        ratchet_status = "PENDING"

    ratchet_stage = {
        "id": "ratchet",
        "label_en": "6. Sim & Monotonic Ratchet",
        "label_zh": "6. 仿真验证与单调棘轮",
        "status": ratchet_status,
        "summary_en": (
            f"Fixed eval {func.get('passed_cases')}/{func.get('evaluated_cases')} passed, {rollback_count} rollback(s)"
            if func.get("evaluated_cases")
            else f"{len(sim_attempts)} self-test sim(s), {rollback_count} rollback(s)"
        ),
        "summary_zh": (
            f"固定评测 {func.get('passed_cases')}/{func.get('evaluated_cases')} 通过，回滚 {rollback_count} 次"
            if func.get("evaluated_cases")
            else f"自测仿真 {len(sim_attempts)} 次，棘轮回滚 {rollback_count} 次"
        ),
        "metrics": {
            "simulation_calls": len(sim_attempts),
            "rollback_count": rollback_count,
            "rejected_selftest_count": len(rejected),
            "passed_cases": func.get("passed_cases"),
            "evaluated_cases": func.get("evaluated_cases"),
        },
        "detail": {"selftest_evaluation": (result or {}).get("selftest_evaluation"), "functional": func},
    }

    return [planner_stage, dialect_stage, coder_stage, verify_stage, tester_stage, ratchet_stage]


def _build_fullflow_stages(ws: Path, ff: dict[str, Any] | None) -> list[dict[str, Any]]:
    ff = ff or {}
    stages_map = ff.get("stages") or {}
    comp_res = (stages_map.get("compile") or {}).get("result") or _read_json_safe(ws / "compile.json") or {}
    if "result" in comp_res and isinstance(comp_res["result"], dict):
        comp_res = comp_res["result"]
    func_top = (stages_map.get("functional") or {}).get("result") or _read_json_safe(ws / "functional.json") or {}
    if "result" in func_top and isinstance(func_top["result"], dict):
        func_top = func_top["result"]
    func = func_top.get("functional") if isinstance(func_top.get("functional"), dict) else {}
    formal_res = ff.get("formal") or (stages_map.get("formal") or {}).get("result") or _read_json_safe(ws / "formal.json") or {}
    if "result" in formal_res and isinstance(formal_res["result"], dict):
        formal_res = formal_res["result"]

    comp_ok = bool(comp_res.get("success") or ff.get("compiled"))
    func_status = str(func.get("status") or func_top.get("status") or "NOT_RUN")
    formal_status = str(formal_res.get("status") or "NOT_RUN")
    return [
        {
            "id": "coder",
            "label_en": "1. Candidate & Compile",
            "label_zh": "1. 候选代码与编译",
            "status": "DONE" if comp_ok else "FAIL",
            "summary_en": "CODESYS compile PASS" if comp_ok else str(comp_res.get("status") or "COMPILE_FAIL"),
            "summary_zh": "CODESYS 编译通过" if comp_ok else str(comp_res.get("status") or "COMPILE_FAIL"),
            "metrics": {"compile_attempts": 1, "final_compiled": comp_ok},
            "detail": {"compilation_attempts": [comp_res] if comp_res else []},
        },
        {
            "id": "verify",
            "label_en": "2. Formal Verification",
            "label_zh": "2. ST->SMV 形式验证",
            "status": formal_status,
            "summary_en": (
                f"{formal_res.get('passed_properties')}/{formal_res.get('total_properties')} props"
                if formal_res.get("total_properties") is not None
                else formal_status
            ),
            "summary_zh": (
                f"性质 {formal_res.get('passed_properties')}/{formal_res.get('total_properties')} 通过"
                if formal_res.get("total_properties") is not None
                else formal_status
            ),
            "metrics": {
                "passed_properties": formal_res.get("passed_properties"),
                "total_properties": formal_res.get("total_properties"),
                "tool": formal_res.get("tool"),
                "engine": formal_res.get("engine"),
                "full_specification_verified": formal_res.get("full_specification_verified"),
            },
            "detail": {"fullflow_formal": _compact_verification_payload(formal_res)},
        },
        {
            "id": "ratchet",
            "label_en": "3. Fixed Evaluation",
            "label_zh": "3. 固定测试集仿真",
            "status": "FAIL" if func_status == "TEST_FAIL" else func_status,
            "summary_en": f"{func.get('passed_cases', 0)}/{func.get('evaluated_cases', 0)} passed (plan {func.get('planned_cases', ff.get('planned_cases', 0))})",
            "summary_zh": f"{func.get('passed_cases', 0)}/{func.get('evaluated_cases', 0)} 通过（计划 {func.get('planned_cases', ff.get('planned_cases', 0))}）",
            "metrics": {
                "passed_cases": func.get("passed_cases"),
                "evaluated_cases": func.get("evaluated_cases"),
            },
            "detail": {"functional": func},
        },
    ]


def _build_baseline_stages(ws: Path, result: dict | None) -> list[dict[str, Any]]:
    is_live = result is None
    turns = sorted(ws.glob("turn_*"))
    tool_files = sorted(ws.glob("turn_*/tool_*.json"))
    compile_attempts = _compile_attempts_from_ws(ws, result, "baseline")
    sim_attempts = _sim_attempts_from_ws(ws, "baseline")
    func = (result or {}).get("functional") or {}
    run_status = (result or {}).get("status")

    context_done = (ws / "task.json").exists() or (ws / "agent" / "prompt.txt").exists()
    tool_status = "DONE" if (not is_live and (turns or tool_files)) else ("RUNNING" if is_live and turns else "PENDING")
    compile_ok = any(a.get("success") for a in compile_attempts)
    gate_status = (
        "DONE"
        if compile_ok
        else (
            "FAIL" if compile_attempts and not is_live else ("RUNNING" if is_live and compile_attempts else "PENDING")
        )
    )
    final_status = (
        run_status
        if run_status in ("PASS", "UNVERIFIED")
        else ("FAIL" if run_status in ("TEST_FAIL", "COMPILE_FAIL", "TOOL_ERROR", "TIMEOUT") else "PENDING")
    )

    return [
        {
            "id": "context",
            "label_en": "1. Task & MCP Context",
            "label_zh": "1. 规约与 MCP 上下文",
            "status": "DONE" if context_done else "PENDING",
            "summary_en": "Visible spec & trusted tool bindings",
            "summary_zh": "可见规约与受控编译仿真工具绑定",
            "metrics": {},
            "detail": {},
        },
        {
            "id": "tool_loop",
            "label_en": "2. Tool-Use Loop",
            "label_zh": "2. 多轮工具调用循环",
            "status": tool_status,
            "summary_en": f"{len(turns)} turn(s), {len(tool_files)} tool call(s)",
            "summary_zh": f"{len(turns)} 轮对话，{len(tool_files)} 次工具调用",
            "metrics": {"turns": len(turns), "tool_calls": len(tool_files)},
            "detail": {},
        },
        {
            "id": "compile_sim",
            "label_en": "3. Compiler & Sim Gate",
            "label_zh": "3. 受控编译/仿真门禁",
            "status": gate_status,
            "summary_en": f"{len(compile_attempts)} compile(s), {len(sim_attempts)} sim(s)",
            "summary_zh": f"编译 {len(compile_attempts)} 次，仿真 {len(sim_attempts)} 次",
            "metrics": {"compile_attempts": len(compile_attempts), "sim_attempts": len(sim_attempts)},
            "detail": {"compilation_attempts": compile_attempts},
        },
        {
            "id": "final",
            "label_en": "4. Final Held-Out Eval",
            "label_zh": "4. 最终冻结评测",
            "status": final_status,
            "summary_en": f"{func.get('passed_cases', 0)}/{func.get('evaluated_cases', 0)} fixed tests"
            if func.get("evaluated_cases")
            else (run_status or "Pending"),
            "summary_zh": f"冻结测试 {func.get('passed_cases', 0)}/{func.get('evaluated_cases', 0)} 通过"
            if func.get("evaluated_cases")
            else (run_status or "等待"),
            "metrics": {"passed_cases": func.get("passed_cases"), "evaluated_cases": func.get("evaluated_cases")},
            "detail": {"functional": func},
        },
    ]


def _build_timeline(
    ws: Path, model_calls: list[dict[str, Any]], exec_events: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    timeline: list[dict[str, Any]] = []
    for idx, ev in enumerate(model_calls):
        kind = ev.get("event", "model_event")
        usage = ev.get("usage") if isinstance(ev.get("usage"), dict) else {}
        timeline.append(
            {
                "seq": idx,
                "utc": ev.get("utc") or "",
                "source": "model",
                "event": kind,
                "actor": ev.get("call_dir") or "llm",
                "model": ev.get("reported_model") or ev.get("model"),
                "elapsed_seconds": ev.get("elapsed_seconds"),
                "total_tokens": usage.get("total_tokens"),
                "status": "REUSED"
                if kind == "request_reused"
                else ("DONE" if kind == "request_completed" else "STARTED"),
                "detail": {
                    k: v
                    for k, v in ev.items()
                    if k
                    in ("call_dir", "request_number", "reasoning_effort_requested", "history_truncated", "new_request")
                },
            }
        )
    for idx, ev in enumerate(exec_events):
        timeline.append(
            {
                "seq": len(model_calls) + idx,
                "utc": ev.get("utc") or "",
                "source": "execution",
                "event": ev.get("event") or "exec_event",
                "actor": ev.get("event", "").split("_")[0] or "codesys",
                "status": ev.get("status") or ("STARTED" if str(ev.get("event", "")).endswith("_started") else "DONE"),
                "detail": {k: v for k, v in ev.items() if k not in ("utc", "event", "status", "functional")},
            }
        )
    for idx, tfile in enumerate(sorted(ws.glob("turn_*/tool_*.json"))):
        tool_data = _read_json_safe(tfile)
        if isinstance(tool_data, dict):
            timeline.append(
                {
                    "seq": len(model_calls) + len(exec_events) + idx,
                    "utc": "",
                    "source": "tool",
                    "event": f"tool_call:{tool_data.get('name', 'unknown')}",
                    "actor": tfile.parent.name,
                    "status": "DONE",
                    "detail": {"name": tool_data.get("name"), "call_id": tool_data.get("call_id")},
                }
            )
    timeline.sort(key=lambda item: (item["utc"] == "", item["utc"], item["seq"]))
    return timeline


def _extract_waveforms(
    ws: Path,
    task: dict | None,
    result: dict | None,
    waveform_builder: Callable[[dict, list[dict], SimResult, Path], list[dict[str, Any]]],
    parent_ctx: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not task:
        return [], {"kind": "none", "provenance": "Task definition unavailable", "execution_verified": False}

    parent_ctx = parent_ctx or _load_parent_fullflow_context(ws)
    eval_candidates: list[tuple[str, Path, Path | None]] = []

    # Highest priority: full-flow fixed evaluation traces stored in task root or ws/functional/
    base_dir = parent_ctx.get("base_dir") or ws
    func_dir = base_dir / "functional"
    if func_dir.is_dir():
        for attempt_dir in sorted(func_dir.glob("attempt_*"), reverse=True):
            if attempt_dir.is_dir():
                eval_candidates.append(
                    ("fixed_evaluation", attempt_dir / "trace.json", attempt_dir / "simulation_result.json")
                )

    # Next: held-out fixed evaluation inside workspace -> functional_trace -> post_failure -> self-test
    eval_candidates.extend(
        [
            (
                "fixed_evaluation",
                ws / "fixed_evaluation" / "trace.json",
                ws / "fixed_evaluation" / "simulation_result.json",
            ),
            ("functional_trace", ws / "functional_trace.json", None),
        ]
    )
    for fdir in sorted(ws.glob("functional_*"), reverse=True):
        if fdir.is_dir():
            eval_candidates.append(("functional_trace", fdir / "trace.json", fdir / "simulation_result.json"))
    eval_candidates.append(
        (
            "post_failure_fixed_evaluation",
            ws / "post_failure_fixed_evaluation" / "trace.json",
            ws / "post_failure_fixed_evaluation" / "simulation_result.json",
        )
    )

    for kind, trace_path, sim_path in eval_candidates:
        trace_data = _read_json_safe(trace_path)
        if not isinstance(trace_data, dict) or not trace_data.get("cases"):
            continue
        sim_json = _read_json_safe(sim_path) if sim_path else None
        parent_func = parent_ctx.get("functional") or {}
        func_info = (sim_json or {}).get("functional") or parent_func.get("functional") or (result or {}).get("functional") or {}
        failures = []
        for d in func_info.get("details") or []:
            if isinstance(d, dict) and d.get("status") != "PASS" and d.get("first_bad_step") is not None:
                failures.append(
                    SimCaseFailure(
                        case_id=str(d.get("case_id", "")),
                        first_bad_step=int(d.get("first_bad_step", 0)),
                        field=str(d.get("field", "")),
                        expected=d.get("expected"),
                        observed=d.get("observed"),
                        inputs_prefix=d.get("inputs_prefix") or [],
                    )
                )
        sim_status = str((sim_json or {}).get("status") or func_info.get("status") or "PASS")
        recorded_ids = set((trace_data.get("cases") or {}).keys())
        target_cases = (
            [c for c in task.get("tests", []) if c.get("id") in recorded_ids] if recorded_ids else task.get("tests", [])
        )
        sim_res = SimResult(
            status=sim_status,
            evaluated_cases=int(func_info.get("evaluated_cases") or len(recorded_ids)),
            passed_cases=int(func_info.get("passed_cases") or 0),
            failures=failures,
            raw=trace_data,
        )
        waveforms = waveform_builder(task, target_cases, sim_res, trace_path.parent)
        try:
            rel_trace = trace_path.relative_to(ws).as_posix()
        except ValueError:
            rel_trace = os.path.relpath(trace_path, ws).replace("\\", "/")
        return waveforms, {
            "kind": kind,
            "trace_relpath": rel_trace,
            "backend": trace_data.get("backend") or func_info.get("evidence") or "UNKNOWN",
            "acquisition": trace_data.get("acquisition") or func_info.get("acquisition") or "",
            "execution_verified": bool((sim_json or {}).get("execution_verified", True))
            if trace_data.get("backend") == "CODESYS_SIMULATION"
            else False,
            "observed_utc": trace_data.get("observed_utc"),
        }

    # Fall back to latest self-test simulation trace if selftest.json + sim_*/trace.json exist
    selftest_cases = _read_json_safe(ws / "selftest.json")
    if isinstance(selftest_cases, list) and selftest_cases:
        for sim_dir in sorted(ws.glob("sim_*"), reverse=True):
            trace_data = _read_json_safe(sim_dir / "trace.json")
            if isinstance(trace_data, dict) and trace_data.get("cases"):
                sim_json = _read_json_safe(sim_dir / "simulation_result.json") or {}
                sim_res = SimResult(
                    status=str(sim_json.get("status") or "PASS"),
                    evaluated_cases=int(sim_json.get("evaluated_cases") or len(selftest_cases)),
                    passed_cases=int(sim_json.get("passed_cases") or 0),
                    failures=[],
                    raw=trace_data,
                )
                waveforms = waveform_builder(task, selftest_cases, sim_res, sim_dir)
                return waveforms, {
                    "kind": "selftest",
                    "trace_relpath": str((sim_dir / "trace.json").relative_to(ws)),
                    "backend": trace_data.get("backend") or sim_json.get("backend") or "UNKNOWN",
                    "acquisition": trace_data.get("acquisition") or "",
                    "execution_verified": bool(sim_json.get("execution_verified", False)),
                    "observed_utc": trace_data.get("observed_utc"),
                }

    return [], {"kind": "none", "provenance": "No recorded simulation trace in workspace", "execution_verified": False}


def _resolve_run_source(ws: Path, root: Path) -> str:
    raw_root = (root / "results" / "raw").resolve()
    resolved = ws.resolve()
    if resolved.is_relative_to(raw_root):
        rel_parts = resolved.relative_to(raw_root).parts
        if rel_parts and rel_parts[0].startswith(("four_group_", "batch_", "six_task_")):
            return "fullflow"
        return "pilot"
    return "experiments"


def _summarize_run(ws: Path, root: Path, source: str) -> dict[str, Any]:
    result = _read_json_safe(ws / "result.json")
    parent_ctx = _load_parent_fullflow_context(ws)
    ff = parent_ctx.get("fullflow")
    effective_result = result if isinstance(result, dict) else (ff if (ws / "fullflow_result.json").is_file() else None)
    runtime_cfg = _read_json_safe(ws / "runtime_config.json")
    model_calls = _read_jsonl_safe(ws / "model_calls.jsonl")
    exec_events = _read_jsonl_safe(ws / "execution.jsonl")
    framework_kind = _detect_framework_kind(ws, effective_result, runtime_cfg)
    task_id = _infer_task_id(ws, effective_result)
    condition, campaign, group = _infer_condition_and_campaign(ws, root, source, effective_result, runtime_cfg)
    versions = _extract_versions(ws, framework_kind, include_diffs=False)
    if framework_kind == "star":
        stages = _build_star_stages(ws, result, runtime_cfg, model_calls, exec_events, versions, parent_ctx=parent_ctx)
    elif framework_kind == "fullflow":
        stages = _build_fullflow_stages(ws, ff)
    else:
        stages = _build_baseline_stages(ws, result)

    is_live = effective_result is None
    active_stage = next((s["id"] for s in stages if s["status"] == "RUNNING"), None)
    if not active_stage:
        done_stages = [s["id"] for s in stages if s["status"] in ("DONE", "PASS", "FAIL", "UNVERIFIED", "COUNTEREXAMPLE")]
        active_stage = done_stages[-1] if done_stages else stages[0]["id"]

    started_utc = (effective_result or {}).get("started_utc") or (runtime_cfg or {}).get("utc")
    if not started_utc and model_calls:
        started_utc = model_calls[0].get("utc")
    model_name = (effective_result or {}).get("model") or (runtime_cfg or {}).get("model")
    if not model_name and model_calls:
        model_name = model_calls[0].get("model")

    tokens = _extract_token_summary(model_calls, effective_result, ws)
    parent_func = (parent_ctx.get("functional") or {}).get("functional") or {}
    func = parent_func if parent_func.get("evaluated_cases") else ((effective_result or {}).get("functional") or {})
    llm_calls = (effective_result or {}).get("llm_calls")
    if llm_calls is None and isinstance(ff, dict):
        llm_calls = ff.get("new_llm_calls") if ff.get("new_llm_calls") else ff.get("source_llm_calls")
    formal_res = parent_ctx.get("formal") or ((ff or {}).get("formal")) or (effective_result or {}).get("verification")
    overall_status = (
        ff.get("status")
        if isinstance(ff, dict) and ff.get("status")
        else (effective_result or {}).get("status") or "RUNNING"
    )
    overall_reason = (
        (ff.get("reason") or ff.get("formal_detail") or ff.get("functional_detail"))
        if isinstance(ff, dict) and ff.get("status") and ff.get("status") != "PASS"
        else None
    ) or (effective_result or {}).get("reason") or ("Active live execution" if is_live else "")
    final_comp = (
        (effective_result or {}).get("final_compiled")
        if (effective_result or {}).get("final_compiled") is not None
        else (ff.get("compiled") if isinstance(ff, dict) else None)
    )
    formal_st = formal_res.get("status") if isinstance(formal_res, dict) else None
    display_status, partial_reason = resolve_showcase_outcome(
        overall_status,
        compiled=final_comp,
        fixed_status=func.get("status"),
        formal_status=formal_st,
        fixed_evaluated=func.get("evaluated_cases"),
        fixed_planned=func.get("planned_cases") or (ff.get("planned_cases") if isinstance(ff, dict) else None),
    )
    return {
        "run_id": ws.relative_to(root).as_posix(),
        "source": source,
        "group": group,
        "is_archived_pilot": source == "pilot",
        "state": "running" if is_live else "completed",
        "condition": condition,
        "campaign": campaign,
        "task_id": task_id,
        "framework": (effective_result or runtime_cfg or {}).get("framework")
        or (ff.get("driver") if isinstance(ff, dict) else None)
        or framework_kind,
        "framework_kind": framework_kind,
        "model": model_name or "",
        "ablation": (effective_result or runtime_cfg or {}).get("ablation"),
        "status": overall_status,
        "display_status": display_status,
        "partial_reason": partial_reason,
        "generation_status": (result or {}).get("status"),
        "fullflow_status": ff.get("status") if isinstance(ff, dict) else None,
        "formal_status": formal_st,
        "reason": overall_reason,
        "started_utc": started_utc or "",
        "finished_utc": (effective_result or {}).get("finished_utc"),
        "elapsed_seconds": (effective_result or {}).get("elapsed_seconds"),
        "llm_calls": llm_calls if llm_calls is not None else tokens["request_started_count"],
        "first_pass_compiled": (effective_result or {}).get("first_pass_compiled"),
        "final_compiled": final_comp,
        "repair_attempts": (effective_result or {}).get("repair_attempts"),
        "cegar_repairs": (effective_result or {}).get("cegar_repairs"),
        "passed_cases": func.get("passed_cases"),
        "evaluated_cases": func.get("evaluated_cases"),
        "current_stage": active_stage,
        "rollback_count": sum(1 for v in versions if v.get("rolled_back")),
        "total_tokens": tokens["total_tokens"],
        "_mtime": _latest_mtime(ws),
    }


def list_runs(root: Path) -> list[dict[str, Any]]:
    """List live experiments/, full-flow benchmark runs, and archived pilot workspaces."""
    runs: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    def _add_run(ws: Path, source: str) -> None:
        rid = ws.relative_to(root).as_posix()
        if rid in seen_ids:
            return
        seen_ids.add(rid)
        runs.append(_summarize_run(ws, root, source))

    exp_dir = root / "experiments"
    if exp_dir.is_dir():
        for dirpath, dirnames, _ in os.walk(exp_dir):
            current = Path(dirpath)
            if current != exp_dir and _is_run_workspace(current):
                _add_run(current, "experiments")
                dirnames[:] = []

    raw_dir = root / "results" / "raw"
    if raw_dir.is_dir():
        for batch in sorted(raw_dir.glob("four_group_*")):
            if not batch.is_dir():
                continue
            for group_dir in sorted(batch.iterdir()):
                if not group_dir.is_dir() or group_dir.name in ("invocations", "evaluation_time_normalization"):
                    continue
                for task_dir in sorted(group_dir.iterdir()):
                    if not task_dir.is_dir() or task_dir.name == "invocations":
                        continue
                    gen_dir = task_dir / "generation"
                    if _is_run_workspace(gen_dir):
                        _add_run(gen_dir, "fullflow")
                    elif (task_dir / "fullflow_result.json").is_file():
                        _add_run(task_dir, "fullflow")

        for pattern in ("batch_*", "six_task_*"):
            for batch in sorted(raw_dir.glob(pattern)):
                if not batch.is_dir():
                    continue
                for task_dir in sorted(batch.iterdir()):
                    if not task_dir.is_dir() or task_dir.name in ("code_snapshot", "invocations"):
                        continue
                    gen_dir = task_dir / "generation"
                    if _is_run_workspace(gen_dir):
                        _add_run(gen_dir, "fullflow")
                    elif (task_dir / "fullflow_result.json").is_file():
                        _add_run(task_dir, "fullflow")

        for batch in sorted(raw_dir.glob("pilot_pair_*")):
            if not batch.is_dir():
                continue
            for child in sorted(batch.iterdir()):
                if child.is_dir() and child.name not in _PILOT_IGNORED_DIRS and _is_run_workspace(child):
                    _add_run(child, "pilot")

    runs.sort(
        key=lambda r: (
            0 if r["state"] == "running" else 1,
            0 if r["source"] == "experiments" else (1 if r["source"] == "fullflow" else 2),
            -(r.pop("_mtime", 0.0)),
        ),
        reverse=False,
    )
    return runs


def inspect_run_trace(
    ws: Path,
    root: Path,
    tasks_by_id: dict[str, dict[str, Any]],
    waveform_builder: Callable[[dict, list[dict], SimResult, Path], list[dict[str, Any]]],
) -> dict[str, Any]:
    """Build full stage trace, candidate versions/diffs, timeline, and waveforms for one run."""
    result = _read_json_safe(ws / "result.json")
    parent_ctx = _load_parent_fullflow_context(ws)
    ff = parent_ctx.get("fullflow")
    effective_result = result if isinstance(result, dict) else (ff if (ws / "fullflow_result.json").is_file() else None)
    runtime_cfg = _read_json_safe(ws / "runtime_config.json")
    model_calls = _read_jsonl_safe(ws / "model_calls.jsonl")
    exec_events = _read_jsonl_safe(ws / "execution.jsonl")
    framework_kind = _detect_framework_kind(ws, effective_result, runtime_cfg)
    task_id = _infer_task_id(ws, effective_result)
    source = _resolve_run_source(ws, root)
    condition, campaign, group = _infer_condition_and_campaign(ws, root, source, effective_result, runtime_cfg)
    versions = _extract_versions(ws, framework_kind, include_diffs=True)
    if framework_kind == "star":
        stages = _build_star_stages(ws, result, runtime_cfg, model_calls, exec_events, versions, parent_ctx=parent_ctx)
    elif framework_kind == "fullflow":
        stages = _build_fullflow_stages(ws, ff)
    else:
        stages = _build_baseline_stages(ws, result)
    timeline = _build_timeline(ws, model_calls, exec_events)
    tokens = _extract_token_summary(model_calls, effective_result, ws)
    eval_task = _read_json_safe(ws / "evaluation_task.json")
    local_task = _read_json_safe(ws / "task.json")
    task = (
        eval_task
        if isinstance(eval_task, dict) and eval_task.get("tests")
        else (
            local_task
            if isinstance(local_task, dict) and local_task.get("tests")
            else (tasks_by_id.get(task_id) or eval_task or local_task)
        )
    )
    waveforms, waveform_source = _extract_waveforms(
        ws, task if isinstance(task, dict) else None, effective_result, waveform_builder, parent_ctx=parent_ctx
    )
    parent_formal = parent_ctx.get("formal") or ((ff or {}).get("formal"))
    harness_formal = (result or {}).get("verification") or (effective_result or {}).get("formal_verification")
    formal = _enrich_verification_ids(
        (
            _compact_verification_payload(parent_formal)
            or _compact_verification_payload(harness_formal)
            or (effective_result or {}).get("formal_verification")
            or {
                "status": "UNVERIFIED",
                "reason": "Candidate ST has no verified SMV encoding",
            }
        ),
        task if isinstance(task, dict) else None,
    )
    if isinstance(task, dict):
        for st in stages:
            if st.get("id") == "verify" and isinstance(st.get("detail"), dict):
                det = st["detail"]
                if det.get("fullflow_formal"):
                    det["fullflow_formal"] = _enrich_verification_ids(det["fullflow_formal"], task)
                if det.get("in_harness"):
                    det["in_harness"] = _enrich_verification_ids(det["in_harness"], task)
                if isinstance(det.get("attempts"), list):
                    det["attempts"] = [_enrich_verification_ids(a, task) for a in det["attempts"]]

    overall_status = (
        ff.get("status")
        if isinstance(ff, dict) and ff.get("status")
        else (effective_result or {}).get("status") or "RUNNING"
    )
    overall_reason = (
        (ff.get("reason") or ff.get("formal_detail") or ff.get("functional_detail"))
        if isinstance(ff, dict) and ff.get("status") and ff.get("status") != "PASS"
        else None
    ) or (effective_result or {}).get("reason") or ("Active live execution" if effective_result is None else "")
    parent_func = (parent_ctx.get("functional") or {}).get("functional") or {}
    func_res = parent_func if parent_func.get("evaluated_cases") else ((effective_result or {}).get("functional") or {})
    final_comp = (
        (effective_result or {}).get("final_compiled")
        if (effective_result or {}).get("final_compiled") is not None
        else (ff.get("compiled") if isinstance(ff, dict) else None)
    )
    display_status, partial_reason = resolve_showcase_outcome(
        overall_status,
        compiled=final_comp,
        fixed_status=func_res.get("status"),
        formal_status=formal.get("status") if isinstance(formal, dict) else None,
        fixed_evaluated=func_res.get("evaluated_cases"),
        fixed_planned=func_res.get("planned_cases") or (ff.get("planned_cases") if isinstance(ff, dict) else None),
    )
    return {
        "run_id": ws.relative_to(root).as_posix(),
        "source": source,
        "group": group,
        "is_archived_pilot": source == "pilot",
        "state": "running" if effective_result is None else "completed",
        "condition": condition,
        "campaign": campaign,
        "task_id": task_id,
        "framework": (effective_result or runtime_cfg or {}).get("framework")
        or (ff.get("driver") if isinstance(ff, dict) else None)
        or framework_kind,
        "framework_kind": framework_kind,
        "model": (effective_result or runtime_cfg or {}).get("model") or (model_calls[0].get("model") if model_calls else ""),
        "ablation": (effective_result or runtime_cfg or {}).get("ablation"),
        "status": overall_status,
        "display_status": display_status,
        "partial_reason": partial_reason,
        "generation_status": (result or {}).get("status"),
        "fullflow_status": ff.get("status") if isinstance(ff, dict) else None,
        "reason": overall_reason,
        "started_utc": (effective_result or {}).get("started_utc") or (runtime_cfg or {}).get("utc") or "",
        "finished_utc": (effective_result or {}).get("finished_utc"),
        "elapsed_seconds": (effective_result or {}).get("elapsed_seconds"),
        "stages": stages,
        "versions": versions,
        "timeline": timeline,
        "token_summary": tokens,
        "formal_verification": formal,
        "waveforms": waveforms,
        "waveform_source": waveform_source,
    }


def load_reference_st(task_id: str, root: Path) -> tuple[int, dict[str, Any]]:
    """Safely load a hand-designed reference ST example from codesys/examples/."""
    if not task_id or not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9_]+", task_id):
        return 400, {"error": f"Invalid task_id: '{task_id}'", "available": False}
    examples_root = (root / "codesys" / "examples").resolve()
    target = (examples_root / f"{task_id}.json").resolve()
    if not target.is_relative_to(examples_root) or not target.is_file():
        return 404, {"error": f"No reference ST example found for '{task_id}'", "task_id": task_id, "available": False}
    data = _read_json_safe(target)
    if not isinstance(data, dict):
        return 500, {
            "error": f"Failed to parse reference ST example for '{task_id}'",
            "task_id": task_id,
            "available": False,
        }
    return 200, {
        "task_id": task_id,
        "available": True,
        "source": target.relative_to(root).as_posix(),
        "declaration": data.get("declaration", ""),
        "implementation": data.get("implementation", ""),
        "supporting_objects": data.get("supporting_objects", []),
        "provenance": data.get("provenance", ""),
    }
