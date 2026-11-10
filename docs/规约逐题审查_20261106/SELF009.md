# SELF009：Rising edge batch counter with reset sampling

审查日期：2026-11-06。结论：**需补完整历史更新**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF009.json)。公式 5 条；测试 2 组、13 拍。

## 题目要求

按PartPulse上升沿计数并饱和，复位/非法Target清零，但仍更新边沿记忆。

## 已合理表达的部分

P1—P4决定错误、计数和完成标志；reset_edge覆盖了复位期间高电平采样。

## 问题及依据

P5仅PartPulse→X qPulse，缺FALSE→下一拍历史FALSE；如果把qPulse当自由状态，永远TRUE会吞掉后续全部边沿。文字定义实际上要求双向，因此这是公式与绑定缺口，不是现有Python参考必错。需求中的Complete保持受Target增加影响，不能擅自改成无条件锁存。

## 建议修订

用G(X(qPulse)↔PartPulse)替换P5，并写qPulse初始FALSE；qCount初始0且更新。countAfter=min(qCount+rise,Target)包括Target降低时无新边沿也截断。Complete按当前Target重算，复位/非法优先。

## 测试对应与补充场景

补Target从2增到3使Complete清零、Target降低且没有上升沿、非法Target期间PartPulse变低再恢复有效、相隔多个低电平后的新边沿；每拍检查Error。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(Error <-> invalid)`

- `P2`：`G((Reset | invalid) -> ((Count = 0) & !Complete))`

- `P3`：`G((!Reset & !invalid) -> (Count = countAfterEdge))`

- `P4`：`G((!Reset & !invalid) -> (Complete <-> (Count >= Target)))`

- `P5`：`G(PartPulse -> X qPulse)`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
