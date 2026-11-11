"""Read CODESYS template dependencies in a disposable project copy. No model API."""
import hashlib
import json
import os
import shutil
import subprocess
import uuid
import argparse
from dataclasses import replace, asdict
from pathlib import Path
from plc_agent.common import ROOT, write_json
from plc_agent.compiler import codesys_command, compiler_lock, compile_st
from plc_agent.config import Settings

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--probe-qualified', action='store_true')
    args = parser.parse_args()
    cfg = Settings.load(load_api=False)
    stamp = 'library_audit_' + uuid.uuid4().hex[:12]
    staging = cfg.get_ascii_work_root() / stamp
    staging.mkdir(parents=True)
    evidence = ROOT / 'results/raw' / stamp
    evidence.mkdir(parents=True)
    source = Path(cfg.codesys_template)
    original_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    shutil.copy2(source, staging / 'template.project')
    shutil.copy2(ROOT / 'codesys/scripts/audit_libraries.py', staging / 'audit.py')
    write_json(staging / 'request.json', {'project': str(staging / 'template.project'), 'result_path': str(staging / 'libraries.json'), 'qualify_device_diagnosis': args.probe_qualified})
    env = os.environ.copy()
    for key in ('PLC_LLM_API_KEY','OPENAI_API_KEY','PLC_API_CONFIG'):
        env.pop(key, None)
    env['PLC_LIBRARY_AUDIT_REQUEST'] = str(staging / 'request.json')
    command = [cfg.codesys_exe, '--profile=' + cfg.codesys_profile, '--runscript=' + str(staging / 'audit.py'), '--noUI', '--culture=en']
    with compiler_lock(cfg.compiler_timeout), (evidence / 'stdout.log').open('wb') as out, (evidence / 'stderr.log').open('wb') as err:
        subprocess.run(codesys_command(command), env=env, stdout=out, stderr=err, timeout=cfg.compiler_timeout,
                       creationflags=subprocess.CREATE_NO_WINDOW, check=True)
    shutil.copy2(staging / 'libraries.json', evidence / 'libraries.json')
    assert original_hash == hashlib.sha256(source.read_bytes()).hexdigest()
    write_json(evidence / 'audit_manifest.json', {'template_sha256': original_hash, 'original_template_unchanged': True})
    print(str(evidence), flush=True)
    data = json.loads((evidence / 'libraries.json').read_text(encoding='utf-8'))
    print(json.dumps({'top_level_references': [{k:r[k] for k in ('name','system_library','qualified_only')} for r in data['references']]}), flush=True)
    if args.probe_qualified:
        shutil.copy2(staging / 'template.project', evidence / 'qualified_candidate.project')
        candidate = json.loads((ROOT / 'results/raw/pilot_pair_2026-11-10T143217961073+0000/PUB003_star/version_00.json').read_text(encoding='utf-8'))
        outcome = compile_st({'id':'PUB003_LIBRARY_QUALIFICATION_PROBE'}, candidate, evidence / 'compile_retained', replace(cfg,codesys_template=str(staging / 'template.project')))
        write_json(evidence / 'qualification_probe.json', asdict(outcome))
        print(json.dumps({'probe_status':outcome.status, 'diagnostics':[d for d in outcome.diagnostics if d.get('code')]}), flush=True)

if __name__ == '__main__':
    main()
