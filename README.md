# PLC Structured Text Coding Agent (STAR v2)

This project implements **STAR v2** (Specification-Targeted Agentic Refinement) and an auditable baseline for generating, compiling, repairing, and preparing formal-verification materials for IEC 61131-3 Structured Text (ST) for industrial PLC environments (CODESYS). The dataset contains all 20 supplied public questions and 12 independently constructed questions (32 tasks total). Every task includes normative specification contracts, scan semantics, formal LTL temporal properties, and fixed expected functional traces.

The implementation strictly separates generated-code compilation, compiler infrastructure failures, and functional/formal verification. Compilation success is accepted only from matching CODESYS rebuild evidence, never a process exit code alone. Independent Python scan contracts (`ScanContract`) validate expected sequences across all 32 tasks; they are distinct from real PLC execution.

The local review UI now covers all 32 tasks with Chinese review notes, 244 property explanations and a persistent Chinese/English switch. Use [Chinese review](http://127.0.0.1:8765/?scope=all&lang=zh) or [English presentation](http://127.0.0.1:8765/?scope=all&lang=en) after starting the web server. See [双语审核界面说明](docs/全题库双语审核界面_20261111.md) and [模板库检查与角色token配置](docs/模板库与Token配置建议_20261111.md). Review translations do not modify benchmark inputs or constitute human approval.

Latest changes and their validation scope: [2026-11-11 更新记录](docs/更新记录_20261111.md). The latest local Python suite passed 158 tests, and browser checks covered all 32 tasks and 244 properties in both languages.

## STAR v2 Architecture

STAR v2 organizes the synthesis and repair loop into five decoupled, auditable phases:

$$\text{Planner} \longrightarrow \text{Dialect} \longrightarrow \text{Coder} \longrightarrow \text{Tester} \longrightarrow \text{Ratchet}$$

1. **Planner**: Receives the existing task requirements, interface, scan semantics and visible specifications, then produces an architecture plan for code generation.
2. **Dialect Adapter**: Enforces IEC 61131-3 strict syntax rules, type mappings (`TON`, `TOF`, `VARIANT`, arrays, enums, structs), and vendor-specific profile compatibility without silent type conversions.
3. **Coder**: Generates clean Structured Text (`FUNCTION_BLOCK FB_Task`) cleanly segregated into interface declarations, implementation body, and supporting objects (DUTs/POUs).
4. **Tester (Differential Self-Test)**: Differential testing against independent finite-state scan oracles (`ScanContract`), randomized seed-deterministic trace generation, and bounded execution monitors after successful compilation.
5. **Ratchet**: Tracks candidate hashes and passed test counts, detects unchanged repairs, retains the best tested candidate within the current self-test set, and enforces iteration budgets.

## OS-Agnostic Environment Management with `uv`

The Python agent logic can run across operating systems; real CODESYS execution requires Windows and local configuration. ASCII path staging is fully automated by the runtime engine (`stage_ascii_workspace` transparently mirrors non-ASCII paths to clean ASCII staging targets for compiler tool safety).

Initialize and synchronize the environment:

```bash
# Create isolated virtual environment
uv venv

# Synchronize all pinned dependencies
uv sync
```

Run test suite:

```bash
uv run --no-sync python -m unittest discover -s tests -v
```

## Windows + CODESYS Field Testing Guide

Local validation on 2026-11-10: 141 Python tests passed; real compiler smoke passed; SELF001 reference passed 2 cases / 10 steps; a deliberately wrong SELF001 implementation compiled but failed real simulation. See [本机验证与修复记录](docs/本机验证与修复_20261110.md). Real CODESYS runs must execute outside the coding agent's restricted sandbox to avoid APInstaller event-log access errors and Gateway connection failures observed on this machine.

For teammates conducting physical machine tests on Windows with CODESYS installed:
- 📖 **Comprehensive Step-by-Step Guide**: [docs/windows_field_test_guide.md](docs/windows_field_test_guide.md)
- 🚀 **One-Click Preflight & Offline Verification**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts\windows_verify.ps1
  ```
  Automatically detects CODESYS paths, runs compiler smoke tests, and executes offline simulation verification with **0 API token cost**.

## Quick Start CLI Workflows

All operational tasks are unified under the `plc-agent` CLI:

- **Preflight Environment Check**:
  ```bash
  uv run plc-agent doctor
  ```
  Validates Python version (>=3.11), required dependencies, compiler paths, and API readiness.

- **Auto-Test Workbench & Waveform Inspector WebUI**:
  ```bash
  uv run plc-agent web
  ```
  Launches the interactive WebUI workbench at `http://127.0.0.1:8765` featuring real-time oscilloscope waveform inspection, multi-pass candidate diffing, and single-click differential test execution.

- **Seed-Deterministic Differential Random Testing**:
  ```bash
  uv run plc-agent random-test --task-id SELF001
  ```
  Generates seed-deterministic randomized scan sequences across boundary conditions and validates against `ScanContract`.

- **Run STAR v2 Agent**:
  ```bash
  uv run plc-agent --allow-model-api run --condition E3 --task-id SELF001
  ```
  Executes the STAR v2 agent on the specified task under experimental condition E3.

- **Run Baseline Agent**:
  ```bash
  uv run plc-agent --allow-model-api run --condition E1 --driver deepseek_harness --task-id SELF001
  ```
  Executes the comparative baseline agent with identical model parameters and compiler budget.

- **Execute Test Evaluation**:
  ```bash
  uv run plc-agent test --condition E3
  ```
  Runs batch functional simulation against fixed test cases and collects actual trace arrays.

- **Compute Statistical Metrics & Bootstrap CIs**:
  ```bash
  uv run plc-agent aggregate
  ```
  Aggregates campaign records, computes compilation rates, functional pass rates, bootstrap confidence intervals, and McNemar exact p-values.

- **Export Formal Verification Bundle**:
  ```bash
  uv run plc-agent export-verify --task-id SELF001
  ```
  Exports formal verification bundles including Structured Text source, LTL temporal specifications (`spec.ltl`), and tool configurations for model checkers (nuXmv, UPPAAL, CBMC).

## Current execution status

STAR v2 is under local validation. The latest two-task STAR pilot used `deepseek-v4.1-flash-1017` with high reasoning: PUB001 passed real CODESYS compilation and all 2 fixed cases / 16 steps; PUB003 ended with TOOL_ERROR after an SA0027 interface-name collision and an incomplete repair response, with functional testing NOT_RUN. The batch used 6 requests / 49,908 tokens including the failed response. See [raw pilot evidence](results/raw/pilot_pair_2026-11-10T143217961073+0000/) and [updated evidence audit](results/raw/pilot_pair_2026-11-10T143217961073+0000/usage_and_evidence_audit.json). These are two pilot tasks, not a full-dataset campaign or a baseline comparison.

A variable-level SA0027 exception compiled a retained PUB003 candidate in a separate probe while another static-analysis rule remained active. This exception is not yet integrated into the agent path. New role-specific output limits and cumulative token accounting have local tests but have not been tried against the paid API. All 32 Chinese review records remain pending human review.

Historical README figures are retained in `docs/historical_readme_results.md` and require original hash-bound logs before reuse.
The current baseline implementation is a custom tool loop, not smolagents. An established external-agent comparison remains pending.
Verification export provides draft ST/property materials, not executable models or a completed formal proof.
The local NuSMV entry point checks supplied SMV models; the included hand-written PUB001 reference is separate from generated ST. Automatic candidate ST-to-SMV translation remains pending, so candidate formal verification remains UNVERIFIED.
`random-test` generates oracle-labelled inputs; it does not execute candidate ST.
CODESYS development/runtime integration requires Windows and local compiler/simulator acceptance.

## Configuration

### API Credentials

API configuration can be supplied via environment variables or a private settings file:

```bash
export PLC_API_CONFIG="/path/to/private/relay-settings.txt"
# Optional overrides:
export PLC_API_BASE_URL="https://your-relay.example/v1"
export PLC_LLM_API_KEY="your-api-key"
```

Verify connection:

```bash
uv run plc-agent probe-models --tool-smoke
```

### CODESYS Compiler Integration

Configure compiler paths in `configs/runtime.json` or via environment variables:

```bash
export PLC_CODESYS_EXE="/path/to/CODESYS/Common/CODESYS.exe"
export PLC_CODESYS_PROFILE="CODESYS V3.5 SP22 Patch 4"
export PLC_CODESYS_TEMPLATE="codesys/templates/benchmark.project"
```

Run compiler verification:

```bash
uv run plc-agent compiler-smoke
```

## Directory Structure

本机新增六题规约中文说明与括号高亮，以及本地 NuSMV SMV 检查入口。手动设置 Static Analysis Light 和检查器覆盖范围见 [静态分析与模型检查使用指南](docs/静态分析与模型检查使用指南.md)，逐条审核材料见 [六题规约中文审核](docs/六题规约中文审核.md)。参考模型的检查结果不代表 Agent 生成 ST 已通过形式验证。

| Directory | Content |
| --- | --- |
| `src/plc_agent/` | STAR v2 core: Planner, Dialect, Coder, Tester, Ratchet, WebUI, CLI, and verification |
| `dataset/public/`, `dataset/self_built/` | 32 frozen structured task definitions with normative contracts |
| `dataset/specifications/catalog.md` | Complete task specifications, interfaces, provenance, and LTL properties |
| `codesys/scripts/`, `codesys/templates/` | CODESYS automation scripting and immutable template project |
| `codesys/examples/` | 16 hand-authored reference ST examples (12 self-built + 4 public tasks covering timed & IN_OUT composite contracts), never model benchmark outputs |
| `configs/` | Nonsecret runtime configuration and experimental condition definitions |
| `experiments/E1` through `E4` | Isolated task/run workspaces, model outputs, compiler logs, and diagnostics |
| `results/raw/`, `results/summary/` | Protocol records, raw logs, reproducible metric summaries, and audits |
| `report/`, `presentation/`, `video/` | 12-page report, presentation deck, speaker notes, and video materials |
| `submission/` | Audited submission package and manifests |
