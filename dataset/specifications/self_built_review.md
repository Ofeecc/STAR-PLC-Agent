# Self-built dataset consistency review

The twelve tasks were independently constructed for this project by choosing a practical teaching scenario, defining an explicit state transition and priority order, and writing fixed expected sequences. A separate Python implementation then checked those constants. This is an assistant consistency review, not a claim of human PLC expert approval or industrial safety certification. No external question source was copied.

The dataset contains 4 easy, 6 medium and 2 hard tasks. It covers a motor latch, neutral-scan reversing, restart inhibition, conveyor indexing, externally clocked signal phases, tank hysteresis, duty/standby selection, scan qualification, edge counting, alarm acknowledgment, actuator sequencing and bounded retry recovery. It has 75 LTL properties, 24 functional test cases and 142 end-of-scan observations.

| Task | Main distinction | Reviewed boundary or priority |
| --- | --- | --- |
| SELF001 | Guarded retained motor | Stop and open guard override Start; guard closing with Start held is explicitly allowed |
| SELF002 | Reversible jog drive | One neutral output scan before reversal; both buttons command neutral |
| SELF003 | Emergency-stop restart inhibition | Initial reset is required; Start and reset cannot take effect together |
| SELF004 | Pallet indexing | Jam wins over reset; fault/completion latch; Stop aborts non-fault cycles |
| SELF005 | Three-phase signal | 2/3/1 logical tick durations; paused clock; disable clears progress |
| SELF006 | Refill tank | Low and high thresholds create hysteresis; inconsistent sensors stop filling |
| SELF007 | Duty/standby pumps | Immediate healthy fallback; preference toggles only after an episode that served demand |
| SELF008 | Consecutive-scan qualification | Presets 1..5, invalid values, immediate trip and reduced threshold |
| SELF009 | Batch counter | Rising edges only; pulse memory updates during reset; target saturation |
| SELF010 | Latched panel alarm | New fault edge reannunciates before simultaneous acknowledgment; reset needs absent fault |
| SELF011 | Fixture handshakes | Home-qualified start; one transition per scan; DONE cannot restart without clear |
| SELF012 | Bounded fault retries | Two healthy WAIT scans; renewed fault clears dwell; two retries then lockout |

## Corrections made during review

The initial reference ST declared the internal restart-inhibition latch TRUE for SELF003 and the internal lead preference TRUE for SELF007, but left their observable VAR_OUTPUT values at the CODESYS default FALSE until the first invocation. That did not match the stated pre-invocation output initialization. `scripts/build_self_dataset.py` now emits explicit output initializers from the task's numeric and Boolean `initial_conditions`. The resulting examples initialize `ResetRequired := TRUE` and `LeadA := TRUE` before invocation. The default-false motor outputs and zero counters are also explicit when listed as initial output values.

The Python reference controller now constructs an explicit initial state per task instead of relying only on lazy dictionary defaults. This allows finite exploration to count canonical state encodings and makes reset semantics inspectable. No expected functional trace was changed to fit the implementation.

SELF004's fault-retention specification now includes an explicit weak-until expansion using standard `U`: the fault remains until a valid cleared-jam reset, or remains forever if the environment never resets it. Strong until alone would incorrectly require the operator eventually to reset.

## Reference checks and their limits

The fixed trace tests passed using `C:\Users\田子佼\.conda\envs\Project1\python.exe`. The review also independently states selected safety predicates and checks every transition reachable in the finite Python models. It covers all Boolean input valuations and the complete specified valid Preset/Target ranges with adjacent invalid boundaries. The exact state, transition and property evaluation counts are recorded by `scripts/check_reference.py` in `results/summary/reference_validation.json`; that generated file is the source for numerical review claims.

The reference ST bodies were inspected against the same requirements: state machines use one CASE branch per invocation; safety-priority branches precede normal transitions; every output is recomputed or deliberately retained; edge memories update even during resets; integer counters remain within their declared USINT/SINT bounds. The ST examples are hand-designed teaching references, not outputs from any benchmark model. They remain unverified CODESYS source until actual compilation and runtime logs exist. The Python exploration does not automatically establish ST/Python equivalence.

Only selected safety predicates are explored automatically. The full 75-property LTL set has not been submitted to an LTL model checker. In particular, recurring colors and eventual qualification are conditional infinite-trace statements; passing finite tests cannot prove them. Physical timing, mechanical interactions, asynchronous inputs, real emergency-stop circuits and certified safety functions are outside this educational dataset's model.

## Reproduction

From the project root in PowerShell:

```powershell
$env:PYTHONPATH = (Resolve-Path .\src).Path
$python = 'C:\Users\田子佼\.conda\envs\Project1\python.exe'
& $python -X utf8 .\scripts\build_self_dataset.py
& $python -X utf8 .\scripts\check_reference.py
& $python -X utf8 -m unittest discover -s tests -p test_reference.py -v
```

All reference checks are evidence type `PYTHON_REFERENCE_ONLY` and are excluded from PLC functional success metrics.
