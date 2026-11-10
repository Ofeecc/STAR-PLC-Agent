# SELF005：Three phase signal with externally clocked durations

审查日期：2026-11-06。结论：**必须补全时长和输出对应**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF005.json)。公式 7 条；测试 2 组、12 拍。

## 题目要求

外部Tick每拍为真计一逻辑拍，红2/绿3/黄1，禁用清进度，没有Tick保持。

## 已合理表达的部分

逻辑Tick与物理时间分开，P7为带持续使能和无穷Tick前提的活性，方向合理。

## 问题及依据

P1只保一盏灯亮，没有灯与Phase对应。P3只保持Phase，不保持elapsed；P4/P5只约束最后一拍转灯，前几拍允许提前切换，无法保证2/3/1。禁用时没有明确Phase=0及计数清零。多数现有步骤只检查Phase，错误灯可漏过。

## 建议修订

设D(0)=2,D(1)=3,D(2)=1。!Enable→(phaseAfter,ageAfter)=(0,0)；Enable且!Tick→保持；Enable且Tick且ageBefore+1<D→同phase,age+1；否则→((phase+1) mod3,0)。Phase=phaseAfter，Red↔Phase=0、Green↔1、Amber↔2。初始(0,0)，每拍更新ghost，禁止仅从实际Phase反推期望灯。

## 测试对应与补充场景

把每拍三灯和Phase全部列入expected；补绿色计数第1/2拍暂停、各阶段禁用恢复、Tick一直TRUE的完整多周期、Tick一直FALSE不进展。P7只能另作无穷性质，不能从这些有限样本宣布证明。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(oneColor)`

- `P2`：`G(!Enable -> (Red & !Green & !Amber))`

- `P3`：`G((Enable & !Tick) -> (Phase = qPhase))`

- `P4`：`G((Enable & Tick & qRedLast) -> Green)`

- `P5`：`G((Enable & Tick & qGreenLast) -> Amber)`

- `P6`：`G((Enable & Tick & qAmber) -> Red)`

- `P7`：`(G Enable & G(F Tick)) -> (G(F Red) & G(F Green) & G(F Amber))`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
