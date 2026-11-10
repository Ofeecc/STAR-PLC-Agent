# SELF007：Duty standby alternation with healthy pump fallback

审查日期：2026-11-06。结论：**必须补全备用与episode状态**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF007.json)。公式 7 条；测试 2 组、12 拍。

## 题目要求

需求时首选健康泵，故障立即切健康备用；一次有服务的需求结束才交替首选泵。

## 已合理表达的部分

P1—P3互锁和故障禁止、P6/P7交替时机方向合理；测试包含备用接替和未服务需求不交替。

## 问题及依据

P4/P5仅要求首选健康泵必须开，没有要求首选故障时健康备用必须开。LeadA=TRUE且A故障B健康时，两泵均关能满足七条。completedServed缺明确episode历史更新；应避免错误实现从不运行导致永远被判未服务而自洽。

## 建议修订

补G((Demand & FaultA & !FaultB) -> PumpB)及对称条件。更完整：PumpA↔Demand & !FaultA & (qLeadA | FaultB)，PumpB↔Demand & !FaultB & (!qLeadA | FaultA)。completed=previousDemand & !Demand & servedBefore；LeadA=completed?!qLeadA:qLeadA。服务记忆在Demand内累计，结束清零；初始首选A、previousDemand=FALSE、served=FALSE。

## 测试对应与补充场景

保留fallback；补首选B故障时A接替、同一需求中两泵都故障又恢复、已经服务后才全故障仍应在结束交替、连续多拍Demand=FALSE只翻转一次。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(!(PumpA & PumpB))`

- `P2`：`G((!Demand | FaultA) -> !PumpA)`

- `P3`：`G((!Demand | FaultB) -> !PumpB)`

- `P4`：`G((Demand & LeadA & !FaultA) -> PumpA)`

- `P5`：`G((Demand & !LeadA & !FaultB) -> PumpB)`

- `P6`：`G(completedServed -> (LeadA <-> !qLeadA))`

- `P7`：`G(!completedServed -> (LeadA <-> qLeadA))`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
