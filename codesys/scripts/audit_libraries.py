# -*- coding: utf-8 -*-
"""Inspect a disposable template copy; never remove installed libraries."""
from __future__ import print_function
import io
import json
import os
from scriptengine import *

request = json.load(io.open(os.environ['PLC_LIBRARY_AUDIT_REQUEST'], encoding='utf-8'))
result = {'references': [], 'objects': []}
project = projects.open(request['project'])
try:
    apps = [o for o in project.get_children(True) if getattr(o, 'is_application', False)]
    if len(apps) != 1:
        raise RuntimeError('Expected one application')
    manager = apps[0].get_library_manager()
    if request.get('qualify_device_diagnosis'):
        matched = [r for r in manager.references if r.name == '#CAA Device Diagnosis']
        if len(matched) != 1:
            raise RuntimeError('Expected one device diagnosis reference')
        matched[0].qualified_only = True
        project.save()
        result['qualification_change'] = {'library': matched[0].name, 'qualified_only': bool(matched[0].qualified_only)}
    def describe(ref, ancestors):
        row = {'name': str(ref.name), 'namespace': str(ref.namespace),
               'system_library': bool(ref.system_library), 'qualified_only': bool(ref.qualified_only)}
        if row['name'] not in ancestors:
            row['dependencies'] = [describe(d, ancestors + [row['name']]) for d in ref.get_dependencies()]
        return row
    result['references'] = [describe(ref, []) for ref in manager.references]
    for obj in project.get_children(True):
        row = {'name': obj.get_name()}
        if getattr(obj, 'has_textual_declaration', False):
            row['declaration'] = obj.textual_declaration.text
        if getattr(obj, 'has_textual_implementation', False):
            row['implementation'] = obj.textual_implementation.text
        result['objects'].append(row)
    with io.open(request['result_path'], 'w', encoding='utf-8') as stream:
        stream.write(unicode(json.dumps(result, ensure_ascii=False, indent=2)))
finally:
    project.close()
