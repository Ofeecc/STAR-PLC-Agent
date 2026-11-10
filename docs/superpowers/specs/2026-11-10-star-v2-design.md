# STAR v2：PLC ST 代码生成与自动测试验证平台设计文档

> 状态：已根据评审意见更新（`uv` + `git` 管理、纯自研无状态 STAR harness、`codex-cli`/`claude-code` 公平基线、自动测试与轨迹可视化 Web 平台、全文档与代码去除操作系统环境标识）。

## 1. 现状与要解决的核心问题

现有项目已有：32 题数据集 V2（20 公共 + 12 自建，244 条 LTL、87 组固定测试、29 题可执行契约）、CODESYS 编译与仿真桥接、旧版实验记录与报告初稿。

本次重构要解决的 6 个核心问题：

| # | 问题 | 重构方案 |
|---|---|---|
| P1 | 旧实验基于 V1 题库，V2 后未重跑 | 在冻结的 V2 题库上完成主实验、消融与有无 Spec 对照 |
| P2 | Agent 输入包含评测用的固定测试期望值 | 通过 `agent_view` 白名单严格脱敏，评测测试集与契约对所有 Agent 隐藏 |
| P3 | 原自研 harness 仅做单轮编译修复，设计单薄 | 重构为 **STAR 确定性状态机 Harness**（无需 smolagents 等第三方框架）：控制契约规划 → 方言卡片 → 代码生成 → 行窗口编译修复 → 独立测试员自测 → 首个分歧拍行为修复 + 字典序防回退 |
| P4 | 自动仿真仅覆盖 21/32 题，且缺少交互式测试与轨迹检查工具 | 补齐计时与 `IN_OUT`/复合适配器至 **32/32 全覆盖**；新增**随机差分一致性测试**；搭建**自动测试与轨迹回放 Web 平台** |
| P5 | 基线曾临时换用 smolagents，且缺少自测仿真能力 | 支持 **`codex-cli` / `claude-code` / `deepseek-harness`** 作为基线，通过受控 MCP Server 提供与 STAR 完全对等的 `compile_st` + `simulate_st` 工具与硬性预算限制 |
| P6 | 编译脚本受非 ASCII 路径影响，且文档与命令混杂特定系统标识 | 自动在短 ASCII 工作目录下暂存编译/仿真工程；全项目统一用 `uv run plc-agent ...` 跨平台入口，代码与文档不出现特定操作系统标识 |

---

## 2. STAR Harness 的实现方式（无需 Smolagents）

STAR（**S**pec-anchored · **T**iered verification · **A**rtifact-centric context · **R**egression-guarded repair）完全采用 **Python 标准库 + `requests` 自研实现**，不依赖 `smolagents`、LangChain 等任何第三方 Agent 库。

核心思想：**模型只做局部提议，Harness 负责状态流转、工具执行、记忆裁剪与判停。**

1. **无状态调用 + 工件黑板（Artifact Blackboard）：**
   每次模型调用均不携带长对话历史，而是由控制器从工作区工件现场拼装最小输入：
   - `task_view.json`：脱敏后的任务视图（需求、接口、初值、扫描语义，及可选 LTL 规约）。
   - `contract.json`：**Planner** 产出的结构化控制契约（状态集合、状态转移、信号优先级表、定时器/计数器表、初值表、歧义假设清单）。
   - `dialect_cards.json`：**Dialect Selector** 根据接口类型（`VARIANT`、`ARRAY[*]`、`LTIME`、`STRING`、`IN_OUT` 等）与需求关键词确定性匹配的 CODESYS 方言卡片（每张 ≤15 行，含正确范式与常见反例）。
   - `version_XX.json`：**Coder** 产出的 ST 声明、实现与辅助类型/功能块。
   - `selftest.json`：**Independent Tester** 在独立上下文中（只看 `task_view.json`，不看候选代码与契约）生成的 3–5 组自测序列。
2. **分级验证与精简诊断（Tiered Verification & Diagnostic Compaction）：**
   - **编译级（Compile Repair）：** 编译失败时，对报错去重并截取出错行前后 ±3 行代码窗口。若候选代码哈希与历史重复（停滞），控制器自动注入重构指令并从 `contract.json` 重新生成。
   - **行为级（Behavior Repair）：** 编译通过后，用 `selftest.json` 跑仿真测试。失败用例自动截断到**首个分歧扫描周期（First Diverging Scan）**，反馈"第 k 拍、输入前缀、某输出期望值 vs 实际值"。允许 Coder 修复代码，或附理由驳回自测中本身有误的用例（驳回上限为自测总数的 50%）。
3. **字典序防回退控制器（Lexicographic Ratchet）：**
   - 候选得分定义为 `(compiled: bool, passed_unrejected_selftests: int)`。
   - 只有得分严格提升时才更新 `best_candidate`，防止修复过程中把已通过的逻辑改坏。

---

## 3. Baseline 选择与实验公平性设计（`codex-cli` / `claude-code` / `deepseek-harness`）

为响应课程作业对现成 Coding Agent 框架对比的要求，基线采用**受控 MCP 工具箱 + 隔离工作区**架构，支持通过配置选择 `codex_cli`、`claude_code` 或内置的通用 ReAct 工具调用基线 `deepseek_harness`（标准 ReAct 循环，模型自主决定何时调 `compile_st` / `simulate_st`）：

1. **为什么之前 `codex-cli` 探针会失败、如何彻底解决：**
   - 原因：之前的探针让 CLI 执行本地 Shell 命令读文件，触发了本地命令策略拦截。
   - 解决：将完整脱敏题目直接放入 Prompt，并通过 `plc_agent.mcp_server` 暴露专用 MCP 工具 `compile_st` 与 `simulate_st`，引导 Agent 直接调用 MCP 工具完成编译、自测与修复，无需执行任何本地 Shell 命令。
2. **四项严格公平性保障（Fairness Protocol）：**
   - **输入视图完全一致：** 基线与 STAR 接收完全相同的 `agent_view(task, spec_visible)`。CLI 的工作目录（`--cd`）设为仅包含 `task_view.json` 的独立空目录，与题库目录物理隔离，禁止读取任何评测用例或参考解。
   - **工具能力完全对等：** `plc_agent.mcp_server` 同时提供 `compile_st(source)` 与 `simulate_st(source, cases)` 两个工具。基线同样可以自己构造测试序列提交仿真并根据反例修代码，与 STAR 的自测能力完全对等。
   - **服务端硬性预算执行：** 编译次数上限（`max_compiles = 4`）、仿真次数上限（`max_simulations = 3`）和单任务总超时（`task_timeout = 1500s`）全部在 **MCP Server 与外层进程管理器**中硬性计数与拦截，不依赖外部 CLI 自身的步数参数。
   - **统一的候选提取与黑盒评测：** 评测器只取任务结束前**通过受控编译服务提交的候选代码**（存储在隔离的 `trusted/` 账本目录，Agent 无权篡改），统一用隐藏的固定测试套件 + 随机差分测试套件评测。

---

## 4. 自动测试验证平台与轻量级 Web 前端

搭建统一的自动测试平台与浏览器端可视化工作台（`uv run plc-agent web --port 8765`），采用 Python 标准库 `http.server` + 单页原生 HTML/CSS/JS 实现（零额外前端构建依赖）：

1. **全覆盖自动测试引擎（32/32 题）：**
   - **计时测试适配器：** 支持 `dt_ms` 步进门控与实际调用间隔采集（默认容差 25 ms）。
   - **`IN_OUT` 与复合类型适配器：** 支持结构体数组、变长数组 `ARRAY[*]`、持久化调用方存储（`$binding` + `retain_storage`）与 `VARIANT` 队列绑定，并将复合输出展平后自动还原。
   - **随机差分一致性测试（Random Differential Testing）：** 补齐全部 32 题的可执行 `ScanContract` 参考模型，按固定随机种子生成合法输入序列，在 CODESYS 仿真器中对比候选 ST 与参考模型在每一拍的输出一致性。
2. **形式化验证桥接（Formal Verification）：**
   - 一键导出标准 `.st` 与展开原子命题后的 `.ltl` 规约包（适配课程组 `PLCModelChecker` / `PLCverif`），支持验证结果导入、汇总与展示。
3. **Web 前端四大视图：**
   - **Dataset & Spec 视图：** 浏览 32 道题的需求、接口、LTL 规约、固定测试与随机测试预览。
   - **Auto-Test & Waveform 视图：** 选择或粘贴任意 ST 候选代码，一键运行编译、固定测试、随机差分测试与规约检查；以**逐拍时序表（Scan Waveform Table）**展示每一步的输入、期望输出、实际输出，自动标红首个分歧拍。
   - **Agent Trace 回放视图：** 逐步检视 STAR 的契约、方言卡片、代码版本、编译诊断切片、自测用例及修复过程，或查看 Baseline 的工具调用轨迹。
   - **Experiment & Ablation 看板：** 汇总主实验（`E1`–`E4`）、消融（`A1`–`A3`）、有无 Spec 对照（`S1`–`S2`）的各项指标、McNemar 显著性检验与成本效率对比。

---

## 5. 环境管理、版本控制与跨平台规范

- **环境管理：** 统一使用 `uv`（`pyproject.toml` + `uv.lock`）。所有功能通过 `uv run plc-agent <command>` 执行，单元测试通过 `uv run python -m unittest discover -s tests -v` 执行。
- **版本控制：** 使用 `git` 管理全部源码、题库、规约、测试与文档；`.gitignore` 排除虚拟环境、私有密钥与临时构建目录。
- **无特定系统环境标识：** 代码、CLI、配置文件、实验报告与演示文档均采用跨平台路径处理与中性技术表述，不保留特定操作系统环境标签。编译与仿真后端自动在系统临时目录下的纯 ASCII 短路径中暂存工程并回传证据文件，队友拿到代码后只需执行 `uv sync` 并配置本地 `CODESYS.exe` 路径即可直接运行全套实验。
