# SELF001：Guarded motor with retained run command

审查日期：2026-11-06。结论：**基本合理，可作首个完善样例**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF001.json)。公式 5 条；测试 2 组、10 拍。

## 题目要求

带门许可的自保持电机，停止或开门优先；关门时Start仍高允许启动。

## 已合理表达的部分

P2—P4覆盖全部输入分支，P1给出初始化，P5是可由这些分支推出的保持性质；两组测试期望一致。

## 问题及依据

qRun应明确绑定上一拍实际Run，或绑定独立参考状态但全流程一致。仅P1初始化加P2—P5并没有单独写历史递推；不能让qRun成为任意布尔值。

## 建议修订

补qRun[0]=FALSE，qRun[k+1]=Run[k]的监控绑定；可用总方程Run↔GuardClosed & !Stop & (Start | qRun)作为完整一步规约。P5可保留作冗余一致性检查。

## 测试对应与补充场景

增加首次调用直接Start=TRUE的显式用例，检查不会因初始Run=FALSE而错误要求首拍仍关。无需添加边沿或人工复位条件。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(first -> !qRun)`

- `P2`：`G((Stop | !GuardClosed) -> !Run)`

- `P3`：`G((Start & !Stop & GuardClosed) -> Run)`

- `P4`：`G((!Start & !Stop & GuardClosed) -> (Run <-> qRun))`

- `P5`：`G(Run -> X(Stop | !GuardClosed | Run))`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
