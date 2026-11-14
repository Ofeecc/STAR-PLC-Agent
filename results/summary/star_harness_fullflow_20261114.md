# 自研 STAR Harness 全题库评测结果（2026-11-14）

完整原始任务证据与阶段日志随本目录一并提交；以下汇总仅包含 STAR harness 两个模型组。Codex 对照组另行运行，不计入本报告。

| 组别 | 模型 | 完成题数 | 编译通过 | 固定用例通过/有效执行/计划 | 形式检查状态 | 总状态分类 |
|---|---|---:|---:|---:|---|---|
| star_deepseek | deepseek-v4.1-flash-1017 | 32/32 | 32 | 226/238/276 | PASS 17, UNSUPPORTED_ST 12, COUNTEREXAMPLE 3 | PARTIAL 26, FAIL 5, TOOL_ERROR 1 |
| star_terra | gpt-6.1-terra | 32/32 | 28 | 217/221/276 | PASS 18, TIMEOUT 1, UNSUPPORTED_ST 8, NOT_RUN 4, COUNTEREXAMPLE 1 | PARTIAL 24, TIMEOUT 1, FAIL 4, TOOL_ERROR 3 |

## 结果说明

- STAR + DeepSeek：32/32 题已记录，32 题编译通过；固定用例 226/238 有效执行通过，题库计划 276 个用例。
- STAR + GPT：32/32 题已记录，28 题编译通过；固定用例 217/221 有效执行通过，题库计划 276 个用例。
- 形式检查中的 PASS、UNSUPPORTED_ST、COUNTEREXAMPLE、TIMEOUT、NOT_RUN 分开统计；形式 PASS 不自动意味着题库全部性质已经逐条证明。
- PARTIAL/FAIL/TOOL_ERROR 是评测总状态，需结合每题阶段证据判读；工具故障不等于候选程序错误。
- 每道题的候选、编译记录、功能测试轨迹、形式验证输入输出等原始记录见下方 JSON 中的 `evidence` 路径。

## 证据目录

- `results/raw/batch_fresh_20261114/`：DeepSeek STAR 六题预试跑。
- `results/raw/four_group_20261114/star_deepseek*/` 与 `evaluation_time_normalization/`：DeepSeek STAR 全题库拼合证据来源。
- `results/raw/four_group_20261114/star_terra/`：GPT STAR 全题库原始证据。
- 机器可读逐题汇总：`results/summary/star_harness_fullflow_20261114.json`。

费用与 API 请求记录随各次运行原始证据保留；不可将其他轮次的花费与本轮直接相加后当作账户余额。
