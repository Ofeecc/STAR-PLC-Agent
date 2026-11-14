"""Recompile and simulate an existing candidate; never requests model inference."""

from __future__ import annotations

import argparse
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from plc_agent.cli import require_compiler_preflight
from plc_agent.common import digest, now, read_json, write_json
from plc_agent.compiler import compile_st, normalize_candidate
from plc_agent.config import Settings
from plc_agent.dataset import load_tasks
from plc_agent.simulation import run_functional


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--task", default="SELF001")
    args = parser.parse_args()
    cfg = Settings.load(ROOT / "configs/runtime.local.json", load_api=False)
    require_compiler_preflight(cfg)
    task = next(t for t in load_tasks() if t["id"] == args.task)
    candidate = normalize_candidate(read_json(args.candidate))
    work = ROOT / "results/raw" / ("local_existing_" + args.task + "_" + now().replace(":", "").replace(".", ""))
    work.mkdir(parents=True)
    report = {
        "purpose": "LOCAL_ENVIRONMENT_ACCEPTANCE_ONLY",
        "task": args.task,
        "candidate_origin": str(args.candidate.resolve()),
        "source_sha256": digest(candidate),
        "observed_utc": now(),
        "model_inference": False,
    }
    compiled = compile_st(task, candidate, work / "compile", cfg)
    report["compile"] = asdict(compiled)
    if compiled.success:
        report["simulation"] = run_functional(task, candidate, digest(candidate), work / "simulation", cfg)
    report["verified"] = bool(
        compiled.success
        and report.get("simulation", {}).get("status") == "PASS"
        and report.get("simulation", {}).get("execution_verified")
    )
    write_json(work / "acceptance.json", report)
    write_json(ROOT / "results/summary/local_acceptance.json", report)
    print("ACCEPTANCE:", "PASS" if report["verified"] else "FAIL")
    print("Evidence:", work / "acceptance.json")
    return 0 if report["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
