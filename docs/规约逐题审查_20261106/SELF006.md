# SELF006：Tank filling with hysteresis and sensor inconsistency

审查日期：2026-11-06。结论：**基本合理，需绑定历史**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF006.json)。公式 5 条；测试 2 组、10 拍。

## 题目要求

上下液位形成补水滞回，上湿下干判故障；抑制和高水位立即关阀。

## 已合理表达的部分

P1—P4覆盖所有上下液位组合与Inhibit分支，P5给初值；两组测试与题意一致。

## 问题及依据

SensorFault是组合故障，不应擅自做成复位锁存。qFill须绑定历史，Inhibit解除在中间液位不自动重启已由保持表达，但监控状态不可丢失。

## 建议修订

明确qFill[0]=FALSE、qFill[k+1]=Fill[k]，SensorFault每拍由HighWet & !LowWet重新计算；无需另加错误保持。可保留原公式作为完整一步规约。

## 测试对应与补充场景

现有10拍覆盖主要边界；补Inhibit时在低位、解除后低位立即开，以及故障恢复到中间液位保持关，区分组合故障与锁存错误。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(SensorFault <-> (HighWet & !LowWet))`

- `P2`：`G((SensorFault | Inhibit | HighWet) -> !Fill)`

- `P3`：`G((!LowWet & !HighWet & !Inhibit) -> Fill)`

- `P4`：`G((middle & !Inhibit) -> (Fill <-> qFill))`

- `P5`：`G(first -> !qFill)`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
