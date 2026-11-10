# Functional testing and CODESYS trace acquisition

Compilation shows that a source can be compiled in a particular project/profile. It does not show that it meets the required control behavior. This project evaluates generated ST using fixed test cases only when outputs were actually observed in CODESYS simulation or a CODESYS runtime. Python reference results are kept separately and are never imported as PLC results.

## Prepare the exact candidate

1. Select the final compiled attempt from the campaign-selected `result.json`. Record its `task_sha256` and the final `compilation_attempts` entry's `source_sha256`. These are canonical JSON digests, not hashes of a prettified `.st` file. Preserve the original result and its evidence.
2. Copy that attempt's `task.project` to an evaluation directory. Keep the generated `FB_Task` declaration, implementation and helper objects unchanged. Add only a driver/caller and watch variables needed to supply inputs and observe outputs. Save the driver source and evaluation project as supporting evidence. If the generated FB or its helpers must be edited, it is a new candidate and must be compiled and reported separately.
3. Ensure the configured cyclic task calls a driver such as `PLC_PRG`. Instantiate one `uut : FB_Task`. The driver must call `uut` exactly once per intended task invocation; do not call it from multiple programs/tasks. Bind every input and IN_OUT parameter. After the call, copy or watch every expected output. No driver statement may implement the intended control behavior on behalf of the generated FB.
4. Initialize a fresh instance before each fixed test case. Initialize caller-owned arrays/records as the task requires. Verify initial state before the first call. Merely setting output bits to zero does not reset hidden edges, counters or timer instances. Use a fresh evaluation instance/application download, or another demonstrated full reinitialization method, and document it.

The compiler's offline linking of `FB_Task` is not the same as cyclic execution. A driver that actually invokes it is required for functional testing.

## Enter simulation and control scan execution

With the evaluation project compiled and logged out, choose Online → Simulation, then Online → Login. On first login, accept creation/download of the simulation application for this evaluation project. Check the visible simulation indicator. The official [simulation procedure](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_testing_in_simulation_mode.html) describes these steps.

For untimed logic, halt the online application at a suitable program step and use Debug → Single Cycle (`Ctrl+F5`) to execute one active-application cycle. Confirm from an invocation counter that the driver called the UUT exactly once. [The Single Cycle command](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_cmd_single_cycle.html) requires online mode and a halted program step. If the installed runtime/debugger does not provide that behavior, use an independently verified driver gate that performs one UUT call per trigger and records the invocation counter.

Before each step, prepare **all** input values from the fixed test, then apply Debug → Write Values (`Ctrl+F7`) while controlling invocation. Prepared values can be entered in the declaration/watch view; the command writes once at the beginning of the next cycle. See the official [Write Values documentation](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_cmd_write_values.html). Verify values at the actual UUT entry and observe outputs only after its return. Persistent forcing is unsuitable for IN_OUT outputs because it can overwrite the FB's updates.

For every scan, record the case ID, zero-based step index, actual sampled inputs, actual end-of-call outputs and an invocation/time marker. A screenshot should include the relevant inputs, outputs and step/counter, or an exported trace should make this association explicit. Record failures exactly as observed, even if they are easy to repair. The result must describe this exact candidate.

## Type-specific procedure

| Interface feature | Acquisition procedure |
| --- | --- |
| BOOL inputs and outputs | Apply TRUE/FALSE values before the call. Record JSON Booleans, not 0/1 strings. Exercise simultaneous requests exactly as fixed. |
| Integer/bit-string values | Use the declared IEC type and exact width. JSON integer results are decimal; a WORD diagnostic may be displayed as `16#8001` but recorded as 32769. Check overflow/range assumptions before interpreting a conversion. |
| REAL values | Record sufficient displayed/exported precision. The evaluator uses absolute tolerance 1e-5 and no relative tolerance. It rejects non-finite values. Do not round a mismatch into a pass. |
| STRING input | Use the exact fixed text, including spaces, empty strings or leading zeros. Quote/escape JSON correctly. Respect declared STRING capacity. |
| Arrays | Preserve the declared IEC bounds. JSON represents elements in declared-index order; record the full constrained array. Do not assume zero-based IEC indexing from JSON list syntax. |
| Structures/DUTs | Define the official fields/types, enter each input field, and record nested JSON objects with exact field names. Extra unconstrained fields may be retained in evidence. |
| IN_OUT references | Allocate concrete caller variables once and pass the same reference each call. Watch their values after the FB returns; avoid forces that overwrite returned values. The `$binding` markers described below are metadata, not ST values. |
| TIME/LTIME | Preserve measured duration and unit conversion in acquisition notes. Fixed traces use IEC duration strings; convert only equivalent units to the expected canonical spelling for import, retaining the raw display/export. String equality in the current importer does not perform IEC duration parsing. |

### Persistent recipe and FIFO bindings

PUB017 uses `ST_Recipe` and `ARRAY[1..10] OF ST_Recipe`. Initialize its caller-owned database once before each case. Step input `{"$binding":"recipe","binding_id":"default","retain_storage":true}` means use the same database, not assign a zero array again. Keep that marker in the trace's `inputs` field so it matches the fixed procedure, and retain a watch/trace export of actual record values as supporting evidence. `recipeIn` is a separate sampled record that may change every step.

PUB018 requires a generic writable scalar and array. Use binding A (DINT, capacity two, lower bound zero) and binding B (BOOL, capacity three, lower bound one), as specified in the task. `item` may be sampled to a fixed scalar value at each call and modified by a successful dequeue. `buffer` is fixed retained caller storage. A successful DINT-only queue does not substantiate the official generic requirement. If the installed profile lacks a suitable VARIANT implementation, preserve the compile/portability failure and report the limitation; do not change the official interface without labeling a separate adapted result.

### Timed and scan-count tasks

The self-built tasks use explicit invocation counts, so a controlled single-call-per-step procedure is appropriate. Several public tasks use actual IEC elapsed time. Their `dt_ms` means elapsed time since the preceding invocation; the first eligible timer call starts at elapsed zero. By contrast, explicit `CycleTime` input is the interval attributed to the current call, and may be accumulated on its first qualifying call.

Do not manually pause for arbitrary amounts of time between calls and claim to have tested an exact timer boundary. Execute timed cases in a cyclic driver with a measured interval and an export that records actual input-transition/output times. Before execution, declare a nonnegative `dt_tolerance_ms` in the task, case or step if the measured task period and jitter need tolerance; otherwise the importer requires exact intervals. Preserve the nominal fixed trace and raw measured timing. Every timed observation must include measured `dt_ms`; missing or out-of-tolerance timing rejects import. If the required boundary cannot be resolved, leave the case UNVERIFIED and explain why. File and timing checks do not replace operator/evidence review of the actual acquisition procedure.

PUB004's maintenance-due threshold is 500 hours. A Python reference jump or an invented elapsed interval is not a real runtime observation. Run the actual-duration case, or use a validated virtual clock interface with separately documented equivalence. Otherwise leave that case unevaluated. Record any runtime limitation on long TIME/LTIME values.

## Trace schema

Write a UTF-8 JSON file only from actual observations. The following is a schema illustration with deliberately empty outputs and placeholder metadata; it is not a valid result or a completed trace:

```json
{
  "task_id": "SELF001",
  "task_sha256": "COPY_FROM_SELECTED_RESULT",
  "source_sha256": "COPY_FROM_LAST_COMPILE_ATTEMPT",
  "backend": "NOT_RECORDED",
  "operator": "",
  "observed_utc": "",
  "evidence_files": [],
  "codesys_profile": "",
  "driver_source": "",
  "timing_notes": "",
  "cases": {
    "latch": [
      {"inputs": {"Start": false, "Stop": false, "GuardClosed": true}, "outputs": {}}
    ]
  }
}
```

After acquisition, `backend` must be `CODESYS_SIMULATION` or `CODESYS_RUNTIME`; enter the actual operator, UTC observation time and evidence paths. Each included case must have exactly the complete fixed number of scan rows. Every row's `inputs` must match the fixed test, including persistent-binding metadata. `outputs` contains observed values; never paste the expected values into this field without executing and observing them. Cases that were not run may be omitted. A single omitted case prevents a whole-task PASS.

Additional metadata fields are allowed and retained in the copied trace. Preserve raw screenshots/exports next to the trace, using submission-relative references when packaging. Evidence references must resolve within the trace directory and name nonempty existing files; the importer computes their SHA256 hashes and verifies any supplied hashes. A file's presence and hash do not prove that acquisition took place, so the final reviewer must inspect it. Record source/profile/driver details to make that review possible. See `functional_trace_format.md` for the precise import contract.

Import after the candidate has verified compilation:

```powershell
.\scripts\run.ps1 import-trace --condition E3 --task SELF001 --trace 'D:\evidence\SELF001.json'
.\scripts\run.ps1 aggregate
```

The task and source digests must match. Each constrained output is compared recursively; expected dicts constrain listed keys, expected arrays constrain every listed element, and omitted expected output names remain unconstrained. Any observed mismatch produces TEST_FAIL. Complete passing cases produce PASS only when every planned case was evaluated; partial passing coverage produces UNVERIFIED. The raw trace is copied into the selected run directory.

## What this evidence can establish

Fixed tests establish only the observed candidate behavior under those sequences and timing conditions. They do not prove all input combinations, all internal states or unbounded LTL liveness. An operator-authored JSON trace needs corroborating runtime evidence. The independent Python oracle can expose inconsistent expected self-task traces, but cannot tell whether generated ST executed those transitions. No PLCVerif or other automatic formal model checking is claimed by this workflow.
