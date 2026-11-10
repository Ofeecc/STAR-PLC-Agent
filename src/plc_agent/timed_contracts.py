"""Sampled-time contracts; supplied timestamps are observations, not a PLC clock."""
from decimal import Decimal
import math
import re

SUPPORTED_TIMED = {'PUB004','PUB005','PUB006','PUB012','PUB013'}
UNITS = {'d':86400000000000,'h':3600000000000,'m':60000000000,
         's':1000000000,'ms':1000000,'us':1000,'ns':1}

def duration_ns(literal):
    if not isinstance(literal,str): raise ValueError('Expected IEC time literal')
    match=re.fullmatch(r'(?:T|TIME|LT|LTIME)#(.+)',literal,re.I)
    if not match: raise ValueError('Invalid time literal')
    body=match[1].lower(); pos=0; total=Decimal(0)
    for part in re.finditer(r'(\d+(?:\.\d+)?)(ms|us|ns|d|h|m|s)',body):
        if part.start()!=pos: raise ValueError('Invalid duration components')
        total+=Decimal(part[1])*UNITS[part[2]];pos=part.end()
    if pos!=len(body) or total!=total.to_integral_value(): raise ValueError('Invalid duration precision')
    return int(total)

def ltime(ns):
    return f'LTIME#{ns//1000000}ms' if ns%1000000==0 else f'LTIME#{ns}ns'

class TimedContract:
    def __init__(self, task_id):
        self.task_id=task_id; self.clock=Decimal(0); self.first=True
        self.since=None; self.debounce=None; self.runtime=0; self.count=0
        self.previous_run=False; self.previous_fault=False; self.history=[0]*5

    def qualified(self, permit, limit):
        if not permit: self.since=None; return False
        if self.since is None: self.since=self.clock
        return self.clock-self.since>=limit

    def step(self,i,dt_ms):
        if isinstance(dt_ms,bool) or not isinstance(dt_ms,(int,float)) or not math.isfinite(dt_ms) or dt_ms<0:
            raise ValueError('Observed finite nonnegative dt_ms required')
        if not self.first:self.clock+=Decimal(str(dt_ms))*1000000
        self.first=False
        if self.task_id in ('PUB004','PUB005'):
            limit=duration_ns(i['DebounceTime'])
            if limit<=0:raise ValueError('DebounceTime must be positive')
            if self.debounce is not None and self.debounce!=limit:raise ValueError('DebounceTime must remain constant per case')
            self.debounce=limit
        if self.task_id in ('PUB004','PUB012'):
            cycle=duration_ns(i['CycleTime'])
            if cycle<=0:raise ValueError('CycleTime must be positive')
        if self.task_id=='PUB004':
            run=self.qualified(i['VISCOSITY_OK'] and i['PASTE_E_STOP_NC'],limit)
            if run:self.runtime+=cycle
            result=dict(VFD_RUN=run,PUMP_RUNTIME_ACC=ltime(self.runtime),PUMP_MAINT_DUE=self.runtime>=500*UNITS['h'])
        elif self.task_id=='PUB005':
            startup=self.clock<5*UNITS['s']
            alarm=self.qualified(not startup and i['Gap_Exceeded'] and i['Weld_E_Stop_NC'],limit)
            result=dict(Operator_Alert=alarm,Weld_Soft_Start_Active=startup)
        elif self.task_id=='PUB006':
            run=self.qualified(i['DO_LOW'] and i['AERATION_E_STOP_NC'],5*UNITS['s'])
            self.count+=int(run and not self.previous_run);self.previous_run=run
            result=dict(BLOWER_RUN=run,AERATION_BLOWER_CYCLE_COUNT=self.count)
        elif self.task_id=='PUB012':
            valid=i['THICKNESS_SIGNAL_VALID'];fault=valid and i['THICKNESS_FAULT']
            if fault and not self.previous_fault:
                self.count+=1;self.since=self.clock
                self.history=[i['FaultTimestamp']]+self.history[:4]
            if not valid:self.since=None
            alarm=valid and (fault or (self.since is not None and self.clock-self.since<500*UNITS['ms']))
            if valid and not fault and i['CUTTING_RUN']:self.runtime+=cycle
            self.previous_fault=fault
            result=dict(THICKNESS_ALARM=bool(alarm),Slab_Fault_Counter=self.count,
                        Slab_Runtime_Accumulator=ltime(self.runtime),Slab_Fault_History=list(self.history))
        elif self.task_id=='PUB013':
            mode=i['HVAC_MODE_SELECTOR'];occupied=i['OCCUPANCY_DETECTED']
            if type(mode) is not int or mode not in range(4):raise ValueError('Mode outside 0..3 domain')
            fan=self.qualified(occupied and mode!=3,30*UNITS['s'])
            adjust=4 if mode==3 else (0 if occupied else ((3 if i['ENERGY_SAVING_MODE'] else 2) if mode==0 else (1 if mode==1 else 4)))
            result=dict(SUPPLY_FAN_RUN=fan,TEMP_SETPOINT_ADJUST=adjust)
        else:raise ValueError('Unsupported timed contract')
        if self.count>65535 or self.runtime>2**63-1:raise ValueError('Counter/runtime exceeds bounded contract domain')
        return result
