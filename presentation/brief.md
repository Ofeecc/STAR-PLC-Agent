# PLC Structured Text Coding Agent Defense

Audience: undergraduate automation course instructor and classmates. Eight slides, English text and speaking notes, under six minutes. Use restrained technical design with editable diagram/table objects and actual compiler/runtime evidence. The source assignment and English report govern facts.

Verified source facts: 20 official public questions and 12 independently constructed questions; 207 LTL properties; 81 functional cases and 576 scan observations. Inputs sampled at scan start and outputs observed at scan end. LTL properties and expected test traces are specifications, not formal proofs.

The self harness parses structured requirements, generates an FB_Task, invokes real CODESYS, extracts diagnostics, repairs within two retries, and records each attempt. Compilation backend verified valid0errors -> deliberate invalid2errors -> repaired0errors with real CODESYS3.5.22.40. Exitcodes were0 in allthree tests, demonstrating why diagnostic inspection is necessary.

Formal baseline: unmodified smolagents1.26.0 ToolCallingAgent with a documented Responses model adapter and compiler tool. Codex CLI setup failed because local approvals were unavailable; its setup records remain preserved. Both frameworks use relay IDs deepseek-v4.1-flash and kimi-k3.1-pro, reasoning medium, max8192 output tokens per response, three total compiler calls and900second task budget. These are relay-reported IDs; upstream identity, context limits and monetary prices are not independently verified.

Experiment table and case study will be filled from final raw campaign records. All128 planned runs remain in the denominator. API failures are infrastructure/transport failures. The automatic simulator supports21tasks/52cases/359scans by schema, but only actual executed observations enter test rates. Physical-time and composite-storage tasks need separately validated adapters. Do not present eligibility as completed evaluation.

Slide outline: objective; dataset and scan specifications; harness architecture; actual compiler evidence; two-by-two experiment protocol; actual compilation and functional results; real diagnostic-driven repair case; conclusions and limitations.
