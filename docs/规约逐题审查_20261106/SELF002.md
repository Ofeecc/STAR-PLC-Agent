# SELF002：Reversing jog drive with a neutral scan

审查日期：2026-11-06。结论：**基本合理，需绑定历史**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF002.json)。公式 6 条；测试 2 组、10 拍。

## 题目要求

点动正反转，直接换向先给一拍全关，然后可运行新方向。

## 已合理表达的部分

P1—P6穷尽停止、冲突、空命令和合法单向请求；中立一拍的测试符合题意。

## 问题及依据

qForward/qReverse必须是真正前一拍输出，不能绑定上次非零方向，否则中立后会一直禁止反转。初始中立仍依赖文字初值。

## 建议修订

明确qForward[0]=qReverse[0]=FALSE；每拍无条件更新为本拍两个实际输出，包括Stop/双按钮/无按钮产生的中立拍。完整公式可保留。

## 测试对应与补充场景

保留直接换向；补每拍交替按钮、Stop后请求反向、双按钮中立后单向，验证使用的是紧邻上一拍而非最后运行方向。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(!(Forward & Reverse))`

- `P2`：`G((Stop | (ForwardButton <-> ReverseButton)) -> (!Forward & !Reverse))`

- `P3`：`G((fwdOnly & qReverse) -> (!Forward & !Reverse))`

- `P4`：`G((revOnly & qForward) -> (!Forward & !Reverse))`

- `P5`：`G((fwdOnly & !qReverse) -> Forward)`

- `P6`：`G((revOnly & !qForward) -> Reverse)`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
