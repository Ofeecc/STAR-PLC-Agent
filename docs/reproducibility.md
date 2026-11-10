# Reproducing and Auditing the Benchmark (STAR v2)

The submitted repository preserves frozen task specifications, generated Structured Text versions, compiler diagnostics, and audited campaign records. A package marked `PARTIAL` is a reproducible work snapshot; it is not a completed benchmark or final report.

## OS-Agnostic Environment Setup with `uv`

The application requires Python 3.11 or newer and uses `uv` for deterministic, cross-platform environment management across Linux, macOS, and Windows. PyTorch and CUDA are not required for remote inference.

All runtime operations are strictly host- and OS-agnostic, with no host-specific drive letters (e.g. `C:\`, `D:\`) or platform tags. ASCII path staging is fully automated by the runtime engine (`stage_ascii_workspace` and `sync_ascii_artifacts` ensure non-ASCII / multibyte paths are transparently mapped to clean ASCII staging targets for compiler tool safety).

Initialize the virtual environment:

```bash
# Create isolated virtual environment
uv venv

# Synchronize all pinned dependencies
uv sync
```

Run preflight checks and full test suite:

```bash
# Preflight environment check
uv run plc-agent doctor

# Validate frozen dataset against specification requirements
uv run plc-agent validate-dataset

# Run full test suite
uv run --no-sync python -m unittest discover -s tests -v
```

`doctor` records the exact executable, prefix, and package versions in `results/summary/environment.json`. The preserved original assignment and question bank are in `requirements/source/`. Dataset validation compares all official requirements verbatim against the packaged JSON snapshot.

Configure the CODESYS executable, profile name, and immutable benchmark template in `configs/runtime.json` or via environment variables (`PLC_CODESYS_EXE`, `PLC_CODESYS_PROFILE`, `PLC_CODESYS_TEMPLATE`).

## Credentials and Model Probing

API credentials can be supplied via process environment variables or a private settings file outside the submission directory:

```bash
export PLC_API_CONFIG="/path/to/private/relay-settings.txt"
# Optional overrides:
export PLC_API_BASE_URL="https://your-relay.example/v1"
export PLC_LLM_API_KEY="your-api-key"
```

Verify model and compiler integration:

```bash
# Verify streaming and function-tool round-trips
uv run plc-agent probe-models --tool-smoke

# Execute valid-invalid-repaired compiler smoke test
uv run plc-agent compiler-smoke
```

The compiler check must produce `PASS`, `COMPILE_FAIL`, `PASS` for the valid, deliberately invalid, and repaired source fixtures. Successful process exit alone is insufficient; raw error diagnostics and compiled POU signatures are verified.

## Campaign Execution and Interpretation

Freeze the dataset before preparing a campaign. All conditions use all 32 tasks, the same compiler profile/template, and the same attempt budget (initial attempt + up to 2 repairs):

```bash
# Initialize campaign manifest and placeholders
uv run plc-agent prepare

# Run single task verification
uv run plc-agent run --condition E3 --task-id SELF001

# Execute complete experimental campaign across all conditions
uv run plc-agent run --condition all

# Execute batch functional test evaluation
uv run plc-agent test --condition all

# Compute statistical metrics, bootstrap CIs, and McNemar p-values
uv run plc-agent aggregate
```

Each task run maintains an isolated workspace under `experiments/E*/<campaign>/<task>/run_*`. The campaign manifest selects one record per condition/task.

### Formal Verification and Differential Testing

- **Differential Differential Random Testing**:
  ```bash
  uv run plc-agent random-test --task-id SELF001
  ```
  Generates seed-deterministic randomized scan sequences across boundary conditions and validates against `ScanContract`.

- **Export Verification Bundle**:
  ```bash
  uv run plc-agent export-verify --task-id SELF001
  ```
  Exports formal verification bundles including Structured Text source, LTL temporal specifications (`spec.ltl`), and tool configurations for model checkers (nuXmv, UPPAAL, CBMC).

- **WebUI Auto-Test Workbench**:
  ```bash
  uv run plc-agent web
  ```
  Launches the interactive WebUI workbench at `http://127.0.0.1:8765` featuring real-time oscilloscope waveform inspection, multi-pass candidate diffing, and single-click differential test execution.

## Offline Submission Audit

The offline audit reads saved records only, making no API calls and launching no compiler processes:

```bash
uv run python scripts/audit_submission.py
```

The output `results/summary/submission_audit.json` recomputes campaign metrics, verifies task coverage, re-checks compiler signatures, and scans all payload files for secret keys or token leaks.

## Building and Verifying Submission Package

```bash
uv run python scripts/package_submission.py
```

Use `--require-complete` for releases requiring 100% audit gate clearance. The packager stages clean snapshots into `.local/package_staging/`, compiles sorted SHA-256 manifests, builds the ZIP archive, and verifies member digests.
