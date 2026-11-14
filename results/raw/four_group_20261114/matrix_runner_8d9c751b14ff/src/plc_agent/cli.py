from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .common import ROOT, artifact_path, digest, now, read_json, write_json
from .compiler import compile_st, final_compile_attempt, verify_evidence
from .config import Settings
from .dataset import load_tasks, public_coverage, validate
from .harness import empty_result, run_harness
from .llm import ProviderError, ResponsesClient
from .metrics import aggregate, audit_records


def _selected_candidate_and_hash(row: dict, record_path: Path):
    """Load the final selected candidate and its verified compiler source hash."""
    candidate_file = record_path.with_name("final_candidate.json")
    candidate = read_json(candidate_file) if candidate_file.is_file() else row.get("final_candidate")
    if candidate is None:
        raise ValueError("Missing final candidate for compiled record")
    source_hash = final_compile_attempt(row, candidate).get("source_sha256")
    if not source_hash:
        raise ValueError("Missing final compiler source hash")
    return candidate, source_hash


def doctor(cfg):
    packages = {}
    for name in ("requests", "smolagents", "huggingface-hub", "rich", "python-dotenv"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    cli = shutil.which("codex")
    result = {
        "observed_utc": now(),
        "python": sys.executable,
        "prefix": sys.prefix,
        "project1_interpreter": Path(sys.prefix).name.casefold() == "project1",
        "isolated_environment": sys.prefix != sys.base_prefix,
        "local_environment_ready": sys.prefix != sys.base_prefix and bool(packages["requests"]),
        "python_version": platform.python_version(),
        "os": platform.platform(),
        "packages": packages,
        "api_key_configured": bool(cfg.api_key),
        "base_url_configured": bool(cfg.base_url),
        "compiler_missing": cfg.compiler_ready(),
        "codesys_exe": cfg.codesys_exe or None,
        "profile": cfg.codesys_profile or None,
        "codex_cli": cli,
        "codex_version": subprocess.run([cli, "--version"], capture_output=True, text=True).stdout.strip()
        if cli
        else None,
    }
    write_json(ROOT / "results/summary/environment.json", result)
    return result


def compiler_smoke(cfg):
    root = ROOT / "results/raw" / ("compiler_smoke_" + now().replace(":", "").replace(".", ""))
    good = {
        "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT\n Start : BOOL;\n Stop : BOOL;\nEND_VAR\nVAR_OUTPUT\n Run : BOOL := FALSE;\nEND_VAR",
        "implementation": "IF Stop THEN\n Run := FALSE;\nELSIF Start THEN\n Run := TRUE;\nEND_IF;",
        "supporting_objects": [],
    }
    bad = {**good, "implementation": "Run := ThisIdentifierDoesNotExist;"}
    runs = []
    for label, code in (("valid", good), ("invalid", bad), ("repaired", good)):
        runs.append({"label": label, **asdict(compile_st({"id": "SMOKE"}, code, root / label, cfg))})
    ok = [r["status"] for r in runs] == ["PASS", "COMPILE_FAIL", "PASS"]
    result = {
        "observed_utc": now(),
        "verified": ok,
        "expected_statuses": ["PASS", "COMPILE_FAIL", "PASS"],
        "runs": runs,
        "profile": cfg.codesys_profile,
        "codesys_exe": cfg.codesys_exe,
        "template_sha256": hashlib.sha256(Path(cfg.codesys_template).read_bytes()).hexdigest()
        if cfg.codesys_template and Path(cfg.codesys_template).is_file()
        else None,
    }
    write_json(root / "smoke_summary.json", result)
    write_json(ROOT / "results/summary/compiler_preflight.json", result)
    return result


def require_compiler_preflight(cfg):
    path = ROOT / "results/summary/compiler_preflight.json"
    if cfg.compiler_ready() or not path.is_file():
        raise ValueError("Real CODESYS valid-invalid-repaired preflight required before paid benchmark")
    pre = read_json(path)
    if not pre["verified"] or pre["profile"] != cfg.codesys_profile or pre["codesys_exe"] != cfg.codesys_exe:
        raise ValueError("Preflight not verified for this compiler configuration")
    if pre["template_sha256"] != hashlib.sha256(Path(cfg.codesys_template).read_bytes()).hexdigest():
        raise ValueError("Template changed since preflight")
    for run in pre["runs"]:
        evidence = artifact_path(run["evidence"])
        verify_evidence(read_json(evidence), read_json(evidence.parent / "request.json"))


def prepare_campaign(tasks, condition_filter="all"):
    path = ROOT / "results/summary/campaign.json"
    if path.is_file():
        manifest = read_json(path)
        if manifest["dataset_sha256"] != digest(tasks):
            raise ValueError("Dataset changed: archive campaign manifest before preparing a new campaign")
        if condition_filter != "all" and condition_filter not in {c["id"] for c in manifest["conditions"]}:
            raise ValueError(f"Existing campaign does not include requested condition {condition_filter}")
        return manifest
    name = "campaign_" + now().replace(":", "").replace(".", "")
    conditions = read_json(ROOT / "configs/experiments.json")["conditions"]
    if condition_filter != "all":
        conditions = [c for c in conditions if c["id"] == condition_filter]
        if not conditions:
            raise ValueError(f"Unknown experiment condition {condition_filter}")
    manifest = {
        "id": name,
        "created_utc": now(),
        "dataset_sha256": digest(tasks),
        "planned_tasks": len(tasks),
        "conditions": conditions,
        "records": {},
    }
    for condition in conditions:
        for task in tasks:
            p = ROOT / "experiments" / condition["id"] / name / task["id"] / "planned_result.json"
            write_json(
                p,
                empty_result(
                    task,
                    condition["id"],
                    condition["model"],
                    condition["framework"],
                    "Awaiting verified compiler and model/framework compatibility",
                ),
            )
            manifest["records"][condition["id"] + "/" + task["id"]] = str(p.relative_to(ROOT))
    write_json(path, manifest)
    return manifest


def summarize():
    manifest = read_json(ROOT / "results/summary/campaign.json")
    records = [read_json(ROOT / path) for path in manifest["records"].values()]
    errors = audit_records(records)
    for row in records:
        for attempt in row["compilation_attempts"]:
            if attempt["status"] in ("PASS", "COMPILE_FAIL"):
                evidence = artifact_path(attempt["evidence"])
                actual_status, actual_success = verify_evidence(
                    read_json(evidence), read_json(evidence.parent / "request.json")
                )
                if digest(read_json(evidence.parent / "candidate.json")) != attempt["source_sha256"]:
                    raise ValueError("Saved candidate differs from the compiled source hash")
                if actual_status != attempt["status"] or actual_success != attempt["success"]:
                    raise ValueError("Stored compiler result disagrees with actual diagnostics")
    result = {
        "generated_utc": now(),
        "campaign": manifest["id"],
        "conditions": aggregate(records, manifest["planned_tasks"]),
        "consistency_errors": errors,
    }
    write_json(ROOT / "results/summary/metrics.json", result)
    fields = [
        "condition",
        "task_id",
        "framework",
        "model",
        "status",
        "first_pass_compiled",
        "final_compiled",
        "repair_attempts",
        "tool_call_count",
        "elapsed_seconds",
    ]
    with (ROOT / "results/summary/task_results.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: r[key] for key in fields} for r in records)
    return result


def probe_models(cfg, smoke=False, requested_models=None):
    client = ResponsesClient(cfg)
    catalog = client.models()
    write_json(ROOT / "results/raw/provider_model_catalog.json", catalog)
    identifiers = [m.get("id") for m in catalog.get("data", [])]
    available_models = sorted({c["model"] for c in read_json(ROOT / "configs/experiments.json")["conditions"]})
    selected = sorted(set(requested_models)) if requested_models else available_models
    unknown_models = sorted(set(selected) - set(available_models))
    if unknown_models:
        raise ValueError(f"Requested model(s) not present in experiment config: {', '.join(unknown_models)}")
    results = {
        "observed_utc": now(),
        "catalog_ids": identifiers,
        "selected": selected,
        "upstream_identity": "UNVERIFIED_RELAY_ALIAS",
        "model_tests": [],
        "prices": None,
        "context_limits": None,
    }
    if smoke:
        # One real function tool invocation and one return for each selected model.
        tool = {
            "type": "function",
            "name": "echo_scan",
            "description": "Echo the integer scan value",
            "parameters": {
                "type": "object",
                "properties": {"scan": {"type": "integer"}},
                "required": ["scan"],
                "additionalProperties": False,
            },
            "strict": True,
        }
        for model in selected:
            entry = {
                "model": model,
                "listed": model in identifiers,
                "responses_streaming": False,
                "tool_roundtrip": False,
                "reasoning_effort": cfg.reasoning_effort,
            }
            try:
                messages = [
                    {"role": "user", "content": "Call echo_scan with scan=7. After its result, reply exactly OK."}
                ]
                response = client.respond(
                    model,
                    messages,
                    ROOT / "results/raw/model_probe" / model / "call",
                    [tool],
                    "required",
                    max_tokens=512,
                )
                calls = [
                    o for o in response["output"] if o.get("type") == "function_call" and o.get("name") == "echo_scan"
                ]
                entry["responses_streaming"] = True
                if len(calls) != 1 or json.loads(calls[0]["arguments"]) != {"scan": 7}:
                    raise ProviderError("Expected one exact function call")
                messages += response["output"]
                messages += [{"type": "function_call_output", "call_id": calls[0]["call_id"], "output": '{"scan":7}'}]
                final = client.respond(
                    model, messages, ROOT / "results/raw/model_probe" / model / "return", [tool], max_tokens=512
                )
                entry["tool_roundtrip"] = final["text"].strip() == "OK"
                entry["reported_model"] = final["reported_model"]
                entry["usage"] = [response["usage"], final["usage"]]
            except ProviderError as exc:
                entry["error"] = str(exc)
            results["model_tests"].append(entry)
    write_json(ROOT / "results/summary/model_capabilities.json", results)
    return results


def main():
    # Redirected Windows stdout may default to GBK; JSON remains ASCII-safe.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description="PLC ST coding benchmark (real CODESYS evidence required)")
    parser.add_argument("--config", default=None, help="Config file; defaults to runtime.local.json, then runtime.json")
    parser.add_argument("--allow-model-api", action="store_true", help="Use only after user authorization for this run")
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd in ("doctor", "validate-dataset", "compiler-smoke", "aggregate"):
        sub.add_parser(cmd)
    prep = sub.add_parser("prepare")
    prep.add_argument("--condition", default="all", help="Prepare only this configured condition or all conditions")
    probe = sub.add_parser("probe-models")
    probe.add_argument("--tool-smoke", action="store_true")
    probe.add_argument("--model", action="append", default=None, help="Probe only this configured model (repeatable)")
    run = sub.add_parser("run")
    run.add_argument("--condition", default="all", help="Condition ID or 'all'")
    run.add_argument("--task", "--task-id", dest="task", help="Optional single task ID")
    run.add_argument("--rerun", action="store_true", help="Force rerun")
    run.add_argument("--driver", default=None, help="Baseline driver (e.g. codex_cli, deepseek_harness, claude_code)")
    run.add_argument(
        "--spec-visible", dest="spec_visible", action="store_true", default=None, help="Make specifications visible"
    )
    run.add_argument("--spec-hidden", dest="spec_visible", action="store_false", help="Hide specifications")
    run.add_argument("--ablation", default=None, help="Ablation type (no_planner, no_dialect, no_selftest)")

    test = sub.add_parser("test")
    test.add_argument("--condition", default="all", help="Condition ID or 'all'")
    test.add_argument("--task", "--task-id", dest="task", help="Optional single task ID")
    test.add_argument("--rerun", action="store_true")

    imp = sub.add_parser("import-trace")
    imp.add_argument("--condition", required=True)
    imp.add_argument("--task", "--task-id", dest="task", required=True)
    imp.add_argument("--trace", required=True)

    exp_verify = sub.add_parser("export-verify")
    exp_verify.add_argument("--task", "--task-id", dest="task", required=True, help="Task ID (e.g. PUB001)")
    exp_verify.add_argument("--candidate", default=None, help="Candidate source path (.json or .st)")
    exp_verify.add_argument("--out-dir", default=None, help="Output directory for verification bundle")

    ver_cand = sub.add_parser("verify-candidate", help="Formally verify ST candidate(s) via ST->SMV + NuSMV/nuXmv")
    ver_cand.add_argument("--task", "--task-id", dest="task", default=None, help="Task ID (e.g. SELF001, PUB006)")
    ver_cand.add_argument("--candidate", default=None, help="Candidate source path (.json or .st)")
    ver_cand.add_argument("--reference", action="store_true", help="Verify codesys/examples/<task>.json reference ST")
    ver_cand.add_argument("--all-references", action="store_true", help="Verify all reference STs and summarize")
    ver_cand.add_argument(
        "--condition", default=None, help="Condition id whose campaign final_candidates should be verified"
    )
    ver_cand.add_argument("--out-dir", default=None, help="Output directory")
    ver_cand.add_argument("--timeout", type=int, default=60, help="Per-task verification timeout seconds")

    imp_verify = sub.add_parser("import-verify")
    imp_verify.add_argument("--bundle-dir", required=True, help="Verification bundle directory")
    imp_verify.add_argument("--evidence", required=True, help="Verification evidence file")

    model_check = sub.add_parser("check-model", help="Check an explicitly encoded SMV model using local NuSMV or nuXmv")
    model_check.add_argument("--model", required=True, help="SMV model path (not ST)")
    model_check.add_argument("--out-dir", required=True)
    model_check.add_argument(
        "--executable",
        default=None,
        help="NuSMV/nuXmv executable path or name; otherwise use NUXMV_EXE/NUSMV_EXE, local installation, or PATH",
    )
    model_check.add_argument("--timeout", type=int, default=60)
    model_check.add_argument(
        "--tool", choices=["auto", "nusmv", "nuxmv"], default="auto", help="Model checker backend (default: auto)"
    )
    model_check.add_argument(
        "--engine",
        choices=["auto", "bdd", "smt"],
        default="auto",
        help="Verification engine (default: auto selects smt for integer/real/array/word models)",
    )

    rand_test = sub.add_parser("random-test")
    rand_test.add_argument("--task", "--task-id", dest="task", required=True, help="Task ID (e.g. PUB001)")
    rand_test.add_argument("--seed", type=int, default=20261110, help="Random seed")
    rand_test.add_argument("--num-cases", type=int, default=None, help="Number of random test cases")
    rand_test.add_argument("--steps-per-case", type=int, default=None, help="Steps per random test case")
    rand_test.add_argument("--out", default=None, help="Optional output JSON file")

    web = sub.add_parser("web", help="Launch interactive Auto-Test & Trace Inspector WebUI")
    web.add_argument("--host", default="127.0.0.1", help="Host interface to bind")
    web.add_argument("--port", type=int, default=8765, help="Port to listen on")
    web.add_argument("--config", default=argparse.SUPPRESS, help="Config file path")

    cfg_p = sub.add_parser("configure", help="Configure local CODESYS paths and API credentials")
    cfg_p.add_argument("--codesys-exe", default=None, help="Path to CODESYS.exe")
    cfg_p.add_argument("--profile", default=None, help="CODESYS profile string (e.g. 'CODESYS V3.5 SP19')")
    cfg_p.add_argument("--template", default=None, help="CODESYS template project path")
    cfg_p.add_argument("--base-url", default=None, help="LLM API Base URL")
    cfg_p.add_argument("--api-key", default=None, help="LLM API Key")
    cfg_p.add_argument("--save-global", action="store_true", help="Save to runtime.json instead of runtime.local.json")

    ref_p = sub.add_parser("test-reference", help="Compile and simulate reference ST solution offline (0 API tokens)")
    ref_p.add_argument("--task", "--task-id", dest="task", default="SELF001", help="Task ID (default: SELF001)")
    ref_p.add_argument("--backend", choices=["auto", "codesys", "fake"], default="auto", help="Execution backend")
    ref_p.add_argument("--out-dir", default=None, help="Output directory for test evidence")
    args = parser.parse_args()
    if args.command in ("run", "probe-models") and not args.allow_model_api:
        parser.error("Model calls require explicit authorization and --allow-model-api")
    cfg = Settings.load(args.config, load_api=args.command in ("run", "probe-models"))
    tasks = load_tasks()
    try:
        if args.command == "doctor":
            result = doctor(cfg)
        elif args.command == "check-model":
            from .model_checker import check_model

            result = check_model(
                args.model,
                args.out_dir,
                args.executable,
                args.timeout,
                tool=args.tool,
                engine=args.engine,
            )
        elif args.command == "validate-dataset":
            result = validate(tasks)
            source = ROOT.parent / "大作业题库json/大作业题库json/大作业题库.json"
            if not source.is_file():
                source = ROOT / "requirements/source/public_bank_original.json"
            if source.is_file():
                result["public_coverage"] = public_coverage(tasks, read_json(source))
            write_json(ROOT / "results/summary/dataset_validation.json", result)
        elif args.command == "probe-models":
            result = probe_models(cfg, args.tool_smoke, args.model)
        elif args.command == "compiler-smoke":
            result = compiler_smoke(cfg)
        elif args.command == "prepare":
            report = validate(tasks)
            if report["errors"] or report["by_kind"].get("public") != 20 or report["by_kind"].get("self_built", 0) < 10:
                raise ValueError("Dataset validation must pass with all20 official and >=10 self tasks")
            result = prepare_campaign(tasks, args.condition)
            result = {"campaign": result["id"], "planned_runs": len(result["records"])}
        elif args.command == "aggregate":
            result = summarize()
        elif args.command == "import-trace":
            from .functional import evaluate_trace

            manifest = read_json(ROOT / "results/summary/campaign.json")
            task = next(t for t in tasks if t["id"] == args.task)
            path = ROOT / manifest["records"][args.condition + "/" + args.task]
            row = read_json(path)
            if not row["final_compiled"]:
                raise ValueError("A verified compiled candidate is required")
            _, source_hash = _selected_candidate_and_hash(row, path)
            trace = read_json(args.trace)
            original_root = Path(args.trace).resolve().parent
            checked = evaluate_trace(task, source_hash, trace, evidence_root=original_root)
            evidence_dir = path.parent / "functional_evidence"
            evidence_dir.mkdir(exist_ok=True)
            stored_refs = []
            for i, evidence in enumerate(checked["evidence_files"]):
                source = Path(evidence["path"])
                target = evidence_dir / (f"{i:03d}_" + source.name)
                shutil.copy2(source, target)
                stored_refs.append({"path": str(target.relative_to(path.parent)), "sha256": evidence["sha256"]})
            trace["evidence_files"] = stored_refs
            row["functional"] = evaluate_trace(task, source_hash, trace, evidence_root=path.parent)
            row["status"] = row["functional"]["status"]
            row["reason"] = "Actual operator-recorded CODESYS trace evaluated"
            write_json(path.parent / "functional_trace.json", trace)
            write_json(path, row)
            result = row["functional"]
        elif args.command == "test":
            from .simulation import run_functional

            manifest = read_json(ROOT / "results/summary/campaign.json")
            outcomes = []
            for condition in manifest["conditions"]:
                if args.condition not in ("all", condition["id"]):
                    continue
                for task in tasks:
                    if args.task and task["id"] != args.task:
                        continue
                    path = ROOT / manifest["records"][condition["id"] + "/" + task["id"]]
                    row = read_json(path)
                    if not row["final_compiled"] or (row["functional"]["evaluated_cases"] > 0 and not args.rerun):
                        continue
                    work = path.parent / ("functional_" + now().replace(":", "").replace(".", ""))
                    candidate, source_hash = _selected_candidate_and_hash(row, path)
                    outcome = run_functional(task, candidate, source_hash, work, cfg)
                    if outcome.get("functional"):
                        row["functional"] = outcome["functional"]
                        if row["status"] in ("UNVERIFIED", "PASS", "TEST_FAIL"):
                            row["status"] = row["functional"]["status"]
                            row["reason"] = "Actual CODESYS IDE simulation of fixed dataset tests"
                    else:
                        row["functional"]["status"] = outcome["status"]
                        row["functional"]["reason"] = outcome.get("reason") or outcome.get("infrastructure_error")
                    row["functional_execution"] = outcome
                    write_json(path, row)
                    item = {
                        "condition": condition["id"],
                        "task": task["id"],
                        "functional_status": row["functional"]["status"],
                        "passed_cases": row["functional"]["passed_cases"],
                        "evaluated_cases": row["functional"]["evaluated_cases"],
                    }
                    outcomes.append(item)
                    print(json.dumps(item), flush=True)
            summarize()
            result = {"functional_runs": len(outcomes)}
        elif args.command == "export-verify":
            from .formal_verify import export_verification_bundle

            task = next((t for t in tasks if t["id"] == args.task), None)
            if not task:
                raise ValueError(f"Task {args.task} not found")
            cand_path = Path(args.candidate) if args.candidate else (ROOT / f"codesys/examples/{args.task}.json")
            if not cand_path.is_file():
                cand_path = ROOT / f"codesys/examples/{args.task}.json"
            if cand_path.suffix == ".json":
                candidate_data = read_json(cand_path)
            else:
                candidate_data = cand_path.read_text(encoding="utf-8")
            out_dir = Path(args.out_dir) if args.out_dir else (ROOT / "results/verification" / args.task)
            result = export_verification_bundle(task, candidate_data, out_dir)
        elif args.command == "verify-candidate":
            from .formal_verify import verify_candidate
            from .metrics import rate

            base_out = Path(args.out_dir) if args.out_dir else (ROOT / "results/verification")
            tasks_by_id = {t["id"]: t for t in tasks}

            def _load_cand(path: Path) -> Any:
                return read_json(path) if path.suffix == ".json" else path.read_text(encoding="utf-8")

            if args.all_references:
                rows_summary: list[dict[str, Any]] = []
                for ex_path in sorted((ROOT / "codesys/examples").glob("*.json")):
                    tid = ex_path.stem
                    t_obj = tasks_by_id.get(tid)
                    if not t_obj:
                        continue
                    v_res = verify_candidate(
                        t_obj, read_json(ex_path), base_out / "references" / tid, timeout=args.timeout
                    )
                    rows_summary.append(
                        {
                            "task_id": tid,
                            "status": v_res.get("status"),
                            "verified": v_res.get("verified"),
                            "passed_properties": v_res.get("passed_properties"),
                            "total_properties": v_res.get("total_properties"),
                            "property_pass_ratio": v_res.get("property_pass_ratio"),
                            "tool": v_res.get("tool"),
                            "engine": v_res.get("engine"),
                            "reason": v_res.get("reason"),
                        }
                    )
                evaluated = [r for r in rows_summary if r["status"] in ("PASS", "COUNTEREXAMPLE")]
                passed_n = sum(1 for r in evaluated if r["status"] == "PASS")
                ratios = [r["property_pass_ratio"] for r in evaluated if r.get("property_pass_ratio") is not None]
                result = {
                    "mode": "all_references",
                    "total_reference_st_files": len(rows_summary),
                    "supported_evaluated_tasks": len(evaluated),
                    "passed_tasks": passed_n,
                    "task_pass_rate": rate(passed_n, len(evaluated)) if evaluated else None,
                    "mean_property_pass_ratio": (sum(ratios) / len(ratios)) if ratios else None,
                    "results": rows_summary,
                }
                write_json(ROOT / "results/summary/st_formal_verification.json", result)
            elif args.condition:
                manifest = read_json(ROOT / "results/summary/campaign.json")
                updated = 0
                eval_rows: list[dict[str, Any]] = []
                for key, rel_path in manifest.get("records", {}).items():
                    if not key.startswith(f"{args.condition}/"):
                        continue
                    rec_path = ROOT / rel_path
                    if not rec_path.is_file():
                        continue
                    rec = read_json(rec_path)
                    tid = rec.get("task_id")
                    t_obj = tasks_by_id.get(tid)
                    cand = rec.get("final_candidate")
                    if not t_obj or cand is None:
                        continue
                    v_res = verify_candidate(t_obj, cand, rec_path.parent / "formal_verify", timeout=args.timeout)
                    rec["verification"] = v_res
                    write_json(rec_path, rec)
                    updated += 1
                    eval_rows.append(
                        {
                            "task_id": tid,
                            "status": v_res.get("status"),
                            "property_pass_ratio": v_res.get("property_pass_ratio"),
                        }
                    )
                summarize()
                result = {
                    "mode": "condition",
                    "condition": args.condition,
                    "updated_records": updated,
                    "results": eval_rows,
                }
            else:
                if not args.task:
                    raise ValueError("Specify --task, --all-references, or --condition")
                t_obj = tasks_by_id.get(args.task)
                if not t_obj:
                    raise ValueError(f"Task {args.task} not found")
                if args.candidate:
                    cand_path = Path(args.candidate)
                    if not cand_path.is_file():
                        raise ValueError(f"Candidate file not found: {cand_path}")
                    cand_data = _load_cand(cand_path)
                elif args.reference or (ROOT / f"codesys/examples/{args.task}.json").is_file():
                    cand_data = read_json(ROOT / f"codesys/examples/{args.task}.json")
                else:
                    raise ValueError(f"No --candidate given and no reference ST exists for {args.task}")
                result = verify_candidate(t_obj, cand_data, base_out / args.task, timeout=args.timeout)
        elif args.command == "import-verify":
            from .formal_verify import import_verification_evidence

            result = import_verification_evidence(Path(args.bundle_dir), Path(args.evidence))
        elif args.command == "random-test":
            from .random_testing import generate_random_cases

            task = next((t for t in tasks if t["id"] == args.task), None)
            if not task:
                raise ValueError(f"Task {args.task} not found")
            cases = generate_random_cases(
                task, seed=args.seed, num_cases=args.num_cases, steps_per_case=args.steps_per_case
            )
            if args.out:
                write_json(Path(args.out), cases)
            result = {"task": task["id"], "cases_generated": len(cases), "seed": args.seed}
        elif args.command == "web":
            from .webui import serve_webui

            serve_webui(args.host, args.port, cfg)
            return 0
        elif args.command == "configure":
            from .config import detect_codesys

            if args.config and args.config != str(ROOT / "configs/runtime.json"):
                target = Path(args.config)
            else:
                target = ROOT / ("configs/runtime.json" if args.save_global else "configs/runtime.local.json")
            default_path = ROOT / "configs/runtime.json"
            current = (
                read_json(target) if target.is_file() else (read_json(default_path) if default_path.is_file() else {})
            )
            if args.codesys_exe:
                current["codesys_exe"] = args.codesys_exe
            elif os.name == "nt" and (not current.get("codesys_exe") or not Path(current["codesys_exe"]).is_file()):
                found_exe, found_prof = detect_codesys()
                if found_exe:
                    current["codesys_exe"] = found_exe
                    if found_prof and not args.profile and not current.get("codesys_profile"):
                        current["codesys_profile"] = found_prof
            if args.profile:
                current["codesys_profile"] = args.profile
            if args.template:
                current["codesys_template"] = args.template
            elif "codesys_template" not in current or not Path(current.get("codesys_template", "")).is_file():
                current["codesys_template"] = "codesys/templates/benchmark.project"
            if args.base_url:
                current["base_url"] = args.base_url
            write_json(target, current)
            updated_cfg = Settings.load(target)
            saved_str = str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else str(target)
            result = {
                "saved_to": saved_str,
                "codesys_exe": updated_cfg.codesys_exe,
                "codesys_profile": updated_cfg.codesys_profile,
                "codesys_template": updated_cfg.codesys_template,
                "compiler_ready": len(updated_cfg.compiler_ready()) == 0,
                "compiler_missing": updated_cfg.compiler_ready(),
            }
        elif args.command == "test-reference":
            from .backend import CodesysBackend, FakeBackend

            task = next((t for t in tasks if t["id"] == args.task), None)
            if not task:
                raise ValueError(f"Task {args.task} not found")
            example_file = ROOT / "codesys/examples" / f"{args.task}.json"
            if not example_file.is_file():
                avail = [p.stem for p in sorted((ROOT / "codesys/examples").glob("*.json"))]
                raise ValueError(f"No reference ST found for {args.task}. Available: {', '.join(avail)}")
            candidate = read_json(example_file)
            use_codesys = args.backend != "fake"
            b_name = "CodesysBackend" if use_codesys else "FakeBackend"
            backend = CodesysBackend(cfg) if use_codesys else FakeBackend()
            ws = Path(args.out_dir) if args.out_dir else (ROOT / "results/raw/test_reference" / args.task)
            ws.mkdir(parents=True, exist_ok=True)
            print(f"[{b_name}] Step 1: Compiling reference candidate for {args.task} ...", flush=True)
            comp_res = backend.compile(task, candidate, ws / "compile")
            compile_ok = comp_res.status == "PASS"
            print(f"[{b_name}] Compile Status: {comp_res.status}", flush=True)
            sim_status = "NOT_RUN"
            passed_cases, total_cases = 0, len(task.get("tests", []))
            failures_summary = []
            if compile_ok:
                print(f"[{b_name}] Step 2: Simulating candidate against {total_cases} test cases ...", flush=True)
                sim_res = backend.simulate(task, candidate, task.get("tests", []), ws / "simulate")
                sim_status = sim_res.status
                passed_cases = sim_res.passed_cases
                total_cases = sim_res.evaluated_cases
                for f in sim_res.failures[:3]:
                    failures_summary.append(
                        {
                            "case_id": f.case_id,
                            "bad_step": f.first_bad_step,
                            "field": f.field,
                            "expected": f.expected,
                            "observed": f.observed,
                        }
                    )
                print(
                    f"[{b_name}] Simulation Status: {sim_status} ({passed_cases}/{total_cases} cases passed)",
                    flush=True,
                )
            ws_str = str(ws.relative_to(ROOT)) if ws.is_relative_to(ROOT) else str(ws)
            result = {
                "task": args.task,
                "backend": b_name,
                "compile_status": comp_res.status,
                "simulation_status": sim_status,
                "passed_cases": passed_cases,
                "total_cases": total_cases,
                "failures": failures_summary,
                "passed": compile_ok and sim_status == "PASS",
                "workspace": ws_str,
            }
        else:
            require_compiler_preflight(cfg)
            if not cfg.api_key:
                raise ValueError("API key missing")
            cap = read_json(ROOT / "results/summary/model_capabilities.json")
            ready = {x["model"] for x in cap["model_tests"] if x["tool_roundtrip"]}
            manifest = prepare_campaign(tasks, args.condition)
            selected_conditions = [c for c in manifest["conditions"] if args.condition in ("all", c["id"])]
            outcomes = []
            for condition in selected_conditions:
                if condition["model"] not in ready:
                    raise ValueError("Selected model Responses tool compatibility unverified")
                for task in tasks:
                    if args.task and task["id"] != args.task:
                        continue
                    key = condition["id"] + "/" + task["id"]
                    old = read_json(ROOT / manifest["records"][key])
                    if old["status"] != "NOT_RUN" and not args.rerun:
                        continue
                    work = (
                        ROOT
                        / "experiments"
                        / condition["id"]
                        / manifest["id"]
                        / task["id"]
                        / ("run_" + now().replace(":", "").replace(".", ""))
                    )
                    spec_vis = (
                        args.spec_visible if args.spec_visible is not None else condition.get("spec_visible", True)
                    )
                    ablation = args.ablation or condition.get("ablation")
                    if condition["framework"] == "self_harness":
                        row = run_harness(
                            task,
                            condition["model"],
                            work,
                            ResponsesClient(cfg),
                            cfg,
                            condition["id"],
                            spec_visible=spec_vis,
                            ablation=ablation,
                        )
                    else:
                        from .baseline import run_baseline

                        driver = args.driver or condition.get("driver", "deepseek_harness")
                        row = run_baseline(
                            task,
                            condition["model"],
                            work,
                            cfg,
                            condition=condition["id"],
                            driver=driver,
                            client=ResponsesClient(cfg),
                            spec_visible=spec_vis,
                            config_path=args.config,
                        )
                    # Merge only the completed run pointer so concurrent condition workers
                    # never overwrite unrelated results from a stale manifest snapshot.
                    manifest = read_json(ROOT / "results/summary/campaign.json")
                    previous_path = manifest["records"][key]
                    if read_json(ROOT / previous_path)["status"] != "NOT_RUN":
                        manifest.setdefault("run_history", {}).setdefault(key, []).append(previous_path)
                    manifest["records"][key] = str((work / "result.json").relative_to(ROOT))
                    write_json(ROOT / "results/summary/campaign.json", manifest)
                    outcomes.append({"condition": condition["id"], "task": task["id"], "status": row["status"]})
                    print(json.dumps(outcomes[-1]), flush=True)
            summarize()
            result = {"executed_runs": len(outcomes)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == "validate-dataset" and (
            result["errors"] or not result.get("public_coverage", {}).get("verbatim_all_included", False)
        ):
            return 1
        if args.command == "compiler-smoke" and not result.get("verified"):
            return 1
        if args.command == "test-reference" and not result.get("passed"):
            return 1
        if args.command == "check-model" and result.get("status") != "MODEL_PROPERTIES_TRUE":
            return 1
        return 0
    except (ValueError, OSError, ProviderError, StopIteration) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
