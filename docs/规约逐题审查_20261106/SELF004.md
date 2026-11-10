# SELF004：Pallet indexing with a latched jam fault

审查日期：2026-11-06。结论：**必须补全状态与输出**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF004.json)。公式 7 条；测试 2 组、11 拍。

## 题目要求

托盘IDLE/MOVING/COMPLETE/FAULT，Jam优先，Fault锁存，完成保持，Reset或非故障Stop复位。

## 已合理表达的部分

Jam优先、有效Reset、主要启动和到出口转移以及弱直到的故障保持方向正确；P7没有错误要求操作者最终复位。

## 问题及依据

缺Stop必须回IDLE、MOVING无到位必须持续、COMPLETE保持和完整输出状态等价。P6只排除Belt与Complete/Fault同时真，没有排除Complete和Fault同时真；P2仅要求Fault真也未禁止其他不恰当指示。

## 建议修订

总转移优先级：Jam→FAULT；否则Reset→IDLE；否则旧FAULT保持；否则Stop→IDLE；旧IDLE且Start且!AtExit→MOVING；旧MOVING且AtExit→COMPLETE；否则保持。定义Belt↔postState=MOVING、Complete↔COMPLETE、Fault↔FAULT以及初始IDLE，即覆盖三输出互斥和所有保持。

## 测试对应与补充场景

补从MOVING/COMPLETE分别Stop、FAULT中Stop不能清故障、完成态长保持、三个输出每拍全检查、MOVING多拍无AtExit。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(Jam -> (Fault & !Belt & !Complete))`

- `P2`：`G((qFault & !Reset) -> Fault)`

- `P3`：`G((!Jam & Reset) -> (!Belt & !Complete & !Fault))`

- `P4`：`G((qIdle & !Jam & !Reset & !Stop & Start & !AtExit) -> Belt)`

- `P5`：`G((qMoving & AtExit & !Jam & !Reset & !Stop) -> (Complete & !Belt))`

- `P6`：`G(!(Belt & (Complete | Fault)))`

- `P7`：`G(Fault -> (G Fault | (Fault U (!Jam & Reset))))`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
