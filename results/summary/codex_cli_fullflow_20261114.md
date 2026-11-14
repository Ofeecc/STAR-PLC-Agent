# Codex CLI 对照组全题库评测结果（2026-11-14）

完整原始任务证据、事件日志、编译诊断、功能轨迹与形式验证输入输出保存在 `results/raw/codex_matrix_resume_20261114/`；以下汇总仅包含 Codex CLI 两个模型组，与 STAR harness 两组合并构成四组完整对照评测。

| 组别 | 模型 | 完成题数 | 编译通过 | 固定用例通过/有效执行/计划 | 形式检查状态 | 总状态分类 |
|---|---|---:|---:|---:|---|---|
| codex_deepseek | deepseek-v4.1-flash-1017 | 32/32 | 28 | 196/208/276 | PASS 16, TIMEOUT 1, NOT_RUN 4, UNSUPPORTED_ST 8, COUNTEREXAMPLE 3 | PARTIAL 20, TIMEOUT 1, FAIL 10, TOOL_ERROR 1 |
| codex_terra | gpt-6.1-terra | 32/32 | 29 | 220/222/276 | PASS 18, TIMEOUT 1, UNSUPPORTED_ST 9, NOT_RUN 3, COUNTEREXAMPLE 1 | PARTIAL 26, TIMEOUT 1, TOOL_ERROR 2, FAIL 3 |

## 结果说明

- Codex CLI + DeepSeek (`E1`)：32/32 题已记录，28 题编译通过；固定用例 196/208 有效执行通过，题库计划 276 个用例。
- Codex CLI + GPT (`E2`)：32/32 题已记录，29 题编译通过；固定用例 220/222 有效执行通过，题库计划 276 个用例。
- 形式检查中的 `PASS`、`UNSUPPORTED_ST`、`COUNTEREXAMPLE`、`TIMEOUT`、`NOT_RUN` 分开统计；形式 `PASS` 不自动意味着题库全部性质已经逐条证明。
- `PARTIAL`/`FAIL`/`TOOL_ERROR`/`TIMEOUT` 是评测总状态，需结合每题阶段证据判读；工具故障或超时不等于候选程序错误。
- 每道题的候选、事件流 (`events.jsonl`)、编译记录、功能测试轨迹与形式验证产物见 `results/summary/codex_cli_fullflow_20261114.json` 中的仓库相对 `evidence` 路径。

## 证据目录

- `results/raw/codex_matrix_resume_20261114/codex_deepseek/`：DeepSeek Codex CLI 全题库原始证据（32 题）。
- `results/raw/codex_matrix_resume_20261114/codex_terra/`：GPT Codex CLI 全题库原始证据（32 题）。
- `results/raw/four_group_20261114/codex_*`、`results/raw/codex_terra_pilot_20261114/`：历史接口修复与早期试跑记录，保留复核，不计入正式题库分母。
- 机器可读逐题汇总：`results/summary/codex_cli_fullflow_20261114.json`。
