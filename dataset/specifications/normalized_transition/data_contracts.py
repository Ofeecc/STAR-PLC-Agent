"""Independent public-task input/history contracts for scalar data processing."""
import math
import struct

SUPPORTED_DATA = {'PUB002', 'PUB003', 'PUB009', 'PUB014', 'PUB017', 'PUB018'}

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
        self.recipes = [
            {'recipeID': 0, 'ingredientType': 0, 'ingredientRatio': 0.0, 'productionTemperature': 0.0}
            for _ in range(10)
        ]
        self.last_query = {
            'recipeID': 0, 'ingredientType': 0, 'ingredientRatio': 0.0, 'productionTemperature': 0.0
        }
        self.prev_add = False
        self.prev_delete = False
        self.prev_modify = False
        self.prev_query = False
        self.recipes_initialized = False
        self.queue = []
        self.prev_enq = False
        self.prev_deq = False

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
            for req_key in ('cyclicExecution', 'trigger', 'reset'):
                if type(i[req_key]) is not bool:
                    raise ValueError(f'PUB009 requires Boolean {req_key}')
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
        if self.task_id == 'PUB017':
            if not self.recipes_initialized and isinstance(i.get('recipe'), list):
                self.recipes = [
                    {'recipeID': int(r.get('recipeID', 0)),
                     'ingredientType': int(r.get('ingredientType', 0)),
                     'ingredientRatio': real32(r.get('ingredientRatio', 0.0)),
                     'productionTemperature': real32(r.get('productionTemperature', 0.0))}
                    for r in i['recipe']
                ]
                self.recipes_initialized = True

            for req_key in ('addRecipe', 'deleteRecipe', 'modifyRecipe', 'queryRecipe'):
                if type(i.get(req_key)) is not bool:
                    raise ValueError(f'PUB017 requires Boolean {req_key}')

            add_req = i['addRecipe']
            del_req = i['deleteRecipe']
            mod_req = i['modifyRecipe']
            qry_req = i['queryRecipe']

            add_edge = add_req and not self.prev_add
            del_edge = del_req and not self.prev_delete
            mod_edge = mod_req and not self.prev_modify
            qry_edge = qry_req and not self.prev_query

            if sum((add_edge, del_edge, mod_edge, qry_edge)) > 1:
                raise ValueError('PUB017 forbids multiple simultaneous request rising edges')

            self.prev_add = add_req
            self.prev_delete = del_req
            self.prev_modify = mod_req
            self.prev_query = qry_req

            recipe_added = False
            recipe_deleted = False
            recipe_modified = False
            error = False
            status = 0

            rec_in = i.get('recipeIn') or {}
            tid = rec_in.get('recipeID', 0)
            ing_type = rec_in.get('ingredientType', 0)
            if type(tid) is not int or not -32768 <= tid <= 32767:
                raise ValueError('PUB017 recipeID must be INT (-32768..32767)')
            if type(ing_type) is not int or not -32768 <= ing_type <= 32767:
                raise ValueError('PUB017 ingredientType must be INT (-32768..32767)')
            real32(rec_in.get('ingredientRatio', 0.0))
            real32(rec_in.get('productionTemperature', 0.0))

            if qry_edge:
                match = None
                if tid != 0:
                    for r in self.recipes:
                        if r['recipeID'] == tid:
                            match = r
                            break
                if match is not None:
                    self.last_query = dict(match)
                    error = False
                    status = 0
                else:
                    error = True
                    status = 0x8001
            elif add_edge:
                if tid == 0:
                    raise ValueError('PUB017 addRecipe requires non-zero recipeID')
                dup = any(r['recipeID'] == tid for r in self.recipes)
                if dup:
                    error = True
                    status = 0x8002
                else:
                    empty_idx = next((idx for idx, r in enumerate(self.recipes) if r['recipeID'] == 0), None)
                    if empty_idx is None:
                        error = True
                        status = 0x8003
                    else:
                        self.recipes[empty_idx] = {
                            'recipeID': tid,
                            'ingredientType': ing_type,
                            'ingredientRatio': real32(rec_in.get('ingredientRatio', 0.0)),
                            'productionTemperature': real32(rec_in.get('productionTemperature', 0.0)),
                        }
                        recipe_added = True
                        error = False
                        status = 0
            elif del_edge:
                match_idx = next((idx for idx, r in enumerate(self.recipes) if r['recipeID'] == tid and tid != 0), None)
                if match_idx is None:
                    error = True
                    status = 0x8004
                else:
                    self.recipes[match_idx]['recipeID'] = 0
                    recipe_deleted = True
                    error = False
                    status = 0
            elif mod_edge:
                match_idx = next((idx for idx, r in enumerate(self.recipes) if r['recipeID'] == tid and tid != 0), None)
                if match_idx is None:
                    error = True
                    status = 0x8005
                else:
                    self.recipes[match_idx] = {
                        'recipeID': tid,
                        'ingredientType': rec_in.get('ingredientType', 0),
                        'ingredientRatio': real32(rec_in.get('ingredientRatio', 0.0)),
                        'productionTemperature': real32(rec_in.get('productionTemperature', 0.0)),
                    }
                    recipe_modified = True
                    error = False
                    status = 0

            if isinstance(i.get('recipe'), list):
                for idx in range(min(len(i['recipe']), len(self.recipes))):
                    if isinstance(i['recipe'][idx], dict):
                        i['recipe'][idx].update(self.recipes[idx])

            return dict(
                recipeAdded=recipe_added,
                recipeDeleted=recipe_deleted,
                recipeModified=recipe_modified,
                recipeQueryResult=dict(self.last_query),
                error=error,
                status=status,
            )
        if self.task_id == 'PUB018':
            buf = i.get('buffer')
            bid = None
            if isinstance(buf, dict) and '$binding' in buf:
                bid = buf.get('binding_id', 'default')
                if bid == 'A':
                    capacity = 2
                elif bid == 'B':
                    capacity = 3
                else:
                    capacity = buf.get('capacity')
            elif isinstance(buf, list):
                capacity = len(buf)
            else:
                raise ValueError('PUB018 requires buffer list or declared binding')
            if type(capacity) is not int or capacity <= 0:
                raise ValueError('PUB018 buffer capacity must be a positive integer')

            for req_key in ('enqueue', 'dequeue', 'reset'):
                if type(i.get(req_key)) is not bool:
                    raise ValueError(f'PUB018 requires Boolean {req_key}')
            enq_req = i['enqueue']
            deq_req = i['dequeue']
            reset_req = i['reset']

            enq_edge = enq_req and not self.prev_enq
            deq_edge = deq_req and not self.prev_deq
            self.prev_enq = enq_req
            self.prev_deq = deq_req

            if not reset_req and enq_edge and deq_edge:
                raise ValueError('PUB018 forbids simultaneous enqueue and dequeue rising edges without reset')

            current_item = i['item']
            if bid == 'A':
                if type(current_item) is not int or not -2**31 <= current_item <= 2**31 - 1:
                    raise ValueError('PUB018 binding A requires DINT item')
            elif bid == 'B':
                if type(current_item) is not bool:
                    raise ValueError('PUB018 binding B requires BOOL item')
            status = 0

            if reset_req:
                self.queue.clear()
                status = 0
            elif enq_edge:
                if len(self.queue) >= capacity:
                    status = 0x8002
                else:
                    self.queue.append(current_item)
                    status = 0
            elif deq_edge:
                if len(self.queue) == 0:
                    status = 0x8001
                else:
                    current_item = self.queue.pop(0)
                    status = 0
            else:
                status = 0

            return dict(elementCount=len(self.queue), status=status, item=current_item)
        raise ValueError('Unsupported data contract')
