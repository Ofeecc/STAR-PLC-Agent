# 批量测试进度

完成 16/16 题；本次进程用时 1030.4 秒。

| 题号 | 编译 | 固定用例 通过/执行/计划 | 形式检查 | 总状态 |
|---|---|---|---|---|
| PUB014 | PASS | 0/8/8 | UNSUPPORTED_ST | FAIL |
| PUB018 | PASS | 0/0/9 | UNSUPPORTED_ST | TOOL_ERROR |
| PUB019 | PASS | 16/17/17 | COUNTEREXAMPLE | FAIL |
| PUB020 | PASS | 10/11/11 | COUNTEREXAMPLE | FAIL |
| SELF001 | PASS | 7/7/7 | PASS | PARTIAL |
| SELF002 | PASS | 7/7/7 | PASS | PARTIAL |
| SELF003 | PASS | 10/10/10 | PASS | PARTIAL |
| SELF004 | PASS | 9/9/9 | PASS | PARTIAL |
| SELF005 | PASS | 7/7/7 | PASS | PARTIAL |
| SELF006 | PASS | 7/7/7 | PASS | PARTIAL |
| SELF007 | PASS | 9/9/9 | PASS | PARTIAL |
| SELF008 | PASS | 7/7/7 | PASS | PARTIAL |
| SELF009 | PASS | 7/7/7 | PASS | PARTIAL |
| SELF010 | PASS | 8/8/8 | PASS | PARTIAL |
| SELF011 | PASS | 12/12/12 | PASS | PARTIAL |
| SELF012 | PASS | 9/9/9 | PASS | PARTIAL |

PARTIAL/UNSUPPORTED_ST 不等同于程序错误；形式检查 PASS 也须核对完整规约覆盖与建模语义。
compile.json / functional.json / formal.json 标注 cached、mode、输入指纹和证据；轨迹回放不算本次重新仿真。
模型调用统计为本输出目录中新生成记录的累计值；断点续跑不会把旧调用当成本次新调用。
