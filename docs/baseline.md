# Codex CLI baseline and compatibility evidence

**Historical setup record only.** Codex could not execute the required tools under its local noninteractive policy. The formal E1/E2 baseline is the unmodified smolagents 1.26.0 ToolCallingAgent, documented in [smolagents_baseline.md](smolagents_baseline.md). The old probes and protocol revision are retained for provenance and are not formal smolagents results.

The original proposed baseline was the installed, unmodified Codex CLI. It received the same task JSON, formal specifications, expected test cases, CODESYS template, and compiler-call budget as the self-developed harness. Codex controlled its own planning, context, file tools, and compiler-tool selection. The project supplied an external MCP compiler service; it did not alter Codex's agent implementation.

## Actual compatibility probes

`scripts/probe_codex.py --run` made one CLI run per selected relay model, with low reasoning and a 120-second timeout. It created an isolated `probe.txt` with a random value and asked the model to read it using one shell tool, then return the value. This probe used no PLC question, no compiler, and no model reference solution. Existing result files prevent automatic repetition when the script is rerun.

The installed executable reported `codex-cli 0.164.0-alpha.11.1`. Both requested routes completed a Responses conversation, but the local command-execution policy rejected the shell commands before execution. Consequently, neither read-file tool loop was verified:

| Relay route | CLI result | Commands blocked before execution | Reported input tokens | Reported output tokens |
|---|---|---:|---:|---:|
| `deepseek-v4.1-flash` | UNVERIFIED | 3 | 110927 | 959 |
| `kimi-k3.1-pro` | UNVERIFIED | 1 | 48253 | 274 |

These numbers are relay/CLI usage records for compatibility probes, not benchmark metrics. They do not establish upstream model identity or a monetary cost. DeepSeek retried rejected reads within its single CLI turn; Kimi stopped after one rejected read. No additional probe inference was used to resolve the policy failure. Both model names also triggered Codex's missing-metadata warning and fallback metadata. Actual context-window limits and upstream identities remain unverified.

The local failure does **not** establish that either relay route lacks tool support: the models selected tools and reacted to the denial messages. It establishes that the attempted local shell execution did not run. The benchmark's MCP compiler path must be verified separately. A model-list response alone cannot establish client compatibility; the [official gateway requirements](https://learn.chatgpt.com/docs/enterprise/gateway-compatibility) require a complete streamed tool-call/result continuation. The [official configuration guide](https://learn.chatgpt.com/docs/config-file/config-advanced) describes custom provider routing and environment-key authentication.

The authoritative files are:

- `results/summary/codex_compatibility.json`: both probe summaries and actual usage.
- `results/raw/codex_compatibility/<model>/events.jsonl`: sanitized CLI events.
- `results/raw/codex_compatibility/<model>/stderr.log`: actual local policy rejections and metadata warnings.
- `results/raw/codex_compatibility/<model>/invocation.json`: exact nonsecret arguments and prompt.

An additional **offline** Project1 check successfully exchanged MCP `initialize`, `tools/list`, and `ping` messages with `plc_agent.mcp_server`. Its record is `results/raw/mcp_transport_probe/result.json`. This establishes JSON-RPC transport and tool discovery only. It did not call CODESYS or a model and does not prove Codex can invoke that compiler service.

## Reproducible invocation

The runner launches `codex exec` with an isolated `--cd` directory, `--ignore-user-config`, `--ephemeral`, `--skip-git-repo-check`, `--json`, and a workspace-write sandbox. It supplies a custom provider using `wire_api="responses"`, `env_key="PLC_LLM_API_KEY"`, and `requires_openai_auth=false`. The key is passed through process environment, never embedded in command arguments or written into experiment configuration. Local user configuration and its unrelated MCP servers are not intentionally loaded. The user's persistent `CODEX_HOME` is not changed.

The compiler server runs through the Project1 interpreter with an explicit `PYTHONPATH`. Codex receives a single `compile_st` tool accepting candidate source. Task identity, workspace location, and budget are controlled by the server. The full task is present in the prompt as well as `task.json`, so a read-file failure need not prevent the model from preparing a source candidate.

Use `scripts/probe_codex.py --run` only when deliberately authorizing the two tiny paid probes; it reuses existing records. To investigate an existing failure, read the retained logs and validate local MCP startup first. Do not repeatedly invoke models to debug a local policy or interpreter-startup error. Do not bypass approval policies or sandbox controls to make a benchmark pass.

## Fair comparison and unavoidable differences

Every condition must include the exact same 20 public and 12 self-built questions, in independent workspaces. The two framework/model pairs share the CODESYS version/profile, template hash, source contract, formal specifications, expected tests, maximum of two repairs after the first compilation, and task deadline. Failures stay in the denominator and raw records remain available. Run the valid-invalid-repaired CODESYS backend fixtures before launching model-backed benchmark work.

The self harness uses deterministic requirement extraction, generation, diagnostics, bounded repair, and termination. Codex chooses its context and tools using its existing implementation. Its own system prompt, tool schemas, error handling, and extra shell/discovery calls create unavoidable prompt and token differences. These are part of the framework comparison and should be disclosed, not hidden by modifying Codex internally.

The shared compiler-call limit is enforceable in the MCP service. A shared internal model-request limit or identical per-response output-token cap is not established for this installed Codex build. A `turn.completed` event can aggregate several internal requests, so completed-turn count must not be presented as exact API-call count. Separate compiler-call count, all completed tool calls, completed agent turns, token usage, wall time, and any actual billed cost. Where the CLI does not expose a measurement, use `null` or an explicit limitation.

The baseline evaluates the last candidate actually submitted to the trusted compiler service; a later unchecked final answer cannot create compilation success. Compilation success without runtime testing is `UNVERIFIED` overall. A timeout or agent crash remains an agent-completion failure even when earlier compilation evidence exists; retain the compilation outcome separately.

## Compiler ledger and local boundaries

Compiler records are stored outside Codex's designated writable `agent` directory. The MCP server owns the task and enforces the attempt budget. Candidate source is data loaded from JSON, not executable Python; the script writes it into CODESYS editor buffers using its API. Evidence includes fresh request IDs and source hashes. The model's prose cannot substitute for these records.

Directory separation is an audit boundary, not proof of a hardened adversarial sandbox. Verify the installed sandbox's actual write restrictions before claiming ledger tamper resistance. The generated ST is compiled offline and is never downloaded to physical equipment. Neither the model nor the compiler needs other experiment directories or reference solutions.

The compiler MCP process should receive only nonsecret compiler configuration. Explicitly forward the selected executable/profile/template/timeout/budget through a sanitized configuration or MCP environment rather than assuming every environment variable is inherited. API credentials remain for the Codex network client. Any raw temporary CLI log must be redacted before inclusion in the submission, including exact-key replacement in addition to generic key-pattern filtering.

Source normalization errors, missing devices/libraries, blocked process creation, and malformed MCP messages require infrastructure/output-error records. They must not be counted as genuine CODESYS syntax failures. Reserve or record attempts consistently even if malformed source is rejected before compilation, so a damaged attempt directory cannot silently block a later repair.

## Status before benchmark execution

At this review stage, the existing CLI is identified and the two requested relay conversations have been observed. Actual shell-tool execution is blocked by local policy, the custom route metadata is incomplete, and the actual Codex-to-MCP-to-CODESYS loop has not yet been demonstrated by these probe records. The baseline runner is implemented, but the four-condition benchmark cannot be called complete until those remaining checks and all task runs are recorded.
