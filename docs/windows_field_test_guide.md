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

在进行耗费 token 的大模型测试前，建议先验证题库参考代码在本地 CODESYS 下的表现：

```powershell
# 1. 验证简单任务 (SELF001: 安全门双按键启停)
uv run plc-agent test-reference --task SELF001

# 2. 验证时序控制任务 (SELF005: 交通灯定时步进控制)
uv run plc-agent test-reference --task SELF005

# 3. 验证复杂数据结构任务 (PUB017: 配方 CRUD 管理器)
uv run plc-agent test-reference --task PUB017
```

---

## 五、 真实 Agent 对比实验流程 (Benchmark Experiments)

当环境准备就绪后，即可执行完整的基准测评与消融实验。

### 1. 单任务端到端试跑 (Smoke Run)
推荐先选择 1 个任务验证 Agent 生成 -> CODESYS 编译 -> 失败反馈 -> 自测修正全链路：
```powershell
uv run plc-agent --allow-model-api run --condition E3 --task-id SELF001
```

### 2. 核心对比实验条件说明
在 `configs/experiments.json` 中已预置所有标准实验矩阵：

| 条件代号 | 实验名称 | 架构配置说明 |
| :--- | :--- | :--- |
| **`E3`** | **STAR v2 (自研完整方案)** | **Planner + CODESYS 方言卡片 + 自测反馈单调棘轮 (推荐主力测试)** |
| `E1` | DeepSeek-V3 Zero-Shot | 零样本直接生成，不含反馈修复循环 (基线) |
| `E2` | Few-Shot Static Prompt | 增加静态示例，无动态自测反馈 |
| `E4` | Claude-3.5-Sonnet / Codex | 高性能通用代码大模型基线 (需对应 API 权限) |
| `A1` | 消融实验：无 Planner | 去除状态机与变量规划，直接由 Coder 编写 ST |
| `A2` | 消融实验：无方言卡片 | 去除 CODESYS 专用语法与定时器规范提示 |
| `A3` | 消融实验：无自测反馈 | 去除测试用例反例引导，仅依赖编译器错误反馈 |

### 3. 批量运行与断点续跑
```powershell
# 运行完整 E3 方案评测集
uv run plc-agent --allow-model-api run --condition E3

# 运行基线 E1
uv run plc-agent --allow-model-api run --condition E1

# 若中途异常退出，再次执行同一命令即可自动从断点续跑（无需 --rerun 参数）
```

### 4. 评测结算与报表生成
实验运行完毕后，执行以下命令进行自动化功能评测并导出科研统计报表：
```powershell
# 1. 运行所有生成候选代码的真实 CODESYS 仿真测试
uv run plc-agent test --condition E3

# 2. 聚合生成总表与审计记录
uv run plc-agent aggregate

# 3. 运行配对 McNemar 检验与 Bootstrap 置信区间统计，生成论文级 LaTeX 表格
python scripts/analyze_results.py
```
统计报表将输出至 `results/summary/` 与 `report/` 目录下。

---

## 六、 启动 WebUI 自动化测试与波形比对平台

实测过程中或测试完成后，可随时启动可视化前端，直观查看代码与时序波形：

```powershell
uv run plc-agent web --port 8765
```
启动后在 Windows 浏览器中打开：**`http://127.0.0.1:8765`**

### 核心功能区：
1. **题库规约审查 (Dataset Explorer)**：查看 20 道公开题 + 12 道自建题的接口变量与 LTL 语义。
2. **时序波形比对 (Waveform Comparator)**：直观对比期望输出与 CODESYS 仿真实际输出的逻辑电平波形，自动红标首次分歧拍（`first_bad_step`）。
3. **Agent 决策链回放 (Trace Playback)**：查看大模型在各个修复轮次中的思考、编译报错诊断与候选代码收敛过程。
4. **沙盒实时试跑 (Sandbox Verifier)**：在网页端直接修改 ST 代码并一键提交后台 CODESYS 编译与仿真。

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
