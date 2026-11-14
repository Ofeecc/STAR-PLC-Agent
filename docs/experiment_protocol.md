# Four-Condition Experiment Protocol (STAR)

> **Current Protocol Note (2026-11-14 Sync)**
> - The sections below preserve the original four-condition (`E1`–`E4`, `smolagents`) design draft. Authoritative current run definitions and execution status live in [`configs/experiments.json`](../configs/experiments.json) (`selection_status: PENDING_REAL_EXECUTION`) and [`configs/runtime.json`](../configs/runtime.json).
> - **Current conditions (`configs/experiments.json`)**: `E1`/`E2` default to `custom_tool_loop` (`driver: "deepseek_harness"` on `deepseek-v4.1-flash-1017` / `kimi-k3.1-pro`; external CLIs require explicit `--driver codex_cli` or `--driver claude_code`); `E3`/`E4` run `self_harness` (STAR); `A1`–`A3` run ablations (`no_planner`, `no_dialect`, `no_selftest`); `S1`–`S2` toggle `spec_visible: false`.
> - **Budget alignment**: `configs/experiments.json` lists condition metadata `compiler: 3`, `timeout: 900`, `max_llm_calls: 30`, while `plc-agent run` passes shared `Settings` (`configs/runtime.json` defaults: `max_repairs: 2` / 3 compiler attempts, `compiler_timeout: 180`, `llm_timeout: 420`, `task_timeout: 2400`, `reasoning_effort: "medium"`, role output caps `16384`/`24576`/`32768`/`24576`, `context_window_tokens: 131072`, `max_total_tokens: 300000`, `max_llm_calls: 9`). Freeze and log the active budget before paired comparisons.
> - **Current frozen dataset (`normalized-20261114`, Human Reviewed)**: 32 tasks, 294 LTL properties, 276 fixed test cases, 2,994 scan steps (`dataset_sha256: d305f96c2faaa87f60a24be90c00ad0b32153492e741b87547d132c591e0e9ee`, status `NORMALIZED_HUMAN_REVIEWED` / `HUMAN_REVIEWED`). See [windows_field_test_guide.md](windows_field_test_guide.md) for current Windows preflight and paired run instructions.

## Objective and Frozen Units

The benchmark evaluates the synthesis of industrial CODESYS Structured Text (ST) by comparing the **STAR** architecture against comparative baselines using the same relay model routes (`deepseek-v4.1-flash` and `kimi-k3.1-pro`). Compilation, functional behavior, execution time, and reported resource consumption are strictly segregated.

The unit of evaluation is one task under one condition. The frozen dataset contains all 20 instructor public tasks and 12 self-built tasks (32 tasks total). The public `requirements` values remain verbatim; explicitly recorded normative assumptions resolve ambiguous behavior. Each condition covers all 32 tasks, totaling 128 planned runs:

| Condition | Framework | Model ID | Description |
| --- | --- | --- | --- |
| E1 | smolagents 1.26.0 ToolCallingAgent | deepseek-v4.1-flash | Comparative agent baseline |
| E2 | smolagents 1.26.0 ToolCallingAgent | kimi-k3.1-pro | Comparative agent baseline |
| E3 | STAR harness | deepseek-v4.1-flash | Decoupled 5-stage synthesis pipeline |
| E4 | STAR harness | kimi-k3.1-pro | Decoupled 5-stage synthesis pipeline |

All workflows use the OS-agnostic unified CLI powered by `uv`:

```bash
# Initialize campaign manifest
uv run plc-agent prepare

# Run single task verification under STAR
uv run plc-agent run --condition E3 --task-id SELF001

# Run single task verification under baseline
uv run plc-agent run --condition E1 --driver deepseek_harness --task-id SELF001

# Execute full experimental campaign
uv run plc-agent run --condition all

# Execute batch functional test evaluation
uv run plc-agent test --condition all

# Aggregate campaign metrics, bootstrap CIs, and McNemar p-values
uv run plc-agent aggregate
```

`prepare` records a SHA-256 digest of the complete structured dataset in `results/summary/campaign.json`. The immutable compiler template hash is recorded during preflight and invocation. Changing a task, assumption, fixed test, interface, compiler version, or template creates a new experimental configuration.

## Common Controls & Resource Budgets

Both frameworks receive the same complete task JSON: natural-language requirements, interface definitions, initial state, scan semantics, assumptions, LTL properties, and fixed test cases. The shared code contract requests a `FUNCTION_BLOCK FB_Task` with separate declaration, implementation, and optional helper DUT/POU objects. All experiment outputs use the same CODESYS compiler backend, installed profile, target/template, and diagnostics.

- **Compiler Attempt Budget**: Exactly **three actual tool calls** (the initial candidate plus at most two repairs).
- **Timeouts**: Compiler timeout is 180 seconds per invocation; LLM request timeout is 180 seconds; task timeout target is 900 seconds.
- **Reasoning Effort**: `medium` for both configured model routes; zero temperature assumed.
- **Serialization & Workspace Isolation**: CODESYS compilation is serialized to prevent IDE repository collisions. Every attempt receives a clean workspace, a fresh request nonce, and a candidate digest.
- **OS-Agnostic ASCII Staging**: The runtime engine automatically executes `stage_ascii_workspace` and `sync_ascii_artifacts` to mirror non-ASCII or deep workspace paths to clean ASCII staging targets, preventing compiler crashes or encoding bugs across operating systems.

## Framework Architecture & STAR Pipeline

### STAR Pipeline (Conditions E3, E4)

STAR organizes synthesis into five decoupled stages:

1. **Planner (`normative_completion`)**: Deterministically analyzes interfaces, initial state, priorities, assumptions, and temporal properties into a structured semantic contract (`analysis.json`).
2. **Dialect Adapter**: Applies IEC 61131-3 syntax normalization, vendor profile adjustments, and type guards (`TON`/`TOF`, `VARIANT`, arrays).
3. **Coder**: Generates structured `FUNCTION_BLOCK FB_Task` code with isolated declarations, implementations, and supporting objects.
4. **Tester (Differential Self-Test)**: Validates candidates against independent finite-state scan oracles (`ScanContract`) and seed-deterministic random testing (`uv run plc-agent random-test --task-id SELF001`) before real compiler invocation.
5. **Ratchet (Lexicographical Monotonic Ratchet)**: Analyzes compiler diagnostics and functional test outcomes, rejecting stagnating revisions and enforcing monotone non-decreasing progress across the 3-attempt budget.

### Comparative Baseline (Conditions E1, E2)

The baseline uses unmodified `smolagents==1.26.0` `ToolCallingAgent` with ReAct prompt, action/observation memory, and model-selected compiler tool calls (`compile_st` and `final_answer`). The compiler tool independently enforces the 3-attempt budget and freezes a successful candidate.

## Isolation and Run Selection

Each run has its own isolated task workspace under `experiments/E*/<campaign>/<task>/run_*`. A fresh agent instance, model adapter, compiler tool, and conversation are created per task. No filesystem, shell, web-search, or reference-solution tool is exposed to the model. The compiler tool is bound to the current task/workspace by trusted infrastructure code. Hand-authored reference ST examples (`codesys/examples/`) and Python oracles are strictly isolated and used solely for offline verification.

Prompt text, request payloads, model responses, source versions, compile attempts, and tool evidence are preserved. Request headers containing credentials are never serialized.

## Outcomes, Metrics, and Release Gates

- **First-Pass Compilation Rate**: Initial candidates compiled cleanly divided by all 32 planned tasks.
- **Final Compilation Rate**: Tasks compiled within the 3-attempt budget divided by all 32 planned tasks.
- **Repair Effectiveness**: Initial compile failures repaired successfully divided by initial compile failures.
- **Case-Level Functional Pass Rate**: Passed test cases divided by evaluated test cases against actual CODESYS IDE simulation or `ScanContract` oracles.
- **Task-Level Functional Pass Rate**: Tasks with 100% of cases passed divided by fully evaluated tasks.
- **Statistical Significance**: McNemar exact test p-values comparing STAR against the baseline, alongside 95% bootstrap confidence intervals.
- **Formal Verification Export**: Formally verifies LTL specifications using model checkers (`uv run plc-agent export-verify --task-id SELF001`).
- **Interactive Workflow, Benchmark & Waveform WebUI**: Live/replayed execution pipeline, candidate version diffs, benchmark matrix, and same-screen CODESYS compile/simulation waveform comparator at `http://127.0.0.1:8765` (`uv run plc-agent web`).
