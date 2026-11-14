"""Inventory, checker-availability probing, and persisted verification status for explicit SMV models."""

from __future__ import annotations

import hashlib
import os
import re
import uuid
from pathlib import Path
from typing import Any

from . import model_checker
from .common import ROOT, now, read_json, write_json

DEFAULT_SMV_STATUS_PATH = ROOT / "configs" / "smv_verification_status.json"
DEFAULT_MODELS_DIR = ROOT / "models"
SMV_VARIANTS = ("reference", "complete", "mutant")


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _detect_model_requirements(smv_path: Path) -> tuple[str, str]:
    text = smv_path.read_text(encoding="utf-8-sig")
    stripped = re.sub(r"--[^\n]*", "", text)
    if model_checker._needs_smt_engine(stripped):
        return "smt", "nuXmv"
    return "bdd", "NuSMV/nuXmv"


def probe_checker_availability() -> dict[str, Any]:
    """Safely probe local/PATH NuSMV and nuXmv availability without throwing."""
    result: dict[str, Any] = {
        "nusmv_available": False,
        "nusmv_exe": None,
        "nusmv_error": None,
        "nuxmv_available": False,
        "nuxmv_exe": None,
        "nuxmv_error": None,
    }
    try:
        exe = model_checker.find_nusmv()
        result["nusmv_available"] = True
        result["nusmv_exe"] = str(exe)
    except ValueError as exc:
        result["nusmv_error"] = str(exc)

    try:
        exe_x = model_checker.find_nuxmv()
        result["nuxmv_available"] = True
        result["nuxmv_exe"] = str(exe_x)
    except ValueError as exc:
        result["nuxmv_error"] = str(exc)
    return result


def _is_checker_available_for(required_engine: str, availability: dict[str, Any]) -> bool:
    if required_engine == "smt":
        return bool(availability.get("nuxmv_available"))
    return bool(availability.get("nusmv_available") or availability.get("nuxmv_available"))


def discover_task_smv_files(task_id: str, models_dir: Path | None = None) -> dict[str, Path]:
    base = models_dir or DEFAULT_MODELS_DIR
    found: dict[str, Path] = {}
    for variant in SMV_VARIANTS:
        candidate = base / f"{task_id}_{variant}.smv"
        if candidate.is_file():
            found[variant] = candidate
    return found


def load_smv_status_store(status_path: Path | None = None) -> dict[str, Any]:
    target = status_path or DEFAULT_SMV_STATUS_PATH
    if target.is_file():
        try:
            data = read_json(target)
            if isinstance(data, dict) and isinstance(data.get("records"), dict):
                return data
        except Exception:
            pass
    return {
        "schema_version": 1,
        "scope": "EXPLICIT_SMV_MODEL_ONLY",
        "updated_utc": None,
        "records": {},
    }


def save_smv_status_store(store: dict[str, Any], status_path: Path | None = None) -> None:
    target = status_path or DEFAULT_SMV_STATUS_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(store)
    payload.setdefault("schema_version", 1)
    payload["scope"] = "EXPLICIT_SMV_MODEL_ONLY"
    payload["updated_utc"] = now()
    tmp_path = target.with_name(f".{target.name}.{uuid.uuid4().hex}.tmp")
    write_json(tmp_path, payload)
    os.replace(tmp_path, target)


def _variant_passed_expectation(variant: str, status: str | None) -> bool:
    if variant == "mutant":
        return status == "COUNTEREXAMPLE"
    return status == "MODEL_PROPERTIES_TRUE"


def _effective_variant_status(
    variant: str,
    live_sha256: str,
    persisted: dict[str, Any] | None,
    checker_missing: bool,
) -> tuple[str, bool]:
    if not persisted:
        return ("CHECKER_MISSING" if checker_missing else "UNVERIFIED"), False

    p_status = persisted.get("status")
    p_sha = persisted.get("model_sha256")
    if p_status == "CHECKER_MISSING":
        if checker_missing:
            return "CHECKER_MISSING", False
        return "UNVERIFIED", False

    if p_sha and p_sha != live_sha256:
        return "STALE", True

    if p_status in {"MODEL_PROPERTIES_TRUE", "COUNTEREXAMPLE", "TOOL_ERROR", "TIMEOUT"}:
        return str(p_status), False

    return ("CHECKER_MISSING" if checker_missing else "UNVERIFIED"), False


def _authoring_labels(authored_variants: list[str], required_engine: str) -> tuple[str, str]:
    if not authored_variants:
        return "SMV: 未编写", "SMV: Not authored"
    tag_map_zh = {"reference": "参考", "complete": "完整", "mutant": "变异"}
    tag_map_en = {"reference": "Ref", "complete": "Complete", "mutant": "Mutant"}
    eng = required_engine.upper()
    zh = f"SMV({eng}): " + "+".join(tag_map_zh.get(v, v) for v in authored_variants)
    en = f"SMV({eng}): " + "+".join(tag_map_en.get(v, v) for v in authored_variants)
    return zh, en


def build_task_smv_status(
    task_id: str,
    *,
    store: dict[str, Any] | None = None,
    status_path: Path | None = None,
    models_dir: Path | None = None,
    availability: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build combined authoring + persisted + live checker status for one task."""
    avail = availability if availability is not None else probe_checker_availability()
    loaded_store = store if store is not None else load_smv_status_store(status_path)
    task_record = (loaded_store.get("records") or {}).get(task_id) or {}
    persisted_models = task_record.get("models") or {}

    files = discover_task_smv_files(task_id, models_dir=models_dir)
    authored_variants = [v for v in SMV_VARIANTS if v in files]

    if not authored_variants:
        auth_zh, auth_en = _authoring_labels([], "bdd")
        return {
            "task_id": task_id,
            "scope": "EXPLICIT_SMV_MODEL_ONLY",
            "candidate_st_verified": False,
            "authored": False,
            "authored_variants": [],
            "required_engine": None,
            "required_tool": None,
            "checker_available": True,
            "checker_missing": False,
            "stale": False,
            "verification_status": "NOT_AUTHORED",
            "persisted_record_present": bool(persisted_models),
            "live_rerunnable": False,
            "last_checked_utc": task_record.get("last_checked_utc"),
            "last_run_attempt": task_record.get("last_run_attempt"),
            "authoring_text_zh": auth_zh,
            "authoring_text_en": auth_en,
            "badge_text_zh": "未编写 SMV",
            "badge_text_en": "Not authored",
            "badge_tone": "muted",
            "checker_availability": avail,
            "models": {},
        }

    variant_details: dict[str, Any] = {}
    task_needs_smt = False
    any_missing = False
    any_stale = False
    latest_checked_utc: str | None = task_record.get("last_checked_utc")

    for variant in authored_variants:
        path = files[variant]
        live_sha = _file_sha256(path)
        req_engine, req_tool = _detect_model_requirements(path)
        if req_engine == "smt":
            task_needs_smt = True
        v_checker_missing = not _is_checker_available_for(req_engine, avail)
        if v_checker_missing:
            any_missing = True
        rec = persisted_models.get(variant)
        eff_status, is_stale = _effective_variant_status(variant, live_sha, rec, v_checker_missing)
        if is_stale:
            any_stale = True
        checked_utc = rec.get("checked_utc") if rec else None
        if checked_utc and (latest_checked_utc is None or checked_utc > latest_checked_utc):
            latest_checked_utc = checked_utc
        try:
            rel_path = path.relative_to(ROOT).as_posix()
        except ValueError:
            rel_path = str(path)

        variant_details[variant] = {
            "variant": variant,
            "path": rel_path,
            "model_sha256": live_sha,
            "recorded_model_sha256": rec.get("model_sha256") if rec else None,
            "required_engine": req_engine,
            "required_tool": req_tool,
            "checker_missing": v_checker_missing,
            "stale": is_stale,
            "persisted_status": rec.get("status") if rec else None,
            "effective_status": eff_status,
            "expected_pass": _variant_passed_expectation(variant, eff_status),
            "expected_properties": rec.get("expected_properties") if rec else None,
            "checked_properties": rec.get("checked_properties") if rec else None,
            "passed_count": rec.get("passed_count") if rec else None,
            "failed_count": rec.get("failed_count") if rec else None,
            "tool": rec.get("tool") if rec else None,
            "engine": rec.get("engine") if rec else None,
            "checked_utc": checked_utc,
            "error": rec.get("error") if rec else None,
        }

    req_engine = "smt" if task_needs_smt else "bdd"
    req_tool = "nuXmv" if task_needs_smt else "NuSMV/nuXmv"
    auth_zh, auth_en = _authoring_labels(authored_variants, req_engine)

    primary_variants = [v for v in ("reference", "complete") if v in variant_details]
    has_mutant = "mutant" in variant_details
    any_failed = any(
        (v_info["effective_status"] in {"TOOL_ERROR", "TIMEOUT"})
        or (v_info["effective_status"] in {"MODEL_PROPERTIES_TRUE", "COUNTEREXAMPLE"} and not v_info["expected_pass"])
        for v_info in variant_details.values()
    )
    any_unverified_missing = any(v_info["effective_status"] == "CHECKER_MISSING" for v_info in variant_details.values())
    any_unverified = any(v_info["effective_status"] == "UNVERIFIED" for v_info in variant_details.values())
    primaries_ok = bool(primary_variants) and all(variant_details[v]["expected_pass"] for v in primary_variants)
    mutant_ok = has_mutant and variant_details["mutant"]["expected_pass"]

    if any_failed:
        v_status = "FAILED"
        badge_tone = "red"
        badge_zh = "SMV 验证异常"
        badge_en = "Verification failed"
    elif any_stale:
        v_status = "STALE"
        badge_tone = "amber"
        badge_zh = f"模型已修改待重验（缺 {req_tool}）" if any_missing else "模型已修改 · 需重验"
        badge_en = f"Stale (missing {req_tool})" if any_missing else "Model changed · Re-verify"
    elif any_unverified_missing:
        v_status = "CHECKER_MISSING"
        badge_tone = "amber"
        badge_zh = f"缺失 {req_tool}（未实时验证）"
        badge_en = f"Missing {req_tool}"
    elif primaries_ok and mutant_ok:
        v_status = "VERIFIED_BOTH"
        if any_missing:
            badge_tone = "cyan"
            badge_zh = f"参考+变异已持久验证 · 缺{req_tool}重跑"
            badge_en = f"Persisted Ref+Mutant OK · No {req_tool}"
        else:
            badge_tone = "green"
            badge_zh = f"已双验（参考+变异 · {req_tool}）"
            badge_en = f"Verified Ref+Mutant ({req_tool})"
    elif primaries_ok:
        v_status = "VERIFIED_REF_ONLY"
        if any_missing:
            badge_tone = "cyan"
            badge_zh = f"参考已持久验证 · 缺{req_tool}重跑"
            badge_en = f"Persisted Ref OK · No {req_tool}"
        else:
            badge_tone = "cyan"
            badge_zh = f"参考已验（{req_tool}）"
            badge_en = f"Ref verified ({req_tool})"
    elif any_unverified:
        v_status = "UNVERIFIED"
        badge_tone = "amber"
        badge_zh = "已编写 · 待验证"
        badge_en = "Authored · Unverified"
    else:
        v_status = "UNVERIFIED"
        badge_tone = "amber"
        badge_zh = "待验证"
        badge_en = "Unverified"

    return {
        "task_id": task_id,
        "scope": "EXPLICIT_SMV_MODEL_ONLY",
        "candidate_st_verified": False,
        "authored": True,
        "authored_variants": authored_variants,
        "required_engine": req_engine,
        "required_tool": req_tool,
        "checker_available": not any_missing,
        "checker_missing": any_missing,
        "stale": any_stale,
        "verification_status": v_status,
        "persisted_record_present": any(v in persisted_models for v in authored_variants),
        "live_rerunnable": not any_missing,
        "last_checked_utc": latest_checked_utc,
        "last_run_attempt": task_record.get("last_run_attempt"),
        "authoring_text_zh": auth_zh,
        "authoring_text_en": auth_en,
        "badge_text_zh": badge_zh,
        "badge_text_en": badge_en,
        "badge_tone": badge_tone,
        "checker_availability": avail,
        "models": variant_details,
    }


def build_all_smv_statuses(
    task_ids: list[str],
    *,
    status_path: Path | None = None,
    models_dir: Path | None = None,
) -> dict[str, dict[str, Any]]:
    avail = probe_checker_availability()
    store = load_smv_status_store(status_path)
    return {
        tid: build_task_smv_status(
            tid,
            store=store,
            status_path=status_path,
            models_dir=models_dir,
            availability=avail,
        )
        for tid in task_ids
    }


def _summarize_counts(result: dict[str, Any]) -> tuple[int, int]:
    props = result.get("property_results") or []
    passed = sum(1 for item in props if item.get("holds") is True)
    failed = sum(1 for item in props if item.get("holds") is False)
    return passed, failed


def record_smv_result(
    task_id: str,
    variant: str,
    smv_path: Path,
    result: dict[str, Any],
    *,
    status_path: Path | None = None,
) -> dict[str, Any]:
    store = load_smv_status_store(status_path)
    records = store.setdefault("records", {})
    task_rec = records.setdefault(task_id, {"models": {}})
    models_rec = task_rec.setdefault("models", {})

    req_engine, req_tool = _detect_model_requirements(smv_path)
    live_sha = _file_sha256(smv_path)
    passed, failed = _summarize_counts(result)
    checked_utc = result.get("created_utc") or now()
    try:
        rel_path = smv_path.relative_to(ROOT).as_posix()
    except ValueError:
        rel_path = str(smv_path)

    entry = {
        "path": rel_path,
        "model_sha256": result.get("model_sha256") or live_sha,
        "required_engine": req_engine,
        "required_tool": req_tool,
        "status": result.get("status"),
        "expected_properties": result.get("expected_properties"),
        "checked_properties": result.get("checked_properties"),
        "passed_count": passed,
        "failed_count": failed,
        "tool": result.get("tool"),
        "engine": result.get("engine"),
        "tool_exe_sha256": result.get("tool_exe_sha256"),
        "checked_utc": checked_utc,
        "error": result.get("error"),
    }
    models_rec[variant] = entry
    task_rec["last_checked_utc"] = checked_utc
    task_rec["last_run_attempt"] = {
        "variant": variant,
        "status": result.get("status"),
        "checked_utc": checked_utc,
        "tool": result.get("tool"),
        "engine": result.get("engine"),
    }
    save_smv_status_store(store, status_path=status_path)
    return store


def record_checker_missing_attempt(
    task_id: str,
    variant: str,
    smv_path: Path,
    error_message: str,
    *,
    status_path: Path | None = None,
) -> dict[str, Any]:
    store = load_smv_status_store(status_path)
    records = store.setdefault("records", {})
    task_rec = records.setdefault(task_id, {"models": {}})
    models_rec = task_rec.setdefault("models", {})

    req_engine, req_tool = _detect_model_requirements(smv_path)
    live_sha = _file_sha256(smv_path)
    checked_utc = now()
    try:
        rel_path = smv_path.relative_to(ROOT).as_posix()
    except ValueError:
        rel_path = str(smv_path)

    existing = models_rec.get(variant)
    # Preserve valid hash-matched baseline evidence; record CHECKER_MISSING only if absent or stale.
    if (
        not existing
        or existing.get("model_sha256") != live_sha
        or existing.get("status") not in {"MODEL_PROPERTIES_TRUE", "COUNTEREXAMPLE"}
    ):
        models_rec[variant] = {
            "path": rel_path,
            "model_sha256": live_sha,
            "required_engine": req_engine,
            "required_tool": req_tool,
            "status": "CHECKER_MISSING",
            "expected_properties": None,
            "checked_properties": 0,
            "passed_count": 0,
            "failed_count": 0,
            "tool": None,
            "engine": req_engine,
            "tool_exe_sha256": None,
            "checked_utc": checked_utc,
            "error": error_message,
        }

    task_rec["last_run_attempt"] = {
        "variant": variant,
        "status": "CHECKER_MISSING",
        "checked_utc": checked_utc,
        "required_engine": req_engine,
        "required_tool": req_tool,
        "error": error_message,
    }
    save_smv_status_store(store, status_path=status_path)
    return store


def run_and_persist_smv_check(
    task_id: str,
    variant: str | None = None,
    *,
    status_path: Path | None = None,
    models_dir: Path | None = None,
    out_root: Path | None = None,
    timeout: int = 60,
) -> tuple[int, dict[str, Any]]:
    """Run local NuSMV/nuXmv on a task's SMV variant and persist the verification record."""
    if variant is not None and variant not in SMV_VARIANTS:
        return 400, {"error": f"Unsupported SMV variant: {variant}"}

    files = discover_task_smv_files(task_id, models_dir=models_dir)
    if variant is not None:
        resolved_variant = variant
    elif "reference" in files:
        resolved_variant = "reference"
    elif "complete" in files:
        resolved_variant = "complete"
    elif "mutant" in files:
        resolved_variant = "mutant"
    else:
        return 404, {"error": f"No SMV model available for task '{task_id}'"}

    smv_path = files.get(resolved_variant)
    if smv_path is None or not smv_path.is_file():
        return 404, {"error": f"SMV variant '{resolved_variant}' not found for task '{task_id}'"}

    avail = probe_checker_availability()
    req_engine, req_tool = _detect_model_requirements(smv_path)
    output = (
        out_root or (ROOT / ".local/model_checker_evidence")
    ) / f"{task_id}_{resolved_variant}_{uuid.uuid4().hex[:8]}"

    try:
        result = model_checker.check_model(smv_path, output, timeout=timeout)
    except (ValueError, OSError) as exc:
        err_msg = str(exc)
        is_missing = (not _is_checker_available_for(req_engine, avail)) or any(
            kw in err_msg.lower() for kw in ("install", "not installed", "does not exist", "nuxmv", "nusmv", "missing")
        )
        if is_missing:
            store = record_checker_missing_attempt(
                task_id, resolved_variant, smv_path, err_msg, status_path=status_path
            )
            smv_status = build_task_smv_status(
                task_id, store=store, status_path=status_path, models_dir=models_dir, availability=avail
            )
            return 503, {
                "status": "TOOL_ERROR",
                "verification_status": "CHECKER_MISSING",
                "checker_missing": True,
                "required_tool": req_tool,
                "required_engine": req_engine,
                "variant": resolved_variant,
                "error": err_msg,
                "smv_status": smv_status,
            }
        return 503, {
            "status": "TOOL_ERROR",
            "verification_status": "TOOL_ERROR",
            "checker_missing": False,
            "variant": resolved_variant,
            "error": err_msg,
        }

    store = record_smv_result(task_id, resolved_variant, smv_path, result, status_path=status_path)
    smv_status = build_task_smv_status(
        task_id, store=store, status_path=status_path, models_dir=models_dir, availability=avail
    )
    payload = dict(result)
    stdout_path = output / "stdout.txt"
    stderr_path = output / "stderr.txt"
    payload["stdout"] = stdout_path.read_text(encoding="utf-8") if stdout_path.is_file() else ""
    payload["stderr"] = stderr_path.read_text(encoding="utf-8") if stderr_path.is_file() else ""
    payload["evidence_dir"] = str(output)
    payload["variant"] = resolved_variant
    payload["verification_status"] = smv_status["verification_status"]
    payload["smv_status"] = smv_status
    return 200, payload


def verify_all_smv_models(
    task_ids: list[str],
    *,
    status_path: Path | None = None,
    models_dir: Path | None = None,
    timeout: int = 60,
) -> dict[str, dict[str, Any]]:
    """Verify every existing SMV variant across all given tasks and persist results."""
    for task_id in task_ids:
        files = discover_task_smv_files(task_id, models_dir=models_dir)
        for variant in SMV_VARIANTS:
            if variant in files:
                run_and_persist_smv_check(
                    task_id,
                    variant,
                    status_path=status_path,
                    models_dir=models_dir,
                    timeout=timeout,
                )
    return build_all_smv_statuses(task_ids, status_path=status_path, models_dir=models_dir)
