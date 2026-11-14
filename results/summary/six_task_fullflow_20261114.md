# DeepSeek 六题完整流程实测（2026-11-14）

模型：`deepseek-v4.1-flash-1017`；框架：STAR/E3；high 思考强度。

每题重新生成 ST；最终固定测试与最终形式验证使用同一候选源代码哈希。Agent 自测不是最终固定测试。

| 题目 | 难度 | 编译 | 固定用例：通过/已测/计划 | 形式验证 | 完整流程 |
|---|---|---|---|---|---|
| PUB001 | easy | PASS | 7/7/7 | PASS | PARTIAL |
| PUB003 | easy | PASS | 8/8/8 | PASS | PARTIAL |
| PUB007 | medium | PASS | 7/7/7 | PASS | PARTIAL |
| PUB009 | medium | PASS | 7/7/7 | UNSUPPORTED_ST | PARTIAL |
| PUB015 | hard | PASS | 13/13/13 | PASS | PARTIAL |
| PUB016 | hard | PASS | 8/8/8 | UNSUPPORTED_ST | PARTIAL |

完成执行 6/6 题；编译通过 6/6；固定用例通过 50/50，已执行 50/50。

固定测试和已转换性质检查同时通过 4/6；形成完整题库规约证明 0/6。尚未证明不等同于代码错误。

模型请求 19 次；提供商返回 token 统计：{"input_tokens": 85099, "output_tokens": 134429, "total_tokens": 219528}。

只统计本轮六题，修复预检和原批次不计入成绩。PARTIAL/UNSUPPORTED_ST/INCONCLUSIVE/TIMEOUT/TOOL_ERROR 不视为正确或错误程序的证明。

## PUB001

- 生成阶段：PASS；All active self-tests passed
- 固定测试：PASS；详见轨迹
- 形式验证：PASS；详见性质结果
- 转换后检查项：通过 18/18（包含辅助检查项，不等同原题库性质条数）。
- 完整规约覆盖：INCOMPLETE_OR_UNMAPPED；建模语义：SUPPORTED_SYMBOLIC_ST_FRAGMENT。
- 尚未证明或未完成对应的题库性质 ID：`['PUB001.COMPLETE', 'PUB001.P1', 'PUB001.P10', 'PUB001.P2', 'PUB001.P3', 'PUB001.P4', 'PUB001.P5', 'PUB001.P6', 'PUB001.P7', 'PUB001.P8', 'PUB001.P9', 'PUB001.P_init']`。
- 证据目录：`results/raw/six_task_fullflow_20261114/PUB001/`

## PUB003

- 生成阶段：PASS；All active self-tests passed
- 固定测试：PASS；详见轨迹
- 形式验证：PASS；详见性质结果
- 转换后检查项：通过 11/11（包含辅助检查项，不等同原题库性质条数）。
- 完整规约覆盖：INCOMPLETE_OR_UNMAPPED；建模语义：MATHEMATICAL_REALS_NOT_IEEE754。
- 尚未证明或未完成对应的题库性质 ID：`['PUB003.COMPLETE', 'PUB003.P1', 'PUB003.P2', 'PUB003.P3', 'PUB003.P4', 'PUB003.P5', 'PUB003.P6', 'PUB003.P7', 'PUB003.P8', 'PUB003.P9', 'PUB003.P_init']`。
- 证据目录：`results/raw/six_task_fullflow_20261114/PUB003/`

## PUB007

- 生成阶段：PASS；All active self-tests passed
- 固定测试：PASS；详见轨迹
- 形式验证：PASS；详见性质结果
- 转换后检查项：通过 5/5（包含辅助检查项，不等同原题库性质条数）。
- 完整规约覆盖：INCOMPLETE_OR_UNMAPPED；建模语义：SUPPORTED_SYMBOLIC_ST_FRAGMENT。
- 尚未证明或未完成对应的题库性质 ID：`['PUB007.COMPLETE', 'PUB007.P1', 'PUB007.P2', 'PUB007.P3', 'PUB007.P4', 'PUB007.P5']`。
- 证据目录：`results/raw/six_task_fullflow_20261114/PUB007/`

## PUB009

- 生成阶段：PASS；All active self-tests passed
- 固定测试：PASS；详见轨迹
- 形式验证：UNSUPPORTED_ST；Integer MOD is unsupported by the nuXmv SMT backend; exact bit-vector lowering is required
- 转换后检查项：通过 0/9（包含辅助检查项，不等同原题库性质条数）。
- 完整规约覆盖：NOT_EVALUATED；建模语义：NOT_EVALUATED。
- 尚未证明或未完成对应的题库性质 ID：`[]`。
- 证据目录：`results/raw/six_task_fullflow_20261114/PUB009/`

## PUB015

- 生成阶段：PASS；All active self-tests passed
- 固定测试：PASS；详见轨迹
- 形式验证：PASS；详见性质结果
- 转换后检查项：通过 11/11（包含辅助检查项，不等同原题库性质条数）。
- 完整规约覆盖：INCOMPLETE_OR_UNMAPPED；建模语义：SUPPORTED_SYMBOLIC_ST_FRAGMENT。
- 尚未证明或未完成对应的题库性质 ID：`['PUB015.COMPLETE', 'PUB015.P_init']`。
- 证据目录：`results/raw/six_task_fullflow_20261114/PUB015/`

## PUB016

- 生成阶段：PASS；All active self-tests passed
- 固定测试：PASS；详见轨迹
- 形式验证：UNSUPPORTED_ST；Candidate input processLength has no observer binding
- 转换后检查项：通过 0/9（包含辅助检查项，不等同原题库性质条数）。
- 完整规约覆盖：NOT_EVALUATED；建模语义：NOT_EVALUATED。
- 尚未证明或未完成对应的题库性质 ID：`[]`。
- 证据目录：`results/raw/six_task_fullflow_20261114/PUB016/`
