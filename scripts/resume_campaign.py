"""Resume only pending generation runs, then run fixed CODESYS simulation tests.

This orchestration wrapper changes no prompts, budgets, candidates, or task data.
It can run in a hidden Windows process while artifacts are prepared separately.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ["PYTHONPATH"] = str(ROOT / "src")
state_path = ROOT / "results/summary/resume_state.json"
state = {"started_utc": datetime.now(timezone.utc).isoformat(), "pid": os.getpid(), "stages": []}

def save():
    state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

for args in (("run", "--condition", "all"), ("test", "--condition", "all"), ("aggregate",)):
    state["current_stage"] = list(args)
    save()
    code = subprocess.call([sys.executable, "-X", "utf8", "-u", "-m", "plc_agent.cli", *args])
    state["stages"].append({"args": list(args), "exit_code": code, "ended_utc": datetime.now(timezone.utc).isoformat()})
    if code:
        state["failed"] = True
        break
state["finished_utc"] = datetime.now(timezone.utc).isoformat()
state["current_stage"] = None
save()
