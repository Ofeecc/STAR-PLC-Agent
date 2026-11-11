"""Independent finite-trace contracts. Never executes ST or proves infinite LTL."""
import math

from .array_contracts import SUPPORTED_ARRAY, ArrayContract, analog_field_matches
from .data_contracts import SUPPORTED_DATA, DataContract
from .process_contracts import SUPPORTED_PROCESS, ProcessContract
from .reference import ReferenceController
from .timed_contracts import SUPPORTED_TIMED, TimedContract, duration_ns

SUPPORTED = {f'SELF{i:03d}' for i in range(1, 13)} | {'PUB001', 'PUB010', 'PUB011'} | SUPPORTED_DATA | SUPPORTED_TIMED | SUPPORTED_PROCESS | SUPPORTED_ARRAY


class ScanContract:
    def __init__(self, task_id):
        if task_id not in SUPPORTED:
            raise ValueError('Unsupported scan contract: ' + task_id)
        self.task_id = task_id
        self.array_contract = ArrayContract(task_id) if task_id in SUPPORTED_ARRAY else None
        self.process_contract = ProcessContract(task_id) if task_id in SUPPORTED_PROCESS else None
        self.timed_contract = TimedContract(task_id) if task_id in SUPPORTED_TIMED else None
        self.data_contract = DataContract(task_id) if task_id in SUPPORTED_DATA else None
        self.reference = ReferenceController(task_id) if task_id.startswith('SELF') else None
        self.phase = 0
        self.previous_mode = None
        self.clock = 0.0
        self.heat_start = None
        self.protection_start = None
        self.demand = False

    def step(self, inputs, dt_ms=None):
        i = inputs
        if self.array_contract:return self.array_contract.step(i)
        if self.process_contract:
            return self.process_contract.step(i)
        if self.timed_contract:
            return self.timed_contract.step(i,dt_ms)
        if self.data_contract:
            return self.data_contract.step(i)
        if self.reference:
            return self.reference.step(i)
        if self.task_id == 'PUB001':
            events = ['bottleSensor', 'cleaningConfirmButton', 'fillingConfirmButton',
                      'cappingConfirmButton', 'packingConfirmButton', 'finishedButton']
            if i[events[self.phase]]:
                self.phase = (self.phase + 1) % 6
            outputs = ['Pump_Motor', 'Filling_Valve', 'Capping_Machine', 'Packing_Machine', 'Completion_Light']
            return {name: self.phase == j for j, name in enumerate(outputs, 1)}
        if self.task_id == 'PUB011':
            # WAIT_A, MOVE_AB, WAIT_B, MOVE_BC, WAIT_C, DONE.
            if not i['Mode']:
                self.phase = 0
                return dict(MotorForward=i['ForwardButton'] and not i['ReverseButton'],
                            MotorReverse=i['ReverseButton'] and not i['ForwardButton'], CompletionLight=False)
            if self.phase == 0 and i['SensorA'] and i['ButtonA']:
                self.phase = 1
            elif self.phase == 1 and i['SensorB']:
                self.phase = 2
            elif self.phase == 2 and i['SensorB'] and i['ButtonB']:
                self.phase = 3
            elif self.phase == 3 and i['SensorC']:
                self.phase = 4
            elif self.phase == 4 and i['SensorC'] and i['ButtonC']:
                self.phase = 5
            elif self.phase == 5 and not i['SensorC']:
                self.phase = 0
            return dict(MotorForward=self.phase in (1, 3), MotorReverse=False,
                        CompletionLight=self.phase == 5 and i['SensorC'])
        if self.task_id == 'PUB010':
            if isinstance(dt_ms, bool) or not isinstance(dt_ms, (int, float)) or not math.isfinite(dt_ms) or dt_ms < 0:
                raise ValueError('PUB010 requires observed finite nonnegative dt_ms')
            self.clock += dt_ms
            value, target = i['TemperatureSensorInput'], i['SetTemperature']
            if not all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in (value, target)):
                raise ValueError('Temperature inputs must be finite numbers')
            fault = not 0 <= value <= 100
            if value < target:
                self.demand = True
            elif value > target:
                self.demand = False
            # Evaluate elapsed time of the preceding energized interval before output update.
            if self.protection_start is not None:
                if self.clock - self.protection_start >= 3000:
                    self.protection_start = None
            elif self.heat_start is not None and self.clock - self.heat_start >= 5000:
                self.protection_start = self.clock
            heat = not fault and self.demand and self.protection_start is None
            if heat:
                if self.heat_start is None:
                    self.heat_start = self.clock
            else:
                self.heat_start = None
            return dict(CurrentTemperature=value, SetTempDisplay=target, HeaterStatus=heat,
                        OverheatProtection=self.protection_start is not None, HeaterOutput=heat)
        raise AssertionError('Unreachable')


def check_contract_trace(task_id, rows):
    """Check supplied observations; caller independently establishes provenance."""
    from .functional import equal
    if task_id not in SUPPORTED:
        return {'status': 'UNSUPPORTED', 'checked_steps': 0, 'violations': []}
    if not rows:
        return {'status': 'INCOMPLETE', 'checked_steps': 0, 'violations': []}
    monitor = ScanContract(task_id)
    violations = []
    for scan, row in enumerate(rows):
        expected = monitor.step(row['inputs'], row.get('dt_ms'))
        actual = row.get('outputs', {})
        for name, value in expected.items():
            matches = name in actual and equal(actual[name], value)
            if task_id=='PUB008' and name in actual:
                matches=analog_field_matches(name,actual[name],value,row['inputs'])
            if task_id=='PUB007' and name in actual:
                matches=equal(actual[name],value,tolerance=0)
            if name in actual and name in ('PUMP_RUNTIME_ACC','Slab_Runtime_Accumulator'):
                try: matches = duration_ns(actual[name]) == duration_ns(value)
                except ValueError: matches = False
            if not matches:
                violations.append({'scan': scan, 'output': name, 'expected': value,
                                   'observed': actual.get(name), 'missing': name not in actual})
    return {'status': 'VIOLATED' if violations else 'NO_VIOLATION_IN_OBSERVED_TRACE',
            'checked_steps': len(rows), 'violations': violations,
            'scope': 'Finite scan transition contract; not full LTL model checking or runtime provenance verification.'}
