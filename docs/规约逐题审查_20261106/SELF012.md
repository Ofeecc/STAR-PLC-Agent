# SELF012：Bounded automatic fault retries with a recovery dwell

审查日期：2026-11-06。结论：**必须补全全部转移与计数**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF012.json)。公式 7 条；测试 2 组、20 拍。

## 题目要求

故障后需连续两拍恢复才自动重试，最多两次；第三次运行故障闭锁，只有有效Reset恢复预算。

## 已合理表达的部分

已有故障禁止、预算范围、有效复位、LOCKED保持及部分重试规则；exhaustion/dwell_interrupt期望与完整题意一致。

## 问题及依据

没有IDLE的Start必须运行、RUNNING健康保持、未用完预算故障后必须进入WAIT、第一健康WAIT拍不得提前运行、非重试拍Attempts保持，以及Stop行为。Run永假、Attempts=0、不闭锁的健康输入轨迹能满足七条，说明公式严重不完整。

## 建议修订

按validReset→旧LOCKED保持→Stop→正常状态分支排序。IDLE且Start且!Fault→RUNNING；RUNNING遇Fault则按qAttempts<2进入WAIT，否则LOCKED；WAIT遇Fault清dwell，健康第一拍dwell=1仍WAIT，第二拍RUNNING且Attempts+1；其余保持。Stop从非锁定态回IDLE并清dwell，但不改Attempts。Run↔postState=RUNNING，Locked↔postState=LOCKED；Attempts除有效Reset和自动重试外全部保持。

## 测试对应与补充场景

增加Stop后手动Start不恢复预算、RUNNING持续健康保持、WAIT第一健康拍必须关、LOCKED中Start/Stop均无效、无效Reset不清预算、有效Reset与Stop同拍优先、Attempts=2后手动启动再故障仍应锁定。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(Fault -> !Run)`

- `P2`：`G((Attempts >= 0) & (Attempts <= 2))`

- `P3`：`G(validReset -> (!Run & !Locked & (Attempts = 0)))`

- `P4`：`G((qLocked & !validReset) -> (Locked & !Run))`

- `P5`：`G((qRunning & Fault & normal & (qAttempts = 2)) -> Locked)`

- `P6`：`G((retryDue & normal) -> (Run & (Attempts = qAttempts + 1)))`

- `P7`：`G((qWait & Fault & normal) -> !Run)`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
