"""Rebuild PUB011..PUB020 from unmodified instructor source plus explicit annotations."""
from pathlib import Path
import json, hashlib

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'PLC_Agent_Final'
SRC = ROOT / '大作业题库json' / '大作业题库json' / '大作业题库.json'
bank = json.loads(SRC.read_text(encoding='utf-8-sig'))
questions = [(g, i, x['en']) for g in ('easy','medium','hard') for i,x in enumerate(bank[g])]
SCAN = ('Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. '
        'Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. '
        'A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; '
        'the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, '
        'are attributed to the current invocation rather than inferred from dt_ms.')

def base(n, scenario, init, assumptions, priorities):
    group,index,raw=questions[n-1]
    interface=[]
    for line in raw.splitlines():
        c=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(c)==4 and c[0] in ('Input','Output','Input/Output'):
            interface.append(dict(direction={'Input':'INPUT','Output':'OUTPUT','Input/Output':'IN_OUT'}[c[0]],name=c[1].strip('`'),type=c[2].strip('`'),description=c[3]))
    return dict(schema_version=1,id=f'PUB{n:03}',kind='public',title=raw.splitlines()[0].lstrip('# '),difficulty=group,
        provenance=dict(source_type='instructor_public_question_bank',source_file='大作业题库json/大作业题库json/大作业题库.json',source_index=f'{group}[{index}] (zero based), flattened task {n}',source_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(),adaptation='Official en text and interface preserved verbatim; interpretations are separate assumptions.',rationale=scenario,review='Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending.'),requirements=raw,scenario=scenario,interface=interface,initial_conditions=init,scan_semantics=SCAN,safety_priority=priorities,assumptions=assumptions,atomic_propositions={},ltl=[],tests=[])

def spec(t, atoms, *properties):
    t['atomic_propositions']=atoms
    for name,formula,explanation in properties:
        t['ltl'].append(dict(id=f"{t['id']}.P{len(t['ltl'])+1}",name=name,formula=formula,explanation=explanation))

def test(t,name,purpose,defaults,sequence,**extra):
    rows=[]
    for s in sequence:
        inp={**defaults,**s[0]}
        for param in t['interface']:
            if param['direction']=='IN_OUT' and param['name'] not in inp:
                inp[param['name']]={'$binding':param['name'],'binding_id':extra.get('binding_id','default'),'retain_storage':True}
        exp=s[1]
        if not exp:
            if any(p['name']=='status' and p['direction']=='OUTPUT' for p in t['interface']):
                exp={'status':0}
            elif t['id']=='PUB012':
                exp={'Slab_Fault_Counter':rows[-1]['expected']['Slab_Fault_Counter']}
            else:
                raise ValueError('An idle scan needs an explicit observable expectation')
        row=dict(inputs=inp,expected=exp)
        if len(s)>2: row['dt_ms']=s[2]
        rows.append(row)
    t['tests'].append(dict(id=f"{t['id']}.T{len(t['tests'])+1}",name=name,purpose=purpose,steps=rows,**extra))

def save(t):
    (OUT/'dataset'/'public'/f"{t['id']}.json").write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Three-station line
D=dict(Mode=True,ForwardButton=False,ReverseButton=False,SensorA=False,SensorB=False,SensorC=False,ButtonA=False,ButtonB=False,ButtonC=False)
t=base(11,'A conveyor shares manual interlocking and an automatic three-station route.',dict(MotorForward=False,MotorReverse=False,CompletionLight=False,phase='WAIT_A'),['Opposing manual buttons produce neither direction.','Buttons are level signals accepted only in their corresponding station wait. One phase transition is accepted per call.','Entering manual mode clears automatic state and completion; return to automatic waits for A.','Only one product is presented; station sensors are not contradictory.'],['Forward and reverse are mutually exclusive.','Destination arrival stops movement before processing resumes.'])
spec(t,dict(auto='Mode',fwd='MotorForward after scan',rev='MotorReverse after scan',mf='ForwardButton AND NOT ReverseButton',mr='ReverseButton AND NOT ForwardButton',arrive='pre-phase MOVE_AB AND SensorB OR pre-phase MOVE_BC AND SensorC',finish='pre-phase WAIT_C AND SensorC AND ButtonC',light='CompletionLight',removed='NOT SensorC'),
 ('Interlock','G(!(fwd & rev))','Motor directions are mutually exclusive.'),
 ('Manual','G(!auto -> ((fwd <-> mf) & (rev <-> mr)))','Manual level requests obey neutral conflict resolution.'),
 ('Auto direction','G(auto -> !rev)','Automatic routing only moves forward.'),
 ('Arrival','G(auto & arrive -> !fwd)','Arrival stops the motor in the observed scan.'),
 ('Completion','G(auto & finish -> light)','C completion asserts the light.'),
 ('Removal','G(auto & removed -> !light)','Removal clears completion.'))
test(t,'manual','Neutral, forward, reverse, conflicting commands.',D,[({'Mode':False},{'MotorForward':False,'MotorReverse':False}),({'Mode':False,'ForwardButton':True},{'MotorForward':True,'MotorReverse':False}),({'Mode':False,'ReverseButton':True},{'MotorForward':False,'MotorReverse':True}),({'Mode':False,'ForwardButton':True,'ReverseButton':True},{'MotorForward':False,'MotorReverse':False})])
test(t,'cycle','Station waits, retained movement, completion and removal.',D,[({}, {'MotorForward':False,'CompletionLight':False}),({'SensorA':True},{'MotorForward':False}),({'SensorA':True,'ButtonA':True},{'MotorForward':True}),({}, {'MotorForward':True}),({'SensorB':True},{'MotorForward':False}),({'SensorB':True,'ButtonB':True},{'MotorForward':True}),({'SensorC':True},{'MotorForward':False,'CompletionLight':False}),({'SensorC':True,'ButtonC':True},{'CompletionLight':True}),({'SensorC':True},{'CompletionLight':True}),({}, {'CompletionLight':False})])
test(t,'wrong_button','Out-of-order confirmations cannot start the route.',D,[({'ButtonB':True,'ButtonC':True},{'MotorForward':False,'CompletionLight':False}),({'SensorA':True,'ButtonB':True},{'MotorForward':False})])
save(t)

# Mechanical arm: commands are decoded from the updated phase, with completion
# sampled from the pre-phase. This gives a single, explicit transition per scan.
D=dict(ManualMode=False,SingleStepMode=False,SingleCycleMode=False,ContinuousMode=False,
       EmergencyStop=True,Start=False,DownButton=False,UpButton=False,LeftButton=False,
       RightButton=False,GripButton=False,ReleaseButton=False,DownLimitSwitch=False,
       UpLimitSwitch=True,LeftLimitSwitch=True,RightLimitSwitch=False,
       GripLimitSwitch=False,ReleaseLimitSwitch=True)
OFF=dict(MoveDown=False,MoveUp=False,MoveLeft=False,MoveRight=False,ActivateGrip=False,ActivateRelease=False)
def arm(command):return {**OFF,command:True}
t=base(19,'An eight-action handling cycle shares manual, confirmed single-step, single-cycle and continuous operation.',
       {**OFF,'next_step':1,'busy':False,'initial_pose':'top left'},
       ['EmergencyStop=FALSE cancels the sequence and outputs; recovery requires a fresh Start edge from a verified top-left pose.',
        'A Start press is a rising edge. Start edges during an active action are ignored; edge history still updates.',
        'No selected mode means all commands off and sequence reset. Changing mode also resets the sequence.',
        'Opposing manual commands on an axis or grip pair are both inhibited. Independent non-opposing actions may run together.',
        'Manual commands are combinational and stop on their matching limit/feedback. Contradictory limit switches are outside the caller contract.',
        'Only one phase transition occurs per invocation. In cycle modes, completion feedback switches to the next command in that scan; an already-active next limit suppresses its command but is processed as completion on the next invocation.',
        'Single-step completion switches all outputs off; the next action requires a fresh Start edge on a later scan.',
        'Continuous completion of left movement wraps to down in the same scan. Single-cycle completion returns to idle.',
        'At the start of a new automatic sequence (action 1, not every individual single step), UpLimitSwitch and LeftLimitSwitch must both be TRUE. Grip and release complete on the supplied feedback switches.'],
       ['Emergency stop overrides every mode and request.','Opposed directions and grip/release are mutually exclusive.','A reached position suppresses its own command immediately.'])
spec(t,dict(safe='EmergencyStop input',off='all six command outputs FALSE',no_mode='none of the four mode selectors TRUE',
            exclusive='NOT(MoveDown AND MoveUp) AND NOT(MoveLeft AND MoveRight) AND NOT(ActivateGrip AND ActivateRelease)',
            down_manual='ManualMode AND DownButton AND NOT UpButton AND NOT DownLimitSwitch',
            down='MoveDown',down_limit='DownLimitSwitch',up_limit='UpLimitSwitch',up='MoveUp',
            left_limit='LeftLimitSwitch',left='MoveLeft',right_limit='RightLimitSwitch',right='MoveRight',
            grip_limit='GripLimitSwitch',grip='ActivateGrip',release_limit='ReleaseLimitSwitch',release='ActivateRelease',
            step_done='SingleStepMode AND pre-busy AND matching completion feedback',
            waiting='SingleStepMode AND NOT pre-busy AND NOT rising(Start)',
            cycle_done='SingleCycleMode AND pre-phase LEFT AND LeftLimitSwitch',
            continuous_done='ContinuousMode AND pre-phase LEFT AND LeftLimitSwitch',
            begin_next='post-phase DOWN with command gated by DownLimitSwitch',
            busy='pre-sequence is executing an action',feedback='matching completion feedback for the pre-action is TRUE',
            idle='post-sequence idle',start='fresh Start edge in idle with top-left pose and selected automatic mode',
            started='post-phase DOWN, busy TRUE',ordered='the next accepted automatic phase follows DOWN, GRIP, UP1, RIGHT, DOWN2, RELEASE, UP2, LEFT'),
     ('Safety','G((!safe | no_mode) -> off)','No command survives emergency stop or no mode.'),
     ('Interlocks','G(exclusive)','Opposed actuators are never commanded together.'),
     ('Manual down','G(safe & ManualMode -> (down <-> down_manual))','Manual down requires the button and an unreached lower limit.'),
     ('Reached limits','G((down_limit -> !down) & (up_limit -> !up) & (left_limit -> !left) & (right_limit -> !right) & (grip_limit -> !grip) & (release_limit -> !release))','Every corresponding completion input suppresses its command.'),
     ('Step wait','G(safe & (step_done | waiting) -> off)','A completed single step waits for another press.'),
     ('Automatic start','G(safe & start -> started)','A permitted fresh start begins down.'),
     ('Order','G(ordered)','The eight preset actions retain their required order.'),
     ('Cycle boundary','G(safe -> ((cycle_done -> (idle & off)) & (continuous_done -> begin_next)))','Single-cycle stops; continuous wraps.'),
     ('Conditional liveness','(G(safe & SingleCycleMode) & G(busy -> F feedback)) -> G(started -> F idle)','With unchanged safe single-cycle mode and eventual matching feedback, every started sequence eventually returns idle.'))
M={**D,'ManualMode':True}
test(t,'manual_limits','Manual hold-to-run, reached limits, opposing requests and emergency priority.',M,[
 ({'DownButton':True},arm('MoveDown')),
 ({'DownButton':True,'DownLimitSwitch':True,'UpLimitSwitch':False},OFF),
 ({},OFF),
 ({'DownButton':True,'UpButton':True,'UpLimitSwitch':False},OFF),
 ({'RightButton':True},arm('MoveRight')),
 ({'RightButton':True,'RightLimitSwitch':True,'LeftLimitSwitch':False},OFF),
 ({'GripButton':True,'ReleaseLimitSwitch':False},arm('ActivateGrip')),
 ({'GripButton':True,'GripLimitSwitch':True,'ReleaseLimitSwitch':False},OFF),
 ({'GripButton':True,'ReleaseButton':True,'ReleaseLimitSwitch':False},OFF),
 ({'EmergencyStop':False,'DownButton':True,'RightButton':True},OFF)])
S={**D,'SingleStepMode':True}
test(t,'single_step','Each new step requires a release and fresh start; held start cannot skip grip.',S,[
 ({},OFF),({'Start':True},arm('MoveDown')),
 ({'Start':True,'UpLimitSwitch':False},arm('MoveDown')),
 ({'Start':True,'DownLimitSwitch':True,'UpLimitSwitch':False},OFF),
 ({'Start':True,'DownLimitSwitch':True,'UpLimitSwitch':False},OFF),
 ({'DownLimitSwitch':True,'UpLimitSwitch':False},OFF),
 ({'Start':True,'DownLimitSwitch':True,'UpLimitSwitch':False,'ReleaseLimitSwitch':False},arm('ActivateGrip')),
 ({'DownLimitSwitch':True,'UpLimitSwitch':False,'GripLimitSwitch':True,'ReleaseLimitSwitch':False},OFF),
 ({'Start':True,'DownLimitSwitch':True,'UpLimitSwitch':False,'GripLimitSwitch':True,'ReleaseLimitSwitch':False},arm('MoveUp'))])
def automatic_arm_sequence(continuous=False):
    return [({},OFF),({'Start':True},arm('MoveDown')),
       ({'DownLimitSwitch':True,'UpLimitSwitch':False,'ReleaseLimitSwitch':False},arm('ActivateGrip')),
       ({'DownLimitSwitch':True,'UpLimitSwitch':False,'GripLimitSwitch':True,'ReleaseLimitSwitch':False},arm('MoveUp')),
       ({'UpLimitSwitch':True,'GripLimitSwitch':True,'ReleaseLimitSwitch':False},arm('MoveRight')),
       ({'UpLimitSwitch':True,'LeftLimitSwitch':False,'RightLimitSwitch':True,'GripLimitSwitch':True,'ReleaseLimitSwitch':False},arm('MoveDown')),
       ({'UpLimitSwitch':False,'DownLimitSwitch':True,'LeftLimitSwitch':False,'RightLimitSwitch':True,'GripLimitSwitch':False,'ReleaseLimitSwitch':False},arm('ActivateRelease')),
       ({'UpLimitSwitch':False,'DownLimitSwitch':True,'LeftLimitSwitch':False,'RightLimitSwitch':True,'ReleaseLimitSwitch':True},arm('MoveUp')),
       ({'UpLimitSwitch':True,'LeftLimitSwitch':False,'RightLimitSwitch':True,'ReleaseLimitSwitch':True},arm('MoveLeft')),
       ({'UpLimitSwitch':True,'LeftLimitSwitch':True,'RightLimitSwitch':False,'ReleaseLimitSwitch':True},arm('MoveDown') if continuous else OFF)]
test(t,'single_cycle','All eight actions complete once and wait at top left.',{**D,'SingleCycleMode':True},automatic_arm_sequence())
test(t,'continuous','The eighth completion wraps immediately to the first action.',{**D,'ContinuousMode':True},automatic_arm_sequence(True))
test(t,'emergency_reset','Emergency cancels an action; releasing emergency does not auto-restart.',{**D,'SingleCycleMode':True},[
 ({},OFF),({'Start':True},arm('MoveDown')),({'EmergencyStop':False,'UpLimitSwitch':False},OFF),
 ({'UpLimitSwitch':False},OFF),({},OFF),({'Start':True},arm('MoveDown'))])
save(t)

# Five-station production line with weighing and a retained firing setpoint.
D=dict(Mode=True,ForwardButton=False,ReverseButton=False,SensorFeed=False,SensorWash=False,
       SensorWeight=False,SensorFiring=False,SensorOutput=False,washComplete=False,
       weightComplete=False,weight=0.0,firingComplete=False)
O=dict(MotorForward=False,MotorReverse=False,kick=False,CompletionLight=False)
t=base(20,'A five-station conveyor cleans, rejects out-of-range weights, calculates a firing setpoint and signals output completion.',
       {**O,'firingTemp':0.0,'phase':'WAIT_FEED'},
       ['Manual opposing requests both inhibit the motor. Entering manual clears sequence, kick and completion but retains the last firing setpoint.',
        'Only one product is processed; the caller does not assert contradictory station sensors.',
        'Mode changes reset the automatic route to WAIT_FEED. Confirmations are levels accepted only in their corresponding processing wait.',
        'Arrival has priority; a confirmation already TRUE on the arrival invocation is accepted no earlier than the next invocation.',
        'A rejected item remains at the weighing station, with kick TRUE, until SensorWeight becomes FALSE. It then returns to WAIT_FEED.',
        'firingTemp updates only for accepted weight and retains the last accepted value otherwise. REAL comparisons use absolute tolerance 1e-5.',
        'At most one phase transition occurs per invocation. Output arrival sets CompletionLight immediately, removal clears it and resets the route.'],
       ['Forward and reverse are mutually exclusive.','Destination arrival stops forward motion.','Unqualified weight never proceeds to firing.','Completion commands from an unrelated station are ignored.'])
spec(t,dict(auto='Mode',fwd='MotorForward',rev='MotorReverse',mf='ForwardButton AND NOT ReverseButton',mr='ReverseButton AND NOT ForwardButton',
            feed='pre-phase WAIT_FEED AND SensorFeed',moving='post-phase MOVE_TO_WASH',
            arrival='pre-phase moving AND corresponding destination sensor TRUE',stopped='NOT MotorForward AND NOT MotorReverse',
            judged='auto AND pre-phase WAIT_WEIGHT AND SensorWeight AND weightComplete',valid='100<=weight<=200',
            reject='kick AND stopped',qualified='NOT kick AND fwd AND firingTemp=500+(weight-100)*0.5',
            output_arrival='auto AND pre-phase MOVE_TO_OUTPUT AND SensorOutput',light='CompletionLight',
            removed='auto AND pre-phase OUTPUT_DONE AND NOT SensorOutput',clear='NOT CompletionLight AND stopped',
            no_judgment='NOT judged OR NOT valid',same_temp='firingTemp=pre-firingTemp',
            arrival_pending='pre-phase is a conveyor movement',processing_wait='pre-phase is WAIT_WASH, WAIT_WEIGHT or WAIT_FIRING',matching_completion='matching station sensor and processing completion are TRUE in the corresponding wait',
            order='automatic route is FEED, WASH, WEIGHT, FIRING, OUTPUT; rejected weights cannot enter FIRING'),
     ('Interlock','G(!(fwd & rev))','Motor directions cannot overlap.'),
     ('Manual','G(!auto -> ((fwd <-> mf) & (rev <-> mr)))','Manual commands follow level inputs with neutral conflict handling.'),
     ('Automatic direction','G(auto -> !rev)','The automatic route never reverses.'),
     ('Arrival stop','G(auto & arrival -> stopped)','An arrived item stops before processing.'),
     ('Weight decision','G(judged -> ((valid -> qualified) & (!valid -> reject)))','The acceptance interval is inclusive and its setpoint is linear.'),
     ('Setpoint retention','G(no_judgment -> same_temp)','No unqualified or unrelated scan changes the last accepted setpoint.'),
     ('Completion','G((output_arrival -> light) & (removed -> clear))','Output arrival and removal control the light.'),
     ('Route','G(order)','Only the ordered processing route advances qualified products.'),
     ('Conditional completion','(G(auto) & G(arrival_pending -> F arrival) & G(processing_wait -> F matching_completion) & G(judged -> valid)) -> G(feed -> F light)','With continuing automatic mode, eventual movement/processing feedback and accepted weights, each feed eventually completes.'))
test(t,'manual','Forward, reverse, both buttons and no request.',D,[
 ({'Mode':False},{**O,'firingTemp':0.0}),
 ({'Mode':False,'ForwardButton':True},{**O,'MotorForward':True}),
 ({'Mode':False,'ReverseButton':True},{**O,'MotorReverse':True}),
 ({'Mode':False,'ForwardButton':True,'ReverseButton':True},O)])
def production_to_weight(weight):
    return [({},O),({'SensorFeed':True},{**O,'MotorForward':True}),
       ({'SensorWash':True},O),({'SensorWash':True,'washComplete':True},{**O,'MotorForward':True}),
       ({'SensorWeight':True},O),({'SensorWeight':True,'weightComplete':True,'weight':weight},
         {**O,'MotorForward':True,'firingTemp':500+(weight-100)*.5} if 100<=weight<=200 else {**O,'kick':True,'firingTemp':0.0})]
for weight in (100.0,150.0,200.0):
    expected_temp=500+(weight-100)*.5
    seq=production_to_weight(weight)+[
       ({'SensorFiring':True},{**O,'firingTemp':expected_temp}),
       ({'SensorFiring':True,'firingComplete':True},{**O,'MotorForward':True,'firingTemp':expected_temp}),
       ({'SensorOutput':True},{**O,'CompletionLight':True,'firingTemp':expected_temp}),
       ({'SensorOutput':True},{**O,'CompletionLight':True}),({}, {**O,'firingTemp':expected_temp})]
    test(t,'qualified_'+str(int(weight)),'Inclusive acceptance and linear firing setpoint for weight '+str(weight),D,seq)
for weight in (99.9,200.1):
    test(t,'rejected_'+str(weight).replace('.','_'),'Reject just outside the inclusive limits, retain rejection until removal.',D,
       production_to_weight(weight)+[({'SensorWeight':True},{**O,'kick':True}),({},O),({'SensorFeed':True},{**O,'MotorForward':True})])
test(t,'wrong_feedback','Out-of-order completions do not move an idle product.',D,[
 ({'washComplete':True,'weightComplete':True,'firingComplete':True},O),
 ({'SensorFeed':True,'weightComplete':True},{**O,'MotorForward':True}),
 ({'SensorWash':True,'washComplete':True},O),
 ({'SensorWash':True,'washComplete':True},{**O,'MotorForward':True})])
save(t)

# IPv4 parser
D=dict(ipText='')
t=base(14,'Strict decimal IPv4 parsing into a network-order unsigned address.',dict(ipValue=0),['Leading zeros are allowed because the official text requires decimal-digit segments without prohibiting them.','Signs, whitespace, hexadecimal notation and embedded nondigits are rejected.','Embedded NUL is a PLC string terminator; visible input is constrained to declared STRING capacity.'],['Malformed or out-of-range data forces zero in the same invocation.'])
spec(t,dict(valid='exactly four nonempty decimal-digit segments separated by periods, each parsed value 0..255',packed='ipValue=a*16777216+b*65536+c*256+d for the four parsed octets',zero='ipValue=0',same_input='input equals previous scan input (not initial call)',same_output='output equals previous scan output'),
 ('Valid assembly','G(valid -> packed)','The first octet is the most significant byte.'),
 ('Invalid input','G(!valid -> zero)','Invalid data never preserves an old result.'),
 ('Stateless parsing','G(same_input -> same_output)','Repeated strings produce repeated results.'))
test(t,'valid','Zero, maximum, byte order and decimal leading zeros.',D,[({'ipText':s},{'ipValue':v}) for s,v in [('0.0.0.0',0),('255.255.255.255',4294967295),('192.168.1.10',3232235786),('1.2.3.4',16909060),('001.002.003.004',16909060)]])
bad=['','1.2.3','1.2.3.4.5','.1.2.3','1..2.3','1.2.3.','1.2.3.256','-1.2.3.4','1.2.3.x',' 1.2.3.4','1.2.3.4 ','0x1.2.3.4','999999999999999999999.2.3.4']
test(t,'invalid','Malformed and overflowing segments clear a previous valid result.',D,[({'ipText':'1.2.3.4'},{'ipValue':16909060})]+[({'ipText':s},{'ipValue':0}) for s in bad])
save(t)

# Material proportioning
D=dict(estop=True,opeMode=True,valveAStart=False,valveBStart=False,valveCStart=False,valveDStart=False,mixMotorStart=False,autoStart=False,processMode=False,levelSensor=0,mixMotorComplete=False)
OFF=dict(valveARun=False,valveBRun=False,valveCRun=False,valveDRun=False,mixMotorRun=False)
def actuator(name):return {**OFF,name:True}
t=base(15,'A mixer toggles manual actuators or sequences two/three-material filling, mixing and discharge.',{**OFF,'phase':'IDLE'},['All manual buttons use rising-edge independent toggles. Edge history updates during emergency stop so held buttons cannot restart outputs on recovery.','Emergency stop resets all manual latches and automatic state. A fresh autoStart edge is required to restart.','Changing operation mode clears old latches and sequence.','autoStart is a rising edge accepted in IDLE; processMode stays fixed during the batch.','Thresholds are >=50, >=80 and >=100 cm. One logical phase transition occurs per invocation.','Valve D stays open after discharge is initiated until emergency stop or mode reset; no drain-complete signal is supplied.'],['estop=FALSE turns every actuator off immediately.','Automatic phases drive only one actuator; independent manual toggles may coexist.'])
spec(t,dict(safe='estop',off='all actuator outputs FALSE',toggle='safe AND NOT opeMode AND rising(valveAStart)',changed='valveARun=NOT pre-valveARun',held='safe AND NOT opeMode AND NOT rising(valveAStart) AND no mode change',same='valveARun=pre-valveARun',toB='safe AND opeMode AND pre-phase FILL_A AND levelSensor>=50',B='valveBRun only',toMix='safe AND opeMode AND pre-phase FILL_B AND levelSensor>=80 AND NOT processMode',Mix='mixMotorRun only',toC='safe AND opeMode AND pre-phase FILL_B AND levelSensor>=80 AND processMode',C='valveCRun only',fromC='safe AND opeMode AND pre-phase FILL_C AND levelSensor>=100',mixed='safe AND opeMode AND pre-phase MIX AND mixMotorComplete',Drain='valveDRun only'),
 ('Emergency','G(!safe -> off)','Emergency permissive dominates mode and buttons.'),
 ('Manual toggle','G((toggle -> changed) & (held -> same))','A held button cannot repeatedly toggle; applies independently to all five buttons.'),
 ('First fill threshold','G(toB -> B)','A closes and B opens at or above 50cm.'),
 ('Two-material branch','G(toMix -> Mix)','The two-material branch skips C.'),
 ('Three-material branch','G((toC -> C) & (fromC -> Mix))','C fills to 100cm before mixing.'),
 ('Mix completion','G(mixed -> Drain)','Mix completion stops mixing and opens D.'))
test(t,'manual_edges','Held signal, second edge, all actuator requests and emergency.',D,[({'opeMode':False},OFF),({'opeMode':False,'valveAStart':True},actuator('valveARun')),({'opeMode':False,'valveAStart':True},actuator('valveARun')),({'opeMode':False},actuator('valveARun')),({'opeMode':False,'valveAStart':True},OFF),({'opeMode':False,'valveBStart':True,'valveCStart':True,'valveDStart':True,'mixMotorStart':True},{**OFF,'valveBRun':True,'valveCRun':True,'valveDRun':True,'mixMotorRun':True}),({'opeMode':False,'estop':False},OFF)])
test(t,'two_material','Equality thresholds and mixing completion.',D,[({},OFF),({'autoStart':True},actuator('valveARun')),({'levelSensor':49},actuator('valveARun')),({'levelSensor':50},actuator('valveBRun')),({'levelSensor':80},actuator('mixMotorRun')),({'levelSensor':80,'mixMotorComplete':True},actuator('valveDRun')),({'estop':False},OFF)])
test(t,'three_material','Skipped thresholds advance and emergency cancels the active cycle.',D,[({},OFF),({'autoStart':True,'processMode':True},actuator('valveARun')),({'levelSensor':55,'processMode':True},actuator('valveBRun')),({'levelSensor':85,'processMode':True},actuator('valveCRun')),({'levelSensor':99,'processMode':True},actuator('valveCRun')),({'levelSensor':100,'processMode':True},actuator('mixMotorRun')),({'estop':False,'mixMotorComplete':True,'processMode':True},OFF),({'processMode':True},OFF)])
save(t)

# Flexible processing
D=dict(processLength=3,sensor1=False,sensor2=False,sensor3=False,sensor4=False,sensor5=False,station1Start=False,station2Complete=False,station3Complete=False,station4Complete=False,processSequence=[4,2,5,0,0,0,0,0])
t=base(16,'A bidirectional conveyor follows a bounded sequence that may revisit processing stations.',dict(conveyorLeft=False,conveyorRight=False,phase='IDLE',currentStation=1,sequenceIndex=1),['The active sequence satisfies the official contract and remains fixed throughout a product cycle.','station1Start is a rising edge accepted with sensor1 while idle.','Destination arrival immediately stops the motor. Completion is accepted only at the current processing wait.','Completion signals are rising edges. Consecutive equal stations denote separate processing operations with fresh edges and no conveyor movement.','Only one sequence-index advancement occurs per invocation. Station5 arrival returns to idle.'],['Left and right are mutually exclusive.','Target arrival stops motion before accepting processing completion.'])
spec(t,dict(left='conveyorLeft',right='conveyorRight',higher='pre-phase MOVING AND targetStation>currentStation AND NOT sensor[targetStation]',lower='pre-phase MOVING AND targetStation<currentStation AND NOT sensor[targetStation]',arrive='pre-phase MOVING AND sensor[targetStation]',stop='NOT conveyorLeft AND NOT conveyorRight',waiting='pre-phase WAIT_PROCESS AND no fresh completion edge',out='pre-phase MOVING AND targetStation=5 AND sensor5',done='post phase IDLE after station5 arrival',moving='pre-phase MOVING',processing='pre-phase WAIT_PROCESS',completion='fresh matching processing-complete edge in the current wait',started='station1Start rising edge accepted with sensor1 in idle'),
 ('Interlock','G(!(left & right))','Both directions can never run together.'),
 ('Direction','G((higher -> (right & !left)) & (lower -> (left & !right)))','The target/current station order determines direction.'),
 ('Arrival','G(arrive -> stop)','Every destination stops movement immediately.'),
 ('Wait','G(waiting -> stop)','A processing wait does not move without completion.'),
 ('Output','G(out -> (done & stop))','The final station completes the sequence.'),
 ('Conditional completion','(G(moving -> F arrive) & G(processing -> F completion)) -> G(started -> F done)','Under the valid fixed-sequence input contract, eventual external feedback permits every started route to complete.'))
test(t,'bidirectional_route','Follow [4,2,5] and ignore a wrong completion input.',D,[({}, {'conveyorLeft':False,'conveyorRight':False}),({'sensor1':True,'station1Start':True},{'conveyorRight':True,'conveyorLeft':False}),({'sensor4':True},{'conveyorRight':False,'conveyorLeft':False}),({'sensor4':True,'station3Complete':True},{'conveyorRight':False,'conveyorLeft':False}),({'sensor4':True,'station4Complete':True},{'conveyorLeft':True,'conveyorRight':False}),({'sensor2':True},{'conveyorLeft':False,'conveyorRight':False}),({'sensor2':True,'station2Complete':True},{'conveyorRight':True,'conveyorLeft':False}),({'sensor5':True},{'conveyorLeft':False,'conveyorRight':False})])
D1={**D,'processLength':1,'processSequence':[5,0,0,0,0,0,0,0]}
test(t,'minimum_length','A one-entry sequence goes directly to output.',D1,[({}, {'conveyorRight':False}),({'sensor1':True,'station1Start':True},{'conveyorRight':True,'conveyorLeft':False}),({'sensor5':True},{'conveyorRight':False,'conveyorLeft':False})])
D2={**D,'processLength':3,'processSequence':[2,2,5,0,0,0,0,0]}
test(t,'repeat_station','A held completion cannot skip a repeated processing operation.',D2,[({}, {'conveyorRight':False}),({'sensor1':True,'station1Start':True},{'conveyorRight':True}),({'sensor2':True},{'conveyorRight':False}),({'sensor2':True,'station2Complete':True},{'conveyorRight':False}),({'sensor2':True,'station2Complete':True},{'conveyorRight':False}),({'sensor2':True},{'conveyorRight':False}),({'sensor2':True,'station2Complete':True},{'conveyorRight':True,'conveyorLeft':False})])
save(t)

# Slab thickness
D=dict(THICKNESS_FAULT=False,THICKNESS_SIGNAL_VALID=True,CUTTING_RUN=False,FaultTimestamp=0,CycleTime='T#100ms')
t=base(12,'Thickness monitoring records faults, alarm minimum holding, normal-cutting time and bounded history.',dict(THICKNESS_ALARM=False,Slab_Fault_Counter=0,Slab_Runtime_Accumulator='LTIME#0ns',Slab_Fault_History=[0]*5),['The counted signal is valid AND fault; a valid fault after signal loss is a new occurrence.','Hold starts at elapsed zero on the trigger call and releases at 500ms if the fault is absent. A fresh rising trigger restarts the hold.','Invalid input cancels the hold immediately.','Positive CycleTime is added on every current qualifying call, including a normal first invocation.','UINT/LTIME overflow is outside these bounded cases and requires a separate policy.'],['Invalid signal overrides minimum alarm holding.','A persistent valid fault keeps the alarm on.','Statistics never control cutting permissives.'])
spec(t,dict(valid='THICKNESS_SIGNAL_VALID',fault='THICKNESS_FAULT',alarm='THICKNESS_ALARM',rise='valid AND fault AND NOT previous(valid AND fault)',record='count=pre-count+1; history[0]=FaultTimestamp; history[j]=pre-history[j-1] for j=1..4',same_stats='count and history equal pre-scan values',hold='trigger age<500ms with no intervening signal loss',normal='valid AND NOT fault AND CUTTING_RUN',add='runtime=pre-runtime+CycleTime',same_time='runtime=pre-runtime'),
 ('Signal loss','G(!valid -> !alarm)','Invalid signal cancels alarm immediately.'),
 ('Fault hold','G(valid & (fault | hold) -> alarm)','The alarm persists during fault and hold.'),
 ('Occurrence','G(rise -> record)','Each valid rising fault shifts the bounded history.'),
 ('No spurious record','G(!rise -> same_stats)','Held faults and invalid inputs do not create records.'),
 ('Runtime','G((normal -> add) & (!normal -> same_time))','Normal runtime counts only eligible intervals.'),
 ('Release','G(valid & !fault & !hold -> !alarm)','Alarm releases when neither fault nor hold remains.'))
test(t,'hold','Check 500ms release and immediate signal-loss override.',D,[({}, {'THICKNESS_ALARM':False,'Slab_Fault_Counter':0},0),({'THICKNESS_FAULT':True,'FaultTimestamp':101},{'THICKNESS_ALARM':True,'Slab_Fault_Counter':1,'Slab_Fault_History':[101,0,0,0,0]},100),({}, {'THICKNESS_ALARM':True},100),({}, {'THICKNESS_ALARM':True},300),({}, {'THICKNESS_ALARM':False},100),({'THICKNESS_FAULT':True,'FaultTimestamp':102},{'THICKNESS_ALARM':True,'Slab_Fault_Counter':2},100),({'THICKNESS_SIGNAL_VALID':False,'THICKNESS_FAULT':True},{'THICKNESS_ALARM':False,'Slab_Fault_Counter':2},10)])
seq=[({}, {'Slab_Fault_Counter':0},0)]
for i in range(1,7):
    seq.extend([({'THICKNESS_FAULT':True,'FaultTimestamp':i},{'Slab_Fault_Counter':i,'Slab_Fault_History':list(range(i,max(0,i-5),-1))+[0]*max(0,5-i)},100),({}, {},100)])
test(t,'history','Six faults retain the five newest timestamps.',D,seq)
test(t,'runtime','Only valid fault-free running accumulates.',D,[({'CUTTING_RUN':True},{'Slab_Runtime_Accumulator':'LTIME#100ms'},0),({'CUTTING_RUN':True},{'Slab_Runtime_Accumulator':'LTIME#200ms'},100),({'CUTTING_RUN':True,'THICKNESS_FAULT':True},{'Slab_Runtime_Accumulator':'LTIME#200ms'},100),({'CUTTING_RUN':True,'THICKNESS_SIGNAL_VALID':False},{'Slab_Runtime_Accumulator':'LTIME#200ms'},100),({}, {'Slab_Runtime_Accumulator':'LTIME#200ms'},100)])
save(t)

# Office HVAC
D=dict(OCCUPANCY_DETECTED=False,ENERGY_SAVING_MODE=False,HVAC_MODE_SELECTOR=0)
t=base(13,'An office fan uses a restartable occupancy delay and mode-dependent temperature setback.',dict(SUPPLY_FAN_RUN=False,TEMP_SETPOINT_ADJUST=0),['Selector values are always 0..3 as required by the official input contract.','Outputs are initialized before the first call, which calculates adjustment immediately.','The timer starts at elapsed zero on the first non-Night occupied call. Fan starts at the first observation at or after 30s.','dt_ms is actual elapsed time since the preceding call; real runtime timer tests must preserve this timing.'],['Occupancy loss or Night immediately stops fan and resets delay.','Energy saving affects only Auto setback.'])
spec(t,dict(permit='OCCUPANCY_DETECTED AND HVAC_MODE_SELECTOR<>3',mature='continuous permit elapsed>=30s',fan='SUPPLY_FAN_RUN',bounded='-4<=TEMP_SETPOINT_ADJUST<=4',occupied='OCCUPANCY_DETECTED AND mode<>3',zero='TEMP_SETPOINT_ADJUST=0',night='mode=3',four='adjust=4',auto_save='mode=0 AND NOT occupancy AND ENERGY_SAVING_MODE',three='adjust=3',auto_standard='mode=0 AND NOT occupancy AND NOT ENERGY_SAVING_MODE',two='adjust=2',comfort='mode=1 AND NOT occupancy',one='adjust=1',economy='mode=2 AND NOT occupancy'),
 ('Fan delay','G(fan <-> (permit & mature))','Fan follows the complete uninterrupted delay.'),
 ('Bounds','G(bounded)','Legal outputs satisfy the required range.'),
 ('Occupied and Night','G((occupied -> zero) & (night -> four))','Night overrides occupied setback.'),
 ('Auto','G((auto_save -> three) & (auto_standard -> two))','Auto unoccupied setback follows energy saving.'),
 ('Fixed modes','G((comfort -> one) & (economy -> four))','Comfort and Economy ignore energy saving.'),
 ('Liveness','G((G permit) -> F fan)','If permit stays TRUE from any scan onward, the fan eventually runs, assuming continued calls and diverging physical time.'))
test(t,'mode_table','Exercise all setback modes and energy saving scope.',D,[({}, {'SUPPLY_FAN_RUN':False,'TEMP_SETPOINT_ADJUST':2},0),({'ENERGY_SAVING_MODE':True},{'TEMP_SETPOINT_ADJUST':3},100),({'HVAC_MODE_SELECTOR':1},{'TEMP_SETPOINT_ADJUST':1},100),({'HVAC_MODE_SELECTOR':1,'ENERGY_SAVING_MODE':True},{'TEMP_SETPOINT_ADJUST':1},100),({'HVAC_MODE_SELECTOR':2},{'TEMP_SETPOINT_ADJUST':4},100),({'HVAC_MODE_SELECTOR':3,'OCCUPANCY_DETECTED':True},{'TEMP_SETPOINT_ADJUST':4,'SUPPLY_FAN_RUN':False},100),({'HVAC_MODE_SELECTOR':2,'OCCUPANCY_DETECTED':True},{'TEMP_SETPOINT_ADJUST':0,'SUPPLY_FAN_RUN':False},100)])
test(t,'delay_restart','Check delay boundary, loss, full restart, Night override.',D,[({'OCCUPANCY_DETECTED':True},{'SUPPLY_FAN_RUN':False},0),({'OCCUPANCY_DETECTED':True},{'SUPPLY_FAN_RUN':False},29900),({'OCCUPANCY_DETECTED':True},{'SUPPLY_FAN_RUN':True},100),({}, {'SUPPLY_FAN_RUN':False},100),({'OCCUPANCY_DETECTED':True},{'SUPPLY_FAN_RUN':False},100),({'OCCUPANCY_DETECTED':True},{'SUPPLY_FAN_RUN':False},29900),({'OCCUPANCY_DETECTED':True},{'SUPPLY_FAN_RUN':True},100),({'OCCUPANCY_DETECTED':True,'HVAC_MODE_SELECTOR':3},{'SUPPLY_FAN_RUN':False},100)])
save(t)

# Recipe management
EMPTY=dict(recipeID=0,ingredientType=0,ingredientRatio=0.0,productionTemperature=0.0)
def rec(i,ratio=.5,temp=80.0):return dict(recipeID=i,ingredientType=i,ingredientRatio=ratio,productionTemperature=temp)
D=dict(addRecipe=False,deleteRecipe=False,modifyRecipe=False,queryRecipe=False,recipeIn=EMPTY)
t=base(17,'A bounded recipe database supports atomic add/delete/modify/query and deterministic empty-slot selection.',dict(recipe=[EMPTY.copy() for _ in range(10)],recipeAdded=False,recipeDeleted=False,recipeModified=False,recipeQueryResult=EMPTY,error=False,status=0),['At most one request rises per call. Requests use rising edges; simultaneous request priority is unspecified by the source.','Only positive nonzero IDs are submitted; zero denotes an unused slot.','Success indicators are one-invocation pulses. error/status clear on idle.','recipeQueryResult retains the last successful query until another successful query.','Deleting a record clears only its recipeID; its other fields become unconstrained.','The caller-owned recipe array is initialized once and persists across steps; do not overwrite it with initial values per scan.','Compare REAL values with absolute tolerance 1e-5.'],['Duplicate checking precedes database-full checking.','Failed requests must not mutate the database.','Insertion uses the lowest-index empty slot.'])
t['supporting_types']=[dict(name='ST_Recipe',kind='DUT',declaration='TYPE ST_Recipe :\nSTRUCT\n recipeID : INT;\n ingredientType : INT;\n ingredientRatio : REAL;\n productionTemperature : REAL;\nEND_STRUCT\nEND_TYPE',source='Official field table; types unchanged.')]
t['test_bindings']=dict(recipe=dict(type='ARRAY[1..10] OF ST_Recipe',initial=[EMPTY.copy() for _ in range(10)],persistence='VAR_IN_OUT caller storage retained across all steps.'))
spec(t,dict(q_missing='rising(queryRecipe) AND ID absent from pre-database',a_dup='rising(addRecipe) AND ID exists',a_full='rising(addRecipe) AND ID absent AND all slots full',d_missing='rising(deleteRecipe) AND ID absent',m_missing='rising(modifyRecipe) AND ID absent',e1='error AND status=16#8001',e2='error AND status=16#8002',e3='error AND status=16#8003',e4='error AND status=16#8004',e5='error AND status=16#8005',error='error output',same='database equals pre-database',add_ok='rising(addRecipe) AND positive ID absent AND empty slot exists',insert='lowest-index pre-empty slot equals recipeIn; all other slots unchanged',add_success='recipeAdded AND NOT error AND status=0',query_ok='rising(queryRecipe) AND matching record exists',result='recipeQueryResult equals matching pre-record',idle='no rising request',clear='NOT error AND status=0 AND NOT recipeAdded AND NOT recipeDeleted AND NOT recipeModified',unique='all nonzero IDs are pairwise distinct'),
 ('Errors','G((q_missing -> e1) & (a_dup -> e2) & (a_full -> e3) & (d_missing -> e4) & (m_missing -> e5))','Distinct failures produce the official status codes.'),
 ('No mutation','G(error -> same)','Rejected operations preserve all records.'),
 ('Lowest insertion','G(add_ok -> (insert & add_success))','Adds use the lowest free slot.'),
 ('Query','G(query_ok -> result)','Query returns the complete matched record.'),
 ('Idle','G(idle -> clear)','Indicators and invocation errors clear on idle.'),
 ('Uniqueness','G(unique)','All operations preserve ID uniqueness from a valid initial database.'))
test(t,'CRUD','Add, query, modify, delete and reuse the first empty slot.',D,[({}, {'error':False,'status':0}),({'addRecipe':True,'recipeIn':rec(1)},{'recipeAdded':True,'error':False,'status':0}),({}, {'recipeAdded':False}),({'queryRecipe':True,'recipeIn':rec(1)},{'recipeQueryResult':rec(1),'error':False}),({},{}),({'modifyRecipe':True,'recipeIn':rec(1,.75,90.)},{'recipeModified':True,'error':False}),({}, {'recipeModified':False}),({'queryRecipe':True,'recipeIn':rec(1)},{'recipeQueryResult':rec(1,.75,90.)}),({},{}),({'deleteRecipe':True,'recipeIn':rec(1)},{'recipeDeleted':True,'error':False}),({}, {'recipeDeleted':False}),({'addRecipe':True,'recipeIn':rec(2)},{'recipeAdded':True,'error':False}),({},{}),({'queryRecipe':True,'recipeIn':rec(2)},{'recipeQueryResult':rec(2)})],notes='Bind persistent recipe storage once. Inspect recipe[1].recipeID=2 after reuse; deleted non-ID fields are unconstrained.')
test(t,'missing_duplicate','All missing-record errors and duplicate rejection preserve existing record.',D,[({'queryRecipe':True,'recipeIn':rec(9)},{'error':True,'status':32769}),({}, {'error':False,'status':0}),({'deleteRecipe':True,'recipeIn':rec(9)},{'error':True,'status':32772}),({},{}),({'modifyRecipe':True,'recipeIn':rec(9)},{'error':True,'status':32773}),({},{}),({'addRecipe':True,'recipeIn':rec(1)},{'recipeAdded':True,'error':False}),({},{}),({'addRecipe':True,'recipeIn':rec(1,.9,100.)},{'error':True,'status':32770,'recipeAdded':False}),({},{}),({'queryRecipe':True,'recipeIn':rec(1)},{'recipeQueryResult':rec(1),'error':False})])
seq=[]
for i in range(1,11):seq.extend([({'addRecipe':True,'recipeIn':rec(i)},{'recipeAdded':True,'status':0}),({}, {'recipeAdded':False,'status':0})])
seq.extend([({'addRecipe':True,'recipeIn':rec(11)},{'error':True,'status':32771}),({},{}),({'addRecipe':True,'recipeIn':rec(1)},{'error':True,'status':32770})])
test(t,'capacity_priority','Fill ten slots; duplicate error has priority over full error.',D,seq)
save(t)

# Generic FIFO
D=dict(enqueue=False,dequeue=False,reset=False,item=0)
t=base(18,'A generic circular FIFO derives capacity/type from caller storage and handles edge requests, wraparound and rejection.',dict(elementCount=0,status=0,head=0,tail=0),['The official VARIANT interface is preserved. Native CODESYS compatibility and runtime type/array metadata access remain unverified; never silently replace it by a DINT-only interface.','Binding A: item DINT, buffer ARRAY[0..1] OF DINT. Binding B: item BOOL, buffer ARRAY[1..3] OF BOOL. Both must run to substantiate genericity.','Buffer is initialized and bound once per test; its association and contents are not externally overwritten between calls. item is caller-writable every scan.','Enqueue and dequeue are never requested together. Reset may coincide with either and wins.','Edge memories update during reset; a request held afterward is not another edge.','Reset need not clear buffer values. Unused storage arrangement is unconstrained.'],['Reset empties the logical queue before handling requests.','Rejected requests preserve queue and item.','Only rising edges perform enqueue/dequeue.'])
t['portability']=dict(status='UNVERIFIED',issue='VARIANT is an official interface but may not be a native CODESYS generic type in the selected profile. A verified variant-reflection library or explicitly disclosed adapter may be required.',required_validation='Compile the unchanged generic interface, verify two element types and different lower bounds/capacities. Adapter results must disclose deviations.')
t['test_bindings']=[dict(id='A',item_type='DINT',buffer_type='ARRAY[0..1] OF DINT',buffer_initial=[0,0],capacity=2),dict(id='B',item_type='BOOL',buffer_type='ARRAY[1..3] OF BOOL',buffer_initial=[False,False,False],capacity=3)]
spec(t,dict(reset='reset input',empty='elementCount=0',ok='status=0',pop_empty='NOT reset AND rising(dequeue) AND pre-count=0',push_full='NOT reset AND rising(enqueue) AND pre-count=capacity',e1='status=16#8001',e2='status=16#8002',same='logical queue equals pre-queue AND item equals sampled item',push='NOT reset AND rising(enqueue) AND pre-count<capacity',pushed='post-queue=pre-queue appended with sampled item AND count=pre-count+1 AND status=0',pop='NOT reset AND rising(dequeue) AND pre-count>0',popped='item=pre-front AND post-queue=pre-queue without front AND count=pre-count-1 AND status=0',bounded='0<=elementCount<=actual buffer length',idle='NOT reset AND no request rising edge'),
 ('Reset','G(reset -> (empty & ok))','Reset overrides simultaneous requests.'),
 ('Rejections','G((pop_empty -> (e1 & same)) & (push_full -> (e2 & same)))','Full and empty failures preserve data.'),
 ('FIFO order','G((push -> pushed) & (pop -> popped))','Accepted edges update the ordered logical queue exactly once.'),
 ('Count','G(bounded)','Count remains within the actual caller capacity.'),
 ('Held request','G(idle -> (ok & same))','Held levels do not perform another operation.'))
test(t,'wrap_full_empty','Capacity-two FIFO preserves order through wrap, full and empty rejection.',D,[({}, {'elementCount':0,'status':0}),({'enqueue':True,'item':10},{'elementCount':1}),({'enqueue':True,'item':99},{'elementCount':1}),({},{}),({'enqueue':True,'item':20},{'elementCount':2}),({},{}),({'enqueue':True,'item':30},{'elementCount':2,'status':32770,'item':30}),({},{}),({'dequeue':True,'item':-1},{'elementCount':1,'status':0,'item':10}),({},{}),({'enqueue':True,'item':30},{'elementCount':2}),({},{}),({'dequeue':True},{'elementCount':1,'item':20}),({},{}),({'dequeue':True},{'elementCount':0,'item':30}),({},{}),({'dequeue':True,'item':77},{'elementCount':0,'status':32769,'item':77})],binding_id='A')
test(t,'reset_priority','Reset coincides with request; held request after reset does not execute.',D,[({'enqueue':True,'item':10},{'elementCount':1}),({},{}),({'reset':True,'enqueue':True,'item':20},{'elementCount':0,'status':0,'item':20}),({'enqueue':True,'item':30},{'elementCount':0,'status':0}),({},{}),({'enqueue':True,'item':40},{'elementCount':1}),({},{}),({'reset':True,'dequeue':True,'item':50},{'elementCount':0,'status':0,'item':50})],binding_id='A')
DB={**D,'item':False}
test(t,'generic_BOOL','Second element type and lower-bound-one buffer.',DB,[({'enqueue':True,'item':True},{'elementCount':1}),({},{}),({'enqueue':True,'item':False},{'elementCount':2}),({},{}),({'enqueue':True,'item':True},{'elementCount':3}),({},{}),({'dequeue':True,'item':False},{'elementCount':2,'item':True}),({},{}),({'dequeue':True,'item':True},{'elementCount':1,'item':False})],binding_id='B')
save(t)
