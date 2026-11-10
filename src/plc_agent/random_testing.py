"""Seed-deterministic random differential test generator for all 32 tasks."""
from __future__ import annotations
import random
from typing import Any
from .scan_contract import ScanContract, check_contract_trace

TIMED_TASKS = {'PUB004', 'PUB005', 'PUB006', 'PUB010', 'PUB012', 'PUB013'}


def _generate_step_input(
    task_id: str,
    rng: random.Random,
    state: dict[str, Any],
) -> tuple[dict[str, Any], float | None]:
    dt_ms: float | None = None
    if task_id in TIMED_TASKS:
        dt_ms = float(rng.choice([10, 20, 50, 100, 200, 500, 1000]))

    if task_id == 'PUB001':
        events = [
            'bottleSensor', 'cleaningConfirmButton', 'fillingConfirmButton',
            'cappingConfirmButton', 'packingConfirmButton', 'finishedButton'
        ]
        active = rng.choice(events) if rng.random() < 0.7 else None
        inp = {e: (e == active) for e in events}
    elif task_id == 'PUB002':
        inp = {'value': rng.randint(0, 0xFFFFFFFF)}
    elif task_id == 'PUB003':
        hi = round(rng.uniform(60.0, 100.0), 2)
        lo = round(rng.uniform(10.0, 50.0), 2)
        width = round(rng.uniform(0.1, 5.0), 2)
        val = round(rng.uniform(0.0, 110.0), 2)
        inp = {'Value': val, 'hiLevel': hi, 'loLevel': lo, 'hystWindow': width}
    elif task_id == 'PUB004':
        deb = state.setdefault('deb', 'T#100ms')
        cyc = state.setdefault('cyc', 'T#10ms')
        inp = {
            'VISCOSITY_OK': rng.choice([True, False]),
            'PASTE_E_STOP_NC': rng.choice([True, True, False]),
            'DebounceTime': deb,
            'CycleTime': cyc,
        }
    elif task_id == 'PUB005':
        deb = state.setdefault('deb', 'T#200ms')
        inp = {
            'Gap_Exceeded': rng.choice([True, False]),
            'Weld_E_Stop_NC': rng.choice([True, True, False]),
            'DebounceTime': deb,
        }
    elif task_id == 'PUB006':
        inp = {
            'DO_LOW': rng.choice([True, False]),
            'AERATION_E_STOP_NC': rng.choice([True, True, False]),
        }
    elif task_id == 'PUB007':
        st = rng.choice([True, False])
        sp = rng.choice([True, False]) if not st else False
        pumps = [
            {
                'priority': rng.randint(-10, 10),
                'selection': rng.choice([True, False]),
                'RunComd': rng.choice([True, False]),
            }
            for _ in range(5)
        ]
        inp = {
            'mode': rng.choice([True, False]),
            'start': st,
            'stop': sp,
            'pumpGroup': pumps,
        }
    elif task_id == 'PUB008':
        cnt = rng.randint(1, 8)
        raw = [rng.randint(-27648, 27648) for _ in range(8)]
        chans = [
            {
                'enable': rng.choice([True, False]),
                'bipolar': rng.choice([True, False]),
                'measuringMode': rng.choice([0, 1, 2]),
                'hiLIM': 100.0,
                'loLIM': 0.0,
                'outputValue': 0.0,
            }
            for _ in range(8)
        ]
        inp = {'count': cnt, 'analogValues': raw, 'channels': chans}
    elif task_id == 'PUB009':
        ws = state.setdefault('ws', rng.randint(2, 8))
        inp = {
            'cyclicExecution': rng.choice([True, False]),
            'trigger': rng.choice([True, False]),
            'value': round(rng.uniform(-100.0, 100.0), 2),
            'windowSize': ws,
            'reset': rng.choice([False, False, False, True]),
        }
    elif task_id == 'PUB010':
        inp = {
            'TemperatureSensorInput': round(rng.uniform(10.0, 95.0), 1),
            'SetTemperature': round(rng.uniform(40.0, 60.0), 1),
        }
    elif task_id == 'PUB011':
        inp = {
            'Mode': rng.choice([True, False]),
            'ForwardButton': rng.choice([True, False]),
            'ReverseButton': rng.choice([True, False]),
            'SensorA': rng.choice([True, False]),
            'SensorB': rng.choice([True, False]),
            'SensorC': rng.choice([True, False]),
            'ButtonA': rng.choice([True, False]),
            'ButtonB': rng.choice([True, False]),
            'ButtonC': rng.choice([True, False]),
        }
    elif task_id == 'PUB012':
        cyc = state.setdefault('cyc', 'T#10ms')
        inp = {
            'THICKNESS_FAULT': rng.choice([True, False]),
            'THICKNESS_SIGNAL_VALID': rng.choice([True, True, False]),
            'CUTTING_RUN': rng.choice([True, False]),
            'FaultTimestamp': rng.randint(1000, 9999),
            'CycleTime': cyc,
        }
    elif task_id == 'PUB013':
        inp = {
            'OCCUPANCY_DETECTED': rng.choice([True, False]),
            'ENERGY_SAVING_MODE': rng.choice([True, False]),
            'HVAC_MODE_SELECTOR': rng.choice([0, 1, 2, 3]),
        }
    elif task_id == 'PUB014':
        inp = {'ipText': f'{rng.randint(1, 254)}.{rng.randint(0, 254)}.{rng.randint(0, 254)}.{rng.randint(1, 254)}'}
    elif task_id == 'PUB015':
        pm = state.setdefault('pm', rng.choice([True, False]))
        inp = {
            'estop': rng.choice([True, True, True, False]),
            'opeMode': rng.choice([True, False]),
            'valveAStart': rng.choice([True, False]),
            'valveBStart': rng.choice([True, False]),
            'valveCStart': rng.choice([True, False]),
            'valveDStart': rng.choice([True, False]),
            'mixMotorStart': rng.choice([True, False]),
            'autoStart': rng.choice([True, False]),
            'processMode': pm,
            'levelSensor': rng.randint(0, 110),
            'mixMotorComplete': rng.choice([True, False]),
        }
    elif task_id == 'PUB016':
        l = state.setdefault('l', 3)
        seq = state.setdefault('seq', [2, 3, 5, 0, 0, 0, 0, 0])
        inp = {
            'processLength': l,
            'processSequence': list(seq),
            'sensor1': rng.choice([True, False]),
            'sensor2': rng.choice([True, False]),
            'sensor3': rng.choice([True, False]),
            'sensor4': rng.choice([True, False]),
            'sensor5': rng.choice([True, False]),
            'station1Start': rng.choice([True, False]),
            'station2Complete': rng.choice([True, False]),
            'station3Complete': rng.choice([True, False]),
            'station4Complete': rng.choice([True, False]),
        }
    elif task_id == 'PUB017':
        op = rng.choice(['none', 'none', 'add', 'del', 'mod', 'qry'])
        rec = {
            'recipeID': rng.randint(1, 8),
            'ingredientType': rng.randint(1, 5),
            'ingredientRatio': round(rng.uniform(0.1, 1.0), 2),
            'productionTemperature': round(rng.uniform(50.0, 120.0), 1),
        }
        inp = {
            'addRecipe': op == 'add',
            'deleteRecipe': op == 'del',
            'modifyRecipe': op == 'mod',
            'queryRecipe': op == 'qry',
            'recipeIn': rec,
            'recipe': {'$binding': 'recipe', 'binding_id': 'default', 'retain_storage': True},
        }
    elif task_id == 'PUB018':
        enq = rng.choice([True, False])
        deq = False if enq else rng.choice([True, False])
        bid = state.setdefault('bid', rng.choice(['A', 'B']))
        inp = {
            'enqueue': enq,
            'dequeue': deq,
            'reset': rng.choice([False, False, False, True]),
            'item': rng.randint(1, 50),
            'buffer': {'$binding': 'buffer', 'binding_id': bid, 'retain_storage': True},
        }
    elif task_id == 'PUB019':
        mode = state.setdefault('mode', rng.choice(['manual', 'single_step', 'single_cycle', 'continuous']))
        inp = {
            'ManualMode': mode == 'manual',
            'SingleStepMode': mode == 'single_step',
            'SingleCycleMode': mode == 'single_cycle',
            'ContinuousMode': mode == 'continuous',
            'EmergencyStop': rng.choice([True, True, True, False]),
            'Start': rng.choice([True, False]),
            'DownButton': rng.choice([True, False]),
            'UpButton': rng.choice([True, False]),
            'LeftButton': rng.choice([True, False]),
            'RightButton': rng.choice([True, False]),
            'GripButton': rng.choice([True, False]),
            'ReleaseButton': rng.choice([True, False]),
            'DownLimitSwitch': rng.choice([True, False]),
            'UpLimitSwitch': rng.choice([True, False]),
            'LeftLimitSwitch': rng.choice([True, False]),
            'RightLimitSwitch': rng.choice([True, False]),
            'GripLimitSwitch': rng.choice([True, False]),
            'ReleaseLimitSwitch': rng.choice([True, False]),
        }
    elif task_id == 'PUB020':
        inp = {
            'Mode': rng.choice([True, False]),
            'ForwardButton': rng.choice([True, False]),
            'ReverseButton': rng.choice([True, False]),
            'SensorFeed': rng.choice([True, False]),
            'SensorWash': rng.choice([True, False]),
            'SensorWeight': rng.choice([True, False]),
            'SensorFiring': rng.choice([True, False]),
            'SensorOutput': rng.choice([True, False]),
            'washComplete': rng.choice([True, False]),
            'weightComplete': rng.choice([True, False]),
            'weight': round(rng.uniform(80.0, 220.0), 1),
            'firingComplete': rng.choice([True, False]),
        }
    else:
        task_obj = state['task_obj']
        inp = {}
        for f in task_obj.get('interface', []):
            if f.get('direction') in ('INPUT', 'IN_OUT'):
                t_type = f.get('type')
                if t_type == 'BOOL':
                    inp[f['name']] = rng.choice([True, False])
                elif t_type in ('USINT', 'INT', 'DINT', 'UINT', 'UDINT'):
                    inp[f['name']] = rng.randint(1, 10)
                else:
                    inp[f['name']] = round(rng.uniform(0.0, 100.0), 2)
    return inp, dt_ms


def generate_random_cases(
    task: dict,
    seed: int = 20261110,
    num_cases: int | None = None,
    steps_per_case: int | None = None,
) -> list[dict]:
    """Generate seed-deterministic random differential test cases verified against ScanContract."""
    tid = task['id']
    rng = random.Random(f"{seed}:{tid}")
    is_timed = tid in TIMED_TASKS

    if num_cases is None:
        num_cases = 1 if is_timed else 4
    if steps_per_case is None:
        steps_per_case = 12 if is_timed else 24

    cases: list[dict] = []
    for c in range(num_cases):
        case_id = f"{tid}.R{c + 1}"
        state: dict[str, Any] = {'task_obj': task}
        contract = ScanContract(tid)
        steps: list[dict] = []

        for _ in range(steps_per_case):
            inp, dt = _generate_step_input(tid, rng, state)
            out = contract.step(inp, dt)
            step: dict[str, Any] = {
                'inputs': inp,
                'expected': out,
                'outputs': out,
            }
            if dt is not None:
                step['dt_ms'] = dt
            steps.append(step)

        # Verifies the generated cases pass check_contract_trace
        res = check_contract_trace(tid, steps)
        if res.get('status') != 'NO_VIOLATION_IN_OBSERVED_TRACE':
            raise AssertionError(f"Generated case {case_id} failed contract verification: {res.get('violations')}")

        cases.append({
            'id': case_id,
            'name': f"random_case_{c + 1}",
            'steps': steps,
        })

    return cases
