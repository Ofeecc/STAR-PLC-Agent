from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from plc_agent.common import digest
from plc_agent.dataset import load_tasks,validate
from plc_agent.reference import evaluate_reference

cases=json.loads((ROOT/'docs/规约逐题审查_20261106/counterexamples.json').read_text(encoding='utf-8'))['cases']
evidence=[]
for case in cases:
    tid=case['task_id']; folder='self_built' if tid.startswith('SELF') else 'public'
    p=ROOT/'dataset'/folder/(tid+'.json'); t=json.loads(p.read_text(encoding='utf-8'))
    steps=[]
    for row in case['rows']:
        expected=row.get('required_outputs')
        if tid=='PUB010':
            expected=dict(row['wrong_outputs'],HeaterOutput=False,HeaterStatus=False)
        elif tid=='PUB011':
            expected=dict(MotorForward=True,MotorReverse=False,CompletionLight=False)
        step={'inputs':row['inputs'],'expected':expected}
        if tid=='PUB010': step['dt_ms']=0 if row['scan']==0 else 100
        steps.append(step)
    test={'id':'V2_omission_regression','purpose':'Reject the concrete wrong behavior documented in the 2026-11-06 specification review.','steps':steps}
    t['tests']=[c for c in t['tests'] if c['id']!=test['id']]+[test]
    rejected=[any(row['wrong_outputs'].get(k)!=v for k,v in step['expected'].items()) for row,step in zip(case['rows'],steps)]
    if not any(rejected): raise ValueError(tid+' witness not rejected')
    if tid.startswith('SELF') and not evaluate_reference(t)['passed']: raise ValueError(tid+' reference disagreement')
    p.write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    evidence.append({'task_id':tid,'wrong_trace_rejected':True,'mismatch_scans':[j for j,x in enumerate(rejected) if x]})
tasks=load_tasks(); report=validate(tasks)
if report['errors']:raise ValueError(report['errors'])
manifest=ROOT/'dataset_versions/v2_revision_manifest.json'
m=json.loads(manifest.read_text(encoding='utf-8'))
for t in tasks:
    old=json.loads((ROOT/'dataset_versions/v1_before_20261106'/('public' if t['kind']=='public' else 'self_built')/(t['id']+'.json')).read_text(encoding='utf-8'))
    if old['requirements']!=t['requirements']:raise ValueError('Changed source text')
    next(c for c in m['changes'] if c['id']==t['id'])['after_sha256']=digest(t)
m['validation']=report;m['regression_witnesses']=evidence
manifest.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'validation':report,'regressions':evidence},ensure_ascii=False))
