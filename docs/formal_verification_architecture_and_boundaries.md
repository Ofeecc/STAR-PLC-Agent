# 自研 IEC 61131-3 ST 形式化验证器：原理、能力边界与严谨返回规范

本文档系统阐述本项目中自建的 **ST → SMV 符号化形式验证引擎**（[st_verifier.py](../src/plc_agent/st_verifier.py)）、底层模型检测器（**NuSMV** 与 **nuXmv**，[model_checker.py](../src/plc_agent/model_checker.py)）的工作原理、三层能力边界划分，以及面对不确定结果或超边界语法时所采取的**六态严谨返回机制**。

---

## 1. 系统定位与双模角色

在本仓库中，自建形式验证器同时承担两类完全解耦的工程角色（详见 [formal_verify.py](../src/plc_agent/formal_verify.py)）：

1. **基准事后独立核查器（Post-hoc Benchmark Verifier）**
   - 通过 CLI `verify-candidate`（支持单题、`--all-references` 全量参考示例验收、以及 `--condition` 批量补核实验记录）或 WebUI 后端路由 `POST /api/verify-candidate` 调用。
   - **完整保留反例与观察器上下文**（`include_expected_observer=True`），输出每条 LTL / INVAR 性质的逐条判定、反例波形（`waveform`）、生成模型路径（`candidate_coupled.smv`）及哈希审计清单（`verification_manifest.json`）。
2. **Agent 闭环验证工具（In-the-Loop Tool & CEGAR）**
   - **MCP 工具接口（[mcp_server.py](../src/plc_agent/mcp_server.py) & [baseline.py](../src/plc_agent/baseline.py)）**：向自研 Agent 与对照基线（`deepseek_harness`、`codex_cli`、`claude_code`）均等暴露 `verify_st` 工具，受 `max_verifications` 预算约束。
   - **STAR v2 Step 3.5 CEGAR（[harness.py](../src/plc_agent/harness.py)）**：候选 ST 编译通过后，自动运行形式化核查并驱动多轮反例引导修复（`llm_cegar_XX`），与三维词典序棘轮 `(compiled_ok, verified_props, passed_selftests)` 联动。
   - **零泄漏隔离保证**：面向 Agent 的所有调用强制设置 `include_expected_observer=False` 并经 `sanitize_counterexamples_for_agent` 清洗——仅返回 `{step, inputs, observed}`，彻底剥离 `observer_vars`（参考实现预期输出及辅助观察状态）与 `internal_state` 细节，避免测试预言机泄漏。

---

## 2. 自研 ST-to-SMV 转换验证器核心原理

自研验证器 `st_verifier.py` 并非调用第三方黑盒转换器，而是针对 **IEC 61131-3 结构化文本（Structured Text, ST）单一周期扫描模型**构建的专用符号编译器，完整流水线包含以下 5 个阶段：

```text
  Candidate ST (declaration + implementation + supporting_objects)
        │
        ▼  [阶段 1] 词法/语法解析 + DUT/枚举展平 (parse_st_function_block)
        │
        ├──▶ [阶段 2] 声明级初值核查 (check_st_initial_instance, t = -1)
        │
        ▼  [阶段 3] 单周期 SSA 符号编译 (_STToSMVCompiler)
        │           ├─ 组合网表 DEFINE (IF/CASE 右结合复用, FOR 静态展开)
        │           ├─ 跨周期状态寄存 (VAR / VAR_OUTPUT / VAR_IN_OUT)
        │           └─ 标准功能块精确编码 (TON/TOF/TP/R_TRIG/F_TRIG/SR/RS/CTU/CTD)
        │
        ▼  [阶段 4] 观察器耦合与安全类型判定 (compile_st_to_smv)
        │           └─ 接入 models/*_{complete,reference}.smv，按安全判定选择 BDD / SMT
        │
        ▼  [阶段 5] 调度 NuSMV / nuXmv + 反例清洗 + 六态判定 (verify_candidate_st)
```

### 2.1 PLC 周期扫描与时间步对应关系
- **$t = -1$（`INITIAL_INSTANCE` 声明态）**：IEC 61131-3 功能块实例化之后、首次扫描执行之前，各输出端口持有声明默认值（如 `BOOL` 默认 `FALSE` 或显式 `:= TRUE`）。`check_st_initial_instance` 直接基于 AST 类型与常量表达式 `default_python_value` 在静态阶段核查 `task["initial_conditions"]`（跳过参考观察器私有内部变量），一旦不匹配立即报告 `INITIAL_INSTANCE` 反例（对应波形 `step: -1`）。
- **$t = 0, 1, 2, \dots$（离散扫描周期）**：在每个 SMV 状态转移步中：
  - `VAR_INPUT` 对应当前周期自由输入符号（或耦合观察器输入）；
  - `VAR`、`VAR_OUTPUT`、`VAR_IN_OUT` 构成跨周期状态寄存器 `cand_state_*`，在每次扫描开始时读取上一周期末的值，经本周期语句顺序求值后的最终值绑定到 `DEFINE` 输出端口 `cand_out_*`，并通过 `next(cand_state_*) := ...` 写回下一周期；
  - `VAR_TEMP` 在每个周期开始时重置为常量默认初值，不跨周期记忆；`VAR CONSTANT` 内联为符号常量。

### 2.2 AST 解析与复合类型展平
- `parse_st_function_block` 支持 `TYPE ... END_TYPE` 中的 `STRUCT`、具名 `ENUM`（含显式整型初值）、类型别名与 `INT(lo..hi)` 子界，支持 `ARRAY[lo..hi]` 一维及多维数组。
- `_flatten_type_leaves` 将所有 `STRUCT` 与静态边界 `ARRAY` 递归展平为叶级标量单元（如 `arr[1].speed` 映射到唯一键 `("arr", 1, "speed")`）。因此结构成员或定长数组元素的读取/赋值均转化为纯标量环境中的精确符号绑定。

### 2.3 单扫描周期 SSA 与控制流合并
- 单个扫描周期内的顺序语句可能对同一变量多次读-改-写。`_STToSMVCompiler` 维护路径键到 `SMVExpr` 的不可变映射环境 `env`：
  - 每次变量写入更新当前 `env[key]`；当表达式较长或含条件选择 `? :` 时，通过 `_fresh_ssa` 生成 `DEFINE cand_ssa_k := ...;`，既消除冗余重复展开导致的表达式指数爆炸，又保证单周期内严格遵循前写后读的顺序语义。
  - **分支（`IF/ELSIF/ELSE` 与 `CASE`）**：分别独立符号执行各分支并传播分支生效条件 `active_cond`，随后自右向左通过 `_merge_envs` 生成 SMV 三目多路选择器 `((cond) ? then_val : else_val)`。
  - **有界循环（`FOR`）**：要求初值、终值与非零步长均为编译期可求值常量整数，在严格上限 `<= 256` 次迭代内做静态展开。
  - **动态数组下标**：读写 `arr[idx]` 时若 `idx` 非编译期常量，则展开为覆盖数组合法索引集合的条件写回/多路读取链。

### 2.4 标准功能块（FB）精确转移与物理时钟耦合
内置支持 `TON`、`TOF`、`TP`、`R_TRIG`、`F_TRIG`、`SR`、`RS`、`CTU`、`CTD` 九类标准功能块。关键约束如下：
- **定时器与物理时间**：优先复用任务观察器中声明的 `dt_ms`、`first_scan` 与单调非负时钟 `clk_now`（若无则自生成满足 `dt_ms >= 0`、`clk >= 0`、`first_scan -> clk_now = 0` 的非零步长符号时钟），精确建模 `TON/TOF/TP` 的 `Q` 与 `ET` 状态演化。
- **未调用实例冻结**：若候选程序在 `VAR` 中声明了某个 FB 实例但本周期未调用，编译器会显式生成 `next(sv) := sv` 自环保持，防止未驱动的状态变量在 SMV 中沦为每步任意跳变的自由变量（避免引入虚假反例）。
- **严格禁止条件/循环内调用**：详见第 3 节能力边界。

### 2.5 观察器耦合与安全护栏
- `compile_st_to_smv` 加载任务经过人工审核与变异体校准的 `models/*_{complete,reference}.smv`（利用括号平衡状态机安全剥离多行 `case ... esac` 块内的语句）。
- 自动将观察器内与候选端口一致的输入变量与输出 `DEFINE` 替换对接至候选 ST 编译产物 `cand_in_*` / `cand_out_*`（支持 `PUB007` 等 `VAR_IN_OUT` 展平数组映射），保留观察器自身的参考不变量/LTL 约束及辅助状态判定。
- 若观察器包含追踪被测输出的小整数子界变量（例如 `qMode : 0..3`），系统会将其自动加宽为 `0..255` 或 `integer`，避免存在缺陷的候选输出在进入性质判定前直接引发 NuSMV 变量赋值越界异常。

---

## 3. 三层能力边界矩阵

为了确保**形式化证明决不出现“假通过（False Positive）”或“崩溃冒充反例（False Negative）”**，我们将整体系统的能力严格划分为以下三层边界：

### 3.1 第一层：自研 ST-to-SMV 转换器能力边界

| 维度 | 支持的可验证片段（Sound Fragment） | 超出边界 / 显式拒绝（抛出 `UnsupportedSTConstructError` → 返回 `UNSUPPORTED_ST`） |
| :--- | :--- | :--- |
| **数据类型** | `BOOL`、`SINT`/`USINT`/`BYTE`、`INT`/`UINT`/`DINT`/`UDINT`/`LINT`/`ULINT`、`WORD`/`DWORD`/`LWORD`、`REAL`/`LREAL`、`TIME`/`LTIME`、显式范围 `STRUCT`、`ENUM`、固定边界 `ARRAY[lo..hi]`（单维 `<= 128`） | `VARIANT`（如 `PUB018`）、`STRING` / `WSTRING`、`ANY*` 泛型、`POINTER`、`REFERENCE`、可变长度数组 `ARRAY[*]`、单维长度 `> 128` 的大数组、未声明外部结构体 |
| **控制流** | `IF / ELSIF / ELSE`、`CASE ... OF`（含区间标签 `lo..hi` 与枚举标签）、编译期常量界与非零常量步长的 `FOR`（迭代 `<= 256` 次） | `WHILE`、`REPEAT` 潜在无界循环；非常量边界或迭代 `> 256` 的 `FOR`；`FOR` 内早退出 `EXIT`；提前 `RETURN`；`GOTO` |
| **函数与功能块** | 单周期内**无条件调用恰好一次**的 `TON`、`TOF`、`TP`、`R_TRIG`、`F_TRIG`、`SR`、`RS`、`CTU`、`CTD`；内置纯函数 `ABS`、`MIN`、`MAX`、`LIMIT`、`SEL`、`MUX` 等 | **条件分支（`IF`/`CASE`）或循环体（`FOR`）内部调用有状态 FB 实例**；单周期重复调用同一 FB 实例；用户自定义子 `FUNCTION` / `METHOD` / 嵌套自定义 `FUNCTION_BLOCK` 调用 |
| **表达式与内存安全** | 布尔逻辑、整数/实数四则与 `MOD`、比较、位向量逻辑、静态与动态索引读写（动态索引展平为合规区间选择）、常量初值 | 编译期**静态数组下标越界**（如对 `ARRAY[1..5]` 静态读写 `arr[99]`）；对非数组变量做动态索引；常量零除 / 零模运算（`/ 0`、`MOD 0`）；非常量成员初始化；未声明变量或结构体未知字段 |
| **规约契约耦合** | 仓库中存在对应 `models/<TASK>_{complete,reference}.smv` 且接口映射完备的任务 | 缺少可用观察器模型、观察器端口与任务接口映射不全（如 `PUB017` 字符串/复杂多字段未建模输出）、或候选 ST 缺少任务契约要求的输出端口 |

> **关键设计原则：为什么禁止条件/循环内调用有状态 FB？**
> 在 IEC 61131-3 中，若将 `TON` 放入 `IF cond THEN timer(IN := TRUE, PT := T#5S); END_IF;`，当 `cond` 为 `FALSE` 时定时器根本未被扫描，`ET`/`Q` 保持冻结；然而很多工业编码或简化模型容易误把分支内 FB 等价于 `IN := FALSE`。为杜绝与实机 CODESYS 行为产生静默语义偏差，转换器主动传播分支守卫 `active_cond` 与循环深度 `_loop_depth`，**一旦检测到条件或循环内调用有状态 FB，立即拒绝并给出提示**：引导 Agent 将其重构为“周期顶层无条件调用，通过 `IN := cond` 传入条件”。

---

### 3.2 第二层：NuSMV（有限状态 BDD / SAT 引擎）能力边界

- **引擎能力**：针对纯布尔、枚举及小有界整数域（BDD 默认无 SMT 特性时）构造精确符号转换关系，执行 CTL / LTL / INVAR 的**全局完备（Complete）状态空间可达性分析**。只要未触发超时或内存耗尽，必能给出确切的 `is true`（无任何反例的全局证明）或 `is false`（最小/见证反例）。
- **有限整数子界优化（`-128..255`）的安全启动判据**：
  - 对纯状态机类任务（如 `PUB001`、`SELF001`–`SELF012`），即使用户代码声明 `state : INT := 0` 来存有限枚举状态（0/1/2），若盲目将其编译为数学无限 `integer` 会迫使求解器从 0.05s 的 NuSMV BDD 退化到 SMT 求解甚至超时。
  - **自动安全防线（`_ast_needs_unbounded_integers`）**：本工具**仅在同时满足以下全部条件时**才启用 NuSMV `-128..255` 有限 BDD 域：
    1. 观察器本身不依赖 SMT；
    2. 候选 ST 不包含 `REAL`、`TIME`、`WORD` 或定时/计数器 FB；
    3. 所有 `INT_SUBRANGE` 上下界严格落于 `[-128, 255]` 内；
    4. AST 中所有整数字面量均在 `[-128, 255]` 内；
    5. 声明为 `INT` / `DINT` / `UDINT` / `LINT` 等无界整型的变量**没有任何算术运算赋值**（`+`、`-`、`*`、`/`、`MOD` 或一元负号）。
  - 一旦出现针对无界整型的算术递增/计算或超出 `[-128, 255]` 的常量/子界，验证器**自动升级到 `nuXmv` SMT 无界整数 `integer` 模式**，绝不在不知情的情况下对算术计数做截断而破坏完备性（Soundness）。
  - 在安全启用 BDD 子界模式的前提下，`_guard_subrange_expr` 仍对 `USINT`/`BYTE` 生成 `mod 256` 回绕语义、对有符号/无界小常量变量生成边界钳位，防止候选错误逻辑造成 NuSMV 报 `cannot assign value` 崩溃。
- **典型边界与风险**：
  - 变量位宽大或包含多个大整数/数组时极易发生 **BDD 状态空间爆炸**（`TIMEOUT` 或进程内存耗尽 `TOOL_ERROR`）。
  - **绝对不支持**数学无界 `integer`、`real` 以及位向量 `word` 算术扩展后的无限状态模型（该类模型会自动或强制路由到 `nuXmv`）。

---

### 3.3 第三层：nuXmv（无限状态 SMT / MathSAT + IC3 / SBMC 引擎）能力边界

- **引擎能力**：通过 MathSAT SMT 求解器支持 `integer`、`real`、`unsigned/signed word[N]` 等无限或大位宽状态类型。调用脚本流水线（`_build_nuxmv_smt_script`）依次执行：
  1. `go_msat`（有限模型可额外执行 `build_boolean_model`）；
  2. `check_invar_ic3`：使用基于 SMT 的 IC3/PDR 算法对 `INVARSPEC` 进行无限时域安全性证明或反例生成；
  3. `msat_check_ltlspec_sbmc_inc -k <bmc_bound>`：默认 `k = 25` 步执行增量有界模型检测（SBMC），用于在复杂时序规约上快速发现浅层反例；
  4. `check_ltlspec_ic3`：使用 LTL-to-Invar 构造与 IC3 对所有 `LTLSPEC` 做无限时域归纳证明。
- **多不变量关系型合取求解（Relational Conjunction Solving）**：
  - 工程实测中发现（例如 `PUB006`），多条独立 `INVARSPEC` 单独送入 `check_invar_ic3` 时，因各自缺乏协同关系不变量支撑而容易超时；将多条 `INVARSPEC` 合取为一个复合不变量 `__CONJ_INVAR__` 后，IC3 可共享同一归纳不变量帧并在亚秒级一次证明全部成立。
  - 当首轮 `check_model`（多 `INVARSPEC` SMT 模式下首探上限 3 秒）超时，验证器自动触发 `_run_conjunction_smt_verification`；若合取也失败或仍含未决性质，则拆分回逐条检测，且**严格禁止将超时或未定条目伪造为通过（`holds=True`）**。
- **理论与工程边界**：
  - **不可判定性与 `unknown`**：包含任意无界 `integer`/`real` 算术的无限状态系统模型检测理论上是**半可判定（Semi-decidable）**问题；遇到非线性算术（如 `MOD`、变量乘除法 `/`）或极深时序依赖时，IC3 可能无法收敛并输出 `-- specification ... is unknown`，此时**绝不能等同于通过，也不能等同于反例**。
  - **有界证伪 vs 无限证明**：`msat_check_ltlspec_sbmc_inc -k 25` 若在 25 步内发现反例则属于真反例（哪怕后续 `check_ltlspec_ic3` 对同一条性质返回 `unknown`，`parse_results` 也会结合 SBMC 阶段结果将其正确归为 `COUNTEREXAMPLE`）；反之，SBMC 在 25 步内“未发现反例”**不能证明性质成立**，必须依赖 IC3 明确返回 `is true`。
  - **不支持 `CTLSPEC`**：`nuXmv` SMT 模式仅接受 `INVARSPEC` 与 `LTLSPEC`（传入 `CTLSPEC`/`SPEC` 立即报错拦截）。

---

## 4. 六态严谨返回规范（Rigorous 6-Status Return Taxonomy）

针对“不确定结果或处理不得当”的场景，引擎严格执行**六态分离原则**。**任何基础设施异常、求解器未决或语法超限都绝对不能混同于候选代码正确（`PASS`）或候选代码逻辑错误（`COUNTEREXAMPLE`）**：

| 返回状态 (`status`) | `verified` | `property_pass_ratio` | 严格触发条件 | 下游行为与严谨处理规则 |
| :--- | :---: | :---: | :--- | :--- |
| **`PASS`** | **`True`** | `1.0` | `INITIAL_INSTANCE` 全部满足，期望性质数 `> 0`，且全部性质均被求解器明确证明 `is true`（`failed=0, unknown=0`）。 | 仅此状态代表严格形式化通过；三维棘轮可晋升并结束 CEGAR。 |
| **`COUNTEREXAMPLE`** | **`False`** | 仅当 `unknown == 0` 时为 `passed / total`；若同时存在未决性质则为 `None` | 至少一条 `INITIAL_INSTANCE` 失败，或至少一条性质被明确证伪（`is false`，含 SBMC 有界证伪）。 | 提取反例序列（面向 Agent 自动脱敏为 `{step, inputs, observed}`）并生成 WebUI 反例波形；触发 CEGAR 修复环。 |
| **`INCONCLUSIVE`** | **`False`** | **`None`** | 无性质被证伪，但求解器对至少一条性质输出 `is unknown`（如非线性 SMT 下 IC3 不收敛），或合取拆分核查后仍有条目未定。 | **严禁当作 `PASS` 或计算虚高通过率**；Agent 收到明确 `guidance` 提示改用 `compile_st` / `simulate_st` 交叉验证，STAR Step 3.5 不进入无效 CEGAR。 |
| **`UNSUPPORTED_ST`** | **`False`** | **`None`** | ST 使用了超边界语法（如 `VARIANT`、`WHILE`、条件内调用 `TON`）、静态越界、常量除零，或任务缺少可用的观察器模型。 | 非候选功能错误；`metrics.py` 单独计入 `verification_unsupported_tasks` 而不计入可评估样本分母。 |
| **`TIMEOUT`** | **`False`** | **`None`** | 进程在未产生明确证伪反例前超过 `timeout`（含多 `INVARSPEC` SMT 首探及合取/逐条超时）。 | 保留部分标准输出日志供审计；计为基础设施/复杂度未闭合，不误判为候选故障。 |
| **`TOOL_ERROR`** | **`False`** | **`None`** | 本地缺少 `NuSMV`/`nuXmv`、退出码非 0、输出行出现 `syntax error` / `aborting` / `cannot assign value` / `range error`、检查到的性质总数与预期不一致，或内部解析/编译异常。 | 与真实 CODESYS 规则一致，视为工具链/基础设施故障，绝不计作候选行为结果。 |

### 相关接口与统计口径
- **逐条性质明细 (`property_results`)**：每条包含 `status` 枚举（`"PASS"` / `"FAIL"` / `"UNKNOWN"`）及对应三值布尔 `holds`（`True` / `False` / `None`），顶层同时给出 `unknown_properties` 计数。
- **Agent MCP 响应 (`verify_st`)**：当返回 `UNSUPPORTED_ST`、`INCONCLUSIVE`、`TIMEOUT` 或 `TOOL_ERROR` 时，负载中附加结构化 `guidance` 与 `unknown_property_ids`，防止 Agent 将超边界或求解未决误解读为程序死锁并盲目乱改可编译代码。
- **聚合评测指标 ([metrics.py](../src/plc_agent/metrics.py))**：
  - `verification_evaluated_tasks` 与 `verification_pass_rate_among_evaluated` **仅统计结论明确的 `PASS` 与 `COUNTEREXAMPLE` 任务**；
  - 新增 `verification_inconclusive_tasks` 与 `verification_unsupported_tasks` 独立透明度字段，避免过滤偏差（Selection Bias）。

---

## 5. 相关文件索引

- 转换与耦合验证主引擎：[src/plc_agent/st_verifier.py](../src/plc_agent/st_verifier.py)
- NuSMV / nuXmv 调度与结果解析：[src/plc_agent/model_checker.py](../src/plc_agent/model_checker.py)
- 清单管理与验证入口：[src/plc_agent/formal_verify.py](../src/plc_agent/formal_verify.py)
- MCP 工具接口与预算控制：[src/plc_agent/mcp_server.py](../src/plc_agent/mcp_server.py)
- STAR v2 主控循环（Step 3.5 CEGAR）：[src/plc_agent/harness.py](../src/plc_agent/harness.py)
- 汇总指标计算：[src/plc_agent/metrics.py](../src/plc_agent/metrics.py)
- 单元测试（含三层边界与不确定态回归测试）：[tests/test_st_verifier.py](../tests/test_st_verifier.py)
