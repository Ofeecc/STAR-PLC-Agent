"""Six hand-constructed specification witnesses, NOT a general LTL evaluator.

Original predicates below are manually translated from the named properties.
All infinite suffixes are constant, and the only non-pointwise obligations
are inactive in these witnesses. This diagnoses specification omissions;
it neither runs generated ST nor proves reference/ST equivalence.
"""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from plc_agent.reference import ReferenceController


def implies(a, b):
    return not a or b


def self_witness(tid, inputs, outputs):
    historical = ROOT / 'dataset_versions/v1_before_20261106'
    dataset = historical if historical.exists() else ROOT / 'dataset'
    task = json.loads((dataset / 'self_built' / (tid + '.json')).read_text(encoding='utf-8'))
    ref = ReferenceController(tid)
    rows = []
    previous = dict(task['initial_conditions'])
    previous_fault = False
    for k, (i, o) in enumerate(zip(inputs, outputs)):
        q = dict(ref.state)
        expected = ref.step(i)
        if tid == 'SELF003':
            qr, qu = previous['Run'], previous['ResetRequired']
            vr = i['EStopNC'] and i['Reset'] and not i['Start'] and not i['Stop']
            checks = [implies(k == 0, qu and not qr),
                      implies(not i['EStopNC'], not o['Run'] and o['ResetRequired']),
                      implies(qu, not o['Run']),
                      implies(qu and i['EStopNC'], o['ResetRequired'] == (not vr)),
                      implies(not qu and i['EStopNC'] and not i['Stop'] and i['Start'], o['Run']),
                      implies(not qu and i['EStopNC'] and i['Stop'], not o['Run'])]
        elif tid == 'SELF007':
            lead_before = previous.get('LeadA', True)
            completed = q['demand'] and not i['Demand'] and q['served']
            checks = [not (o['PumpA'] and o['PumpB']),
                      implies(not i['Demand'] or i['FaultA'], not o['PumpA']),
                      implies(not i['Demand'] or i['FaultB'], not o['PumpB']),
                      implies(i['Demand'] and o['LeadA'] and not i['FaultA'], o['PumpA']),
                      implies(i['Demand'] and not o['LeadA'] and not i['FaultB'], o['PumpB']),
                      implies(completed, o['LeadA'] == (not lead_before)),
                      implies(not completed, o['LeadA'] == lead_before)]
        elif tid == 'SELF010':
            rise = i['Fault'] and not previous_fault
            qa = previous['Alarm']
            checks = [o['Horn'] == (o['Alarm'] and not o['Acknowledged']),
                      implies(i['Fault'], o['Alarm']),
                      implies(rise, o['Alarm'] and not o['Acknowledged'] and o['Horn']),
                      implies(i['Reset'] and not i['Fault'], not any(o.values())),
                      implies(not i['Fault'] and not i['Reset'] and qa, o['Alarm']),
                      implies(not rise and not i['Reset'] and i['Ack'] and qa, o['Acknowledged'])]
            previous_fault = i['Fault']
        elif tid == 'SELF012':
            vr = i['Reset'] and not i['Fault'] and not i['Start']
            normal = not vr and not i['Stop']
            retry = q['mode'] == 2 and not i['Fault'] and q['free'] == 1
            checks = [implies(i['Fault'], not o['Run']), 0 <= o['Attempts'] <= 2,
                      implies(vr, not o['Run'] and not o['Locked'] and o['Attempts'] == 0),
                      implies(q['mode'] == 3 and not vr, o['Locked'] and not o['Run']),
                      implies(q['mode'] == 1 and i['Fault'] and normal and q['attempts'] == 2, o['Locked']),
                      implies(retry and normal, o['Run'] and o['Attempts'] == q['attempts'] + 1),
                      implies(q['mode'] == 2 and i['Fault'] and normal, not o['Run'])]
        else:
            raise ValueError(tid)
        if len(checks) != len(task['ltl']):
            raise ValueError('Property translation count mismatch')
        rows.append(dict(scan=k, inputs=i, wrong_outputs=o, required_outputs=expected,
                         original_properties={p['id']: bool(ok) for p, ok in zip(task['ltl'], checks)}))
        previous.update(o)
    return dict(task_id=tid, rows=rows,
                original_all_satisfied=all(all(r['original_properties'].values()) for r in rows),
                violates_required_outputs=any(r['wrong_outputs'] != r['required_outputs'] for r in rows),
                suffix='Repeat the final input/output row forever. History reaches a fixed point; the same checks remain true.')


def public_witness(tid):
    if tid == 'PUB010':
        i = dict(TemperatureSensorInput=40.0, SetTemperature=30.0)
        rows = []
        for k in range(3):
            heat = k == 0  # Wrong: the first call heats above the setpoint.
            o = dict(CurrentTemperature=40.0, SetTempDisplay=30.0, HeaterStatus=heat,
                     OverheatProtection=False, HeaterOutput=heat)
            sensor_fault = False
            demand = False
            heat_limit = False  # No heating interval has lasted five seconds.
            protect_previous = False
            checks = [implies(sensor_fault, not heat),
                      implies(o['OverheatProtection'], not heat), o['HeaterStatus'] == heat,
                      o['CurrentTemperature'] == i['TemperatureSensorInput'] and o['SetTempDisplay'] == i['SetTemperature'],
                      implies(not sensor_fault and not o['OverheatProtection'] and demand and not heat_limit, heat),
                      implies(heat_limit, o['OverheatProtection'] and not heat),
                      implies(protect_previous, o['OverheatProtection']),
                      True]  # P8's antecedent OverheatProtection is always FALSE.
            rows.append(dict(scan=k, inputs=i, wrong_outputs=o,
                             requirement_violation=heat,
                             original_properties={'P' + str(j + 1): bool(x) for j, x in enumerate(checks)}))
    elif tid == 'PUB011':
        i = dict(Mode=True, ForwardButton=False, ReverseButton=False,
                 SensorA=True, SensorB=False, SensorC=False,
                 ButtonA=True, ButtonB=False, ButtonC=False)
        o = dict(MotorForward=False, MotorReverse=False, CompletionLight=False)
        rows = []
        for k in range(3):
            auto, fwd, rev, light = True, False, False, False
            arrive = finish = False  # Expected route waits forever for B arrival.
            checks = [not(fwd and rev), implies(not auto, not fwd and not rev),
                      implies(auto, not rev), implies(auto and arrive, not fwd),
                      implies(auto and finish, light), implies(auto and not i['SensorC'], not light)]
            rows.append(dict(scan=k, inputs=i, wrong_outputs=o,
                             requirement_violation=True,
                             original_properties={'PUB011.P' + str(j + 1): bool(x) for j, x in enumerate(checks)}))
    else:
        raise ValueError(tid)
    return dict(task_id=tid, rows=rows,
                original_all_satisfied=all(all(r['original_properties'].values()) for r in rows),
                violates_required_outputs=any(r['requirement_violation'] for r in rows),
                suffix='Repeat final row forever. PUB010 has no further heating/protection; PUB011 never receives the destination sensor.')


def main():
    idle3 = dict(Start=False, Stop=False, EStopNC=True, Reset=False)
    cases = [self_witness('SELF003',
             [dict(idle3, Reset=True), dict(idle3, Start=True), idle3, idle3],
             [dict(Run=False, ResetRequired=False), dict(Run=True, ResetRequired=False),
              dict(Run=False, ResetRequired=False), dict(Run=False, ResetRequired=False)]),
             self_witness('SELF007', [dict(Demand=True, FaultA=True, FaultB=False)] * 3,
                          [dict(PumpA=False, PumpB=False, LeadA=True)] * 3),
             self_witness('SELF010', [dict(Fault=True, Ack=False, Reset=True),
                                     dict(Fault=True, Ack=True, Reset=True), dict(Fault=True, Ack=True, Reset=True)],
                          [dict(Alarm=True, Acknowledged=False, Horn=True)] * 3),
             self_witness('SELF012', [dict(Start=True, Stop=False, Fault=False, Reset=False),
                                     dict(Start=False, Stop=False, Fault=False, Reset=False),
                                     dict(Start=False, Stop=False, Fault=False, Reset=False)],
                          [dict(Run=False, Locked=False, Attempts=0)] * 3),
             public_witness('PUB010'), public_witness('PUB011')]
    if not all(c['original_all_satisfied'] and c['violates_required_outputs'] for c in cases):
        raise AssertionError('A proposed witness did not demonstrate the claimed omission')
    result = dict(evidence='HAND_TRANSLATED_SPECIFICATION_WITNESSES', general_ltl_parser=False,
                  generated_st_executed=False, model_checking_performed=False,
                  scope='Six named formula sets only. Predicates manually translated; constant infinite tails explained in each record. Python SELF reference supplies independent expected states/outputs, never actual PLC evidence.',
                  cases=cases)
    (HERE / 'counterexamples.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(witnesses=len(cases), all_show_omission=True), ensure_ascii=False))


if __name__ == '__main__':
    main()
