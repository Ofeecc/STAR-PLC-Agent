"""Ordinal-array scan contracts. Physical bounds remain runtime-adapter metadata."""
import math
from copy import deepcopy

from .data_contracts import finite

SUPPORTED_ARRAY={'PUB007','PUB008'}

class ArrayContract:
    def __init__(self,task_id):self.task_id=task_id

    def step(self,i):
        if self.task_id=='PUB007':
            pumps=i['pumpGroup']
            if not isinstance(pumps,list) or len(pumps)!=5:raise ValueError('Exactly five pump records required')
            for p in pumps:
                if type(p['priority']) is not int or not -32768<=p['priority']<=32767:raise ValueError('Pump priority outside INT')
                if type(p['selection']) is not bool or type(p['RunComd']) is not bool:raise ValueError('Pump Boolean field type mismatch')
            result=deepcopy(pumps)
            selected=set(sorted(range(5),key=lambda j:(-pumps[j]['priority'],j))[:3])
            for j,p in enumerate(result):
                if i['stop']:p['RunComd']=False
                elif i['start']:p['RunComd']=j in selected if i['mode'] else p['selection']
            return {'pumpGroup':result}
        if self.task_id=='PUB008':
            raw,channels,count=i['analogValues'],i['channels'],i['count']
            if not isinstance(raw,list) or not isinstance(channels,list) or type(count) is not int or not 0<=count<=min(len(raw),len(channels)):
                raise ValueError('count outside supplied array lengths')
            if any(type(v) is not int or not -32768<=v<=32767 for v in raw):raise ValueError('Analog input outside INT')
            result=deepcopy(channels)
            for j,c in enumerate(result):
                if type(c['enable']) is not bool or type(c['bipolar']) is not bool or type(c['measuringMode']) is not int or not -32768<=c['measuringMode']<=32767:
                    raise ValueError('Analog configuration field type mismatch')
                if 'retVal' in c and (type(c['retVal']) is not int or not 0<=c['retVal']<=0xffff):
                    raise ValueError('Analog retVal outside WORD domain')
                finite(c['hiLIM']);finite(c['loLIM']);finite(c['outputValue'])
                if j>=count or not c['enable']:continue
                hi,lo=finite(c['hiLIM']),finite(c['loLIM']);mode=c['measuringMode']
                if mode not in (0,1,2):c['retVal']=0x8001;continue
                if hi<=lo:c['retVal']=0x8002;continue
                c['retVal']=0
                if mode==0:
                    fraction=(raw[j]+27648)/55296 if c['bipolar'] else raw[j]/27648
                    c['outputValue']=finite(lo+fraction*(hi-lo))
                else:c['outputValue']=raw[j]/(10 if mode==1 else 100)
            return {'analogValues':list(raw),'channels':result}
        raise ValueError('Unsupported array contract')

def analog_field_matches(name,actual,expected,inputs):
    """Tolerance applies only to successfully converted outputValue, not preserved data."""
    from .functional import equal
    if name!='channels':return equal(actual,expected,tolerance=0)
    if not isinstance(actual,list) or len(actual)!=len(expected):return False
    for j,(got,want) in enumerate(zip(actual,expected)):
        if not isinstance(got,dict) or got.keys()!=want.keys():return False
        sampled=inputs['channels'][j]
        converted=j<inputs['count'] and sampled['enable'] and sampled['measuringMode'] in (0,1,2) and sampled['hiLIM']>sampled['loLIM']
        for key,value in want.items():
            if key not in got:return False
            if key=='outputValue' and converted:
                x=got[key]
                if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or not math.isclose(x,value,abs_tol=1e-5,rel_tol=2e-6):return False
            elif not equal(got[key],value,tolerance=0):return False
    return True
