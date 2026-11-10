# -*- coding: utf-8 -*-
"""Run INSIDE CODESYS Scripting (IronPython 2.7), never with Project1 Python.
Official API references are recorded in docs/codesys_setup.md.
"""
from __future__ import print_function
import io
import json
import os
import sys
import traceback
from scriptengine import *

try:
    text_type = unicode
except NameError:
    text_type = str

def write(path, data):
    def safe(value):
        if isinstance(value, dict):
            return dict((safe(k), safe(v)) for k, v in value.items())
        if isinstance(value, (list, tuple)):
            return [safe(v) for v in value]
        if isinstance(value, str) and not isinstance(value, text_type):
            return value.decode("utf-8", "replace")
        return value
    with io.open(path + ".tmp", "w", encoding="utf-8") as stream:
        stream.write(text_type(json.dumps(safe(data), ensure_ascii=False, indent=2)))
    os.rename(path + ".tmp", path)

def attr(obj, name):
    try:
        return text_type(getattr(obj, name))
    except Exception:
        return ""

def replace_checked(document, value):
    # ScriptTextDocument normalizes CR/CRLF to LF. Compare the actual editor
    # buffer so a failed insertion cannot compile an unrelated empty body.
    document.replace(new_text=value)
    expected = value.replace("\r\n", "\n").replace("\r", "\n").strip()
    actual = document.text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if actual != expected:
        raise RuntimeError("Text insertion verification failed")

request = json.load(io.open(os.environ["PLC_CODESYS_REQUEST"], encoding="utf-8"))
result = {"backend": "CODESYS", "request_id": request["request_id"],
          "source_sha256": request["source_sha256"], "finished": False,
          "rebuild_invoked": False, "error_count": None, "diagnostics": [],
          "compiled_pou_crc": None, "infrastructure_error": None}
project = None
try:
    if request["request_id"] not in sys.argv[1:]:
        raise RuntimeError("--scriptargs nonce missing; check this installed profile's CLI")
    project = projects.open(request["project"])
    apps = [o for o in project.get_children(True) if getattr(o, "is_application", False)]
    if len(apps) != 1:
        raise RuntimeError("Template must contain exactly one application")
    app = apps[0]
    candidate = request["candidate"]
    for obj in candidate.get("supporting_objects", []):
        name = obj["name"]
        if name in ("FB_Task", "PLC_PRG"):
            raise RuntimeError("Supporting object uses reserved name")
        for existing in app.find(name, True):
            existing.remove()
        if obj.get("kind") == "DUT":
            new = app.create_dut(name=name, type=DutType.Structure)
        else:
            kinds = {"FUNCTION": PouType.Function, "PROGRAM": PouType.Program, "FUNCTION_BLOCK": PouType.FunctionBlock}
            kind = kinds[obj.get("kind", "FUNCTION_BLOCK")]
            kwargs = {"name": name, "type": kind}
            if kind == PouType.Function:
                kwargs["return_type"] = obj["return_type"]
            new = app.create_pou(**kwargs)
        replace_checked(new.textual_declaration, obj["declaration"])
        if obj.get("implementation"):
            replace_checked(new.textual_implementation, obj["implementation"])
    for existing in app.find("FB_Task", True):
        existing.remove()
    pou = app.create_pou(name="FB_Task", type=PouType.FunctionBlock)
    replace_checked(pou.textual_declaration, candidate["declaration"])
    replace_checked(pou.textual_implementation, candidate["implementation"])
    if not pou.build_properties.link_always_is_valid:
        raise RuntimeError("Profile cannot force FB_Task compilation; configure a binding caller")
    pou.build_properties.link_always = True
    project.save()
    # Clean and clear ALL categories first. Fail closed if any API call fails.
    app.clean()
    for category in system.get_message_categories():
        system.clear_messages(category)
    app.rebuild()
    result["rebuild_invoked"] = True
    errors = 0
    for category in system.get_message_categories():
        # FatalError is a distinct flag and must also prevent success.
        errors += len(system.get_message_objects(category, Severity.Error))
        errors += len(system.get_message_objects(category, Severity.FatalError))
        for message in system.get_message_objects(category):
            result["diagnostics"].append({"category": str(category), "severity": attr(message, "severity"),
                                          "text": attr(message, "text"), "position": attr(message, "position_text")})
    result["error_count"] = int(errors)
    if errors == 0:
        crc = pou.get_signature_crc(application=app)
        if crc is None or not str(crc):
            raise RuntimeError("Compiler did not provide a signature for FB_Task")
        result["compiled_pou_crc"] = str(crc)
    project.save()
except Exception:
    result["infrastructure_error"] = traceback.format_exc()
finally:
    result["finished"] = True
    write(request["result_path"], result)
    if project is not None:
        project.close()
