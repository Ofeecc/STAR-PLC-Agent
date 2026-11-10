# Automatic functional testing in CODESYS IDE simulation

The automatic backend executes the generated Structured Text in the installed CODESYS IDE simulator. It does not execute a Python translation or the independent reference controller. `src/plc_agent/simulation.py` prepares an isolated project copy and `codesys/scripts/run_tests.py` runs inside CODESYS Scripting. The ordinary compiler result remains a separate record because the functional test project adds an instrumented `PLC_PRG` caller.

Before any online login, the script sets and checks the device's IDE simulation mode. It never scans a gateway, selects a network PLC address, provides PLC credentials, writes a boot application, or connects to physical equipment. Each operation uses the shared compiler lock and releases the online application and project afterward.

## Fixed scan execution

The test caller is a native, editable ST `CASE` sequencer. It creates a separate fresh `FB_Task` instance for each fixed test case. On each real simulator task scan, the caller assigns that step's inputs, records the actual sampled values, invokes the generated FB once, and stores its observed outputs in typed trace arrays. It then increments the step and invocation counters. The host waits for the exact planned step count and invocation count, stops the simulator, and reads every trace element through the CODESYS monitoring API.

Expected outputs are not inserted into the test caller. They are compared with observed outputs only after actual execution. An offline regression mutates all expected answers and checks that the emitted test program is unchanged. Separate regressions check fresh instances, invocation counts, literal types, and unsupported clock/binding cases. These adapter checks are not PLC execution evidence.

## Coverage and limits

The current adapter supports scalar BOOL, signed and unsigned integer types, bit strings, REAL/LREAL, and fixed STRING inputs. Its eligibility rules cover all 12 self-built tasks and public tasks PUB001, PUB002, PUB003, PUB009, PUB011, PUB014, PUB015, PUB019, and PUB020. These 21 tasks contain 52 of the 81 fixed cases and 359 of the 576 scan observations.

Those numbers describe adapter eligibility, not the number of completed or passing tests. Actual campaign coverage and pass rates must be read from the raw traces and recalculated with the aggregation script. A compiled candidate may still fail a functional case. Cases from a compile-failed task cannot be counted as runtime evaluations.

The adapter deliberately returns `UNVERIFIED` for physical elapsed-time tests (`dt_ms`), TIME/LTIME interfaces, caller-owned VAR_IN_OUT storage, arrays, structures, and VARIANT bindings. In particular, it does not compress a 500-hour maintenance test into a short simulated interval or claim that a normal simulator scan is a controlled wall-clock interval. These cases retain the fixed manual procedures and expected results in `dataset/test_cases/manual_tests.md`. Any future clock or composite adapter requires separate validation before its results enter the benchmark.

## Operation and evidence

After a campaign candidate has passed real CODESYS compilation, use the CLI `test` subcommand with the selected condition and task. For example, from the project directory:

```powershell
.\scripts\run.ps1 test --condition E3 --task SELF001
```

The CLI validates the source hash and passes the exact final compiled candidate to `run_functional`. Each execution preserves the generated test caller, input manifest, copied CODESYS project, compiler diagnostics, process logs, raw monitoring representations, sequence counters, trace JSON, and evaluation summary. `trace.json` includes the task and source hashes and references to supporting files; the importer/evaluator checks those files before counting cases. The acquisition label identifies the automated native scan sequencer.

The observed data are finite test results. They do not establish unbounded LTL liveness, verify every possible input sequence, or prove the safety of a deployed control system.

## Integration validation

An initial BOOL smoke fixture was executed through an explicit request/acknowledgement gate. Its four readbacks matched FALSE, TRUE, TRUE, FALSE and the actual invocation counters were one through four. Monitoring can return a cached value immediately after a prepared write, so the probe now waits for confirmed readback before publishing the next request.

The generic sequencer was then run on the already-generated E3/SELF001 candidate, with the exact source hash from its compilation record. Both fixed cases and all ten scan observations passed in the actual CODESYS IDE simulator. This is a backend integration check; formal campaign results are recorded separately through the CLI.
