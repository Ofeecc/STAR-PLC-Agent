# Public questions 1 through 10 specification review

The ten records preserve the teacher-supplied `en` strings without editing them. They cover all six easy tasks and the first four medium tasks in source order. They contain 70 temporal/state properties, 23 test cases and 133 scan observations. These are specifications and expected traces. None are CODESYS execution evidence.

Every actual FB parameter is recorded in `interface`. In PUB008 the source rows describing `channels[].fieldName` are element-field definitions rather than extra FB parameters; they are retained in the original requirements and normalized into `data_types`. PUB007 likewise records the required `ST_Pump` structure. Only fields marked written may be modified. The array tests explicitly include a case with different lower bounds.

## Scan and timer convention

Inputs are sampled at invocation, retained state is the state before that invocation, and outputs are observed after execution. An initial condition describes a fresh instance before its first scan. The first listed test step executes the FB and may therefore turn an output on. This avoids the assignment example's ambiguous delayed motor output.

For wall-clock timers, the first sampled eligible TRUE invocation has elapsed zero. `dt_ms` describes time since the previous invocation while previous sample values are held stable. Exact threshold tests use 4999 plus 1 ms or 2999 plus 1 ms. They require a controlled execution clock or appropriately tolerant actual timed sampling. They are not a claim that arbitrary desktop scheduling can reliably hit a 1 ms boundary. PUB004 separately accumulates caller-supplied CycleTime on scans whose final VFD_RUN is TRUE; this is an explicit interpretation of its source wording.

PUB004's maintenance test contains a 500-hour interval and the matching supplied CycleTime. It is a complete expected arithmetic trace but cannot be called a short live runtime test. A validated virtual clock would be needed to accelerate it; otherwise report that case as not executed. Its 1.8 billion milliseconds fit TIME's unsigned 32-bit duration, and its accumulator must use LTIME.

## Ambiguities resolved for repeatable evaluation

| Task | Evaluation choice | Reason |
|---|---|---|
| PUB001 | One active stage and at most one transition per scan; out-of-phase confirmations ignored | Prevents contradictory simultaneous actuators and skipping a physical stage |
| PUB002 | Previous DWORD starts at zero; first nonzero value counts as rising | Defines first invocation and all 32 bits consistently |
| PUB003 | Strict trigger/release inequalities; invalid settings preserve alarm values; range error first | Follows the source's strict wording and early-return requirement |
| PUB004 | E-stop clears completed as well as incomplete qualification | Prevents immediate restart with stale validity |
| PUB005 | Startup timer continues through E-stop; inhibition indication remains truthful | E-stop suppresses the alert but is not described as a new power-up |
| PUB006 | Start count increments in the scan that first outputs TRUE | Aligns counter with actual run transitions |
| PUB007 | Start selects and latches a set; stop overrides; lower pump index wins ties | Source does not specify tie-breaking or reselection timing |
| PUB008 | Disabled/skipped channels retain outputs; invalid-mode error before invalid-limit error; extrapolate raw values | Makes all unspecified branches explicit without adding new parameters |
| PUB009 | Warm-up mean uses observed samples; reset suppresses same-scan sampling; window change clears history | Avoids zero-padding and mixed-window ambiguities |
| PUB010 | Equality retains demand; protection trips at >=5 s; clears after >=3 s; faults do not reset active cooldown | Source says “more than” but also specifies a 5 s interval; the chosen boundary is stated visibly |

These are evaluation interpretations, not changes claimed to be present in the teacher's wording. A teacher clarification should update the assumptions, related properties and all affected expected steps together before paid benchmark runs.

## Scope of the temporal properties

Formulas use LTL operators over explicitly defined atomic predicates and integer/real/bitvector state relations. `forall` expressions are finite abbreviations that can be expanded into conjunctions. Arithmetic expressions and helper functions such as popcount and history mean are interpreted atomic predicates, not additional temporal operators. Canonical ghost state defines the specification independently of a generated implementation's variable names. Conditional liveness presumes advancing time and explicitly stated environmental fairness. Finite scan tests do not prove an unbounded LTL property.

Review checked source interface names, stop/fault priority, threshold equality, history reset, conditional liveness and long-duration overflow. Automated formal model checking remains unperformed. Public tasks with generic arrays, data types or PLC timer dependencies still require real CODESYS compilation and runtime review.
