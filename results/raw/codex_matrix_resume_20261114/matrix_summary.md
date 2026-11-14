# 四组完整流程评测

更新：2026-11-14T14:32:58.880470+00:00；状态：COMPLETE_WITH_RECORDED_ERRORS

| 组别 | 框架 | 模型 | 已记录/计划 | 编译通过 | 固定用例通过/有效执行/全量计划 | 形式结果 |
|---|---|---|---|---|---|---|
| star_deepseek | star | deepseek-v4.1-flash-1017 | 11/32 | 11 | 65/67/276 | {'PASS': 5, 'UNSUPPORTED_ST': 6} |
| codex_deepseek | codex_cli | deepseek-v4.1-flash-1017 | 32/32 | 28 | 196/208/276 | {'PASS': 16, 'TIMEOUT': 1, 'NOT_RUN': 4, 'UNSUPPORTED_ST': 8, 'COUNTEREXAMPLE': 3} |
| star_terra | star | gpt-6.1-terra | 0/32 | 0 | 0/0/276 | {} |
| codex_terra | codex_cli | gpt-6.1-terra | 32/32 | 29 | 220/222/276 | {'PASS': 18, 'TIMEOUT': 1, 'UNSUPPORTED_ST': 9, 'NOT_RUN': 3, 'COUNTEREXAMPLE': 1} |

STAR＋DeepSeek 的六题采用已经完成的候选与真实评测，明确列明 imported_completed_pilot；其余题目独立生成。
PARTIAL / UNSUPPORTED_ST / 未执行不等于程序错误或形式证明通过。
有效执行仅计时序符合原定条件的用例；TIMING_NOT_REPRODUCED 与超长时间未执行用例保留在全量计划分母，不计通过。
接口返回费用累计：7.843808 元（含最初六题；不是账户余额；缺失费用字段的请求数 11）。
