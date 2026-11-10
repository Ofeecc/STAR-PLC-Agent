# Defense questions and speaking prompts

Use these answers as preparation. The generation campaign has executed all 128 planned runs. Functional evaluation is a separate stage; use the final `results/summary/metrics.json` and report for its completed counts. During the functional batch, do not turn a partial case rate into a claim about all tasks.

## Why is an Agent Harness necessary

A model response alone cannot establish that ST compiles. Our harness organizes the task, submits the generated FB to CODESYS, reads real compiler diagnostics, requests a focused repair when needed and preserves the attempts. The bounded loop makes tool feedback part of the generation process and gives an auditable stopping rule.

## How does this differ from a normal LLM API call

The API client is only one component. The harness also extracts the required interface, initialization and priorities; supplies LTL and fixed tests; creates isolated compiler projects; classifies diagnostic versus infrastructure failures; selects repair context; and records outcomes. A one-shot call lacks that external validation and control loop.

## Why keep the design lightweight

The assignment needs a coherent generation-and-compilation system that can be explained in a short defense. A deterministic controller with one model role makes the repair budget and evidence easy to inspect. More agents would add cost and context interactions without a demonstrated benefit for this benchmark.

## What is the existing-agent baseline

The formal baseline is the unmodified smolagents 1.26.0 ToolCallingAgent. The library owns its default ReAct prompt, action/observation memory, multi-step loop and tool execution. Its public Model and Tool interfaces connect the shared Responses client and CODESYS compiler. Only `compile_st` and the normal `final_answer` tool are exposed. Both selected relay models actually generated and compiled SELF001 through this Agent; `results/summary/framework_capabilities.json` binds the tool-call arguments to compiler source hashes and diagnostics.

## How does our harness differ from smolagents

Our controller chooses a fixed generation/compile/repair sequence and selects relevant diagnostics and source history. Smolagents uses model-selected function calls and its normal action/observation memory. Both receive the same task, medium reasoning, an 8192 output-token cap per request and at most three compiler attempts. The baseline can use a fourth model call for its final answer, while our harness normally stops after clean compilation. Those prompt, memory and final-answer differences are disclosed.

## Why was Codex not used as the final baseline

Codex CLI was initially preferred. Its relay conversations completed, but the installed local noninteractive execution policy blocked the required shell/MCP tool execution. This was a setup infrastructure issue, rather than evidence of weak model code generation. The baseline was explicitly changed to smolagents before the full campaign. Original failures and the old manifest remain in `results/raw/protocol_revision_codex_to_smolagents.json` and the setup logs. No execution policy was bypassed or Codex result relabeled.

## Is compilation genuinely performed by CODESYS

Yes. The installed system is CODESYS 3.5.22.40, profile `CODESYS V3.5 SP22 Patch 4`. Its embedded script opens a copied project, inserts native ST, clears old messages, cleans/rebuilds and collects diagnostic severities. The outer process checks source hashes, a unique request nonce and evidence that FB_Task was compiled. The actual valid/undefined-identifier/repaired preflight produced 0, 2 and 0 errors. All three processes exited with code zero. Raw projects, source and compiler messages remain under the paths in `results/summary/compiler_preflight.json`.

## Why does a process exit code not prove success

The IDE can finish running its automation script even when compilation produced errors. A process return value describes process execution, not program semantics. We require matching rebuild diagnostics and evidence that the submitted POU was compiled, and preserve the project/source for inspection.

## How were LTL properties constructed

We first fixed a scan convention: inputs are sampled for the call and outputs are observed at its end. We then translated each task's initialization, stop priority, interlocks, retained state and transitions into predicates and LTL formulas. Numeric/timing predicates and fairness assumptions are explicitly defined. Public ambiguities are documented separately from the unchanged source text. The formulas are specifications; no automatic model-checking proof is claimed.

## Why does the motor example need a timing decision

The assignment's example formulas use next-step motor values and its table shows a delayed observed start, while the prose can be read as end-of-current-scan behavior. We use end-of-call observation consistently and state that choice in every task. The same interpretation goes to both frameworks and the fixed tests, so timing ambiguity is not silently used to favor either agent.

## How was functional correctness tested

The fixed tests describe complete input sequences and constrained expected outputs. The native CODESYS IDE simulation adapter creates a fresh FB instance per case, applies fixed inputs through a scan sequencer, calls the generated FB and stores monitored typed output arrays. Expected outputs stay outside the executing ST and are compared afterward. Task/source hashes and raw simulation evidence bind the observations to the compiled candidate. The adapter is eligible for 21 of 32 tasks, 52 of 81 cases and 359 of 576 scan observations before generation failures. Those are eligibility counts, not pass counts. Timed and composite/IN_OUT/VARIANT tasks remain outside automated coverage. The Python oracle validates expected self-task sequences separately and contributes no PLC runtime passes.

## Is compilation enough for a pass

No. Compiled candidates remain UNVERIFIED until their fixed cases are executed. E1/PUB014 is a real example: compiler feedback repaired the string-length call, and the second build compiled, but actual CODESYS simulation failed both fixed cases (0/2), with 13/19 individual scan observations passing. Compilation fixed an API/type issue without establishing IPv4 behavior. The selected run contains `version_00.json`, `version_01.json`, `compile_00`, `compile_01` and its actual functional trace. A task passes only when all its planned cases are evaluated and pass.

## What are the actual four-condition compilation results

All 128 generation runs executed, with 32 planned tasks per condition. Counts include infrastructure failures in the denominator:

| Condition | Framework / relay route | First-pass compiled | Final compiled |
| --- | --- | ---: | ---: |
| E1 | smolagents / deepseek-v4.1-flash | 27/32 (84.4%) | 29/32 (90.6%) |
| E2 | smolagents / kimi-k3.1-pro | 27/32 (84.4%) | 27/32 (84.4%) |
| E3 | Our harness / deepseek-v4.1-flash | 26/32 (81.3%) | 26/32 (81.3%) |
| E4 | Our harness / kimi-k3.1-pro | 30/32 (93.8%) | 31/32 (96.9%) |

These are observed single-run compilation outcomes. A clean build does not establish task fidelity or runtime correctness; the public VARIANT FIFO particularly needs that distinction. Recalculate the table from the final selected records before defense.

## Show one real repair by our own harness

Use E4/SELF012, the bounded fault-retry controller. Its first candidate declared the enum literal `LOCKED` and the required Boolean output `Locked`. CODESYS resolves those names case-insensitively, and the first build reported three type errors, including `Cannot compare type 'INT' with type 'BOOL'` and `Cannot convert type 'BOOL' to type 'E_TASKSTATE'`. The model received the actual diagnostics and prefixed enum literals as `TASK_IDLE`, `TASK_RUNNING`, `TASK_WAIT` and `TASK_LOCKED`, keeping the output interface. The second actual build had zero errors after one repair. `version_00.json`, `version_01.json` and both compiler evidence files preserve the change. Functional results must be read independently from the completed test stage.

## Is the comparison fair

Both frameworks use the same task JSON, two model IDs, compiler installation, template, fixed tests, three-attempt compiler budget, Responses client, medium reasoning and 8192 output cap. Workspaces/conversations are fresh and reference solutions are excluded. We disclose default memory/tool prompts, model-selected versus controller-selected compilation, the baseline's possible final-answer call and cooperative deadline enforcement. One repetition and relay failures limit any ranking claim. The purpose is a credible comparison, without tuning our harness to win.

## How are failures counted

Every planned task stays in the campaign denominator. Actual remaining compiler errors are COMPILE_FAIL; interrupted relay streams, TLS failures and timeouts retain their infrastructure/resource statuses. Compiler coverage is reported separately. Missing functional cases are not passes. Failed runs and explicit reruns remain preserved. We derive comparable attempted-request counts from saved `llm_*/request.json` files because the raw baseline counter counts attempts while the raw harness field counts completed responses. Usage missing after interrupted streams remains unknown; unknown price does not become zero cost.

## Are the two model identities proven

We can prove which relay IDs were requested and what the provider returned. Catalog listing and protocol probes establish that those aliases are available and support the tested Responses streaming/tool round trip. They do not independently prove the upstream model identity. Context and price information are left unknown unless verified provider data is available.

## What are the main limitations

One repetition cannot establish broad statistical stability. Finite simulation traces do not prove all LTL properties or unbounded liveness. The automated runtime adapter covers scalar scan-based tasks; physical timing and composite caller bindings need further work. The public VARIANT FIFO can compile under a custom substitute type without establishing the requested generic behavior. Relay aliases do not prove upstream identity or pricing, and interrupted responses can omit token usage. These limits belong beside the measured compiler and functional coverage.

## What would you improve next

Broaden the existing native simulation adapter to timed and composite tasks, add repeated trials under a frozen protocol, and investigate a verified formal-checking path. Changes should be evaluated in a new protocol version, preserving the current raw records and fixed tests.

## Short demonstration sequence

Show the frozen task and its priority property, then the generated ST, actual CODESYS diagnostics, a focused repair and the subsequent real compile result. Show a separate functional trace and its expected-output comparison. Finish with the four-condition table and its denominators. Use an actual recorded case; if it has not run, label the demonstration as an implementation walkthrough.
