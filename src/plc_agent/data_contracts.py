"""Independent public-task input/history contracts for scalar data processing."""
import math
import struct

SUPPORTED_DATA = {'PUB002', 'PUB003', 'PUB009', 'PUB014'}

def finite(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError('Expected finite numeric input')
    return value

def real32(value):
    try:
        result = struct.unpack('<f', struct.pack('<f', finite(value)))[0]
    except (OverflowError, struct.error) as exc:
        raise ValueError('REAL overflow outside contract') from exc
    return finite(result)

class DataContract:
    def __init__(self, task_id):
        self.task_id = task_id
        self.previous = 0
        self.high = self.low = False
        self.trigger = False
        self.window = None
        self.history = []
        self.average = 0.0
        self.reached = False

    def step(self, i):
        if self.task_id == 'PUB002':
            value = i['value']
            if type(value) is not int or not 0 <= value <= 0xffffffff:
                raise ValueError('DWORD outside unsigned 32-bit domain')
            rise = value & (~self.previous & 0xffffffff)
            fall = self.previous & (~value & 0xffffffff)
            self.previous = value
            return dict(hasChanged=bool(rise or fall), hasRisingEdges=bool(rise),
                        risingBits=rise, noOfRisingBits=rise.bit_count(),
                        hasFallingEdges=bool(fall), fallingBits=fall, noOfFallingBits=fall.bit_count())
        if self.task_id == 'PUB003':
            value, hi, lo, width = [real32(i[k]) for k in ('Value','hiLevel','loLevel','hystWindow')]
            if width < 0:
                raise ValueError('Negative hysteresis is outside declared domain')
            status = 0x8001 if lo >= hi else (0x8002 if width >= real32(hi-lo) else 0)
            if not status:
                if value > hi: self.high = True
                elif value < real32(hi-width): self.high = False
                if value < lo: self.low = True
                elif value > real32(lo+width): self.low = False
            return dict(hiAlarm=self.high, loAlarm=self.low, error=bool(status), status=status)
        if self.task_id == 'PUB009':
            size = i['windowSize']
            if type(size) is not int or not -32768 <= size <= 32767:
                raise ValueError('windowSize outside INT domain')
            value = finite(i['value'])
            rise = i['trigger'] and not self.trigger
            self.trigger = i['trigger']
            error = not 1 <= size <= 100
            if not error:
                if size != self.window or i['reset']:
                    self.history = []
                self.window = size
                if not i['reset'] and (i['cyclicExecution'] or rise):
                    self.history.append(value)
                    self.history = self.history[-size:]
                self.average = finite(sum(self.history) / len(self.history)) if self.history else 0.0
                self.reached = len(self.history) == size
            return dict(average=self.average, windowSizeReached=self.reached,
                        error=error, status=0x8200 if error else 0)
        if self.task_id == 'PUB014':
            text = i['ipText']
            if not isinstance(text, str): raise ValueError('Expected PLC STRING')
            text = text.split('\0', 1)[0]
            if len(text.encode('utf-8')) > 254:
                raise ValueError('Input exceeds STRING(254) capacity')
            parts = text.split('.')
            if len(parts) != 4: return {'ipValue': 0}
            value = 0
            for part in parts:
                if not part or any(c < '0' or c > '9' for c in part): return {'ipValue': 0}
                octet = 0
                for c in part:
                    octet = octet * 10 + ord(c) - ord('0')
                    if octet > 255: return {'ipValue': 0}
                value = value * 256 + octet
            return {'ipValue': value}
        raise ValueError('Unsupported data contract')
