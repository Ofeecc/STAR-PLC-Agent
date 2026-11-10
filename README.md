# PLC Structured Text Coding Agent

This project implements a lightweight coding harness and an unmodified `smolagents==1.26.0` ToolCallingAgent baseline for a CODESYS Structured Text benchmark. The dataset contains all 20 supplied public questions and 12 independently constructed questions. Every task includes source records, scan semantics, LTL properties and fixed expected functional traces.

The implementation separates generated-code compilation, compiler infrastructure failures and functional behavior. Compilation success is accepted only from matching CODESYS rebuild evidence, never a process exit code alone. Python reference checks validate expected sequences for the self-built tasks; they are not execution of generated ST.

The original assignment, public JSON and 25-page public PDF are preserved in `requirements/source/`. The PDF and JSON contain the same twenty titles/difficulties and matching normalized requirements/interface content; see [source provenance and reproducible alignment checks](requirements/source_provenance.md). Added interpretations remain separate from the official text.

## Current evidence

Use the timestamped records in `results/summary/` as the authority. The existing Project1 interpreter is verified, all 20 official source texts are present verbatim, and both configured relay aliases passed Responses streaming/function-tool round trips. Real CODESYS preflight produced 0, 2 and 0 compiler errors for valid, deliberately invalid and repaired programs. Both selected models have generated and actually compiled `SELF001` through both frameworks; the hash-bound integration evidence is in `results/summary/framework_capabilities.json`. The full campaign and functional evaluation have their own separate coverage/status fields. The relay aliases do not independently verify upstream model identity. This README leaves evolving rates to the recalculated machine summaries.

Codex CLI was investigated first, but its installed local approval policy blocked shell/MCP tool execution. The formal baseline was changed to smolagents before its full campaign; the old manifest, failed setup records and rationale remain in `results/raw/protocol_revision_codex_to_smolagents.json` and `docs/baseline.md`. No execution policy was bypassed and no Codex result was relabeled as a smolagents result.

All 128 planned generation runs and the supported native-simulation batch have now finished. Recalculated outcomes are:

| Condition | First compilation | Final compilation | Actual cases passed/evaluated | Case coverage |
| --- | ---: | ---: | ---: | ---: |
| E1 baseline A | 27/32 | 29/32 | 42/45 | 45/81 |
| E2 baseline B | 27/32 | 27/32 | 46/48 | 48/81 |
| E3 harness A | 26/32 | 26/32 | 38/38 | 38/81 |
| E4 harness B | 30/32 | 31/32 | 50/52 | 52/81 |

The functional percentages are conditional on execution. Unsupported elapsed-time/composite bindings remain unverified, and fourteen transport failures remain in the compilation denominators. Full analysis is in [results/analysis/summary.md](results/analysis/summary.md).

Final artifacts are the [12-page English report](report/report.pdf), [8-slide editable deck](presentation/slides.pptx), [speaker notes](presentation/speaker_notes.md), [defense Q&A](presentation/defense_qa.md), and [actual explanation video](video/explanation.mp4), measured at 4:53.936. The video uses disclosed synthetic English narration. The release remains **PARTIAL** for full functional coverage and the requested real IDE screenshot; [manual screenshot steps](docs/compiler_screenshot.md) are provided. Native PowerPoint display and subjective audio listening were not verified. The machine-readable audit and ZIP receipt under `results/summary/` and `submission/` state the final package boundaries.

## Windows quick start

Open PowerShell in the `PLC_Agent_Final` directory. The launcher uses `%USERPROFILE%\.conda\envs\Project1\python.exe` directly and sets `PYTHONPATH=src`. It does not use base Python, reinstall PyTorch or create an environment. On the inspected machine, requests was reused and only small pinned baseline dependencies were added. On another machine, install the baseline optional dependencies into Project1 if absent:

```powershell
& "$env:USERPROFILE\.conda\envs\Project1\python.exe" -m pip install -e '.[baseline]'
```

```powershell
.\scripts\run.ps1 doctor
.\scripts\run.ps1 validate-dataset
$env:PYTHONPATH = Join-Path (Get-Location) 'src'
& "$env:USERPROFILE\.conda\envs\Project1\python.exe" -X utf8 -m unittest discover -s tests -v
```

`doctor` must report `project1_interpreter: true`. If Project1 lives elsewhere on a different machine, edit only the interpreter path in `scripts/run.ps1`; do not silently run the agent with another environment. If the machine lacks requests, install that lightweight dependency into Project1 without upgrading unrelated ML packages. CODESYS runs its own embedded Scripting interpreter.

## Private API configuration

The client supports the relay's Responses API. Configure the current PowerShell session, using the user's own private file outside the submission directory:

```powershell
$env:PLC_API_CONFIG = 'D:\private\relay-settings.txt'
# Optional override when the file contains only a key:
$env:PLC_API_BASE_URL = 'https://your-relay.example/v1'
.\scripts\run.ps1 probe-models
.\scripts\run.ps1 probe-models --tool-smoke
```

The private file's first line contains the existing key. An optional `base_url = "https://.../v1"` line is recognized. During local development, an `APIKEY相关.txt` file in the parent directory is recognized as a fallback. Its pasted TOML or MCP configuration is never executed. Environment variables override file values. `PLC_LLM_API_KEY` is supported for an already-secured environment. `.env.example` documents names; the program does **not** automatically load a `.env` file. Never place a key in `runtime.json`, commands committed to source control, report screenshots or the submission ZIP.

The non-inference model-list request verifies advertised IDs. `--tool-smoke` makes two small inference calls per model to verify streaming, a function call and its return. It records usage and leaves unsupported pricing/context metadata unknown. The chosen IDs are `deepseek-v4.1-flash` and `kimi-k3.1-pro`, with reasoning effort medium. Inspect `results/summary/model_capabilities.json` before running a campaign.

## CODESYS configuration and mandatory preflight

Install the official Windows Development System with CODESYS Scripting and create a clean standard project as described in [CODESYS setup](docs/codesys_setup.md). Use one Application, the installed target and a working Standard library. Keep the template immutable. Configure actual installed paths and the exact installed profile name:

```powershell
$env:PLC_CODESYS_EXE = 'D:\CODESYS\CODESYS\Common\CODESYS.exe' # example only
$env:PLC_CODESYS_PROFILE = 'exact installed profile name'
$env:PLC_CODESYS_TEMPLATE = (Resolve-Path '.\codesys\templates\benchmark.project').Path
# Set only if the installed CODESYS instance requires it:
# $env:PLC_CODESYS_ADDITIONAL_FOLDER = 'exact installed instance folder'
.\scripts\run.ps1 doctor
.\scripts\run.ps1 compiler-smoke
```

Do not copy example paths without checking them. The smoke test submits a valid motor FB, an undefined-identifier defect and the repaired source. It must produce `PASS`, `COMPILE_FAIL`, `PASS` with `verified: true`. Every source, copied project, request, stdout/stderr log and diagnostic evidence file is retained under `results/raw/compiler_smoke_*/`. Missing compiler or scripting support is an infrastructure failure. The runner refuses paid benchmark execution until the preflight matches the executable, profile and template hash.

## Benchmark execution

The default protocol is one run per task and condition: 32 tasks × 4 conditions = 128 planned runs. Each allows one initial compilation and at most two repairs, a 180-second compiler timeout and a 900-second task limit. See [the experiment protocol](docs/experiment_protocol.md) for actual enforceable limits and framework differences.

| Condition | Framework | Relay model ID |
| --- | --- | --- |
| E1 | Unmodified smolagents 1.26.0 ToolCallingAgent | deepseek-v4.1-flash |
| E2 | Unmodified smolagents 1.26.0 ToolCallingAgent | kimi-k3.1-pro |
| E3 | Self-developed harness | deepseek-v4.1-flash |
| E4 | Self-developed harness | kimi-k3.1-pro |

```powershell
.\scripts\run.ps1 prepare
# Begin with a small real integration run after both preflights:
.\scripts\run.ps1 run --condition E3 --task SELF001
.\scripts\run.ps1 run --condition E1 --task SELF001
# Then execute every remaining task; existing completed records are skipped:
.\scripts\run.ps1 run --condition all
.\scripts\run.ps1 aggregate
```

`prepare` freezes the dataset hash and creates explicit NOT_RUN records. A changed dataset cannot reuse that campaign. `--rerun` creates a new run directory and updates the campaign's selected record; it does not erase the older run. Disclose any rerun-selection rule and retain failed runs. Do not use reruns to select the most favorable response after seeing results.

The baseline uses the library's default ReAct prompt, action/observation memory and model-selected compiler tool calls. The public `Model` and `Tool` extension points connect it to the shared Responses client and real compiler; library internals and prompt templates are unchanged. The compiler tool enforces the same three-attempt budget. Only `compile_st` and the standard `final_answer` tool are exposed. Both frameworks receive the same task JSON, including assumptions, LTL and tests. They have no reference-answer access. See [the verified baseline integration](docs/smolagents_baseline.md).

## Functional execution and trace import

Compilation alone leaves a task `UNVERIFIED`. The native CODESYS IDE simulation adapter executes supported scalar, scan-based tests and preserves actual monitored trace arrays. It uses a fresh FB instance for each fixed test and explicitly verifies simulation mode before login. The current adapter does not automate physical-time tests, IN_OUT/composite interfaces or the public VARIANT queue; unsupported tests retain a specific `UNVERIFIED` reason. Run the functional batch after generation:

```powershell
.\scripts\run.ps1 test --condition all
.\scripts\run.ps1 aggregate
```

See [automated simulation](docs/automated_simulation.md), [functional testing](docs/functional_testing.md) and [the complete manual test instructions](dataset/test_cases/manual_tests.md). For a manual simulation/runtime test, reset the FB before each case and preserve actual sampled inputs and outputs, exact task/source hashes, operator, time and supporting trace evidence.

```powershell
.\scripts\run.ps1 import-trace --condition E3 --task SELF001 --trace 'D:\evidence\SELF001.json'
.\scripts\run.ps1 aggregate
```

Only CODESYS simulation/runtime trace types are eligible. Missing cases remain unevaluated. The importer rejects mismatching task/source hashes, changed inputs, incomplete scan sequences and missing/out-of-tolerance observed timing for timed steps. Supporting evidence paths must resolve to nonempty files within the trace directory; their hashes are recorded and any supplied hashes are checked. A matching file and hash still require review of the actual acquisition; they do not prove that a runtime generated the observations.

## Outputs and interpretation

The campaign manifest selects one record for each task/condition. Recalculate `results/summary/metrics.json` and `task_results.csv` with `aggregate`. Planned-denominator compilation rates count all tasks; evaluated-only rates and compiler coverage are also reported. No measured compilation rate is emitted when no actual compiler evaluation exists. Functional case rate is passed/evaluated cases; task rate uses tasks with all cases evaluated. These denominators must accompany every table.

`compiler_call_count` records actual compiler invocations separately from model-selected tool calls. The smolagents tool count includes function calls such as `final_answer`; the harness's tool count covers compiler invocations. The baseline's raw `llm_calls` counts attempted requests, while the harness increments its raw field only after a completed response. For a comparable attempted-request count, the analysis counts saved `llm_*/request.json` files. Missing usage from interrupted streams remains unknown. Compare observed token usage with its coverage, and leave monetary cost null without a verified price.

In campaign task results, `PASS` means every fixed case was evaluated and passed. `COMPILE_FAIL` means real compiler errors remained. `TEST_FAIL` means an evaluated functional case failed. `TOOL_ERROR` and `TIMEOUT` retain infrastructure/resource failure status. `NOT_RUN` means no run occurred. `UNVERIFIED` includes compiled candidates awaiting functional execution and malformed/unverified agent outputs, with a specific reason retained in each result. An individual compiler attempt's PASS describes compilation only.

| Directory | Content |
| --- | --- |
| `src/plc_agent/` | Client, harness, compiler, baseline, MCP tool, trace evaluator and metrics |
| `dataset/public/`, `dataset/self_built/` | Structured frozen task records |
| `dataset/specifications/catalog.md` | Full task text, interfaces, provenance, LTL and test index |
| `codesys/scripts/`, `codesys/templates/` | Embedded scripting and immutable project template |
| `codesys/examples/` | Hand-authored self-task reference examples, never model results |
| `configs/` | Nonsecret runtime limits and four-condition configuration |
| `experiments/E1` through `E4` | Isolated task/run workspaces, model outputs and compiler evidence |
| `results/raw/`, `results/summary/` | Protocol records and reproducible summaries |
| `report/`, `presentation/`, `video/` | Report, editable deck and actual/recording-ready video materials |
| `requirements/checklist.md` | Rubric and remaining evidence gates |
| `submission/` | Audited hand-in package when created |

The submission excludes keys, private API files, Conda environments, model weights, caches, installers and large temporary previews. A final hand-in must contain the successful compiler preflight, actual experiment records, an English report PDF and editable presentation. An explanation recording must be under six minutes; a script is not a completed video. Submission deadline: **13 November 2026, 23:59 Asia/Hong_Kong**.
