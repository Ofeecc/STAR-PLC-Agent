# Reproducing and auditing the submission

The submitted files preserve source text, generated ST versions, actual compiler diagnostics and the selected campaign records. Run the audit before hand-in. A package marked `PARTIAL` is a reproducible work snapshot; it is not a completed benchmark or final report.

## Windows environment

Use the existing `Project1` interpreter. The application requires Python 3.11 or newer and `requests`. The selected existing-agent baseline additionally uses the pinned `smolagents` version recorded by the runner. PyTorch and CUDA are not required for remote inference and should not be reinstalled for this project.

From the project folder:

```powershell
.\scripts\run.ps1 doctor
.\scripts\run.ps1 validate-dataset
$env:PYTHONPATH = (Resolve-Path '.\src').Path
& "$env:USERPROFILE\.conda\envs\Project1\python.exe" -X utf8 -m unittest discover -s tests -v
```

`doctor` records the exact executable, prefix and package versions. The preserved original assignment and question bank are in `requirements/source/`. Dataset validation compares all official requirements verbatim against the packaged JSON snapshot; it does not depend on a sibling question-bank folder being present.

Configure the actual CODESYS executable, exact installed profile and frozen benchmark project in `configs/runtime.json`, or use the documented `PLC_CODESYS_*` variables. Use `docs/codesys_setup.md` for installation and template creation. An offline compiler build has no connection to physical equipment. IDE simulation must explicitly confirm simulation mode before login.

## Credentials and model access

Keep a real key outside the project or use a process environment variable. The local private API file and `.env` are excluded from the archive. `.env.example` contains variable names only. Do not copy a Conda environment, an account-authentication file or an installer into the submission folder.

The recorded relay model IDs identify the provider's aliases. They do not independently authenticate the upstream model, establish a context limit or verify a price. The model capability log records actual streaming/function-call round trips. `results/summary/framework_capabilities.json` separately binds real generated-source and CODESYS compiler-tool evidence for both models through smolagents and the self harness. Probe outputs and benchmark usage are separate records.

```powershell
.\scripts\run.ps1 probe-models --tool-smoke
.\scripts\run.ps1 compiler-smoke
```

These commands are integration checks, not benchmark repetitions. The compiler check must show `PASS`, `COMPILE_FAIL`, `PASS` for the valid, deliberately invalid and repaired source. Successful process exit alone is insufficient. The failed build's raw error diagnostics must remain available.

## Campaign execution and interpretation

Freeze the dataset before preparing a campaign. All four conditions use every task, the same project template, the same CODESYS version, the same fixed tests and the same compiler-attempt budget. The existing framework's context/tool loop and the self-developed deterministic repair controller are intentionally different; those differences are documented in the protocol.

```powershell
.\scripts\run.ps1 prepare
.\scripts\run.ps1 run --condition all
.\scripts\run.ps1 aggregate
```

Each task has a separate run folder. The campaign manifest selects one record per condition/task; previous setup attempts or explicit reruns stay preserved. If a framework is replaced during setup, retain the old manifest and tool failure evidence and record the protocol revision. Never silently relabel an old Codex result as a smolagents result.

The formal E1/E2 baseline is the unmodified `smolagents==1.26.0` ToolCallingAgent. Its default ReAct prompt and action/observation memory are retained, with only documented model/Tool adapters. It has no filesystem, shell or reference-answer tool. Both frameworks share the Responses client, reasoning/output settings and compiler budget. Codex's blocked local tool execution is preserved as setup evidence; `scripts/select_baseline.py` is a historical one-time migration helper and should not be rerun over a completed campaign.

The compiler source hash uses canonical JSON serialization of `declaration`, `implementation` and `supporting_objects`; it is not the byte hash of `FB_Task.st`. Source-file hashes and archive hashes use ordinary binary SHA-256. The audit checks the candidate, request nonce, source hash, rebuild marker, error severities, result status and project files for both successful and failed compiler attempts.

`NOT_RUN` means no completed execution is selected. `TOOL_ERROR` and compiler/runtime infrastructure errors are distinct from generated-code failures. `UNVERIFIED` can mean code compiled but fixed runtime tests have not been observed. Compilation and functional correctness are reported separately. Reference Python state-machine checks and finite safety exploration are development evidence and never count as real PLC execution or a full LTL proof.

Execute supported fixed tests with `.\scripts\run.ps1 test --condition all`. The native CODESYS simulation adapter verifies simulation mode, creates fresh FB instances for cases, records actual scan outputs and compares them with the frozen expected values outside ST. It does not automatically evaluate timed or composite/IN_OUT/VARIANT tasks. Alternatively import genuine operator-acquired traces using the operation guide. Traces must bind task/source hashes, preserve sampled inputs and observed outputs, include measured timing where required, and reference existing supporting files. Imported evidence is copied under the run folder for portability. Report missing cases and coverage instead of inventing a pass rate. Compile-failed candidates cannot be executed and remain visible in the compilation denominator.

For request accounting, derive attempted calls from each run's saved `llm_*/request.json` files. The baseline raw `llm_calls` counts attempts, while the harness raw field counts completed responses; interrupted-stream usage can therefore be absent. Report usage coverage and never turn missing tokens or unknown monetary price into zero cost.

## Offline submission audit

This audit reads saved data only. It makes no paid API call and launches no CODESYS process.

```powershell
& "$env:USERPROFILE\.conda\envs\Project1\python.exe" -X utf8 .\scripts\audit_submission.py
```

The full result is `results/summary/submission_audit.json`. The audit recomputes the selected campaign metrics, checks fixed task coverage, rechecks compiler successes and failures, and scans eligible payload files for the locally configured secret and common token patterns. It scans decompressed Office XML and speaker notes as well as raw bytes. Reports contain only filenames, finding types and counts; secret values are never emitted.

Keep the top-level `PLC_Agent_Final` directory when moving the project. The standalone auditor accepts `--root` and resolves historical absolute evidence references through the retained project-root suffix. It never follows an unrelated absolute path or a `..` path outside the project. Original raw path strings remain provenance. On another Windows machine, update local executable/profile/template settings and rerun compiler preflight before new inference experiments.

The audit verifies saved-record consistency. It cannot prove the upstream model's identity or authenticate a manually entered observation. Those limits remain explicit in the report.

## Final artifact review

PDF and PPTX containers must be valid, but opening a ZIP container does not establish layout quality. After compiling and rendering the final report, inspect every page. Render and inspect every slide and check that required text, tables and diagrams remain editable. Save a hash-bound record at `results/summary/artifact_qa.json`:

```json
{
  "report": {
    "path": "report/report.pdf",
    "sha256": "binary SHA-256 of the reviewed PDF",
    "compiled": true,
    "page_count": 2,
    "visual_inspection_passed": true,
    "reviewed_pages": [1, 2]
  },
  "presentation": {
    "path": "presentation/slides.pptx",
    "sha256": "binary SHA-256 of the reviewed PPTX",
    "visual_inspection_passed": true,
    "editable_verified": true,
    "reviewed_slides": [1, 2, 3, 4, 5, 6, 7, 8]
  }
}
```

The example page/slide lists are illustrative; record every page/slide actually inspected in order. The audit obtains PDF page count with `pdfinfo` when available, otherwise uses the review's `page_count`. It gets slide count from the PPTX container and requires all numbered pages/slides to be covered. A file edited after review invalidates its old hash. This is an operator review record supported by the rendering workflow, not automatic proof of good layout.

The explanation video must be shorter than 360 seconds if produced. `scripts/create_narration.ps1` and `create_video.py` can create a real locally encoded narrated slide video from final PNGs and speaking notes. Windows SAPI narration is disclosed as computer-generated; static slides are not described as live PLC footage. The script measures the actual saved MP4 and decodes it completely. The audit uses `ffprobe`, or the completed MP4 movie header when ffprobe is absent, rather than trusting a sidecar duration. An unknown duration remains unverified. When production is unavailable, provide the finished deck, notes and practical recording plan and state that no finished recording is included. This supplies the recording-ready fallback, while the finished-video gate stays `PARTIAL`.

## Building and verifying the ZIP

Wait until campaign outputs and final artifacts have stopped changing, then run:

```powershell
& "$env:USERPROFILE\.conda\envs\Project1\python.exe" -X utf8 .\scripts\package_submission.py
```

Use `--require-complete` for a release that must satisfy every audit gate. The default permits a clearly named `PARTIAL` snapshot, but an integrity or secret-scan failure always blocks packaging. `submission/status.json` records pending checks and never promotes missing experiment evidence to completion.

The builder copies a snapshot into `.local/package_staging/`, includes sorted SHA-256 manifests, creates the ZIP, reopens every member, verifies its bytes against staging and checks its paths. It does not delete or move original files. Staging, credentials, environments, weights, installers and rebuildable caches are excluded from the archive. Draft report notes are omitted while a final PDF is absent. Generated ST, `.project` files, actual failed attempts and raw logs remain included.

`submission/MANIFEST.json` and `MANIFEST.sha256` inside the ZIP cover all payload files except the two manifest views themselves, whose own hashes would be circular. The external package receipt records the final ZIP hash. The archive root is `PLC_Agent_Final/`, preserving relative paths. A concurrent campaign-manifest change during staging makes packaging stop; rerun after work finishes.
