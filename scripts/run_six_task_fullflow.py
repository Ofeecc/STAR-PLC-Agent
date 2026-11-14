"""Six-task pilot: synthesis, real compiler, held-out fixed tests, final ST formal check.

Each stage is saved before the next starts. Reinvoking the same output directory
resumes missing stages; completed synthesis is never silently paid for again.
"""
import argparse
from pathlib import Path

from plc_agent.cli import _selected_candidate_and_hash, require_compiler_preflight
from plc_agent.common import ROOT, digest, now, read_json, write_json
from plc_agent.config import Settings
from plc_agent.dataset import load_tasks, validate
from plc_agent.formal_verify import verify_candidate
from plc_agent.harness import run_harness
from plc_agent.llm import ResponsesClient
from plc_agent.model_checker import find_nusmv, find_nuxmv
from plc_agent.simulation import run_functional

IDS = ('PUB001', 'PUB003', 'PUB007', 'PUB009', 'PUB015', 'PUB016')
MODEL = 'deepseek-v4.1-flash-1017'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-model-api', action='store_true')
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()
    cfg = Settings.load(load_api=args.allow_model_api)
    tasks = load_tasks()
    assert not validate(tasks)['errors']
    require_compiler_preflight(cfg)
    find_nusmv()
    find_nuxmv()
    cap = read_json(ROOT/'results/summary/model_capabilities.json')
    assert any(x['model'] == MODEL and x['tool_roundtrip'] for x in cap['model_tests'])
    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    manifest = {'created_utc': now(), 'model': MODEL, 'task_ids': IDS,
                'dataset_sha256': digest(tasks), 'scope': 'six_task_pilot_not_full_assignment',
                'settings': {k: v for k, v in vars(cfg).items() if k != 'api_key'}}
    if (out/'manifest.json').exists():
        old = read_json(out/'manifest.json')
        assert old['dataset_sha256'] == manifest['dataset_sha256']
    else:
        write_json(out/'manifest.json', manifest)
    rows = []
    for tid in IDS:
        task = next(t for t in tasks if t['id'] == tid)
        work = out/tid
        record = work/'generation/result.json'
        if not record.exists():
            if not args.allow_model_api:
                raise ValueError('Missing generation requires authorized --allow-model-api')
            print(f'{tid}: generating ST', flush=True)
            run_harness(task, MODEL, work/'generation', ResponsesClient(cfg), cfg, 'E3')
        row = read_json(record)
        final = work/'fullflow_result.json'
        if final.exists():
            rows.append(read_json(final))
            continue
        result = {'task_id': tid, 'difficulty': task['difficulty'], 'model': MODEL,
                  'generation_status': row['status'], 'generation_reason': row.get('reason'),
                  'compiled': bool(row['final_compiled']), 'llm_calls': row['llm_calls'],
                  'usage': row.get('usage', []), 'planned_cases': len(task['tests']),
                  'generation_record': str(record), 'functional': {'status': 'NOT_RUN'},
                  'verification': {'status': 'NOT_RUN'}, 'status': 'PARTIAL'}
        if row['final_compiled']:
            candidate, source_hash = _selected_candidate_and_hash(row, record)
            functional_path = work/'fixed_tests/simulation_result.json'
            print(f'{tid}: real CODESYS fixed tests ({len(task["tests"])})', flush=True)
            outcome = read_json(functional_path) if functional_path.exists() else run_functional(
                task, candidate, source_hash, work/'fixed_tests', cfg)
            result['functional'] = outcome.get('functional') or outcome
            result['functional_execution'] = str(functional_path)
            print(f'{tid}: final candidate ST -> SMV -> model checker', flush=True)
            # Full reviewed task/spec, no agent-generated assertions or reference ST.
            result['verification'] = verify_candidate(task, candidate, work/'formal', timeout=60)
            fs, vs = result['functional']['status'], result['verification']['status']
            result['stage_checks_passed'] = fs == 'PASS' and vs == 'PASS'
            if fs == 'PASS' and result['verification'].get('full_specification_verified'):
                result['status'] = 'PASS'
            elif fs == 'TEST_FAIL' or vs == 'COUNTEREXAMPLE':
                result['status'] = 'FAIL'
        else:
            result['status'] = row['status']
        write_json(final, result)
        rows.append(result)
        summary = {'generated_utc': now(), 'planned_tasks': len(IDS), 'completed_tasks': len(rows),
                   'planned_cases': sum(len(t['tests']) for t in tasks if t['id'] in IDS), 'results': rows}
        write_json(out/'summary.json', summary)
        print(f'{tid}: compiled={result["compiled"]}, fixed={result["functional"]["status"]}, formal={result["verification"]["status"]}', flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
