"""Normalize all task contracts, preserving original requirements and test data."""
from copy import deepcopy
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from plc_agent.common import digest, read_json, write_json
from plc_agent.dataset import load_tasks, validate
from plc_agent.normalized_spec import CONTRACT_FILES, NormalizedScanMonitor, reference_step, canonical_source_bytes
from plc_agent.scan_contract import ScanContract

VERSION = '2.1-normalized-20261111'
ARCHIVE = ROOT / 'dataset_versions/before_normalization_20261111'
FROZEN = ROOT / 'dataset/specifications/normalized_transition_v1'

# These are descriptions of fixed definitions, not instructions to finish them.
RULES = {
'PUB001': '参考阶段q初值0。事件按q选bottleSensor、cleaningConfirmButton、fillingConfirmButton、cappingConfirmButton、packingConfirmButton、finishedButton；选中事件真则qAfter=(q+1)%6，否则qAfter=q。五个期望输出依次为qAfter=1、2、3、4、5，每拍只选择旧q的一个分支。',
'PUB002': 'prev初值DWORD#0。rise=value & (~prev & 0xFFFFFFFF)，fall=prev & (~value & 0xFFFFFFFF)。两个掩码、popcount、掩码非零标志和value!=prev标志分别与实际七个输出比较；prevAfter=value，每次调用更新一次。',
'PUB003': '四个REAL参数先按IEEE binary32舍入且有限，hystWindow>=0。lo>=hi时报8001，否则width>=real32(hi-lo)时报8002；错误时参考高低报警保持。有效时高报警由value>hi置真、value<real32(hi-width)置假、其余保持；低报警由value<lo置真、value>real32(lo+width)置假、其余保持。初值均FALSE。',
'PUB004': '物理采样时钟首拍0、以后累加dt_ms。permit=VISCOSITY_OK & PASTE_E_STOP_NC；首次permit真时记录起点，假时清起点，run=permit且年龄>=固定正DebounceTime。acc初值0；accAfter=accBefore+(run?CycleTime:0)，CycleTime先解释为纳秒；maint=accAfter>=500h。累计域0..2^63-1纳秒。',
'PUB005': '首拍时钟0；startup=clock<5s，急停不重启此时钟。gapPermit=!startup & Gap_Exceeded & Weld_E_Stop_NC；首次gapPermit真年龄0，假清起点；alarm=gapPermit且年龄>=固定正DebounceTime。两个期望输出为alarm、startup。',
'PUB006': 'permit=DO_LOW & AERATION_E_STOP_NC；首次真年龄0，假清计时；run=permit且年龄>=5s。countAfter=countBefore+int(run & !refRunBefore)，初始count=0/refRun=FALSE；每拍更新refRun。计数域0..65535，越界输入历史不在评测域。',
'PUB007': '数组序号j=0..4，对应PLC下标j+1。stop时全部RunComd=FALSE；否则start时手动取selection，自动取按(-priority,j)升序排列的前三项；无start保持采样RunComd。priority和selection实际扫描后必须精确等于采样值。',
'PUB008': '序号j=0..len(channels)-1；仅j<count且enable处理，0<=count<=min两数组长度。非法mode优先报8001，否则hi<=lo报8002，均保留采样outputValue；成功清码，mode0按单极raw/27648或双极(raw+27648)/55296线性映射，mode1/2分别raw/10、raw/100。其他项及配置精确保留，仅成功outputValue使用abs=1e-5、rel=2e-6。',
'PUB009': 'previousTrigger初值FALSE且每次调用后=本拍trigger。valid=1<=windowSize<=100；非法时average/reached保持并报8200。有效窗口首次建立或改变、或reset时清空历史；非reset且cyclicExecution或trigger上升沿时追加value并保留最后windowSize项。average=空则0否则sum/n，reached=(n=windowSize)。初始历史空、average=0、reached=FALSE。',
'PUB010': '时钟由观察dt_ms累加。demand低于设定置真、高于置假、相等保持，初值FALSE。先释放年龄>=3s的旧保护；无旧保护且旧连续加热年龄>=5s则本拍触发保护。heat=传感器0..100有效 & demandAfter & 无保护；首次heat真记录当前时刻，heat假清热起点。显示值取输入；保护输出取保护状态。>=5s是既有评测解释，并非老师额外澄清。',
'PUB011': '参考阶段WAIT_A/MOVE_AB/WAIT_B/MOVE_BC/WAIT_C/DONE初始WAIT_A；按SensorA&ButtonA、SensorB、SensorB&ButtonB、SensorC、SensorC&ButtonC、!SensorC分别推进一阶。手动清参考阶段，正反转分别为ForwardButton&!ReverseButton及反向对称式，灯灭；自动仅移动阶段正转、不反转，DONE且SensorC时灯亮。',
'PUB012': 'validFault=VALID & FAULT，其新上升沿count加1，历史=[FaultTimestamp]+旧历史前4项，并记录hold起点。无效清hold；alarm=valid & (fault或hold年龄<500ms)。valid & !fault & CUTTING_RUN时runtime加CycleTime，否则保持。初始count/runtime=0、历史五个0、previousValidFault=FALSE。计数/累计不得溢出。',
'PUB013': 'mode域0..3；permit=occupied & mode!=3，首次许可年龄0、失去立即清计时；fan=permit且年龄>=30s。adjust=mode3则4，否则有人则0，否则mode0取节能3/普通2、mode1取1、mode2取4。初始化adjust=0与首次调用计算分开。',
'PUB014': '文本取首NUL之前且容量<=254字节。恰四个非空ASCII数字段，每段按a=10*a+digit递推，任何段>255或非数字即非法。允许前导零。合法期望ipValue=((a*256+b)*256+c)*256+d，否则0；无跨拍状态。',
'PUB015': '五按钮及autoStart历史初值FALSE、每拍更新。急停优先，其次已建立模式的变化；二者清阶段/五锁存且当拍全关。手动逐项latchAfter=latchBefore XOR buttonRise。自动IDLE遇autoStartRise进A，A液位>=50进B，B>=80按批次processMode进C或MIX，C>=100进MIX，MIX完成进DRAIN；每拍一阶，DRAIN保持至复位条件。五输出对应转移后A/B/C/DRAIN/MIX。批次模式在活动批次内固定。',
'PUB016': '活动路线长度1..8，前项为2/3/4且末项5，活动周期内固定。初始IDLE、station=1、index=0。IDLE在station1Start上升沿且sensor1时选择首目标；MOVING到目标后进入WAIT_PROCESS或目标5回IDLE；WAIT_PROCESS仅对应完成新边沿推进index，同站继续等待。输出仅转移后MOVING且未到目标时按target与station方向开启；所有边沿历史逐拍更新。',
'PUB017': '数据库首拍由调用前recipe初始化，之后为跨拍保留存储；非零ID唯一，输入ID正且每拍至多一个请求上升沿。四请求历史初值FALSE、每拍更新。查询缺失8001；新增重复8002优先于满库8003，否则最低空位整体写入；删除缺失8004否则只清ID；修改缺失8005否则整体替换。失败/空闲库保持。三个成功输出是单拍脉冲，成功/空闲error=FALSE/status=0；查询结果仅成功查询时更新，初值零记录。成功删除槽的非ID字段当拍不受约束，此后无覆盖操作时与采样实际值比较保持；不把这些物理表示字段写回参考数据库。',
'PUB018': '独立逻辑队列Q初始空、enqPrev/deqPrev=FALSE。reset优先QAfter=[]；否则单个enqueue新沿且未满时追加采样item，满报8002；dequeue新沿且非空时返回旧队首并去首，空报8001；其余状态0。elementCount=|QAfter|；仅成功pop改变实际item，其余等于采样item。buffer物理布局不受约束，其正确性由完整可观察出队行为约束。绑定A容量2、B容量3，其余容量由实际buffer元数据固定。',
'PUB019': '八动作顺序为下/夹/上/右/下/松/上/左。安全失去或无模式全关复位，其次模式变化当拍全关复位；模式选择互斥。手动六命令分别=本按钮 & !反向按钮 & !本限位。单步完成时全关、保存下一步，新Start沿再启动；首步要求上左到位。单周期末回IDLE；连续末回第一步；自动只在本动作匹配限位时推进一阶，输出按转移后动作并由本限位门控。Start历史每拍更新。',
'PUB020': '参考阶段WAIT_FEED→MOVE_WASH→WAIT_WASH→MOVE_WEIGHT→WAIT_WEIGHT→REJECT或MOVE_FIRING→WAIT_FIRING→MOVE_OUTPUT→OUTPUT_DONE；每拍按旧阶段只推进一阶。重量100..200含边界合格，合格温度real32(500+real32(real32(weight-100)*0.5))；不合格保持温度并剔除至SensorWeight假。完成取走后回初始。手动清流程、方向按钮互锁、kick/灯关闭、温度保持。自动仅运输阶段正转、不反转；kick对应REJECT、灯对应OUTPUT_DONE。',
'SELF001': 'r初值FALSE；rAfter=GuardClosed & !Stop & (Start | rBefore)；期望Run=rAfter。',
'SELF002': 'd初值0；desired在Stop或两方向按钮相等时为0，否则前进1/后退-1。dAfter在desired!=0且dBefore=-desired时为0，否则desired；Forward=(dAfter=1)，Reverse=(dAfter=-1)。',
'SELF003': 'required初值TRUE、run初值FALSE。按顺序选择首个分支：!EStopNC置required=TRUE/run=FALSE；旧required真时run=FALSE，仅Reset & !Start & !Stop清required；否则Stop清run、否则Start置run，其余保持。两个实际输出分别比较runAfter、requiredAfter。',
'SELF004': 'mode初值IDLE。优先Jam→FAULT，其次Reset→IDLE，其次旧FAULT保持，其次Stop→IDLE，其次旧MOVING且AtExit→COMPLETE，其次旧IDLE且Start且!AtExit→MOVING，其余保持。Belt/Complete/Fault分别等价于新mode为MOVING/COMPLETE/FAULT。',
'SELF005': 'phase=0/age=0初值。!Enable时重置0/0；否则Tick时age加1，到当前phase的阈值(2,3,1)则phase=(phase+1)%3且age=0；其他保持。Red/Green/Amber分别等价于新phase=0/1/2，Phase等于新phase。Tick是逻辑调用计数，不是物理时间。',
'SELF006': 'fill初值FALSE；sensorFault=HighWet & !LowWet。sensorFault或Inhibit或HighWet时fillAfter=FALSE，否则!LowWet时TRUE，其余保持；实际Fill/SensorFault分别比较这两个期望值。',
'SELF007': 'leadA=TRUE/served=FALSE/previousDemand=FALSE初值。Demand假时双泵关，仅previousDemand & served时轮换leadA，然后清served；Demand真时由leadA选择无故障主泵，主故障则无故障备用，双故障均关；served累计本需求段任一泵运行。previousDemand每拍=Demand，LeadA比较转移后偏好。',
'SELF008': 'count初值0；Preset有效域1..5。!Request或Trip或非法Preset时countAfter=0，否则min(countBefore+1,Preset)；Count比较该值，Ready=有效且countAfter>=Preset。',
'SELF009': 'count=0/pulsePrev=FALSE初值。invalid=Target不在1..20；invalid或Reset时countAfter=0，否则min(countBefore+int(PartPulse & !pulsePrev),Target)。Complete=!invalid & !Reset & countAfter>=Target，Error=invalid；pulsePrev每拍更新为PartPulse。',
'SELF010': 'latched/ack/previousFault初值FALSE。Reset & !Fault时清latched/ack；否则Fault时置latched，若Fault新沿清ack、否则Ack置ack；否则旧latched且Ack置ack，其余保持。Alarm=latchedAfter，Acknowledged=ackAfter，Horn=latchedAfter & !ackAfter。previousFault每拍=Fault。',
'SELF011': 'mode初值IDLE。Stop或Reset优先回IDLE；IDLE且Start & RetractDone进EXTEND；EXTEND/CLAMP/RELEASE/RETRACT仅各自匹配完成信号推进一阶；DONE保持。四动作输出分别等价于转移后对应阶段，Busy等价于阶段1..4，Done等价于阶段5。',
'SELF012': 'mode=IDLE/attempts=0/free=0初值。优先Reset & !Fault & !Start清全部；其次LOCKED保持；其次Stop回IDLE并清free但保留attempts；RUNNING且Fault转WAIT或已重试2次转LOCKED；WAIT中Fault清free否则加1，free>=2时attempts加1并回RUNNING、free=0；IDLE且Start & !Fault进RUNNING。输出Run/Locked取新mode，Attempts取新attempts。',
}

OBS_HISTORY = {
'PUB003': {'hiPrev':'hiAlarm','loPrev':'loAlarm'},
'PUB004': {'accPrev':'PUMP_RUNTIME_ACC'},
'PUB006': {'runPrev':'BLOWER_RUN','countPrev':'AERATION_BLOWER_CYCLE_COUNT'},
'PUB010': {'protectPrev':'OverheatProtection'},
'SELF001': {'qRun':'Run'}, 'SELF002': {'qForward':'Forward','qReverse':'Reverse'},
'SELF003': {'qRun':'Run','qRequired':'ResetRequired'},
'SELF006': {'qFill':'Fill'}, 'SELF007': {'qLeadA':'LeadA'},
'SELF008': {'qCount':'Count'}, 'SELF009': {'qCount':'Count'},
'SELF010': {'qAlarm':'Alarm','qAck':'Acknowledged'},
'SELF012': {'qAttempts':'Attempts'},
}
INPUT_HISTORY = {'PUB002': {'prev':('value',0)}, 'PUB009':{'previousTrigger':('trigger',False)},
                 'SELF009':{'qPulse':('PartPulse',False)},'SELF010':{'qFault':('Fault',False)}}
TIMED_LIVENESS={'PUB004':{'P7'},'PUB005':{'P5'},'PUB006':{'P5'},
                'PUB010':{'P8'},'PUB013':{'PUB013.P6'}}


def plain_state(value):
    if isinstance(value, Decimal): return {'decimal':str(value)}
    if isinstance(value, dict): return {k:plain_state(v) for k,v in value.items()}
    if isinstance(value, (list,tuple)): return [plain_state(v) for v in value]
    if hasattr(value,'__dict__'): return {'class':type(value).__name__,'state':plain_state(vars(value))}
    return value


def auxiliary_bindings(tid):
    """Bind legacy state vocabulary to exact reference paths, not candidate internals."""
    result = {
        'Spre': 'Sref[k], before the invocation; initialized by reference_state_initial',
        'Spost': 'Sref[k+1], after exactly one pinned transition on I[k]',
        'first': 'k=0 (first invocation); distinct from the pre-invocation initial observation',
        'pre-output': 'actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT',
        'previous-input': 'I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation',
        'reference_warning': 'Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.',
    }
    phases = {
        'PUB001': ('phase', ['IDLE','CLEANING','FILLING','CAPPING','PACKING','COMPLETE']),
        'PUB011': ('phase', ['WAIT_A','MOVE_AB','WAIT_B','MOVE_BC','WAIT_C','DONE']),
        'PUB015': ('process_contract.phase', ['IDLE','FILL_A','FILL_B','FILL_C','MIX','DRAIN']),
        'PUB016': ('process_contract.phase', ['IDLE','MOVING','WAIT_PROCESS']),
        'PUB020': ('process_contract.phase', ['WAIT_FEED','MOVE_TO_WASH','WAIT_WASH','MOVE_TO_WEIGHT','WAIT_WEIGHT','REJECT','MOVE_TO_FIRING','WAIT_FIRING','MOVE_TO_OUTPUT','OUTPUT_DONE']),
        'SELF004': ('reference.state.mode', ['IDLE','MOVING','COMPLETE','FAULT']),
        'SELF005': ('reference.state.phase', ['RED','GREEN','AMBER']),
        'SELF011': ('reference.state.mode', ['IDLE','EXTEND','CLAMP','RELEASE','RETRACT','DONE']),
        'SELF012': ('reference.state.mode', ['IDLE','RUNNING','WAIT','LOCKED']),
    }
    if tid in phases:
        path, labels = phases[tid]
        result.update(phase={'pre': 'Spre.'+path, 'post': 'Spost.'+path,
                            'enum': dict(enumerate(labels)), 'initial': 0})
    if tid == 'PUB016':
        result.update(targetStation='Spre.process_contract.target', currentStation='Spre.process_contract.station',
                      route='Spre.process_contract.route', index='Spre.process_contract.index')
    if tid == 'PUB015':
        result['modeChanged']='Spre.process_contract.mode is not None AND Spre.process_contract.mode != I[k].opeMode'
    if tid == 'PUB019':
        result.update(action_index={'pre_cycle':'Spre.process_contract.arm_step', 'pre_single_step':'Spre.process_contract.step_index',
            'initial_cycle':0,'initial_single_step':1,
            'enum':{1:'DOWN',2:'GRIP',3:'UP1',4:'RIGHT',5:'DOWN2',6:'RELEASE',7:'UP2',8:'LEFT'},
            'feedback':['DownLimitSwitch','GripLimitSwitch','UpLimitSwitch','RightLimitSwitch','DownLimitSwitch','ReleaseLimitSwitch','UpLimitSwitch','LeftLimitSwitch']},
            busy='SingleStepMode ? Spre.process_contract.step_busy : Spre.process_contract.arm_step != 0',
            modeChanged='Spre.process_contract.arm_mode is not None AND differs from selected input mode (manual/single_step/single_cycle/continuous/None)',
            mode_initial=None, start_memory='Spre.process_contract.prev_start, initially FALSE; next=I[k].Start')
    if tid in ('PUB004','PUB005','PUB006','PUB012','PUB013'):
        result['timing']={'clock':'Spost.timed_contract.clock (exact integer nanoseconds; first invocation 0)',
            'start':'Spost.timed_contract.since; None means inactive',
            'qualified':'start is not None AND clock-start >= duration_ns(limit)',
            'hold':'start is not None AND clock-start < 500000000',
            'initial_start':None,'initial_clock':0,
            'limit':'DebounceTime for PUB004/PUB005, 5000000000ns for PUB006, 30000000000ns for PUB013',
            'previous_fault':'Spre.timed_contract.previous_fault, initially FALSE; next=THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT',
            'pre_count':'Spre.timed_contract.count','pre_history':'Spre.timed_contract.history',
            'pre_runtime':'Spre.timed_contract.runtime'}
    if tid in ('PUB017','PUB018'):
        result['storage']={'pre_database':'Spre.data_contract.recipes; first invocation uses separately sampled I[0].recipe',
            'actual_database':'O[k].recipe; preservation compares sampled I[k].recipe',
            'pre_queue':'Spre.data_contract.queue','post_queue':'Spost.data_contract.queue',
            'pre_count':'len(Spre.data_contract.queue)', 'capacity':'length of the actual caller buffer binding, fixed per case',
            'rise':'I[k].request AND NOT corresponding Spre.data_contract.prev_{add/delete/modify/query/enq/deq}',
            'initial_request_memories':False,'initial_queue':[]}
    return result


def precise_auxiliary_predicates(tid):
    maps = {
        'PUB001': {'phase':'Spre.phase (0..5); phase at the next LTL position is this scan\'s Spost.phase',
                   'oneHotOutputs':'sum(int(O[k][n]) for n in [Pump_Motor,Filling_Valve,Capping_Machine,Packing_Machine,Completion_Light]) <= 1',
                   'init':'At the separate pre-invocation initial observation: Spre.phase=0 AND each actual listed initial output is FALSE'},
        'SELF004': {'qIdle':'Spre.reference.state.mode=0','qMoving':'Spre.reference.state.mode=1','qComplete':'Spre.reference.state.mode=2','qFault':'Spre.reference.state.mode=3'},
        'SELF005': {'qRedLast':'Spre.reference.state.phase=0 AND Spre.reference.state.age=1',
                    'qGreenLast':'Spre.reference.state.phase=1 AND Spre.reference.state.age=2',
                    'qAmber':'Spre.reference.state.phase=2','qPhase':'Spre.reference.state.phase',
                    'oneColor':'int(O[k].Red)+int(O[k].Green)+int(O[k].Amber)=1'},
        'SELF007': {'completedServed':'Spre.reference.state.demand AND NOT I[k].Demand AND Spre.reference.state.served'},
        'SELF011': {**{'q'+label:'Spre.reference.state.mode='+str(j) for j,label in enumerate(['Idle','Extend','Clamp','Release','Retract','Done'])},
                    'oneAction':'int(O[k].Extend)+int(O[k].Clamp)+int(O[k].Release)+int(O[k].Retract)<=1'},
        'SELF012': {'qLocked':'Spre.reference.state.mode=3','qRunning':'Spre.reference.state.mode=1','qWait':'Spre.reference.state.mode=2',
                    'retryDue':'Spre.reference.state.mode=2 AND NOT I[k].Fault AND Spre.reference.state.free>=1'},
        'PUB014': {'same_input':'k>=1 AND I[k].ipText=I[k-1].ipText',
                   'same_output':'k>=1 AND O[k].ipValue=O[k-1].ipValue'},
    }
    return maps.get(tid,{})


def main():
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    FROZEN.mkdir(parents=True, exist_ok=True)
    modules = (*CONTRACT_FILES, 'normalized_spec.py')
    hashes = {}
    for name in modules:
        source = canonical_source_bytes(ROOT/'src/plc_agent'/name)
        target=FROZEN/name
        if target.exists() and canonical_source_bytes(target)!=source:
            raise ValueError('Frozen transition changed; create a new definition version: '+name)
        target.write_bytes(source)
        hashes[name]=hashlib.sha256(source).hexdigest()
    changes=[]
    for current in load_tasks():
        tid=current['id']; archive=ARCHIVE/(tid+'.json')
        if not archive.exists(): write_json(archive,current)
        original=read_json(archive); t=deepcopy(original)
        fields = {p['name']:p for p in t['interface']}
        initial = {k:deepcopy(v) for k,v in t['initial_conditions'].items()
                   if k in fields and fields[k]['direction']=='OUTPUT'}
        histories={}
        for alias, output in OBS_HISTORY.get(tid,{}).items():
            histories[alias]={'kind':'previous_observed_output','source':'O[k-1].'+output,
                'initial':t['initial_conditions'][output],
                'update':'After comparing scan k, store ACTUAL O[k].'+output+'; never write into reference state.'}
        for alias,(input_name,zero) in INPUT_HISTORY.get(tid,{}).items():
            histories[alias]={'kind':'previous_sampled_input','source':'I[k-1].'+input_name,
                'initial':zero,'update':'After EVERY scan k, including invalid/reset/stop, store I[k].'+input_name}
        reference=ScanContract(tid)
        covered=set()
        for case in t['tests']:
            probe=ScanContract(tid)
            for step in case['steps']:
                covered.update(reference_step(t,probe,step['inputs'],step.get('dt_ms')))
        missing={f['name'] for f in t['interface'] if f['direction'] in ('OUTPUT','IN_OUT')}-covered
        if missing and not(tid=='PUB018' and missing=={'buffer'}):
            raise ValueError('Unspecified outputs '+tid+': '+str(missing))
        rule=RULES[tid]
        relation=('令(Sref[k+1], E[k])=T_'+tid+'(Sref[k], deepCopy(I[k]), dt_ms[k])。'
                  'T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。'
                  'CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。'
                  'Sref只由采样输入推进，绝不由O或候选内部变量推进。\n'+rule)
        quantified={}
        t['specification_version']=VERSION
        for p in t['ltl']:
            old=p['formula']
            if p['id'] in TIMED_LIVENESS.get(tid,set()):
                p['formula']='(G(F(TimeTick))) -> ('+p['formula']+')'
                p['explanation']+=' Explicit non-Zeno environment premise: physical elapsed time crosses infinitely many 1ms boundaries.'
                t['atomic_propositions']['TimeTick']='Boolean: floor(t[k]/1ms)>floor(t[k-1]/1ms), with t[0]=0, TimeTick[0]=FALSE, t[k]=sum(dt_ms[1..k]). G(F(TimeTick)) states unbounded physical time progress; merely positive dt is insufficient.'
            if tid=='PUB002' and p['id']=='P6':
                p['formula']='G('+' & '.join(f'(ValueBit{b} <-> X(PrevBit{b}))' for b in range(32))+')'
                p['explanation']='For every bit b=0..31, the next sampled-input memory bit equals the current value bit. X applies only to a Boolean proposition; memory is initialized to DWORD#0.'
                for b in range(32):
                    t['atomic_propositions'][f'ValueBit{b}']=f'Boolean ((I[k].value >> {b}) & 1) = 1, unsigned DWORD width 32.'
                    t['atomic_propositions'][f'PrevBit{b}']=f'Boolean ((inputMemory.prev[k] >> {b}) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.'
            if tid=='PUB009' and p['id']=='P6':
                p['formula']='G(trigger <-> X(previousTrigger))'
                p['explanation']='Both operands are Boolean propositions. previousTrigger[0]=FALSE; previousTrigger[k+1]=I[k].trigger on every invocation, including invalid/reset.'
            if tid=='PUB007' and 'forall i in 1..5:' in old:
                import re
                body=re.search(r'forall i in 1\.\.5: (.*)\)',old)[1]
                # Remove the quantifier-closing parentheses, retaining outer G/implication.
                body=body[:-1] if body.endswith(')') and p['id'] in ('P1','P2','P3','P4') else body
                bodies={'P1':lambda j:f'!runs[{j}]', 'P2':lambda j:f'runs[{j}]=select[{j}]',
                        'P3':lambda j:f'(runs[{j}] <-> TopThree{j})','P4':lambda j:f'runs[{j}]=runPrev[{j}]'}
                guards={'P1':'stop','P2':'!stop & start & !mode','P3':'!stop & start & mode','P4':'!stop & !start'}
                p['formula']='G(('+guards[p['id']]+') -> ('+' & '.join('('+bodies[p['id']](j)+')' for j in range(1,6))+'))'
                for j in range(1,6):
                    t['atomic_propositions'][f'TopThree{j}']=f'({j}-1) is in first three ordinal indices of sorted(range(5), key=lambda j: (-I[k].pumpGroup[j].priority,j)).'
            if tid=='PUB008' and 'forall j:' in old:
                name='AllChannels_'+p['id']
                body=old[len('G(forall j: '):-1]
                quantified[name]={'operator':'finite_conjunction','variable':'j','lower_inclusive':0,
                    'upper_exclusive':'len(I[k].channels)','empty_value':True,'body':body,
                    'instantiation':'For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.',
                    'index_mapping':'j is zero-based ordinal; PLC index is each array own lower bound + j.',
                    'guard':'enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.',
                    'numeric_comparison':'Converted outputValue uses the comparison policy; status/config/preserved fields are exact.'}
                p['formula']='G('+name+')'
                t['atomic_propositions'][name]=json.dumps(quantified[name],ensure_ascii=False)
            p['language']='LTL_OVER_TYPED_SCAN_PREDICATES'
            p['encoding_status']='NOT_LOWERED_TO_MODEL_CHECKER'
            p['scope']='INITIAL_INSTANCE' if p['formula']=='init' else 'SCAN_SEQUENCE'
            if p['formula']=='G(CompleteBehaviorV2)':
                p['explanation']='Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.'
        # Interface symbols always denote observations, not oracle expressions.
        for name,f in fields.items():
            direction=f['direction']
            t['atomic_propositions'][name]=(f'I[k].{name}: sampled input ({f["type"]}).' if direction=='INPUT' else
                f'O[k].{name}: independently observed post-scan candidate value ({f["type"]}); never defined as expected output.'+
                (f' I[k].{name} denotes separately captured caller value before invocation.' if direction=='IN_OUT' else ''))
        for alias,binding in histories.items():
            t['atomic_propositions'][alias]=json.dumps(binding,ensure_ascii=False)
        t['atomic_propositions'].update(precise_auxiliary_predicates(tid))
        if 'first' in t['atomic_propositions']:t['atomic_propositions']['first']='k=0; first invocation, not the pre-invocation observation'
        if tid=='PUB004':t['atomic_propositions']['accNext']='O[k].PUMP_RUNTIME_ACC, actual post-scan LTIME; never reference accumulator.'
        if tid=='PUB013':
            t['atomic_propositions'].update(mode='I[k].HVAC_MODE_SELECTOR',occupancy='I[k].OCCUPANCY_DETECTED',adjust='O[k].TEMP_SETPOINT_ADJUST')
        if tid=='PUB012':
            t['atomic_propositions'].update(count='O[k].Slab_Fault_Counter',history='O[k].Slab_Fault_History',runtime='O[k].Slab_Runtime_Accumulator')
        t['atomic_propositions']['CompleteBehaviorV2']=relation
        normalized={'schema_version':1,'status':'NORMALIZED_PENDING_HUMAN_REVIEW',
            'language':'LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.',
            'candidate_formal_verification':'UNVERIFIED','initial_observed':initial,
            'reference_state_initial':plain_state(reference),
            'transition':{'entrypoint':'plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])',
                'reference_binding':f'Persistent plc_agent.scan_contract.ScanContract({tid!r}); constructed once per independent case, current state is Sref[k].',
                'state_update':'Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.',
                'module_sha256':hashes,'hash_encoding':'UTF-8 without BOM; all line endings normalized to LF before SHA256',
                'frozen_sources':str(FROZEN.relative_to(ROOT)).replace('\\','/')},
            'constrained_observed_fields':sorted(covered),'unconstrained_representation_fields':sorted(missing),
            'comparison':{'integer_boolean':'exact type and value; no tolerance',
                'float':'finite; abs error<=1e-5; dictionary/list shape and non-float values exact',
                'PUB008':'only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact',
                'PUB017':'Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.',
                'TIME_LTIME':'exact integer nanoseconds after IEC literal parsing',
                'implementation':'plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference'},
            'observation':{'I[k]':'deep-copied inputs immediately before invocation k',
                'O[k]':'actual outputs immediately after invocation k, supplied by independent execution backend',
                'Sref[k]':'independent reference state BEFORE k; unrelated to similarly named candidate variables',
                'initial':'fresh instance BEFORE invocation 0; never substituted by O[0]',
                'X':'next scan-sequence position; argument must be Boolean, not a numeric term',
                'time':'dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans'},
            'history_bindings':histories,'auxiliary_state_bindings':auxiliary_bindings(tid),'finite_conjunctions':quantified,
            'reference_state_rule':'Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.',
            'primitives':{'bitwise':'DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.',
                'time_literals':'IEC TIME/LTIME literals are exact integer durations in nanoseconds.',
                'observed_arrays':'All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.',
                'boolean_next':'X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.',
                'time_progress':'Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise.'},
            'assumptions':deepcopy(t['assumptions']),
            'domain_policy':'Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.',
            'limitations':['No ST-to-model translation or infinite-trace proof is implemented here.',
                'Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.',
                'Finite matching cannot establish liveness or validate runtime provenance.'],
            'rules_zh':rule}
        t['normalized_specification']=normalized
        c=t['specification_contract']
        c['normative_completion']=relation
        c['history_binding']='I, O and Sref namespaces, initialization and updates are defined in normalized_specification.observation, history_bindings and reference_state_initial. Candidate output never drives Sref.'
        c['evaluation_scope']='Versioned executable scan predicate plus LTL over interpreted predicates. No native checker encoding or completed formal proof is claimed.'
        c.pop('deterministic_transition_python',None)
        c['transition_binding']='Use normalized_specification.transition and exact pinned source snapshots.'
        for protected in ('requirements','interface','tests','initial_conditions','assumptions'):
            if t[protected]!=original[protected]:raise AssertionError('Protected field changed: '+tid+'/'+protected)
        folder='public' if t['kind']=='public' else 'self_built'
        write_json(ROOT/'dataset'/folder/(tid+'.json'),t)
        changes.append({'id':tid,'before_sha256':digest(original),'after_sha256':digest(t),
            'properties':len(t['ltl']),'constrained_fields':sorted(covered),'human_review':'PENDING',
            'changed_formulas':[{'id':p['id'],'before':old['formula'],'after':p['formula']} for p,old in zip(t['ltl'],original['ltl']) if p['formula']!=old['formula']]})
    tasks=load_tasks(); result=validate(tasks)
    if result['errors']:raise ValueError(result['errors'])
    # Inspect test expectations as observations ONLY to check definition consistency.
    # This does not assert that any candidate ran or passed these tests.
    fixture_failures=[]
    for t in tasks:
        for case in t['tests']:
            monitor=NormalizedScanMonitor(t)
            for k,step in enumerate(case['steps']):
                r=monitor.step(step['inputs'],step['expected'],step.get('dt_ms'))
                # Fixed expectations are often partial: compare only supplied fields.
                for field, expected in r['expected'].items():
                    if field in step['expected'] and not r['field_results'][field]:
                        fixture_failures.append({'task':t['id'],'case':case['id'],'scan':k,'field':field})
    report={'version':VERSION,'task_count':len(tasks),'property_count':result['ltl_properties'],
        'complete_predicate_definitions':32,'human_approved':0,'candidate_formally_verified':0,
        'native_model_checker_encoded':0,'fixture_alignment_failures':fixture_failures,
        'fixture_scope':'EXPECTATION_CONSISTENCY_ONLY_NO_ST_EXECUTION',
        'dataset_sha256':result['dataset_sha256'],'changes':changes}
    write_json(ROOT/'results/summary/specification_normalization_20261111.json',report)
    if fixture_failures:raise ValueError('Fixed expectations disagree with normalized predicates; inspect report.')
    print(json.dumps({k:v for k,v in report.items() if k!='changes'},ensure_ascii=False))


if __name__=='__main__':main()
