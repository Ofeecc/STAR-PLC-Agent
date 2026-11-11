"""Configured PUB001/PUB003 runs with context and execution evidence.

Default is a local plan check. --run requires explicit approval for the selected runs.
"""
import argparse
from dataclasses import asdict, replace
import hashlib
import json
from pathlib import Path
import subprocess
import shutil
import time

from plc_agent.backend import CodesysBackend
from plc_agent.baseline import run_baseline
from plc_agent.cli import require_compiler_preflight
from plc_agent.common import ROOT, digest, now, read_json, write_json
from plc_agent.compiler import normalize_candidate
from plc_agent.config import Settings
from plc_agent.dataset import load_tasks
from plc_agent.harness import run_harness
from plc_agent.llm import ResponsesClient
from plc_agent.simulation import run_functional
from plc_agent.task_view import agent_view

SPEC = read_json(ROOT/'configs/pilot_pair.json')
MODEL = SPEC['model']
RUNS = [(r['task'],r['agent'],r['condition']) for r in SPEC['runs']]


class RecordedBackend:
    def __init__(self, settings, workspace):
        self.delegate = CodesysBackend(settings)
        self.workspace = workspace

    def event(self, event, **fields):
        row = {'utc':now(), 'event':event, **fields}
        with (self.workspace/'execution.jsonl').open('a',encoding='utf-8') as stream:
            stream.write(json.dumps(row,ensure_ascii=False)+'\n')
        print(json.dumps(row,ensure_ascii=False),flush=True)

    def compile(self, task, candidate, workspace):
        self.event('compile_started', path=str(workspace))
        result = self.delegate.compile(task,candidate,workspace)
        self.event('compile_finished',status=result.status,success=result.success,
                   source_sha256=result.source_sha256)
        return result

    def simulate(self, task, candidate, cases, workspace):
        self.event('selftest_started',path=str(workspace),cases=len(cases))
        result = self.delegate.simulate(task,candidate,cases,workspace)
        self.event('selftest_finished',status=result.status,passed=result.passed_cases,
                   evaluated=result.evaluated_cases)
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--allow-model-api',action='store_true')
    args = parser.parse_args()
    if args.run and not args.allow_model_api:
        parser.error('Ask for approval of the selected experiments, then pass --allow-model-api')
    cfg = replace(Settings.load(load_api=True), **SPEC['settings'])
    tasks = {t['id']:t for t in load_tasks()}
    plan = {'model':MODEL,'reasoning_effort_requested':cfg.reasoning_effort,
            'local_context_budget':cfg.context_window_tokens,
            'context_budget_method':'conservative UTF8 byte upper bound; full history retained or request stopped',
            'max_requests_per_run':cfg.max_llm_calls,'max_candidate_compiles_per_run':3,
            'max_output_tokens_per_request':cfg.max_output_tokens,
            'max_selftest_simulations_per_run':3,'fixed_evaluations_per_run':1,
            'runs':[{'task':t,'agent':a,'condition':c,'fixed_cases':len(tasks[t]['tests']),
                     'fixed_steps':sum(len(x['steps']) for x in tasks[t]['tests'])} for t,a,c in RUNS],
            'baseline_implementation':'project custom_tool_loop, driver=deepseek_harness',
            'baseline_status':SPEC.get('baseline_status',''),
            'stop_batch_on_infrastructure_error':True,'key_loaded':bool(cfg.api_key)}
    print(json.dumps(plan,ensure_ascii=False,indent=2),flush=True)
    require_compiler_preflight(cfg)
    if not cfg.api_key:
        raise ValueError('API key missing')
    if not args.run:
        return 0
    folder = ROOT/'results/raw'/('pilot_pair_'+now().replace(':','').replace('.',''))
    folder.mkdir(parents=True,exist_ok=False)
    write_json(folder/'plan.json',plan)
    snapshot = asdict(cfg)
    snapshot.pop('api_key',None)
    snapshot['template_sha256'] = hashlib.sha256(Path(cfg.codesys_template).read_bytes()).hexdigest()
    snapshot['git_head'] = subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True).stdout.strip()
    write_json(folder/'runtime_config.json',snapshot)
    source_files = [*ROOT.glob('src/plc_agent/*.py'), *ROOT.glob('codesys/scripts/*.py'),
                    Path(__file__), ROOT/'configs/pilot_pair.json']
    source_manifest = {}
    for source in source_files:
        relative = source.resolve().relative_to(ROOT)
        target=folder/'source_snapshot'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,target)
        source_manifest[str(relative)]=hashlib.sha256(source.read_bytes()).hexdigest()
    write_json(folder/'source_manifest.json',source_manifest)
    rows=[]
    for tid, agent, condition in RUNS:
        task=tasks[tid]
        experiment_started=time.monotonic()
        workspace=folder/f'{tid}_{agent}'
        # run_harness owns creation of its workspace. Backend event writes happen later.
        client=ResponsesClient(cfg)
        backend=RecordedBackend(cfg,workspace)
        print(json.dumps({'event':'experiment_started','task':tid,'agent':agent,'utc':now()},ensure_ascii=False),flush=True)
        if agent=='baseline':
            row=run_baseline(task,MODEL,workspace,cfg,condition,driver='deepseek_harness',
                             client=client,backend=backend,spec_visible=True)
        else:
            row=run_harness(task,MODEL,workspace,client,cfg,condition,backend=backend,spec_visible=True)
        row['agent_generation_status']=row['status']
        row['model_requests_attempted']=client.request_count
        candidate=row.get('final_candidate')
        source_hash=digest(normalize_candidate(candidate)) if candidate else None
        compiled=bool(candidate and any(a.get('success') and a.get('source_sha256')==source_hash
                                       for a in row.get('compilation_attempts',[])))
        if compiled and row['status'] not in ('TOOL_ERROR','TIMEOUT'):
            backend.event('fixed_evaluation_started',cases=len(task['tests']))
            outcome=run_functional(task,candidate,source_hash,workspace/'fixed_evaluation',cfg)
            row['functional_execution']=outcome
            row['functional']=outcome.get('functional',{'status':outcome['status'],'evaluated_cases':0,'passed_cases':0})
            row['status']=outcome['status']
            row['reason']='Held-out fixed dataset evaluation after agent generation; results not returned to the agent'
            backend.event('fixed_evaluation_finished',status=row['status'],functional=row['functional'])
        row['formal_verification']={'status':'UNVERIFIED','reason':'Candidate ST has no verified SMV encoding'}
        row['agent_elapsed_seconds']=row['elapsed_seconds']
        row['elapsed_seconds']=time.monotonic()-experiment_started
        row['finished_utc']=now()
        write_json(workspace/'evaluation_task.json',task)
        write_json(workspace/'result.json',row)
        rows.append({'task':tid,'agent':agent,'status':row['status'],
                     'model_requests':client.request_count,'compiler_calls':row['compiler_call_count'],
                     'functional':row['functional'],'result_path':str(workspace/'result.json')})
        write_json(folder/'summary.json',{'plan':plan,'completed_runs':rows})
        write_json(folder/'trace_index.json',{'artifacts':[str(p.relative_to(folder)) for p in sorted(folder.rglob('*'))
                                                        if p.is_file() and p.suffix in ('.json','.jsonl','.st','.log')]})
        print(json.dumps({'event':'experiment_finished',**rows[-1]},ensure_ascii=False),flush=True)
        if row['status'] in ('TOOL_ERROR','TIMEOUT'):
            print('Stopped remaining experiments on infrastructure error; no automatic paid rerun.',flush=True)
            break
    print(json.dumps({'evidence_dir':str(folder),'completed_runs':len(rows)},ensure_ascii=False),flush=True)
    return 0 if len(rows)==len(RUNS) and all(r['status']=='PASS' for r in rows) else 1


if __name__=='__main__':
    raise SystemExit(main())
