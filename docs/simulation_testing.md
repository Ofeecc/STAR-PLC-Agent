# Optional automated testing in CODESYS IDE simulation

This prototype uses the real CODESYS IDE simulator and a disposable copy of the validated compiler template. It makes no LLM calls. Its only fixture is a known BOOL function block `y := x;`, with four requested invocations producing FALSE, TRUE, TRUE, FALSE. It is an infrastructure smoke test, not a result for any of the 32 benchmark tasks.

At authoring, this prototype has passed Python syntax inspection only. Actual simulation login, monitored reads, and request acknowledgement must succeed on the installed profile before the output can be described as runtime evidence.

## APIs established by the installed stubs

The installed files under `D:\Codesys\CODESYS\ScriptLib\Stubs\scriptengine` expose:

| Object | Operation | Role |
|---|---|---|
| Device | `set_simulation_mode(True)` and `get_simulation_mode()` | Select and verify IDE simulation before online operations |
| `online` | `create_online_application(application)` | Create a disposable online application handle |
| Online application | `login(OnlineChangeOption.Never, False)` | Full code download to the verified simulator; do not delete unrelated applications |
| Online application | `start()`, `stop()`, `reset(ResetOption.Cold)` | Execute and initialize the isolated simulation fixture |
| Online application | `set_prepared_value(expression, text)`, `write_prepared_values()` | Write requested test inputs |
| Online application | `read_value()` and `read_values()` | Read actual monitored simulator values |
| Online application | `logout()` and `Dispose()` | Release the simulation session |

The [device API](https://content.helpme-codesys.com/en/ScriptingEngine/ScriptDeviceObject.html) owns simulation selection. It is not a writable property on the online application. The [online API](https://content.helpme-codesys.com/en/ScriptingEngine/ScriptOnline.html) provides the connection, monitoring, and state operations. Monitoring must be available for reads; failures remain explicit infrastructure failures.

## Why the prototype uses an acknowledgement gate

The installed scripting API contains an `ApplicationState.single_cycle` **state value**, but no documented `single_cycle()` invocation method. CODESYS does have a [Debug > Single Cycle command](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_cmd_single_cycle.html). The command requires an online halted application. Invoking menu commands with `system.commands[...].execute()` is an undocumented escape path, as identified in an [official CODESYS forum response](https://forge.codesys.com/forge/talk/Engineering/thread/cb4c263657/); a guessed GUID or token must not be presented as a verified single-scan API.

The prototype instead inserts this explicit wrapper in the existing task-called `PLC_PRG`:

```iecst
IF RequestSeq <> AckSeq THEN
    uut(x := TestInput);
    TestOutput := uut.y;
    CallCount := CallCount + 1;
    AckSeq := RequestSeq;
END_IF;
```

The simulator's cyclic task may run many times between host operations, but the function block is invoked exactly once for each new request sequence. The host first writes `TestInput` and reads it back, then writes the next sequence number. It waits until `AckSeq` matches and checks the actual output and `CallCount`. Thus ordinary host scheduling latency cannot silently create repeated FB invocations. This is a controlled **FB invocation** mechanism; it does not claim the entire application executes only one physical task cycle.

The initial handshake state must be zero after reset. All four actual acknowledgements and output comparisons must pass. A result's `actual_simulation` flag changes to true only after monitored reads have succeeded from the verified simulator. `execution_verified` changes to true only after all four steps pass. Local checks, compilation, or a process exit code cannot set those flags by themselves.

## Run after compiler validation

First establish the actual valid-invalid-repaired compiler fixtures. Then, with the compiler executable, exact profile, and frozen template configured, run:

```powershell
$env:PYTHONPATH = (Resolve-Path '.\src').Path
& 'C:\Users\田子佼\.conda\envs\Project1\python.exe' -X utf8 `
    '.\codesys\run_simulation_probe.py' --run-simulation
```

An optional `--config <local-compiler-config.json>` supplies nonsecret compiler configuration. The wrapper deliberately does not load an API key. It copies the frozen template to a fresh `results\raw\simulation_probe\<nonce>\simulation.project`. The embedded script refuses to modify the template, rejects a project or result file outside that workspace, verifies IDE simulation before login and subsequent online operations, and never configures a gateway or scans a network. It does not create a boot project or access physical PLC equipment.

The wrapper uses `codesys_command()` so profile and script path values are quoted in the form required by the actual Windows CODESYS command-line parser. It shares the serial compiler lock and saves the nonsecret invocation, template/script hashes, request, source fixture, project copy, stdout/stderr, and actual evidence. A timeout kills only the process tree launched for this fixture.

Read `result.json` and `simulation_evidence.json`. A PASS is valid only with matching nonce, normal process termination, `actual_simulation=true`, `execution_verified=true`, four passed steps, and actual monitored values. A login, compiler, monitoring, acknowledgement, or cleanup failure remains visible in the evidence. No missing evidence may be replaced with Python reference outputs.

## Extension limits

This gate can later support timer-free task traces, provided the complete interface, persistent IN_OUT bindings, reset behavior, and actual output comparisons are implemented. It cannot automatically validate the whole dataset merely because the BOOL fixture passes.

For TON and other clock-driven blocks, time elapses in the runtime between invocations. Host delays are not a deterministic PLC timer clock. A timing model, controlled cycle interval, or separately verified virtual-time path is required. The 500-hour runtime boundary and generic VARIANT FIFO remain separate challenges. Retained/persistent data need task-specific reset procedures; a cold reset does not promise to erase all persistent storage. Finite tests also do not prove unbounded LTL liveness.

Keep the simulation smoke's records outside E1-E4 metrics. Only executions of each generated candidate against the fixed task test cases can contribute to the benchmark's functional pass rates.
