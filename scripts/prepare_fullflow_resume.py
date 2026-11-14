"""Prepare a continuation config while retaining only completed STAR evidence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/raw/four_group_20261114"
source = json.loads((OUT / "matrix_summary.json").read_text(encoding="utf-8"))
config = json.loads((ROOT / "configs/fullflow_matrix.json").read_text(encoding="utf-8"))
star = next(g for g in config["groups"] if g["id"] == "star_deepseek")
star["directory"] = "star_deepseek_v4"
star["source_dir"] = "results/raw/four_group_20261114/star_deepseek_v3"
retained = {}
infra = {"TOOL_ERROR", "TIMEOUT", "UNVERIFIED", "MISSING_CANDIDATE", "STOPPED"}
pilot = {"PUB001", "PUB003", "PUB007", "PUB009", "PUB015", "PUB016"}
for row in source["groups"][0]["results"]:
    tid = row["task_id"]
    if tid in pilot or row["status"] in infra:
        continue
    evidence = Path(row["matrix_evidence"])
    retained[tid] = evidence.resolve().relative_to(ROOT).as_posix()
star["retained_results"] = retained
config["continuation_note"] = (
    "Continue all four confirmed groups. GPT-6.1-terra calls route through the configured teacher API key "
    "via the local Responses proxy; Codex CLI receives only a temporary local relay token, not a ChatGPT login. "
    "STAR DeepSeek retains completed tasks and retries PUB014 functional simulation in a fresh output directory."
)
path = OUT / "matrix_config_resume.json"
path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"config": str(path), "star_retained": sorted(retained), "groups": [g["id"] for g in config["groups"]]}, ensure_ascii=False))
