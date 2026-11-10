from __future__ import annotations
import argparse
import csv
import hashlib
import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from .common import ROOT, digest, now, read_json, write_json, artifact_path
from .config import Settings
from .dataset import load_tasks, public_coverage, validate
from .harness import empty_result, run_harness
from .llm import ResponsesClient, ProviderError
from .compiler import compile_st, verify_evidence
from .metrics import aggregate, audit_records

def doctor(cfg):
    packages = {}
    for name in ("requests", "smolagents", "huggingface-hub", "rich", "python-dotenv"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    cli = shutil.which("codex")
    result = {"observed_utc": now(), "python": sys.executable, "prefix": sys.prefix,
              "project1_interpreter": Path(sys.prefix).name.casefold() == "project1",
              "isolated_environment": sys.prefix != sys.base_prefix,
              "local_environment_ready": sys.prefix != sys.base_prefix and all(packages.values()), "python_version": platform.python_version(),
              "os": platform.platform(), "packages": packages, "api_key_configured": bool(cfg.api_key),
              "base_url_configured": bool(cfg.base_url), "compiler_missing": cfg.compiler_ready(),
              "codesys_exe": cfg.codesys_exe or None, "profile": cfg.codesys_profile or None,
              "codex_cli": cli, "codex_version": subprocess.run([cli, "--version"], capture_output=True, text=True).stdout.strip() if cli else None}
    write_json(ROOT / "results/summary/environment.json", result)
    return result

def compiler_smoke(cfg):
    root = ROOT / "results/raw" / ("compiler_smoke_" + now().replace(":", "").replace(".", ""))
    good = {"declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT\n Start : BOOL;\n Stop : BOOL;\nEND_VAR\nVAR_OUTPUT\n Run : BOOL := FALSE;\nEND_VAR",
            "implementation": "IF Stop THEN\n Run := FALSE;\nELSIF Start THEN\n Run := TRUE;\nEND_IF;", "supporting_objects": []}
    bad = {**good, "implementation": "Run := ThisIdentifierDoesNotExist;"}
    runs = []
    for label, code in (("valid", good), ("invalid", bad), ("repaired", good)):
        runs.append({"label": label, **asdict(compile_st({"id": "SMOKE"}, code, root / label, cfg))})
    ok = [r["status"] for r in runs] == ["PASS", "COMPILE_FAIL", "PASS"]
    result = {"observed_utc": now(), "verified": ok, "expected_statuses": ["PASS", "COMPILE_FAIL", "PASS"],
              "runs": runs, "profile": cfg.codesys_profile, "codesys_exe": cfg.codesys_exe,
              "template_sha256": hashlib.sha256(Path(cfg.codesys_template).read_bytes()).hexdigest() if cfg.codesys_template and Path(cfg.codesys_template).is_file() else None}
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

def prepare_campaign(tasks):
    path = ROOT / "results/summary/campaign.json"
    if path.is_file():
        manifest = read_json(path)
        if manifest["dataset_sha256"] != digest(tasks):
            raise ValueError("Dataset changed: archive campaign manifest before preparing a new campaign")
        return manifest
    name = "campaign_" + now().replace(":", "").replace(".", "")
    conditions = read_json(ROOT / "configs/experiments.json")["conditions"]
    manifest = {"id": name, "created_utc": now(), "dataset_sha256": digest(tasks), "planned_tasks": len(tasks),
                "conditions": conditions, "records": {}}
    for condition in conditions:
        for task in tasks:
            p = ROOT / "experiments" / condition["id"] / name / task["id"] / "planned_result.json"
            write_json(p, empty_result(task, condition["id"], condition["model"], condition["framework"], "Awaiting verified compiler and model/framework compatibility"))
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
                actual_status, actual_success = verify_evidence(read_json(evidence), read_json(evidence.parent / "request.json"))
                if digest(read_json(evidence.parent / "candidate.json")) != attempt["source_sha256"]:
                    raise ValueError("Saved candidate differs from the compiled source hash")
                if actual_status != attempt["status"] or actual_success != attempt["success"]:
                    raise ValueError("Stored compiler result disagrees with actual diagnostics")
    result = {"generated_utc": now(), "campaign": manifest["id"], "conditions": aggregate(records, manifest["planned_tasks"]), "consistency_errors": errors}
    write_json(ROOT / "results/summary/metrics.json", result)
    fields = ["condition", "task_id", "framework", "model", "status", "first_pass_compiled", "final_compiled", "repair_attempts", "tool_call_count", "elapsed_seconds"]
    with (ROOT / "results/summary/task_results.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: r[key] for key in fields} for r in records)
    return result

def probe_models(cfg, smoke=False):
    client = ResponsesClient(cfg)
    catalog = client.models()
    write_json(ROOT / "results/raw/provider_model_catalog.json", catalog)
    identifiers = [m.get("id") for m in catalog.get("data", [])]
    selected = sorted({c["model"] for c in read_json(ROOT / "configs/experiments.json")["conditions"]})
    results = {"observed_utc": now(), "catalog_ids": identifiers, "selected": selected,
               "upstream_identity": "UNVERIFIED_RELAY_ALIAS", "model_tests": [], "prices": None, "context_limits": None}
    if smoke:
        # One real function tool invocation and one return for each selected model.
        tool = {"type": "function", "name": "echo_scan", "description": "Echo the integer scan value", "parameters": {
            "type": "object", "properties": {"scan": {"type": "integer"}}, "required": ["scan"], "additionalProperties": False}, "strict": True}
        for model in selected:
            entry = {"model": model, "listed": model in identifiers, "responses_streaming": False, "tool_roundtrip": False, "reasoning_effort": cfg.reasoning_effort}
            try:
                messages = [{"role": "user", "content": "Call echo_scan with scan=7. After its result, reply exactly OK."}]
                response = client.respond(model, messages, ROOT / "results/raw/model_probe" / model / "call", [tool], "required", max_tokens=512)
                calls = [o for o in response["output"] if o.get("type") == "function_call" and o.get("name") == "echo_scan"]
                entry["responses_streaming"] = True
                if len(calls) != 1 or json.loads(calls[0]["arguments"]) != {"scan": 7}:
                    raise ProviderError("Expected one exact function call")
                messages += response["output"]
                messages += [{"type": "function_call_output", "call_id": calls[0]["call_id"], "output": '{"scan":7}'}]
                final = client.respond(model, messages, ROOT / "results/raw/model_probe" / model / "return", [tool], max_tokens=512)
                entry["tool_roundtrip"] = final["text"].strip() == "OK"
                entry["reported_model"] = final["reported_model"]
                entry["usage"] = [response["usage"], final["usage"]]
            except ProviderError as exc:
                entry["error"] = str(exc)
            results["model_tests"].append(entry)
    write_json(ROOT / "results/summary/model_capabilities.json", results)
    return results

def main():
    parser = argparse.ArgumentParser(description="PLC ST coding benchmark (real CODESYS evidence required)")
    parser.add_argument("--config", default=str(ROOT / "configs/runtime.json"))
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd in ("doctor", "validate-dataset", "compiler-smoke", "prepare", "aggregate"):
        sub.add_parser(cmd)
    probe = sub.add_parser("probe-models"); probe.add_argument("--tool-smoke", action="store_true")
    run = sub.add_parser("run"); run.add_argument("--condition", choices=["E1", "E2", "E3", "E4", "all"], required=True)
    run.add_argument("--task"); run.add_argument("--rerun", action="store_true")
    test = sub.add_parser("test"); test.add_argument("--condition", choices=["E1", "E2", "E3", "E4", "all"], required=True)
    test.add_argument("--task"); test.add_argument("--rerun", action="store_true")
    imp = sub.add_parser("import-trace"); imp.add_argument("--condition", required=True); imp.add_argument("--task", required=True); imp.add_argument("--trace", required=True)
    args = parser.parse_args()
    cfg = Settings.load(args.config, load_api=args.command in ("run", "probe-models"))
    tasks = load_tasks()
    try:
        if args.command == "doctor":
            result = doctor(cfg)
        elif args.command == "validate-dataset":
            result = validate(tasks)
            source = ROOT.parent / "大作业题库json/大作业题库json/大作业题库.json"
            if not source.is_file():
                source = ROOT / "requirements/source/public_bank_original.json"
            if source.is_file():
                result["public_coverage"] = public_coverage(tasks, read_json(source))
            write_json(ROOT / "results/summary/dataset_validation.json", result)
        elif args.command == "probe-models":
            result = probe_models(cfg, args.tool_smoke)
        elif args.command == "compiler-smoke":
            result = compiler_smoke(cfg)
        elif args.command == "prepare":
            report = validate(tasks)
            if report["errors"] or report["by_kind"].get("public") != 20 or report["by_kind"].get("self_built", 0) < 10:
                raise ValueError("Dataset validation must pass with all20 official and >=10 self tasks")
            result = prepare_campaign(tasks)
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
            source_hash = row["compilation_attempts"][-1]["source_sha256"]
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
                    candidate = read_json(path.parent / "final_candidate.json")
                    outcome = run_functional(task, candidate, row["compilation_attempts"][-1]["source_sha256"], work, cfg)
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
                    item = {"condition": condition["id"], "task": task["id"], "functional_status": row["functional"]["status"],
                        "passed_cases": row["functional"]["passed_cases"], "evaluated_cases": row["functional"]["evaluated_cases"]}
                    outcomes.append(item)
                    print(json.dumps(item), flush=True)
            summarize()
            result = {"functional_runs": len(outcomes)}
        else:
            require_compiler_preflight(cfg)
            if not cfg.api_key:
                raise ValueError("API key missing")
            cap = read_json(ROOT / "results/summary/model_capabilities.json")
            ready = {x["model"] for x in cap["model_tests"] if x["tool_roundtrip"]}
            manifest = prepare_campaign(tasks)
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
                    work = ROOT / "experiments" / condition["id"] / manifest["id"] / task["id"] / ("run_" + now().replace(":", "").replace(".", ""))
                    if condition["framework"] == "self_harness":
                        row = run_harness(task, condition["model"], work, ResponsesClient(cfg), cfg, condition["id"])
                    elif condition["framework"] == "smolagents":
                        from .smol_baseline import run_smolagents
                        row = run_smolagents(task, condition["model"], work, cfg, condition["id"], client=ResponsesClient(cfg))
                    else:
                        from .baseline import run_codex
                        row = run_codex(task, condition["model"], work, cfg, condition["id"], args.config)
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
        if args.command == "validate-dataset" and (result["errors"] or not result.get("public_coverage", {}).get("verbatim_all_included", False)):
            return 1
        return 0
    except (ValueError, OSError, ProviderError, StopIteration) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
