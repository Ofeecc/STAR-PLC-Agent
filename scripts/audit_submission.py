"""Offline audit of the submission snapshot; never calls an LLM or PLC.

This checks reproducibility and consistency of saved evidence. It does not
authenticate a remote model or prove that a human-entered runtime trace is true.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from plc_agent.common import digest, now, read_json, write_json
from plc_agent.compiler import normalize_candidate, verify_evidence
from plc_agent.dataset import load_tasks, public_coverage, validate
from plc_agent.functional import evaluate_trace
from plc_agent.metrics import aggregate, audit_records

INCLUDED_DIRECTORIES = {
    "src", "tests", "scripts", "codesys", "configs", "dataset", "requirements",
    "experiments", "results", "docs", "report", "presentation", "video",
}
INCLUDED_ROOT_FILES = {"README.md", "pyproject.toml", ".gitignore", ".env.example", "LICENSE"}
EXCLUDED_PARTS = {
    ".git", ".local", ".venv", "venv", "env", "envs", "node_modules",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "installers",
    "weights", "checkpoints", ".cache", "cache", "caches", "build", "tmp", "temp",
}
EXCLUDED_SUFFIXES = {
    ".pyc", ".pyo", ".pdb", ".bak", ".tmp", ".cache", ".precompilecache",
    ".opt", ".compileinfo", ".bootinfo", ".exe", ".msi", ".msix", ".dll",
    ".safetensors", ".ckpt", ".pt", ".pth", ".onnx", ".gguf",
}
SECRET_PATTERNS = (
    ("api_token", re.compile(rb"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}")),
    ("bearer_token", re.compile(rb"(?i)\bbearer[ \t]+[A-Za-z0-9_.-]{24,}")),
    ("assigned_api_key", re.compile(rb'''(?i)["']?(?:api[_-]?key|access[_-]?token|client[_-]?secret)["']?[ \t]*[:=][ \t]*["']([A-Za-z0-9_.-]{24,})["']''')),
)


def sha256_file(path: Path) -> str:
    checksum = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(chunk)
    return checksum.hexdigest()


def relative(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def artifact_path(value: str | Path, root: Path = ROOT) -> Path:
    """Resolve historical absolute evidence paths after moving the whole project.

    Never follow an unrelated absolute path or permit '..' to leave the project.
    Original path strings remain unchanged in raw records.
    """
    root = root.resolve()
    raw = str(value).replace("\\", "/")
    candidate = Path(value)
    if not candidate.is_absolute() and not re.match(r"^[A-Za-z]:/", raw):
        resolved = (root / raw).resolve()
        if not resolved.is_relative_to(root):
            raise ValueError("Evidence path escapes project")
        return resolved
    try:
        resolved = candidate.resolve()
        if resolved.is_relative_to(root):
            return resolved
    except (OSError, ValueError):
        pass
    marker = "/" + root.name + "/"
    position = raw.casefold().rfind(marker.casefold())
    if position < 0:
        raise ValueError("Historical evidence path has no project-root suffix")
    suffix = raw[position + len(marker):]
    resolved = (root / suffix).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError("Relocated evidence path escapes project")
    return resolved


def exclusion_reason(path: Path, root: Path = ROOT) -> str | None:
    rel = path.relative_to(root)
    lowered = [part.casefold() for part in rel.parts]
    name = path.name.casefold()
    if any(part in EXCLUDED_PARTS or part.endswith(".egg-info") for part in lowered):
        return "cache, local state, environment, installer, or build output"
    if name != ".env.example" and (name == ".env" or name.startswith(".env.") or "apikey" in name or "api_key" in name):
        return "private API configuration"
    if name.endswith(".key") or name.startswith("auth.") or name in {"credentials", "credentials.json", "token.json", "secrets.json"}:
        return "credential material"
    if path.suffix.casefold() in EXCLUDED_SUFFIXES or name.endswith("~") or "simulation.bootinfo" in name:
        return "rebuildable cache, executable, installer, model weight, or temporary file"
    if name == "codesys_login.png":
        return "irrelevant account-login screenshot"
    if lowered[0] == "presentation" and any(part in {"backup", "exports", "live_preview"} for part in lowered[1:]):
        return "intermediate slide exports, automatic backups, or live preview state; final deck and editable SVG sources are retained"
    if path.is_symlink():
        return "symbolic link is not followed into a submission"
    if rel.parts[0] == "report" and name == "methods.md" and not list((root / "report").rglob("*.pdf")):
        return "unfinished report draft; final PDF is absent"
    if len(rel.parts) == 1:
        return None if path.name in INCLUDED_ROOT_FILES else "unlisted root file"
    return None if rel.parts[0] in INCLUDED_DIRECTORIES else "not a deliverable directory"


def submission_inventory(root: Path = ROOT) -> tuple[list[Path], list[dict[str, str]]]:
    root = root.resolve()
    selected, omitted = [], []
    for path in sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix().casefold()):
        if not path.is_file():
            continue
        reason = exclusion_reason(path, root)
        if reason:
            # Submission staging and local state are intentionally not itemized.
            if path.relative_to(root).parts[0] not in {"submission", ".local", ".git"}:
                omitted.append({"path": path.relative_to(root).as_posix(), "reason": reason})
            continue
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            omitted.append({"path": path.relative_to(root).as_posix(), "reason": "resolved path leaves project"})
            continue
        selected.append(path)
    return selected, omitted


def known_secrets(root: Path = ROOT) -> list[bytes]:
    """Read only into memory. The returned values must never enter a report."""
    candidates = [os.environ.get(name, "") for name in ("PLC_LLM_API_KEY", "OPENAI_API_KEY")]
    private_path = os.environ.get("PLC_API_CONFIG")
    path = Path(private_path) if private_path else root.parent / "APIKEY相关.txt"
    if path.is_file():
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        first = lines[0].strip() if lines else ""
        match = re.search(r"sk-[A-Za-z0-9_.-]+", first)
        if match:
            candidates.append(match.group())
        elif first and "=" not in first and " " not in first:
            candidates.append(first)
    return list({value.encode("utf-8") for value in candidates if len(value) >= 12})


def _scan_bytes(data: bytes, location: str, secrets: list[bytes]) -> list[dict[str, Any]]:
    findings = []
    exact_count = sum(data.count(secret) for secret in secrets)
    if exact_count:
        findings.append({"path": location, "kind": "configured_secret", "count": exact_count})
    for label, pattern in SECRET_PATTERNS:
        count = len(pattern.findall(data))
        if count:
            findings.append({"path": location, "kind": label, "count": count})
    return findings


def scan_file(path: Path, label: str, secrets: list[bytes]) -> list[dict[str, Any]]:
    data = path.read_bytes()
    findings = _scan_bytes(data, label, secrets)
    # Office containers can hide a secret in compressed XML or speaker notes.
    if path.suffix.casefold() in {".docx", ".pptx", ".xlsx", ".zip"} and zipfile.is_zipfile(io.BytesIO(data)):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                if member.file_size > 64 * 1024 * 1024:
                    findings.append({"path": label + "!" + member.filename, "kind": "oversized_unscanned_member", "count": 1})
                    continue
                findings.extend(_scan_bytes(archive.read(member), label + "!" + member.filename, secrets))
    return findings


def check_compile_attempt(attempt: dict[str, Any], root: Path = ROOT) -> dict[str, Any]:
    status = attempt.get("status")
    if status not in {"PASS", "COMPILE_FAIL"}:
        return {"eligible": False, "status": status, "infrastructure_error_retained": bool(attempt.get("infrastructure_error"))}
    evidence_path = artifact_path(attempt["evidence"], root)
    evidence = read_json(evidence_path)
    folder = evidence_path.parent
    request = read_json(folder / "request.json")
    candidate = normalize_candidate(read_json(folder / "candidate.json"))
    if digest(candidate) != request["source_sha256"] or digest(candidate) != attempt["source_sha256"]:
        raise ValueError("Saved candidate/source hash mismatch")
    if request.get("candidate") != candidate:
        raise ValueError("Saved request candidate differs from saved candidate")
    checked_status, success = verify_evidence(evidence, request)
    if status != checked_status or bool(attempt.get("success")) != success:
        raise ValueError("Stored compilation outcome differs from actual diagnostics")
    if attempt.get("process_exit_code") != 0:
        raise ValueError("Eligible compilation process did not exit normally")
    if type(evidence.get("error_count")) is not int or evidence["error_count"] < 0:
        raise ValueError("Invalid compiler error count")
    errors = [d for d in evidence.get("diagnostics", []) if "error" in str(d.get("severity", "")).casefold()]
    if len(errors) != evidence["error_count"]:
        raise ValueError("Compiler diagnostic severities do not match error_count")
    for filename in ("FB_Task.st", "stdout.log", "stderr.log", "invocation.json"):
        if not (folder / filename).is_file():
            raise ValueError("Missing compiler artifact: " + filename)
    project = artifact_path(attempt["project"], root)
    if not project.is_file() or project.stat().st_size == 0:
        raise ValueError("Compiled project is absent or empty")
    return {"eligible": True, "status": status, "error_count": evidence["error_count"],
            "source_sha256": attempt["source_sha256"], "request_id": request["request_id"],
            "evidence": relative(evidence_path, root)}


def _check_item(identifier: str, state: str, detail: str, paths: list[str] | None = None) -> dict[str, Any]:
    return {"id": identifier, "status": state, "detail": detail, "evidence": paths or []}


def framework_identity(value: Any) -> str:
    """Accept a version-qualified record while preserving the raw record string."""
    value = str(value or "")
    return "smolagents" if re.fullmatch(r"smolagents(?:_\d+(?:\.\d+)*(?:[A-Za-z0-9.-]*)?)?", value) else value


def _media_duration(path: Path) -> float | None:
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        try:
            result = subprocess.run([ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
                                    capture_output=True, text=True, check=True, timeout=20)
            return float(json.loads(result.stdout)["format"]["duration"])
        except (OSError, ValueError, KeyError, subprocess.SubprocessError):
            pass
    # The imageio-ffmpeg wheel supplies FFmpeg, without ffprobe. Read the
    # completed MP4's own movie header, never an unverified sidecar assertion.
    if path.suffix.casefold() != ".mp4":
        return None
    try:
        data = path.read_bytes()

        def boxes(start, end):
            position = start
            while position + 8 <= end:
                size, kind = struct.unpack_from(">I4s", data, position)
                header = 8
                if size == 1:
                    if position + 16 > end:
                        raise ValueError("Truncated MP4 box")
                    size = struct.unpack_from(">Q", data, position + 8)[0]
                    header = 16
                elif size == 0:
                    size = end - position
                if size < header or position + size > end:
                    raise ValueError("Invalid MP4 box size")
                yield kind, position + header, position + size
                position += size

        for kind, start, end in boxes(0, len(data)):
            if kind != b"moov":
                continue
            for child, payload, bound in boxes(start, end):
                if child != b"mvhd":
                    continue
                version = data[payload]
                if version == 0 and payload + 20 <= bound:
                    scale, duration = struct.unpack_from(">II", data, payload + 12)
                elif version == 1 and payload + 32 <= bound:
                    scale, duration = struct.unpack_from(">IQ", data, payload + 20)
                else:
                    raise ValueError("Unsupported MP4 movie header")
                return duration / scale if scale > 0 else None
    except (OSError, ValueError, struct.error, IndexError):
        return None
    return None


def _pdf_page_count(path: Path) -> int | None:
    command = shutil.which("pdfinfo")
    if not command:
        return None
    try:
        result = subprocess.run([command, str(path)], capture_output=True, text=True, errors="replace", check=True, timeout=20)
        match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", result.stdout)
        return int(match.group(1)) if match else None
    except (OSError, ValueError, subprocess.SubprocessError):
        return None


def audit(root: Path = ROOT, *, scan_secrets: bool = True) -> dict[str, Any]:
    root = root.resolve()
    checks, errors, warnings = [], [], []
    tasks = load_tasks(root)
    validation = validate(tasks)
    source = root / "requirements/source/public_bank_original.json"
    coverage = public_coverage(tasks, read_json(source)) if source.is_file() else None
    dataset_ok = not validation["errors"] and coverage is not None and coverage["verbatim_all_included"]
    dataset_ok = dataset_ok and validation["by_kind"].get("self_built", 0) >= 10
    checks.append(_check_item("dataset", "PASS" if dataset_ok else "FAIL", f"{validation['task_count']} tasks; {validation['test_cases']} cases; {validation['test_steps']} scan steps; verbatim official coverage checked", ["dataset", "requirements/source/public_bank_original.json"]))
    errors.extend(validation["errors"])
    if not dataset_ok:
        errors.append("Dataset coverage or structural validation failed")
    source_alignment = root / "requirements/source_alignment.json"
    source_ok = False
    if source_alignment.is_file():
        try:
            alignment = read_json(source_alignment)
            source_ok = alignment.get("aligned_under_documented_normalization") is True
            for name, entry in alignment.get("sources", {}).items():
                path = root / "requirements" / (name if name == "public_bank_pdf.txt" else "source/" + name)
                if not path.is_file() or path.stat().st_size != entry["bytes"] or sha256_file(path) != entry["sha256"]:
                    raise ValueError("Source snapshot byte hash/size mismatch: " + name)
            if not source_ok:
                raise ValueError("Source alignment record is not affirmative")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append("Original source integrity: " + str(exc))
    checks.append(_check_item("source_records", "PASS" if source_ok else "PARTIAL", "Original source byte hashes and documented adaptation/alignment records are retained", ["requirements/source", "requirements/source_alignment.json", "dataset/specifications"]))

    preflight_path = root / "results/summary/compiler_preflight.json"
    preflight_checks = []
    try:
        preflight = read_json(preflight_path)
        preflight_checks = [check_compile_attempt(row, root) for row in preflight["runs"]]
        expected = ["PASS", "COMPILE_FAIL", "PASS"]
        if not preflight.get("verified") or [row["status"] for row in preflight_checks] != expected:
            raise ValueError("Expected valid-invalid-repaired statuses were not verified")
        template_path = artifact_path("codesys/templates/benchmark.project", root)
        if sha256_file(template_path) != preflight.get("template_sha256"):
            raise ValueError("Frozen compiler template changed after preflight")
        checks.append(_check_item("codesys_compiler", "PASS", "Real valid-invalid-repaired evidence was rechecked, including the failed build", [relative(preflight_path, root)]))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        checks.append(_check_item("codesys_compiler", "PARTIAL", str(exc), [relative(preflight_path, root)]))
        if preflight_path.is_file():
            errors.append("Compiler preflight consistency: " + str(exc))

    model_path = root / "results/summary/model_capabilities.json"
    model_ids, compatible = [], set()
    if model_path.is_file():
        model_data = read_json(model_path)
        model_ids = model_data.get("selected", [])
        compatible = {row["model"] for row in model_data.get("model_tests", []) if row.get("tool_roundtrip")}
    checks.append(_check_item("two_models", "PASS" if len(set(model_ids)) >= 2 and set(model_ids).issubset(compatible) else "PARTIAL", "Two relay IDs require actual streaming/tool round trips; upstream identity, context limits and prices remain unverified unless separately evidenced", [relative(model_path, root)]))

    campaign_path = root / "results/summary/campaign.json"
    records, compile_checks, computed_metrics = [], [], []
    manifest_before = campaign_path.read_bytes() if campaign_path.is_file() else b""
    condition_statuses = []
    execution_complete = False
    if manifest_before:
        manifest = json.loads(manifest_before.decode("utf-8-sig"))
        tasks_by_id = {task["id"]: task for task in tasks}
        if manifest.get("dataset_sha256") != digest(tasks):
            errors.append("Campaign dataset hash differs from frozen dataset")
        conditions = manifest.get("conditions", [])
        if {c.get("id") for c in conditions} != {"E1", "E2", "E3", "E4"}:
            errors.append("Campaign does not declare exactly E1-E4")
        actual_keys = set(manifest.get("records", {}))
        expected_keys = {condition + "/" + task_id for condition in ("E1", "E2", "E3", "E4") for task_id in tasks_by_id}
        if actual_keys != expected_keys:
            errors.append("Campaign condition-task coverage differs from the fixed dataset")
        condition_map = {c["id"]: c for c in conditions}
        for key, stored_path in sorted(manifest.get("records", {}).items()):
            try:
                path = artifact_path(stored_path, root)
                row = read_json(path)
                records.append(row)
                if key != row["condition"] + "/" + row["task_id"]:
                    raise ValueError("Manifest record identity mismatch")
                task = tasks_by_id[row["task_id"]]
                condition = condition_map[row["condition"]]
                if row.get("task_sha256") != digest(task):
                    raise ValueError("Task changed after this run")
                if framework_identity(row.get("framework")) != framework_identity(condition.get("framework")) or row.get("model") != condition.get("model"):
                    raise ValueError("Recorded framework/model differs from the campaign condition")
                for attempt in row.get("compilation_attempts", []):
                    compile_checks.append({"record": key, **check_compile_attempt(attempt, root)})
                if row.get("final_compiled"):
                    final = normalize_candidate(read_json(path.parent / "final_candidate.json"))
                    if digest(final) != row["compilation_attempts"][-1]["source_sha256"]:
                        raise ValueError("Final evaluated source differs from the last compilation")
                if row.get("functional", {}).get("evaluated_cases", 0):
                    trace_path = path.parent / "functional_trace.json"
                    if not trace_path.is_file():
                        # Automatic IDE simulation keeps its actual trace in a
                        # timestamped functional workspace. Manual import puts a
                        # portable copy at the run root. Audit the selected real
                        # trace without moving or rewriting either provenance.
                        selected_trace = row.get("functional_execution", {}).get("trace_path")
                        if not selected_trace:
                            raise ValueError("Evaluated functional row has no saved trace path")
                        trace_path = artifact_path(selected_trace, root)
                        if not trace_path.is_relative_to(path.parent.resolve()):
                            raise ValueError("Functional trace escapes its selected run")
                    trace = read_json(trace_path)
                    trace_root = trace_path.parent
                    # Supporting references may be historical absolute paths.
                    for reference in trace.get("evidence_files", []):
                        name = reference.get("path") if isinstance(reference, dict) else reference
                        if name and (Path(name).is_absolute() or re.match(r"^[A-Za-z]:[/\\]", name)):
                            relocated = artifact_path(name, root)
                            replacement = str(relocated.relative_to(trace_root))
                            if isinstance(reference, dict):
                                reference["path"] = replacement
                            else:
                                trace["evidence_files"][trace["evidence_files"].index(reference)] = replacement
                    checked = evaluate_trace(task, row["compilation_attempts"][-1]["source_sha256"], trace, evidence_root=trace_root)
                    for field in ("status", "planned_cases", "evaluated_cases", "passed_cases", "evaluated_steps", "passed_steps"):
                        if checked[field] != row["functional"][field]:
                            raise ValueError("Functional trace recomputation disagrees with " + field)
            except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
                errors.append(key + ": " + str(exc))
        errors.extend(audit_records(records))
        try:
            computed_metrics = aggregate(records, len(tasks))
            for condition in computed_metrics:
                rows = [r for r in records if r["condition"] == condition["condition"]]
                done = len(rows) == len(tasks) and all(r.get("status") != "NOT_RUN" and r.get("finished_utc") for r in rows)
                condition_statuses.append({"condition": condition["condition"], "executed": sum(r.get("status") != "NOT_RUN" for r in rows), "planned": len(tasks), "execution_complete": done,
                                           "status_counts": condition["status_counts"], "compiler_coverage": condition["compiler_coverage"]})
            execution_complete = len(condition_statuses) == 4 and all(c["execution_complete"] for c in condition_statuses)
            metrics_path = root / "results/summary/metrics.json"
            if metrics_path.is_file() and read_json(metrics_path).get("conditions") != computed_metrics:
                warnings.append("Saved metrics differ from the captured campaign; regenerate aggregate before hand-in")
        except (ValueError, KeyError, TypeError) as exc:
            errors.append("Metric recomputation: " + str(exc))
    checks.append(_check_item("four_condition_benchmark", "PASS" if execution_complete else "PARTIAL", f"{sum(c['executed'] for c in condition_statuses)} of {4 * len(tasks)} runs executed; failed runs remain in the denominator and raw logs", ["results/summary/campaign.json", "experiments"]))
    frameworks = {framework_identity(r.get("framework")) for r in records if r.get("status") != "NOT_RUN"}
    pairs = {(r["condition"], r["model"]) for r in records if r.get("status") != "NOT_RUN" and r.get("compilation_attempts")}
    checks.append(_check_item("existing_agent_baseline", "PASS" if execution_complete and len(frameworks) >= 2 and len(pairs) == 4 else "PARTIAL", "The saved record must identify the actual existing framework and show its compiler tool use with both selected models", ["docs/baseline.md", "docs/smolagents_baseline.md", "results/summary/codex_compatibility.json"]))
    compiled_rows = [r for r in records if r.get("final_compiled")]
    tested_rows = [r for r in compiled_rows if r["functional"]["planned_cases"] > 0 and r["functional"]["evaluated_cases"] == r["functional"]["planned_cases"]]
    functional_complete = bool(compiled_rows) and len(tested_rows) == len(compiled_rows)
    checks.append(_check_item("functional_execution", "PASS" if functional_complete else "PARTIAL", f"All fixed cases evaluated for {len(tested_rows)} of {len(compiled_rows)} compiled candidates; Python reference checks are excluded", ["experiments", "docs/functional_testing.md"]))

    screenshot_ok = False
    screenshot_record = root / "results/summary/compiler_screenshot.json"
    if screenshot_record.is_file():
        try:
            shot = read_json(screenshot_record)
            shot_file = artifact_path(shot["path"], root)
            screenshot_ok = (shot_file.resolve().is_relative_to(root.resolve())
                             and shot_file.is_file() and shot_file.stat().st_size > 0
                             and shot.get("sha256") == sha256_file(shot_file)
                             and shot.get("actual_codesys_gui") is True
                             and bool(shot.get("captured_utc")))
        except (OSError, ValueError, KeyError, TypeError):
            screenshot_ok = False
    checks.append(_check_item("compiler_gui_screenshot", "PASS" if screenshot_ok else "PARTIAL",
        "The requested real IDE screenshot needs a hash-bound capture record; diagnostic text is not a GUI screenshot",
        ["docs/compiler_screenshot.md", "results/summary/compiler_screenshot.json"]))

    report_pdfs = [p for p in [root / "report/report.pdf"] if p.is_file()]
    slides = [p for p in [root / "presentation/slides.pptx"] if p.is_file()]
    report_ok = bool(report_pdfs) and any(p.read_bytes().startswith(b"%PDF-") and b"%%EOF" in p.read_bytes()[-2048:] for p in report_pdfs)
    ppt_info = []
    for path in slides:
        try:
            with zipfile.ZipFile(path) as archive:
                count = sum(bool(re.fullmatch(r"ppt/slides/slide\d+\.xml", name)) for name in archive.namelist())
                ppt_info.append({"path": relative(path, root), "slides": count, "editable_ooxml": count > 0})
        except (OSError, zipfile.BadZipFile):
            errors.append("Invalid PPTX container: " + relative(path, root))
    checks.append(_check_item("english_pdf_report", "PASS" if report_ok else "PARTIAL", "A readable compiled PDF is required; visual QA and numerical consistency must also be documented", [relative(p, root) for p in report_pdfs]))
    checks.append(_check_item("editable_presentation", "PASS" if any(p["editable_ooxml"] and 6 <= p["slides"] <= 8 for p in ppt_info) else "PARTIAL", "An editable OOXML deck of 6-8 slides is expected; container inspection is not visual QA", [p["path"] for p in ppt_info]))
    qa_path = root / "results/summary/artifact_qa.json"
    qa_ok = False
    if qa_path.is_file():
        try:
            qa = read_json(qa_path)
            report_qa, slides_qa = qa["report"], qa["presentation"]
            report_file, slides_file = artifact_path(report_qa["path"], root), artifact_path(slides_qa["path"], root)
            page_count = _pdf_page_count(report_file) or report_qa.get("page_count")
            slide_count = next((entry["slides"] for entry in ppt_info if entry["path"] == relative(slides_file, root)), None)
            report_pages = report_qa.get("reviewed_pages", [])
            slide_pages = slides_qa.get("reviewed_slides", [])
            qa_ok = (report_qa.get("compiled") is True and report_qa.get("visual_inspection_passed") is True
                     and isinstance(page_count, int) and page_count > 0 and report_pages == list(range(1, page_count + 1))
                     and report_qa.get("sha256") == sha256_file(report_file)
                     and slides_qa.get("visual_inspection_passed") is True and slides_qa.get("editable_verified") is True
                     and isinstance(slide_count, int) and slide_count > 0 and slide_pages == list(range(1, slide_count + 1))
                     and slides_qa.get("sha256") == sha256_file(slides_file))
            if not qa_ok:
                warnings.append("Artifact QA record is incomplete or its hashes no longer match final files")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            warnings.append("Artifact QA record could not be verified: " + str(exc))
    checks.append(_check_item("artifact_visual_qa", "PASS" if qa_ok else "PARTIAL", "A saved, hash-bound review records actual PDF-page inspection and editable-slide inspection; it is an operator assertion backed by the renderer workflow", ["results/summary/artifact_qa.json"]))
    video_info = []
    for path in sorted((root / "video").glob("*")):
        if path.suffix.casefold() in {".mp4", ".mov", ".mkv", ".webm", ".avi"}:
            video_info.append({"path": relative(path, root), "seconds": _media_duration(path)})
    short_video = any(v["seconds"] is not None and 0 < v["seconds"] < 360 for v in video_info)
    recording_materials = (root / "presentation/speaker_notes.md").is_file() and any(p.is_file() for p in (root / "video/recording_plan.md", root / "video/README.md"))
    checks.append(_check_item("explanation_video", "PASS" if short_video else "PARTIAL", "Verified video must be shorter than 360 seconds; a recording-ready fallback is useful but does not count as a finished teacher-required recording", [v["path"] for v in video_info]))
    checks.append(_check_item("recording_materials", "PASS" if recording_materials else "PARTIAL", "Speaking notes, a practical recording plan and defense questions should match the final results", ["presentation/speaker_notes.md", "presentation/defense_qa.md", "video/recording_plan.md"]))
    unit_log = root / "results/summary/unit_tests.log"
    unit_text = unit_log.read_text(encoding="utf-8-sig", errors="replace") if unit_log.is_file() else ""
    checks.append(_check_item("offline_tests", "PASS" if re.search(r"Ran \d+ tests", unit_text) and re.search(r"\bOK\b", unit_text) else "PARTIAL", "Saved offline unit/regression evidence; synthetic unit fixtures are never campaign results", ["results/summary/unit_tests.log"]))

    selected, omitted = submission_inventory(root)
    secret_findings = []
    if scan_secrets:
        secrets = known_secrets(root)
        for path in selected:
            secret_findings.extend(scan_file(path, relative(path, root), secrets))
    checks.append(_check_item("submission_secret_scan", "FAIL" if secret_findings else "PASS" if scan_secrets else "PARTIAL", f"{len(selected)} eligible files scanned; {len(secret_findings)} findings. Secret values are never reported."))
    if secret_findings:
        errors.append("Secret scan findings must be resolved before packaging")
    if manifest_before and campaign_path.read_bytes() != manifest_before:
        warnings.append("Campaign changed while this audit ran; rerun after execution finishes")
    pending = [c["id"] for c in checks if c["status"] == "PARTIAL"]
    status = "FAIL" if errors else "PARTIAL" if pending or warnings else "PASS"
    return {"schema_version": 1, "audited_utc": now(), "status": status,
            "evidence_scope": "Offline consistency and packaging audit; no paid model calls or PLC invocations",
            "checks": checks, "pending_mandatory_or_delivery_checks": pending, "errors": errors,
            "warnings": warnings, "dataset": validation, "public_coverage": coverage,
            "compiler_preflight_recomputed": preflight_checks, "campaign_conditions": condition_statuses,
            "eligible_compilation_attempts_recomputed": sum(c["eligible"] for c in compile_checks),
            "metrics_recomputed": computed_metrics, "campaign_snapshot_sha256": hashlib.sha256(manifest_before).hexdigest() if manifest_before else None,
            "presentation_containers": ppt_info,
            "video_files": video_info, "secret_findings": secret_findings,
            "selected_file_count": len(selected), "selected_bytes": sum(p.stat().st_size for p in selected),
            "exclusions": omitted}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, help="Default: results/summary/submission_audit.json")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    result = audit(root)
    output = args.output or root / "results/summary/submission_audit.json"
    write_json(output, result)
    print(json.dumps({"status": result["status"], "audit": str(output), "errors": result["errors"],
                      "pending": result["pending_mandatory_or_delivery_checks"], "warnings": result["warnings"],
                      "secret_finding_count": len(result["secret_findings"])}, ensure_ascii=False, indent=2))
    return 1 if result["status"] == "FAIL" or (args.require_complete and result["status"] != "PASS") else 0


if __name__ == "__main__":
    raise SystemExit(main())
