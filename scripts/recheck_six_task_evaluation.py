"""Re-evaluate retained real PLC traces and final candidates after evaluator fixes.

No model access. Original stage evidence remains immutable. Corrected evaluation
is stored separately and merged only when requested after the batch completes.
"""
import argparse

from plc_agent.cli import _selected_candidate_and_hash
from plc_agent.common import ROOT, now, read_json, write_json
from plc_agent.dataset import load_tasks
from plc_agent.formal_verify import verify_candidate
from plc_agent.functional import evaluate_trace

p = argparse.ArgumentParser(); p.add_argument('--task'); p.add_argument('--merge', action='store_true'); args = p.parse_args()
base = ROOT/'results/raw/six_task_fullflow_20261114'
tasks = {t['id']: t for t in load_tasks()}
rows = []
for tid in ('PUB001', 'PUB003', 'PUB007', 'PUB009', 'PUB015', 'PUB016'):
    path = base/tid/'fullflow_result.json'
    if not path.exists():
        continue
    row = read_json(path)
    if args.task and tid != args.task:
        rows.append(row); continue
    task = tasks[tid]
    if row['compiled']:
        genpath = base/tid/'generation/result.json'
        cand, sha = _selected_candidate_and_hash(read_json(genpath), genpath)
        out = base/'evaluation_v2'/tid
        out.mkdir(parents=True, exist_ok=True)
        tracepath = base/tid/'fixed_tests/trace.json'
        if tracepath.exists():
            row['functional'] = evaluate_trace(task, sha, read_json(tracepath), evidence_root=tracepath.parent)
            write_json(out/'functional_reevaluation.json', row['functional'])
        row['verification'] = verify_candidate(task, cand, out/'formal', timeout=60)
        f, v = row['functional'], row['verification']
        row['stage_checks_passed'] = f['status'] == 'PASS' and v['status'] == 'PASS'
        row['status'] = ('PASS' if f['status'] == 'PASS' and v.get('full_specification_verified') else
                         'FAIL' if f['status'] == 'TEST_FAIL' or v['status'] == 'COUNTEREXAMPLE' else 'PARTIAL')
        row['evaluation_revision'] = {'utc': now(), 'trace_path': str(tracepath), 'source_sha256': sha,
                                      'corrected_evidence': str(out), 'new_model_requests': 0}
        write_json(out/'fullflow_result.json', row)
        print(f'{tid}: fixed={f["status"]} {f.get("passed_cases")}/{f.get("evaluated_cases")}; formal={v["status"]}', flush=True)
    rows.append(row)
if args.merge:
    assert len(rows) == 6, 'Do not merge partial batch'
    summary = read_json(base/'summary.json')
    summary['results'] = rows
    summary['completed_tasks'] = len(rows)
    write_json(base/'summary_before_evaluator_correction.json', read_json(base/'summary.json'))
    write_json(base/'summary.json', summary)
