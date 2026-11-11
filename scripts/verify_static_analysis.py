"""Verify the saved template with real compilation and a deliberate SA0033 trigger.

Run from the repository root with its Python environment and PYTHONPATH=src.
No IDE automation or language-model API is used.
"""
import argparse
import hashlib
import json
import re
from dataclasses import asdict
from pathlib import Path

from plc_agent.cli import compiler_smoke, require_compiler_preflight
from plc_agent.common import ROOT, now, read_json, write_json
from plc_agent.compiler import compile_st
from plc_agent.config import Settings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--probe-only', action='store_true', help='Reuse matching successful compiler preflight')
    args = parser.parse_args()
    cfg = Settings.load(load_api=False)
    initial_hash = hashlib.sha256(Path(cfg.codesys_template).read_bytes()).hexdigest()
    if args.probe_only:
        require_compiler_preflight(cfg)
        preflight = read_json(ROOT / 'results/summary/compiler_preflight.json')
    else:
        print('Running valid / invalid / repaired compiler preflight...', flush=True)
        preflight = compiler_smoke(cfg)
    print(json.dumps({'compiler_verified': preflight['verified'], 'statuses': [r['status'] for r in preflight['runs']]}), flush=True)
    folder = ROOT / 'results/raw' / ('static_analysis_' + now().replace(':', '').replace('.', ''))
    candidate = {
        'declaration': 'FUNCTION_BLOCK FB_Task\nVAR_INPUT\n Start : BOOL;\n Stop : BOOL;\nEND_VAR\nVAR_OUTPUT\n Run : BOOL := FALSE;\nEND_VAR\nVAR\n StaticAnalysisUnusedProbe : DINT := 123;\nEND_VAR',
        'implementation': 'IF Stop THEN\n Run := FALSE;\nELSIF Start THEN\n Run := TRUE;\nEND_IF;',
        'supporting_objects': [],
    }
    print('Compiling isolated copy with deliberate unused local variable...', flush=True)
    task = {'id': 'STATIC_ANALYSIS_SMOKE', 'diagnostic_probe_program': {
        'declaration': 'PROGRAM PLC_PRG\nVAR\n ProbeInstance : FB_Task;\n StaticAnalysisUnusedProgramProbe : DINT;\nEND_VAR',
        'implementation': 'ProbeInstance(Start := FALSE, Stop := TRUE);',
    }}
    probe = asdict(compile_st(task, candidate, folder / 'unused_variable', cfg))
    matched = [d for d in probe['diagnostics'] if re.search(r'\bSA0033\b', d.get('code', '') + ' ' + d.get('text', ''), re.I)
               and any(name.casefold() in d.get('text', '').casefold() for name in ('StaticAnalysisUnusedProbe', 'StaticAnalysisUnusedProgramProbe'))]
    final_hash = hashlib.sha256(Path(cfg.codesys_template).read_bytes()).hexdigest()
    verified = bool(preflight['verified'] and probe['status'] in ('PASS', 'COMPILE_FAIL') and matched
                    and initial_hash == final_hash == preflight['template_sha256'])
    result = {'observed_utc': now(), 'verified': verified, 'template_sha256': final_hash,
              'template_unchanged_during_check': initial_hash == final_hash,
              'compiler_preflight_verified': preflight['verified'],
              'compiler_statuses': [r['status'] for r in preflight['runs']],
              'unused_variable_probe': probe, 'matched_static_diagnostics': matched,
              'scope': 'SA0033_TRIGGER_AND_COMPILER_PREFLIGHT; other rules not individually exercised'}
    write_json(folder / 'static_analysis_summary.json', result)
    write_json(ROOT / 'results/summary/static_analysis_preflight.json', result)
    print(json.dumps({'verified': verified, 'probe_status': probe['status'], 'matched': matched,
                      'evidence_dir': str(folder)}, ensure_ascii=False, indent=2), flush=True)
    return 0 if verified else 1


if __name__ == '__main__':
    raise SystemExit(main())
