"""Author public tasks 1..10 from the supplied unmodified English question text.

This script writes specifications and EXPECTED sequences, never execution results.
Run from PLC_Agent_Final with a Python 3 standard-library interpreter.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / '大作业题库json' / '大作业题库json' / '大作业题库.json'
bank = json.loads(SOURCE.read_text(encoding='utf-8-sig'))
source_tasks = bank['easy'] + bank['medium'][:4]
SCAN = ('At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, '
        'outputs O[k] are observed after execution, and q[k+1] is the updated state. '
        'Each test creates a fresh FB instance before step 0. An initialized instance '
        'has not yet executed a scan. Timer elapsed time is zero on the first '
        'eligible sampled invocation; dt_ms is elapsed wall time since the previous '
        'invocation, not automatically a synthetic input to the FB. No unobserved '
        'past input stability is assumed. All sequences here are expected values.')


def interface(text):
    fields = []
    for line in text.splitlines():
        cells = [x.strip().strip('`') for x in line.strip().strip('|').split('|')]
        if len(cells) != 4 or cells[0] not in ('Input', 'Output', 'Input/Output'):
            continue
        fields.append(dict(direction={'Input':'INPUT','Output':'OUTPUT','Input/Output':'IN_OUT'}[cells[0]],
                           name=cells[1], type=cells[2], description=cells[3]))
    return fields


def base(n):
    raw = source_tasks[n-1]['en']
    return dict(schema_version=1, id=f'PUB{n:03d}', kind='public',
                title=raw.splitlines()[0].lstrip('# '), difficulty='easy' if n<=6 else 'medium',
                provenance=dict(source_type='official_course_question_bank',
                                source_file='大作业题库json/大作业题库json/大作业题库.json',
                                source_index={'group':'easy' if n<=6 else 'medium', 'index_1based':n if n<=6 else n-6},
                                adaptation='Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.',
                                rationale='Teacher-supplied PLC task; retains the specified interface and control scenario.',
                                review='Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC.'),
                requirements=raw, scenario=raw.split('## Requirements\n\n',1)[1].split('\n')[0],
                interface=interface(raw), initial_conditions={}, scan_semantics=SCAN,
                safety_priority=[], assumptions=[], ltl=[], atomic_propositions={}, tests=[])


def prop(t, formula, explanation):
    t['ltl'].append(dict(id=f"P{len(t['ltl'])+1}", formula=formula, explanation=explanation))


def test(t, purpose, steps, defaults=None, notes=None):
    defaults = defaults or {v['name']: False for v in t['interface'] if v['direction']=='INPUT' and v['type']=='BOOL'}
    trace=[]
    for inp, out, *rest in steps:
        trace.append(dict(inputs={**defaults, **inp}, expected=out, **(dict(dt_ms=rest[0]) if rest else {})))
    entry=dict(id=f"T{len(t['tests'])+1}",purpose=purpose,steps=trace)
    if notes: entry['notes']=notes
    t['tests'].append(entry)


tasks=[]
t=base(1)
t['initial_conditions']={'phase':0,'Pump_Motor':False,'Filling_Valve':False,'Capping_Machine':False,'Packing_Machine':False,'Completion_Light':False}
t['assumptions']=['The five process actuators are mutually exclusive; each completed phase switches off its actuator when the next starts.', 'One phase transition at most is allowed per scan. Confirmation signals outside their active phase are ignored.', 'Confirmation inputs are level sampled. A held confirmation can complete its relevant phase on a later scan, but cannot skip several phases in one scan.', 'finishedButton resets only the completed phase. A bottle still present can start a new cleaning cycle on the following idle scan.']
t['safety_priority']=['Active phase restricts which confirmation can be accepted.', 'Only the current phase actuator may run.']
t['atomic_propositions']={'phase':'Ghost pre-scan state 0 idle, 1 cleaning, 2 filling, 3 capping, 4 packing, 5 complete; phase is updated once per scan.', 'oneHotOutputs':'At most one of Pump_Motor, Filling_Valve, Capping_Machine, Packing_Machine, Completion_Light is TRUE.', 'init':'Before the first scan, phase=0 and all outputs FALSE.', 'all variable names':'The identically named sampled input or end-of-scan output in interface.'}
prop(t,'init', 'A fresh instance is idle with outputs off before first execution.')
prop(t,'G(oneHotOutputs)', 'No two processing stages are energized together.')
prop(t,'G((phase=0 & bottleSensor) -> (Pump_Motor & X(phase=1)))','Bottle detection starts cleaning in the same scan.')
for phase,button,out in [(1,'cleaningConfirmButton','Filling_Valve'),(2,'fillingConfirmButton','Capping_Machine'),(3,'cappingConfirmButton','Packing_Machine'),(4,'packingConfirmButton','Completion_Light')]:
    prop(t,f'G((phase={phase} & {button}) -> ({out} & X(phase={phase+1})))','A phase-specific confirmation advances exactly one stage.')
prop(t,'G((phase=5 & !finishedButton) -> (Completion_Light & X(phase=5)))','Completion persists until pickup is confirmed.')
prop(t,'G((phase=5 & finishedButton) -> (!Completion_Light & X(phase=0)))','Pickup confirmation rearms the line.')
prop(t,'G((phase=1 & G((phase=1) -> F(cleaningConfirmButton)) & G((phase=2) -> F(fillingConfirmButton)) & G((phase=3) -> F(cappingConfirmButton)) & G((phase=4) -> F(packingConfirmButton))) -> F(Completion_Light))', 'Conditional progress: from cleaning, if every active phase eventually receives its matching confirmation, completion eventually occurs.')
t['assumptions'].append('For the progress property, future confirmations are ordered and sustained until their matching phase accepts them. Unordered one-scan pulses do not imply completion.')
outs=['Pump_Motor','Filling_Valve','Capping_Machine','Packing_Machine','Completion_Light']
o=lambda active=None:{x:x==active for x in outs}
test(t,'Full bottle cycle and stable completion', [({},o()),({'bottleSensor':True},o(outs[0])),({},o(outs[0])),({'cleaningConfirmButton':True},o(outs[1])),({'fillingConfirmButton':True},o(outs[2])),({'cappingConfirmButton':True},o(outs[3])),({'packingConfirmButton':True},o(outs[4])),({},o(outs[4])),({'finishedButton':True},o()),({},o())])
test(t,'Out-of-order confirmations cannot skip phases', [({'fillingConfirmButton':True,'packingConfirmButton':True},o()),({'bottleSensor':True,'cleaningConfirmButton':True,'fillingConfirmButton':True},o(outs[0])),({'fillingConfirmButton':True},o(outs[0])),({'finishedButton':True},o(outs[0])),({'cleaningConfirmButton':True,'fillingConfirmButton':True},o(outs[1])),({'fillingConfirmButton':True},o(outs[2]))])
tasks.append(t)

t=base(2)
t['initial_conditions']={'previousValue':0,'risingBits':0,'fallingBits':0,'noOfRisingBits':0,'noOfFallingBits':0,'hasChanged':False,'hasRisingEdges':False,'hasFallingEdges':False}
t['assumptions']=['The previous DWORD is initialized to DWORD#0. Therefore nonzero bits on the first scan count as rising edges.', 'Bitwise complement is restricted to 32 bits; counts range from 0 through 32.']
t['safety_priority']=['Previous value is updated after calculating both edge masks.']
t['atomic_propositions']={'prev':'Ghost pre-scan previous DWORD; initialized to zero.', 'risingBits':'End-of-scan mask value & NOT prev, restricted to DWORD width.', 'fallingBits':'End-of-scan mask prev & NOT value, restricted to DWORD width.', 'popcount':'Number of set bits in the unsigned 32-bit argument.', 'other interface names':'Identically named sampled inputs or observed outputs.'}
prop(t,'G(risingBits = (value AND NOT prev))','The rising mask identifies only 0-to-1 bits.')
prop(t,'G(fallingBits = (prev AND NOT value))','The falling mask identifies only 1-to-0 bits.')
prop(t,'G((risingBits AND fallingBits)=0)','A bit cannot rise and fall in one scan.')
prop(t,'G((noOfRisingBits=popcount(risingBits)) & (noOfFallingBits=popcount(fallingBits)))','Both counts equal their mask population.')
prop(t,'G((hasRisingEdges <-> risingBits<>0) & (hasFallingEdges <-> fallingBits<>0) & (hasChanged <-> value<>prev))','Flags match masks and value changes.')
prop(t,'G(X(prev)=value)','The current value is the next scan history.')
def edge(v,p):
    r=v&(~p&0xffffffff); f=p&(~v&0xffffffff)
    return dict(hasChanged=v!=p,hasRisingEdges=bool(r),risingBits=r,noOfRisingBits=r.bit_count(),hasFallingEdges=bool(f),fallingBits=f,noOfFallingBits=f.bit_count())
vals=[0,1,1,3,2,0,0xffffffff,0,0x80000000,0x7fffffff]
test(t,'No change, mixed edges, full width and bit 31', [({'value':v},edge(v,vals[i-1] if i else 0)) for i,v in enumerate(vals)],defaults={})
test(t,'First nonzero invocation is compared with initialized zero', [({'value':0xffffffff},edge(0xffffffff,0)),({'value':0xffffffff},edge(0xffffffff,0xffffffff))],defaults={})
tasks.append(t)

t=base(3)
t['initial_conditions']={'hiAlarm':False,'loAlarm':False,'error':False,'status':0}
t['assumptions']=['Threshold comparisons are strict as written. Equality with trigger or release thresholds retains the previous alarm value.', 'Invalid configuration returns early, preserving alarm outputs. error and status are recalculated each scan; valid configuration clears them.', 'loLevel>=hiLevel takes priority over the hysteresis-width error. hystWindow is assumed nonnegative; negative values are outside the defined input domain.']
t['safety_priority']=['Invalid range is diagnosed before invalid hysteresis width.', 'No alarm update is allowed in an invalid-configuration scan.']
t['atomic_propositions']={'badRange':'loLevel >= hiLevel', 'badWindow':'hystWindow >= hiLevel-loLevel', 'valid':'!badRange & !badWindow & hystWindow>=0', 'hiPrev':'Pre-scan retained hiAlarm', 'loPrev':'Pre-scan retained loAlarm', 'sameAlarms':'hiAlarm=hiPrev & loAlarm=loPrev', 'interface names':'Identically named sampled input or observed output.'}
prop(t,'G(badRange -> (error & status=16#8001 & sameAlarms))','Invalid limits take priority and leave alarms unchanged.')
prop(t,'G((!badRange & badWindow) -> (error & status=16#8002 & sameAlarms))','The hysteresis range must be smaller than the limit separation.')
prop(t,'G(valid -> (!error & status=0))','Valid input clears transient configuration errors.')
prop(t,'G((valid & Value>hiLevel) -> hiAlarm)','A high excursion activates the high alarm.')
prop(t,'G((valid & Value<hiLevel-hystWindow) -> !hiAlarm)','Below the strict release boundary, high alarm clears.')
prop(t,'G((valid & hiLevel-hystWindow<=Value & Value<=hiLevel) -> (hiAlarm=hiPrev))','The high hysteresis band retains history.')
prop(t,'G((valid & Value<loLevel) -> loAlarm)','A low excursion activates the low alarm.')
prop(t,'G((valid & Value>loLevel+hystWindow) -> !loAlarm)','Above the strict low release boundary, low alarm clears.')
prop(t,'G((valid & loLevel<=Value & Value<=loLevel+hystWindow) -> (loAlarm=loPrev))','The low hysteresis band retains history.')
defaults=dict(Value=50.0,hiLevel=80.0,loLevel=20.0,hystWindow=5.0)
def alarm(h=False,l=False,e=False,s=0): return dict(hiAlarm=h,loAlarm=l,error=e,status=s)
test(t,'Strict high and low hysteresis boundaries', [({},alarm()),({'Value':80.0},alarm()),({'Value':81.0},alarm(True)),({'Value':75.0},alarm(True)),({'Value':74.0},alarm()),({'Value':20.0},alarm()),({'Value':19.0},alarm(False,True)),({'Value':25.0},alarm(False,True)),({'Value':26.0},alarm())],defaults)
test(t,'Configuration priority, output retention and recovery', [({'Value':90.0},alarm(True)),({'loLevel':80.0,'hystWindow':80.0},alarm(True,False,True,32769)),({'hystWindow':60.0},alarm(True,False,True,32770)),({},alarm())],defaults)
tasks.append(t)

t=base(4)
t['initial_conditions']={'VFD_RUN':False,'PUMP_RUNTIME_ACC':'LTIME#0ns','PUMP_MAINT_DUE':False,'debounceElapsed_ms':0}
t['assumptions']=['DebounceTime and CycleTime are strictly positive. Inputs are held stable between timed test samples.', 'Debouncing follows a TON-style clock: elapsed is zero on the first permitted TRUE sample and becomes valid at elapsed>=DebounceTime.', 'An E-stop resets debounce validity as well as incomplete timing, so re-enabling requires a full new qualification.', 'At each invocation, add the supplied CycleTime to the LTIME accumulator iff the end-of-scan VFD_RUN is TRUE. Do not use TIME for the 500-hour accumulator.', 'PUMP_MAINT_DUE is a level comparison accumulated runtime>=500h and has no reset input. Its threshold case is specified but is not a short practical runtime test.']
t['safety_priority']=['Emergency stop or raw viscosity FALSE clears the run permission immediately.', 'Maintenance does not override run permission.']
t['atomic_propositions']={'permit':'VISCOSITY_OK & PASTE_E_STOP_NC', 'qualified':'Continuous permitted raw TRUE duration >= DebounceTime, with first sampled TRUE at elapsed zero.', 'accPrev':'Pre-scan PUMP_RUNTIME_ACC as nonnegative LTIME.', 'accNext':'End-of-scan PUMP_RUNTIME_ACC.', 'interface names':'Identically named sampled input or end-of-scan output.'}
prop(t,'G(VFD_RUN <-> (permit & qualified))','The run output follows the qualified permissive.')
prop(t,'G(!permit -> !VFD_RUN)','Raw loss or E-stop stops immediately.')
prop(t,'G((!permit) -> X(!qualified))','A lost permissive clears qualification history; future qualification must be rebuilt.')
prop(t,'G(VFD_RUN -> accNext=accPrev+TIME_TO_LTIME(CycleTime))','Only enabled intervals are accumulated in a long time type.')
prop(t,'G(!VFD_RUN -> accNext=accPrev)','Stopping retains accumulated service time.')
prop(t,'G(PUMP_MAINT_DUE <-> accNext>=LTIME#500h)','Maintenance threshold is 500 hours.')
prop(t,'G((G(permit) & DebounceTime>TIME#0ms) -> F(VFD_RUN))','A continuously permitted demand eventually starts under advancing time.')
d=dict(VISCOSITY_OK=False,PASTE_E_STOP_NC=True,DebounceTime='T#2s',CycleTime='T#1s')
def pump(run=False,acc=0,due=False): return dict(VFD_RUN=run,PUMP_RUNTIME_ACC=f'LTIME#{acc}ms',PUMP_MAINT_DUE=due)
test(t,'Qualification boundary, accumulation, stop retention and restart', [({},pump(),0),({'VISCOSITY_OK':True},pump(),1000),({'VISCOSITY_OK':True},pump(),1000),({'VISCOSITY_OK':True},pump(True,1000),1000),({'VISCOSITY_OK':True},pump(True,2000),1000),({},pump(False,2000),1000),({'VISCOSITY_OK':True},pump(False,2000),1000),({'VISCOSITY_OK':True},pump(False,2000),1000),({'VISCOSITY_OK':True},pump(True,3000),1000)],d)
test(t,'E-stop clears incomplete debounce and completed permission', [({'VISCOSITY_OK':True},pump(),0),({'VISCOSITY_OK':True},pump(),1000),({'VISCOSITY_OK':True,'PASTE_E_STOP_NC':False},pump(),1000),({'VISCOSITY_OK':True},pump(),1000),({'VISCOSITY_OK':True},pump(),1000),({'VISCOSITY_OK':True},pump(True,1000),1000),({'VISCOSITY_OK':True,'PASTE_E_STOP_NC':False},pump(False,1000),1000)],d)
test(t,'Long-duration maintenance arithmetic boundary', [({'VISCOSITY_OK':True},pump(),0),({'VISCOSITY_OK':True,'CycleTime':'T#500h'},pump(True,1800000000,True),1800000000),({'VISCOSITY_OK':True},pump(True,1800001000,True),1000),({},pump(False,1800001000,True),1000)],d,notes='This expected trace contains a genuine 500-hour elapsed interval matching CycleTime; it is not a short physical-runtime test or evidence of 500 hours of operation. Automated execution needs a separately validated virtual-clock mechanism, otherwise perform only as a long-duration test. TIME#500h is 1.8e9 ms and fits unsigned 32-bit TIME.')
tasks.append(t)

t=base(5)
t['initial_conditions']={'Operator_Alert':False,'Weld_Soft_Start_Active':True,'startupElapsed_ms':0,'gapElapsed_ms':0}
t['assumptions']=['Power-up inhibition uses a monotonically advancing 5-second timer that starts on the first FB invocation and continues through E-stop.', 'Weld_Soft_Start_Active reports startup inhibition even during E-stop. E-stop overrides the alert and resets gap timing but does not restart power-up inhibition.', 'At exactly 5 seconds startup inhibition clears. That scan is the first eligible gap sample, with gap elapsed zero; there is no credited debounce time during inhibition.', 'DebounceTime is positive. Alert clears and debounce resets immediately on raw gap FALSE or E-stop.']
t['safety_priority']=['E-stop immediately suppresses the alarm in every phase.', 'Initialization suppresses alarm and prevents gap timing.']
t['atomic_propositions']={'startup':'Elapsed time since the first invocation is less than 5 seconds.', 'gapQualified':'Gap_Exceeded has remained TRUE with Weld_E_Stop_NC TRUE and !startup for at least DebounceTime, measured from first eligible invocation.', 'interface names':'Identically named sampled input or observed output.'}
prop(t,'G(Weld_Soft_Start_Active <-> startup)','Soft-start output means only the startup monitoring inhibition interval.')
prop(t,'G((startup | !Weld_E_Stop_NC | !Gap_Exceeded) -> !Operator_Alert)','Startup, E-stop or no gap forces the alarm off.')
prop(t,'G(Operator_Alert <-> (!startup & Weld_E_Stop_NC & Gap_Exceeded & gapQualified))','Alarm requires post-startup continuous qualified gap.')
prop(t,'G((startup | !Weld_E_Stop_NC | !Gap_Exceeded) -> X(!gapQualified))','Each suppressing condition clears or blocks gap qualification.')
prop(t,'G((G(Weld_E_Stop_NC & Gap_Exceeded)) -> F(Operator_Alert))','Persistent gap eventually alarms after startup and debounce, assuming advancing time.')
d=dict(Gap_Exceeded=False,Weld_E_Stop_NC=True,DebounceTime='T#2s')
def weld(alert=False,start=True):return dict(Operator_Alert=alert,Weld_Soft_Start_Active=start)
test(t,'Initialization excludes gap timing and debounce starts at 5s', [({'Gap_Exceeded':True},weld(),0),({'Gap_Exceeded':True},weld(),4000),({'Gap_Exceeded':True},weld(False,False),1000),({'Gap_Exceeded':True},weld(False,False),1000),({'Gap_Exceeded':True},weld(True,False),1000),({},weld(False,False),100)],d)
test(t,'E-stop suppresses startup and normal alerts without restarting inhibition', [({'Gap_Exceeded':True,'Weld_E_Stop_NC':False},weld(),0),({'Gap_Exceeded':True,'Weld_E_Stop_NC':False},weld(False,False),5000),({'Gap_Exceeded':True},weld(False,False),100),({'Gap_Exceeded':True},weld(True,False),2000),({'Gap_Exceeded':True,'Weld_E_Stop_NC':False},weld(False,False),100),({'Gap_Exceeded':True},weld(False,False),100),({'Gap_Exceeded':True},weld(False,False),1000),({'Gap_Exceeded':True},weld(True,False),1000)],d)
tasks.append(t)

t=base(6)
t['initial_conditions']={'BLOWER_RUN':False,'AERATION_BLOWER_CYCLE_COUNT':0,'delayElapsed_ms':0}
t['assumptions']=['Start delay elapsed is zero at the first sample of DO_LOW & AERATION_E_STOP_NC; run becomes TRUE at elapsed>=5s.', 'Count increments on the same invocation that changes end-of-scan BLOWER_RUN from FALSE to TRUE.', 'Tests stay below UINT overflow; overflow behavior is outside the specified operating domain.']
t['safety_priority']=['DO_LOW FALSE or emergency stop overrides timing and resets it immediately.']
t['atomic_propositions']={'permit':'DO_LOW & AERATION_E_STOP_NC', 'delayDone':'Permissive has continuously remained true for >=5s after its first sampled TRUE.', 'runPrev':'Pre-scan retained BLOWER_RUN.', 'countPrev':'Pre-scan AERATION_BLOWER_CYCLE_COUNT.', 'interface names':'Identically named sampled input or observed output.'}
prop(t,'G(BLOWER_RUN <-> (permit & delayDone))','Run is enabled only after the full delay.')
prop(t,'G(!permit -> (!BLOWER_RUN & X(!delayDone)))','Loss of demand or safety permissive clears run and its timer.')
prop(t,'G((!runPrev & BLOWER_RUN) -> AERATION_BLOWER_CYCLE_COUNT=countPrev+1)','One count per genuine start.')
prop(t,'G((runPrev | !BLOWER_RUN) -> AERATION_BLOWER_CYCLE_COUNT=countPrev)','No repeated count during continuous operation or stop.')
prop(t,'G((G(permit)) -> F(BLOWER_RUN))','A sustained permitted demand eventually starts under advancing time.')
d=dict(DO_LOW=False,AERATION_E_STOP_NC=True)
o=lambda r,c:dict(BLOWER_RUN=r,AERATION_BLOWER_CYCLE_COUNT=c)
test(t,'Exact delay threshold, sustained operation and second counted start', [({},o(False,0),0),({'DO_LOW':True},o(False,0),100),({'DO_LOW':True},o(False,0),4999),({'DO_LOW':True},o(True,1),1),({'DO_LOW':True},o(True,1),1000),({},o(False,1),100),({'DO_LOW':True},o(False,1),100),({'DO_LOW':True},o(True,2),5000)],d)
test(t,'Emergency stop discards partial and completed delay', [({'DO_LOW':True},o(False,0),0),({'DO_LOW':True},o(False,0),4000),({'DO_LOW':True,'AERATION_E_STOP_NC':False},o(False,0),1000),({'DO_LOW':True},o(False,0),100),({'DO_LOW':True},o(False,0),4999),({'DO_LOW':True},o(True,1),1),({'DO_LOW':True,'AERATION_E_STOP_NC':False},o(False,1),1)],d)
tasks.append(t)

t=base(7)
t['data_types']={'ST_Pump':{'kind':'STRUCT','fields':[{'name':'priority','type':'INT','access':'read_only'},{'name':'selection','type':'BOOL','access':'read_only'},{'name':'RunComd','type':'BOOL','access':'written'}]}}
t['initial_conditions']={'running':False,'pumpGroup[].RunComd':False}
t['assumptions']=['stop has priority over start and clears all five commands.', 'A start command selects the running set from current mode/configuration; commands are retained while neither button is TRUE. There is no automatic selection change until another start.', 'Equal priorities are resolved by lower array index first. Selection is ignored in automatic mode.', 'The caller initializes every RunComd FALSE before creating the first operational scan. Only RunComd may be written.']
t['safety_priority']=['Stop wins over a simultaneous start.', 'Read-only priority and selection fields must be unchanged.']
t['atomic_propositions']={'top3':'The three indices with highest priority, lower index winning a tie.', 'runPrev[i]':'The pre-scan RunComd value of pump i.', 'readOnlyPreserved':'All five priority and selection values equal their sampled values.', 'runs[i]':'Post-scan pumpGroup[i].RunComd, for i=1..5.', 'select[i]':'Sampled pumpGroup[i].selection.', 'interface names':'Identically named sampled input or output.'}
prop(t,'G(stop -> (forall i in 1..5: !runs[i]))','Stop de-energizes all pumps.')
prop(t,'G((!stop & start & !mode) -> (forall i in 1..5: runs[i]=select[i]))','Manual start uses exactly the selected pumps.')
prop(t,'G((!stop & start & mode) -> (forall i in 1..5: runs[i]=(i in top3)))','Automatic start runs exactly the highest-priority three.')
prop(t,'G((!stop & !start) -> (forall i in 1..5: runs[i]=runPrev[i]))','Start/stop operation latches commands.')
prop(t,'G(readOnlyPreserved)','The FB may not modify priorities or selections.')
def group(prios=(10,20,30,40,50),sel=(True,False,True,False,False),run=(False,)*5):
    return [dict(priority=p,selection=s,RunComd=r) for p,s,r in zip(prios,sel,run)]
def ps(g,mode=False,start=False,stop=False,run=(False,)*5):
    out=[{**x,'RunComd':r} for x,r in zip(g,run)]
    return (dict(mode=mode,start=start,stop=stop,pumpGroup=g),dict(pumpGroup=out))
test(t,'Manual latching, read-only fields and simultaneous stop/start', [ps(group(),start=True,run=(True,False,True,False,False)),ps(group(run=(True,False,True,False,False)),run=(True,False,True,False,False)),ps(group(run=(True,False,True,False,False)),start=True,stop=True)],defaults={})
test(t,'Automatic top-three selection and deterministic ties', [ps(group(),mode=True,start=True,run=(False,False,True,True,True)),ps(group(prios=(5,5,5,5,5),run=(False,False,True,True,True)),mode=True,start=True,run=(True,True,True,False,False)),ps(group(prios=(-3,0,-1,-2,4),run=(True,True,True,False,False)),mode=True,start=True,run=(False,True,True,False,True))],defaults={})
tasks.append(t)

t=base(8)
t['data_types']={'ST_AnalogChannel':{'kind':'STRUCT','fields':[{'name':n,'type':typ,'access':'written' if n in ('retVal','outputValue') else 'read_only'} for n,typ in [('enable','BOOL'),('hiLIM','REAL'),('loLIM','REAL'),('bipolar','BOOL'),('measuringMode','INT'),('retVal','WORD'),('outputValue','REAL')]]}}
t['initial_conditions']={'state':'No internal history required. IN_OUT output fields retain caller-provided values when skipped.'}
t['assumptions']=['Disabled and out-of-count channels retain both retVal and outputValue.', 'Successful enabled conversion sets retVal=0. Invalid channels preserve outputValue while returning the error code.', 'Invalid measuringMode has priority over invalid hiLIM/loLIM. Limit validation applies to enabled channels in every mode.', 'Scaling extrapolates outside nominal raw range; no saturation is specified.', 'Test metadata array_lower_bounds defines the physical array indices used by the caller. JSON arrays are ordered storage values, not IEC index literals. The caller satisfies count bounds.']
t['safety_priority']=['Process only the first count ordinal entries, pairing arrays at their independent lower bounds.', 'Do not modify raw analog values or any channel configuration.']
t['atomic_propositions']={'j':'An ordinal position starting at zero.', 'enabled(j)':'j<count and sampled channels[j].enable.', 'modeOK(j)':'Sampled measuringMode is 0,1,2.', 'limitsOK(j)':'Sampled hiLIM>loLIM.', 'raw(j)':'Sampled analogValues at its lower bound+j.', 'scaled(j)':'loLIM+(raw/27648)*(hiLIM-loLIM) for unipolar; loLIM+((raw+27648)/55296)*(hiLIM-loLIM) for bipolar.', 'preserved(j)':'The channel retVal/outputValue equal sampled values.', 'readonlyPreserved':'analogValues and channel configuration equal all their sampled values.', 'channel output names':'Post-scan fields of the channel at the indicated ordinal position.'}
prop(t,'G(readonlyPreserved)','Input arrays and configuration are never modified.')
prop(t,'G(forall j: !enabled(j) -> preserved(j))','Disabled and unprocessed channels are unchanged.')
prop(t,'G(forall j: (enabled(j) & !modeOK(j)) -> (retVal(j)=16#8001 & outputValue(j)=sampledOutputValue(j)))','Unsupported modes return the defined status without conversion.')
prop(t,'G(forall j: (enabled(j) & modeOK(j) & !limitsOK(j)) -> (retVal(j)=16#8002 & outputValue(j)=sampledOutputValue(j)))','Invalid limits return their status without conversion.')
prop(t,'G(forall j: (enabled(j) & modeOK(j) & limitsOK(j)) -> retVal(j)=0)','Successful enabled channels clear their status.')
prop(t,'G(forall j: (enabled(j) & limitsOK(j) & measuringMode(j)=0) -> outputValue(j)=scaled(j))','Linear scale uses the correct unipolar or bipolar range.')
prop(t,'G(forall j: (enabled(j) & limitsOK(j) & measuringMode(j)=1) -> outputValue(j)=raw(j)/10)','Standard-temperature resolution is one tenth.')
prop(t,'G(forall j: (enabled(j) & limitsOK(j) & measuringMode(j)=2) -> outputValue(j)=raw(j)/100)','Climatic-temperature resolution is one hundredth.')
t['atomic_propositions']['sampledOutputValue(j)']='The caller-provided outputValue before this scan.'
t['atomic_propositions']['measuringMode(j)']='The sampled measuringMode configuration for ordinal j.'
def ch(mode=0,bipolar=False,enable=True,lo=0.,hi=100.,ret=7,out=-999.):return dict(enable=enable,hiLIM=hi,loLIM=lo,bipolar=bipolar,measuringMode=mode,retVal=ret,outputValue=out)
def ats(raw,chs,results,count=None):
    outputs=[{**c,**r} for c,r in zip(chs,results)]
    return (dict(count=len(raw) if count is None else count,analogValues=raw,channels=chs),dict(analogValues=raw,channels=outputs))
test(t,'Unipolar and bipolar endpoints, midpoint and temperature modes', [ats([0,27648,-27648,0,27648,1234,-1234],[ch(),ch(),ch(bipolar=True),ch(bipolar=True),ch(bipolar=True),ch(mode=1),ch(mode=2)],[dict(retVal=0,outputValue=v) for v in [0.,100.,0.,50.,100.,123.4,-12.34]])],defaults={})
t['tests'][-1]['array_lower_bounds']={'analogValues':-2,'channels':7}
t['tests'][-1]['tolerance']={'absolute':0.0001,'relative':0.00001}
test(t,'Disabled channel, invalid mode priority, invalid limits and count truncation', [ats([1,2,3,4,5],[ch(enable=False),ch(mode=9,lo=10,hi=0),ch(lo=10,hi=10),ch(mode=2),ch()], [{},{'retVal':32769},{'retVal':32770},{'retVal':0,'outputValue':0.04},{}],count=4)],defaults={})
test(t,'count zero preserves every value and negative raw extrapolates', [ats([-27648],[ch()],[{}],count=0),ats([-27648],[ch()],[dict(retVal=0,outputValue=-100.)])],defaults={})
tasks.append(t)

t=base(9)
t['initial_conditions']={'average':0.0,'windowSizeReached':False,'error':False,'status':0,'sampleCount':0,'previousTrigger':False}
t['assumptions']=['During warm-up, average is the mean of the actual accepted samples; zero-filled unused capacity is excluded.', 'reset has priority over sampling for a valid window; it clears history and sets average=0 and windowSizeReached=FALSE.', 'Changing a valid windowSize clears history before any same-scan accepted sample. Invalid window sets error/status and does not accept or change history.', 'An invalid-window scan preserves average/windowSizeReached. Returning to a valid window clears error/status. Trigger edge history is updated on every invocation, including reset and invalid-window scans.', 'cyclicExecution accepts exactly one sample per scan and ignores the trigger. windowSizeReached becomes TRUE once the accepted sample count reaches windowSize.']
t['safety_priority']=['Invalid window returns an error before sampling.', 'Reset overrides sample acceptance.', 'Cyclic and trigger conditions cannot cause double insertion.']
t['atomic_propositions']={'valid':'1<=windowSize<=100', 'triggerRise':'trigger & !previousTrigger', 'accept':'valid & !reset & (cyclicExecution | triggerRise)', 'history':'Ghost ordered list of at most windowSize accepted samples, newest last.', 'historyAfter':'history after clearing on reset/window change and adding one accepted sample, discarding oldest if full.', 'unchangedMean':'average and windowSizeReached equal their pre-scan values.', 'interface names':'Identically named sampled input or observed output.'}
prop(t,'G(!valid -> (error & status=16#8200 & unchangedMean))','Window bounds are checked without silently accepting data.')
prop(t,'G(valid -> (!error & status=0))','A valid window clears configuration error.')
prop(t,'G((valid & reset) -> (average=0 & !windowSizeReached))','Reset produces an empty history.')
prop(t,'G((valid & !reset) -> average=meanOrZero(historyAfter))','The result is the arithmetic mean of the active window or zero when empty.')
prop(t,'G(valid -> (windowSizeReached <-> length(historyAfter)=windowSize))','Full-window indication follows history population.')
prop(t,'G(X(previousTrigger)=trigger)','Rising-edge memory updates even if sampling is inhibited.')
prop(t,'G((valid & !reset & !cyclicExecution & !triggerRise & !windowChanged) -> unchangedMean)','No event means no sample update.')
t['atomic_propositions'].update({'meanOrZero':'Arithmetic mean for a nonempty list, otherwise zero.', 'length':'Number of samples in the history list.', 'windowChanged':'Current valid windowSize differs from the last valid configured size.', 'previousTrigger':'Pre-scan retained trigger, initialized FALSE.'})
d=dict(cyclicExecution=False,trigger=False,value=0.,windowSize=3,reset=False)
def avg(a=0.,full=False,e=False,s=0):return dict(average=a,windowSizeReached=full,error=e,status=s)
test(t,'Cyclic warm-up, sliding replacement and reset priority', [({'cyclicExecution':True,'value':3.},avg(3.)),({'cyclicExecution':True,'value':6.},avg(4.5)),({'cyclicExecution':True,'value':9.},avg(6.,True)),({'cyclicExecution':True,'value':12.,'trigger':True},avg(9.,True)),({'cyclicExecution':True,'value':99.,'reset':True},avg()),({'cyclicExecution':True,'value':-6.},avg(-6.))],d)
test(t,'Rising edge only, held trigger, window change and invalid bounds', [({'trigger':True,'value':2.},avg(2.)),({'trigger':True,'value':100.},avg(2.)),({'value':100.},avg(2.)),({'trigger':True,'value':4.},avg(3.)),({'windowSize':1,'cyclicExecution':True,'value':8.},avg(8.,True)),({'windowSize':0},avg(8.,True,True,33280)),({'windowSize':101},avg(8.,True,True,33280)),({'windowSize':1,'reset':True},avg()),({'windowSize':1,'trigger':True,'value':5.},avg(5.,True))],d)
t['tests'][-1]['tolerance']={'absolute':1e-9,'relative':1e-9}
tasks.append(t)

t=base(10)
t['initial_conditions']={'HeaterOutput':False,'HeaterStatus':False,'OverheatProtection':False,'heatDemand':False,'heatElapsed_ms':0,'cooldownElapsed_ms':0}
t['assumptions']=['At equality TemperatureSensorInput=SetTemperature, retain the last heat-demand state. On a fresh instance the retained demand is FALSE.', 'The prose says "more than" a period and gives 5s. The evaluation resolves this to a 5-second threshold: protection trips at continuous heating elapsed>=5s, beginning with elapsed zero at the first energized sample.', 'Protection is latched for at least 3s from its trip. At elapsed>=3s it may clear and heat can restart in the same scan if the sensor is valid and demand remains.', 'A sensor fault immediately turns heat off and resets continuous-heating time. It does not clear or restart an already active cooldown.', 'The display outputs mirror their corresponding sampled temperature and setpoint even during a fault. HeaterStatus equals HeaterOutput. Inputs are held stable between timed samples.']
t['safety_priority']=['Sensor fault or active overheat protection overrides the heat demand.', 'Protection shutdown is evaluated before the output is finalized.']
t['atomic_propositions']={'sensorFault':'TemperatureSensorInput<0 OR TemperatureSensorInput>100', 'demand':'Ghost retained demand; set below setpoint, clear above, retain at equality.', 'heatLimitReached':'Continuous energized time has reached 5s, with first energized scan at elapsed zero.', 'cooldownDone':'At least 3s has elapsed since protection trip.', 'protectPrev':'Pre-scan retained OverheatProtection.', 'interface names':'Identically named sampled input or observed output.'}
prop(t,'G(sensorFault -> !HeaterOutput)','Invalid sensor data must never energize the heater.')
prop(t,'G(OverheatProtection -> !HeaterOutput)','The heater remains off during cooldown.')
prop(t,'G(HeaterStatus=HeaterOutput)','The status output reports actual commanded heat.')
prop(t,'G((CurrentTemperature=TemperatureSensorInput) & (SetTempDisplay=SetTemperature))','The displays mirror sampled values.')
prop(t,'G((!sensorFault & !OverheatProtection & demand & !heatLimitReached) -> HeaterOutput)','A permitted heat demand energizes the heater.')
prop(t,'G(heatLimitReached -> (OverheatProtection & !HeaterOutput))','The continuous-heating threshold trips protection in the same scan.')
prop(t,'G((protectPrev & !cooldownDone) -> OverheatProtection)','Protection cannot clear before its cooldown expires.')
prop(t,'G((OverheatProtection & G(!sensorFault & demand)) -> F(HeaterOutput))','With advancing time and persistent valid demand, heating resumes after finite cooldown.')
d=dict(TemperatureSensorInput=20.,SetTemperature=30.)
def temp(v=20.,s=30.,heat=False,protect=False):return dict(CurrentTemperature=v,SetTempDisplay=s,HeaterStatus=heat,OverheatProtection=protect,HeaterOutput=heat)
test(t,'Heating threshold, cooldown boundary and safe restart', [({},temp(heat=True),0),({},temp(heat=True),4999),({},temp(protect=True),1),({},temp(protect=True),2999),({},temp(heat=True),1),({'TemperatureSensorInput':31.},temp(31.),100)],d)
test(t,'Sensor faults, valid endpoint values and equality retention', [({'TemperatureSensorInput':30.},temp(30.),0),({'TemperatureSensorInput':0.},temp(0.,heat=True),100),({'TemperatureSensorInput':30.},temp(30.,heat=True),100),({'TemperatureSensorInput':-0.1},temp(-0.1),100),({'TemperatureSensorInput':100.},temp(100.),100),({'TemperatureSensorInput':100.1},temp(100.1),100),({'TemperatureSensorInput':30.},temp(30.),100)],d)
test(t,'Fault during protection cannot clear the cooldown', [({},temp(heat=True),0),({},temp(protect=True),5000),({'TemperatureSensorInput':-1.},temp(-1.,protect=True),1000),({},temp(protect=True),1000),({},temp(heat=True),1000)],d)
tasks.append(t)

for t in tasks:
    p=ROOT/'dataset'/'public'/f"{t['id']}.json"
    p.write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

print(json.dumps({'tasks':len(tasks),'ltl_properties':sum(len(t['ltl']) for t in tasks),'test_cases':sum(len(t['tests']) for t in tasks),'test_steps':sum(len(c['steps']) for t in tasks for c in t['tests'])}))
