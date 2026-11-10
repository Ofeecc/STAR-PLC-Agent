# SELF003：Emergency stop reset with restart inhibition

审查日期：2026-11-06。结论：**必须补全保持**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF003.json)。公式 6 条；测试 2 组、10 拍。

## 题目要求

上电和急停后必须先满足安全复位，再允许Start；解除后保持运行直到停止或急停。

## 已合理表达的部分

P1—P4正确约束初始闭锁和有效复位，P5/P6的启动停止优先级一致。

## 问题及依据

缺!qRequired且安全时ResetRequired保持FALSE，也缺无Start/Stop时Run保持。因而已启动后下一拍自动停机，或者无理由重新闭锁，可能满足现有六条。现有reset_restart第3个零基索引拍检查了Run保持，说明测试要求强于公式。

## 建议修订

增加G((!qRequired & EStopNC) -> !ResetRequired)和G((!qRequired & EStopNC & !Stop & !Start) -> (Run↔qRun))；qRun/qRequired每拍绑定前一输出。完整优先级为急停→若闭锁则只尝试有效复位且Run关→Stop→Start→保持；解除闭锁当拍不能启动。

## 测试对应与补充场景

保留旧测试；补解除后长时间空闲不重新闭锁、运行中Reset不停止、Stop后不必再次Reset、Start与Stop同拍停止、急停与Reset同拍闭锁。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(first -> (qRequired & !qRun))`

- `P2`：`G(!EStopNC -> (!Run & ResetRequired))`

- `P3`：`G(qRequired -> !Run)`

- `P4`：`G((qRequired & EStopNC) -> (ResetRequired <-> !validReset))`

- `P5`：`G((!qRequired & EStopNC & !Stop & Start) -> Run)`

- `P6`：`G((!qRequired & EStopNC & Stop) -> !Run)`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
