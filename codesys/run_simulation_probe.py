"""Launch the optional, real CODESYS IDE simulation fixture on a fresh copy.

No LLM calls and no physical PLC connection. Does not modify the compiler
template. This must only be run after the real compiler backend preflight.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path

from plc_agent.common import ROOT, now, read_json, write_json
from plc_agent.compiler import _kill_tree, codesys_command
from plc_agent.config import Settings


def compiler_settings(path=None):
    # This operation does not load the API configuration or any API key.
    allowed = {"codesys_exe", "codesys_profile", "codesys_template", "additional_folder", "compiler_timeout"}
    data = read_json(path) if path else {}
    values = {key: value for key, value in data.items() if key in allowed}
    for env_name, key in (("PLC_CODESYS_EXE", "codesys_exe"), ("PLC_CODESYS_PROFILE", "codesys_profile"),
                          ("PLC_CODESYS_TEMPLATE", "codesys_template"), ("PLC_CODESYS_ADDITIONAL_FOLDER", "additional_folder")):
        if os.environ.get(env_name):
            values[key] = os.environ[env_name]
    return Settings(**values)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="Optional local compiler configuration JSON")
    parser.add_argument("--run-simulation", action="store_true", help="Explicitly run IDE simulation, never a physical PLC")
    args = parser.parse_args()
    if not args.run_simulation:
        parser.error("Pass --run-simulation explicitly after compiler validation")
    settings = compiler_settings(args.config)
    token = uuid.uuid4().hex
    folder = ROOT / "results/raw/simulation_probe" / token
    folder.mkdir(parents=True)
    result = {"kind": "IDE_SIMULATION_BOOL_SMOKE", "request_id": token, "started_utc": now(),
              "status": "NOT_RUN", "actual_simulation": False, "benchmark_result": False,
              "physical_connection_allowed": False, "paid_model_calls": 0}
    missing = settings.compiler_ready()
    if missing:
        result["reason"] = "Missing compiler configuration: " + ", ".join(missing)
        write_json(folder / "result.json", result)
        print(str(folder / "result.json"))
        return 2
    template = Path(settings.codesys_template).resolve()
    project = folder / "simulation.project"
    shutil.copy2(template, project)
    request = {"request_id": token, "mode": "IDE_SIMULATION_ONLY", "no_physical_connection": True,
               "workspace": str(folder), "template": str(template), "project": str(project),
               "result_path": str(folder / "simulation_evidence.json")}
    write_json(folder / "request.json", request)
    command = [settings.codesys_exe, "--profile=" + settings.codesys_profile,
               "--runscript=" + str(ROOT / "codesys/scripts/simulation_probe.py"), "--noUI"]
    if settings.additional_folder:
        command.append("--additionalfolder=" + settings.additional_folder)
    write_json(folder / "invocation.json", {"argv": command,
               "template_sha256": hashlib.sha256(template.read_bytes()).hexdigest(),
               "script_sha256": hashlib.sha256((ROOT / "codesys/scripts/simulation_probe.py").read_bytes()).hexdigest()})
    env = os.environ.copy()
    env["PLC_CODESYS_SIMULATION_REQUEST"] = str(folder / "request.json")
    for key in ("PLC_LLM_API_KEY", "OPENAI_API_KEY", "PLC_API_CONFIG"):
        env.pop(key, None)
    started = time.monotonic()
    try:
        lock_path = ROOT / ".local/compiler.lock"
        lock_path.parent.mkdir(exist_ok=True)
        with lock_path.open("a+b") as lock:
            if os.name == "nt":
                import msvcrt
                if lock.tell() == 0:
                    lock.write(b"0"); lock.flush()
                lock.seek(0)
                deadline = time.monotonic() + 900
                while True:
                    try:
                        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                        break
                    except OSError:
                        if time.monotonic() >= deadline:
                            raise TimeoutError("Waited 900 seconds for the shared CODESYS compiler lock")
                        time.sleep(0.25)
            with (folder / "stdout.log").open("wb") as stdout, (folder / "stderr.log").open("wb") as stderr:
                process = subprocess.Popen(codesys_command(command), env=env, stdout=stdout, stderr=stderr,
                                           creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
                try:
                    result["process_exit_code"] = process.wait(timeout=max(180, settings.compiler_timeout))
                except subprocess.TimeoutExpired:
                    _kill_tree(process)
                    result["status"], result["reason"] = "TIMEOUT", "IDE simulation process exceeded timeout"
            evidence_path = folder / "simulation_evidence.json"
            if result["status"] != "TIMEOUT":
                evidence = read_json(evidence_path)
                if evidence.get("request_id") != token or evidence.get("physical_connection_allowed") is not False:
                    raise ValueError("Unrelated or unsafe simulation evidence")
                result.update({key: evidence[key] for key in ("status", "actual_simulation", "execution_verified", "steps", "infrastructure_error") if key in evidence})
                result["evidence"] = str(evidence_path)
                if result["process_exit_code"] != 0:
                    result["status"], result["reason"] = "TOOL_ERROR", "CODESYS simulation process exited abnormally"
    except (OSError, ValueError, KeyError) as exc:
        result["status"], result["reason"] = "TOOL_ERROR", f"{type(exc).__name__}: {exc}"
    result["elapsed_seconds"] = time.monotonic() - started
    result["finished_utc"] = now()
    write_json(folder / "result.json", result)
    print(str(folder / "result.json"))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
