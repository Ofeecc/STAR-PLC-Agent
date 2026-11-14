"""Build an audited ZIP snapshot. Incomplete evidence remains explicitly PARTIAL.

No source files are deleted or moved. Staging snapshots stay under .local and
are excluded from the archive; credentials, environments and caches are omitted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import uuid
import zipfile
from pathlib import Path

from audit_submission import (
    ROOT,
    audit,
    exclusion_reason,
    known_secrets,
    scan_file,
    sha256_file,
    submission_inventory,
)
from plc_agent.common import now, write_json


def verify_zip(
    path: Path, expected: dict[str, dict], archive_root: str, secrets: list[bytes], root: Path = ROOT
) -> dict:
    """Reopen every member and compare its bytes, name and secret scan to staging."""
    with zipfile.ZipFile(path) as archive:
        corrupt = archive.testzip()
        if corrupt:
            raise ValueError("Corrupt ZIP member: " + corrupt)
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("ZIP contains duplicate paths")
        expected_names = {archive_root + "/" + name for name in expected}
        if set(names) != expected_names:
            raise ValueError("ZIP inventory differs from the staged manifest")
        for member in archive.infolist():
            prefix, name = member.filename.split("/", 1)
            if prefix != archive_root or ".." in Path(name).parts or name.startswith("/"):
                raise ValueError("Unsafe ZIP path")
            payload = archive.read(member)
            entry = expected[name]
            if len(payload) != entry["bytes"] or hashlib.sha256(payload).hexdigest() != entry["sha256"]:
                raise ValueError("ZIP payload differs from manifest: " + name)
            # Names are checked again independently of the earlier source walk.
            if name not in {"submission/status.json", "submission/MANIFEST.json", "submission/MANIFEST.sha256"}:
                reason = exclusion_reason(root / name, root)
                if reason:
                    raise ValueError("Forbidden file included in ZIP: " + name)
            for secret in secrets:
                if secret and secret in payload:
                    raise ValueError("Configured secret found in ZIP member: " + name)
    return {"verified": True, "members": len(expected), "bytes": path.stat().st_size, "sha256": sha256_file(path)}


def build_package(root: Path = ROOT, *, output: Path | None = None, require_complete: bool = False) -> dict:
    root = root.resolve()
    report = audit(root)
    write_json(root / "results/summary/submission_audit.json", report)
    if report["status"] == "FAIL":
        raise ValueError("Submission audit failed; inspect results/summary/submission_audit.json")
    if require_complete and report["status"] != "PASS":
        raise ValueError("Submission is PARTIAL; required evidence or deliverables remain pending")
    package_id = now().replace(":", "").replace(".", "") + "_" + uuid.uuid4().hex[:8]
    stage = (root / ".local/package_staging" / package_id).resolve()
    if not stage.is_relative_to(root) or stage == root:
        raise ValueError("Invalid staging target")
    stage.mkdir(parents=True, exist_ok=False)
    selected, omitted = submission_inventory(root)
    for source in selected:
        rel = source.relative_to(root)
        target = (stage / rel).resolve()
        if not target.is_relative_to(stage):
            raise ValueError("Staged path escapes snapshot")
        target.parent.mkdir(parents=True, exist_ok=True)
        # CopyFile2 (used by Python 3.12 on Windows) can reject an otherwise
        # valid deeply nested experiment path. Use explicit extended paths;
        # target containment was checked above, and no OS setting is changed.
        source_copy = "\\\\?\\" + str(source.resolve()) if os.name == "nt" else source
        target_copy = "\\\\?\\" + str(target.resolve()) if os.name == "nt" else target
        shutil.copy2(source_copy, target_copy)
    # A live campaign may complete a run during copying. Do not label a mixed
    # snapshot with the audit of another manifest; retry after the work finishes.
    staged_campaign = stage / "results/summary/campaign.json"
    if staged_campaign.is_file() and report.get("campaign_snapshot_sha256") != sha256_file(staged_campaign):
        raise ValueError("Campaign changed while staging; rerun packaging after execution finishes")
    status = {
        "schema_version": 1,
        "package_id": package_id,
        "created_utc": now(),
        "status": report["status"],
        "complete_submission_claim": report["status"] == "PASS",
        "checks": report["checks"],
        "pending": report["pending_mandatory_or_delivery_checks"],
        "warnings": report["warnings"],
        "source_audit": "results/summary/submission_audit.json",
        "scope": "Source, frozen data, actual compiler/experiment logs and available artifacts; no fabricated results",
        "not_included": [
            "API credentials",
            "Conda environment",
            "model weights",
            "installers",
            "build/runtime caches",
            "temporary staging",
        ],
    }
    write_json(stage / "submission/status.json", status)
    secrets = known_secrets(root)
    for path in sorted(stage.rglob("*")):
        if path.is_file() and scan_file(path, path.relative_to(stage).as_posix(), secrets):
            raise ValueError(
                "Secret or unscanned archive finding in staged file: " + path.relative_to(stage).as_posix()
            )
    # The manifest describes every payload file except itself and its text view;
    # a file cannot contain its own final hash without a circular definition.
    payload = {}
    for path in sorted(stage.rglob("*"), key=lambda p: p.relative_to(stage).as_posix()):
        if path.is_file():
            payload[path.relative_to(stage).as_posix()] = {"sha256": sha256_file(path), "bytes": path.stat().st_size}
    manifest = {
        "schema_version": 1,
        "package_id": package_id,
        "created_utc": status["created_utc"],
        "hash_algorithm": "SHA-256",
        "paths_are_relative_to": root.name,
        "self_exclusion": ["submission/MANIFEST.json", "submission/MANIFEST.sha256"],
        "files": payload,
    }
    write_json(stage / "submission/MANIFEST.json", manifest)
    (stage / "submission/MANIFEST.sha256").write_text(
        "".join(entry["sha256"] + "  " + name + "\n" for name, entry in payload.items()), encoding="utf-8"
    )
    all_files = {**payload}
    for name in ("submission/MANIFEST.json", "submission/MANIFEST.sha256"):
        path = stage / name
        all_files[name] = {"sha256": sha256_file(path), "bytes": path.stat().st_size}
    day = status["created_utc"][:10].replace("-", "")
    destination = output or root / "submission" / f"PLC_Agent_Final_submission_{report['status']}_{day}.zip"
    destination = destination.resolve()
    if not destination.is_relative_to(root / "submission"):
        raise ValueError("Package output must remain inside the project submission directory")
    destination.parent.mkdir(exist_ok=True)
    temporary = destination.with_name(destination.name + ".tmp")
    with zipfile.ZipFile(
        temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6, strict_timestamps=False
    ) as archive:
        for name in sorted(all_files):
            archive.write(stage / name, root.name + "/" + name)
    verification = verify_zip(temporary, all_files, root.name, secrets, root)
    temporary.replace(destination)
    result = {
        "status": report["status"],
        "path": str(destination),
        "package_id": package_id,
        "created_utc": status["created_utc"],
        "payload_file_count": len(payload),
        "zip_verification": verification,
        "pending": status["pending"],
        "warnings": status["warnings"],
        "manifest": "submission/MANIFEST.json inside ZIP",
        "stage": str(stage),
        "excluded_count": len(omitted),
    }
    write_json(root / "submission/package_receipt.json", result)
    write_json(root / "submission/status.json", status)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    try:
        result = build_package(args.root, output=args.output, require_complete=args.require_complete)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
