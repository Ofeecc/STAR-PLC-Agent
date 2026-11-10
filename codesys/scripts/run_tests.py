# -*- coding: utf-8 -*-
"""Execute fixed scan tests on generated ST inside verified IDE simulation only."""
from __future__ import print_function
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

def text(value):
    if isinstance(value, text_type):
        return value
    if isinstance(value, binary_type):
        for encoding in ("utf-8", "mbcs", "cp1252", "latin-1"):
            try:
                return value.decode(encoding)
            except (UnicodeError, LookupError):
                pass
    return text_type(value)

def safe(value):
    if isinstance(value, dict):
        return dict((text(k), safe(v)) for k, v in value.items())
    if isinstance(value, (tuple, list)):
        return [safe(v) for v in value]
    if isinstance(value, (binary_type, text_type)):
        return text(value)
    return value

def replace(document, value):
    document.replace(new_text=value)
    if document.text.replace("\r\n", "\n").strip() != value.replace("\r\n", "\n").strip():
        raise RuntimeError("Generated source was not preserved in editor buffer")

def parse(raw, type_name):
    value = text(raw).strip().replace("_", "")
    typ = type_name.upper()
    if typ == "BOOL":
        if value.upper() in ("TRUE", "BOOL#TRUE"):
            return True
        if value.upper() in ("FALSE", "BOOL#FALSE"):
            return False
        raise RuntimeError("Unexpected BOOL representation: " + value)
    if typ.startswith("STRING("):
        value = text(raw)
        if len(value) >= 2 and value[0] == "'" and value[-1] == "'":
            value = value[1:-1]
        return value.replace("$N", "\n").replace("$R", "\r").replace("$'", "'").replace("$$", "$")
    if "#" in value:
        prefix, rest = value.split("#", 1)
        if prefix.upper() == typ:
            value = rest
    if typ in ("REAL", "LREAL"):
        return float(value)
    for marker, base in (("16#", 16), ("8#", 8), ("2#", 2)):
        if value.upper().startswith(marker):
            return int(value[len(marker):], base)
    return int(value)

def require_sim():
    if device is None or not device.get_simulation_mode():
        raise RuntimeError("Refusing online operation outside IDE simulation")

def stop_if_running():
    require_sim()
    state = con.application_state
    if state == ApplicationState.run:
        con.stop()
    elif state != ApplicationState.stop:
        raise RuntimeError("Unexpected simulator state: " + text(state))

def read_controls():
    raw = con.read_values(("PLC_PRG.BenchStep", "PLC_PRG.BenchCalls", "PLC_PRG.BenchDone"))
    return parse(raw[0], "UDINT"), parse(raw[1], "UDINT"), parse(raw[2], "BOOL")

def wait_controls(expected_step, expected_calls, expected_done, timeout):
    deadline = time.time() + timeout
    while time.time() < deadline:
        current = read_controls()
        if current == (expected_step, expected_calls, expected_done):
            return current
        system.delay(20)
    raise RuntimeError("Timed out waiting for simulator sequencer: " + str(current))

request = json.load(io.open(os.environ["PLC_CODESYS_TEST_REQUEST"], encoding="utf-8"))
result = {"backend": "CODESYS_SIMULATION", "request_id": request.get("request_id"),
          "source_sha256": request.get("source_sha256"), "status": "TOOL_ERROR", "actual_simulation": False,
          "execution_verified": False, "physical_connection_allowed": False,
          "observations": [], "raw_monitoring": {}, "compiler_diagnostics": [], "cleanup_errors": [],
          "infrastructure_error": None}
project = None
device = None
con = None
started = time.time()
try:
    if request.get("mode") != "IDE_SIMULATION_ONLY" or request.get("no_physical_connection") is not True:
        raise RuntimeError("Missing explicit simulation-only control")
    workspace = os.path.normcase(os.path.abspath(request["workspace"]))
    for name in ("project", "result_path"):
        if os.path.dirname(os.path.normcase(os.path.abspath(request[name]))) != workspace:
            raise RuntimeError("Simulation artifacts must stay in request workspace")
    if os.path.normcase(os.path.abspath(request["project"])) == os.path.normcase(os.path.abspath(request["template"])):
        raise RuntimeError("Refusing to modify frozen template")
    project = projects.open(request["project"], primary=True)
    apps = [o for o in project.get_children(True) if getattr(o, "is_application", False)]
    devices = [o for o in project.get_children(True) if getattr(o, "is_device", False)]
    if len(apps) != 1 or len(devices) != 1:
        raise RuntimeError("Expected one target/application")
    app, device = apps[0], devices[0]
    device.set_simulation_mode(True)
    require_sim()
    project.active_application = app
    candidate = request["candidate"]
    for obj in candidate.get("supporting_objects", []):
        if obj["name"] in ("FB_Task", "PLC_PRG"):
            raise RuntimeError("Reserved helper object name")
        for existing in app.find(obj["name"], True):
            existing.remove()
        if obj.get("kind") == "DUT":
            new = app.create_dut(name=obj["name"], type=DutType.Structure)
        else:
            kind = {"FUNCTION": PouType.Function, "PROGRAM": PouType.Program, "FUNCTION_BLOCK": PouType.FunctionBlock}[obj.get("kind", "FUNCTION_BLOCK")]
            kwargs = {"name": obj["name"], "type": kind}
            if kind == PouType.Function:
                kwargs["return_type"] = obj["return_type"]
            new = app.create_pou(**kwargs)
        replace(new.textual_declaration, obj["declaration"])
        if obj.get("implementation"):
            replace(new.textual_implementation, obj["implementation"])
    for old in app.find("FB_Task", True):
        old.remove()
    fb = app.create_pou(name="FB_Task", type=PouType.FunctionBlock)
    replace(fb.textual_declaration, candidate["declaration"])
    replace(fb.textual_implementation, candidate["implementation"])
    programs = [o for o in app.find("PLC_PRG", True) if getattr(o, "has_textual_declaration", False) and getattr(o, "has_textual_implementation", False)]
    if len(programs) != 1:
        raise RuntimeError("Expected task-called PLC_PRG")
    plan = request["program"]
    replace(programs[0].textual_declaration, plan["declaration"])
    replace(programs[0].textual_implementation, plan["implementation"])
    project.save()
    app.clean()
    for category in system.get_message_categories():
        system.clear_messages(category)
    app.rebuild()
    errors = 0
    for category in system.get_message_categories():
        errors += len(system.get_message_objects(category, Severity.Error))
        errors += len(system.get_message_objects(category, Severity.FatalError))
        for message in system.get_message_objects(category):
            result["compiler_diagnostics"].append({"severity": text(message.severity), "text": text(message.text)})
    result["compiler_error_count"] = int(errors)
    if errors:
        raise RuntimeError("Functional test wrapper did not compile; original candidate compilation record remains separate")
    result["compiled_pou_crc"] = text(fb.get_signature_crc(application=app))
    con = online.create_online_application(app)
    require_sim()
    con.login(OnlineChangeOption.Never, False)
    if not con.is_logged_in:
        raise RuntimeError("Simulation login failed")
    stop_if_running()
    con.reset(ResetOption.Cold)
    stop_if_running()
    result["initial_controls"] = wait_controls(0, 0, False, 5.0)
    result["actual_simulation"] = True
    require_sim()
    con.start()
    count = plan["step_count"]
    result["final_controls"] = wait_controls(count, count, True, max(30.0, count * 0.2))
    stop_if_running()
    expressions = []
    for index in range(count):
        expressions += ["PLC_PRG.TraceIn%d[%d]" % (i, index) for i in range(len(plan["inputs"]))]
        expressions += ["PLC_PRG.TraceOut%d[%d]" % (i, index) for i in range(len(plan["outputs"]))]
    raw = []
    for offset in range(0, len(expressions), 64):
        batch = expressions[offset:offset + 64]
        values = con.read_values(tuple(batch))
        if len(values) != len(batch):
            raise RuntimeError("Incomplete simulator monitoring response")
        raw += [text(v) for v in values]
    result["raw_monitoring"] = dict(zip(expressions, raw))
    position = 0
    for index in range(count):
        row = {"index": index, "inputs": {}, "outputs": {}}
        for field in plan["inputs"]:
            row["inputs"][field["name"]] = parse(raw[position], field["type"])
            position += 1
        for field in plan["outputs"]:
            row["outputs"][field["name"]] = parse(raw[position], field["type"])
            position += 1
        result["observations"].append(row)
    result["execution_verified"] = True
    result["status"] = "PASS"
    project.save()
except Exception:
    result["infrastructure_error"] = traceback.format_exc()
finally:
    if con is not None:
        try:
            require_sim()
            if con.is_logged_in:
                try:
                    stop_if_running()
                finally:
                    con.logout()
        except Exception:
            result["cleanup_errors"].append(traceback.format_exc())
        try:
            con.Dispose()
        except Exception:
            result["cleanup_errors"].append(traceback.format_exc())
    if project is not None:
        try:
            project.close()
        except Exception:
            result["cleanup_errors"].append(traceback.format_exc())
    if result["cleanup_errors"] and result["status"] == "PASS":
        result["status"] = "TOOL_ERROR"
        result["execution_verified"] = False
        result["infrastructure_error"] = "Simulation execution completed but cleanup failed"
    result["elapsed_seconds"] = time.time() - started
    with io.open(request["result_path"], "w", encoding="utf-8") as stream:
        stream.write(text(json.dumps(safe(result), ensure_ascii=False, indent=2)))
    print("Real IDE simulation evidence written: " + request["result_path"])
