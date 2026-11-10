# PLC Structured Text Coding Agent

## Introduction

This project investigates how an agent can generate Structured Text (ST) for CODESYS, obtain real compiler feedback and repair unsuccessful code. An isolated model response is insufficient for this workflow: generated text must be placed in a valid PLC project, compiled, associated with trustworthy diagnostics and evaluated against the requested behavior. We implemented a lightweight Python harness and an external compiler service, with the unmodified smolagents ToolCallingAgent as the existing-agent baseline. The experiment compares two frameworks using the same two relay model routes. Compilation and functional correctness are measured separately.

This methods draft describes implemented and verified infrastructure. Actual model-generated programs have been compiled and simulation pilots have executed, but final campaign outcomes and functional coverage belong in the results section recalculated from the selected raw records.

## Experimental environment

The host runs Windows 11, build 26200. The application uses the existing Conda environment `Project1`, Python 3.12.7 and Requests 2.32.5. Existing packages include PyTorch 2.2.2, NumPy 1.26.4, pandas 2.3.3 and Matplotlib 3.10.6; local GPU inference is unnecessary. The harness uses remote APIs and lightweight standard-library components rather than installing another ML environment. Small dependencies were added for the pinned smolagents 1.26.0 baseline; PyTorch and CUDA were reused without replacement.

CODESYS 3.5.22.40 is installed at `D:/Codesys`, with profile `CODESYS V3.5 SP22 Patch 4`. Its scripting interpreter runs inside CODESYS, separately from Project1. The reusable template contains one application. Each compilation copies that template into a new workspace. Runtime configuration sets a 180-second compiler timeout, a 180-second model-response limit and a 900-second task deadline. Generation allows two repairs after the initial attempt, giving at most three compiler calls. The configured reasoning effort is `medium`.

Both controllers check remaining task time before further generation and compilation, pass that remainder to the shared client and clip compiler waiting to it. The client also enforces its configured per-request limit and checks streaming elapsed time. These cooperative limits do not constitute a separate process-level kill of the whole controller at exactly 900 seconds; OS scheduling, lock waiting and cleanup may add overhead. Actual elapsed time and any overshoot must remain visible.

Environment metadata, the current configuration and actual compiler evidence are retained in `results/summary/environment.json`, `configs/runtime.json` and `results/summary/compiler_preflight.json`. Per-run configuration snapshots omit API credentials. Credentials are loaded from process environment or a private local file and are excluded from submitted configuration and sanitized logs.

## Dataset construction

The dataset contains all 20 supplied public questions and 12 self-built questions. Public English statements are preserved verbatim from the supplied JSON; interpretations are stored separately. Validation checks that every official statement is included and records a source hash. The combined dataset has 10 easy, 14 medium and 8 hard questions, with 207 LTL properties, 81 test cases and 576 planned scan observations.

Each task records provenance, rationale, interfaces and types, initialization, scan semantics, priorities, assumptions, temporal properties and fixed expected sequences. The public set includes process sequencing, edge detection, hysteresis, runtime accumulation, arrays, parsing, recipe management and generic FIFO behavior. Composite types and caller-owned storage receive explicit binding information. In particular, the official FIFO's `VARIANT` interface remains unchanged; its CODESYS portability is a disclosed issue rather than grounds to silently substitute a scalar-only task.

The self-built questions were synthesized for this project, with the assistant's construction and review process stated in their provenance. They cover guarded motor retention, neutral-scan reversal, restart inhibition, pallet indexing, traffic phases, tank hysteresis, alternating pumps, consecutive-scan qualification, edge counting, alarm acknowledgment, actuator handshakes and bounded fault retries. They use four easy, six medium and two hard tasks. Fixed expectations were written separately from Python transition implementations, then compared. These checks are assistant consistency review, not external industrial certification. The dataset validation and full source/adaptation records are available in `results/summary/dataset_validation.json` and `dataset/`.

## Scan semantics and specifications

For invocation `k`, inputs `I[k]` are sampled once, retained pre-state is `q[k]`, and outputs `O[k]` are observed after execution. The invocation computes the next retained state `q[k+1]`. Each test creates a fresh instance; step zero executes normally. Initial conditions describe the instance before that invocation, not an extra delayed output row.

This convention resolves an ambiguity in the assignment's motor example. Its embedded formulas use `G((StopBtn ∨ EStop) → X ¬Motor)` and `G((StartBtn ∧ ¬StopBtn ∧ ¬EStop) → X Motor)`. The example table likewise shows startup in the following row. These are consistent with rows containing pre-scan motor state. Our rows contain end-of-scan outputs, so corresponding properties use same-row outputs: `G((StopBtn | EStop) -> !Motor)` and `G((StartBtn & !StopBtn & !EStop) -> Motor)`. Applying the original `X` formulas directly to our observations would incorrectly reject a start followed immediately by a stop.

Properties address priorities, mutual exclusion, retention, transitions and faults. Arithmetic comparisons and named predicates are defined in each task's atomic propositions. Conditional liveness states its environmental assumptions: recurring traffic phases require persistent enable and recurring ticks, for example. Strong until requires eventual release; a latched fault that may await reset forever instead uses the weak-until expansion `G Fault | (Fault U validReset)`. Finite tests cannot prove unbounded liveness. Detailed interpretation is in `docs/ltl_semantics.md`.

The twelve self-built reference models passed 24 fixed cases with 142 observations. Separate finite exploration checked 44 selected safety predicates over 5,152 transitions. These results validate the Python reference models, not generated ST or the complete LTL property set. Their evidence is explicitly `PYTHON_REFERENCE_ONLY` and is excluded from PLC success rates (`results/summary/reference_validation.json`).

## Self-developed harness

The harness follows a bounded control loop:

`Task JSON → requirement analysis → ST generation → CODESYS compilation → diagnostic analysis → focused repair → recompile → functional evaluation`

Requirement analysis extracts the function-block interface, initialization, scan convention, priorities, assumptions and formal properties. Generation requests a JSON object containing a `FUNCTION_BLOCK FB_Task` declaration, its ST implementation and any helper types or POUs. Explicit object separation avoids relying on informal code-fence extraction. All source versions and request/response records are retained.

After compilation, the diagnostic analyzer deduplicates relevant error messages and bounds their size. A repair request contains the original task, current source, current errors and compact repair history. It asks for focused changes while preserving correct behavior and interfaces. The harness stops after successful compilation, exhausted repair budget, infrastructure failure or a resource limit. Compilation success yields overall `UNVERIFIED` until actual functional observations are evaluated. This separation prevents a syntactically valid but behaviorally wrong program from being reported as a functional success.

## Real CODESYS compilation and preflight

`compile_st(task, source_code, workspace)` creates a fresh template copy and launches CODESYS with `--runscript`, `--scriptargs` and `--noUI`. The internal script writes source through CODESYS editor APIs and reads the buffers back to confirm insertion. It forces `FB_Task` into the build, cleans previous output, clears diagnostic categories and rebuilds the application. Error and fatal-error messages are collected with locations. A successful result also requires a compiled POU signature, matching request nonce and source hash, and normal process completion. Windows argument quoting is handled explicitly because the installed application expects quoted option values. The relevant official APIs document command-line execution, rebuilding and message collection [1–3].

The backend passed an actual valid–invalid–repaired preflight:

| Fixture | CODESYS errors | Recorded result |
| --- | ---: | --- |
| Valid motor latch | 0 | PASS |
| Undefined identifier introduced | 2 | COMPILE_FAIL |
| Corrected motor latch | 0 | PASS |

The invalid fixture produced both an undefined-identifier diagnostic and a type-conversion diagnostic. All three processes exited with code zero, demonstrating why exit status alone cannot establish compilation success. Fresh projects, source files, invocations, compiler messages and signatures are retained under the directory referenced by `results/summary/compiler_preflight.json`. This preflight validates the backend; its deterministic correction is not a claim of model-driven repair success.

## Baseline and four-condition protocol

The selected relay IDs are `deepseek-v4.1-flash` and `kimi-k3.1-pro`. Both appeared in the provider catalog and completed an actual streamed Responses function-call/result round trip at medium reasoning effort. The probes requested `echo_scan(7)`, returned its result and verified continuation. This establishes the tested API behavior, not upstream model identity, context limits or pricing (`results/summary/model_capabilities.json`).

The formal conditions are E1 smolagents/DeepSeek route, E2 smolagents/Kimi route, E3 harness/DeepSeek route and E4 harness/Kimi route. Each condition covers the same 32 tasks, compiler template/profile, formal specifications, fixed tests, three-call compiler budget and task deadline. That produces 128 planned task runs. Both frameworks see expected tests, so the experiment measures specification following rather than hidden-test generalization.

The unmodified smolagents ToolCallingAgent retains its default ReAct prompt, action/observation memory, loop and tool execution. A documented Model subclass connects the same Responses transport; a documented Tool exposes the bound-task CODESYS compiler [4,5]. No library source or prompt template is patched. A fresh Agent and conversation are created per task, with only the compiler and standard final-answer tool. No shell, filesystem, web-search or reference-answer tool is exposed. The evaluated source is the successful compiler-submitted candidate, not unchecked final prose.

Both frameworks use the same 8,192 output-token cap and medium reasoning. The baseline permits four model calls/steps to allow up to three candidates and its normal final-answer step; the harness permits at most three generation/repair responses and stops at clean compilation. The baseline's default prompts, textual memory, tool schemas and possible final-answer call are deliberate framework differences. Compiler-call count is separate from model-selected function calls. Raw baseline `llm_calls` counts attempted requests, while the harness increments that field after completed responses; comparable attempted-call analysis therefore counts saved request files. Observed usage is reported with missing-response coverage. Missing tokens and unknown prices are not treated as zero cost.

Codex CLI was the initially preferred framework. Its relay conversations completed, but installed local policy rejected command/MCP execution. The formal baseline was explicitly replaced before the full smolagents campaign, preserving the old manifest and failed setup records under `results/raw/protocol_revision_codex_to_smolagents.json`; no execution policy was bypassed. These setup failures are not smolagents benchmark results. Actual generated-source compilation of `SELF001` now verifies both model/framework combinations for smolagents and the harness, with compiler nonce/source hashes and model-selected tool-call evidence recorded in `results/summary/framework_capabilities.json`.

## Actual CODESYS functional execution

The functional adapter runs supported fixed tests inside CODESYS IDE simulation, explicitly verifying simulation mode before online login. A generated PLC_PRG scan sequencer assigns the complete fixed inputs at each step, invokes the candidate FB once, and writes typed input/output trace arrays. Separate fresh FB instances isolate test cases. Expected outputs are never inserted into the executing ST; Python compares the acquired output arrays with the frozen dataset afterward. Monitoring checks the actual completion step and call count before extracting observations. This is native simulation of the generated ST, not a Python replacement for PLC execution.

The current adapter is eligible for 21 of 32 tasks, covering 52 of 81 cases and 359 of 576 scan observations before generation failures. It supports scalar scan-based interfaces. Timing-sensitive tests, composite/IN_OUT interfaces and the generic VARIANT queue remain outside its automated scope, with explicit UNVERIFIED reasons and manual procedures. Actual simulation pilots passed the generated E3/SELF001 tests and E3/PUB002 DWORD tests, including bit 31 and the full unsigned 32-bit range. Their saved traces establish adapter integration; final campaign counts must be taken from selected task records rather than counted again as extra benchmark cases.

## Evaluation and limitations

First-pass and final compilation rates use the full planned task denominator, with actual compiler coverage and infrastructure statuses shown separately. Repair effectiveness measures first-attempt failures recovered within budget. Functional case rates use evaluated cases; functional task rates require every planned case to pass and report complete-task coverage. Raw failures are retained. Aggregation checks consistency and does not substitute Python outputs for PLC observations.

Actual functional traces identify the task and compiled source, preserve supporting files and hashes, and match fixed inputs. Timed steps require measured intervals within a preregistered tolerance. Manual acquisition remains an operator-supported claim requiring evidence review. Automated simulation and its measured coverage do not establish correctness for unsupported tasks or unbounded LTL properties. No additional PLC platform or monetary-cost conclusion is claimed.

## Primary implementation references

1. CODESYS, [Starting Scripts from the Command Line](https://content.helpme-codesys.com/en/CODESYS%20Scripting/_cds_starting_script_via_command_line.html).
2. CODESYS, [ScriptApplication](https://content.helpme-codesys.com/en/ScriptingEngine/ScriptApplication.html).
3. CODESYS, [ScriptSystem](https://content.helpme-codesys.com/en/ScriptingEngine/ScriptSystem.html).
4. Hugging Face, [smolagents Agent reference](https://huggingface.co/docs/smolagents/reference/agents).
5. Hugging Face, [smolagents Model reference](https://huggingface.co/docs/smolagents/reference/models).
