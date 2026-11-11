# -*- coding: utf-8 -*-
"""Read-only installation probe. Execute inside CODESYS Scripting.

Set PLC_CODESYS_PROBE to a new output JSON path. Optionally set
PLC_CODESYS_TEMPLATE to a saved standard project to inspect it without saving.
No project or device-repository changes are performed.
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

def text(value):
    if value is None:
        return None
    if isinstance(value, str) and not isinstance(value, text_type):
        return value.decode("utf-8", "replace")
    return text_type(value)

def json_safe(value):
    if isinstance(value, dict):
        return dict((text(k), json_safe(v)) for k, v in value.items())
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, str):
        return text(value)
    return value

def property_text(obj, name):
    try:
        return text(getattr(obj, name))
    except Exception:
        return None

def file_inventory(root, suffixes, max_depth=5):
    found = []
    if not os.path.isdir(root):
        return found
    root_depth = root.rstrip(os.sep).count(os.sep)
    for folder, dirs, files in os.walk(root):
        depth = folder.count(os.sep) - root_depth
        if depth >= max_depth:
            dirs[:] = []
        for name in files:
            if name.lower().endswith(suffixes):
                found.append(os.path.join(folder, name))
    return found

output_path = os.environ["PLC_CODESYS_PROBE"]
result = {"kind": "CODESYS_INSTALLATION_PROBE", "actual_compilation": False,
          "python_version": sys.version, "argv": list(sys.argv),
          "executable": property_text(system, "executable_filename"),
          "ui_present": bool(system.ui_present), "devices": [], "profile_files": [],
          "template_files": [], "project_objects": [], "errors": []}
project = None
try:
    from System.Diagnostics import FileVersionInfo
    info = FileVersionInfo.GetVersionInfo(system.executable_filename)
    result["executable_file_version"] = text(info.FileVersion)
    result["executable_product_version"] = text(info.ProductVersion)
except Exception:
    result["errors"].append("File version: " + traceback.format_exc())
try:
    from System import Environment
    # Restrict recorded command-line data to installation selection flags.
    args = [text(a) for a in Environment.GetCommandLineArgs()]
    result["launch_selection"] = [a for a in args if a.startswith(("--profile", "--additionalfolder", "--noUI"))]
except Exception:
    result["errors"].append("Launch flags: " + traceback.format_exc())
try:
    install_root = os.environ.get("PLC_CODESYS_INSTALL_ROOT")
    if not install_root:
        install_root = os.path.dirname(os.path.dirname(system.executable_filename))
    inventory = file_inventory(install_root, (".profile", ".project", ".template"))
    result["profile_files"] = [p for p in inventory if p.lower().endswith(".profile")]
    result["template_files"] = [p for p in inventory if p.lower().endswith((".project", ".template"))]
except Exception:
    result["errors"].append("Installation files: " + traceback.format_exc())
try:
    devices = device_repository.get_all_devices(name="", source=None)
    for device in devices:
        try:
            ident = device.device_id
            info = device.device_info
            result["devices"].append({"name": text(info.name), "vendor": text(info.vendor),
                                      "type": property_text(ident, "type"),
                                      "id": property_text(ident, "id"),
                                      "version": property_text(ident, "version"),
                                      "device_id_text": text(ident)})
        except Exception:
            result["errors"].append("Device record: " + traceback.format_exc())
except Exception:
    result["errors"].append("Device repository: " + traceback.format_exc())
try:
    template = os.environ.get("PLC_CODESYS_TEMPLATE")
    if template:
        # Inspect a separate project; do not save it or change its objects.
        project = projects.open(template)
        for obj in project.get_children(recursive=True):
            entry = {"name": obj.get_name(), "type_guid": text(obj.type),
                     "is_application": bool(getattr(obj, "is_application", False)),
                     "has_textual_declaration": bool(getattr(obj, "has_textual_declaration", False)),
                     "has_textual_implementation": bool(getattr(obj, "has_textual_implementation", False))}
            if getattr(obj, "is_device", False):
                entry["device_identification"] = text(obj.get_device_identification())
            result["project_objects"].append(entry)
except Exception:
    result["errors"].append("Template inspection: " + traceback.format_exc())
finally:
    if project is not None:
        project.close()
    folder = os.path.dirname(output_path)
    if folder and not os.path.isdir(folder):
        os.makedirs(folder)
    with io.open(output_path, "w", encoding="utf-8") as stream:
        stream.write(text_type(json.dumps(json_safe(result), ensure_ascii=False, indent=2)))
    print("CODESYS installation probe written: " + output_path)
