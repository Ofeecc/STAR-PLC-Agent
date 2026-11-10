"""Render a separate, versioned static review; never modify benchmark tasks."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NOTES = []

def note(tid, verdict, meaning, good, problems, proposal, cases, decision="无需额外题意决定；按下述建议完善。"):
    NOTES.append(dict(id=tid, verdict=verdict, meaning=meaning, good=good,
                      problems=problems, proposal=proposal, cases=cases, decision=decision))

note("PUB001", "必须补全", "按空闲→清洗→灌装→旋盖→包装→完成的顺序工作，当前工序收到对应确认后才进入下一步。",
     "P2互斥、P3—P9的主要转移与完成灯保持符合当前评测约定；T1、T2覆盖整周期和乱序确认。",
     "P3—P7只规定收到确认时动作，没有规定未确认时本工序的执行器必须持续，也没有完整规定空闲输出全关。P9只要求完成灯关闭，允许其他执行器在复位当拍误开。P1的init说的是调用前状态，不能直接当成首行调用后输出性质。phase只列了名称，缺完整更新。P10是条件活性，不能弥补逐拍输出遗漏。",
     "独立定义nextPhase：0有瓶→1，否则0；1清洗确认→2，否则1；2灌装确认→3，否则2；3旋盖确认→4，否则3；4包装确认→5，否则4；5取瓶确认→0，否则5。每拍只用旧phase选择一个分支。补G(X(phase)=nextPhase)，并逐一规定Pump_Motor↔nextPhase=1、Filling_Valve↔2、Capping_Machine↔3、Packing_Machine↔4、Completion_Light↔5；其余全部为假。初始phase=0作为独立初值条件。",
     "现有T1包含清洗保持，T2包含忽略错位确认，但灌装、旋盖、包装都缺独立多拍等待。增加每阶段等待、全部确认一直为真时每拍只进一阶、取瓶当拍五输出全关、瓶持续存在后下一空闲拍重启。",
     "电平确认、一拍一转移、瓶未离开允许下一周期重启，都是本项目补充约定；应随题目提供给两个Agent。")

note("PUB002", "基本合理，需精确定义", "对32位输入逐位比较前一拍，输出上升/下降位掩码、数量和变化标志。",
     "P1—P6覆盖掩码、计数、标志及历史更新；测试包含首次非零、最高位、全32位及混合变化。未发现这些期望值与题意直接冲突。",
     "prev=0是补充初值；X(prev)=value是带数据的时序关系，需要编码。atomic_propositions把risingBits写成正确掩码表达式，容易与同名被测输出混淆：如果监控器直接算正确掩码并覆盖观察值，P1会成为恒真。",
     "明确risingBits/fallingBits始终指实际输出；另定义riseExpected=value & (~prev & 16#FFFFFFFF)、fallExpected=prev & (~value & 16#FFFFFFFF)。比较实际值与期望值；初始prev=0，每拍结束只更新一次prev。计数域0..32，按无符号DWORD处理。",
     "保留现有用例；可补交替位16#AAAAAAAA↔16#55555555和全部位不变时两个计数均归零，防止只处理低位或计数不清。",
     "确认第一次采样与零比较的约定；原题未明确首次采样是否只建立基线。")

note("PUB003", "基本合理，需限定输入域", "高低报警分别按严格阈值触发和释放，滞回区保留历史，配置错误输出对应错误码。",
     "P1—P9对有效配置的触发、释放、等号保持和错误优先级覆盖较完整；T1/T2的边界和恢复期望一致。",
     "负hystWindow被排除，但原输入类型REAL仍可传入；NaN、无穷和算术溢出没有契约。窗口错误时也提前返回并保留报警是补充解释。更正：在有限数值、合法窗口0<=hystWindow<hiLevel-loLevel、两报警初始FALSE且错误配置保留历史的条件下，两报警互斥。高报警触发同时满足低报警释放条件，低报警触发同时满足高报警释放条件；保持区重叠本身不能令两报警同时置位。",
     "把有限REAL、hystWindow>=0写为显式环境前提。hiPrev/loPrev绑定上一拍实际输出和初值FALSE，配置无效不更新这两个输出。保留严格>,<及错误码优先级；浮点比较和容差按被检关系分别约定，勿把阈值比较自动放宽。",
     "现有用例已查四个关键等号。建议增加hystWindow=0、配置改变后落入保持区、先高后低且滞回区重叠的序列，确保不会错误强制报警互斥。",
     "决定负窗口属于非法输入域还是需要新增错误行为；不能自行发明官方错误码。")

note("PUB004", "需明确计时与参数策略", "粘度条件持续合格后才开泵，急停优先，累计运行时间达到500小时给维护提示。",
     "运行使能等价式、LTIME累计、停泵保持和维护不干预泵均已表达；T1/T2含资格建立、丢失和急停，T3给出500小时算术边界。",
     "qualified依靠文字定义，尚无可执行时钟。DebounceTime运行中变化策略没有写明。CycleTime按当前输出累计会把启动当拍整个间隔计入，这与按前一时间区间实际运行时长累计不同，必须公开。P3的X(!qualified)不能替代完整计时更新。长期LTIME溢出未限定。",
     "明确输入在调用间保持，第一合格采样elapsed=0；丢失permit当拍清计时。选择并注明DebounceTime固定或动态更新规则。把累计写成accAfter=accBefore+(VFD_RUN?TIME_TO_LTIME(CycleTime):0)，并标成离散调用累计口径；约束累计不溢出。维护输出等价于accAfter>=500h。",
     "保留原用例；补急停与合格到时同拍、原始条件抖动、维护提示出现后仍继续开泵。动态参数策略选定后补相应场景。T3的500小时不能作为普通短时实机测试计入；加速需有经过验证的时钟机制。",
     "急停清已完成资格、当前输出决定CycleTime累计、动态参数策略，属于需要固定的评测解释。")

note("PUB005", "主要逻辑合理，需落地计时", "上电先屏蔽5秒，随后对超焊缝信号去抖；急停立即关闭报警。",
     "P1—P5覆盖上电指示、屏蔽、不累计去抖、正常报警和信号丢失；现有时序期望与声明的解释一致。",
     "startup和gapQualified仅有文字，没有时钟更新定义；动态DebounceTime未定义。急停期间上电计时继续、软启动指示仍为真是补充解释。无穷活性P5需要时间持续前进，有限测试不能证明。",
     "独立保留startupStart与gapStart。上电到时拍才允许首次gap采样，elapsed从0开始；startup或急停或Gap_Exceeded=FALSE立即清gap历史。明确DebounceTime为固定正值，或给出参数改变策略。startup仅代表上电屏蔽，不能被解释为速度斜坡。",
     "补4.999/5.000秒边界、Gap_Exceeded在屏蔽结束前后变化、去抖中途急停、刚到资格阈值同拍急停。时间戳应来自真实运行或经验证的受控时钟。",
     "保持现有上电计时跨急停的解释前，应把它作为统一假设提供；不能声称原题明确规定此实现细节。")

note("PUB006", "基本合理，需落地计时", "低溶氧需求与急停许可连续满足5秒才运行，每次运行由假变真计一次启动。",
     "P1—P4基本完整覆盖使能、停机、计数和计数保持；测试含4.999/5秒、二次启动及急停重建计时。",
     "delayDone的监控状态没有实现；runPrev/countPrev须绑定观察历史。计数UINT回绕不在当前域内，应明确域限制而不是只说测试没碰到。条件活性缺少形式化的时间进展假设。",
     "将permit连续计时、首次TRUE年龄0、FALSE清零定义成确定时钟状态；运行与permit且elapsed>=5s等价。初始runPrev=FALSE、countPrev=0，每拍更新。加入累计启动次数<65536的评测域或另外约定溢出策略。",
     "现有边界较好；补首次调用需求TRUE且急停FALSE、需求与急停恢复同拍、已运行后需求FALSE再TRUE必须重新等5秒。")

note("PUB007", "主要争议在评测假设", "手动选泵；自动按优先级选五台中前三台，停止优先。",
     "在当前start电平重选、其余时间保持的解释下，P1—P5覆盖所有RunComd及配置不变，现有优先级计算一致。",
     "原题没有清楚规定自动是否持续重选，当前只start时选，可能与另一种合理实现不同。start被按电平处理而非边沿；并列按小序号也是补充约定。模式变化无start时保留原泵组，可能使自动模式暂时不是三台运行；不能又无条件要求自动永远恰好三台。",
     "明确运行态、启动/停止及重选事件的契约，给出每拍对全部五个RunComd的方程。以排序键(-priority,index)独立算top3，所有priority/selection保持采样值，不允许排序时交换整个结构破坏外部顺序。",
     "已有手动/自动/并列/负优先级；补运行中改priority、改selection、切mode且无start、start持续TRUE时改变配置，区分持续重选和锁存。",
     "在运行中自动持续重选与只在start重选之间选择统一口径；当前结果只能声称符合后者。")

note("PUB008", "基本合理，需补类型及容差", "批量按各自数组下界的相对位置转换模拟量，处理启用、模式错误、上下限错误和保留字段。",
     "P1—P8覆盖只读字段、跳过保留、错误优先级、三种计算；现有用例含端点、温度、count=0、不同数组下界和外推。",
     "forall j没有把定义域写进公式；analogValues和channels长度不同，不能读不存在元素。scaled的raw+27648若按INT中间值计算会溢出；这是实现风险，需在参考算术说明。REAL数学等号与实际绝对1e-5比较不一致，较大数值可能出现误判。",
     "明确j∈[0,len(channels)-1]，转换读取仅在j<count且j<len(analogValues)时，count≤min两长度为环境前提；域外不访问。独立以足够宽的类型算期望；定义转换误差关系，例如与IEC REAL舍入相容的逐输出绝对/相对容差，先固定再评测。",
     "保留不同下界元数据；补两数组不同长度但count合法、INT极值、较大/较小工程量跨度、错误恢复、温度模式下无效上下限。绝对1e-5是否适用需由数值精度评审确定。",
     "不同下界、禁用保留、所有模式验证上下限、非法模式优先及外推均需作为统一补充约定。")

note("PUB009", "基本合理，需精确定义历史", "按每拍或触发上升沿接受一个数据，维护滑动平均，支持复位和窗口错误。",
     "P1—P7与当前暖机用实际样本、复位优先及窗口变化清空的解释一致；现有均值期望未发现算术冲突。",
     "historyAfter只是文字函数；lastValidWindow没有初值和更新方程。无效窗期间是否保持上一有效窗口历史、回到同一有效窗口是否继续，需完整绑定。当前只用小数值绝对1e-5不能覆盖LREAL的大尺度舍入误差。",
     "以独立输入历史维护history和lastValidWindow：非法窗不改；首次有效建立窗口；有效窗口变化或reset清空；!reset且cyclicExecution或triggerRise时追加一个样本并截断到窗口长。每拍更新previousTrigger，包括非法和复位拍。average=空则0否则均值，Reached=长度等于窗口。",
     "增加窗口100填满并滑动、非法窗期间trigger上升后恢复且仍高、reset时trigger高后释放复位、窗口变化且无采样、cyclic与trigger同时触发仍只采一个、大正负值抵消。",
     "暖机分母、变窗清空、非法窗保留、边沿在复位和错误期间仍更新，都是要公开的评测解释。")

note("PUB010", "必须补全并统一边界", "低于设定温度加热，高于则关闭；传感器故障或过热保护必须关闭，连续加热到阈值后冷却。",
     "故障关断、保护关断、显示和值一致、冷却未完成时保持保护已表达；现有测试包含故障及精确时间边界。",
     "P5只写需要热时开，没有!demand时必须关；高于设定值的一个短暂错误加热可以满足全部八条。保护也缺禁止无原因触发的约束。假设写冷却>=3秒可解除，T1却要求恰3秒必解除，二者强弱不一致。原文more than 5s与当前>=5s不一致。heatLimitReached依赖连续energized时间，若当拍已关输出，必须仍用进入该拍前的加热历史判定，否则会循环定义。",
     "选定>5s或>=5s边界并解释。先由旧运行区间算heatAgeBeforeDecision/是否到时，再更新保护与冷却，最后规定HeaterOutput↔sensorValid & demandAfter & !protectionAfter；demandAfter为低温置真、高温置假、等温保持。明确冷却第一个>=3秒观测拍是否必须解除，并规定无旧保护且未到限不得自行保护。",
     "T1最后高温拍能发现关断遗漏，但公式不能。增加无加热需求时不得自行热、无超时不得自行保护、冷却到时但温度过高/故障、加热被高温中断后计时重置，以及5秒两侧样本。",
     "优先按原文严格>5秒修订，或将>=5秒明确标为课程评测解释；3秒是强制解除还是最短等待也需统一。")

note("PUB011", "必须补全", "自动依次完成A→B→C，手动点动互锁，C确认后灯亮直到取走。",
     "P1—P4的互锁、手动命令和到站停机正确；T2实际包含正向起步和行进保持。",
     "六条公式没有自动起步、运动保持、B确认发车和多数阶段更新。自动模式永远不走，在一直SensorA和ButtonA为真的输入下也不会违反公式。灯只要求finish当拍亮，没有完整保持/禁止提前亮。手动模式未约束CompletionLight。",
     "明确WAIT_A→MOVE_AB→WAIT_B→MOVE_BC→WAIT_C→DONE→WAIT_A的输入条件、无触发保持及模式复位。输出按转移后的阶段：仅MOVE_AB/MOVE_BC正转，自动反转恒假；仅DONE且产品未取走灯亮。手动灯灭，正反向按按钮互斥方程。",
     "保留T1—T3；补两个运输段的多拍无传感器保持、B/C确认同到站拍如何处理、按钮提前一直按住、自动中切手动再切回、产品未取走时灯多拍保持。",
     "固定到站与完成同拍是否接受，以及切模式清流程的解释；当前T2按到站后另一拍确认。")

note("PUB012", "基本合理，需落地计时和历史", "有效故障触发至少500ms报警并记录最近五次，正常切割才累计时间，信号无效优先关报警。",
     "P1—P6覆盖故障与保持期、次数、队列更新、未触发保持和正常运行累计。六次记录的测试顺序正确。",
     "hold年龄与previous(valid AND fault)需独立更新；重触发重新计500ms是补充解释。首次正常调用dt=0但加CycleTime=100ms是离散累计口径，不能称该测试已观测到100ms真实运行。UINT和LTIME需约束溢出域。",
     "用上次有效故障边沿的独立时间戳定义hold，invalid立即清hold，每拍更新validFault历史；FaultTimestamp只是记录数据，不拿它当500ms时钟。计数/数组逐项等于旧值更新，runtime按当前qualifying条件加转换后的CycleTime。",
     "增加500ms内二次故障重新延长、invalid后fault仍真算新事件、CUTTING_RUN与信号同时变化、故障计数与历史在无事件时全保持。")

note("PUB013", "基本合理，需落地计时", "有人且非夜间连续30秒后开风机；各模式按占用状态给定温度偏移。",
     "模式0..3内P2—P5覆盖所有温度偏移分支，occupied排除了Night，所以P3不存在有人夜间必须同时0和4的矛盾。T1/T2期望与此一致。",
     "mature需独立计时和清零状态。原子命题使用mode/occupancy/adjust等别名但没有逐项写出与接口名的映射。非法模式被环境排除，不能对它声称正确。",
     "补mode=HVAC_MODE_SELECTOR、occupancy=OCCUPANCY_DETECTED、adjust=TEMP_SETPOINT_ADJUST。permit失去时当拍风机关、清计时；再次建立从0算；初始值与第一调用计算分开。活性前提加入实际时间进展。",
     "保留夜间/失去占用及30秒边界；增加有人时Auto→Comfort→Economy不失permit的切换、Night→非Night重等30秒、已运行后切Night。")

note("PUB014", "基本合理，需独立解析定义", "严格解析四个0..255十进制段，网络字节序拼成UDINT，非法输入输出0。",
     "有效与无效两个分支已穷尽，P3是冗余确定性约束；测试涵盖字节序、范围、格式、前导零和长数字。",
     "valid/packed须由ipText独立解析，不能以输出非零来推导有效性；0.0.0.0本来有效。超长十进制段可能使有限整数中间值回绕；应定义按数学数值判断范围，或在每一步超255立即判非法。",
     "给每字符ASCII数字及恰三个点的精确定义；允许任意数量前导零，只要总STRING容量满足。用逐段安全累加a=10*a+d且超255拒绝，合法后以足够宽无符号算术拼接；实际ipValue只作被检输出。",
     "补+1.2.3.4、换行/制表符、四段全带前导零、很长零前缀但值合法、连续重复输入；输入域明确NUL按PLC字符串终止语义。")

note("PUB015", "必须补全并消除优先级歧义", "手动五个执行器各自按按钮上升沿翻转；自动按50/80/100cm分支混料后排料，急停全关。",
     "急停极性与原题一致；主要液位阈值、是否加C和混合完成后的排料已列入。测试比公式覆盖更完整。",
     "P2只约束阀A，阀B/C/D与搅拌电机可以永不响应。未定义autoStart必须打开A、阶段保持、排料保持及ghost阶段更新。toggle没有排除模式变化，但假设又说模式变化清旧锁存：若切入手动且A上升，复位与翻转谁先未定义。自动动作谓词也未排除模式重置。",
     "按优先级急停→模式变化→正常分支明确复位当拍是否抑制按钮；随后为五个手动输出逐一写XOR上升沿方程，所有按钮历史每拍更新。自动给完整IDLE/FILL_A/FILL_B/FILL_C/MIX/DRAIN转移表，输出由转移后阶段唯一决定。独立定义processMode批次固定或采样锁存。",
     "已有五输出手动开启，但B/C/D/电机二次翻转、保持和急停恢复仍需补；增加模式切换与按钮同拍、各自动阶段长等待、processMode两条完整至排料、排料保持。",
     "模式重置当拍是否接受新按钮/autoStart，排料何时关，需按现有补充解释统一；不能凭全局互斥禁止合法的独立手动动作并行。")

note("PUB016", "必须补全转移", "按给定工位序列移动、到站等待对应加工完成，再依序行进到5号输出站。",
     "方向互锁、移动中方向、到站停机和条件活性有基础；测试有[4,2,5]与直接[5]。",
     "缺启动受理当拍发车、加工完成后的序号推进、目标与序列元素对应、相同工位重复加工等精确规则。higher/lower只在旧MOVING成立，不能约束启动当拍。P6活性只要求最终完成，不能保证中间严格走对工位。",
     "独立维护currentStation、index、target和phase。接受start后index=1，目标为sequence[1]；异站按方向移动，同站进入等待且电机全关。到达加工站进入WAIT_PROCESS；对应完成新边沿才index+1并重新取目标；5站到达回IDLE。无事件保持，一拍最多推进一个index。输出按转移后阶段计算。",
     "增加[2,2,5]以新边沿完成两次加工、长度8、错误完成边沿、完成信号一直高、非目标站传感器TRUE不停车、两个移动方向的无传感器多拍保持。",
     "启动/完成采用上升沿与重复工位需新边沿是补充解释；应作为题目契约明确给出。")

note("PUB017", "必须补全数据操作和状态", "按ID增删改查最多10条配方，禁止重复，新增用最小空位，失败有指定错误码。",
     "五种错误码、失败不改库、插入位置和ID唯一性已经表达；原测试含CRUD和满库/重复错误。",
     "没有成功删除、修改对数据库的要求，没有这两类成功脉冲。查询成功未要求error=FALSE/status=0，也未约束查询/空闲不改数据库。P2只在error为真时保库，恶意或错误实现可在error为假时破坏库。成功指示反向条件及其他指示清零不全。T1不直接检查数据库，删除后未再查被删ID，也没有同时保留多个记录后核对未修改记录。",
     "逐操作定义dbAfter与dbBefore：新增替换最低空位；删除只将匹配记录ID置0，其余记录保持，删除槽非ID字段保持或不约束须声明；修改仅匹配槽整体替换；查询/空闲/失败数据库全保持。successAdded/Deleted/Modified分别与对应成功事件等价，每拍脉冲；所有成功/空闲error=FALSE,status=0。查询结果仅成功查询更新，其余保持。",
     "增加删除后查同ID报8001、修改一条不改变其他两条、删除非首槽后复用最小空槽、操作当拍检查全部十槽、成功拍其他指示为假、请求持续高不重复执行、错误后查询结果保持。",
     "上升沿、同拍最多一个请求、正ID域及查询结果保持是补充解释；初始数据库唯一是环境前提或空库初值。")

note("PUB018", "需补可观察数据绑定", "泛型环形FIFO按上升沿入队出队，复位清空，空满拒绝并返回错误码。",
     "P1—P5覆盖主要队列操作、拒绝和边界；两种元素类型与不同下界是正确的泛型验收方向。",
     "empty仅写elementCount=0，没有明确logical queue也清空；same只保持logical queue和item，没有直接规定elementCount保持。pushed未要求入队时item不被改写。logical queue的count与物理buffer内容映射缺失，若只在监控器里维护理想队列而不比实际输出，可能自证正确。VARIANT本机支持仍未验证。",
     "定义Q为独立输入历史参考序列，并把elementCount=|QAfter|写成每拍不变量；pop实际item等于QBefore首项，push/idle/reject/reset实际item等于采样值。reset后QAfter=[]。buffer可允许不同环形布局，但要明确由受检head/tail映射验证存储，或以完整出队序列核对可观察FIFO行为，不凭理想Q自己通过。保持接口，不私改为DINT特例。",
     "已有绕回、空满、复位与请求同拍；补容量1、多次复位后旧数据不得再次读出、reset时dequeue保持到下一拍、入队不得更改item、清空后填满再完整出队；A/B两种绑定都需要真实证据。",
     "第一调用为空是调用前状态，不应禁止第一拍合法enqueue后count=1；现有T2/T3本身即如此解释。")

note("PUB019", "必须补全模式与动作", "机械臂六动作，手动按住动作、单步逐次确认、单周期执行八步、连续循环，急停立即取消。",
     "急停极性、成对互锁和限位关断合理；现有测试包含四种模式、完整八步和急停恢复。",
     "手动等价使能只覆盖down，另五个动作未覆盖。ordered一句自然语言没有可判定转移；必须继续运动、非首步的单步Start、无完成时保持、busy与输出的关系没有充分约束。start原子只定义首步，不能覆盖单步第2..8步。模式切换复位与当前已写公式的同拍优先级仍需明确。",
     "手动对六动作均写命令=安全 & manual & 本按钮 & !反向按钮 & !本限位。自动独立建8个动作状态与单步等待态，记录nextStep/busy；按匹配反馈才前进，一拍至多一阶。单步完成全关，下一新Start边沿启动保存的nextStep；单周期末IDLE，连续末转DOWN；每个动作输出由转移后状态并按限位门控。急停/无模式/模式变化按声明优先复位。",
     "手动T1没有单独激活每个方向；补上、左、右、夹、松各自按下/松开/限位/反向冲突。单步目前只走开头，补完整八步；补动作中Start被忽略、完成反馈提前为真、模式变化与Start同拍、多拍无反馈保持。",
     "已达下一个限位时只抑制输出、下一拍处理完成，以及复位后要求顶左姿态，是补充评测解释，须公开。")

note("PUB020", "必须补全流程与谓词", "上料→清洗→称重→合格烧制→输出，不合格剔除，合格100..200映射500..550。",
     "手动互锁、合格边界和温度线性计算、拒绝及输出灯已有公式；现有100/150/200与99.9/200.1的测试计算正确。",
     "没有明确上料发车、清洗完成/烧制完成发车、运动保持、拒绝保持和多数状态转移。order仍是文字。原子moving被定义为post-phase MOVE_TO_WASH，而arrival又写pre-phase moving，前后状态混用，且不能覆盖其余运输段。P7未充分规定完成灯在未取走时持续。",
     "列出WAIT_FEED/MOVE_WASH/WAIT_WASH/MOVE_WEIGHT/WAIT_WEIGHT/REJECT/MOVE_FIRING/WAIT_FIRING/MOVE_OUTPUT/OUTPUT_DONE全转移表，明确旧阶段判定事件、转移后阶段决定输出。arrival分四运输段按目标传感器定义。称重成功只更新一次firingTemp，其余保持；REJECT在SensorWeight仍TRUE时kick保持，移除后回WAIT_FEED。",
     "已有主要路线和拒绝；补所有运输段无到站多拍保持、清洗/称重/烧制多拍等待、无关完成信号、手自动切换中断、上一合格批次后拒绝仍保持上次firingTemp、完成灯长保持。",
     "到站拍不接受完成、拒绝保持到移除、模式变化重置、温度保持是补充约定；别把moving含糊别名带入检查器。")

note("SELF001", "基本合理，可作首个完善样例", "带门许可的自保持电机，停止或开门优先；关门时Start仍高允许启动。",
     "P2—P4覆盖全部输入分支，P1给出初始化，P5是可由这些分支推出的保持性质；两组测试期望一致。",
     "qRun应明确绑定上一拍实际Run，或绑定独立参考状态但全流程一致。仅P1初始化加P2—P5并没有单独写历史递推；不能让qRun成为任意布尔值。",
     "补qRun[0]=FALSE，qRun[k+1]=Run[k]的监控绑定；可用总方程Run↔GuardClosed & !Stop & (Start | qRun)作为完整一步规约。P5可保留作冗余一致性检查。",
     "增加首次调用直接Start=TRUE的显式用例，检查不会因初始Run=FALSE而错误要求首拍仍关。无需添加边沿或人工复位条件。")

note("SELF002", "基本合理，需绑定历史", "点动正反转，直接换向先给一拍全关，然后可运行新方向。",
     "P1—P6穷尽停止、冲突、空命令和合法单向请求；中立一拍的测试符合题意。",
     "qForward/qReverse必须是真正前一拍输出，不能绑定上次非零方向，否则中立后会一直禁止反转。初始中立仍依赖文字初值。",
     "明确qForward[0]=qReverse[0]=FALSE；每拍无条件更新为本拍两个实际输出，包括Stop/双按钮/无按钮产生的中立拍。完整公式可保留。",
     "保留直接换向；补每拍交替按钮、Stop后请求反向、双按钮中立后单向，验证使用的是紧邻上一拍而非最后运行方向。")

note("SELF003", "必须补全保持", "上电和急停后必须先满足安全复位，再允许Start；解除后保持运行直到停止或急停。",
     "P1—P4正确约束初始闭锁和有效复位，P5/P6的启动停止优先级一致。",
     "缺!qRequired且安全时ResetRequired保持FALSE，也缺无Start/Stop时Run保持。因而已启动后下一拍自动停机，或者无理由重新闭锁，可能满足现有六条。现有reset_restart第3个零基索引拍检查了Run保持，说明测试要求强于公式。",
     "增加G((!qRequired & EStopNC) -> !ResetRequired)和G((!qRequired & EStopNC & !Stop & !Start) -> (Run↔qRun))；qRun/qRequired每拍绑定前一输出。完整优先级为急停→若闭锁则只尝试有效复位且Run关→Stop→Start→保持；解除闭锁当拍不能启动。",
     "保留旧测试；补解除后长时间空闲不重新闭锁、运行中Reset不停止、Stop后不必再次Reset、Start与Stop同拍停止、急停与Reset同拍闭锁。")

note("SELF004", "必须补全状态与输出", "托盘IDLE/MOVING/COMPLETE/FAULT，Jam优先，Fault锁存，完成保持，Reset或非故障Stop复位。",
     "Jam优先、有效Reset、主要启动和到出口转移以及弱直到的故障保持方向正确；P7没有错误要求操作者最终复位。",
     "缺Stop必须回IDLE、MOVING无到位必须持续、COMPLETE保持和完整输出状态等价。P6只排除Belt与Complete/Fault同时真，没有排除Complete和Fault同时真；P2仅要求Fault真也未禁止其他不恰当指示。",
     "总转移优先级：Jam→FAULT；否则Reset→IDLE；否则旧FAULT保持；否则Stop→IDLE；旧IDLE且Start且!AtExit→MOVING；旧MOVING且AtExit→COMPLETE；否则保持。定义Belt↔postState=MOVING、Complete↔COMPLETE、Fault↔FAULT以及初始IDLE，即覆盖三输出互斥和所有保持。",
     "补从MOVING/COMPLETE分别Stop、FAULT中Stop不能清故障、完成态长保持、三个输出每拍全检查、MOVING多拍无AtExit。")

note("SELF005", "必须补全时长和输出对应", "外部Tick每拍为真计一逻辑拍，红2/绿3/黄1，禁用清进度，没有Tick保持。",
     "逻辑Tick与物理时间分开，P7为带持续使能和无穷Tick前提的活性，方向合理。",
     "P1只保一盏灯亮，没有灯与Phase对应。P3只保持Phase，不保持elapsed；P4/P5只约束最后一拍转灯，前几拍允许提前切换，无法保证2/3/1。禁用时没有明确Phase=0及计数清零。多数现有步骤只检查Phase，错误灯可漏过。",
     "设D(0)=2,D(1)=3,D(2)=1。!Enable→(phaseAfter,ageAfter)=(0,0)；Enable且!Tick→保持；Enable且Tick且ageBefore+1<D→同phase,age+1；否则→((phase+1) mod3,0)。Phase=phaseAfter，Red↔Phase=0、Green↔1、Amber↔2。初始(0,0)，每拍更新ghost，禁止仅从实际Phase反推期望灯。",
     "把每拍三灯和Phase全部列入expected；补绿色计数第1/2拍暂停、各阶段禁用恢复、Tick一直TRUE的完整多周期、Tick一直FALSE不进展。P7只能另作无穷性质，不能从这些有限样本宣布证明。")

note("SELF006", "基本合理，需绑定历史", "上下液位形成补水滞回，上湿下干判故障；抑制和高水位立即关阀。",
     "P1—P4覆盖所有上下液位组合与Inhibit分支，P5给初值；两组测试与题意一致。",
     "SensorFault是组合故障，不应擅自做成复位锁存。qFill须绑定历史，Inhibit解除在中间液位不自动重启已由保持表达，但监控状态不可丢失。",
     "明确qFill[0]=FALSE、qFill[k+1]=Fill[k]，SensorFault每拍由HighWet & !LowWet重新计算；无需另加错误保持。可保留原公式作为完整一步规约。",
     "现有10拍覆盖主要边界；补Inhibit时在低位、解除后低位立即开，以及故障恢复到中间液位保持关，区分组合故障与锁存错误。")

note("SELF007", "必须补全备用与episode状态", "需求时首选健康泵，故障立即切健康备用；一次有服务的需求结束才交替首选泵。",
     "P1—P3互锁和故障禁止、P6/P7交替时机方向合理；测试包含备用接替和未服务需求不交替。",
     "P4/P5仅要求首选健康泵必须开，没有要求首选故障时健康备用必须开。LeadA=TRUE且A故障B健康时，两泵均关能满足七条。completedServed缺明确episode历史更新；应避免错误实现从不运行导致永远被判未服务而自洽。",
     "补G((Demand & FaultA & !FaultB) -> PumpB)及对称条件。更完整：PumpA↔Demand & !FaultA & (qLeadA | FaultB)，PumpB↔Demand & !FaultB & (!qLeadA | FaultA)。completed=previousDemand & !Demand & servedBefore；LeadA=completed?!qLeadA:qLeadA。服务记忆在Demand内累计，结束清零；初始首选A、previousDemand=FALSE、served=FALSE。",
     "保留fallback；补首选B故障时A接替、同一需求中两泵都故障又恢复、已经服务后才全故障仍应在结束交替、连续多拍Demand=FALSE只翻转一次。")

note("SELF008", "基本合理，需固定算术语义", "连续合格请求按扫描累计到1..5预设值，Trip/无请求/非法Preset清零，Preset改变立即生效。",
     "P1—P4覆盖所有输入分支，计数饱和，动态降低Preset测试一致；有限上界能支撑P5的条件进展。",
     "qCount须绑定上一拍Count与初始0；nextCount用数学整数先加后min，不能把任意USINT溢出语义直接带入参考。若合法状态维持0..5，中间+1实际不会溢出。",
     "明确invalid↔Preset<1或>5，qCount[0]=0且逐拍更新；计数按清零分支或min(qCount+1,Preset)精确确定，Ready与合法且Count>=Preset等价。P5保留作派生性质。",
     "补Preset增加可使Ready暂时清零、Request/Trip与减小Preset同拍、Preset=255，保证非法值处理一致。")

note("SELF009", "需补完整历史更新", "按PartPulse上升沿计数并饱和，复位/非法Target清零，但仍更新边沿记忆。",
     "P1—P4决定错误、计数和完成标志；reset_edge覆盖了复位期间高电平采样。",
     "P5仅PartPulse→X qPulse，缺FALSE→下一拍历史FALSE；如果把qPulse当自由状态，永远TRUE会吞掉后续全部边沿。文字定义实际上要求双向，因此这是公式与绑定缺口，不是现有Python参考必错。需求中的Complete保持受Target增加影响，不能擅自改成无条件锁存。",
     "用G(X(qPulse)↔PartPulse)替换P5，并写qPulse初始FALSE；qCount初始0且更新。countAfter=min(qCount+rise,Target)包括Target降低时无新边沿也截断。Complete按当前Target重算，复位/非法优先。",
     "补Target从2增到3使Complete清零、Target降低且没有上升沿、非法Target期间PartPulse变低再恢复有效、相隔多个低电平后的新边沿；每拍检查Error。")

note("SELF010", "必须修订确认分支并补保持", "故障锁存报警，新故障边沿取消确认，持续故障可确认，故障消失后Reset才清除。",
     "P1—P5的声光关系、故障置位、新故障优先和有效Reset清除合理；现有reset_priority已明确持续故障时Reset不能阻止Ack。",
     "P6用了!Reset，但Reset只在!Fault时有效。Fault持续且Reset=TRUE、Ack=TRUE时，Ack仍应生效，却被P6漏掉。没有完整的Alarm/确认状态保持，也未禁止没有故障时凭空报警/确认。qFault无完整逐拍更新关系。",
     "定义validReset=Reset & !Fault。优先validReset清Alarm/Ack；否则rise置Alarm并清Ack；否则Fault或qAlarm保持Alarm，若Ack且本来有报警则置确认，否则确认保持；无报警时不得自行确认。完整方程：Alarm↔!validReset & (Fault | qAlarm)；Acknowledged=validReset或rise时FALSE，否则qAck | (Ack & qAlarm)。Horn↔Alarm & !Acknowledged；qFault下一拍等于Fault，所有历史有初值。",
     "保留reset_priority第1零基索引拍作为关键反例；补已确认持续Fault且Reset=TRUE/Ack=FALSE确认仍保持、报警未出现时Ack、故障消失后无Reset长保持、新故障与Ack/Reset同拍。")

note("SELF011", "必须补全保持和状态输出", "工装EXTEND→CLAMP→RELEASE→RETRACT→DONE，回零才可启动，无反馈保持，停止/复位回IDLE。",
     "主要逐拍转移和Stop/Reset优先已写，oneAction限制四命令互斥；全部反馈为真仍逐阶段走的测试正确。",
     "只有EXTEND写无反馈保持；另三个动作可无故停止。Busy与四动作、Done与DONE态没有等价关系，初始IDLE无合法Start时全关也未完整表达。P8只要求Done，不要求四命令全关且Busy假。",
     "给六态总转移：Stop或Reset→IDLE；IDLE满足Start且RetractDone→EXTEND；四动作各匹配反馈→下一态，否则保持；DONE保持。Extend/Clamp/Release/Retract分别↔postState对应动作；Busy↔四动作之一；Done↔postState=DONE；初始IDLE。",
     "新增CLAMP/RELEASE/RETRACT各自多拍无反馈，DONE中Start无效，IDLE未回零时所有六输出检查；原测试不少步骤只查部分输出，应扩展为完整映射。")

note("SELF012", "必须补全全部转移与计数", "故障后需连续两拍恢复才自动重试，最多两次；第三次运行故障闭锁，只有有效Reset恢复预算。",
     "已有故障禁止、预算范围、有效复位、LOCKED保持及部分重试规则；exhaustion/dwell_interrupt期望与完整题意一致。",
     "没有IDLE的Start必须运行、RUNNING健康保持、未用完预算故障后必须进入WAIT、第一健康WAIT拍不得提前运行、非重试拍Attempts保持，以及Stop行为。Run永假、Attempts=0、不闭锁的健康输入轨迹能满足七条，说明公式严重不完整。",
     "按validReset→旧LOCKED保持→Stop→正常状态分支排序。IDLE且Start且!Fault→RUNNING；RUNNING遇Fault则按qAttempts<2进入WAIT，否则LOCKED；WAIT遇Fault清dwell，健康第一拍dwell=1仍WAIT，第二拍RUNNING且Attempts+1；其余保持。Stop从非锁定态回IDLE并清dwell，但不改Attempts。Run↔postState=RUNNING，Locked↔postState=LOCKED；Attempts除有效Reset和自动重试外全部保持。",
     "增加Stop后手动Start不恢复预算、RUNNING持续健康保持、WAIT第一健康拍必须关、LOCKED中Start/Stop均无效、无效Reset不清预算、有效Reset与Stop同拍优先、Attempts=2后手动启动再故障仍应锁定。")

def main():
    tasks = sorted((ROOT / 'dataset/public').glob('PUB*.json')) + sorted((ROOT / 'dataset/self_built').glob('SELF*.json'))
    by_id = {n['id']: n for n in NOTES}
    if len(by_id) != 32 or len(NOTES) != 32:
        raise ValueError('Review must contain exactly 32 distinct tasks')
    inventory = []
    for path in tasks:
        raw = path.read_bytes()
        task = json.loads(raw)
        n = by_id[task['id']]
        relative = path.relative_to(ROOT).as_posix()
        blocks = [f"# {task['id']}：{task['title']}",
                  f"审查日期：2026-11-06。结论：**{n['verdict']}**。方法：题意、假设、全部公式及现有测试的静态语义审查。",
                  f"原题数据：[查看 JSON](../../{relative})。公式 {len(task['ltl'])} 条；测试 {len(task['tests'])} 组、{sum(len(c['steps']) for c in task['tests'])} 拍。",
                  '## 题目要求', n['meaning'], '## 已合理表达的部分', n['good'],
                  '## 问题及依据', n['problems'], '## 建议修订', n['proposal'],
                  '## 测试对应与补充场景', n['cases'], '## 需要固定的题意解释', n['decision'],
                  '## 原公式逐条索引']
        blocks += [f"- `{p['id']}`：`{p['formula']}`" for p in task['ltl']]
        blocks += ['以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。']
        (HERE / (task['id'] + '.md')).write_text('\n\n'.join(blocks) + '\n', encoding='utf-8')
        inventory.append(dict(task_id=task['id'], title=task['title'], source=relative,
                              source_file_sha256=hashlib.sha256(raw).hexdigest(),
                              formulas=len(task['ltl']), cases=len(task['tests']),
                              steps=sum(len(c['steps']) for c in task['tests']),
                              review=n, document=task['id'] + '.md'))
    (HERE / 'review_manifest.json').write_text(json.dumps(dict(
        review_date='2026-11-06', evidence='STATIC_SEMANTIC_REVIEW',
        dataset_modified=False, formal_model_checking=False, generated_st_execution=False,
        task_count=len(inventory), tasks=inventory), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(documents=len(inventory), formulas=sum(t['formulas'] for t in inventory),
                          cases=sum(t['cases'] for t in inventory), steps=sum(t['steps'] for t in inventory)), ensure_ascii=False))

if __name__ == '__main__':
    main()
