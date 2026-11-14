# STAR-PLC-Agent Windows + CODESYS 实测操作指南

> 本指南专为持有 Windows 物理机并安装有 CODESYS 环境的组员编写。  
> 按照本手册指引，您可以在 10 分钟内完成环境自检、真实 CODESYS 编译器冒烟验证、离线参考模型仿真、启动可视化 Web 看板，并执行全自动的 Agent 评测实验。

---

## 一、 实测机环境要求

1. **操作系统**：Windows 10 / Windows 11 (64位)
2. **Python 环境**：Python 3.10 或更高版本（强烈推荐安装并使用现代化包管理器 [`uv`](https://docs.astral.sh/uv/)）
3. **CODESYS 软件**：
   - CODESYS Development System V3.5（例如 SP17 / SP18 / SP19 / SP20 / SP21 / SP22 均可）
   - 安装时包含 **CODESYS Scripting**（系统标准安装已默认包含 IronPython 2.7 脚本引擎）
4. **Git**：用于克隆和拉取最新版本代码

---

## 二、 5分钟极速上手 (Quickstart)

### 步骤 1：拉取代码并安装依赖
在 Windows 终端（PowerShell 或 CMD）中执行：
```powershell
# 1. 克隆代码仓库
git clone https://github.com/Ofeecc/STAR-PLC-Agent.git
cd STAR-PLC-Agent

# 2. 安装并同步 Python 虚拟环境 (uv 会自动构建极速隔离环境)
uv sync
```
*(注：如果未安装 `uv`，可执行 `pip install uv`，或使用系统 Python：`python -m venv .venv` 然后激活虚拟环境安装)*

---

### 步骤 2：一键实测自检 (零 API 额度消耗)
我们专门为您制作了自动化实测体检脚本，会自动探测 CODESYS 路径、验证编译器连通性、并完成一次真实的离线仿真：
```powershell
powershell -ExecutionPolicy Bypass -File scripts\windows_verify.ps1
```

该脚本将自动执行以下 5 项检测：
1. **Python / uv 环境检测**：确认解释器与必要依赖包正常。
2. **CODESYS 路径自动探测**：自动检索 `C:\Program Files` 与 `D:\` 盘下的 `CODESYS.exe` 与匹配的 `.profile`。
3. **系统体检 (`doctor`)**：输出软硬件与依赖就绪报告。
4. **真实编译器冒烟验证 (`compiler-smoke`)**：调用真实 CODESYS 后台编译 Valid、Invalid、Repaired 三段 ST 代码，验证 ScriptEngine 与错误捕获机制。
5. **离线参考仿真验证 (`test-reference`)**：使用题库中的参考实现对 `SELF001` 进行离线逐拍仿真，验证真实仿真环境。

> [!TIP]
> **只要上述脚本输出绿色 `[SUCCESS]`，即证明您的 Windows + CODESYS 机器完全具备实测能力！**

---

## 三、 配置与手动微调 (可选)

如果您的 CODESYS 安装在非标准路径，或需要手动指定 Profile，可以使用内置配置命令：

```powershell
# 自动探测并保存到 configs/runtime.local.json
uv run plc-agent configure

# 或手动指定可执行文件路径与 Profile 字符串
uv run plc-agent configure --codesys-exe "C:\Program Files\CODESYS 3.5 SP19\CODESYS\Common\CODESYS.exe" --profile "CODESYS V3.5 SP19 Patch 2"
```

### 模型 API 凭据配置 (实测 Agent 时使用)
如需执行包含大模型调用的 Agent 实验，只需在项目根目录下创建 `.env` 文件（或设置环境变量）：
```ini
# .env 文件内容
PLC_LLM_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PLC_API_BASE_URL=https://api.deepseek.com/v1
```
*(系统同样兼容从根目录的 `APIKEY相关.txt` 中自动提取密钥)*

---

## 四、 离线与仿真验证 (无需消耗模型 API)

在进行耗费 token 的大模型测试前，先在普通 Windows PowerShell（非受限沙盒）验证环境、编译器冒烟与参考 ST 在本地 CODESYS 下的表现，并为每次验收建立独立输出目录以保留原始诊断、`simulation_evidence.json` 和 `trace.json`：

```powershell
git rev-parse HEAD
uv sync
uv run plc-agent validate-dataset
uv run plc-agent compiler-smoke   # 预期按顺序返回 PASS -> COMPILE_FAIL -> PASS

$run = "results/raw/reference-$(Get-Date -Format yyyyMMdd-HHmmss)"
# 1. 验证基本联锁与编译/采样/评分全链路 (SELF001: 7 组用例, 39 拍)
uv run plc-agent test-reference --task-id SELF001 --backend codesys --out-dir "$run/SELF001"

# 2. 验证连续扫描计数与动态预置 (SELF008: 7 组用例, 45 拍)
uv run plc-agent test-reference --task-id SELF008 --backend codesys --out-dir "$run/SELF008"

# 3. 复杂数据结构参考校验 (可选，如 PUB017 配方 CRUD 管理器)
uv run plc-agent test-reference --task-id PUB017 --backend codesys --out-dir "$run/PUB017"
```

> [!NOTE]
> - 建议先回收 `SELF001` 与 `SELF008` 的完整证据，再按需选择性复跑 `PUB006`（`BenchElapsed` 已从包装器移除，需结合实际周期评估毫秒定时用例的采样覆盖）。
> - **关于 `PUB018`**：当前 `codesys/examples/PUB018.json` 已包含头尾索引与回绕计算，但 `buffer` 写入与 `item` 出队赋值尚未补全，且泛型绑定与目标 CODESYS 版本的兼容性待验证；首轮实测与对比请优先选用可稳定完成采样的任务。

---

## 五、 真实 Agent 对比实验流程 (Benchmark Experiments)

> [!CAUTION]
> 教师中继 API 额度有限。**每次执行消耗真实模型 API 的命令（`probe-models`、`run`）前，必须先获得团队/用户明确批准**；`--allow-model-api` 仅用于记录已获批准，不能替代事先确认。

当 CODESYS 与 API 环境均就绪后，按以下步骤进行预检、成对试跑与全量实验。

### 1. 运行前预检与预算对齐
1. **核对 `campaign.json` 与 `model_capabilities.json`**：
   - 当前冻结题库哈希为 `b4b9ff871b09d72f0eadb9ea798e181a515a9d23de710877408cda5760aada98`（已完成全部 32 题人工审阅）。若本机 `results/summary/campaign.json` 为旧题库残留，先归档旧批次再执行 `uv run plc-agent prepare`。
   - `plc-agent run` 会读取本地 `results/summary/model_capabilities.json`（未随主线提交）。若缺失且本机无已有记录，在获 API 授权后先执行探针（将对已配置模型发起工具冒烟请求）：
     ```powershell
     uv run plc-agent --allow-model-api probe-models --tool-smoke
     ```
2. **明确生效预算口径（成对对比前固定并记录）**：
   - `configs/experiments.json` 中记录了条件元数据 `compiler: 3`、`timeout: 900`、`max_llm_calls: 30`；
   - `plc-agent run` 实际使用共享 `Settings`（`configs/runtime.json` 及代码默认值）：`max_repairs: 2`（即首编 + 最多 2 次修复，共 3 次编译）、`compiler_timeout: 180`、`llm_timeout: 420`、`task_timeout: 2400`、`reasoning_effort: "medium"`、角色输出上限（`planner=16384`、`coder=24576`、`repair=32768`、`tester=24576`）、`context_window_tokens=131072`、`max_total_tokens=300000`，以及 `Settings` 默认 `max_llm_calls=9`。
   - 成对运行前请确认并在实验记录中注明实际生效上限；若使用外部 CLI（如 `codex_cli`、`claude_code`），需额外说明其无法统一强制相同的单响应 token 上限。

### 2. 先做两题同模型成对预检（推荐全量前执行）
推荐优先选用 **`SELF001`**（基本联锁，先校准编译器与采样后端）和 **`PUB002`**（32 位输入历史/最高位/掩码，7 组 39 拍，无物理计时抖动依赖）。先运行内部同模型对照（STAR v2 `E3` vs `E1/deepseek_harness`），验证生成、编译、`test` 固定用例评测与 token 审计全链路：

```powershell
uv run plc-agent prepare

# 第一题：SELF001（共 4 条命令，两条 run 各自消耗 API 额度）
uv run plc-agent --allow-model-api run --condition E3 --task-id SELF001
uv run plc-agent test --condition E3 --task-id SELF001
uv run plc-agent --allow-model-api run --condition E1 --driver deepseek_harness --task-id SELF001
uv run plc-agent test --condition E1 --task-id SELF001

# 第二题：将 --task-id SELF001 替换为 --task-id PUB002 重复上述四步
```

- 课程说明要求选用**已有 Agent 框架**作为外部基线。若本机已合法配置 `codex` 或 `claude` 且工具调用审批策略可用（禁止绕过策略限制），可通过 `--driver codex_cli` 或 `--driver claude_code` 运行同题外部基线对比；若外部模型与 STAR 不同，需在结果表中分别注明各自模型。
- 统计请求次数与 token 时，请以工作区 `model_calls.jsonl` 中的 `request_started` 与响应返回 `usage` 为准（包含失败或截断响应已报告的用量；未返回则标为缺失）。

### 3. 标准实验条件矩阵 (`configs/experiments.json`)
`configs/experiments.json` 当前预置了以下 9 个条件（`selection_status` 当前为 `PENDING_REAL_EXECUTION`）：

| 条件代号 | 框架 (`framework` / `driver`) | 模型 (`model`) | 核心差异 / 用途 |
| :--- | :--- | :--- | :--- |
| `E1` | `custom_tool_loop` (`deepseek_harness`) | `deepseek-v4.1-flash-1017` | DeepSeek 路由对照组（可加 `--driver codex_cli`/`claude_code` 接外部基线） |
| `E2` | `custom_tool_loop` (`deepseek_harness`) | `kimi-k3.1-pro` | Kimi 路由对照组（`spec_visible: true`） |
| **`E3`** | **`self_harness` (STAR v2 完整方案)** | **`deepseek-v4.1-flash-1017`** | **Planner + CODESYS 方言 + 自测反馈单调棘轮（主力实验）** |
| **`E4`** | **`self_harness` (STAR v2 完整方案)** | **`kimi-k3.1-pro`** | **STAR v2 跨模型验证组（Kimi 路由）** |
| `A1` | `self_harness` (`ablation: no_planner`) | `deepseek-v4.1-flash-1017` | 消融实验：关闭 Planner 结构化规范阶段 |
| `A2` | `self_harness` (`ablation: no_dialect`) | `deepseek-v4.1-flash-1017` | 消融实验：关闭 CODESYS 方言适配器提示 |
| `A3` | `self_harness` (`ablation: no_selftest`) | `deepseek-v4.1-flash-1017` | 消融实验：关闭 ScanContract 微分自测反馈 |
| `S1` | `self_harness` (`spec_visible: false`) | `deepseek-v4.1-flash-1017` | 规约可见性对照：隐藏规范化规约（STAR v2） |
| `S2` | `custom_tool_loop` (`deepseek_harness`, `spec_visible: false`) | `deepseek-v4.1-flash-1017` | 规约可见性对照：隐藏规范化规约（对照组） |

### 4. 批量运行、断点续跑与评测结算
```powershell
# 1. 运行指定条件（已完成的非 NOT_RUN 任务默认跳过；强制重跑加 --rerun）
uv run plc-agent --allow-model-api run --condition E3
uv run plc-agent --allow-model-api run --condition E1

# 2. 对已生成候选执行真实 CODESYS 固定用例仿真测试
uv run plc-agent test --condition E3
uv run plc-agent test --condition E1

# 3. 聚合生成汇总与审计记录 (results/summary/)
uv run plc-agent aggregate

# 4. 可选：运行配对 McNemar 检验与 Bootstrap 置信区间统计脚本
uv run python scripts/analyze_results.py
```

---

## 六、 启动 WebUI 自动化测试与波形比对平台

实测过程中或测试完成后，可随时启动可视化前端，直观查看代码与时序波形：

```powershell
uv run plc-agent web --port 8765
```
启动后在 Windows 浏览器中打开：**`http://127.0.0.1:8765`**

### 核心功能区（极简白底黑字视图，默认英文并支持右上角实时切换中文）：
1. **数据集与规约 (`Dataset & Specs`)**：浏览已完成人工审阅的 32 题接口契约、双语符号词表、高亮 LTL 公式浮窗与固定/随机扫描测试。
2. **动态工作流与评测看板 (`Workflow & Benchmark`)**：支持对 `experiments/` 实时运行记录 2 秒自动轮询跟踪及历史试跑回放（STAR v2 五阶段与基线工具循环），查看阶段细节、候选源码行级 Diff、调用时间线、落盘真实仿真波形及实验条件矩阵。
3. **编译仿真与波形实验台 (`Sandbox & Waveform Lab`)**：同屏集成 ST 源码编辑（一键载入骨架、人工参考 ST 或轨迹候选）、CODESYS 编译诊断、NuSMV 包导出与逐周期输入/预期/实测信号偏差波形对比。

---

## 七、 Windows 常见问题排错手册 (FAQ)

### Q1：运行 `windows_verify.ps1` 提示 `无法加载文件，因为在此系统上禁止运行脚本`？
- **原因**：Windows PowerShell 默认执行策略限制。
- **解决**：在 PowerShell 窗口执行一次临时提权命令：
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
  然后再重新执行脚本。

### Q2：`doctor` 提示 `Missing compiler configuration: codesys_exe`？
- **原因**：CODESYS 安装在自定义盘符，或安装目录名称不标准。
- **解决**：打开文件资源管理器找到 `CODESYS.exe`（通常位于 `<安装目录>\Common\CODESYS.exe`），然后运行：
  ```powershell
  uv run plc-agent configure --codesys-exe "你的实际路径\CODESYS.exe"
  ```

### Q3：提示 Profile 不匹配 `The profile '...' is not installed`？
- **原因**：配置的 Profile 字符串与实测机安装的 Profile 文件名不完全一致。
- **解决**：
  1. 打开资源管理器，进入 `CODESYS.exe` 同级的 `../Profiles/` 目录。
  2. 观察目录下的 `.profile` 文件，例如 `CODESYS V3.5 SP19 Patch 2.profile`。
  3. 执行配置命令，将 Profile 名设置为去除 `.profile` 后缀的名称：
     ```powershell
     uv run plc-agent configure --profile "CODESYS V3.5 SP19 Patch 2"
     ```

### Q4：CODESYS 运行一直卡住无反应（180 秒超时）？
- **原因**：首次安装的 CODESYS 在无头启动时可能弹出过系统模态对话框（如“网络防火墙访问”、“更新通知”、“第三方插件许可”等），在后台等待用户点击。
- **解决**：
  1. 在桌面双击手动打开一次 `CODESYS.exe`。
  2. 点击菜单 `文件` -> `打开工程`，打开本项目中的 `codesys/templates/benchmark.project`。
  3. 观察是否有任何弹窗，全部点击确定或勾选“不再提示”，然后关闭 CODESYS。
  4. 重新运行 `uv run plc-agent compiler-smoke` 即可畅通。

### Q5：中文路径或用户名是否会导致 IronPython 报错？
- **系统保障**：我们的底层实现了 **ASCII Staging 自动暂存区机制**。无论您的仓库处于哪个含有中文或空格的文件夹下，编译与仿真任务都会自动在系统根目录的 `C:\plc_work\` 纯 ASCII 安全沙盒中无损执行，彻底杜绝 IronPython 2.7 的编码崩溃隐患。

### Q6：测试时遇到网络防火墙或代理中断？
- **解决**：
  若您使用了网络代理软件，请在终端中显式指定代理环境变量：
  ```powershell
  $env:HTTP_PROXY="http://127.0.0.1:7890"
  $env:HTTPS_PROXY="http://127.0.0.1:7890"
  ```
  或者在 `.env` 中直接配置国内直连的 API 中继地址。

---

> [!NOTE]
> 实测过程中如有任何异常日志，请将 `results/raw/` 下对应的任务目录（或命令行报错截图）反馈给团队，系统生成的详细 `request.json`、`stdout.log` 和 `codesys_evidence.json` 可准确定位问题根源。
