# Discrete scan semantics and LTL interpretation

Every task is evaluated as a sequence of invocations of one function-block instance. A new instance is created before each test case. Test step 0 executes normally; it is not an extra initialization delay. The JSON `initial_conditions` describe the instance before that first invocation. Public-task interpretations are documented separately from the unchanged official requirement text.

## Inputs and outputs in one record

For invocation `k`, let `I[k]` be the input values sampled at the beginning of that invocation, `q[k]` its retained pre-state, and `O[k]` its outputs observed after execution. One invocation computes `q[k+1] = delta(q[k], I[k])` and `O[k] = lambda(q[k], I[k])`. Most reference examples store outputs in the retained variables, so an output assigned during invocation `k` is available as retained pre-state at invocation `k+1`.

Our LTL trace record is `T[k] = (I[k], q[k], O[k])`. Consequently:

- `G(stop -> !run)` says that a sampled stop suppresses the output at the end of that same invocation.
- `G((start & !stop) -> run)` says that a permitted start is visible at the end of that invocation.
- `qRun` is an explicitly defined proposition for the pre-scan latch, not the current end-of-scan output.
- `X` advances to the next invocation record. `G(Run -> X(Stop | !GuardClosed | Run))` permits a higher-priority input in the next scan to stop the motor.
- `first` is true only in the first invocation of a freshly reset test instance. An initialization statement about pre-state does not force the first output to remain unchanged when step 0 contains a start request.

Inputs are held fixed throughout each invocation. The logical model does not describe asynchronous hardware response within a scan, task preemption, contact bounce between samples, or the physical safety response of a certified safety PLC.

## Resolving the assignment motor example

The equations embedded in `Final project_ENGLISH.docx` are:

```text
G((StopBtn ∨ EStop) → X ¬Motor)
G((StartBtn ∧ ¬StopBtn ∧ ¬EStop) → X Motor)
```

The example table shows StartBtn TRUE and Motor FALSE in `state1`, then Motor TRUE in `state2` after StartBtn has returned FALSE. This is consistent with a *pre-scan* state sequence `S[k] = (I[k], q[k])`: the input in `state1` updates the motor latch appearing in `state2`. Under that representation, `X Motor` is the updated state. It need not mean that the physical PLC waits for an additional complete scan before updating its output.

Our dataset uses end-of-scan outputs in the same row as the sampled input. Its equivalent stop and start requirements therefore use same-record outputs:

```text
G((StopBtn | EStop) -> !Motor)
G((StartBtn & !StopBtn & !EStop) -> Motor)
```

This change is a declared change of observation convention. The two formula sets must not be evaluated on the same mixed trace and claimed equivalent. For example, Start at invocation `k` followed by Stop at `k+1` produces Motor TRUE then FALSE under our convention; blindly applying the assignment's `X Motor` to these end-of-scan observations would incorrectly reject the correct stop response.

## Formula notation

`G`, `F`, `X`, and `U` have their ordinary infinite-trace LTL meanings: globally, eventually, next, and strong until. `!`, `&`, `|`, `->`, and `<->` denote Boolean operations. Numeric comparisons, arithmetic expressions, array relationships, and names such as `oneColor`, `retryDue`, or `nextCount` abbreviate the state predicates defined in each task's `atomic_propositions`. They are not untyped new temporal operators. An eventual export to a model checker must translate these predicates into that tool's supported finite state or theory encoding.

Strong until `a U b` requires that `b` eventually occur and that `a` hold beforehand. A reset is not assumed to occur unless the task states that environmental assumption. SELF004 therefore expresses latched retention using the weak-until expansion `G Fault | (Fault U (!Jam & Reset))`: the fault may remain forever if no valid reset arrives. This expresses retention without adding an unintended liveness obligation on the operator.

SELF005's recurring-color property explicitly assumes persistent enable and infinitely many logical ticks. SELF008's eventual qualification property assumes every future invocation has a valid request, no trip and a valid preset. Without those assumptions, a persistent stop or absent clock can legitimately prevent progress. A finite passing test cannot establish either unbounded liveness property.

## Timing and test execution

All twelve SELF tasks intentionally use invocation counts or explicit logical ticks. SELF005's tick is an external enable for one logical tick per TRUE invocation, not a physical second or a rising-edge detector. SELF008 counts consecutive invocations. SELF012's recovery dwell is two healthy WAIT invocations, and a fault invocation clears its progress. `dt_ms` is unused by these self-built Python reference models.

Public tasks with TIME-based requirements need a real runtime clock or a separately validated clock-control mechanism. Their expected traces and time-boundary assumptions are documented per task. A wall-clock sleep performed by a host script, or a Python reference calculation, is not evidence that CODESYS timers executed at the expected instants. Runtime measurements must include the actual invocation interval and an agreed tolerance where required.

IN_OUT buffers and databases belong to the caller and must persist across steps. Supplying a complete input map in the test data does not authorize resetting caller storage on every invocation. Binding metadata, initial storage, per-step commands, and observed results must be handled separately in the runtime adapter.

## What has been verified

`scripts/check_reference.py` checks the fixed SELF expected traces against separate Python transition systems and explores selected safety predicates over their finite reachable state spaces. Boolean inputs are exhaustive; SELF008 presets 0 through 6 and SELF009 targets 0 through 21 cover all specified valid values plus adjacent invalid boundaries. Other invalid USINT values are represented by the same invalid branch and are not individually enumerated.

These results are labeled `PYTHON_REFERENCE_ONLY`. The script is not an ST interpreter or an LTL model checker. It neither executes generated code nor proves generated ST equivalent to the reference model. Its counts must never enter CODESYS compilation or PLC functional-test pass rates. The authoritative review output is `results/summary/reference_validation.json`.
