"""Offline rechecks on retained candidates; never counted as new agent runs."""
from dataclasses import asdict
from plc_agent.common import ROOT, read_json, write_json, digest
from plc_agent.dataset import load_tasks
from plc_agent.config import Settings
from plc_agent.compiler import compile_st
from plc_agent.formal_verify import verify_candidate
from plc_agent.simulation import run_functional
from plc_agent.model_checker import find_nusmv, find_nuxmv

cfg = Settings.load(load_api=False)
tasks = {t['id']: t for t in load_tasks()}
m = read_json(ROOT/'results/summary/campaign.json')
out = ROOT/'results/raw/pilot_fix_preflight_20261114'
out.mkdir(parents=True, exist_ok=True)
p3 = ROOT/m['records']['E3/PUB003']
c3 = read_json(p3.parent/'compile_00/candidate.json')
r = {'NuSMV': str(find_nusmv()), 'nuXmv': str(find_nuxmv())}
r['attribute_compile'] = asdict(compile_st(tasks['PUB003'], c3, out/'attribute_compile', cfg))
write_json(out/'summary.json', r)
print('attribute compile: '+r['attribute_compile']['status'], flush=True)
p4 = ROOT/m['records']['E3/PUB004']
c4 = read_json(p4.parent/'final_candidate.json')
cases = read_json(p4.parent/'selftest.json')
r['timing_simulation'] = run_functional(tasks['PUB004'], c4, digest(c4), out/'timing_simulation', cfg, cases=cases)
write_json(out/'summary.json', r)
print('timing simulation: '+r['timing_simulation']['status']+' '+str(r['timing_simulation'].get('reason')), flush=True)
p1 = ROOT/m['records']['E3/PUB001']
r['formal'] = verify_candidate(tasks['PUB001'], read_json(p1.parent/'final_candidate.json'), out/'formal', timeout=30)
write_json(out/'summary.json', r)
print('formal: '+r['formal']['status']+' '+str(r['formal'].get('reason')), flush=True)
