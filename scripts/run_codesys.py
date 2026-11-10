"""Run an in-IDE script with captured binary logs, using a real installed profile."""
import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from plc_agent.compiler import codesys_command

parser = argparse.ArgumentParser()
parser.add_argument("script")
parser.add_argument("--exe", default="D:/Codesys/CODESYS/Common/CODESYS.exe")
parser.add_argument("--profile", default="CODESYS V3.5 SP22 Patch 4")
parser.add_argument("--log", required=True)
parser.add_argument("--timeout", type=int, default=180)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
log = root / args.log
log.parent.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
env["PLC_CODESYS_TEMPLATE"] = str(root / "codesys/templates/benchmark.project")
env["PLC_CODESYS_PROBE"] = str(root / "results/raw/codesys_installation.json")
env["PLC_CODESYS_INSTALL_ROOT"] = "D:/Codesys/CODESYS"
command = [args.exe, "--profile=" + args.profile, "--runscript=" + str((root / args.script).resolve()), "--noUI", "--culture=en"]
with log.open("wb") as stream:
    proc = subprocess.run(codesys_command(command), cwd=root, env=env, stdout=stream, stderr=subprocess.STDOUT,
        timeout=args.timeout, creationflags=subprocess.CREATE_NO_WINDOW)
print("CODESYS exit:", proc.returncode)
print("Log:", log)
raise SystemExit(proc.returncode)
