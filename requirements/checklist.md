# Assignment evidence checklist

Deadline: **2026-11-13 23:59 Asia/Hong_Kong**. This is an evidence checklist, not a declaration that the submission is complete. File existence alone does not establish successful compiler, runtime, model or artifact validation. Reconcile the final report and presentation against the latest raw records before hand-in.

Status vocabulary: IMPLEMENTED means source/material exists; VERIFIED means the stated check has actual evidence; PENDING means required evidence remains absent at this documentation checkpoint; OPTIONAL means a bonus that is not needed for the basic assignment.

## Mandatory dataset and specification work

| Requirement | Evidence path/check | Checkpoint status |
| --- | --- | --- |
| Read full English assignment, including equations and motor timing example | `requirements/source/Final project_ENGLISH.docx`; documented scan convention in `dataset/CONTRACT.md` | VERIFIED by task inspection; unchanged source snapshot retained |
| Inspect supplied public PDF and JSON completely | Original snapshots in `requirements/source/`, full `public_bank_pdf.txt`, `source_alignment.json` and reproducible alignment script | VERIFIED: 25 PDF pages, all20 titles/difficulties, matching normalized requirements/interface content; no substantive source discrepancy detected |
| Include every supplied public question | `dataset/public/PUB001.json` through `PUB020.json`; `validate-dataset` public coverage | VERIFIED: all 20 official requirements retained verbatim against the packaged source snapshot |
| At least ten self-built tasks | `dataset/self_built/SELF001.json` through `SELF012.json` | IMPLEMENTED: 12 |
| Traceable source/adaptation records | Every task `provenance`; review files under `dataset/specifications/` | IMPLEMENTED; final human rationality review recommended |
| Diverse realistic tasks and difficulty | Dataset summaries and `dataset/specifications/catalog.md` | IMPLEMENTED: Boolean control, sequencing, data processing, timers, arrays, records, generic queue |
| Interface, types, initialization, scan convention, priorities | Every task JSON and `dataset/CONTRACT.md` | IMPLEMENTED; ambiguous public behavior explicitly annotated |
| LTL for public and self-built tasks | Every task `ltl` and `atomic_propositions`; full catalog | IMPLEMENTED; formal model checking not claimed |
| Test cases and fixed expected outcomes for every task | Every task `tests`; `dataset/test_cases/manual_tests.md` | IMPLEMENTED; expected values are not execution evidence |
| Dataset integrity/count audit | `results/summary/dataset_validation.json`, `validate-dataset` | VERIFIED: 32 tasks, 207 LTL properties, 81 cases and 576 scan steps; rerun if the frozen data changes |

## Mandatory engineering and model work

| Requirement | Evidence path/check | Checkpoint status |
| --- | --- | --- |
| Reuse inspected Project1 | `scripts/run.ps1`; `results/summary/environment.json` | VERIFIED Project1 Python 3.12.7 and requests present; no environment rebuild needed |
| Meaningful lightweight harness | `src/plc_agent/harness.py`, client, compiler, diagnostic handling | IMPLEMENTED; requirement analysis, generation, tool invocation, repair context and termination |
| Real CODESYS insertion and compile | `src/plc_agent/compiler.py`; `codesys/scripts/build.py`; copied `.project` and raw diagnostics | VERIFIED: CODESYS 3.5.22.40, profile CODESYS V3.5 SP22 Patch 4, actual isolated builds |
| Valid/invalid/repaired compiler check | `compiler-smoke`; `results/summary/compiler_preflight.json`; three raw attempt directories | VERIFIED actual PASS/COMPILE_FAIL/PASS, with 0/2/0 compiler errors and all process exit codes 0 |
| Compile success based on diagnostics and fresh source | Nonce/source digest, rebuild flag, error count, POU CRC in evidence | VERIFIED in installed profile; offline audit rechecks both successful and failed attempts |
| Preserve intermediate ST/projects/logs | Per-run `version_*.json`, `compile_*/FB_Task.st`, request and result files | VERIFIED actual selected runs preserve generated versions and compiler evidence; final all-run audit required |
| Existing tool-using coding-agent baseline | `smolagents` ToolCallingAgent integration and actual tool submissions; `results/summary/framework_capabilities.json` | VERIFIED unmodified smolagents 1.26.0 actual compiler-tool use with both models; blocked Codex setup records and explicit baseline revision retained |
| Two actual available model IDs | `configs/experiments.json`; catalog/probes in `results/raw/` and `results/summary/model_capabilities.json` | VERIFIED relay listing and small Responses/function round trips for both IDs; upstream identity UNVERIFIED |
| Record schema/parameters/reasoning | Client payloads, configs, capability logs, experiment protocol | VERIFIED shared Responses streaming, medium effort and 8192 output cap; prices/context unknown |
| Avoid secrets in logs and submission | Redaction/config handling; `scripts/audit_submission.py`, `package_submission.py` | VERIFIED: final eligible-file and staged/ZIP scans found zero configured/common token leaks; final receipt binds the archive |

## Mandatory experiment and analysis work

| Requirement | Evidence path/check | Checkpoint status |
| --- | --- | --- |
| Four conditions: E1/E2 baseline, E3/E4 harness | `configs/experiments.json`; `framework_capabilities.json` | VERIFIED actual integration for all four framework/model pairs |
| Each condition covers all 32 tasks | Campaign manifest and 128 selected result paths | VERIFIED: all 128 planned generation runs attempted; transport failures preserved and compiler coverage shown separately |
| Comparable tasks/compiler/tests/repair budget | `docs/experiment_protocol.md`; shared client and compiler tool budget | IMPLEMENTED protocol; disclose default memory/tool prompts and baseline final-answer step |
| Isolated workspaces and no solution leakage | `experiments/E*/.../run_*`; baseline agent vs trusted records | VERIFIED local provenance/text checks for all 128 runs and 207 requests; cross-task/path/reference fingerprints absent. Semantic/remote-state isolation is not proven; see `results/summary/prompt_isolation_audit.json` |
| First-pass and final compilation rates | `metrics.py`; `aggregate`; `metrics.json`, `task_results.csv` | VERIFIED: first 27/32, 27/32, 26/32, 30/32; final 29/32, 27/32, 26/32, 31/32; frozen compilation snapshot rechecked |
| Functional case/task results | Native CODESYS simulation trace files, `test`, `import-trace` and result fields | VERIFIED finite observations: E1 42/45, E2 46/48, E3 38/38, E4 50/52 cases; coverage out of 81 each. Full coverage PARTIAL |
| Failures/timeouts/infrastructure errors retained | Raw result statuses/reasons; manifest selection history | VERIFIED: fourteen selected provider/transport failures, one final compiler failure and seven failed functional cases preserved |
| Runtime/repair/tool usage/token/cost records | Per-run JSON; provider events; summaries | Actual records retained; derive comparable request attempts from saved requests, show missing usage, leave unknown price/cost null |
| Selected real repair and failure studies | Actual version/diagnostic/repair paths cited by report | VERIFIED evidence-linked E1/PUB014 and PUB018, E2/PUB018, E4/SELF012 and E3/PUB010 studies; compile/runtime/interface distinctions explicit |
| Fair evidence-based interpretation | Experiment protocol and final report | IMPLEMENTED final analysis; single repetition, coverage differences, incomplete usage and unverified relay identity disclosed |

## Required written and presentation deliverables

| Requirement | Evidence path/check | Checkpoint status |
| --- | --- | --- |
| Operation instructions and source explanation | `README.md`, setup/protocol/functional docs | IMPLEMENTED; final clean-machine reproduction PENDING |
| English experiment report | `report/latex/main.tex` and `report/report.pdf` | VERIFIED: final 12-page English report compiled; actual results included |
| Report environment/dataset/spec/framework/results | Rubric contents and raw-record references in report | VERIFIED against manifest-selected analysis; artifact hashes and review in `artifact_qa.json` |
| Architecture diagram and compilation workflow | Report/deck editable/source diagram | VERIFIED source TikZ and editable slide-native diagrams |
| Genuine compiler screenshots and repair examples | Evidence captured from actual CODESYS | PARTIAL: real logs and repairs retained; actual GUI screenshot absent after app-opening approval timeout. See `docs/compiler_screenshot.md` |
| Successfully compile report and inspect all pages | Saved compiler diagnostics and rendered page QA | VERIFIED: local and built-in compilation succeeded; all 12 rendered pages visually inspected; no overfull boxes or unresolved references |
| Editable concise 6–8-slide PPT | `presentation/slides.pptx` and editable sources | VERIFIED: 8 slides, 159 native editable shapes, 8 notes, no slide pictures; all exact SVG source previews inspected. Native PowerPoint display UNVERIFIED |
| Speaking notes under six minutes | `presentation/speaker_notes.md`; timing estimate/rehearsal | VERIFIED actual synthesized narration duration 289.886 seconds; aligned to eight slides |
| Defense preparation | `presentation/defense_qa.md` | IMPLEMENTED preparation; update with actual results |
| Explanation recording under six minutes | Actual video + measured duration, or clearly labeled recording-ready plan if production unavailable | VERIFIED actual MP4 293.936 seconds; H264/AAC, full decode and eight-frame visual QA passed; synthetic narration disclosed, no human listening claim |
| Audited submission ZIP | `submission/` final archive + sorted manifests/status; `scripts/package_submission.py` | VERIFIED actual ZIP creation, reopen/CRC, every-member SHA-256 and credential/path checks; `submission/package_receipt.json` records final size/hash. PARTIAL gates remain visible |

## Optional advanced work

| Bonus | Evidence needed | Status |
| --- | --- | --- |
| Automatic execution of fixed PLC tests | Actual CODESYS IDE simulation adapter, monitored scan arrays and trace comparison | IMPLEMENTED with actual pilots; adapter eligible for 21 scalar/scan-based tasks, 52 cases and 359 scans; timed/composite tasks remain unverified |
| PLCVerif or another real formal checker | Version, translated model/spec, raw verifier results/timeouts | OPTIONAL; not integrated/claimed |
| Stronger specification checks | Sound monitor/verification implementation with documented scope | OPTIONAL; reference checks and data validation are development aids only |
| Multi-platform compilation | Real second-platform integration and separate results | OPTIONAL; not integrated/claimed |
| Context/diagnostic improvements | Auditable implementation and ablation if claimed as performance gain | IMPLEMENTED basic deduplication/repair summaries; no measured gain claimed |
| More repetitions or statistical stability | Preregistered repeated campaigns, all results retained | OPTIONAL; default one repetition cannot establish broad stability |

## Final release audit

- Re-run core unit tests and save their actual output with interpreter/version.
- Re-run dataset validation after freeze, verify 20 official questions and at least 10 self-built questions, and confirm each has LTL/tests.
- Verify CODESYS executable/profile/template and real valid/invalid/repaired evidence.
- Confirm actual selected existing-agent tool use for both models and all four condition/task records; retain the blocked Codex setup logs and explicit baseline revision.
- Recalculate every report/deck number from raw records and document denominators/coverage.
- Distinguish runtime observations, reference checks, unbounded formal verification and missing evidence.
- Inspect report PDF pages, editable PPT content, notes timing and actual video duration if a recording exists.
- Audit ZIP paths/content for API secrets, local auth files, environment/model weights, caches and installers.
- Leave any mandatory unmet gate visibly PENDING/PARTIAL; never call an unfinished benchmark complete.

The machine-readable release checklist is `results/summary/submission_audit.json`, regenerated by `scripts/audit_submission.py`. It rechecks source and compiler hashes, recomputes selected results, validates existing runtime evidence and leaves missing experiment/artifact gates `PARTIAL`. Use `scripts/package_submission.py --require-complete` only after those gates pass. The audit's integrity checks cannot authenticate a provider's upstream model or prove a human-entered runtime observation.
