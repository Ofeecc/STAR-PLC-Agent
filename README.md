# PLC Structured Text Coding Agent (STAR v2)

This project implements **STAR v2** (Specification-Targeted Agentic Refinement) and an auditable baseline harness for generating, compiling, repairing, and preparing formal-verification materials for IEC 61131-3 Structured Text (ST) in industrial PLC environments (CODESYS). The frozen dataset contains all 20 instructor-supplied public tasks and 12 independently constructed self-built tasks (**32 tasks**, **294 LTL properties**, **276 fixed test cases**, **2,994 scan steps**; `dataset_sha256: b4b9ff871b09d72f0eadb9ea798e181a515a9d23de710877408cda5760aada98`). Every task includes normative specification contracts, discrete scan semantics, formal LTL temporal properties, and fixed expected functional traces.

The implementation strictly separates generated-code compilation, compiler infrastructure failures, and functional/formal verification. Compilation success is accepted only from matching CODESYS rebuild evidence, never a process exit code alone. Independent Python scan contracts (`ScanContract`) validate expected sequences across all 32 tasks; they are distinct from real PLC execution.

The local review and trace WebUI covers all 32 human-reviewed tasks with three focused views (**Dataset & Specs**, **Workflow & Benchmark**, and **Sandbox & Waveform Lab**), defaulting to English with a persistent English/Chinese toggle. Use [English UI](http://127.0.0.1:8765/?lang=en) or [Chinese UI](http://127.0.0.1:8765/?lang=zh) after starting `uv run plc-agent web`. See [docs/README.md](docs/README.md) for active guides, design specs, and archived milestone logs (including [双语审核界面说明](docs/archive/全题库双语审核界面_20261111.md), [模板库与Token配置建议](docs/archive/模板库与Token配置建议_20261111.md), [2026-11-11 更新记录](docs/archive/更新记录_20261111.md), [规约规范化与逐题定义](docs/archive/规约规范化_20261111.md), and [2026-11-12 全量审计汇总](docs/archive/规约与模型全量审计汇总_20261112.md)).

All 32 composite scan predicates use normalized executable transition definitions, segregated input/observed/reference namespaces, explicit comparison policies, and explicit non-Zeno timing premises (`results/summary/specification_normalization_20261112.json`). Human review of all 32 normalized specifications and bilingual review notes is complete (`NORMALIZED_HUMAN_REVIEWED` / `HUMAN_REVIEWED`). The 294 LTL properties and `models/*.smv` reference models (`configs/smv_verification_status.json`) validate reference abstractions — **candidate ST-to-SMV formal verification remains `UNVERIFIED`**, and historical pilot runs retain their original task hashes.

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

Local validation on 2026-11-10: 141 Python tests passed; real compiler smoke passed; SELF001 reference passed 2 cases / 10 steps; a deliberately wrong SELF001 implementation compiled but failed real simulation. See [本机验证与修复记录](docs/archive/本机验证与修复_20261110.md). Real CODESYS runs must execute outside the coding agent's restricted sandbox to avoid APInstaller event-log access errors and Gateway connection failures observed on this machine.

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

- **Workflow & Waveform Inspector WebUI**:
  ```bash
  uv run plc-agent web
  ```
  Launches the minimalist English-default (EN/ZH toggle) WebUI at `http://127.0.0.1:8765`, combining bilingual task & LTL spec exploration, live/replayed 5-stage STAR v2 & baseline workflow telemetry with version diffs, benchmark matrix views, and a same-screen ST compiler/simulation & step-by-step waveform comparator.

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

- **Campaign Status**: `PENDING_REAL_EXECUTION` in [configs/experiments.json](configs/experiments.json). Offline dataset replay, harness fixes, and unit tests are current on Linux; end-to-end Windows + CODESYS paired comparison runs are pending team execution (see [docs/windows_field_test_guide.md](docs/windows_field_test_guide.md)).
- **Experiment Fix Merge (2026-11-14)**: Merged the 2026-11-13 harness and test-engine fixes ([archived handoff note](docs/archive/交接与实测方案_20261113.md)): `final_compile_attempt()` binds `test`, `import-trace`, and metrics to the selected candidate hash on STAR rollbacks; `harness.py` and `baseline.py` isolate infrastructure failures (`TOOL_ERROR`/`TIMEOUT`) cleanly; `/api/evaluate` preserves infrastructure/unverified outcomes without collapsing them to `COMPILE_FAIL`.
- **Historical Two-Task Pilot (2026-11-10)**: Ran under `deepseek-v4.1-flash-1017` on an earlier dataset revision (`PUB001` passed compilation and 2/2 cases, 16 steps; `PUB003` hit `TOOL_ERROR` after SA0027 collision and truncated repair output; 6 requests / 49,908 tokens total). See [raw pilot evidence](results/raw/pilot_pair_2026-11-10T143217961073+0000/) and [updated evidence audit](results/raw/pilot_pair_2026-11-10T143217961073+0000/usage_and_evidence_audit.json). These pilot runs are not a full-dataset campaign or a baseline comparison.
- **Explicit Reference SMV Models**: `models/` contains 66 explicit `.smv` models checked locally with NuSMV/nuXmv (`configs/smv_verification_status.json`). Because automatic candidate ST-to-SMV translation is not implemented, candidate formal verification remains `UNVERIFIED`.
- **Additional Controls & Safeguards**:
  - Historical README figures remain isolated in [docs/historical_readme_results.md](docs/historical_readme_results.md) and require original hash-bound logs before reuse.
  - Current baseline conditions (`E1`/`E2`) default to `custom_tool_loop` (`deepseek_harness`), not `smolagents`; external baseline drivers (`codex_cli`, `claude_code`) require compliant tool-use approvals.
  - `export-verify` produces draft verification bundles, and `random-test` produces oracle-labelled inputs without executing candidate ST.
  - Full CODESYS development/runtime acceptance requires running outside restricted agent sandboxes on Windows (`AGENTS.md`).

## Configuration

### API Credentials

API configuration can be supplied via environment variables, `.env`, or a private settings file (`APIKEY相关.txt` / `PLC_API_CONFIG`):

```bash
export PLC_API_CONFIG="/path/to/private/relay-settings.txt"
# Optional overrides:
export PLC_API_BASE_URL="https://your-relay.example/v1"
export PLC_LLM_API_KEY="your-api-key"
```

Verify connection (requires explicit API budget approval first):

```bash
uv run plc-agent --allow-model-api probe-models --tool-smoke
```

### CODESYS Compiler Integration

Configure machine-specific paths via `uv run plc-agent configure` (writes gitignored `configs/runtime.local.json`) or environment variables — keep tracked `configs/runtime.json` clean of local machine secrets or edits:

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

See [docs/README.md](docs/README.md) for the complete documentation index, [docs/静态分析与模型检查使用指南.md](docs/静态分析与模型检查使用指南.md) for Static Analysis Light / NuSMV/nuXmv workflows, [docs/archive/六题规约中文审核.md](docs/archive/六题规约中文审核.md) for six-task Chinese review notes, and `docs/archive/` for historical milestone records. Reference model checks never establish candidate ST formal verification.

| Directory | Content |
| --- | --- |
| `src/plc_agent/` | STAR v2 core: Planner, Dialect, Coder, Tester, Ratchet, WebUI, CLI, and verification |
| `dataset/public/`, `dataset/self_built/` | 32 frozen structured task definitions (20 public + 12 self-built) with normative contracts |
| `dataset/specifications/catalog.md` | Complete task specifications, interfaces, provenance, and LTL properties |
| `codesys/scripts/`, `codesys/templates/` | CODESYS automation scripting and immutable template project |
| `codesys/examples/` | 16 hand-authored reference ST examples (12 self-built + 4 public tasks), never model benchmark outputs |
| `models/` | 66 explicit `.smv` models and reference/mutant verification files (`EXPLICIT_SMV_MODEL_ONLY`) |
| `configs/` | Nonsecret runtime defaults (`runtime.json`), condition matrix (`experiments.json`), SMV check status |
| `docs/` | Active setup/protocol guides ([docs/README.md](docs/README.md)), design specs (`superpowers/`), archived logs (`archive/`), and frozen per-task review records (`规约逐题审查_20261106/`) |
| `scripts/` | Dataset normalization, validation, Windows preflight (`windows_verify.ps1`), and analysis/packaging helpers |
| `results/raw/`, `results/summary/` | Protocol records, pilot raw logs, dataset/spec validation outputs, and reproducible audits |
| `experiments/` | Runtime-created per-condition workspaces (`E1`–`E4`, `A1`–`A3`, `S1`–`S2`) populated when `plc-agent run` executes |
| `report/`, `presentation/`, `video/` | Final deliverable templates and static assets (experiment results pending full campaign) |
| `submission/` | Audited submission packaging templates and manifests |
