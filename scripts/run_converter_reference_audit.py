"""Run available reference ST examples through the local verifier."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from plc_agent.dataset import load_tasks
from plc_agent.st_verifier import verify_candidate_st

tasks = {t['id']: t for t in load_tasks()}
out = ROOT / 'results/raw/converter_reference_audit_20261114'
out.mkdir(parents=True, exist_ok=True)
rows = []
for path in sorted((ROOT / 'codesys/examples').glob('*.json')):
    task_id = path.stem
    if task_id not in tasks:
        continue
    candidate = json.loads(path.read_text(encoding='utf-8-sig'))
    result = verify_candidate_st(tasks[task_id], candidate, out / task_id, timeout=8, executable=sys.argv[1], tool='nuxmv')
    rows.append({k: result.get(k) for k in ('task_id', 'status', 'reason', 'passed_properties', 'failed_properties')})
    (out / 'summary.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    print(task_id, result['status'], result.get('reason') or '', flush=True)
