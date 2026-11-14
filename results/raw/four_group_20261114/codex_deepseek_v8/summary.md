# 批量测试进度

完成 1/1 题；本次进程用时 93.2 秒。

| 题号 | 编译 | 固定用例 通过/执行/计划 | 形式检查 | 总状态 |
|---|---|---|---|---|
| PUB001 | NOT_RUN/FAIL | 0/0/7 | NOT_RUN | TOOL_ERROR |

PARTIAL/UNSUPPORTED_ST 不等同于程序错误；形式检查 PASS 也须核对完整规约覆盖与建模语义。
compile.json / functional.json / formal.json 标注 cached、mode、输入指纹和证据；轨迹回放不算本次重新仿真。
模型调用统计为本输出目录中新生成记录的累计值；断点续跑不会把旧调用当成本次新调用。
