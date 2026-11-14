"""Build a separate Codex retry config after the first matrix pass completes."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/raw/four_group_20261114"
config = json.loads((OUT / "matrix_config_resume.json").read_text(encoding="utf-8"))
for group in config["groups"]:
    if group["id"] == "codex_deepseek":
        group["directory"] = "codex_deepseek_v10"
    elif group["id"] == "codex_terra":
        group["directory"] = "codex_terra_v10"
config["continuation_note"] += (
    " Codex retries v2-v9 reached no trusted compiler calls; model connectivity requires host permission for the local "
    "relay and an approve mode on the already-authorized local MCP server. The v10 retry removes Codex-only input/total-token "
    "guards, isolates Codex state per task, restricts CLI network to localhost, captures output through pipes, and retains "
    "the shared per-call output ceiling, request count, timeout, and 75 CNY stop. Earlier evidence is preserved."
)
path = OUT / "matrix_config_codex_retry_v10.json"
path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(path)
