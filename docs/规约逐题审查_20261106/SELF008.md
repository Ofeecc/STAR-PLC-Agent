# SELF008：Consecutive scan qualification with an immediate trip

审查日期：2026-11-06。结论：**基本合理，需固定算术语义**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF008.json)。公式 5 条；测试 2 组、11 拍。

## 题目要求

连续合格请求按扫描累计到1..5预设值，Trip/无请求/非法Preset清零，Preset改变立即生效。

## 已合理表达的部分

P1—P4覆盖所有输入分支，计数饱和，动态降低Preset测试一致；有限上界能支撑P5的条件进展。

## 问题及依据

qCount须绑定上一拍Count与初始0；nextCount用数学整数先加后min，不能把任意USINT溢出语义直接带入参考。若合法状态维持0..5，中间+1实际不会溢出。

## 建议修订

明确invalid↔Preset<1或>5，qCount[0]=0且逐拍更新；计数按清零分支或min(qCount+1,Preset)精确确定，Ready与合法且Count>=Preset等价。P5保留作派生性质。

## 测试对应与补充场景

补Preset增加可使Ready暂时清零、Request/Trip与减小Preset同拍、Preset=255，保证非法值处理一致。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G((Trip | !Request | invalid) -> (!Ready & (Count = 0)))`

- `P2`：`G((Request & !Trip & !invalid) -> (Count = nextCount))`

- `P3`：`G(Ready <-> qualified)`

- `P4`：`G(!invalid -> ((Count >= 0) & (Count <= Preset)))`

- `P5`：`(G(Request & !Trip & !invalid)) -> F Ready`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
