# -*- coding: utf-8 -*-
"""Prepare ONLY a new workspace copy of the vendor standard template."""
from __future__ import print_function
import io
import json
import os
from scriptengine import *

path = os.environ["PLC_CODESYS_TEMPLATE"]
flags = VersionUpdateFlags.SilentMode | VersionUpdateFlags.UpdateAll
project = projects.open(path, primary=True, update_flags=flags)
try:
    target = [d for d in device_repository.get_all_devices() if d.device_info.name == "CODESYS Control Win V3 x64"]
    if len(target) != 1:
        raise RuntimeError("Expected exactly one installed Control Win V3 x64 device")
    devices = [o for o in project.get_children(True) if getattr(o, "is_device", False)]
    if len(devices) != 1:
        raise RuntimeError("Expected exactly one template device")
    devices[0].update(device=target[0].device_id)
    if hasattr(project, "set_compilerversion_to_newest"):
        project.set_compilerversion_to_newest()
    apps = [o for o in project.get_children(True) if getattr(o, "is_application", False)]
    if len(apps) != 1:
        raise RuntimeError("Expected exactly one application")
    app = apps[0]
    manager = app.get_library_manager()
    for reference in list(manager.references):
        print("Library reference: " + str(reference))
        print("Library reference fields: " + str([n for n in dir(reference) if not n.startswith('_')]))
    project.active_application = app
    project.save()
    print("Prepared target: " + str(target[0].device_id))
    if hasattr(project, "get_compilerversion"):
        print("Compiler version: " + str(project.get_compilerversion()))
    app.rebuild()
    for category in system.get_message_categories():
        for message in system.get_message_objects(category):
            print(str(message.severity) + ": " + message.text)
    print("Saved current benchmark template: " + path)
finally:
    project.close()
