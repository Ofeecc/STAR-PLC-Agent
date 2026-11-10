# SELF011：Single cycle actuator handshakes with one transition per scan

审查日期：2026-11-06。结论：**必须补全保持和状态输出**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF011.json)。公式 9 条；测试 2 组、14 拍。

## 题目要求

工装EXTEND→CLAMP→RELEASE→RETRACT→DONE，回零才可启动，无反馈保持，停止/复位回IDLE。

## 已合理表达的部分

主要逐拍转移和Stop/Reset优先已写，oneAction限制四命令互斥；全部反馈为真仍逐阶段走的测试正确。

## 问题及依据

只有EXTEND写无反馈保持；另三个动作可无故停止。Busy与四动作、Done与DONE态没有等价关系，初始IDLE无合法Start时全关也未完整表达。P8只要求Done，不要求四命令全关且Busy假。

## 建议修订

给六态总转移：Stop或Reset→IDLE；IDLE满足Start且RetractDone→EXTEND；四动作各匹配反馈→下一态，否则保持；DONE保持。Extend/Clamp/Release/Retract分别↔postState对应动作；Busy↔四动作之一；Done↔postState=DONE；初始IDLE。

## 测试对应与补充场景

新增CLAMP/RELEASE/RETRACT各自多拍无反馈，DONE中Start无效，IDLE未回零时所有六输出检查；原测试不少步骤只查部分输出，应扩展为完整映射。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(oneAction)`

- `P2`：`G((Stop | Reset) -> (!Busy & !Done & !Extend & !Clamp & !Release & !Retract))`

- `P3`：`G((normal & qIdle & Start & RetractDone) -> Extend)`

- `P4`：`G((normal & qExtend & ExtendDone) -> Clamp)`

- `P5`：`G((normal & qClamp & ClampDone) -> Release)`

- `P6`：`G((normal & qRelease & ReleaseDone) -> Retract)`

- `P7`：`G((normal & qRetract & RetractDone) -> Done)`

- `P8`：`G((normal & qDone) -> Done)`

- `P9`：`G((normal & qExtend & !ExtendDone) -> Extend)`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
