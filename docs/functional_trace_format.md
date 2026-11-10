# Importing actual CODESYS functional observations

Functional evaluation imports observations from a real CODESYS runtime or CODESYS simulation. The Python reference controller is excluded. A trace is an operator-recorded artifact; the importer validates its task/source identity, fixed inputs, supporting files, timing and expected outputs. Checking files and hashes does not independently establish that an operator's provenance statement is true. The report must retain that limitation when testing is manual.

Keep the trace JSON and its supporting screenshots, exported monitoring data or runtime logs in one directory. References in `evidence_files` must resolve inside that directory, be nonempty existing files, and stay available for later audit. Both a string path and an object with `path` and optional `sha256` are accepted. A supplied hash must match the file. The evaluator records computed SHA256 hashes and byte sizes in its result.

The top-level trace fields are:

| Field | Meaning |
| --- | --- |
| `task_id` | Exact dataset task ID |
| `task_sha256` | Hash produced by `plc_agent.common.digest(task)` for the frozen task record |
| `source_sha256` | Source hash of the exact compiled candidate being evaluated |
| `backend` | `CODESYS_SIMULATION` or `CODESYS_RUNTIME` |
| `operator` | Person or acquisition system that actually observed execution |
| `observed_utc` | Actual acquisition time, preferably an ISO8601 UTC timestamp |
| `evidence_files` | Supporting files relative to the trace directory |
| `cases` | Object mapping fixed test-case IDs to ordered observations |

Every included test case must contain exactly the number of observations specified by the dataset. Each observation has an `inputs` mapping and an `outputs` mapping. The input mapping must match the fixed test, with Boolean `true` distinct from numeric `1`. Output mappings may include more monitored values than the test expects. All specified expected outputs must match; missing expected fields fail that scan. Numeric outputs use absolute tolerance `1e-5`, Boolean outputs require Boolean values, and arrays preserve length and ordering. Normalize IEC time literals consistently when preparing observations.

If a fixed step includes `dt_ms`, the observed row must also include the measured `dt_ms`: elapsed time since the preceding invocation, not the duration of a host-side sleep. It must match the fixed value exactly unless a nonnegative `dt_tolerance_ms` was declared before experimentation. Tolerance lookup is step, then case, then task, with default zero. A timing mismatch rejects the import; it is not silently treated as a functional-code failure, because the planned test was not executed. Record the actual acquisition clock and runtime scheduling method in supporting evidence.

Do not add a tolerance after seeing a failed result. Amend the dataset, archive the campaign and rerun the applicable conditions if the test protocol needs to change. Timer tests at exact thresholds may require a controlled runtime clock; an approximate manual delay is insufficient evidence for such a boundary.

Each test case resets its function-block instance. Caller-owned IN_OUT arrays or databases are initialized and bound once according to the test's binding metadata, then retained across its scans. A complete per-step logical input description is not an instruction to overwrite persistent caller storage. Keep those binding operations in the acquisition record.

Missing cases remain `NOT_RUN` in case details. A task receives functional `PASS` only if every planned case is evaluated and passes; a partial all-passing import is `UNVERIFIED`. A case-level rate uses evaluated cases as its denominator, and the task-level rate uses fully evaluated tasks. Report task coverage alongside those rates. Infrastructure failure, unexecuted cases and Python reference checks must not become PLC successes.

The command-line importer should call the evaluator with the resolved trace directory as `evidence_root`, preserve the raw trace and supporting files under the corresponding experiment run, and retain the computed hashes. Library callers can supply `evidence_root` explicitly; its default is the project root.
