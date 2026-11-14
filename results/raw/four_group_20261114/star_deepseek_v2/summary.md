# 批量测试进度

完成 4/24 题；本次进程用时 721.9 秒。

| 题号 | 编译 | 固定用例 通过/执行/计划 | 形式检查 | 总状态 |
|---|---|---|---|---|
| PUB004 | PASS | 2/4/8 | UNSUPPORTED_ST | FAIL |
| PUB006 | PASS | 1/1/7 | PASS | PARTIAL |
| PUB008 | PASS | 0/0/9 | UNSUPPORTED_ST | TOOL_ERROR |
| PUB010 | PASS | 4/4/8 | UNSUPPORTED_ST | PARTIAL |

PARTIAL/UNSUPPORTED_ST 不等同于程序错误；形式检查 PASS 也须核对完整规约覆盖与建模语义。
compile.json / functional.json / formal.json 标注 cached、mode、输入指纹和证据；轨迹回放不算本次重新仿真。
模型调用统计为本输出目录中新生成记录的累计值；断点续跑不会把旧调用当成本次新调用。
