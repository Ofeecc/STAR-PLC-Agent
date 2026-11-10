"""Versioned corrections from the per-task semantic review. No model calls."""
import inspect
import json
import shutil
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from plc_agent.common import digest
from plc_agent.dataset import validate
from plc_agent.reference import ReferenceController


def main():
    review=json.loads((ROOT/'docs/规约逐题审查_20261106/review_manifest.json').read_text(encoding='utf-8'))
    archive=ROOT/'dataset_versions/v1_before_20261106'
    if archive.exists():
        raise SystemExit('Archive already exists; refusing to overwrite or apply twice')
    shutil.copytree(ROOT/'dataset',archive)
    changes=[]
    for entry in review['tasks']:
        path=ROOT/entry['source']; t=json.loads(path.read_text(encoding='utf-8'))
        tid=t['id']; n=entry['review']; old=digest(t)
        t['specification_version']='2.0-review-corrections-20261106'
        t['specification_contract']={
            'observation':'I[k] is sampled before execution; O[k] is observed after execution. Initial conditions apply before invocation zero.',
            'normative_completion':n['proposal'],
            'history_binding':'Every previous-output name refers to the preceding observed output with the declared initial value. Previous-input memories update on EVERY invocation, including reset, invalid input, stop and mode change. Reference phase/history is independently advanced from sampled inputs by the stated transition rules, never supplied by the candidate.',
            'evaluation_scope':'Properties include interpreted data predicates. No claim of export to a model checker or completed formal proof.',
            'review_source':'docs/规约逐题审查_20261106/'+tid+'.md'}
        t['assumptions']=list(t.get('assumptions',[]))
        t['assumptions'].append('The specification_contract is normative and supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.')
        # Every reviewed missing requirement is a normative predicate, not merely advice.
        t['atomic_propositions']['CompleteBehaviorV2']=n['proposal']
        t['ltl'].append({'id':tid+'.V2.COMPLETE','formula':'G(CompleteBehaviorV2)',
                         'explanation':'The complete per-invocation relation defined in specification_contract.normative_completion; requires explicit encoding before model checking.'})
        if tid.startswith('SELF'):
            method=getattr(ReferenceController,'_'+tid)
            t['specification_contract']['reference_state_initial']=ReferenceController._INITIAL_STATES[tid]
            t['specification_contract']['deterministic_transition_python']=inspect.getsource(method)
            t['specification_contract']['transition_binding']='Initialize an independent reference state with reference_state_initial. For every sampled input execute the listed deterministic transition once; require EVERY actual OUTPUT to equal its returned value. Do not update this reference state from candidate outputs. This defines the complete scan relation; it is not evidence of ST execution.'
            t['atomic_propositions']['CompleteBehaviorV2']='Every observed OUTPUT equals the output of the independent deterministic transition in specification_contract, initialized and advanced exactly as transition_binding specifies.'
        if tid=='SELF009':
            next(p for p in t['ltl'] if p['id']=='P5')['formula']='G(X(qPulse) <-> PartPulse)'
        if tid=='SELF010':
            next(p for p in t['ltl'] if p['id']=='P6')['formula']='G((!rise & !(Reset & !Fault) & Ack & qAlarm) -> Acknowledged)'
        additions={
          'SELF003':['G((!qRequired & EStopNC) -> !ResetRequired)','G((!qRequired & EStopNC & !Stop & !Start) -> (Run <-> qRun))'],
          'SELF007':['G((Demand & FaultA & !FaultB) -> PumpB)','G((Demand & FaultB & !FaultA) -> PumpA)'],
          'PUB010':['G((TemperatureSensorInput>SetTemperature) -> !HeaterOutput)'],
        }
        for j,f in enumerate(additions.get(tid,[])):
            t['ltl'].append({'id':tid+'.V2.'+str(j+1),'formula':f,'explanation':'Explicit correction of a demonstrated omission.'})
        if tid=='PUB010':
            t['assumptions'].append('V2 evaluation decision: retain the existing >=5s trip threshold as an explicit benchmark interpretation of the source more-than wording; cooldown MUST clear at the first observed elapsed>=3s, though a sensor fault or absent demand still prevents heating. No spontaneous protection is allowed. This benchmark interpretation is not claimed to be instructor clarification.')
        if tid in ('PUB004','PUB005'):
            t['assumptions'].append('DebounceTime is a strictly positive constant throughout each test case. Dynamic changes are outside this benchmark domain. Time must advance for eventual-start properties.')
        if tid in ('PUB003','PUB008','PUB009','PUB010','PUB017','PUB020'):
            t['assumptions'].append('Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.')
        if tid=='PUB007':
            t['assumptions'].append('V2 confirms the existing evaluation policy: start is level-sensitive and reselects each TRUE invocation; without start, mode/selection/priority changes do not reselect. Automatic top-three applies to selection events, not unconditionally to every automatic invocation.')
        if tid in ('PUB015','PUB019'):
            t['assumptions'].append('V2 mode-change priority: emergency stop first; then a change of mode after the first invocation clears sequence/latches and suppresses commands for that invocation; edge memories still update. The first invocation establishes the selected mode and executes normally. New commands are accepted on subsequent invocations subject to their edge rules.')
            if tid=='PUB015':
                for a in ('toggle','toB','toMix','toC','fromC','mixed'):
                    t['atomic_propositions'][a]='No mode change this invocation AND ('+t['atomic_propositions'][a]+')'
            else:
                for p in t['ltl']:
                    if p['id'] in ('PUB019.P3','PUB019.P5','PUB019.P6','PUB019.P8'):
                        p['formula']=p['formula'].replace('safe &','safe & !modeChanged &').replace('G(safe ->','G((safe & !modeChanged) ->')
                t['atomic_propositions']['modeChanged']='Selected mode differs from previous invocation; FALSE for the first invocation.'
        # Full reference expectations remove partial-output blind spots on self tasks.
        if tid.startswith('SELF'):
            for case in t['tests']:
                controller=ReferenceController(tid)
                for step in case['steps']:
                    expected=controller.step(step['inputs'])
                    if any(expected[k]!=v for k,v in step['expected'].items()):
                        raise ValueError('Existing expectation disagreement: '+tid)
                    step['expected']=expected
        path.write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        changes.append({'id':tid,'before_sha256':old,'after_sha256':digest(t),'requirements_unchanged':True})
    tasks=[json.loads(p.read_text(encoding='utf-8')) for folder in ('public','self_built') for p in sorted((ROOT/'dataset'/folder).glob('*.json'))]
    result=validate(tasks)
    if result['errors']: raise ValueError(result['errors'])
    out=ROOT/'dataset_versions/v2_revision_manifest.json'
    out.write_text(json.dumps({'version':'2.0-review-corrections-20261106','changes':changes,'validation':result,
        'limitations':'Public interpreted predicates still require executable monitor implementation; no completed LTL model checking or PLC test run is claimed.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__': main()
