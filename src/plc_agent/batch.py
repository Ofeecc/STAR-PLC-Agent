"""Resumable, bounded multi-process evaluation of actual candidate ST.

Independent tasks overlap API/solver work. All IDE operations retain the shared
CODESYS lock. Model access is opt-in; evaluating saved candidates is the default.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import multiprocessing
import os
import time
import traceback
import uuid
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from dataclasses import asdict
from pathlib import Path

from .common import ROOT, artifact_path, digest, now, read_json, redact, write_json
from .compiler import compiler_lock, final_compile_attempt, normalize_candidate, verify_evidence
from .config import Settings
from .dataset import load_tasks, validate

PILOT = ("PUB001", "PUB003", "PUB007", "PUB009", "PUB015", "PUB016")
STAGES = ("compile", "functional", "formal")
INFRA = {"TOOL_ERROR", "TIMEOUT", "UNVERIFIED", "MISSING_CANDIDATE", "STOPPED"}
MODEL = "deepseek-v4.1-flash-1017"


def select_tasks(tasks, selection):
    if selection in ("all", "public", "self"):
        return [t for t in tasks if selection == "all" or
                t["id"].startswith("PUB" if selection == "public" else "SELF")]
    ids = list(PILOT) if selection == "pilot" else selection.upper().split(",")
    ids = [tid.strip() for tid in ids]
    by_id = {t["id"]: t for t in tasks}
    if not ids or len(ids) != len(set(ids)) or any(tid not in by_id for tid in ids):
        raise ValueError("Task IDs must be unique and present in the dataset: " + selection)
    return [by_id[tid] for tid in ids]


def code_fingerprint():
    files = sorted((ROOT / "src/plc_agent").glob("*.py")) + sorted((ROOT / "codesys/scripts").glob("*.py"))
    # Observers are part of the proof input, not just generated artifacts.
    files += sorted((ROOT / "models").rglob("*.smv"))
    return digest({str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files})


def find_record(source, task_id):
    base = Path(source) / task_id
    return next((p for p in (base / "generation/result.json", base / "result.json") if p.is_file()), None)


def load_source(record, task, model, driver=None):
    row = read_json(record)
    if row.get("task_id") != task["id"] or row.get("task_sha256") != digest(task):
        raise ValueError("Generation record does not match current task/spec/test hashes")
    if row.get("model") != model:
        raise ValueError("Generation record model differs from selected model")
    if driver and row.get("framework") not in (("star", "self_harness") if driver == "star" else (driver,)):
        raise ValueError("Generation record framework differs from selected driver")
    candidate_file = record.with_name("final_candidate.json")
    candidate = read_json(candidate_file) if candidate_file.is_file() else row.get("final_candidate")
    return row, normalize_candidate(candidate) if candidate is not None else None


def next_attempt(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for number in range(1, 10000):
        target = directory / f"attempt_{number:04d}"
        if not target.exists():
            return target
    raise ValueError("Too many stage attempts")


def _reused_compile(row, candidate):
    attempt = final_compile_attempt(row, candidate)
    evidence_path = artifact_path(attempt.get("evidence") or "missing_evidence.json")
    evidence = read_json(evidence_path)
    status, success = verify_evidence(evidence, {
        "request_id": attempt.get("request_id"), "source_sha256": digest(candidate)})
    if not success or attempt.get("process_exit_code") != 0:
        raise ValueError("Saved compilation does not prove success")
    return dict(attempt, status=status, success=success, evidence=str(evidence_path))


def stage_result(work, stage, key, options, action):
    cache = work / f"{stage}.json"
    if cache.is_file():
        saved = read_json(cache)
        if saved.get("key") != key:
            raise ValueError("Stage inputs changed; choose a new --out-dir: " + str(cache))
        if not (options["retry_infra"] and saved["result"].get("status") in INFRA):
            return dict(saved, cached=True)
    attempt = next_attempt(work / stage)
    started = time.monotonic()
    result, mode = action(attempt)
    saved = {"key": key, "stage": stage, "result": result, "mode": mode,
             "elapsed_seconds": time.monotonic() - started, "finished_utc": now(),
             "attempt_dir": str(attempt), "cached": False}
    write_json(cache, saved)
    return saved


def run_task(job):
    """Runs in an isolated spawned process; never shares a model client or IDE."""
    from .compiler import compile_st
    from .formal_verify import verify_candidate
    from .functional import evaluate_trace
    from .simulation import run_functional

    task, options = job["task"], job["options"]
    work = Path(options["out_dir"]) / task["id"]
    work.mkdir(parents=True, exist_ok=True)
    cfg = Settings(**options["settings"])
    started = time.monotonic()
    row = {"task_id": task["id"], "difficulty": task["difficulty"], "model": options["model"],
           "planned_cases": len(task["tests"]), "status": "PARTIAL", "new_llm_calls": 0,
           "compiled": None, "driver": options.get("driver", "star"), "condition": options.get("condition", "E3"),
           "stages": {}, "functional": {"status": "NOT_RUN"},
           "verification": {"status": "NOT_RUN"}, "started_utc": now()}

    def progress(stage):
        write_json(work / "progress.json", {"task_id": task["id"], "stage": stage, "utc": now(), "pid": os.getpid()})
        if (Path(options["out_dir"]) / "STOP").exists():
            raise InterruptedError("STOP requested; no new stage launched")

    try:
        progress("load_candidate")
        record = find_record(options["out_dir"], task["id"]) or find_record(options["source_dir"], task["id"])
        if record is None:
            if not options["generate_missing"]:
                row.update(status="MISSING_CANDIDATE", reason="No saved generation record; no model request made")
                return _finish(work, row, started)
            generation = work / "generation"
            if generation.exists() and any(generation.iterdir()):
                raise ValueError("Incomplete generation artifacts exist; inspect before authorizing a new run")
            progress("generation")
            cfg = Settings.load(options.get("config"), load_api=True)
            if not cfg.api_key:
                raise ValueError("API key missing")
            if options.get("driver", "star") == "star":
                from .harness import run_harness
                from .llm import ResponsesClient
                generated = run_harness(task, options["model"], generation, ResponsesClient(cfg), cfg, options.get("condition", "E3"))
            else:
                from .baseline import run_baseline
                generated = run_baseline(task, options["model"], generation, cfg,
                                         condition=options["condition"], driver=options["driver"])
            row["new_llm_calls"] = generated.get("llm_calls", 0)
            record = generation / "result.json"
        source, candidate = load_source(record, task, options["model"], options.get("driver"))
        # Generated records remain authoritative after an interrupted worker.
        if record.parent == work / "generation":
            row["new_llm_calls"] = source.get("llm_calls", 0)
        row.update(generation_record=str(record), generation_status=source.get("status"),
                   source_llm_calls=source.get("llm_calls", 0), usage=source.get("usage", []))
        if candidate is None:
            source_status = source.get("status")
            status = ("FAIL" if source_status in ("COMPILE_FAIL", "TEST_FAIL") else
                      source_status if source_status in INFRA else "UNVERIFIED")
            row.update(status=status, reason=source.get("reason") or "No selected candidate")
            return _finish(work, row, started)
        sha = digest(candidate)
        row["source_sha256"] = sha
        write_json(work / "candidate.json", candidate)
        key = digest({"task": digest(task), "source": sha, "manifest": options["fingerprint"]})

        for stage in options["stages"]:
            progress(stage)

            def execute(attempt):
                if stage == "compile":
                    if not options["recompile"]:
                        try:
                            return _reused_compile(source, candidate), "saved_verified_compilation"
                        except (OSError, ValueError, KeyError):
                            pass
                    return asdict(compile_st(task, candidate, attempt, cfg)), "fresh_codesys_compilation"
                if stage == "functional":
                    if options["reuse_traces"]:
                        trace_path = record.parent.parent / "fixed_tests/trace.json"
                        if record.parent.name != "generation":
                            trace_path = record.parent / "fixed_tests/trace.json"
                        trace = read_json(trace_path)
                        evaluated = evaluate_trace(task, sha, trace, evidence_root=trace_path.parent, allow_timing_gaps=True)
                        return dict(evaluated, original_trace=str(trace_path)), "replayed_real_trace_no_new_simulation"
                    return run_functional(task, candidate, sha, attempt, cfg), "fresh_codesys_simulation"
                return verify_candidate(task, candidate, attempt, timeout=options["formal_timeout"]), "fresh_st_to_smv_check"

            saved = stage_result(work, stage, key, options, execute)
            row["stages"][stage] = saved
            outcome = saved["result"]
            if stage == "compile":
                row["compiled"] = outcome.get("success") is True and outcome.get("status") == "PASS"
                if not row["compiled"]:
                    row["status"] = "FAIL" if outcome.get("status") == "COMPILE_FAIL" else outcome.get("status", "TOOL_ERROR")
                    row["reason"] = outcome.get("infrastructure_error")
                    break
            elif stage == "functional":
                row["functional"] = outcome.get("functional") or outcome
                # An execution/cleanup failure must not be hidden by a nested test verdict.
                if outcome.get("status") in INFRA:
                    row["functional"] = dict(row["functional"], status=outcome["status"], reason=outcome.get("reason"))
            else:
                row["verification"] = outcome
        f, v = row["functional"], row["verification"]
        row["stage_checks_passed"] = f["status"] == "PASS" and v["status"] == "PASS"
        statuses = [s["result"].get("status") for s in row["stages"].values()] + [f["status"], v["status"]]
        infra = next((s for s in statuses if s in INFRA), None)
        if infra:
            row["status"] = infra
        elif any(s in ("COMPILE_FAIL", "TEST_FAIL", "COUNTEREXAMPLE") for s in statuses):
            row["status"] = "FAIL"
        elif row["compiled"] and f["status"] == "PASS" and v.get("full_specification_verified"):
            row["status"] = "PASS"
    except InterruptedError as exc:
        row.update(status="STOPPED", reason=str(exc))
    except Exception as exc:
        row.update(status="TOOL_ERROR", reason=redact(f"{type(exc).__name__}: {exc}", (cfg.api_key,)))
        (work / "error.txt").write_text(redact(traceback.format_exc(), (cfg.api_key,)), encoding="utf-8")
    return _finish(work, row, started)


def _finish(work, row, started):
    row.update(finished_utc=now(), elapsed_seconds=time.monotonic() - started)
    write_json(work / "fullflow_result.json", row)
    write_json(work / "progress.json", {"task_id": row["task_id"], "stage": "finished", "status": row["status"], "utc": now()})
    return row


def save_summary(out, tasks, results, started, stopped, invocation_id):
    rows = [results[t["id"]] for t in tasks if t["id"] in results]
    summary = {"updated_utc": now(), "invocation_id": invocation_id, "planned_tasks": len(tasks), "completed_tasks": len(rows),
               "stopped": stopped, "pending_tasks": [t["id"] for t in tasks if t["id"] not in results],
               "elapsed_seconds": time.monotonic() - started,
               "compiled_tasks": sum(r["compiled"] is True for r in rows),
               "fixed_passed_cases": sum(r["functional"].get("passed_cases", 0) for r in rows),
               "fixed_evaluated_cases": sum(r["functional"].get("evaluated_cases", 0) for r in rows),
               "new_generation_llm_calls_in_output": sum(r.get("new_llm_calls", 0) for r in rows),
               "results": rows}
    write_json(out / "summary.json", summary)
    write_json(out / "invocations" / invocation_id / "summary.json", summary)
    table = [{"task": r["task_id"], "difficulty": r["difficulty"], "compiled": r["compiled"],
              "passed_cases": r["functional"].get("passed_cases", 0),
              "evaluated_cases": r["functional"].get("evaluated_cases", 0), "planned_cases": r["planned_cases"],
              "formal": r["verification"]["status"], "overall": r["status"],
              "elapsed_seconds": round(r["elapsed_seconds"], 2)} for r in rows]
    with (out / "summary.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(table[0]) if table else ["task", "overall"])
        writer.writeheader(); writer.writerows(table)
    lines = ["# 批量测试进度", "", f"完成 {len(rows)}/{len(tasks)} 题；本次进程用时 {summary['elapsed_seconds']:.1f} 秒。", "",
             "| 题号 | 编译 | 固定用例 通过/执行/计划 | 形式检查 | 总状态 |", "|---|---|---|---|---|"]
    for r in rows:
        f = r["functional"]
        comp = "PASS" if r["compiled"] else "NOT_RUN/FAIL"
        lines.append(f"| {r['task_id']} | {comp} | {f.get('passed_cases', 0)}/{f.get('evaluated_cases', 0)}/{r['planned_cases']} | {r['verification']['status']} | {r['status']} |")
    lines += ["", "PARTIAL/UNSUPPORTED_ST 不等同于程序错误；形式检查 PASS 也须核对完整规约覆盖与建模语义。",
              "compile.json / functional.json / formal.json 标注 cached、mode、输入指纹和证据；轨迹回放不算本次重新仿真。",
              "模型调用统计为本输出目录中新生成记录的累计值；断点续跑不会把旧调用当成本次新调用。"]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tasks", default="pilot", help="pilot/all/public/self or comma-separated IDs")
    p.add_argument("--source-dir", default=str(ROOT / "results/raw/six_task_fullflow_20261114"))
    p.add_argument("--out-dir", help="Use the same directory to resume; default is timestamped")
    p.add_argument("--config")
    p.add_argument("--model", default=MODEL)
    p.add_argument("--driver", choices=("star", "codex_cli"), default="star")
    p.add_argument("--condition", help="Experiment label; default E3 for STAR, E1 for Codex")
    p.add_argument("--workers", type=int, default=2, help="Concurrent task processes; IDE remains serial")
    p.add_argument("--stages", nargs="+", choices=STAGES, default=list(STAGES))
    p.add_argument("--formal-timeout", type=int, default=60)
    p.add_argument("--reuse-traces", action="store_true", help="Re-evaluate saved real traces; no new simulation")
    p.add_argument("--recompile", action="store_true", help="Do not reuse generation compilation evidence")
    p.add_argument("--retry-infra", action="store_true", help="Retry saved infrastructure outcomes, preserving attempts")
    p.add_argument("--keep-going", action="store_true", help="Keep dispatching after infrastructure failures")
    p.add_argument("--generate-missing", action="store_true")
    p.add_argument("--allow-model-api", action="store_true", help="Records prior explicit owner approval; not approval itself")
    p.add_argument("--dry-run", action="store_true", help="Only display/save execution plan")
    args = p.parse_args(argv)
    args.condition = args.condition or ("E3" if args.driver == "star" else "E1")
    if not 1 <= args.workers <= 8 or args.formal_timeout < 1:
        p.error("workers must be 1..8 and formal-timeout positive")
    if args.generate_missing and not args.allow_model_api:
        p.error("--generate-missing requires prior owner approval and --allow-model-api")
    if len(set(args.stages)) != len(args.stages):
        p.error("Duplicate stages")
    tasks = select_tasks(load_tasks(), args.tasks)
    errors = validate(tasks)["errors"]
    if errors:
        raise ValueError("Dataset invalid: " + "; ".join(errors[:5]))
    cfg = Settings.load(args.config, load_api=False)
    settings = {k: v for k, v in asdict(cfg).items() if k != "api_key"}
    out = Path(args.out_dir or ROOT / "results/raw" / time.strftime("batch_%Y%m%d_%H%M%S")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    options = {**vars(args), "out_dir": str(out), "source_dir": str(Path(args.source_dir).resolve()),
               "settings": settings, "stages": [s for s in STAGES if s in args.stages]}
    template = Path(cfg.codesys_template)
    binding = {"task_hashes": {t["id"]: digest(t) for t in tasks}, "code_sha256": code_fingerprint(),
               "model": args.model, "driver": args.driver, "condition": args.condition,
               "source_dir": options["source_dir"], "settings": settings,
               "stages": options["stages"], "reuse_traces": args.reuse_traces, "recompile": args.recompile,
               "formal_timeout": args.formal_timeout,
               "template_sha256": hashlib.sha256(template.read_bytes()).hexdigest() if template.is_file() else None}
    options["fingerprint"] = digest(binding)
    plan = {"created_utc": now(), "task_ids": [t["id"] for t in tasks], "workers": args.workers,
            "driver": args.driver, "model": args.model, "condition": args.condition,
            "codesys_concurrency": 1, "stages": options["stages"], "out_dir": str(out),
            "may_call_model": args.generate_missing, "reuse_traces": args.reuse_traces,
            "saved_record_available": {t["id"]: bool(find_record(out, t["id"]) or find_record(options["source_dir"], t["id"])) for t in tasks}}
    print(f"Batch: {len(tasks)} tasks, {args.workers} task workers, CODESYS serial; output: {out}", flush=True)
    with compiler_lock(timeout=1, path=out / ".batch.lock"):
        if args.dry_run:
            write_json(out / "plan.json", plan)
            print(plan, flush=True)
            return 0
        manifest = out / "manifest.json"
        if manifest.exists() and read_json(manifest).get("fingerprint") != options["fingerprint"]:
            raise ValueError("Task/code/config changed; use a new --out-dir to preserve evidence")
        if not manifest.exists():
            write_json(manifest, {"fingerprint": options["fingerprint"], "binding": binding, "plan": plan})
        write_json(out / "plan.json", plan)
        results, stopped, started = {}, False, time.monotonic()
        invocation_id = time.strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:8]
        pending = iter(tasks)
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn")) as pool:
            active = {}

            def dispatch():
                nonlocal stopped
                if (out / "STOP").exists():
                    stopped = True
                while not stopped and len(active) < args.workers:
                    task = next(pending, None)
                    if task is None:
                        break
                    active[pool.submit(run_task, {"task": task, "options": options})] = task["id"]
                    print(task["id"] + ": queued", flush=True)

            dispatch()
            save_summary(out, tasks, results, started, stopped, invocation_id)
            while active:
                finished, _ = wait(active, timeout=1, return_when=FIRST_COMPLETED)
                for future in finished:
                    tid = active.pop(future)
                    try:
                        row = future.result()
                    except Exception as exc:
                        task = next(t for t in tasks if t["id"] == tid)
                        row = {"task_id": tid, "difficulty": task["difficulty"], "status": "TOOL_ERROR",
                               "reason": redact("Worker process failed: " + str(exc)), "compiled": None,
                               "functional": {"status": "NOT_RUN"}, "verification": {"status": "NOT_RUN"},
                               "planned_cases": len(task["tests"]), "elapsed_seconds": 0}
                        write_json(out / tid / "worker_error.json", row)
                    results[tid] = row
                    print(f"{tid}: {row['status']}; fixed={row['functional']['status']}, formal={row['verification']['status']}, {row['elapsed_seconds']:.1f}s", flush=True)
                    with (out / "events.jsonl").open("a", encoding="utf-8") as stream:
                        import json
                        stream.write(json.dumps({"utc": now(), "task_id": tid, "status": row["status"]}) + "\n")
                    if row["status"] in INFRA and not args.keep_going:
                        stopped = True
                    save_summary(out, tasks, results, started, stopped, invocation_id)
                dispatch()
        save_summary(out, tasks, results, started, stopped, invocation_id)
    return 2 if stopped or any(r["status"] in INFRA for r in results.values()) else int(any(r["status"] == "FAIL" for r in results.values()))


if __name__ == "__main__":
    raise SystemExit(main())
