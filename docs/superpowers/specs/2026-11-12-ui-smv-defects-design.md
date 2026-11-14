# Design: Web UI Alias/State Popovers, Persistent SMV Verification Status, and Audit Defect Fixes

**Date:** 2026-11-12  
**Status:** Implemented (2026-11-12; commits `8351b61`, `5b54645`, `25e9169`)  
**Baseline Commit:** `164f190` (`feat: add SMV models for all 32 tasks and nuXmv SMT verification`)

---

## 1. Intent, Goals, Non-Goals, and Anti-Goals

### Goals
1. **UI 变量/别名高亮、持久化状态强调与中文悬停浮窗**：
   - 在 Web UI 规约浏览区中，准确区分并高亮接口变量（`INPUT`、`OUTPUT`、`IN_OUT`）、规约别名/原子命题（`atomic_propositions`、`finite_conjunctions`），以及**持久化存储与跨拍状态变量**（`IN_OUT` `retain_storage`、输入驱动参考幽灵前态 `Spre`/`Spost`/`q*`/`pre_*`、`I[k-1]` 边沿记忆、实测输出历史 `O[k-1]`）。
   - 为每个变量与别名提供鼠标悬停（及键盘聚焦）的中文信息浮窗，展示中文名、分类、类型/绑定路径、中文释义及持久化风险提示。
2. **全 32 题 SMV 编写/验证状态持久化入库与 `nuXmv` 缺失处理**：
   - 新建并提交持久化状态文件 `configs/smv_verification_status.json`，记录全部 32 题对应的 `models/{id}_*.smv` 编写清单、模型 SHA256、所需引擎（`bdd` / `smt`）、检查器校验结果与时间戳。
   - 在题库卡片（`.pilot-card`）及打开具体题目详情区（`#task-overview`）的**右上角**清晰展示 SMV 编写状态与验证状态。
   - 当本地缺少 `nuXmv` 或 `NuSMV` 时，优雅降级为显式缺失状态（`CHECKER_MISSING` / `TOOL_UNAVAILABLE`），清晰区分“本地工具未安装”与“模型验证失败/尚未编写”，且不破坏仓库中已入库的持久化基线结果（同时动态比较当前模型 SHA256 检测是否 `STALE`）。
3. **修复本轮审计暴露的 P0 与 P1 缺陷**：
   - P0：接入 `NormalizedScanMonitor` 到主评估链路、消除 `baseline` 与 `harness` 工具上下文不对称、修正 `metrics.py` 形式化统计口径、加固 `dataset.py` 绑定与输入检查、补齐 `simulation.py` 变界数组下界与 `PUB017` `IN_OUT` 支持。
   - P1：修复 `PUB003`/`PUB008`/`PUB010`/`PUB016`/`PUB017`/`PUB018`/`PUB019`/`PUB020`/`SELF005`/`SELF011`/`SELF012` 契约与数据集矛盾，通过新快照 `dataset/specifications/normalized_transition_v2/` 固定更新后的契约哈希，并同步更新 `dataset/` 与 `configs/task_review_zh.json` 校验哈希。

### Non-Goals
- **不做 P2 独立 LTL 全量重写**：不重构全 32 题去掉 `CompleteBehaviorV2` 后的独立 `P1..Pn` 公式体系。
- **不宣称候选 ST 已获形式证明**：所有 SMV 模型校验范围仍固定标注为 `EXPLICIT_SMV_MODEL_ONLY`（`candidate_st_verified: false`）。
- **不提交 `uv.lock` 与 `.local/` 内容**：`uv.lock` 保持未暂存/未提交状态；`.local/model_checkers/` 等本地运行产物不入库。

### Anti-Goals
- 严禁改写历史冻结归档 `dataset_versions/before_normalization_20261111/` 与 `dataset/specifications/normalized_transition_v1/`。
- 严禁在 `nuXmv`/`NuSMV` 缺失时伪造 PASS/TRUE 或隐藏工具错误。
- 严禁在 `baseline`/`harness` 工作区向被测 Agent 暴露参考答案、测试用例或标准状态机源码。

---

## 2. Architecture & Detailed Design

### Component 1: Web UI 变量/别名高亮、持久化状态强调与中文悬停浮窗

#### Backend Data Enrichment ([src/plc_agent/webui.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/webui.py) + [configs/task_review_zh.json](file:///home/ofeecc/Projects/GenAI/configs/task_review_zh.json))
- 在 `configs/task_review_zh.json` 中为每道题补全 `aliases_zh` 字典（键为 `atomic_propositions`、`history_bindings`、`finite_conjunctions` 及核心辅助前缀如 `Spre` / `Spost` / `TimeTick` 中出现但未出现在 `interface_zh` 的别名），包含字段：
  - `label_zh`: 中文短名称
  - `description_zh`: 中文精确定义（涵盖绑定路径、初值、更新规则及与实测输出的边界）
  - `persistence_note_zh` *(可选/针对状态词)*: 跨拍持久化/幽灵状态警告说明
- 后端 `GET /api/task` 响应新增 `symbol_glossary`（按符号名索引的对象字典），整合 `task.interface`、`task.test_bindings`、`task.atomic_propositions`、`normalized_specification.{history_bindings,auxiliary_state_bindings,finite_conjunctions}` 以及 `review.{interface_zh,aliases_zh}`，每项包含：
  - `name`: 符号名
  - `category`: 以下六类之一：
    1. `input` — 采样输入 `I[k]`
    2. `output` — 实测输出 `O[k]`
    3. `persistent_inout` — `IN_OUT` 持久化存储（如 `retain_storage`、引用数组）
    4. `ghost_state` — 输入驱动参考前态/幽灵状态（`Spre.*`、`Spost.*`、`q*` 相位/计时、`prev_*` / `previous-input`）
    5. `obs_history` — 前拍实测输出历史 `O[k-1]`（如 `hiPrev`、`accPrev`、`protectPrev`、`qAttempts`）
    6. `alias` — 纯组合/宏观别名与有限合取宏（`oneHotOutputs`、`badRange`、`AllChannels_*` 等）
  - `category_zh`: 中文分类徽章名
  - `type`: IEC 数据类型或绑定路径
  - `is_persistent`: 布尔值（`persistent_inout`、`ghost_state`、`obs_history` 及显式带状态的别名均标为 `true`）
  - `definition_zh`: 中文悬浮说明
  - `definition_source`: 英文/原规范定义原文
  - `persistence_warning_zh`: 若 `is_persistent=true`，说明跨拍保持、初值复位或“不可与 `O[k-1]` / 候选内部变量混用”的注意点

#### Frontend UI Rendering ([src/plc_agent/webui_assets/app.js](file:///home/ofeecc/Projects/GenAI/src/plc_agent/webui_assets/app.js) + [src/plc_agent/webui_assets/index.html](file:///home/ofeecc/Projects/GenAI/src/plc_agent/webui_assets/index.html))
- **图例与速查面板**：在 `#ltl-container` 上方渲染“图例 + 持久化/别名/接口变量速查表”，默认前置显示持久化/历史状态词，帮助审校者先识别状态与存储假设再看公式。
- **公式词元高亮 (`formatSpec`)**：
  - 将公式中匹配 `symbol_glossary` 的标识符渲染为带样式的交互词元 `<button type="button" class="spec-tok spec-tok--{category}" data-symbol="{name}">...</button>`，与逻辑/时序运算符（`G/F/X/U/R/!/&/|/->/<->`）及括号配对高亮共存。
  - `persistent_inout`、`ghost_state`、`obs_history` 使用更醒目的边框/角标高亮，直观区分“采样输入 / 实测输出 / 持久化及幽灵状态 / 组合别名”。
- **中文悬停浮窗 (`#spec-popover`)**：
  - 支持 `mouseover`、`focusin` 触发，鼠标移出/按下 `Escape` 关闭，并根据视口边缘自动计算定位。
  - 浮窗固定展示中文：符号名 + 中文分类徽章 + 数据类型/绑定路径 + 中文释义 +（若有）持久化警示框 + 可展开/精简原文对照。

---

### Component 2: SMV 编写与验证状态持久化入库 + 缺失 `nuXmv` 处理 + UI 展示

#### Repo-Tracked Status Store & Helper ([src/plc_agent/smv_status.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/smv_status.py) + `configs/smv_verification_status.json`)
- 新增模块 `src/plc_agent/smv_status.py`（只读加载与受控写入）：
  - **动态盘点 `models/`**：针对每道题扫描 `{id}_reference.smv`、`{id}_complete.smv`、`{id}_mutant.smv`，计算实际文件 SHA256，并使用 `model_checker._needs_smt_engine` 判定所需模型检查器（`nuXmv (SMT)` 或 `NuSMV/nuXmv (BDD)`）。
  - **检查本地可执行文件可用性 (`probe_checker_availability`)**：分别探测 `find_nusmv()` 与 `find_nuxmv()`（捕获 `ValueError` 返回 `available: bool` 与缺失原因，不抛出未捕获异常）。
  - **读写持久化清单 `configs/smv_verification_status.json`**：
    - 结构为 `{ "schema_version": 1, "updated_utc": ..., "records": { "<TASK_ID>": { "models": { "<variant>": { "path", "model_sha256", "required_tool", "required_engine", "status", "checked_properties", "expected_properties", "passed_count", "failed_count", "tool", "engine", "tool_exe_sha256", "checked_utc", "error" } }, "last_run_attempt": { ... } } } }`。
    - 实施阶段用当前本机已安装的 `nuXmv` 对 32 题全部参考/完整/变异体模型跑一次全量检查，将真实经过验证的记录写入 `configs/smv_verification_status.json` 并入库。
  - **合成实时展示状态 (`build_task_smv_status`)**：
    - 当无任何 `.smv` 文件：`authoring_status = "NOT_AUTHORED"`，`verification_status = "NOT_AUTHORED"`。
    - 计算各已写模型文件当前 SHA256 与持久化记录中的 `model_sha256` 是否一致；任一存在变化则标记 `stale = true`。
    - 缺失工具判断：结合该题所需引擎（`bdd` 或 `smt`），若本机当前既无对应检查器（例如需 `smt` 时 `nuxmv_available == false`，或需 `bdd` 时两者均 `false`），置 `checker_missing = true`，显式给出缺工具提示（如 `缺失 nuXmv（SMT 题目实时验证不可用）`）。
    - **重要语义分离**：若持久化记录中有完整匹配的 SHA256 验证结果，即使当前机器缺少 `nuXmv`，仍如实区分“当前本机工具缺失（无法实时重跑）”与“仓库已持久化记录（Verified @ <commit/timestamp>）”——即优先显示持久记录结果并叠加 `工具缺失 / 未重跑` 提示；若无持久记录（或记录为 `CHECKER_MISSING` / 已过期），则直接显示 `CHECKER_MISSING`（缺 `nuXmv`/`NuSMV`）。

#### Web API & Live Checking ([src/plc_agent/webui.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/webui.py))
- `GET /api/tasks`：每个任务摘要新增 `smv_status`（含 `authored_variants`、`required_engine`、`verification_status`、`stale`、`checker_missing`、`badge_text_zh`、`badge_text_en`、`badge_tone`）。
- `GET /api/task?id=...`：详情响应新增完整 `smv_status`（含每个变体文件的详细编写与持久化验证结果、本地 `checker_availability`）。
- `POST /api/check-reference-model`：
  - 支持全 32 题与可选字段 `variant`（白名单 `'reference' | 'complete' | 'mutant'`，默认优先 `'complete'` / `'reference'`，并校验 `task_id` 属于已知 32 题以防路径穿越；向后兼容缺省 `variant`）。
  - 执行 `check_model(model_path, output_dir)`：
    - 若抛出工具缺失 `ValueError`（如未安装 `nuXmv` / `NuSMV`），返回 HTTP `503`，响应保留 `"status": "TOOL_ERROR"` 兼容既有契约并附带 `"verification_status": "CHECKER_MISSING"`、`"checker_missing": true`、`"smv_status": ...`，同时更新持久化文件中的 `last_run_attempt` 为 `CHECKER_MISSING`（不破坏匹配 SHA256 的历史已验证证据，但若该变体原本无记录则记为 `CHECKER_MISSING`）。
    - 若检查成功完成，立即将新结果（含 `model_sha256`、`property_results` 计数、`tool`、`engine`、`checked_utc`）原子写回 `configs/smv_verification_status.json`（除非测试传入 mock/临时路径开关，单测使用临时路径隔离），并返回最新 `smv_status`。

#### UI Status Badges ([src/plc_agent/webui_assets/index.html](file:///home/ofeecc/Projects/GenAI/src/plc_agent/webui_assets/index.html) + [app.js](file:///home/ofeecc/Projects/GenAI/src/plc_agent/webui_assets/app.js))
- **题库卡片（`.pilot-card`）**：卡片顶部/状态区展示简洁双段徽章：SMV 编写情况（如 `SMV: 参考+变异`）与验证状态（颜色区分：`已双验` 绿、`参考通过` 青、`缺 nuXmv` 橙、`存在差异/待刷新` 红/黄）。
- **具体打开题目右上角（`#task-overview`）**：将概览卡片改造为左右栏布局，**右上角**专门放置 SMV 状态角标卡，显示：
  - 编写清单（参考 / 完整 / 变异体模型有无及所需引擎 `BDD` / `SMT`）；
  - 持久化验证结果与哈希一致性；
  - 检查器在线状态（`nuXmv 可用` / `缺失 nuXmv`）；
  - 为当前题目（不限于 `PUB001`）提供一键运行 `参考模型` / `变异体模型` 校验按钮并实时更新右上角与卡片徽章。

---

### Component 3: 本轮暴露的 P0 基础设施缺陷修复

1. **接入 `NormalizedScanMonitor` 到主评估流水线 ([src/plc_agent/functional.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/functional.py), [src/plc_agent/normalized_spec.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/normalized_spec.py))**：
   - `outputs_equal(task, actual, expected, inputs)`：区分标量类型，布尔与整型要求精确匹配（`type(actual) is not bool` 且禁止对整数错误套用 `1e-5` 容差），仅声明为浮点或预期为浮点的值应用容差；`PUB008` 调用 `analog_field_matches` / `exact_shape_equal` 时按 `PUB008` 分字段策略执行。
   - `evaluate_trace`：对于含 `normalized_specification` 的任务，使用 `NormalizedScanMonitor` 校验每一步实测输出（含 `PUB017` 删除槽状态保持）；若执行结果包含初始观察 `initial_observed`（如 `trace.get("initial_observed")`），调用 `monitor.check_initial(...)`；对普通每拍轨迹则每步调用 `monitor.step(...)` 检验完整输出。
   - 修复 `normalized_spec.py` 第 144-146 行（`PUB017` 删除槽）：当检测到某槽位在本拍被删除（目标 ID 清为 `0`），不能直接 `deepcopy(got[j])` 放行任意字段结构，须校验 `got[j]` 为合法配方字典且保留字段具备合法有限类型（`ingredientType` 为 `int`、`ingredientRatio`/`productionTemperature` 为有限数字）。
   - 修复 `exact_shape_equal` 对 `PUB008` `REAL` 接口字段遇到测试输入整型字面量（或把 `PUB008.json` `T2` 的 `hiLIM`/`loLIM` 从 `0`/`10` 统一为 `0.0`/`10.0`），确保输入严格校验通过。
2. **消除 `baseline.py` 与 `harness.py` 的工具上下文不对称 ([src/plc_agent/baseline.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/baseline.py), [src/plc_agent/harness.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/harness.py))**：
   - `baseline.py`：工作区写入脱敏的 `view`（`agent_view(task, spec_visible=spec_visible)`），但向 `dispatch(..., task=task, ...)` 传入完整 `task`，使仿真阶段与 `check_contract_trace` / `test_bindings` / `normalized_specification` 一致生效。
   - `harness.py`：工作区仅写入脱敏 `task_view.json`（移除 `write_json(workspace / "task.json", task)` 泄漏），后端仍通过内部参数传入完整 `task`。
3. **修复 `metrics.py` 指标与分母口径 ([src/plc_agent/metrics.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/metrics.py))**：
   - `verification_passes` 仅当 `v.get("verified") is True`（或显式 `status == "PASS"` 且未标 `verified=False`）时计入，**绝不把 `"SAT"`、`"UNSAT"`、`"VERIFIED"` 原样计为形式验证通过**。
   - `rate` 计算统一分母语义：`first_pass_compilation_rate`、`final_compilation_rate`、`test_task_pass_rate`、`verification_pass_rate` 保持既有契约并在输出中显式区分 `planned_tasks` vs `evaluated_tasks`（所有以 `planned_tasks` 为主率的分母保持全量规划基准，补充 `evaluated_test_pass_rate = rate(test_passes, evaluated_tasks)`）。
4. **加固 `dataset.py` 与 `simulation.py` ([src/plc_agent/dataset.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/dataset.py), [src/plc_agent/simulation.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/simulation.py))**：
   - `dataset.validate`：对含 `normalized_specification` 的任务调用 `check_definition_binding(task)`（真正核对 SHA256 而非只判非空）；对测试用例增加额外未定义输入键 `extra_inputs = step.get("inputs", {}).keys() - inputs` 检查；并用 `NormalizedScanMonitor` 交叉核验每道题全部固定用例 `tests`。
   - `simulation.py`：`generate_assignments` 与 `get_case_inouts` 优先读取 `case.get("array_lower_bounds")` / `task.get("test_bindings")`（如 `PUB008` 的 `analogValues` `-2`、`channels` `7`）来生成 `ARRAY[low..high]` 与数组下标循环，不再硬编码 `1`；补充 `PUB017` `recipe` `IN_OUT` 绑定与结构数组初始化支持。

---

### Component 4: 本轮暴露的 P1 契约与数据集缺陷修复

1. **版本化迁移至 `normalized_transition_v2`**：
   - 保持 `dataset/specifications/normalized_transition_v1/` 与 `dataset_versions/before_normalization_20261111/` 只读不动。
   - 更新 `scripts/normalize_specifications.py` 写入新快照目录 `dataset/specifications/normalized_transition_v2/`（记录 `VERSION = '2.2-normalized-20261112'`），重算 32 题 `normalized_specification.transition` SHA256，并同步更新 `configs/task_review_zh.json` 的 `dataset_sha256`、`source_task_sha256` 与 `tests_zh.*.source_sha256`。
   - 同步更新 `tests/test_spec_normalization.py` 中的历史基线比对（显式验证仅允许本轮记录的修复字段发生变化，未修改题目的 `requirements`/`interface`/`tests`/`initial_conditions`/`assumptions` 仍与归档严格一致）。
2. **逐题契约与数据集修复明细**：
   - **`PUB017`** ([data_contracts.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/data_contracts.py)): 新增操作在 `recipeIn.recipeID <= 0` 时拒绝写入并抛出 `ValueError`（符合 `PUB017.json` “仅接受正非零 ID”域策略）；将静默并发请求在文档中明确为静态判定优先级或保持单沿验证并在 `PUB017` 测试与 `random_testing.py` 中补充边界用例。
   - **`PUB010`** ([scan_contract.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/scan_contract.py)): 增加 `self.clock_initialized` 状态，确保首拍（`k=0`）`clock` 从 `0` 起步而非把首拍 `dt_ms` 累加进初始计时起点；当 `fault`（温度不在 `0..100`）有效时冻结 `self.demand`，不再按超限故障值翻转滞回需求。
   - **`PUB016`** ([dataset/public/PUB016.json](file:///home/ofeecc/Projects/GenAI/dataset/public/PUB016.json)): 将顶层 `initial_conditions.sequenceIndex` 从 `1` 修正为 `0`，与 `reference_state_initial.state.index = 0` 及 `CompleteBehaviorV2` 描述统一。
   - **`PUB019`** ([process_contracts.py](file:///home/ofeecc/Projects/GenAI/src/plc_agent/process_contracts.py)): 当 `not safe or cur_mode is None` 时将 `self.arm_mode = None` 清空，避免安全失灵或空模式退出后重新切回原模式时漏触发模式变更复位。
   - **`SELF012`** ([dataset/self_built/SELF012.json](file:///home/ofeecc/Projects/GenAI/dataset/self_built/SELF012.json)): 修复 `atomic_propositions.qAttempts` 及 `normalized_specification.history_bindings`——明确区分输入驱动参考前态计数 `Spre.reference.state.attempts`（供 `P5`/`P6` 与 `qRunning`/`retryDue` 保持同一语义基准）与实测历史 `O[k-1].Attempts`，并在 `initial_observed` 中补齐 `Run: False, Locked: False`。
   - **`SELF005` & `SELF011`** ([dataset/self_built/SELF005.json](file:///home/ofeecc/Projects/GenAI/dataset/self_built/SELF005.json), [SELF011.json](file:///home/ofeecc/Projects/GenAI/dataset/self_built/SELF011.json)): 由各输出初始值填充 `normalized_specification.initial_observed`（告别空字典 `{}`）。
   - **`PUB008`, `PUB020`, `PUB003`**:
     - 将 `PUB008` `T2` 中的整数 `hiLIM: 0`/`loLIM: 10` 修正为浮点 `0.0`/`10.0`；对齐 `PUB008` `T1.tolerance` 与 `normalized_spec.py` 分字段容差（统一采用 `T1` 所声明且已在规约说明的容差策略：转换 `outputValue` `abs=1e-4, rel=1e-5` 或同步规范表述为同一基准，设计实现上以兼容 `REAL` 转换的 `abs=1e-4, rel=1e-5` 对齐两者）。
     - `PUB020`：`firingTemp` 在 `500..550` 区间 32 位 IEEE `REAL` 1 ULP 约为 `6.1e-5`，在 `normalized_spec.py` 与 `PUB020.json` 中将该输出的绝对容差标定为 `1e-4`。
     - `PUB003`：在 `PUB003.json` `assumptions`/`normalized_specification` 中补充明确注释说明独立 `ltl` 阈值表达式按参考契约 IEEE binary32 (`real32`) 边界求值，消除精确实数与单精度舍入的歧义。
   - **`random_testing.py`**: 解除对 `PUB015`、`PUB016`、`PUB017`、`PUB018`、`PUB019` 的过度锁死约束，保留合规前提下允许触发过程切换模式、回退路线（如 `4 -> 2 -> 5`）与多请求冲突测试分支（配合参考合同预期）。

---

## 3. Global Invariants & Error Handling

- **缺失 `nuXmv` 降级原则**：UI 与 `/api/tasks`、`/api/task` 绝不因本地没有 `nuXmv` 而报错失败（必须正常返回 200 及完整展示数据）；仅在用户主动触发 `POST /api/check-reference-model` 且所需检查器缺失时返回 HTTP `503` + `verification_status: "CHECKER_MISSING"` + `checker_missing: true`。
- **路径安全**：`POST /api/check-reference-model` 严禁接受任意路径；`task_id` 必须命中已加载 32 题 ID，`variant` 必须为 `'reference' | 'complete' | 'mutant'` 白名单。
- **测试隔离**：所有 Web UI 单测涉及修改 `configs/smv_verification_status.json` 时，通过依赖注入/临时路径 patch 隔离，避免跑单元测试污染入库状态文件。

---

## 4. Verification Strategy

1. 全部 Python 单元测试套件：`uv run python -m unittest discover -s tests` 全部通过（含新增的 UI 别名/浮窗接口测试、SMV 状态持久化与 `nuXmv` 缺失模拟测试、`normalized_spec` 主评估接入测试、P0/P1 回归测试）。
2. 全量 32 题 SMV 模型通过本地 `nuXmv` 验证并生成入库的 `configs/smv_verification_status.json`。
3. 数据集自检：`python3 -m plc_agent.cli validate-dataset`（或对应模块调用）返回零错误。
4. 通过无头/HTTP 烟测验证 Web UI `/`、`/api/tasks`、`/api/task` 与前端 JS 语法无报错。
