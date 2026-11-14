from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .common import digest, now, read_json, write_json
from .compiler import normalize_candidate


def export_verification_bundle(task: dict, candidate: dict | str, out_dir: Path | str) -> dict[str, Any]:
    """Export formal verification bundle (ST source, LTL spec, manifest) for model checkers."""
    out_dir = Path(out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    candidate_norm = normalize_candidate(candidate)
    source_hash = digest(candidate_norm)

    # 1. candidate.st: assemble helper DUTs, supporting objects, and FB_Task
    st_parts = []
    for obj in candidate_norm.get("supporting_objects", []):
        decl = obj.get("declaration", "").strip()
        impl = obj.get("implementation", "").strip()
        kind = obj.get("kind", "").upper()
        part = decl
        if impl:
            part += "\n\n" + impl
        if kind == "FUNCTION" and not part.rstrip().endswith("END_FUNCTION"):
            part += "\nEND_FUNCTION"
        elif kind == "FUNCTION_BLOCK" and not part.rstrip().endswith("END_FUNCTION_BLOCK"):
            part += "\nEND_FUNCTION_BLOCK"
        st_parts.append(part)

    fb_decl = candidate_norm["declaration"].strip()
    fb_impl = candidate_norm["implementation"].strip()
    fb_text = fb_decl + "\n\n" + fb_impl
    if not fb_text.rstrip().endswith("END_FUNCTION_BLOCK"):
        fb_text += "\nEND_FUNCTION_BLOCK\n"
    else:
        fb_text += "\n"
    st_parts.append(fb_text)

    full_st = "\n\n".join(st_parts)
    st_file = out_dir / "candidate.st"
    st_file.write_text(full_st, encoding="utf-8")

    # 2. spec.ltl: format each property ID, description, and formula
    ltl_items = task.get("ltl", [])
    ltl_lines = [
        f"-- Formal verification specification for Task {task.get('id', 'UNKNOWN')}",
        f"-- Generated: {now()}",
        "",
    ]
    formatted_props = []
    for idx, prop in enumerate(ltl_items, start=1):
        if isinstance(prop, dict):
            pid = prop.get("id", f"PROP_{idx}")
            formula = prop.get("formula", "TRUE")
            desc = prop.get("explanation") or prop.get("description") or prop.get("name") or ""
        else:
            pid = f"PROP_{idx}"
            formula = str(prop)
            desc = ""
        ltl_lines.append(f"-- Property: {pid}")
        if desc:
            ltl_lines.append(f"-- Description: {desc}")
        ltl_lines.append(f"LTLSPEC NAME {pid} := {formula};")
        ltl_lines.append("")
        formatted_props.append(
            {
                "id": pid,
                "formula": formula,
                "description": desc,
            }
        )

    ltl_file = out_dir / "spec.ltl"
    ltl_file.write_text("\n".join(ltl_lines), encoding="utf-8")

    # 3. verification_manifest.json
    manifest: dict[str, Any] = {
        "task_id": task.get("id"),
        "source_sha256": source_hash,
        "st_path": "candidate.st",
        "ltl_path": "spec.ltl",
        "properties": formatted_props,
        "atomic_propositions": task.get("atomic_propositions", {}),
        "tools_supported": [],
        "encoding_complete": False,
        "task_sha256": digest(task),
        "bundle_status": "REQUIRES_PROPERTY_AND_MODEL_ENCODING",
        "created_utc": now(),
    }
    write_json(out_dir / "verification_manifest.json", manifest)
    return manifest


def verify_candidate(
    task: dict[str, Any],
    candidate: dict[str, Any] | str,
    out_dir: Path | str,
    timeout: int = 60,
    executable: str | None = None,
    tool: str = "auto",
    engine: str = "auto",
    bmc_bound: int = 25,
    include_expected_observer: bool = True,
    use_observer_smv: bool = True,
    extra_assertions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Export verification bundle, compile ST->SMV, and run NuSMV/nuXmv on candidate ST."""
    from .st_verifier import verify_candidate_st

    out = Path(out_dir).resolve()
    manifest = export_verification_bundle(task=task, candidate=candidate, out_dir=out)
    try:
        result = verify_candidate_st(
            task=task,
            candidate=candidate,
            out_dir=out,
            timeout=timeout,
            executable=executable,
            tool=tool,
            engine=engine,
            bmc_bound=bmc_bound,
            include_expected_observer=include_expected_observer,
            use_observer_smv=use_observer_smv,
            extra_assertions=extra_assertions,
        )
    except (OSError, ValueError) as exc:
        # Missing executables/configuration must not abort functional testing
        # or be attributed to invalid model output by the caller.
        result = {
            "task_id": task.get("id"), "status": "TOOL_ERROR", "verified": False,
            "candidate_st_verified": False, "reason": f"Verification infrastructure: {exc}",
            "total_properties": len(task.get("ltl", [])), "passed_properties": 0,
            "failed_properties": 0, "unknown_properties": len(task.get("ltl", [])),
            "property_pass_ratio": None, "property_results": [],
        }
        write_json(out / "verification_result.json", result)

    if result.get("smv_path"):
        manifest["smv_path"] = result["smv_path"]
        manifest["observer_smv"] = result.get("observer_smv")
        manifest["tools_supported"] = [result.get("tool")] if result.get("tool") else ["NuSMV", "nuXmv"]
        manifest["encoding_complete"] = True
        manifest["bundle_status"] = result.get("status", "UNKNOWN")
        manifest["verification_status"] = result.get("status")
        manifest["candidate_st_verified"] = result.get("verified", False)
        manifest["property_pass_ratio"] = result.get("property_pass_ratio")
    else:
        manifest["bundle_status"] = result.get("status", "UNSUPPORTED_ST")
        manifest["verification_status"] = result.get("status")
        manifest["reason"] = result.get("reason")
    write_json(out / "verification_manifest.json", manifest)
    return result


def import_verification_evidence(bundle_dir: Path | str, evidence_file: Path | str) -> dict[str, Any]:
    """Parse verification results (SAT / UNSAT / Counterexample) and write verification_result.json."""
    bundle_dir = Path(bundle_dir).resolve()
    evidence_file = Path(evidence_file).resolve()

    manifest_path = bundle_dir / "verification_manifest.json"
    manifest = read_json(manifest_path) if manifest_path.is_file() else {}
    task_id = manifest.get("task_id")

    raw_text = evidence_file.read_text(encoding="utf-8", errors="replace")
    status = "UNKNOWN"
    data = {}
    try:
        parsed = json.loads(raw_text)
        if isinstance(parsed, dict):
            data = parsed
    except json.JSONDecodeError:
        pass
    # Solver SAT/UNSAT has no universal property-validity meaning.
    reported = str(data.get("status", data.get("result", ""))).upper()
    truths = re.findall(r"^--\s*specification\s+(?:.+?\s+)?is\s+(true|false)\s*$", raw_text, re.I | re.M)
    if (
        reported in {"COUNTEREXAMPLE", "FAIL"}
        or "false" in [v.lower() for v in truths]
        or re.search(r"trace type:\s*counterexample", raw_text, re.I)
    ):
        status = "COUNTEREXAMPLE"
    elif reported in {"SAT", "UNSAT"}:
        status = reported
    elif truths and all(v.lower() == "true" for v in truths):
        status = "PROPERTIES_TRUE"
    elif reported in {"PASS", "VERIFIED"}:
        status = "REPORTED_PASS"
    expected_ids = {p["id"] for p in manifest.get("properties", [])}
    checks = data.get("property_results", {})
    bound = bool(
        manifest.get("encoding_complete") is True
        and expected_ids
        and data.get("source_sha256") == manifest.get("source_sha256")
        and data.get("task_sha256") == manifest.get("task_sha256")
        and data.get("tool") in manifest.get("tools_supported", [])
        and isinstance(checks, dict)
        and set(checks) == expected_ids
    )
    verified = bool(
        bound and reported == "PASS" and status != "COUNTEREXAMPLE" and all(v is True for v in checks.values())
    )
    result = {
        "task_id": task_id,
        "source_sha256": manifest.get("source_sha256"),
        "evidence_file": evidence_file.name,
        "status": "PASS" if verified else status,
        "verified": verified,
        "evidence_bound": bound,
        "reason": None if verified else "No complete, encoded and hash-bound property proof",
        "details": data or {"raw_evidence_snippet": raw_text[:500]},
        "imported_utc": now(),
    }
    write_json(bundle_dir / "verification_result.json", result)
    return result
