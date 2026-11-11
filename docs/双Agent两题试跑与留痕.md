# PUB001 / PUB003 自研 Agent 试跑与留痕

范围变更：用户取消本轮基线试跑；当前仅执行 PUB001 STAR、PUB003 STAR 两组。后续基线拟采用 codex-cli、Claude Code 等成熟框架，现有 custom_tool_loop 暂不作为本轮对比对象。

最新完整重跑已结束（北京时间2026-11-10 22:32—22:37）：PUB001 实际编译、自测和固定测试通过，固定测试2/2用例、16/16步；PUB003 被模板库名称与题目输出 `error` 的 SA0027 冲突拦截，代码修复请求随后耗尽8192输出 token，未进入 Tester。两题共6次实际请求、49,908 token（包括失败请求），不能记为两题全通过。详见 `results/raw/pilot_pair_2026-11-10T143217961073+0000/本轮结果.md` 和同目录 `usage_and_evidence_audit.json`。该历史批次Tester为16384，其余阶段为8192；2026-11-11后续配置已调整，原始实验未改写。

首轮记录：PUB001 首次编译通过，独立 Tester 的响应因 max_output_tokens 截断后流程停止；保留代码的单独固定评测为2/2用例、16/16步通过。记录见 `results/raw/pilot_pair_2026-11-10T141534862064+0000/试跑记录与继续方案.md`。曾准备准确复用已完成请求的继续方案；用户随后要求提高 Tester 上限、从头重跑两题，当前配置采用完整重跑，不启用缓存复用。

当前配置：`configs/pilot_pair.json`。模型deepseek-v4.1-flash-1017、high、本地128K上下文；Planner输出16384、Coder24576、修复32768、Tester24576。每题累计安全阈值300000 token、最多9次请求；单请求420秒、单题2400秒；pilot候选编译最多3次、自测3次，最后固定验收1次。自测范围仍为2例、每例最多8步。新参数尚未付费试跑，详见 `docs/模板库与Token配置建议_20261111.md`。

128K 是本地输入加预留输出的限制，不修改模型服务自身的最大窗口。当前采用完整 JSON 上下文的 UTF-8 字节数加256作为保守计数代理，并记录计数方法；真实用量以 API 返回 usage 为准。超限停止请求，完整历史仍保存，便于人工调整；无静默截断或自动摘要。high 是请求参数，记录在原始请求中。

先从仓库根目录运行 `python scripts/run_pilot_pair.py` 查看计划。实际 API 实验须获得用户明确批准后，才能运行 `python scripts/run_pilot_pair.py --run --allow-model-api`。所用 Python 环境需安装本项目，或设置 PYTHONPATH=src；真实 CODESYS 编译与仿真须在正常 Windows 进程运行。

实验顺序：PUB001 STAR、PUB003 STAR，两组合计最多18次模型请求。基础设施错误停止后续实验，保留已获得证据；没有自动付费重跑。固定测试只在生成完成后执行，其结果不会返回给 Agent 继续修改代码。

每次运行创建独立 `results/raw/pilot_pair_时间戳`：

| 文件或目录 | 内容 |
| --- | --- |
| plan.json / runtime_config.json | 预算、模型、框架、模板哈希与运行参数；不含 Key |
| source_snapshot / source_manifest.json | 本轮使用的源码副本及文件哈希，包含未提交的修改 |
| 各组 task_view.json 或 task.json | Agent 实际可见的题目与规约 |
| 各组 evaluation_task.json | 固定评测的完整题目与测试数据，生成阶段不发送给 Agent |
| llm_* 或 turn_*/request.json | 每轮完整模型输入、工具定义、思考强度和输出预算 |
| llm_* 或 turn_*/context.json | 上下文哈希、计数方式、预算以及是否截断 |
| llm_* 或 turn_*/response.json / events.json | 服务实际返回的内容、协议事件、用量和可见摘要 |
| model_calls.jsonl | 每次请求的开始、结束、失败、预算拦截和时间 |
| execution.jsonl / turn_*/tool_*.json | 工具调用及结果、编译和仿真过程 |
| compile_* / compiler_records / sim_* | 各版本候选代码、CODESYS 诊断和自测证据 |
| fixed_evaluation | 最终固定测试的程序、实际输入输出轨迹、逐步判定 |
| summary.json / trace_index.json | 本轮各组汇总与留痕文件索引 |

以上日志保留应用提交的上下文及服务实际返回内容。API Key 在写入请求、响应和事件日志时脱敏，不复制 .env 和 runtime.local.json。候选 ST 的形式验证状态单独列为 UNVERIFIED；手写参考 SMV 的验证结果不计入这些 Agent 实验成绩。
