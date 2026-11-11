# -*- coding: utf-8 -*-
"""Experimental IDE-simulation-only BOOL fixture.

Executed inside CODESYS, on a disposable copy created by run_simulation_probe.py.
No gateway scan, physical address, credentials, boot project, or source archive
download is used. Simulation mode is checked before every online operation.
This probes a request/acknowledgement gate, not an undocumented single_cycle API.
"""
from __future__ import print_function
import hashlib
import io
import json
import os
import re
import time
import traceback
from scriptengine import *

try:
    text_type = unicode
    binary_type = str
except NameError:
    text_type = str
    binary_type = bytes


def safe_text(value):
    if isinstance(value, text_type):
        return value
    if isinstance(value, binary_type):
        for encoding in ("utf-8", "mbcs", "cp1252", "latin-1"):
            try:
                return value.decode(encoding)
            except (UnicodeError, LookupError):
                pass
    return text_type(value)


def json_safe(value):
    if isinstance(value, dict):
        return {safe_text(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_safe(v) for v in value]
    if isinstance(value, (binary_type, text_type)):
        return safe_text(value)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return safe_text(value)


class ProbeTimeout(Exception):
    pass


def diagnostics():
    messages = []
    errors = 0
    for category in system.get_message_categories():
        errors += len(system.get_message_objects(category, Severity.Error))
        errors += len(system.get_message_objects(category, Severity.FatalError))
        for message in system.get_message_objects(category):
            messages.append({"severity": safe_text(message.severity), "text": safe_text(message.text)})
    return int(errors), messages


def replace_checked(document, value):
    document.replace(new_text=value)
    if document.text.replace("\r\n", "\n").strip() != value.replace("\r\n", "\n").strip():
        raise RuntimeError("Fixture text insertion was not preserved")


def boolean(value):
    value = safe_text(value).strip().upper()
    if value in ("TRUE", "BOOL#TRUE"):
        return True
    if value in ("FALSE", "BOOL#FALSE"):
        return False
    raise RuntimeError("Unexpected BOOL monitoring representation: " + value)


def unsigned(value):
    value = safe_text(value).strip().replace("_", "")
    if "#" in value and not value.startswith(("16#", "8#", "2#")):
        prefix, value = value.split("#", 1)
        if prefix.upper() not in ("UINT", "UDINT", "ULINT", "USINT"):
            raise RuntimeError("Unexpected counter type: " + prefix)
    for marker, base in (("16#", 16), ("8#", 8), ("2#", 2)):
        if value.startswith(marker):
            return int(value[len(marker):], base)
    if not re.match(r"^[0-9]+$", value):
        raise RuntimeError("Unexpected counter monitoring representation: " + value)
    return int(value)


def require_simulation(device):
    if not device.get_simulation_mode():
        raise RuntimeError("Refusing online operation: device is not in IDE simulation mode")


def ensure_stopped(online_app):
    require_simulation(device)
    state = online_app.application_state
    if state == ApplicationState.stop:
        return
    if state != ApplicationState.run:
        raise RuntimeError("Unexpected simulator state before stop: " + safe_text(state))
    online_app.stop()
    if online_app.application_state != ApplicationState.stop:
        raise RuntimeError("Simulator did not reach STOP state")


def ensure_running(online_app):
    require_simulation(device)
    state = online_app.application_state
    if state == ApplicationState.run:
        return
    if state != ApplicationState.stop:
        raise RuntimeError("Unexpected simulator state before start: " + safe_text(state))
    online_app.start()
    if online_app.application_state != ApplicationState.run:
        raise RuntimeError("Simulator did not reach RUN state")


def read_snapshot(online_app):
    expressions = ("PLC_PRG.TestInput", "PLC_PRG.TestOutput", "PLC_PRG.RequestSeq", "PLC_PRG.AckSeq", "PLC_PRG.CallCount")
    raw = online_app.read_values(expressions)
    if len(raw) != len(expressions):
        raise RuntimeError("Incomplete runtime monitoring response")
    return {"raw": dict(zip(expressions, [safe_text(v) for v in raw])),
            "input": boolean(raw[0]), "output": boolean(raw[1]),
            "request": unsigned(raw[2]), "ack": unsigned(raw[3]), "call_count": unsigned(raw[4])}


def wait_for_ack(online_app, sequence, timeout=5.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        snapshot = read_snapshot(online_app)
        if snapshot["ack"] == sequence:
            # Read once more after acknowledgement to avoid combining an old
            # output sample with a just-updated AckSeq in one monitoring batch.
            confirmed = read_snapshot(online_app)
            if confirmed["ack"] == sequence:
                return confirmed
        system.delay(20)
    raise ProbeTimeout("IDE simulation did not acknowledge sequence " + str(sequence))

def wait_for_input(online_app, expected, timeout=5.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        actual = boolean(online_app.read_value("PLC_PRG.TestInput"))
        if actual == expected:
            return actual
        # Monitoring values can be cached until the next refresh; a successful
        # write must be confirmed rather than assumed to be immediately visible.
        system.delay(20)
    raise ProbeTimeout("Prepared input write did not become visible")


request = json.load(io.open(os.environ["PLC_CODESYS_SIMULATION_REQUEST"], encoding="utf-8"))
result = {"kind": "IDE_SIMULATION_BOOL_SMOKE", "request_id": request.get("request_id"),
          "status": "NOT_RUN", "actual_simulation": False, "execution_verified": False,
          "benchmark_result": False, "physical_connection_allowed": False,
          "scan_control": "PLC_PRG sequence request/ack gate; exactly one FB invocation per acknowledged request",
          "single_cycle_api_used": False, "steps": [], "compiler_diagnostics": [],
          "cleanup_errors": [], "infrastructure_error": None}
project = None
online_app = None
device = None
started = time.time()

fb_declaration = "FUNCTION_BLOCK FB_Task\nVAR_INPUT\n x : BOOL;\nEND_VAR\nVAR_OUTPUT\n y : BOOL;\nEND_VAR"
fb_implementation = "y := x;"
program_declaration = """PROGRAM PLC_PRG
VAR
 uut : FB_Task;
 TestInput : BOOL := FALSE;
 TestOutput : BOOL := FALSE;
 RequestSeq : UDINT := 0;
 AckSeq : UDINT := 0;
 CallCount : UDINT := 0;
END_VAR"""
program_implementation = """IF RequestSeq <> AckSeq THEN
 uut(x := TestInput);
 TestOutput := uut.y;
 CallCount := CallCount + 1;
 AckSeq := RequestSeq;
END_IF;"""
fixture_text = (fb_declaration + "\n" + fb_implementation + "\nEND_FUNCTION_BLOCK\n\n"
                + program_declaration + "\n" + program_implementation + "\nEND_PROGRAM\n")
result["fixture_sha256"] = hashlib.sha256(fixture_text.encode("utf-8")).hexdigest()

try:
    if request.get("mode") != "IDE_SIMULATION_ONLY" or request.get("no_physical_connection") is not True:
        raise RuntimeError("Missing explicit IDE-simulation-only request")
    workspace = os.path.normcase(os.path.abspath(request["workspace"]))
    project_path = os.path.normcase(os.path.abspath(request["project"]))
    output_path = os.path.normcase(os.path.abspath(request["result_path"]))
    if os.path.dirname(project_path) != workspace or os.path.basename(project_path) != "simulation.project":
        raise RuntimeError("Fixture must use the disposable simulation.project in the request workspace")
    if os.path.dirname(output_path) != workspace:
        raise RuntimeError("Result file must stay in the request workspace")
    if project_path == os.path.normcase(os.path.abspath(request["template"])):
        raise RuntimeError("Refusing to modify the frozen compiler template")
    project = projects.open(request["project"], primary=True)
    apps = [obj for obj in project.get_children(True) if getattr(obj, "is_application", False)]
    devices = [obj for obj in project.get_children(True) if getattr(obj, "is_device", False)]
    if len(apps) != 1 or len(devices) != 1:
        raise RuntimeError("Fixture requires exactly one device and application")
    app, device = apps[0], devices[0]
    device.set_simulation_mode(True)
    require_simulation(device)
    project.active_application = app
    for obj in app.find("FB_Task", True):
        obj.remove()
    fb = app.create_pou(name="FB_Task", type=PouType.FunctionBlock)
    replace_checked(fb.textual_declaration, fb_declaration)
    replace_checked(fb.textual_implementation, fb_implementation)
    programs = [obj for obj in app.find("PLC_PRG", True)
                if getattr(obj, "has_textual_declaration", False) and getattr(obj, "has_textual_implementation", False)]
    if len(programs) != 1:
        raise RuntimeError("Template must contain exactly one task-called PLC_PRG")
    replace_checked(programs[0].textual_declaration, program_declaration)
    replace_checked(programs[0].textual_implementation, program_implementation)
    project.save()
    with io.open(os.path.join(request["workspace"], "fixture.st"), "w", encoding="utf-8") as stream:
        stream.write(safe_text(fixture_text))
    app.clean()
    for category in system.get_message_categories():
        system.clear_messages(category)
    app.rebuild()
    error_count, result["compiler_diagnostics"] = diagnostics()
    result["compiler_error_count"] = error_count
    if error_count:
        raise RuntimeError("Known simulation fixture failed CODESYS compilation; inspect actual diagnostics")
    result["compiled_pou_crc"] = safe_text(fb.get_signature_crc(application=app))
    require_simulation(device)
    online_app = online.create_online_application(app)
    # Keep the installed API's documented default operation timeout. Its
    # integer unit is not stated consistently across published versions.
    # Never means full code download, but ONLY to the already verified simulator.
    # False explicitly refuses deletion of unrelated simulator applications.
    online_app.login(OnlineChangeOption.Never, False)
    if not online_app.is_logged_in:
        raise RuntimeError("IDE simulation login did not complete")
    require_simulation(device)
    result["state_after_login"] = safe_text(online_app.application_state)
    ensure_stopped(online_app)
    online_app.reset(ResetOption.Cold)
    ensure_stopped(online_app)
    initial = read_snapshot(online_app)
    result["initial_read"] = initial
    result["actual_simulation"] = True
    if initial["request"] != 0 or initial["ack"] != 0 or initial["call_count"] != 0:
        raise RuntimeError("Fixture reset did not produce fresh handshake state")
    # No FB call occurs while RequestSeq equals AckSeq, even though the task runs.
    require_simulation(device)
    ensure_running(online_app)
    plan = [False, True, True, False]
    for sequence, input_value in enumerate(plan, 1):
        require_simulation(device)
        # Two-phase host write: confirm input storage before exposing a new request.
        online_app.set_prepared_value("PLC_PRG.TestInput", "TRUE" if input_value else "FALSE")
        online_app.write_prepared_values()
        actual_input = wait_for_input(online_app, input_value)
        if actual_input != input_value:
            raise RuntimeError("Prepared input write was not observed")
        online_app.set_prepared_value("PLC_PRG.RequestSeq", str(sequence))
        online_app.write_prepared_values()
        snapshot = wait_for_ack(online_app, sequence)
        passed = snapshot["input"] == input_value and snapshot["output"] == input_value and snapshot["call_count"] == sequence
        result["steps"].append({"sequence": sequence, "input": input_value, "expected_output": input_value,
                                "actual": snapshot, "passed": passed})
        if not passed:
            result["status"] = "TEST_FAIL"
            break
    if len(result["steps"]) == len(plan) and all(step["passed"] for step in result["steps"]):
        result["execution_verified"] = True
        result["status"] = "PASS"
except ProbeTimeout:
    result["status"] = "TIMEOUT"
    result["infrastructure_error"] = traceback.format_exc()
except Exception:
    result["status"] = "TOOL_ERROR"
    result["infrastructure_error"] = traceback.format_exc()
finally:
    if online_app is not None:
        try:
            require_simulation(device)
            if online_app.is_logged_in:
                try:
                    ensure_stopped(online_app)
                finally:
                    online_app.logout()
        except Exception:
            result["cleanup_errors"].append(traceback.format_exc())
        try:
            online_app.Dispose()
        except Exception:
            result["cleanup_errors"].append(traceback.format_exc())
    if project is not None:
        try:
            project.close()
        except Exception:
            result["cleanup_errors"].append(traceback.format_exc())
    if result["cleanup_errors"] and result["status"] == "PASS":
        result["status"] = "TOOL_ERROR"
        result["infrastructure_error"] = "Simulation smoke passed but resource cleanup failed"
    result["elapsed_seconds"] = time.time() - started
    with io.open(request["result_path"], "w", encoding="utf-8") as stream:
        stream.write(safe_text(json.dumps(json_safe(result), ensure_ascii=False, indent=2)))
    print("IDE simulation smoke evidence written: " + request["result_path"])
