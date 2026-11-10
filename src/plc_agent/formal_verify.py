from __future__ import annotations
import json
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
    for prop in ltl_items:
        pid = prop.get("id", "PROP")
        formula = prop.get("formula", "TRUE")
        desc = prop.get("explanation") or prop.get("description") or prop.get("name") or ""
        ltl_lines.append(f"-- Property: {pid}")
        if desc:
            ltl_lines.append(f"-- Description: {desc}")
        ltl_lines.append(f"LTLSPEC NAME {pid} := {formula};")
        ltl_lines.append("")
        formatted_props.append({
            "id": pid,
            "formula": formula,
            "description": desc,
        })

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
        "tools_supported": ["nuXmv", "UPPAAL", "CBMC"],
        "created_utc": now(),
    }
    write_json(out_dir / "verification_manifest.json", manifest)
    return manifest


def import_verification_evidence(bundle_dir: Path | str, evidence_file: Path | str) -> dict[str, Any]:
    """Parse verification results (SAT / UNSAT / Counterexample) and write verification_result.json."""
    bundle_dir = Path(bundle_dir).resolve()
    evidence_file = Path(evidence_file).resolve()

    manifest_path = bundle_dir / "verification_manifest.json"
    manifest = read_json(manifest_path) if manifest_path.is_file() else {}
    task_id = manifest.get("task_id")

    raw_text = evidence_file.read_text(encoding="utf-8", errors="replace")
    status = "UNKNOWN"
    details: dict[str, Any] = {}

    try:
        data = json.loads(raw_text)
        if isinstance(data, dict):
            status = data.get("status") or data.get("result") or "UNKNOWN"
            details = data.get("details", data)
    except json.JSONDecodeError:
        pass

    if status == "UNKNOWN":
        upper = raw_text.upper()
        if (
            "COUNTEREXAMPLE" in upper
            or "TRACE TYPE: COUNTEREXAMPLE" in upper
            or "IS FALSE" in raw_text.lower()
            or "VIOLATION" in upper
            or "VERIFICATION FAILED" in upper
        ):
            status = "COUNTEREXAMPLE"
        elif "UNSAT" in upper:
            status = "UNSAT"
        elif (
            "SAT" in upper
            or "VERIFIED" in upper
            or ("IS TRUE" in raw_text.lower() and "IS FALSE" not in raw_text.lower())
        ):
            status = "SAT"
        else:
            status = "UNKNOWN"

    verified = status in ("SAT", "UNSAT")
    result: dict[str, Any] = {
        "task_id": task_id,
        "source_sha256": manifest.get("source_sha256"),
        "evidence_file": evidence_file.name,
        "status": status,
        "verified": verified,
        "details": details or {"raw_evidence_snippet": raw_text[:500]},
        "imported_utc": now(),
    }
    write_json(bundle_dir / "verification_result.json", result)
    return result
