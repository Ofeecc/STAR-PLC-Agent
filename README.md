# PLC Structured Text Coding Agent (STAR v2)

This project implements **STAR v2** (Specification-Targeted Agentic Refinement) and an auditable baseline for generating, compiling, repairing, and formally verifying IEC 61131-3 Structured Text (ST) for industrial PLC environments (CODESYS). The dataset contains all 20 supplied public questions and 12 independently constructed questions (32 tasks total). Every task includes normative specification contracts, scan semantics, formal LTL temporal properties, and fixed expected functional traces.

The implementation strictly separates generated-code compilation, compiler infrastructure failures, and functional/formal verification. Compilation success is accepted only from matching CODESYS rebuild evidence, never a process exit code alone. Independent Python scan contracts (`ScanContract`) validate expected sequences across all 32 tasks; they are distinct from real PLC execution.

## STAR v2 Architecture

STAR v2 organizes the synthesis and repair loop into five decoupled, auditable phases:

$$\text{Planner} \longrightarrow \text{Dialect} \longrightarrow \text{Coder} \longrightarrow \text{Tester} \longrightarrow \text{Ratchet}$$

1. **Planner (`normative_completion`)**: Ingests natural-language requirements, interface definitions, initial states, scan semantics, and temporal specifications. Synthesizes a deterministic scan-by-scan input-output contract and state transition system.
2. **Dialect Adapter**: Enforces IEC 61131-3 strict syntax rules, type mappings (`TON`, `TOF`, `VARIANT`, arrays, enums, structs), and vendor-specific profile compatibility without silent type conversions.
3. **Coder**: Generates clean Structured Text (`FUNCTION_BLOCK FB_Task`) cleanly segregated into interface declarations, implementation body, and supporting objects (DUTs/POUs).
4. **Tester (Differential Self-Test)**: Differential testing against independent finite-state scan oracles (`ScanContract`), randomized seed-deterministic trace generation, and bounded execution monitors before expensive compiler invocation.
5. **Ratchet (Lexicographical Monotonic Ratchet)**: Tracks candidate hashes, diagnostic error severities, and passed test counts. Rejects stagnating repairs, prevents regressions, and enforces strict iteration budgets.

## OS-Agnostic Environment Management with `uv`

The project is fully OS-agnostic and runs across Linux, macOS, and Windows without platform-specific scripts or host-specific drive letters (`C:\`, `D:\`). ASCII path staging is fully automated by the runtime engine (`stage_ascii_workspace` transparently mirrors non-ASCII paths to clean ASCII staging targets for compiler tool safety).

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
  uv run plc-agent run --condition E3 --task-id SELF001
  ```
  Executes the STAR v2 agent on the specified task under experimental condition E3.

- **Run Baseline Agent**:
  ```bash
  uv run plc-agent run --condition E1 --driver deepseek_harness --task-id SELF001
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

## Current Evidence & Campaign Outcomes

Use the timestamped records in `results/summary/` as the authority. Real CODESYS preflight produced 0, 2 and 0 compiler errors for valid, deliberately invalid and repaired programs. Both selected models have generated and compiled code across all conditions:

| Condition | Framework | Model ID | First compilation | Final compilation | Actual cases passed/evaluated | Case coverage |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| E1 | smolagents 1.26.0 ToolCallingAgent | deepseek-v4.1-flash | 27/32 | 29/32 | 42/45 | 45/81 |
| E2 | smolagents 1.26.0 ToolCallingAgent | kimi-k3.1-pro | 27/32 | 27/32 | 46/48 | 48/81 |
| E3 | STAR v2 harness | deepseek-v4.1-flash | 26/32 | 26/32 | 38/38 | 38/81 |
| E4 | STAR v2 harness | kimi-k3.1-pro | 30/32 | 31/32 | 50/52 | 52/81 |

Full analysis is available in [results/analysis/summary.md](results/analysis/summary.md). Final artifacts include the [English report](report/report.pdf), [editable slide deck](presentation/slides.pptx), [speaker notes](presentation/speaker_notes.md), [defense Q&A](presentation/defense_qa.md), and [explanation video](video/explanation.mp4).

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
