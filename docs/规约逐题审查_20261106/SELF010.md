# SELF010：Latched alarm with acknowledgment and reannunciation

审查日期：2026-11-06。结论：**必须修订确认分支并补保持**。方法：题意、假设、全部公式及现有测试的静态语义审查。

原题数据：[查看 JSON](../../dataset/self_built/SELF010.json)。公式 6 条；测试 2 组、9 拍。

## 题目要求

故障锁存报警，新故障边沿取消确认，持续故障可确认，故障消失后Reset才清除。

## 已合理表达的部分

P1—P5的声光关系、故障置位、新故障优先和有效Reset清除合理；现有reset_priority已明确持续故障时Reset不能阻止Ack。

## 问题及依据

P6用了!Reset，但Reset只在!Fault时有效。Fault持续且Reset=TRUE、Ack=TRUE时，Ack仍应生效，却被P6漏掉。没有完整的Alarm/确认状态保持，也未禁止没有故障时凭空报警/确认。qFault无完整逐拍更新关系。

## 建议修订

定义validReset=Reset & !Fault。优先validReset清Alarm/Ack；否则rise置Alarm并清Ack；否则Fault或qAlarm保持Alarm，若Ack且本来有报警则置确认，否则确认保持；无报警时不得自行确认。完整方程：Alarm↔!validReset & (Fault | qAlarm)；Acknowledged=validReset或rise时FALSE，否则qAck | (Ack & qAlarm)。Horn↔Alarm & !Acknowledged；qFault下一拍等于Fault，所有历史有初值。

## 测试对应与补充场景

保留reset_priority第1零基索引拍作为关键反例；补已确认持续Fault且Reset=TRUE/Ack=FALSE确认仍保持、报警未出现时Ack、故障消失后无Reset长保持、新故障与Ack/Reset同拍。

## 需要固定的题意解释

无需额外题意决定；按下述建议完善。

## 原公式逐条索引

- `P1`：`G(Horn <-> (Alarm & !Acknowledged))`

- `P2`：`G(Fault -> Alarm)`

- `P3`：`G(rise -> (Alarm & !Acknowledged & Horn))`

- `P4`：`G((Reset & !Fault) -> (!Alarm & !Acknowledged & !Horn))`

- `P5`：`G((!Fault & !Reset & qAlarm) -> Alarm)`

- `P6`：`G((!rise & !Reset & Ack & qAlarm) -> Acknowledged)`

以上修订为评审建议，尚未替换正式题库。基本合理不等于已通过形式验证；新增场景尚未写入或运行。
