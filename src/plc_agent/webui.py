"""CODESYS STAR Auto-Testing & Waveform Agent Trace Inspector Web Platform.

Provides a standalone zero-dependency HTTP server with a rich single-page application
for exploring tasks, visualizing logic waveforms, inspecting agent traces,
and testing/verifying ST programs.
"""

from __future__ import annotations

import contextlib
import csv
import dataclasses
import http.server
import json
import re
import tempfile
import threading
import urllib.parse
import uuid
from pathlib import Path
from typing import Any

from .backend import Backend, CodesysBackend, FakeBackend, SimResult
from .common import ROOT, digest, read_json
from .config import Settings
from .dataset import load_tasks
from .formal_verify import export_verification_bundle, verify_candidate
from .functional import outputs_equal
from .random_testing import generate_random_cases
from .run_trace import (
    _is_run_workspace,
    inspect_run_trace,
    list_runs,
    load_reference_st,
    resolve_safe_run_dir,
    resolve_showcase_outcome,
)
from .smv_status import (
    build_all_smv_statuses,
    build_task_smv_status,
    probe_checker_availability,
    run_and_persist_smv_check,
)
from .symbol_glossary import build_symbol_glossary
from .task_view import agent_view


def _is_compiler_ready(settings: Settings) -> bool:
    ready = settings.compiler_ready()
    if isinstance(ready, bool):
        return ready
    if isinstance(ready, (list, tuple, set)):
        return len(ready) == 0
    return bool(ready)


def _safe_json_serialize(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, (list, tuple)):
        return [_safe_json_serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _safe_json_serialize(v) for k, v in obj.items()}
    return obj


def _build_step_waveforms(
    task: dict,
    cases: list[dict],
    sim_res: SimResult,
    workspace: Path,
) -> list[dict[str, Any]]:
    """Build detailed step-by-step logic signal waveforms with divergence highlighting."""
    # Check if a real execution trace was dumped in the workspace or raw result
    raw_cases: dict[str, Any] = {}
    if sim_res.raw and isinstance(sim_res.raw, dict):
        raw_cases = sim_res.raw.get("cases") or {}
    if not raw_cases:
        trace_file = workspace / "trace.json"
        if trace_file.is_file():
            try:
                trace_data = read_json(trace_file)
                raw_cases = trace_data.get("cases", {})
            except Exception:
                raw_cases = {}

    waveforms = []
    failure_map = {f.case_id: f for f in sim_res.failures}

    for case_idx, case in enumerate(cases):
        case_id = case.get("id", f"case_{case_idx + 1}")
        case_name = case.get("name", case_id)
        case_fail = failure_map.get(case_id)
        raw_case = raw_cases.get(case_id, {})
        raw_steps = raw_case.get("steps", []) if isinstance(raw_case, dict) else raw_case

        steps_data = []
        for step_idx, step in enumerate(case.get("steps", [])):
            inputs = step.get("inputs", {})
            expected = step.get("expected", {})
            dt_ms = step.get("dt_ms")

            if raw_steps and step_idx < len(raw_steps):
                obs = raw_steps[step_idx].get("outputs", raw_steps[step_idx])
                is_match = outputs_equal(task, obs, expected, inputs)
                divergence = None
                if not is_match:
                    diff_fields = [
                        k for k in expected if not outputs_equal(task, {k: obs.get(k)}, {k: expected.get(k)}, inputs)
                    ]
                    field_name = diff_fields[0] if diff_fields else next(iter(expected.keys()), "")
                    divergence = {
                        "field": field_name,
                        "expected": expected.get(field_name),
                        "observed": obs.get(field_name) if isinstance(obs, dict) else obs,
                    }
                steps_data.append(
                    {
                        "step": step_idx,
                        "inputs": inputs,
                        "expected": expected,
                        "observed": obs,
                        "dt_ms": dt_ms,
                        "match": is_match,
                        "divergence": divergence,
                    }
                )
            elif case_fail:
                if step_idx < case_fail.first_bad_step:
                    steps_data.append(
                        {
                            "step": step_idx,
                            "inputs": inputs,
                            "expected": expected,
                            "observed": None,
                            "dt_ms": dt_ms,
                            "match": None,
                            "divergence": None,
                        }
                    )
                elif step_idx == case_fail.first_bad_step:
                    obs = {case_fail.field: case_fail.observed}
                    steps_data.append(
                        {
                            "step": step_idx,
                            "inputs": inputs,
                            "expected": expected,
                            "observed": obs,
                            "dt_ms": dt_ms,
                            "match": False,
                            "divergence": {
                                "field": case_fail.field,
                                "expected": case_fail.expected,
                                "observed": case_fail.observed,
                            },
                        }
                    )
                else:
                    steps_data.append(
                        {
                            "step": step_idx,
                            "inputs": inputs,
                            "expected": expected,
                            "observed": None,
                            "dt_ms": dt_ms,
                            "match": None,
                            "divergence": None,
                        }
                    )
            else:
                steps_data.append(
                    {
                        "step": step_idx,
                        "inputs": inputs,
                        "expected": expected,
                        "observed": None,
                        "dt_ms": dt_ms,
                        "match": None,
                        "divergence": None,
                    }
                )

        waveforms.append(
            {
                "case_id": case_id,
                "name": case_name,
                "passed": False if case_fail else (True if raw_steps and sim_res.status == "PASS" else None),
                "steps": steps_data,
            }
        )

    return waveforms


def normalize_evidence_path(raw_path: str | None) -> str | None:
    if not raw_path or not isinstance(raw_path, str):
        return None
    cleaned = raw_path.strip().replace("\\", "/")
    if not cleaned:
        return None
    for marker in ("results/raw/", "experiments/", "results/summary/"):
        idx = cleaned.find(marker)
        if idx >= 0:
            return cleaned[idx:]
    return cleaned.lstrip("/") if re.match(r"^[A-Za-z]:/", cleaned) else cleaned


def _resolve_trace_run_id(active_root: Path, evidence_rel: str | None) -> str | None:
    cleaned = normalize_evidence_path(evidence_rel)
    if not cleaned:
        return None
    target = (active_root / cleaned).resolve()
    raw_root = (active_root / "results" / "raw").resolve()
    exp_root = (active_root / "experiments").resolve()
    task_dir = target.parent if target.is_file() else target
    if not (task_dir.is_relative_to(raw_root) or task_dir.is_relative_to(exp_root)):
        return None
    gen_dir = task_dir / "generation"
    if gen_dir.is_dir() and _is_run_workspace(gen_dir):
        return gen_dir.relative_to(active_root).as_posix()
    if task_dir.is_dir() and _is_run_workspace(task_dir):
        return task_dir.relative_to(active_root).as_posix()
    return None


def _extract_fixed_tests_summary(row: dict[str, Any]) -> dict[str, Any]:
    ft = row.get("fixed_tests")
    if isinstance(ft, dict) and ("status" in ft or "passed" in ft or "evaluated" in ft):
        return ft
    stages = row.get("stages") or {}
    func_stage = (stages.get("functional") or {}).get("result") or {}
    func = (
        func_stage.get("functional")
        if isinstance(func_stage.get("functional"), dict)
        else (row.get("functional") if isinstance(row.get("functional"), dict) else {})
    )
    planned = row.get("planned_cases") if row.get("planned_cases") is not None else func.get("planned_cases")
    if not func and func_stage:
        return {
            "status": str(func_stage.get("status") or ("NOT_RUN" if not row.get("compiled") else "UNKNOWN")),
            "passed": int(func_stage.get("passed_cases") or 0),
            "evaluated": int(func_stage.get("evaluated_cases") or 0),
            "planned": int(planned or 0),
        }
    return {
        "status": str(func.get("status") or func_stage.get("status") or "NOT_RUN"),
        "passed": int(func.get("passed_cases") or 0),
        "evaluated": int(func.get("evaluated_cases") or 0),
        "planned": int(planned or 0),
    }


def _extract_formal_summary(row: dict[str, Any]) -> dict[str, Any]:
    fm = row.get("formal")
    if isinstance(fm, dict) and "status" in fm:
        return fm
    stages = row.get("stages") or {}
    formal_stage = (stages.get("formal") or {}).get("result") or {}
    verif = row.get("verification") if isinstance(row.get("verification"), dict) else {}
    src = formal_stage if formal_stage.get("status") else verif
    if not src:
        return {"status": "NOT_RUN", "full_specification_verified": None}
    return {
        "status": str(src.get("status") or "NOT_RUN"),
        "full_specification_verified": src.get("full_specification_verified"),
    }


def normalize_benchmark_task_row(active_root: Path, row: dict[str, Any], group_id: str | None = None) -> dict[str, Any]:
    """Normalize a summary or matrix task record into the canonical WebUI benchmark row shape."""
    tid = str(row.get("task_id") or "")
    ev_rel = normalize_evidence_path(row.get("evidence") or row.get("matrix_evidence"))
    if not ev_rel and group_id and tid:
        candidate = active_root / "results" / "raw" / "codex_matrix_resume_20261114" / group_id / tid / "fullflow_result.json"
        if candidate.is_file():
            ev_rel = candidate.relative_to(active_root).as_posix()

    llm_calls = row.get("llm_calls")
    if llm_calls is None:
        llm_calls = row.get("source_llm_calls") if row.get("source_llm_calls") is not None else row.get("new_llm_calls")

    normalized = {
        "task_id": tid,
        "difficulty": row.get("difficulty") or "",
        "status": row.get("status") or "UNKNOWN",
        "compiled": row.get("compiled"),
        "generation_status": row.get("generation_status"),
        "fixed_tests": _extract_fixed_tests_summary(row),
        "formal": _extract_formal_summary(row),
        "llm_calls": llm_calls,
        "elapsed_seconds": row.get("elapsed_seconds"),
        "evidence": ev_rel,
    }
    enriched = _apply_showcase_task_outcome(normalized)
    enriched["trace_run_id"] = _resolve_trace_run_id(active_root, ev_rel)
    return enriched


def _apply_showcase_task_outcome(row: dict[str, Any]) -> dict[str, Any]:
    raw_st = str(row.get("status") or "UNKNOWN")
    ft = row.get("fixed_tests") or {}
    fm = row.get("formal") or {}
    disp_st, reason_tag = resolve_showcase_outcome(
        raw_st,
        compiled=row.get("compiled"),
        fixed_status=ft.get("status"),
        formal_status=fm.get("status"),
        fixed_evaluated=ft.get("evaluated"),
        fixed_planned=ft.get("planned"),
    )
    out = dict(row)
    out["raw_status"] = raw_st
    out["status"] = disp_st
    out["partial_reason"] = reason_tag
    return out


def _count_outcomes(tasks: list[dict[str, Any]], key: str = "status") -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in tasks:
        st = str(row.get(key) or "UNKNOWN")
        counts[st] = counts.get(st, 0) + 1
    return counts


def _compute_difficulty_breakdown(tasks: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    buckets: dict[str, dict[str, Any]] = {}
    for row in tasks:
        diff = str(row.get("difficulty") or "unknown")
        b = buckets.setdefault(
            diff,
            {
                "tasks": 0,
                "compiled": 0,
                "fixed_passed": 0,
                "fixed_evaluated": 0,
                "fixed_planned": 0,
                "formal_pass": 0,
                "pass": 0,
                "partial": 0,
                "fail": 0,
                "tool_error": 0,
                "timeout": 0,
            },
        )
        b["tasks"] += 1
        if row.get("compiled"):
            b["compiled"] += 1
        ft = row.get("fixed_tests") or {}
        b["fixed_passed"] += int(ft.get("passed") or 0)
        b["fixed_evaluated"] += int(ft.get("evaluated") or 0)
        b["fixed_planned"] += int(ft.get("planned") or 0)
        fm = row.get("formal") or {}
        if fm.get("status") == "PASS":
            b["formal_pass"] += 1
        st = str(row.get("status") or "")
        if st == "PASS":
            b["pass"] += 1
        elif st == "PARTIAL":
            b["partial"] += 1
        elif st == "FAIL":
            b["fail"] += 1
        elif st == "TOOL_ERROR":
            b["tool_error"] += 1
        elif st == "TIMEOUT":
            b["timeout"] += 1
    return buckets


_GROUP_ORDER = {
    "star_deepseek": 0,
    "star_terra": 1,
    "codex_deepseek": 2,
    "codex_terra": 3,
    "six_task_fullflow": 10,
    "codex_cli_pilot": 11,
    "early_pilot_pair": 20,
}
_TIER_ORDER = {"primary": 0, "subset": 1, "archived_pilot": 2}


def _driver_display_label(driver: str) -> str:
    low = (driver or "").strip().lower()
    if low in ("codex_cli", "codex"):
        return "Codex CLI"
    if low == "star":
        return "STAR"
    return driver.upper() or "Run"


def _build_benchmark_groups(active_root: Path, summaries: dict[str, Any]) -> dict[str, Any]:
    groups: list[dict[str, Any]] = []
    seen_group_ids: set[str] = set()
    interpretations: list[str] = []

    # Load dedicated cohort summaries before composite snapshots so clean cohort files take precedence.
    ordered_items = sorted(
        summaries.items(),
        key=lambda kv: (1 if "snapshot" in kv[0] else 0, kv[0]),
    )

    for stem, payload in ordered_items:
        if not isinstance(payload, dict) or not isinstance(payload.get("groups"), list):
            continue
        if payload.get("interpretation"):
            interp = payload["interpretation"]
            if isinstance(interp, list):
                interpretations.extend(str(x) for x in interp if x)
            else:
                interpretations.append(str(interp))
        for raw_g in payload["groups"]:
            if not isinstance(raw_g, dict):
                continue
            gid = str(raw_g.get("group_id") or stem)
            if gid in seen_group_ids:
                continue
            seen_group_ids.add(gid)
            tasks_out = [
                normalize_benchmark_task_row(active_root, t_row, group_id=gid)
                for t_row in (raw_g.get("tasks") or [])
                if isinstance(t_row, dict)
            ]
            driver = str(raw_g.get("driver") or "")
            driver_label = _driver_display_label(driver)
            model = str(raw_g.get("model") or "")
            cond = str(raw_g.get("condition") or "")
            formal_counts = raw_g.get("formal_status_counts") or {}
            if not formal_counts and tasks_out:
                for row in tasks_out:
                    fst = str((row.get("formal") or {}).get("status") or "UNKNOWN")
                    formal_counts[fst] = formal_counts.get(fst, 0) + 1
            groups.append(
                {
                    "group_id": gid,
                    "source_file": f"results/summary/{stem}.json",
                    "date": str(payload.get("date") or ""),
                    "tier": "primary",
                    "archived": False,
                    "title_en": f"{driver_label} · {model}" + (f" ({cond})" if cond else ""),
                    "title_zh": f"{driver_label} · {model}" + (f" ({cond})" if cond else ""),
                    "driver": driver,
                    "model": model,
                    "condition": cond,
                    "completed_tasks": int(raw_g.get("completed_tasks") or len(tasks_out)),
                    "planned_tasks": int(raw_g.get("planned_tasks") or len(tasks_out)),
                    "compiled_tasks": int(raw_g.get("compiled_tasks") or 0),
                    "fixed_cases": raw_g.get("fixed_cases") or {},
                    "formal_status_counts": formal_counts,
                    "outcome_counts": _count_outcomes(tasks_out, "status"),
                    "raw_outcome_counts": raw_g.get("outcome_counts") or _count_outcomes(tasks_out, "raw_status"),
                    "difficulty_breakdown": _compute_difficulty_breakdown(tasks_out),
                    "tasks": tasks_out,
                }
            )

    six_csv = active_root / "results" / "summary" / "six_task_fullflow_20261114.csv"
    if six_csv.is_file():
        try:
            with six_csv.open("r", encoding="utf-8-sig", newline="") as f:
                csv_rows = list(csv.DictReader(f))
            if csv_rows:
                tasks_out = []
                formal_counts: dict[str, int] = {}
                compiled_n = passed_c = eval_c = plan_c = 0
                for row in csv_rows:
                    tid = row.get("task", "")
                    comp = str(row.get("compiled", "")).lower() == "true"
                    p_n = int(row.get("passed_cases") or 0)
                    e_n = int(row.get("evaluated_cases") or 0)
                    pl_n = int(row.get("planned_cases") or 0)
                    f_st = row.get("formal_status") or "UNKNOWN"
                    ff_st = row.get("fullflow_status") or "UNKNOWN"
                    if comp:
                        compiled_n += 1
                    passed_c += p_n
                    eval_c += e_n
                    plan_c += pl_n
                    formal_counts[f_st] = formal_counts.get(f_st, 0) + 1
                    ev_rel = f"results/raw/batch_fresh_20261114/{tid}/fullflow_result.json"
                    tasks_out.append(
                        _apply_showcase_task_outcome(
                            {
                                "task_id": tid,
                                "difficulty": row.get("difficulty") or "",
                                "status": ff_st,
                                "compiled": comp,
                                "generation_status": "PASS",
                                "fixed_tests": {
                                    "status": "PASS" if p_n == e_n and e_n == pl_n and e_n > 0 else "PARTIAL",
                                    "passed": p_n,
                                    "evaluated": e_n,
                                    "planned": pl_n,
                                },
                                "formal": {"status": f_st, "full_specification_verified": False if f_st == "PASS" else None},
                                "llm_calls": None,
                                "evidence": ev_rel,
                                "trace_run_id": _resolve_trace_run_id(active_root, ev_rel),
                            }
                        )
                    )
                groups.append(
                    {
                        "group_id": "six_task_fullflow",
                        "source_file": "results/summary/six_task_fullflow_20261114.csv",
                        "date": "2026-11-14",
                        "tier": "subset",
                        "archived": False,
                        "title_en": "STAR · deepseek-v4.1-flash-1017 (6-Task Re-check)",
                        "title_zh": "STAR · deepseek-v4.1-flash-1017（6 题完整流程重测）",
                        "driver": "star",
                        "model": "deepseek-v4.1-flash-1017",
                        "condition": "E3",
                        "completed_tasks": len(tasks_out),
                        "planned_tasks": len(tasks_out),
                        "compiled_tasks": compiled_n,
                        "fixed_cases": {"passed": passed_c, "evaluated": eval_c, "planned": plan_c},
                        "formal_status_counts": formal_counts,
                        "outcome_counts": _count_outcomes(tasks_out, "status"),
                        "raw_outcome_counts": _count_outcomes(tasks_out, "raw_status"),
                        "difficulty_breakdown": _compute_difficulty_breakdown(tasks_out),
                        "tasks": tasks_out,
                    }
                )
        except Exception:
            pass

    codex_pilot = summaries.get("codex_cli_pilot_20261114")
    if isinstance(codex_pilot, dict) and codex_pilot.get("task_id"):
        ft = codex_pilot.get("fixed_tests") or {}
        fv = codex_pilot.get("formal_verification") or {}
        overall = str(codex_pilot.get("overall") or "UNVERIFIED")
        f_st = str(fv.get("status") or "UNKNOWN")
        tid = str(codex_pilot["task_id"])
        task_entry = _apply_showcase_task_outcome(
            {
                "task_id": tid,
                "difficulty": "easy",
                "status": overall,
                "compiled": codex_pilot.get("compile") == "PASS",
                "generation_status": codex_pilot.get("generation_status"),
                "fixed_tests": {
                    "status": ft.get("status"),
                    "passed": ft.get("passed", 0),
                    "evaluated": ft.get("executed", 0),
                    "planned": ft.get("planned", 0),
                },
                "formal": {
                    "status": f_st,
                    "full_specification_verified": fv.get("full_specification_verified"),
                },
                "llm_calls": codex_pilot.get("requests"),
                "elapsed_seconds": codex_pilot.get("elapsed_seconds"),
                "evidence": codex_pilot.get("evidence_note"),
                "trace_run_id": None,
            }
        )
        groups.append(
            {
                "group_id": "codex_cli_pilot",
                "source_file": "results/summary/codex_cli_pilot_20261114.json",
                "date": str(codex_pilot.get("date") or ""),
                "tier": "subset",
                "archived": False,
                "title_en": f"Codex CLI · {codex_pilot.get('model', '')} (Pilot 1/1)",
                "title_zh": f"Codex CLI · {codex_pilot.get('model', '')}（试测 1 题）",
                "driver": str(codex_pilot.get("driver") or "codex_cli"),
                "model": str(codex_pilot.get("model") or ""),
                "condition": "codex_cli",
                "completed_tasks": 1,
                "planned_tasks": 1,
                "compiled_tasks": 1 if task_entry["compiled"] else 0,
                "fixed_cases": {
                    "passed": int(ft.get("passed") or 0),
                    "evaluated": int(ft.get("executed") or 0),
                    "planned": int(ft.get("planned") or 0),
                },
                "formal_status_counts": {f_st: 1},
                "outcome_counts": _count_outcomes([task_entry], "status"),
                "raw_outcome_counts": _count_outcomes([task_entry], "raw_status"),
                "difficulty_breakdown": _compute_difficulty_breakdown([task_entry]),
                "tasks": [task_entry],
                "note": codex_pilot.get("evidence_note"),
            }
        )

    pilot_latest = summaries.get("pilot_pair_latest")
    if isinstance(pilot_latest, dict) and isinstance(pilot_latest.get("statuses"), dict):
        statuses = pilot_latest["statuses"]
        pilot_tasks = []
        outcome_counts: dict[str, int] = {}
        compiled_n = 0
        for tid, st in statuses.items():
            st_s = str(st)
            outcome_counts[st_s] = outcome_counts.get(st_s, 0) + 1
            if st_s == "PASS":
                compiled_n += 1
            pilot_tasks.append(
                {
                    "task_id": tid,
                    "difficulty": "easy",
                    "status": st_s,
                    "compiled": st_s == "PASS",
                    "generation_status": st_s,
                    "fixed_tests": {"status": st_s, "passed": None, "evaluated": None, "planned": None},
                    "formal": {"status": "UNVERIFIED", "full_specification_verified": None},
                    "llm_calls": None,
                    "evidence": "results/summary/pilot_pair_latest.json",
                    "trace_run_id": None,
                }
            )
        groups.append(
            {
                "group_id": "early_pilot_pair",
                "source_file": "results/summary/pilot_pair_latest.json",
                "date": "2026-11-10",
                "tier": "archived_pilot",
                "archived": True,
                "title_en": "Early Pilot Pair (Pre-CEGAR 2026-11-10)",
                "title_zh": "前期两题试跑归档（CEGAR 上线前）",
                "driver": "star_early_pilot",
                "model": "early-pilot",
                "condition": "pilot",
                "completed_tasks": len(pilot_tasks),
                "planned_tasks": len(pilot_tasks),
                "compiled_tasks": compiled_n,
                "fixed_cases": {},
                "formal_status_counts": {"UNVERIFIED": len(pilot_tasks)},
                "outcome_counts": outcome_counts,
                "difficulty_breakdown": _compute_difficulty_breakdown(pilot_tasks),
                "tasks": pilot_tasks,
            }
        )

    groups.sort(key=lambda g: (_TIER_ORDER.get(g.get("tier", ""), 99), _GROUP_ORDER.get(g.get("group_id", ""), 99)))
    unique_interps = list(dict.fromkeys(interpretations))
    return {
        "benchmark_groups": groups,
        "interpretation": (
            (unique_interps[0] + " ") if unique_interps else ""
        )
        + "Display status classifies compiled + 100% planned fixed tests PASS + coupled SMV checks PASS as PASS; PARTIAL strictly retains Reason 2 (UNSUPPORTED_ST or incomplete fixed-test execution). Raw archive statuses remain preserved on disk.",
    }


def handle_api_request(
    method: str,
    path: str,
    query: dict,
    body: dict | None,
    settings: Settings,
    backend: Backend | None = None,
    smv_status_path: Path | None = None,
    evidence_root: Path | None = None,
    workspace_root: Path | None = None,
) -> tuple[int, dict]:
    """Dispatch API request to internal handlers and return (status_code, json_dict)."""
    method = method.upper()
    resolved_status_path = smv_status_path or getattr(settings, "smv_status_path", None)
    active_root = workspace_root or ROOT

    def get_query_param(name: str) -> str | None:
        val = query.get(name)
        if isinstance(val, list):
            return str(val[0]) if val else None
        return str(val) if val is not None else None

    review_path = ROOT / "configs/pilot_review.json"
    pilot_items = read_json(review_path).get("tasks", []) if review_path.is_file() else []
    all_review_path = ROOT / "configs/task_review_zh.json"
    review_items = read_json(all_review_path).get("tasks", []) if all_review_path.is_file() else pilot_items
    review_by_id = {r["id"]: r for r in review_items}

    if method == "POST" and path == "/api/check-reference-model":
        # Fixed whitelisted tasks & variants only: never execute a browser-supplied path or command.
        if not isinstance(body, dict):
            return 400, {"error": "Request body must be a JSON object"}
        task_id = body.get("task_id")
        variant = body.get("variant")
        known_ids = {t["id"] for t in load_tasks()}
        if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9_]+", task_id) or task_id not in known_ids:
            return 400, {"error": f"Unsupported or invalid task_id: '{task_id}'"}
        if variant is not None and (not isinstance(variant, str) or variant not in ("reference", "complete", "mutant")):
            return 400, {"error": f"Unsupported SMV variant: '{variant}'"}
        return run_and_persist_smv_check(task_id, variant, status_path=resolved_status_path)

    # 1. GET /api/tasks
    if method == "GET" and path == "/api/tasks":
        tasks = load_tasks()
        smv_statuses = build_all_smv_statuses([t["id"] for t in tasks], status_path=resolved_status_path)
        task_list = [
            {
                "id": t["id"],
                "title": t.get("title", ""),
                "kind": t.get("kind", ""),
                "difficulty": t.get("difficulty", ""),
                "tests_count": len(t.get("tests", [])),
                "steps_count": sum(len(c.get("steps", [])) for c in t.get("tests", [])),
                "properties_count": len(t.get("ltl", [])),
                "smv_status": smv_statuses[t["id"]],
            }
            for t in tasks
        ]
        return 200, {
            "tasks": task_list,
            "total": len(task_list),
            "pilot_review": pilot_items,
            "task_review": review_items,
            "checker_availability": probe_checker_availability(),
        }

    # 2. GET /api/task?id=...
    if method == "GET" and path == "/api/task":
        task_id = get_query_param("id")
        if not task_id:
            return 400, {"error": "Missing required query parameter: 'id'"}
        tasks = load_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return 404, {"error": f"Task '{task_id}' not found"}
        rand_cases = generate_random_cases(task)
        review = review_by_id.get(task_id)
        if review:
            review = dict(review, source_matches=review.get("source_task_sha256") == digest(task))
        return 200, {
            "task": task,
            "agent_view": agent_view(task),
            "tests": task.get("tests", []),
            "random_cases": rand_cases,
            "review": review,
            "symbol_glossary": build_symbol_glossary(task, review),
            "smv_status": build_task_smv_status(task_id, status_path=resolved_status_path),
            "task_sha256": digest(task),
        }

    # 3. POST /api/evaluate
    if method == "POST" and path == "/api/evaluate":
        if not body or not isinstance(body, dict):
            return 400, {"error": "Request body must be a JSON object"}
        task_id = body.get("task_id")
        if not task_id:
            return 400, {"error": "Missing required field: 'task_id'"}
        candidate = body.get("candidate")
        if candidate is None:
            return 400, {"error": "Missing required field: 'candidate'"}

        tasks = load_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return 404, {"error": f"Task '{task_id}' not found"}

        if backend is None:
            if _is_compiler_ready(settings):
                backend = CodesysBackend(settings)
            else:
                return 503, {
                    "error": "CODESYS is not configured; candidate execution was not performed",
                    "status": "UNVERIFIED",
                }

        resolved_evidence_root = evidence_root or (ROOT / ".local" / "webui_evidence")
        with contextlib.nullcontext(resolved_evidence_root / uuid.uuid4().hex) as tmpdir:
            workspace = Path(tmpdir)
            compile_res = backend.compile(task, candidate, workspace / "compile")

            cases = list(task.get("tests", []))
            if body.get("include_random", False):
                cases.extend(generate_random_cases(task))

            if not compile_res.success:
                sim_res = SimResult(
                    status=compile_res.status,
                    passed_cases=0,
                    evaluated_cases=0,
                    failures=[],
                    infrastructure_error=compile_res.infrastructure_error,
                )
                waveform: list[dict] = []
            else:
                sim_res = backend.simulate(task, candidate, cases, workspace / "simulate")
                waveform = _build_step_waveforms(task, cases, sim_res, workspace / "simulate")

            return 200, {
                "evidence_workspace": str(workspace),
                "execution_kind": "FAKE_REFERENCE_ONLY" if isinstance(backend, FakeBackend) else "CODESYS",
                "compile": _safe_json_serialize(compile_res),
                "simulation": _safe_json_serialize(sim_res),
                "waveform": waveform,
            }

    # 4. GET /api/experiments
    if method == "GET" and path == "/api/experiments":
        summaries: dict[str, Any] = {}
        summary_dir = active_root / "results/summary"
        if summary_dir.is_dir():
            for f in sorted(summary_dir.glob("*.json")):
                try:
                    summaries[f.stem] = read_json(f)
                except Exception:
                    pass

        conditions = []
        cfg_path = active_root / "configs/experiments.json"
        if cfg_path.is_file():
            try:
                conditions = read_json(cfg_path).get("conditions", [])
            except Exception:
                conditions = []

        metrics = summaries.get("metrics")
        campaign = summaries.get("campaign")
        bench_bundle = _build_benchmark_groups(active_root, summaries)
        return 200, {
            "metrics": metrics,
            "campaign": campaign,
            "conditions": conditions,
            "summaries": summaries,
            "benchmark_groups": bench_bundle["benchmark_groups"],
            "interpretation": bench_bundle["interpretation"],
        }

    # 4b. GET /api/runs
    if method == "GET" and path == "/api/runs":
        runs = list_runs(active_root)
        return 200, {
            "runs": runs,
            "total": len(runs),
            "active_count": sum(1 for r in runs if r["state"] == "running"),
        }

    # 4c. GET /api/run-trace?run=...
    if method == "GET" and path == "/api/run-trace":
        run_rel = get_query_param("run") or ""
        ws, code, err_msg = resolve_safe_run_dir(active_root, run_rel)
        if ws is None:
            return code, {"error": err_msg}
        tasks_by_id = {t["id"]: t for t in load_tasks()}
        return 200, inspect_run_trace(ws, active_root, tasks_by_id, _build_step_waveforms)

    # 4d. GET /api/reference-st?id=...
    if method == "GET" and path == "/api/reference-st":
        task_id = get_query_param("id") or ""
        return load_reference_st(task_id, active_root)

    # 5. POST /api/export-verify
    if method == "POST" and path == "/api/export-verify":
        if not body or not isinstance(body, dict):
            return 400, {"error": "Request body must be a JSON object"}
        task_id = body.get("task_id")
        if not task_id:
            return 400, {"error": "Missing required field: 'task_id'"}
        candidate = body.get("candidate")
        if candidate is None:
            return 400, {"error": "Missing required field: 'candidate'"}

        tasks = load_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return 404, {"error": f"Task '{task_id}' not found"}

        out_dir_str = body.get("out_dir")
        if out_dir_str:
            out_dir = Path(out_dir_str)
        else:
            out_dir = Path(tempfile.mkdtemp(prefix=f"star_verify_{task_id}_"))

        out_dir.mkdir(parents=True, exist_ok=True)
        manifest = export_verification_bundle(task, candidate, out_dir)

        st_file = out_dir / manifest.get("st_path", "candidate.st")
        ltl_file = out_dir / manifest.get("ltl_path", "spec.ltl")
        st_content = st_file.read_text(encoding="utf-8") if st_file.is_file() else ""
        ltl_content = ltl_file.read_text(encoding="utf-8") if ltl_file.is_file() else ""

        return 200, {
            "status": "PASS",
            "manifest": manifest,
            "bundle_dir": str(out_dir),
            "files": {
                "st_path": str(st_file),
                "ltl_path": str(ltl_file),
                "manifest_path": str(out_dir / "verification_manifest.json"),
            },
            "candidate_st": st_content,
            "spec_ltl": ltl_content,
        }

    # 5b. POST /api/verify-candidate
    if method == "POST" and path == "/api/verify-candidate":
        if not body or not isinstance(body, dict):
            return 400, {"error": "Request body must be a JSON object"}
        task_id = body.get("task_id")
        if not task_id:
            return 400, {"error": "Missing required field: 'task_id'"}
        candidate = body.get("candidate")
        if candidate is None:
            return 400, {"error": "Missing required field: 'candidate'"}

        tasks = load_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return 404, {"error": f"Task '{task_id}' not found"}

        out_dir_str = body.get("out_dir")
        out_dir = Path(out_dir_str) if out_dir_str else Path(tempfile.mkdtemp(prefix=f"star_st_verify_{task_id}_"))
        out_dir.mkdir(parents=True, exist_ok=True)
        timeout = int(body.get("timeout") or 30)
        ver_res = verify_candidate(task=task, candidate=candidate, out_dir=out_dir, timeout=timeout)
        smv_path = Path(ver_res["smv_path"]) if ver_res.get("smv_path") else None
        smv_text = smv_path.read_text(encoding="utf-8", errors="replace") if smv_path and smv_path.is_file() else ""
        return 200, {**ver_res, "bundle_dir": str(out_dir), "smv_text": smv_text}

    return 404, {"error": f"Not found: {method} {path}"}


def render_index_html() -> str:
    """Inline local assets so the reviewer UI has no CDN/network dependencies."""
    assets = Path(__file__).parent / "webui_assets"
    html = (assets / "index.html").read_text(encoding="utf-8")
    script = (assets / "app.js").read_text(encoding="utf-8")
    return html.replace("/*__APP_SCRIPT__*/", script)


class WebUIRequestHandler(http.server.BaseHTTPRequestHandler):
    """Custom HTTP handler dispatching static HTML UI and REST API."""

    def __init__(self, *args, settings: Settings, backend: Backend | None = None, **kwargs) -> None:
        self.settings = settings
        self.backend = backend
        super().__init__(*args, **kwargs)

    def log_message(self, format: str, *args) -> None:
        # Suppress routine log messages during automated testing
        pass

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html", "/index.htm"):
            html = render_index_html()
            encoded = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return

        if parsed.path.startswith("/api/"):
            query = urllib.parse.parse_qs(parsed.query)
            status, data = handle_api_request("GET", parsed.path, query, None, self.settings, backend=self.backend)
            body_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body_bytes)))
            self.end_headers()
            self.wfile.write(body_bytes)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith("/api/"):
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                body = json.loads(raw_body.decode("utf-8")) if raw_body else {}
            except Exception:
                body = None

            query = urllib.parse.parse_qs(parsed.query)
            status, data = handle_api_request("POST", parsed.path, query, body, self.settings, backend=self.backend)
            body_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body_bytes)))
            self.end_headers()
            self.wfile.write(body_bytes)
            return

        self.send_response(404)
        self.end_headers()


def serve_webui(
    host: str = "127.0.0.1",
    port: int = 8765,
    settings: Settings | None = None,
    stop_event: threading.Event | None = None,
    bound_port_box: list[int] | None = None,
) -> None:
    """Run interactive Auto-Testing & Waveform Trace Inspector Web server."""
    cfg = settings or Settings.load()

    def handler_factory(*args, **kwargs):
        return WebUIRequestHandler(*args, settings=cfg, **kwargs)

    server = http.server.HTTPServer((host, port), handler_factory)
    actual_port = server.server_port
    if bound_port_box is not None and len(bound_port_box) > 0:
        bound_port_box[0] = actual_port

    if stop_event is not None:
        server.timeout = 0.2
        while not stop_event.is_set():
            server.handle_request()
        server.server_close()
    else:
        print(f"🚀 CODESYS STAR WebUI running at http://{host}:{actual_port}/")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
