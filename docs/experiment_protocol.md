# Four-condition experiment protocol

## Objective and frozen units

The benchmark compares generation of CODESYS Structured Text by an unmodified existing coding agent and a lightweight self-developed harness, using the same two relay model IDs. Compilation, functional behavior, time and reported resource consumption are separate outcomes. The project does not assume that the self-developed harness will outperform the baseline.

The unit of evaluation is one task under one framework/model condition. The frozen dataset contains all 20 instructor public tasks and 12 self-built tasks. The public `requirements` values remain verbatim; explicitly recorded assumptions resolve ambiguous behavior. Each condition covers all 32 tasks, including hard/generic tasks and failures. There is one planned repetition per condition/task, totaling 128 runs.

`prepare` records a SHA-256 digest of the complete structured dataset in `results/summary/campaign.json`. Each result records the task digest. Public source coverage is checked against the supplied question-bank JSON when it is present beside the project. The immutable compiler template hash is recorded during preflight and invocation. The executable/profile and version evidence must be retained. Changing a task, assumption, fixed test, interface, compiler version or template creates a new experimental configuration; do not silently combine incompatible results.

| Condition | Framework | Model ID |
| --- | --- | --- |
| E1 | smolagents 1.26.0 ToolCallingAgent | deepseek-v4.1-flash |
| E2 | smolagents 1.26.0 ToolCallingAgent | kimi-k3.1-pro |
| E3 | Self-developed harness | deepseek-v4.1-flash |
| E4 | Self-developed harness | kimi-k3.1-pro |

The names above are the relay's actual exposed identifiers. Listing and successful tool-call probes establish access/protocol behavior, not independent proof of an upstream vendor/model identity. Pricing and context limits remain unknown unless the provider supplies verifiable metadata. Token usage is reported only when supplied by the service or baseline event stream.

Codex CLI was the initial preferred baseline. Its relay conversations worked, but the installed local noninteractive approval policy blocked shell/MCP execution. The baseline was explicitly replaced before the full smolagents campaign. `results/raw/protocol_revision_codex_to_smolagents.json` preserves the previous manifest and failure rationale; old setup runs remain available and are excluded from formal smolagents metrics. No policy was bypassed. Actual `SELF001` generation and compiler-tool evidence for all four pairs is summarized in `results/summary/framework_capabilities.json`.

## Common controls

Both frameworks receive the same complete task JSON: natural-language source, interface, initialization, scan convention, assumptions, LTL propositions/properties and fixed tests. The shared code contract requests a `FUNCTION_BLOCK FB_Task` with separate declaration, implementation and optional helper DUT/POU objects. All experiment outputs use the same CODESYS compiler backend, installed profile, target/template and diagnostics. Alternative compilers are excluded from CODESYS success counts.

The default compiler budget is **three actual tool calls**: the initial candidate plus at most two repairs. Compiler timeout is 180 seconds per invocation. LLM connection/read/deadline configuration is 180 seconds per request, and the task timeout target is 900 seconds. Reasoning effort is medium for both configured IDs. No temperature parameter is assumed. CODESYS compilation is serialized to avoid concurrent IDE repository access. Every attempt receives a new project copy and workspace, a new request nonce, and a source digest. The backend cleans, rebuilds, reads diagnostic severities and requires evidence that the submitted POU was compiled. A zero process exit code alone is insufficient.

Both controllers check the remaining 900-second task deadline before further generation and compilation. They pass the remaining time to the common client and clip the compiler timeout to that remainder. The client additionally applies its 180-second configured request limit and checks elapsed streaming time; the compiler process has a bounded wait. These are cooperative controller/client limits, rather than a separate hard kill of the complete framework at exactly 900 seconds. OS scheduling, connection/read operations, lock waiting or cleanup can add overhead. Report actual elapsed time and any overshoot.

## Deliberate framework differences

The self harness deterministically extracts interface, initial state, priorities, assumptions and LTL into `analysis.json`. It sends one generation request, calls the compiler, and—only after actual compiler errors—constructs a focused repair prompt. Its repair context contains the original task, current candidate, deduplicated relevant diagnostics capped by the implementation, and earlier repair summaries. It does not resend every raw compiler log. Success, budget exhaustion, infrastructure failure and resource limits terminate the loop.

The unmodified `smolagents.ToolCallingAgent` owns the baseline's ReAct system prompt, memory, model/tool loop and tool execution. A documented `Model.generate` subclass adapts the common Responses client, and a documented `Tool` exposes the bound-task compiler. The shared task and source contract are supplied as task/instruction text; the library's default prompt template and internals are not patched. The only tools are `compile_st` and the standard `final_answer`. The compiler tool independently enforces three actual attempts and freezes a successful candidate. The evaluated source is the submitted candidate backed by actual compiler evidence, rather than an unchecked final prose response.

Both frameworks use the same Responses streaming client, `max_output_tokens=8192` and medium reasoning. The baseline allows at most four model calls/steps: up to three source submissions and the normal final-answer step. The self harness permits at most three generation/repair responses and normally terminates immediately after a clean build. Baseline prompts, tool schemas, default textual memory and the possible final-answer call add work that the harness does not perform. These are disclosed framework differences. Token and elapsed-time measurements describe complete behavior under these settings, rather than a pure model-only comparison.

The self harness consumes Responses streaming without making the LLM select the compiler function itself. Compiler use is controlled by the harness. The smolagents baseline asks the model to select tool calls and feeds observations back through its ordinary memory. Small function-tool round trips validate provider protocol behavior; actual generated-source compiler submissions separately establish full integration for both models. They do not establish functional correctness for all tasks.

## Isolation and run selection

Each run has its own task workspace under `experiments/E*/<campaign>/<task>/run_*`. A fresh smolagents Agent, model adapter, compiler tool and conversation are created per task. No filesystem, shell, web-search or reference-solution tool is exposed to the baseline. The compiler tool is bound to the current task/workspace by trusted code. The self harness only receives the current task and its own repair history. No task's generated solution or reference answer is inserted into another run's prompt. Hand-authored ST examples and Python oracles are used for development checks only.

Prompt text, request payloads, model responses, source versions, compile attempts and tool evidence are retained. Request headers containing credentials are not serialized. API keys must never be copied into workspace inputs or the submission.

The default runner resumes unfinished campaign entries and skips any entry whose selected status is not NOT_RUN. `--rerun` creates another preserved directory and changes the manifest selection. A rerun must have an explicit reason such as an identified infrastructure/configuration correction. Report original and replacement results or preregister a uniform rerun policy. Never select the best candidate from repeated trials without disclosing the selection. Pilot runs performed before protocol freeze are labeled separately and are not silently mixed with the final campaign.

## Outcomes and denominators

First-pass compilation success is compiled initial candidates divided by all 32 planned tasks. Final compilation success is tasks compiled within the allowed attempts divided by all 32 planned tasks. Report compiler coverage and evaluated-only first-pass rate alongside these campaign rates whenever coverage is incomplete. A campaign with no actual compiler evaluation has undefined measured rates, not an observed 0% model score. Compiler-service failures remain TOOL_ERROR/TIMEOUT and must not be described as syntax-generation errors.

Repair effectiveness is initial compile failures repaired successfully divided by initial compile failures. Compile errors and infrastructure errors are distinct. A model output that cannot be parsed into the source schema is not a genuine compiler rejection; keep its recorded reason and status rather than fabricate diagnostics.

Case-level functional pass rate is passed cases divided by evaluated cases. A case passes only if every fixed step meets all constrained expected outputs. Task-level rate is passed tasks divided by fully evaluated tasks. Missing cases remain NOT_RUN; compiled code without complete functional evaluation remains UNVERIFIED. Finite test success does not prove the LTL properties. Automatic formal model checking is not claimed unless a real verifier artifact is provided.

The automated functional stage runs the generated FB inside native CODESYS IDE simulation. A generated scan sequencer assigns fixed inputs, invokes one FB call per observed scan and records typed output arrays; expected values are kept outside the ST execution code and are compared afterward. Fresh FB instances isolate cases. The adapter supports scalar scan-based interfaces. Timing-sensitive tests, composite/IN_OUT data and the VARIANT queue require further execution support and remain explicitly unverified; missing coverage is reported for every condition. Python reference checks are excluded from runtime metrics.

Record elapsed time, compiler calls, repairs, raw errors, completion status and reported usage. `compiler_call_count` is separate from framework tool actions. The baseline's `tool_call_count` counts model-requested function calls, including `final_answer`; the harness's external tool is its compiler call. The baseline raw `llm_calls` counts attempted requests, while the harness's raw field increments only after a completed response. Analysis derives comparable attempted-request counts from saved `llm_*/request.json` files and retains both accounting definitions. Missing usage fields remain null. When a provider reports input and output tokens but no total, aggregation derives the total by addition; it never reports missing token usage as zero. Cost is null without verifiable price/usage accounting.

## Analysis and release gates

Run `aggregate` to recreate tables from the manifest-selected raw records. Review `consistency_errors`, inspect every successful compiler evidence/source hash, and preserve failures. Summaries must distinguish case and task denominators, initial and final compilation, real execution and reference checks, alias identity and proven protocol behavior. Use actual successes/failures for case studies; retain the failing source, diagnostic, repair and subsequent compile result. No invented repair example may be presented as a measured experiment.

The final report/deck can be called complete only after the full task coverage, actual CODESYS smoke sequence, both framework/model integrations, four conditions, trace evidence, numerical audit and delivery files are checked. Otherwise retain an explicit pending/partial status.
