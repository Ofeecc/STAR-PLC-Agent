"""Queue four isolated experiment groups, retaining finished pilot work."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from plc_agent.batch import PILOT
from plc_agent.common import ROOT, digest, now, read_json, write_json
from plc_agent.compiler import compiler_lock
from plc_agent.dataset import load_tasks


def snapshot_runner(out):
    sources = sorted((ROOT / "src/plc_agent").glob("*.py"))
    revision = digest({p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources})[:12]
    entry = out / f"run_matrix_{revision}.py"
    if entry.exists():
        return entry
    snapshot_name = f"matrix_runner_{revision}"
    target = out / snapshot_name / "src/plc_agent"
    target.mkdir(parents=True, exist_ok=True)
    for source in (ROOT / "src/plc_agent").glob("*.py"):
        shutil.copy2(source, target / source.name)
    common = target / "common.py"
    common.write_text(common.read_text(encoding="utf-8").replace(
        "ROOT = Path(__file__).resolve().parents[2]", "ROOT = Path(" + repr(str(ROOT)) + ")"), encoding="utf-8")
    batch = target / "batch.py"
    batch.write_text(batch.read_text(encoding="utf-8").replace(
        '(ROOT / "src/plc_agent").glob("*.py")', 'Path(__file__).resolve().parent.glob("*.py")'), encoding="utf-8")
    entry.write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parent/" +
                     repr(snapshot_name + "/src") + "))\nfrom plc_agent.batch import main\nif __name__ == '__main__':\n    raise SystemExit(main())\n", encoding="utf-8")
    write_json(out / snapshot_name / "snapshot_manifest.json", {
        "revision": revision, "created_utc": now(), "source_files": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}})
    return entry


def busy(out):
    try:
        with compiler_lock(timeout=0.05, path=out / ".batch.lock"):
            return False
    except TimeoutError:
        return True


def costs(out):
    total, reported, unknown = Decimal(0), 0, 0
    # Count upstream terminal files once, never sum duplicated aggregate usages.
    sources = list(out.glob("*/**/response.json"))
    sources += list((ROOT / "results/raw/six_task_fullflow_20261114").glob("*/generation/llm_*/response.json"))
    for path in set(sources):
        try:
            usage = read_json(path).get("usage") or {}
            if usage.get("cost") is None:
                unknown += 1
            else:
                amount = Decimal(str(usage["cost"]).replace("¥", "").replace("￥", "").strip())
                if not amount.is_finite() or amount < 0:
                    raise ValueError("Invalid reported amount")
                total += amount
                reported += 1
        except (OSError, ValueError, InvalidOperation):
            unknown += 1
    return {"reported_cny": str(total), "reported_requests": reported, "unknown_cost_requests": unknown,
            "not_account_balance": True, "includes_initial_six_pilot": True}


def group_rows(out, group, task_by_id):
    rows = []
    group_id = group["id"]
    for tid, task in task_by_id.items():
        path = out / group.get("directory", group_id) / tid / "fullflow_result.json"
        imported = group_id == "star_deepseek" and tid in PILOT
        if imported:
            path = ROOT / "results/raw/batch_fresh_20261114" / tid / "fullflow_result.json"
        if tid in group.get("retained_results", {}):
            path = ROOT / group["retained_results"][tid]
            imported = True
        if not path.exists():
            continue
        row = read_json(path)
        if imported:
            record = read_json(row["generation_record"])
            if record.get("task_sha256") != digest(task):
                raise ValueError("Imported pilot task changed: " + tid)
        rows.append(dict(row, matrix_evidence=str(path), imported_completed_pilot=imported))
    return rows


def report(out, config, state):
    tasks = {t["id"]: t for t in load_tasks()}
    groups = []
    for group in config["groups"]:
        rows = group_rows(out, group, tasks)
        groups.append({**group, "planned_tasks": len(tasks), "completed_tasks": len(rows),
                       "planned_fixed_cases": sum(len(t["tests"]) for t in tasks.values()),
                       "compiled_tasks": sum(r.get("compiled") is True for r in rows),
                       "fixed_passed_cases": sum(r["functional"].get("passed_cases", 0) for r in rows),
                       "fixed_evaluated_cases": sum(r["functional"].get("evaluated_cases", 0) for r in rows),
                       "formal_status_counts": dict(Counter(r["verification"]["status"] for r in rows)),
                       "outcome_counts": dict(Counter(r["status"] for r in rows)), "results": rows})
    summary = {"updated_utc": now(), "state": state, "cost": costs(out), "groups": groups}
    write_json(out / "matrix_summary.json", summary)
    lines = ["# 四组完整流程评测", "", f"更新：{summary['updated_utc']}；状态：{state}", "",
             "| 组别 | 框架 | 模型 | 已记录/计划 | 编译通过 | 固定用例通过/有效执行/全量计划 | 形式结果 |",
             "|---|---|---|---|---|---|---|"]
    for g in groups:
        lines.append(f"| {g['id']} | {g['driver']} | {g['model']} | {g['completed_tasks']}/{g['planned_tasks']} | {g['compiled_tasks']} | {g['fixed_passed_cases']}/{g['fixed_evaluated_cases']}/{g['planned_fixed_cases']} | {g['formal_status_counts']} |")
    lines += ["", "STAR＋DeepSeek 的六题采用已经完成的候选与真实评测，明确列明 imported_completed_pilot；其余题目独立生成。",
              "PARTIAL / UNSUPPORTED_ST / 未执行不等于程序错误或形式证明通过。",
              "有效执行仅计时序符合原定条件的用例；TIMING_NOT_REPRODUCED 与超长时间未执行用例保留在全量计划分母，不计通过。",
              f"接口返回费用累计：{summary['cost']['reported_cny']} 元（含最初六题；不是账户余额；缺失费用字段的请求数 {summary['cost']['unknown_cost_requests']}）。"]
    (out / "matrix_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summary


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out-dir", default=str(ROOT / "results/raw/four_group_20261114"))
    p.add_argument("--config", default=str(ROOT / "configs/fullflow_matrix.json"))
    p.add_argument("--allow-model-api", action="store_true")
    p.add_argument("--run", action="store_true")
    p.add_argument("--only", help="Comma-separated group IDs; default all")
    args = p.parse_args()
    if args.run and not args.allow_model_api:
        p.error("Execution needs prior explicit owner approval and --allow-model-api")
    out = Path(args.out_dir).resolve(); out.mkdir(parents=True, exist_ok=True)
    config = read_json(args.config)
    task_ids = [t["id"] for t in load_tasks()]
    selected = args.only.split(",") if args.only else [g["id"] for g in config["groups"]]
    if set(selected) - {g["id"] for g in config["groups"]}:
        p.error("Unknown group IDs")
    manifest = {"created_utc": now(), "configuration": config, "selected_groups": selected,
                "planned_tasks_per_group": task_ids, "pilot_imports": list(PILOT),
                "authorization": "User active goal explicitly requests verified full runs and four groups; see authorization.txt"}
    write_json(out / "matrix_plan.json", manifest)
    report(out, config, "PLANNED")
    if not args.run:
        print(json.dumps(manifest, ensure_ascii=False, indent=2)); return 0
    entry = snapshot_runner(out)
    with compiler_lock(timeout=1, path=out / ".matrix.lock"):
        for group in config["groups"]:
            gid = group["id"]
            if gid not in selected:
                continue
            group_out = out / group.get("directory", gid)
            group_out.mkdir(parents=True, exist_ok=True)
            launched, process, handle = False, None, None
            while True:
                snapshot = report(out, config, "RUNNING " + gid)
                if (out / "STOP").exists() or Decimal(snapshot["cost"]["reported_cny"]) >= Decimal(str(config["reported_cost_stop_cny"])):
                    (group_out / "STOP").touch()
                    report(out, config, "STOP_REQUESTED_BUDGET_OR_OPERATOR")
                    return 2
                row = next(g for g in snapshot["groups"] if g["id"] == gid)
                if not busy(group_out):
                    # Every task having a durable row means this group has been
                    # attempted. Preserve stage errors in the report, but do not
                    # let one unsupported task prevent the remaining tasks/groups.
                    if row["completed_tasks"] == len(task_ids) and not row["outcome_counts"].get("STOPPED", 0):
                        break
                    if launched:
                        if handle: handle.close()
                        report(out, config, "BLOCKED " + gid)
                        return 2
                    retained = set(group.get("retained_results", {}))
                    if gid == "star_deepseek":
                        retained.update(PILOT)
                    ordered = [t for t in list(PILOT) + [x for x in task_ids if x not in PILOT] if t not in retained]
                    command = [sys.executable, "-X", "utf8", "-u", str(entry), "--tasks", ",".join(ordered),
                               "--source-dir", str(ROOT / group["source_dir"]) if group.get("source_dir") else str(out / "empty_sources"),
                               "--driver", group["driver"], "--model", group["model"], "--condition", group["condition"]]
                    command += ["--out-dir", str(group_out), "--workers", str(config["workers_per_group"]),
                                "--generate-missing", "--allow-model-api", "--retry-infra", "--keep-going"]
                    write_json(group_out / "matrix_invocation.json", {"argv": command, "utc": now()})
                    handle = (out / (gid + "_matrix_console.log")).open("ab")
                    process = subprocess.Popen(command, cwd=ROOT, stdout=handle, stderr=subprocess.STDOUT,
                                               creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
                    launched = True
                    print(gid + ": launched", flush=True)
                    time.sleep(2)
                else:
                    if process is None and not launched:
                        print(gid + ": attached to running batch", flush=True)
                        launched = True
                time.sleep(10)
            if process:
                process.wait(timeout=30)
            if handle: handle.close()
            print(gid + ": complete", flush=True)
        final = report(out, config, "COMPLETE")
        if any(g["outcome_counts"].get(s, 0) for g in final["groups"]
               for s in ("TOOL_ERROR", "TIMEOUT", "UNVERIFIED", "MISSING_CANDIDATE", "STOPPED", "FAIL")):
            report(out, config, "COMPLETE_WITH_RECORDED_ERRORS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
