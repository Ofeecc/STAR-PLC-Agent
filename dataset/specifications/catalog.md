# Dataset source specifications and test catalog
This document is generated from the task JSON files. It records requirements, provenance, formal specifications and planned test expectations. It contains no actual CODESYS execution results.
Regenerate after a deliberate dataset revision with `python scripts/build_dataset_docs.py`, then prepare a new campaign when the frozen hash has changed.
| ID | Origin | Difficulty | Title | LTL properties | Cases | Scan observations |
| --- | --- | --- | --- | ---: | ---: | ---: |
| PUB001 | public | easy | Automated Filling Line Control | 12 | 7 | 91 |
| PUB002 | public | easy | Dual-Word Edge Detection | 8 | 7 | 39 |
| PUB003 | public | easy | Alarm Handling | 11 | 8 | 49 |
| PUB004 | public | easy | Jam Pump Debouncing and Runtime Maintenance | 9 | 8 | 55 |
| PUB005 | public | easy | Weld Gap Alarm and Startup Inhibition | 7 | 7 | 48 |
| PUB006 | public | easy | Aeration Blower Delayed Start | 7 | 7 | 58 |
| PUB007 | public | medium | Multi-Pump Switching Control System | 6 | 7 | 30 |
| PUB008 | public | medium | Analog Batch Processing | 9 | 9 | 12 |
| PUB009 | public | medium | Calculate Moving Average | 9 | 7 | 455 |
| PUB010 | public | medium | Temperature Logic Control | 13 | 8 | 54 |
| PUB011 | public | medium | Automated Production Line Control | 9 | 8 | 82 |
| PUB012 | public | medium | Slab Thickness Alarm and Fault History | 8 | 8 | 70 |
| PUB013 | public | medium | Office HVAC Multi-mode Energy-Saving Control | 8 | 12 | 80 |
| PUB014 | public | medium | IPv4 Parsing with Format and Range Checks | 5 | 8 | 61 |
| PUB015 | public | hard | Material Proportioning Process Control | 10 | 13 | 127 |
| PUB016 | public | hard | Flexible Processing Control | 9 | 8 | 160 |
| PUB017 | public | hard | Recipe Management System | 9 | 8 | 157 |
| PUB018 | public | hard | FIFO First-In-First-Out Queue | 8 | 9 | 140 |
| PUB019 | public | hard | Mechanical Arm Control | 12 | 17 | 306 |
| PUB020 | public | hard | Production Control | 12 | 11 | 156 |
| SELF001 | self_built | easy | Guarded motor with retained run command | 7 | 7 | 39 |
| SELF002 | self_built | medium | Reversing jog drive with a neutral scan | 8 | 7 | 44 |
| SELF003 | self_built | medium | Emergency stop reset with restart inhibition | 10 | 10 | 62 |
| SELF004 | self_built | medium | Pallet indexing with a latched jam fault | 11 | 9 | 61 |
| SELF005 | self_built | medium | Three phase signal with externally clocked durations | 11 | 7 | 66 |
| SELF006 | self_built | easy | Tank filling with hysteresis and sensor inconsistency | 7 | 7 | 39 |
| SELF007 | self_built | medium | Duty standby alternation with healthy pump fallback | 11 | 9 | 60 |
| SELF008 | self_built | easy | Consecutive scan qualification with an immediate trip | 7 | 7 | 45 |
| SELF009 | self_built | easy | Rising edge batch counter with reset sampling | 7 | 7 | 56 |
| SELF010 | self_built | medium | Latched alarm with acknowledgment and reannunciation | 10 | 8 | 50 |
| SELF011 | self_built | hard | Single cycle actuator handshakes with one transition per scan | 13 | 12 | 148 |
| SELF012 | self_built | hard | Bounded automatic fault retries with a recovery dwell | 11 | 9 | 94 |

## PUB001 Automated Filling Line Control

Origin: public. Difficulty: easy.

### Source and adaptation

```json
{
  "source_type": "official_course_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": {
    "group": "easy",
    "index_1based": 1
  },
  "adaptation": "Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.",
  "rationale": "Teacher-supplied PLC task; retains the specified interface and control scenario.",
  "review": "Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC."
}
```

### Natural language source

# Automated Filling Line Control

- **Difficulty:** Easy (easy)

## Requirements

An automated filling line responsible for cleaning, filling, capping, and packaging bottles. Each step of the production line is controlled by PLC and triggered by signals from sensors and operators.
Control requirements:
When the sensor bottleSensor detects a bottle, it triggers the start of the cleaning pump and continues to work.
After cleaning is completed, the operator operates the button cleaningConfirmButton to trigger the cleaning completion signal, automatically starting the filling valve for filling.
After filling is completed, the operator operates the button fillingConfirmButton to trigger the filling completion signal, automatically starting the capping machine for capping.
After capping is completed, the operator operates the button cappingConfirmButton to trigger the capping completion signal, starting the packing machine for packaging.
After packaging is completed, the operator operates the button packingConfirmButton to trigger the packaging completion signal, lighting up the packaging completion indicator light.
After the operator picks up the packaged bottle, they press the confirmation button finishedButton to reset the indicator light and prepare for the next bottle's production cycle.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `bottleSensor` | `BOOL` | The bottle reaches the sensor, triggering a signal when a bottle is detected |
| Input | `cleaningConfirmButton` | `BOOL` | Operator confirmation button, used to confirm the completion of the cleaning process |
| Input | `fillingConfirmButton` | `BOOL` | Operator confirmation button, used to confirm the completion of the filling process |
| Input | `cappingConfirmButton` | `BOOL` | Operator confirmation button, used to confirm the completion of the capping process |
| Input | `packingConfirmButton` | `BOOL` | Operator confirmation button, used to confirm the completion of the packaging process |
| Input | `finishedButton` | `BOOL` | Operator confirmation button, used to confirm that the bottle has been picked up |
| Output | `Pump_Motor` | `BOOL` | Control output for the operation of the cleaning pump motor |
| Output | `Filling_Valve` | `BOOL` | Control output for the operation of the filling valve |
| Output | `Capping_Machine` | `BOOL` | Control output for the operation of the capping machine |
| Output | `Packing_Machine` | `BOOL` | Control output for the operation of the packing machine |
| Output | `Completion_Light` | `BOOL` | Indicator light for packaging completion |

### Scenario

An automated filling line responsible for cleaning, filling, capping, and packaging bottles. Each step of the production line is controlled by PLC and triggered by signals from sensors and operators.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | bottleSensor | BOOL | The bottle reaches the sensor, triggering a signal when a bottle is detected |
| INPUT | cleaningConfirmButton | BOOL | Operator confirmation button, used to confirm the completion of the cleaning process |
| INPUT | fillingConfirmButton | BOOL | Operator confirmation button, used to confirm the completion of the filling process |
| INPUT | cappingConfirmButton | BOOL | Operator confirmation button, used to confirm the completion of the capping process |
| INPUT | packingConfirmButton | BOOL | Operator confirmation button, used to confirm the completion of the packaging process |
| INPUT | finishedButton | BOOL | Operator confirmation button, used to confirm that the bottle has been picked up |
| OUTPUT | Pump_Motor | BOOL | Control output for the operation of the cleaning pump motor |
| OUTPUT | Filling_Valve | BOOL | Control output for the operation of the filling valve |
| OUTPUT | Capping_Machine | BOOL | Control output for the operation of the capping machine |
| OUTPUT | Packing_Machine | BOOL | Control output for the operation of the packing machine |
| OUTPUT | Completion_Light | BOOL | Indicator light for packaging completion |

### Initial conditions

```json
{
  "phase": 0,
  "Pump_Motor": false,
  "Filling_Valve": false,
  "Capping_Machine": false,
  "Packing_Machine": false,
  "Completion_Light": false
}
```

### Scan semantics

At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

### Safety and priorities

- Active phase restricts which confirmation can be accepted.
- Only the current phase actuator may run.

### Explicit assumptions

- The five process actuators are mutually exclusive; each completed phase switches off its actuator when the next starts.
- One phase transition at most is allowed per scan. Confirmation signals outside their active phase are ignored.
- Confirmation inputs are level sampled. A held confirmation can complete its relevant phase on a later scan, but cannot skip several phases in one scan.
- finishedButton resets only the completed phase. A bottle still present can start a new cleaning cycle on the following idle scan.
- For the progress property, future confirmations are ordered and sustained until their matching phase accepts them. Unordered one-scan pulses do not imply completion.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `phase`: Spre.phase (0..5); phase at the next LTL position is this scan's Spost.phase
- `oneHotOutputs`: sum(int(O[k][n]) for n in [Pump_Motor,Filling_Valve,Capping_Machine,Packing_Machine,Completion_Light]) <= 1
- `init`: At the separate pre-invocation initial observation: Spre.phase=0 AND each actual listed initial output is FALSE
- `all variable names`: The identically named sampled input or end-of-scan output in interface.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB001(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
参考阶段q初值0。事件按q选bottleSensor、cleaningConfirmButton、fillingConfirmButton、cappingConfirmButton、packingConfirmButton、finishedButton；选中事件真则qAfter=(q+1)%6，否则qAfter=q。五个期望输出依次为qAfter=1、2、3、4、5，每拍只选择旧q的一个分支。
- `bottleSensor`: I[k].bottleSensor: sampled input (BOOL).
- `cleaningConfirmButton`: I[k].cleaningConfirmButton: sampled input (BOOL).
- `fillingConfirmButton`: I[k].fillingConfirmButton: sampled input (BOOL).
- `cappingConfirmButton`: I[k].cappingConfirmButton: sampled input (BOOL).
- `packingConfirmButton`: I[k].packingConfirmButton: sampled input (BOOL).
- `finishedButton`: I[k].finishedButton: sampled input (BOOL).
- `Pump_Motor`: O[k].Pump_Motor: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Filling_Valve`: O[k].Filling_Valve: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Capping_Machine`: O[k].Capping_Machine: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Packing_Machine`: O[k].Packing_Machine: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Completion_Light`: O[k].Completion_Light: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `phase0_idle`: phase=0

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Pump_Motor": false,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB001",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB001'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Capping_Machine",
    "Completion_Light",
    "Filling_Valve",
    "Packing_Machine",
    "Pump_Motor"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "phase": {
      "pre": "Spre.phase",
      "post": "Spost.phase",
      "enum": {
        "0": "IDLE",
        "1": "CLEANING",
        "2": "FILLING",
        "3": "CAPPING",
        "4": "PACKING",
        "5": "COMPLETE"
      },
      "initial": 0
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The five process actuators are mutually exclusive; each completed phase switches off its actuator when the next starts.",
    "One phase transition at most is allowed per scan. Confirmation signals outside their active phase are ignored.",
    "Confirmation inputs are level sampled. A held confirmation can complete its relevant phase on a later scan, but cannot skip several phases in one scan.",
    "finishedButton resets only the completed phase. A bottle still present can start a new cleaning cycle on the following idle scan.",
    "For the progress property, future confirmations are ordered and sustained until their matching phase accepts them. Unordered one-scan pulses do not imply completion.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "参考阶段q初值0。事件按q选bottleSensor、cleaningConfirmButton、fillingConfirmButton、cappingConfirmButton、packingConfirmButton、finishedButton；选中事件真则qAfter=(q+1)%6，否则qAfter=q。五个期望输出依次为qAfter=1、2、3、4、5，每拍只选择旧q的一个分支。"
}
```

**P1**

```text
init
```

A fresh instance is idle with outputs off before first execution.

**P2**

```text
G(oneHotOutputs)
```

No two processing stages are energized together.

**P3**

```text
G((phase=0 & bottleSensor) -> (Pump_Motor & X(phase=1)))
```

Bottle detection starts cleaning in the same scan.

**P4**

```text
G((phase=1 & cleaningConfirmButton) -> (Filling_Valve & X(phase=2)))
```

A phase-specific confirmation advances exactly one stage.

**P5**

```text
G((phase=2 & fillingConfirmButton) -> (Capping_Machine & X(phase=3)))
```

A phase-specific confirmation advances exactly one stage.

**P6**

```text
G((phase=3 & cappingConfirmButton) -> (Packing_Machine & X(phase=4)))
```

A phase-specific confirmation advances exactly one stage.

**P7**

```text
G((phase=4 & packingConfirmButton) -> (Completion_Light & X(phase=5)))
```

A phase-specific confirmation advances exactly one stage.

**P8**

```text
G((phase=5 & !finishedButton) -> (Completion_Light & X(phase=5)))
```

Completion persists until pickup is confirmed.

**P9**

```text
G((phase=5 & finishedButton) -> (!Completion_Light & X(phase=0)))
```

On finishedButton during completion, clear Completion_Light and return to IDLE.

**P10**

```text
G((phase=1 & G((phase=1) -> F(cleaningConfirmButton)) & G((phase=2) -> F(fillingConfirmButton)) & G((phase=3) -> F(cappingConfirmButton)) & G((phase=4) -> F(packingConfirmButton))) -> F(Completion_Light))
```

Conditional progress: from cleaning, if every active phase eventually receives its matching confirmation, completion eventually occurs.

**P11**

```text
G(((phase=0 & !bottleSensor) -> (!Pump_Motor & !Filling_Valve & !Capping_Machine & !Packing_Machine & !Completion_Light & X(phase=0))) & ((phase=1 & !cleaningConfirmButton) -> (Pump_Motor & !Filling_Valve & !Capping_Machine & !Packing_Machine & !Completion_Light & X(phase=1))) & ((phase=2 & !fillingConfirmButton) -> (!Pump_Motor & Filling_Valve & !Capping_Machine & !Packing_Machine & !Completion_Light & X(phase=2))) & ((phase=3 & !cappingConfirmButton) -> (!Pump_Motor & !Filling_Valve & Capping_Machine & !Packing_Machine & !Completion_Light & X(phase=3))) & ((phase=4 & !packingConfirmButton) -> (!Pump_Motor & !Filling_Valve & !Capping_Machine & Packing_Machine & !Completion_Light & X(phase=4))) & ((phase=5 & finishedButton) -> (!Pump_Motor & !Filling_Valve & !Capping_Machine & !Packing_Machine & !Completion_Light & X(phase=0))))
```

Closes the unconfirmed phase-hold and finish-clearing obligations left implicit by P3..P9.

**PUB001.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Full bottle cycle and stable completion | 10 |
| T2 | Out-of-order confirmations cannot skip phases | 6 |
| PUB001.T3 | PUB001.T3 | 16 |
| PUB001.R22.filling_hold | 灌装阶段无完成确认时仍应保持阀门开启 | 5 |
| PUB001.R22.dwell_0 | 原流程各稳定状态连续保持：T1 | 30 |
| PUB001.R22.dwell_1 | 原流程各稳定状态连续保持：T2 | 14 |
| PUB001.T4 | Two-cycle restart isolation: finishedButton resets to idle even while bottleSensor is held high, then next idle scan restarts Cycle 2. | 10 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB002 Dual-Word Edge Detection

Origin: public. Difficulty: easy.

### Source and adaptation

```json
{
  "source_type": "official_course_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": {
    "group": "easy",
    "index_1based": 2
  },
  "adaptation": "Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.",
  "rationale": "Teacher-supplied PLC task; retains the specified interface and control scenario.",
  "review": "Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC."
}
```

### Natural language source

# Dual-Word Edge Detection

- **Difficulty:** Easy (easy)

## Requirements

Write a function block FB that checks for rising and falling edges in each bit of a dual-word (DWord) input value every cycle. The function block should be able to detect and report changes, rising edges, and falling edges in the input value.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `value` | `DWORD` | The input value to be checked for changes and edge triggering |
| Output | `hasChanged` | `BOOL` | True indicates that the input value has changed |
| Output | `hasRisingEdges` | `BOOL` | True indicates that rising edges have occurred in the input value |
| Output | `risingBits` | `DWORD` | The bit stream of rising edges, where each bit indicates whether the corresponding input bit has experienced a rising edge (1 for a rising edge, 0 for no rising edge) |
| Output | `noOfRisingBits` | `USINT` | The number of rising edges in the input value |
| Output | `hasFallingEdges` | `BOOL` | True indicates that falling edges have occurred in the input value |
| Output | `fallingBits` | `DWORD` | The bit stream of falling edges, where each bit indicates whether the corresponding input bit has experienced a falling edge (1 for a falling edge, 0 for no falling edge) |
| Output | `noOfFallingBits` | `USINT` | The number of falling edges in the input value |

### Scenario

Write a function block FB that checks for rising and falling edges in each bit of a dual-word (DWord) input value every cycle. The function block should be able to detect and report changes, rising edges, and falling edges in the input value.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | value | DWORD | The input value to be checked for changes and edge triggering |
| OUTPUT | hasChanged | BOOL | True indicates that the input value has changed |
| OUTPUT | hasRisingEdges | BOOL | True indicates that rising edges have occurred in the input value |
| OUTPUT | risingBits | DWORD | The bit stream of rising edges, where each bit indicates whether the corresponding input bit has experienced a rising edge (1 for a rising edge, 0 for no rising edge) |
| OUTPUT | noOfRisingBits | USINT | The number of rising edges in the input value |
| OUTPUT | hasFallingEdges | BOOL | True indicates that falling edges have occurred in the input value |
| OUTPUT | fallingBits | DWORD | The bit stream of falling edges, where each bit indicates whether the corresponding input bit has experienced a falling edge (1 for a falling edge, 0 for no falling edge) |
| OUTPUT | noOfFallingBits | USINT | The number of falling edges in the input value |

### Initial conditions

```json
{
  "previousValue": 0,
  "risingBits": 0,
  "fallingBits": 0,
  "noOfRisingBits": 0,
  "noOfFallingBits": 0,
  "hasChanged": false,
  "hasRisingEdges": false,
  "hasFallingEdges": false
}
```

### Scan semantics

At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

### Safety and priorities

- Previous value is updated after calculating both edge masks.

### Explicit assumptions

- The previous DWORD is initialized to DWORD#0. Therefore nonzero bits on the first scan count as rising edges.
- Bitwise complement is restricted to 32 bits; counts range from 0 through 32.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `prev`: {"kind": "previous_sampled_input", "source": "I[k-1].value", "initial": 0, "update": "After EVERY scan k, including invalid/reset/stop, store I[k].value"}
- `risingBits`: O[k].risingBits: independently observed post-scan candidate value (DWORD); never defined as expected output.
- `fallingBits`: O[k].fallingBits: independently observed post-scan candidate value (DWORD); never defined as expected output.
- `popcount`: Number of set bits in the unsigned 32-bit argument.
- `other interface names`: Identically named sampled inputs or observed outputs.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB002(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
prev初值DWORD#0。rise=value & (~prev & 0xFFFFFFFF)，fall=prev & (~value & 0xFFFFFFFF)。两个掩码、popcount、掩码非零标志和value!=prev标志分别与实际七个输出比较；prevAfter=value，每次调用更新一次。
- `ValueBit0`: Boolean ((I[k].value >> 0) & 1) = 1, unsigned DWORD width 32.
- `PrevBit0`: Boolean ((inputMemory.prev[k] >> 0) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit1`: Boolean ((I[k].value >> 1) & 1) = 1, unsigned DWORD width 32.
- `PrevBit1`: Boolean ((inputMemory.prev[k] >> 1) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit2`: Boolean ((I[k].value >> 2) & 1) = 1, unsigned DWORD width 32.
- `PrevBit2`: Boolean ((inputMemory.prev[k] >> 2) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit3`: Boolean ((I[k].value >> 3) & 1) = 1, unsigned DWORD width 32.
- `PrevBit3`: Boolean ((inputMemory.prev[k] >> 3) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit4`: Boolean ((I[k].value >> 4) & 1) = 1, unsigned DWORD width 32.
- `PrevBit4`: Boolean ((inputMemory.prev[k] >> 4) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit5`: Boolean ((I[k].value >> 5) & 1) = 1, unsigned DWORD width 32.
- `PrevBit5`: Boolean ((inputMemory.prev[k] >> 5) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit6`: Boolean ((I[k].value >> 6) & 1) = 1, unsigned DWORD width 32.
- `PrevBit6`: Boolean ((inputMemory.prev[k] >> 6) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit7`: Boolean ((I[k].value >> 7) & 1) = 1, unsigned DWORD width 32.
- `PrevBit7`: Boolean ((inputMemory.prev[k] >> 7) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit8`: Boolean ((I[k].value >> 8) & 1) = 1, unsigned DWORD width 32.
- `PrevBit8`: Boolean ((inputMemory.prev[k] >> 8) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit9`: Boolean ((I[k].value >> 9) & 1) = 1, unsigned DWORD width 32.
- `PrevBit9`: Boolean ((inputMemory.prev[k] >> 9) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit10`: Boolean ((I[k].value >> 10) & 1) = 1, unsigned DWORD width 32.
- `PrevBit10`: Boolean ((inputMemory.prev[k] >> 10) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit11`: Boolean ((I[k].value >> 11) & 1) = 1, unsigned DWORD width 32.
- `PrevBit11`: Boolean ((inputMemory.prev[k] >> 11) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit12`: Boolean ((I[k].value >> 12) & 1) = 1, unsigned DWORD width 32.
- `PrevBit12`: Boolean ((inputMemory.prev[k] >> 12) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit13`: Boolean ((I[k].value >> 13) & 1) = 1, unsigned DWORD width 32.
- `PrevBit13`: Boolean ((inputMemory.prev[k] >> 13) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit14`: Boolean ((I[k].value >> 14) & 1) = 1, unsigned DWORD width 32.
- `PrevBit14`: Boolean ((inputMemory.prev[k] >> 14) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit15`: Boolean ((I[k].value >> 15) & 1) = 1, unsigned DWORD width 32.
- `PrevBit15`: Boolean ((inputMemory.prev[k] >> 15) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit16`: Boolean ((I[k].value >> 16) & 1) = 1, unsigned DWORD width 32.
- `PrevBit16`: Boolean ((inputMemory.prev[k] >> 16) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit17`: Boolean ((I[k].value >> 17) & 1) = 1, unsigned DWORD width 32.
- `PrevBit17`: Boolean ((inputMemory.prev[k] >> 17) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit18`: Boolean ((I[k].value >> 18) & 1) = 1, unsigned DWORD width 32.
- `PrevBit18`: Boolean ((inputMemory.prev[k] >> 18) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit19`: Boolean ((I[k].value >> 19) & 1) = 1, unsigned DWORD width 32.
- `PrevBit19`: Boolean ((inputMemory.prev[k] >> 19) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit20`: Boolean ((I[k].value >> 20) & 1) = 1, unsigned DWORD width 32.
- `PrevBit20`: Boolean ((inputMemory.prev[k] >> 20) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit21`: Boolean ((I[k].value >> 21) & 1) = 1, unsigned DWORD width 32.
- `PrevBit21`: Boolean ((inputMemory.prev[k] >> 21) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit22`: Boolean ((I[k].value >> 22) & 1) = 1, unsigned DWORD width 32.
- `PrevBit22`: Boolean ((inputMemory.prev[k] >> 22) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit23`: Boolean ((I[k].value >> 23) & 1) = 1, unsigned DWORD width 32.
- `PrevBit23`: Boolean ((inputMemory.prev[k] >> 23) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit24`: Boolean ((I[k].value >> 24) & 1) = 1, unsigned DWORD width 32.
- `PrevBit24`: Boolean ((inputMemory.prev[k] >> 24) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit25`: Boolean ((I[k].value >> 25) & 1) = 1, unsigned DWORD width 32.
- `PrevBit25`: Boolean ((inputMemory.prev[k] >> 25) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit26`: Boolean ((I[k].value >> 26) & 1) = 1, unsigned DWORD width 32.
- `PrevBit26`: Boolean ((inputMemory.prev[k] >> 26) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit27`: Boolean ((I[k].value >> 27) & 1) = 1, unsigned DWORD width 32.
- `PrevBit27`: Boolean ((inputMemory.prev[k] >> 27) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit28`: Boolean ((I[k].value >> 28) & 1) = 1, unsigned DWORD width 32.
- `PrevBit28`: Boolean ((inputMemory.prev[k] >> 28) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit29`: Boolean ((I[k].value >> 29) & 1) = 1, unsigned DWORD width 32.
- `PrevBit29`: Boolean ((inputMemory.prev[k] >> 29) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit30`: Boolean ((I[k].value >> 30) & 1) = 1, unsigned DWORD width 32.
- `PrevBit30`: Boolean ((inputMemory.prev[k] >> 30) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `ValueBit31`: Boolean ((I[k].value >> 31) & 1) = 1, unsigned DWORD width 32.
- `PrevBit31`: Boolean ((inputMemory.prev[k] >> 31) & 1) = 1; prev[0]=0; prev[k+1]=I[k].value.
- `value`: I[k].value: sampled input (DWORD).
- `hasChanged`: O[k].hasChanged: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `hasRisingEdges`: O[k].hasRisingEdges: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `noOfRisingBits`: O[k].noOfRisingBits: independently observed post-scan candidate value (USINT); never defined as expected output.
- `hasFallingEdges`: O[k].hasFallingEdges: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `noOfFallingBits`: O[k].noOfFallingBits: independently observed post-scan candidate value (USINT); never defined as expected output.
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.hasChanged=false, O_init.hasRisingEdges=false, O_init.risingBits=0, O_init.noOfRisingBits=0, O_init.hasFallingEdges=false, O_init.fallingBits=0, O_init.noOfFallingBits=0.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "risingBits": 0,
    "fallingBits": 0,
    "noOfRisingBits": 0,
    "noOfFallingBits": 0,
    "hasChanged": false,
    "hasRisingEdges": false,
    "hasFallingEdges": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB002",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": {
        "class": "DataContract",
        "state": {
          "task_id": "PUB002",
          "previous": 0,
          "high": false,
          "low": false,
          "trigger": false,
          "window": null,
          "history": [],
          "average": 0.0,
          "reached": false,
          "recipes": [
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            }
          ],
          "last_query": {
            "recipeID": 0,
            "ingredientType": 0,
            "ingredientRatio": 0.0,
            "productionTemperature": 0.0
          },
          "prev_add": false,
          "prev_delete": false,
          "prev_modify": false,
          "prev_query": false,
          "recipes_initialized": false,
          "queue": [],
          "prev_enq": false,
          "prev_deq": false
        }
      },
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB002'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "fallingBits",
    "hasChanged",
    "hasFallingEdges",
    "hasRisingEdges",
    "noOfFallingBits",
    "noOfRisingBits",
    "risingBits"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "prev": {
      "kind": "previous_sampled_input",
      "source": "I[k-1].value",
      "initial": 0,
      "update": "After EVERY scan k, including invalid/reset/stop, store I[k].value"
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The previous DWORD is initialized to DWORD#0. Therefore nonzero bits on the first scan count as rising edges.",
    "Bitwise complement is restricted to 32 bits; counts range from 0 through 32.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "prev初值DWORD#0。rise=value & (~prev & 0xFFFFFFFF)，fall=prev & (~value & 0xFFFFFFFF)。两个掩码、popcount、掩码非零标志和value!=prev标志分别与实际七个输出比较；prevAfter=value，每次调用更新一次。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(risingBits = (value AND NOT prev))
```

The rising mask identifies only 0-to-1 bits.

**P2**

```text
G(fallingBits = (prev AND NOT value))
```

The falling mask identifies only 1-to-0 bits.

**P3**

```text
G((risingBits AND fallingBits)=0)
```

A bit cannot rise and fall in one scan.

**P4**

```text
G((noOfRisingBits=popcount(risingBits)) & (noOfFallingBits=popcount(fallingBits)))
```

Both counts equal their mask population.

**P5**

```text
G((hasRisingEdges <-> risingBits<>0) & (hasFallingEdges <-> fallingBits<>0) & (hasChanged <-> value<>prev))
```

Flags match masks and value changes.

**P6**

```text
G((ValueBit0 <-> X(PrevBit0)) & (ValueBit1 <-> X(PrevBit1)) & (ValueBit2 <-> X(PrevBit2)) & (ValueBit3 <-> X(PrevBit3)) & (ValueBit4 <-> X(PrevBit4)) & (ValueBit5 <-> X(PrevBit5)) & (ValueBit6 <-> X(PrevBit6)) & (ValueBit7 <-> X(PrevBit7)) & (ValueBit8 <-> X(PrevBit8)) & (ValueBit9 <-> X(PrevBit9)) & (ValueBit10 <-> X(PrevBit10)) & (ValueBit11 <-> X(PrevBit11)) & (ValueBit12 <-> X(PrevBit12)) & (ValueBit13 <-> X(PrevBit13)) & (ValueBit14 <-> X(PrevBit14)) & (ValueBit15 <-> X(PrevBit15)) & (ValueBit16 <-> X(PrevBit16)) & (ValueBit17 <-> X(PrevBit17)) & (ValueBit18 <-> X(PrevBit18)) & (ValueBit19 <-> X(PrevBit19)) & (ValueBit20 <-> X(PrevBit20)) & (ValueBit21 <-> X(PrevBit21)) & (ValueBit22 <-> X(PrevBit22)) & (ValueBit23 <-> X(PrevBit23)) & (ValueBit24 <-> X(PrevBit24)) & (ValueBit25 <-> X(PrevBit25)) & (ValueBit26 <-> X(PrevBit26)) & (ValueBit27 <-> X(PrevBit27)) & (ValueBit28 <-> X(PrevBit28)) & (ValueBit29 <-> X(PrevBit29)) & (ValueBit30 <-> X(PrevBit30)) & (ValueBit31 <-> X(PrevBit31)))
```

For every bit b=0..31, the next sampled-input memory bit equals the current value bit. X applies only to a Boolean proposition; memory is initialized to DWORD#0.

**PUB002.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | No change, mixed edges, full width and bit 31 | 10 |
| T2 | First nonzero invocation is compared with initialized zero | 2 |
| V2_data_contract_boundaries | Independently calculated edge/history/parser boundary regression | 2 |
| PUB002.T3 | PUB002.T3 | 6 |
| PUB002.R22.isolated_bits | 第2位与第4位独立变化、混合沿后保持 | 8 |
| PUB002.T4 | 16-bit half-word swaps and full 32-bit complementary bit flips with consecutive zero-edge hold. | 6 |
| PUB002.T5 | All-ones saturation followed by checkerboard parity inversions (0xAAAAAAAA <-> 0x55555555) and clear. | 5 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB003 Alarm Handling

Origin: public. Difficulty: easy.

### Source and adaptation

```json
{
  "source_type": "official_course_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": {
    "group": "easy",
    "index_1based": 3
  },
  "adaptation": "Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.",
  "rationale": "Teacher-supplied PLC task; retains the specified interface and control scenario.",
  "review": "Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC."
}
```

### Natural language source

# Alarm Handling

- **Difficulty:** Easy (easy)

## Requirements

In industrial automation systems, monitoring the status of equipment is crucial. When equipment parameters exceed the normal range, the system needs to issue an alarm. To avoid frequent triggering of alarms due to minor fluctuations in parameters, an alarm management system with hysteresis function needs to be implemented.
When Value is greater than hiLevel, trigger high alarm hiAlarm.
When Value is less than hiLevel-hystWindow, exit high alarm hiAlarm.
When Value is less than loLevel, trigger low alarm loAlarm.
When Value is greater than loLevel+hystWindow, exit low alarm loAlarm.
If loLevel is greater than or equal to hiLevel, output error error=true, status=16#8001, and exit the program
If the hysteresis window value hystWindow is greater than or equal to the deviation range between hiLevel and loLevel, output error error=true, status=16#8002

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `Value` | `REAL` | Input value |
| Input | `hiLevel` | `REAL` | High limit alarm value |
| Input | `loLevel` | `REAL` | Low limit alarm value |
| Input | `hystWindow` | `REAL` | Hysteresis window |
| Output | `hiAlarm` | `BOOL` | High limit alarm |
| Output | `loAlarm` | `BOOL` | Low limit alarm |
| Output | `error` | `BOOL` | FALSE: No error occurred;<br>TRUE: Error occurred during execution of FB |
| Output | `status` | `WORD` | Status code |

### Scenario

In industrial automation systems, monitoring the status of equipment is crucial. When equipment parameters exceed the normal range, the system needs to issue an alarm. To avoid frequent triggering of alarms due to minor fluctuations in parameters, an alarm management system with hysteresis function needs to be implemented.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Value | REAL | Input value |
| INPUT | hiLevel | REAL | High limit alarm value |
| INPUT | loLevel | REAL | Low limit alarm value |
| INPUT | hystWindow | REAL | Hysteresis window |
| OUTPUT | hiAlarm | BOOL | High limit alarm |
| OUTPUT | loAlarm | BOOL | Low limit alarm |
| OUTPUT | error | BOOL | FALSE: No error occurred;<br>TRUE: Error occurred during execution of FB |
| OUTPUT | status | WORD | Status code |

### Initial conditions

```json
{
  "hiAlarm": false,
  "loAlarm": false,
  "error": false,
  "status": 0
}
```

### Scan semantics

At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

### Safety and priorities

- Invalid range is diagnosed before invalid hysteresis width.
- No alarm update is allowed in an invalid-configuration scan.

### Explicit assumptions

- Threshold comparisons are strict as written. Equality with trigger or release thresholds retains the previous alarm value.
- Invalid configuration returns early, preserving alarm outputs. error and status are recalculated each scan; valid configuration clears them.
- loLevel>=hiLevel takes priority over the hysteresis-width error. hystWindow is assumed nonnegative; negative values are outside the defined input domain.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.
- All REAL inputs (value, loLevel, hiLevel, hystWindow) and reference threshold arithmetic (real32(hi-lo), real32(hi-width), real32(lo+width)) use IEEE 754 binary32 (REAL) rounding.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `badRange`: loLevel >= hiLevel
- `badWindow`: real32(I.hystWindow)>=Span
- `valid`: !badRange & !badWindow & hystWindow>=0
- `hiPrev`: {"kind": "previous_observed_output", "source": "O[k-1].hiAlarm", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].hiAlarm; never write into reference state."}
- `loPrev`: {"kind": "previous_observed_output", "source": "O[k-1].loAlarm", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].loAlarm; never write into reference state."}
- `sameAlarms`: hiAlarm=hiPrev & loAlarm=loPrev
- `interface names`: Identically named sampled input or observed output.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB003(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
四个REAL参数先按IEEE binary32舍入且有限，hystWindow>=0。lo>=hi时报8001，否则width>=real32(hi-lo)时报8002；错误时参考高低报警保持。有效时高报警由value>hi置真、value<real32(hi-width)置假、其余保持；低报警由value<lo置真、value>real32(lo+width)置假、其余保持。初值均FALSE。
- `Value`: I[k].Value: sampled input (REAL).
- `hiLevel`: I[k].hiLevel: sampled input (REAL).
- `loLevel`: I[k].loLevel: sampled input (REAL).
- `hystWindow`: I[k].hystWindow: sampled input (REAL).
- `hiAlarm`: O[k].hiAlarm: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `loAlarm`: O[k].loAlarm: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `error`: O[k].error: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `status`: O[k].status: independently observed post-scan candidate value (WORD); never defined as expected output.
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.hiAlarm=false, O_init.loAlarm=false, O_init.error=false, O_init.status=0.
- `HighRelease`: real32(real32(I.hiLevel)-real32(I.hystWindow))
- `LowRelease`: real32(real32(I.loLevel)+real32(I.hystWindow))
- `Span`: real32(real32(I.hiLevel)-real32(I.loLevel))
- `real32`: IEEE754 binary32 rounding to nearest ties-to-even; finite declared domain. All REAL input symbols denote binary32 sampled values.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "hiAlarm": false,
    "loAlarm": false,
    "error": false,
    "status": 0
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB003",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": {
        "class": "DataContract",
        "state": {
          "task_id": "PUB003",
          "previous": 0,
          "high": false,
          "low": false,
          "trigger": false,
          "window": null,
          "history": [],
          "average": 0.0,
          "reached": false,
          "recipes": [
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            }
          ],
          "last_query": {
            "recipeID": 0,
            "ingredientType": 0,
            "ingredientRatio": 0.0,
            "productionTemperature": 0.0
          },
          "prev_add": false,
          "prev_delete": false,
          "prev_modify": false,
          "prev_query": false,
          "recipes_initialized": false,
          "queue": [],
          "prev_enq": false,
          "prev_deq": false
        }
      },
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB003'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "error",
    "hiAlarm",
    "loAlarm",
    "status"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "hiPrev": {
      "kind": "previous_observed_output",
      "source": "O[k-1].hiAlarm",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].hiAlarm; never write into reference state."
    },
    "loPrev": {
      "kind": "previous_observed_output",
      "source": "O[k-1].loAlarm",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].loAlarm; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "Threshold comparisons are strict as written. Equality with trigger or release thresholds retains the previous alarm value.",
    "Invalid configuration returns early, preserving alarm outputs. error and status are recalculated each scan; valid configuration clears them.",
    "loLevel>=hiLevel takes priority over the hysteresis-width error. hystWindow is assumed nonnegative; negative values are outside the defined input domain.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.",
    "All REAL inputs (value, loLevel, hiLevel, hystWindow) and reference threshold arithmetic (real32(hi-lo), real32(hi-width), real32(lo+width)) use IEEE 754 binary32 (REAL) rounding.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "四个REAL参数先按IEEE binary32舍入且有限，hystWindow>=0。lo>=hi时报8001，否则width>=real32(hi-lo)时报8002；错误时参考高低报警保持。有效时高报警由value>hi置真、value<real32(hi-width)置假、其余保持；低报警由value<lo置真、value>real32(lo+width)置假、其余保持。初值均FALSE。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(badRange -> (error & status=16#8001 & sameAlarms))
```

Invalid limits take priority and leave alarms unchanged.

**P2**

```text
G((!badRange & badWindow) -> (error & status=16#8002 & sameAlarms))
```

The hysteresis range must be smaller than the limit separation.

**P3**

```text
G(valid -> (!error & status=0))
```

Valid input clears transient configuration errors.

**P4**

```text
G((valid & Value>hiLevel) -> hiAlarm)
```

A high excursion activates the high alarm.

**P5**

```text
G((valid & Value<HighRelease) -> !hiAlarm)
```

Below the strict release boundary, high alarm clears.

**P6**

```text
G((valid & HighRelease<=Value & Value<=hiLevel) -> (hiAlarm=hiPrev))
```

The high hysteresis band retains history.

**P7**

```text
G((valid & Value<loLevel) -> loAlarm)
```

A low excursion activates the low alarm.

**P8**

```text
G((valid & Value>LowRelease) -> !loAlarm)
```

Above the strict low release boundary, low alarm clears.

**P9**

```text
G((valid & loLevel<=Value & Value<=LowRelease) -> (loAlarm=loPrev))
```

The low hysteresis band retains history.

**PUB003.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Strict high and low hysteresis boundaries | 9 |
| T2 | Configuration priority, output retention and recovery | 4 |
| V2_data_contract_boundaries | Independently calculated edge/history/parser boundary regression | 6 |
| PUB003.T3 | PUB003.T3 | 7 |
| PUB003.R22.invalid_low | 低报警已置位后进入非法配置，应保留低报警 | 2 |
| PUB003.R22.real_boundaries | REAL迟滞阈值相等保持及两侧变化 | 8 |
| PUB003.T4 | Negative engineering thresholds with hysteresis retention boundaries and direct hi-to-lo jump. | 8 |
| PUB003.T5 | Error priority transition (16#8002 -> 16#8001), hysteresis alarm retention through config errors, and valid release. | 5 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB004 Jam Pump Debouncing and Runtime Maintenance

Origin: public. Difficulty: easy.

### Source and adaptation

```json
{
  "source_type": "official_course_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": {
    "group": "easy",
    "index_1based": 4
  },
  "adaptation": "Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.",
  "rationale": "Teacher-supplied PLC task; retains the specified interface and control scenario.",
  "review": "Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC."
}
```

### Natural language source

# Jam Pump Debouncing and Runtime Maintenance

- **Difficulty:** Easy (easy)

## Requirements

Control a jam transfer pump on a food production line, including viscosity-signal debouncing, emergency-stop priority, runtime accumulation and a maintenance-due indication.

1. Accept the viscosity condition only after VISCOSITY_OK has remained TRUE for DebounceTime. Invalidate the condition immediately when the input becomes FALSE.
2. Allow VFD_RUN to be TRUE only when PASTE_E_STOP_NC is TRUE and the viscosity condition is valid. An emergency stop immediately disables the run output and clears any incomplete debounce timing.
3. Accumulate PUMP_RUNTIME_ACC using the actual invocation interval CycleTime only while VFD_RUN is TRUE. Preserve the accumulated time while the pump is stopped.
4. Set PUMP_MAINT_DUE when accumulated runtime reaches 500 hours. This indication is informational and must not affect pump operation or the safety permissive.
5. At power-up, initialize the run output to OFF, accumulated runtime to zero and the maintenance indication to FALSE.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `VISCOSITY_OK` | `BOOL` | Raw signal indicating that viscosity is within the permitted range. |
| Input | `PASTE_E_STOP_NC` | `BOOL` | Normally closed emergency-stop circuit; TRUE permits operation and FALSE means emergency stop. |
| Input | `DebounceTime` | `TIME` | Required continuous valid duration for the viscosity signal; must be positive. |
| Input | `CycleTime` | `TIME` | Actual elapsed interval represented by this invocation; must be positive. |
| Output | `VFD_RUN` | `BOOL` | Pump variable-frequency-drive run command. |
| Output | `PUMP_MAINT_DUE` | `BOOL` | Maintenance indication when accumulated runtime reaches 500 hours. |
| Output | `PUMP_RUNTIME_ACC` | `LTIME` | Accumulated enabled runtime, using a long-duration time type. |

### Scenario

Control a jam transfer pump on a food production line, including viscosity-signal debouncing, emergency-stop priority, runtime accumulation and a maintenance-due indication.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | VISCOSITY_OK | BOOL | Raw signal indicating that viscosity is within the permitted range. |
| INPUT | PASTE_E_STOP_NC | BOOL | Normally closed emergency-stop circuit; TRUE permits operation and FALSE means emergency stop. |
| INPUT | DebounceTime | TIME | Required continuous valid duration for the viscosity signal; must be positive. |
| INPUT | CycleTime | TIME | Actual elapsed interval represented by this invocation; must be positive. |
| OUTPUT | VFD_RUN | BOOL | Pump variable-frequency-drive run command. |
| OUTPUT | PUMP_MAINT_DUE | BOOL | Maintenance indication when accumulated runtime reaches 500 hours. |
| OUTPUT | PUMP_RUNTIME_ACC | LTIME | Accumulated enabled runtime, using a long-duration time type. |

### Initial conditions

```json
{
  "VFD_RUN": false,
  "PUMP_RUNTIME_ACC": "LTIME#0ns",
  "PUMP_MAINT_DUE": false,
  "debounceElapsed_ms": 0
}
```

### Scan semantics

At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

### Safety and priorities

- Emergency stop or raw viscosity FALSE clears the run permission immediately.
- Maintenance does not override run permission.

### Explicit assumptions

- DebounceTime and CycleTime are strictly positive. Inputs are held stable between timed test samples.
- Debouncing follows a TON-style clock: elapsed is zero on the first permitted TRUE sample and becomes valid at elapsed>=DebounceTime.
- An E-stop resets debounce validity as well as incomplete timing, so re-enabling requires a full new qualification.
- At each invocation, add the supplied CycleTime to the LTIME accumulator iff the end-of-scan VFD_RUN is TRUE. Do not use TIME for the 500-hour accumulator.
- PUMP_MAINT_DUE is a level comparison accumulated runtime>=500h and has no reset input. Its threshold case is specified but is not a short practical runtime test.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- DebounceTime is a strictly positive constant throughout each test case. Dynamic changes are outside this benchmark domain. Time must advance for eventual-start properties.
- On timed benchmark tests, CycleTime equals the step dt_ms. Both DebounceTime and CycleTime use exact integer nanoseconds within unsigned 32-bit IEC TIME bounds (<=4294967295 ms), whereas PUMP_RUNTIME_ACC uses 64-bit LTIME (0..2^63-1 ns). Scan k=0 initializes the debounce clock at 0 ms but adds CycleTime to PUMP_RUNTIME_ACC if end-of-scan VFD_RUN is TRUE.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `permit`: VISCOSITY_OK & PASTE_E_STOP_NC
- `qualified`: Continuous permitted raw TRUE duration >= DebounceTime, with first sampled TRUE at elapsed zero.
- `accPrev`: {"kind": "previous_observed_output", "source": "O[k-1].PUMP_RUNTIME_ACC", "initial": "LTIME#0ns", "update": "After comparing scan k, store ACTUAL O[k].PUMP_RUNTIME_ACC; never write into reference state."}
- `accNext`: O[k].PUMP_RUNTIME_ACC, actual post-scan LTIME; never reference accumulator.
- `interface names`: Identically named sampled input or end-of-scan output.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB004(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
物理采样时钟首拍0、以后累加dt_ms；CycleTime与采样周期dt_ms一致，首拍运行工时按CycleTime语义计入。permit=VISCOSITY_OK & PASTE_E_STOP_NC；首次permit真时记录起点，假时清起点，run=permit且年龄>=固定正DebounceTime。acc初值0；accAfter=accBefore+(run?CycleTime:0)，CycleTime先解释为纳秒；maint=accAfter>=500h。累计域0..2^63-1纳秒。
- `TimeTick`: Boolean: floor(t[k]/1ms)>floor(t[k-1]/1ms), with t[0]=0, TimeTick[0]=FALSE, t[k]=sum(dt_ms[1..k]). G(F(TimeTick)) states unbounded physical time progress; merely positive dt is insufficient.
- `VISCOSITY_OK`: I[k].VISCOSITY_OK: sampled input (BOOL).
- `PASTE_E_STOP_NC`: I[k].PASTE_E_STOP_NC: sampled input (BOOL).
- `DebounceTime`: I[k].DebounceTime: sampled input (TIME).
- `CycleTime`: I[k].CycleTime: sampled input (TIME).
- `VFD_RUN`: O[k].VFD_RUN: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `PUMP_MAINT_DUE`: O[k].PUMP_MAINT_DUE: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `PUMP_RUNTIME_ACC`: O[k].PUMP_RUNTIME_ACC: independently observed post-scan candidate value (LTIME); never defined as expected output.
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.VFD_RUN=false, O_init.PUMP_MAINT_DUE=false, O_init.PUMP_RUNTIME_ACC="LTIME#0ns".

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ns",
    "PUMP_MAINT_DUE": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB004",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": {
        "class": "TimedContract",
        "state": {
          "task_id": "PUB004",
          "clock": {
            "decimal": "0"
          },
          "first": true,
          "since": null,
          "debounce": null,
          "runtime": 0,
          "count": 0,
          "previous_run": false,
          "previous_fault": false,
          "history": [
            0,
            0,
            0,
            0,
            0
          ]
        }
      },
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB004'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "PUMP_MAINT_DUE",
    "PUMP_RUNTIME_ACC",
    "VFD_RUN"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "accPrev": {
      "kind": "previous_observed_output",
      "source": "O[k-1].PUMP_RUNTIME_ACC",
      "initial": "LTIME#0ns",
      "update": "After comparing scan k, store ACTUAL O[k].PUMP_RUNTIME_ACC; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "timing": {
      "clock": "Spost.timed_contract.clock (exact integer nanoseconds; first invocation 0)",
      "start": "Spost.timed_contract.since; None means inactive",
      "qualified": "start is not None AND clock-start >= duration_ns(limit)",
      "hold": "start is not None AND clock-start < 500000000",
      "initial_start": null,
      "initial_clock": 0,
      "limit": "DebounceTime for PUB004/PUB005, 5000000000ns for PUB006, 30000000000ns for PUB013",
      "previous_fault": "Spre.timed_contract.previous_fault, initially FALSE; next=THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT",
      "pre_count": "Spre.timed_contract.count",
      "pre_history": "Spre.timed_contract.history",
      "pre_runtime": "Spre.timed_contract.runtime"
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "DebounceTime and CycleTime are strictly positive. Inputs are held stable between timed test samples.",
    "Debouncing follows a TON-style clock: elapsed is zero on the first permitted TRUE sample and becomes valid at elapsed>=DebounceTime.",
    "An E-stop resets debounce validity as well as incomplete timing, so re-enabling requires a full new qualification.",
    "At each invocation, add the supplied CycleTime to the LTIME accumulator iff the end-of-scan VFD_RUN is TRUE. Do not use TIME for the 500-hour accumulator.",
    "PUMP_MAINT_DUE is a level comparison accumulated runtime>=500h and has no reset input. Its threshold case is specified but is not a short practical runtime test.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "DebounceTime is a strictly positive constant throughout each test case. Dynamic changes are outside this benchmark domain. Time must advance for eventual-start properties.",
    "On timed benchmark tests, CycleTime equals the step dt_ms. Both DebounceTime and CycleTime use exact integer nanoseconds within unsigned 32-bit IEC TIME bounds (<=4294967295 ms), whereas PUMP_RUNTIME_ACC uses 64-bit LTIME (0..2^63-1 ns). Scan k=0 initializes the debounce clock at 0 ms but adds CycleTime to PUMP_RUNTIME_ACC if end-of-scan VFD_RUN is TRUE.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "物理采样时钟首拍0、以后累加dt_ms；CycleTime与采样周期dt_ms一致，首拍运行工时按CycleTime语义计入。permit=VISCOSITY_OK & PASTE_E_STOP_NC；首次permit真时记录起点，假时清起点，run=permit且年龄>=固定正DebounceTime。acc初值0；accAfter=accBefore+(run?CycleTime:0)，CycleTime先解释为纳秒；maint=accAfter>=500h。累计域0..2^63-1纳秒。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(VFD_RUN <-> (permit & qualified))
```

The run output follows the qualified permissive.

**P2**

```text
G(!permit -> !VFD_RUN)
```

Raw loss or E-stop stops immediately.

**P3**

```text
G((!permit) -> X(!qualified))
```

A lost permissive clears qualification history; future qualification must be rebuilt.

**P4**

```text
G(VFD_RUN -> accNext=accPrev+TIME_TO_LTIME(CycleTime))
```

Only enabled intervals are accumulated in a long time type.

**P5**

```text
G(!VFD_RUN -> accNext=accPrev)
```

Stopping retains accumulated service time.

**P6**

```text
G(PUMP_MAINT_DUE <-> accNext>=LTIME#500h)
```

Maintenance threshold is 500 hours.

**P7**

```text
(G(F(TimeTick))) -> (G((G(permit) & DebounceTime>TIME#0ms) -> F(VFD_RUN)))
```

A continuously permitted demand eventually starts under advancing time. Explicit non-Zeno environment premise: physical elapsed time crosses infinitely many 1ms boundaries.

**PUB004.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Qualification boundary, accumulation, stop retention and restart | 9 |
| T2 | E-stop clears incomplete debounce and completed permission | 7 |
| T3 | Long-duration maintenance arithmetic boundary | 4 |
| V2_permit_loss_at_deadline | Permission loss at the exact deadline wins; recovery starts a fresh full interval, even after a long gap. | 5 |
| PUB004.T5 | PUB004.T5 | 8 |
| PUB004.R22.interrupted_delay | 启动延时中断后重新计时、运行后急停恢复 | 9 |
| PUB004.R22.maintenance_edge | 累计500小时前1ms、恰好到期及维护提示后重启 | 6 |
| PUB004.T6 | Multi-CycleTime runtime accumulation after debounce, permit loss retention, and fresh requalification. | 7 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB005 Weld Gap Alarm and Startup Inhibition

Origin: public. Difficulty: easy.

### Source and adaptation

```json
{
  "source_type": "official_course_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": {
    "group": "easy",
    "index_1based": 5
  },
  "adaptation": "Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.",
  "rationale": "Teacher-supplied PLC task; retains the specified interface and control scenario.",
  "review": "Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC."
}
```

### Natural language source

# Weld Gap Alarm and Startup Inhibition

- **Difficulty:** Easy (easy)

## Requirements

Control a weld-gap alarm with power-up monitoring inhibition, input debouncing during normal monitoring and emergency-stop priority.

1. Gap_Exceeded indicates that the scanner has detected a weld gap exceeding the permitted 1.5 mm value.
2. Begin with a 5-second initialization inhibition period after power-up. During this period, Operator_Alert is FALSE, Weld_Soft_Start_Active is TRUE, and gap-signal debounce time does not accumulate.
3. Resume gap monitoring after initialization. Allow the alarm only after Gap_Exceeded has remained TRUE for DebounceTime. When the signal becomes FALSE, switch off the alarm and clear debounce timing.
4. When Weld_E_Stop_NC is FALSE, the emergency stop takes priority over initialization and normal monitoring. Operator_Alert must immediately become FALSE and any incomplete debounce timing must be cleared.
5. Weld_Soft_Start_Active indicates only the power-up inhibition period; it does not represent a continuous speed ramp.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `Gap_Exceeded` | `BOOL` | Scanner indication that the gap exceeds 1.5 mm. |
| Input | `Weld_E_Stop_NC` | `BOOL` | TRUE means the emergency stop is inactive; FALSE means it is active. |
| Input | `DebounceTime` | `TIME` | Gap-signal debounce duration during normal monitoring; must be positive. |
| Output | `Operator_Alert` | `BOOL` | Audible and visual alarm command. |
| Output | `Weld_Soft_Start_Active` | `BOOL` | Monitoring-inhibition status during the 5-second power-up initialization. |

### Scenario

Control a weld-gap alarm with power-up monitoring inhibition, input debouncing during normal monitoring and emergency-stop priority.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Gap_Exceeded | BOOL | Scanner indication that the gap exceeds 1.5 mm. |
| INPUT | Weld_E_Stop_NC | BOOL | TRUE means the emergency stop is inactive; FALSE means it is active. |
| INPUT | DebounceTime | TIME | Gap-signal debounce duration during normal monitoring; must be positive. |
| OUTPUT | Operator_Alert | BOOL | Audible and visual alarm command. |
| OUTPUT | Weld_Soft_Start_Active | BOOL | Monitoring-inhibition status during the 5-second power-up initialization. |

### Initial conditions

```json
{
  "Operator_Alert": false,
  "Weld_Soft_Start_Active": true,
  "startupElapsed_ms": 0,
  "gapElapsed_ms": 0
}
```

### Scan semantics

At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

### Safety and priorities

- E-stop immediately suppresses the alarm in every phase.
- Initialization suppresses alarm and prevents gap timing.

### Explicit assumptions

- Power-up inhibition uses a monotonically advancing 5-second timer that starts on the first FB invocation and continues through E-stop.
- Weld_Soft_Start_Active reports startup inhibition even during E-stop. E-stop overrides the alert and resets gap timing but does not restart power-up inhibition.
- At exactly 5 seconds startup inhibition clears. That scan is the first eligible gap sample, with gap elapsed zero; there is no credited debounce time during inhibition.
- DebounceTime is positive. Alert clears and debounce resets immediately on raw gap FALSE or E-stop.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- DebounceTime is a strictly positive constant throughout each test case. Dynamic changes are outside this benchmark domain. Time must advance for eventual-start properties.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `startup`: Elapsed time since the first invocation is less than 5 seconds.
- `gapQualified`: Gap_Exceeded has remained TRUE with Weld_E_Stop_NC TRUE and !startup for at least DebounceTime, measured from first eligible invocation.
- `interface names`: Identically named sampled input or observed output.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB005(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
首拍时钟0；startup=clock<5s，急停不重启此时钟。gapPermit=!startup & Gap_Exceeded & Weld_E_Stop_NC；首次gapPermit真年龄0，假清起点；alarm=gapPermit且年龄>=固定正DebounceTime。两个期望输出为alarm、startup。
- `TimeTick`: Boolean: floor(t[k]/1ms)>floor(t[k-1]/1ms), with t[0]=0, TimeTick[0]=FALSE, t[k]=sum(dt_ms[1..k]). G(F(TimeTick)) states unbounded physical time progress; merely positive dt is insufficient.
- `Gap_Exceeded`: I[k].Gap_Exceeded: sampled input (BOOL).
- `Weld_E_Stop_NC`: I[k].Weld_E_Stop_NC: sampled input (BOOL).
- `DebounceTime`: I[k].DebounceTime: sampled input (TIME).
- `Operator_Alert`: O[k].Operator_Alert: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Weld_Soft_Start_Active`: O[k].Weld_Soft_Start_Active: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.Operator_Alert=false, O_init.Weld_Soft_Start_Active=true.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": true
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB005",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": {
        "class": "TimedContract",
        "state": {
          "task_id": "PUB005",
          "clock": {
            "decimal": "0"
          },
          "first": true,
          "since": null,
          "debounce": null,
          "runtime": 0,
          "count": 0,
          "previous_run": false,
          "previous_fault": false,
          "history": [
            0,
            0,
            0,
            0,
            0
          ]
        }
      },
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB005'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Operator_Alert",
    "Weld_Soft_Start_Active"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "timing": {
      "clock": "Spost.timed_contract.clock (exact integer nanoseconds; first invocation 0)",
      "start": "Spost.timed_contract.since; None means inactive",
      "qualified": "start is not None AND clock-start >= duration_ns(limit)",
      "hold": "start is not None AND clock-start < 500000000",
      "initial_start": null,
      "initial_clock": 0,
      "limit": "DebounceTime for PUB004/PUB005, 5000000000ns for PUB006, 30000000000ns for PUB013",
      "previous_fault": "Spre.timed_contract.previous_fault, initially FALSE; next=THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT",
      "pre_count": "Spre.timed_contract.count",
      "pre_history": "Spre.timed_contract.history",
      "pre_runtime": "Spre.timed_contract.runtime"
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "Power-up inhibition uses a monotonically advancing 5-second timer that starts on the first FB invocation and continues through E-stop.",
    "Weld_Soft_Start_Active reports startup inhibition even during E-stop. E-stop overrides the alert and resets gap timing but does not restart power-up inhibition.",
    "At exactly 5 seconds startup inhibition clears. That scan is the first eligible gap sample, with gap elapsed zero; there is no credited debounce time during inhibition.",
    "DebounceTime is positive. Alert clears and debounce resets immediately on raw gap FALSE or E-stop.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "DebounceTime is a strictly positive constant throughout each test case. Dynamic changes are outside this benchmark domain. Time must advance for eventual-start properties.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "首拍时钟0；startup=clock<5s，急停不重启此时钟。gapPermit=!startup & Gap_Exceeded & Weld_E_Stop_NC；首次gapPermit真年龄0，假清起点；alarm=gapPermit且年龄>=固定正DebounceTime。两个期望输出为alarm、startup。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(Weld_Soft_Start_Active <-> startup)
```

Soft-start output means only the startup monitoring inhibition interval.

**P2**

```text
G((startup | !Weld_E_Stop_NC | !Gap_Exceeded) -> !Operator_Alert)
```

Startup, E-stop or no gap forces the alarm off.

**P3**

```text
G(Operator_Alert <-> (!startup & Weld_E_Stop_NC & Gap_Exceeded & gapQualified))
```

Alarm requires post-startup continuous qualified gap.

**P4**

```text
G((startup | !Weld_E_Stop_NC | !Gap_Exceeded) -> X(!gapQualified))
```

Each suppressing condition clears or blocks gap qualification.

**P5**

```text
(G(F(TimeTick))) -> (G((G(Weld_E_Stop_NC & Gap_Exceeded)) -> F(Operator_Alert)))
```

Persistent gap eventually alarms after startup and debounce, assuming advancing time. Explicit non-Zeno environment premise: physical elapsed time crosses infinitely many 1ms boundaries.

**PUB005.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Initialization excludes gap timing and debounce starts at 5s | 6 |
| T2 | E-stop suppresses startup and normal alerts without restarting inhibition | 8 |
| PUB005.T3 | PUB005.T3 | 10 |
| PUB005.R22.gap_reset | 去抖未完成时信号中断，恢复后必须重新计时 | 6 |
| PUB005.T4 | Exact 5000ms startup exit does not count pre-exit gap duration; full DebounceTime starts at exit scan. | 5 |
| PUB005.T5 | Minimum positive 1ms debounce after 5s startup and immediate E-stop alert clearing with fresh requalification. | 6 |
| PUB005.T6 | Normal gap flicker clearing at 5000ms+ resets debounce while never retriggering Weld_Soft_Start_Active. | 7 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB006 Aeration Blower Delayed Start

Origin: public. Difficulty: easy.

### Source and adaptation

```json
{
  "source_type": "official_course_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": {
    "group": "easy",
    "index_1based": 6
  },
  "adaptation": "Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.",
  "rationale": "Teacher-supplied PLC task; retains the specified interface and control scenario.",
  "review": "Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC."
}
```

### Natural language source

# Aeration Blower Delayed Start

- **Difficulty:** Easy (easy)

## Requirements

Control a wastewater-treatment aeration blower with a low-dissolved-oxygen demand, a 5-second start delay, emergency-stop priority and start-cycle counting.

1. Start delay timing when both DO_LOW and AERATION_E_STOP_NC are TRUE. Allow BLOWER_RUN to become TRUE only after these conditions have remained satisfied for 5 seconds.
2. If DO_LOW becomes FALSE or an emergency stop occurs, immediately disable BLOWER_RUN and reset the start timer, whether timing is incomplete or complete. A new demand must wait the full 5 seconds again.
3. Increment AERATION_BLOWER_CYCLE_COUNT once on each FALSE-to-TRUE transition of BLOWER_RUN. Do not count repeatedly during continuous operation.
4. At power-up, initialize the blower to OFF and the start count to zero. The start delay gates a BOOL enable; no continuous speed ramp is required.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `DO_LOW` | `BOOL` | Dissolved oxygen is below its threshold and aeration is needed. |
| Input | `AERATION_E_STOP_NC` | `BOOL` | TRUE means the emergency stop is inactive; FALSE means it is active. |
| Output | `BLOWER_RUN` | `BOOL` | Blower motor-contactor run command. |
| Output | `AERATION_BLOWER_CYCLE_COUNT` | `UINT` | Count of actual blower starts. |

### Scenario

Control a wastewater-treatment aeration blower with a low-dissolved-oxygen demand, a 5-second start delay, emergency-stop priority and start-cycle counting.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | DO_LOW | BOOL | Dissolved oxygen is below its threshold and aeration is needed. |
| INPUT | AERATION_E_STOP_NC | BOOL | TRUE means the emergency stop is inactive; FALSE means it is active. |
| OUTPUT | BLOWER_RUN | BOOL | Blower motor-contactor run command. |
| OUTPUT | AERATION_BLOWER_CYCLE_COUNT | UINT | Count of actual blower starts. |

### Initial conditions

```json
{
  "BLOWER_RUN": false,
  "AERATION_BLOWER_CYCLE_COUNT": 0,
  "delayElapsed_ms": 0
}
```

### Scan semantics

At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

### Safety and priorities

- DO_LOW FALSE or emergency stop overrides timing and resets it immediately.

### Explicit assumptions

- Start delay elapsed is zero at the first sample of DO_LOW & AERATION_E_STOP_NC; run becomes TRUE at elapsed>=5s.
- Count increments on the same invocation that changes end-of-scan BLOWER_RUN from FALSE to TRUE.
- Tests stay below UINT overflow; overflow behavior is outside the specified operating domain.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `permit`: DO_LOW & AERATION_E_STOP_NC
- `delayDone`: Permissive has continuously remained true for >=5s after its first sampled TRUE.
- `runPrev`: {"kind": "previous_observed_output", "source": "O[k-1].BLOWER_RUN", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].BLOWER_RUN; never write into reference state."}
- `countPrev`: {"kind": "previous_observed_output", "source": "O[k-1].AERATION_BLOWER_CYCLE_COUNT", "initial": 0, "update": "After comparing scan k, store ACTUAL O[k].AERATION_BLOWER_CYCLE_COUNT; never write into reference state."}
- `interface names`: Identically named sampled input or observed output.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB006(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
permit=DO_LOW & AERATION_E_STOP_NC；首次真年龄0，假清计时；run=permit且年龄>=5s。countAfter=countBefore+int(run & !refRunBefore)，初始count=0/refRun=FALSE；每拍更新refRun。计数域0..65535，越界输入历史不在评测域。
- `TimeTick`: Boolean: floor(t[k]/1ms)>floor(t[k-1]/1ms), with t[0]=0, TimeTick[0]=FALSE, t[k]=sum(dt_ms[1..k]). G(F(TimeTick)) states unbounded physical time progress; merely positive dt is insufficient.
- `DO_LOW`: I[k].DO_LOW: sampled input (BOOL).
- `AERATION_E_STOP_NC`: I[k].AERATION_E_STOP_NC: sampled input (BOOL).
- `BLOWER_RUN`: O[k].BLOWER_RUN: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `AERATION_BLOWER_CYCLE_COUNT`: O[k].AERATION_BLOWER_CYCLE_COUNT: independently observed post-scan candidate value (UINT); never defined as expected output.
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.BLOWER_RUN=false, O_init.AERATION_BLOWER_CYCLE_COUNT=0.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB006",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": {
        "class": "TimedContract",
        "state": {
          "task_id": "PUB006",
          "clock": {
            "decimal": "0"
          },
          "first": true,
          "since": null,
          "debounce": null,
          "runtime": 0,
          "count": 0,
          "previous_run": false,
          "previous_fault": false,
          "history": [
            0,
            0,
            0,
            0,
            0
          ]
        }
      },
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB006'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "AERATION_BLOWER_CYCLE_COUNT",
    "BLOWER_RUN"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "runPrev": {
      "kind": "previous_observed_output",
      "source": "O[k-1].BLOWER_RUN",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].BLOWER_RUN; never write into reference state."
    },
    "countPrev": {
      "kind": "previous_observed_output",
      "source": "O[k-1].AERATION_BLOWER_CYCLE_COUNT",
      "initial": 0,
      "update": "After comparing scan k, store ACTUAL O[k].AERATION_BLOWER_CYCLE_COUNT; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "timing": {
      "clock": "Spost.timed_contract.clock (exact integer nanoseconds; first invocation 0)",
      "start": "Spost.timed_contract.since; None means inactive",
      "qualified": "start is not None AND clock-start >= duration_ns(limit)",
      "hold": "start is not None AND clock-start < 500000000",
      "initial_start": null,
      "initial_clock": 0,
      "limit": "DebounceTime for PUB004/PUB005, 5000000000ns for PUB006, 30000000000ns for PUB013",
      "previous_fault": "Spre.timed_contract.previous_fault, initially FALSE; next=THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT",
      "pre_count": "Spre.timed_contract.count",
      "pre_history": "Spre.timed_contract.history",
      "pre_runtime": "Spre.timed_contract.runtime"
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "Start delay elapsed is zero at the first sample of DO_LOW & AERATION_E_STOP_NC; run becomes TRUE at elapsed>=5s.",
    "Count increments on the same invocation that changes end-of-scan BLOWER_RUN from FALSE to TRUE.",
    "Tests stay below UINT overflow; overflow behavior is outside the specified operating domain.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "permit=DO_LOW & AERATION_E_STOP_NC；首次真年龄0，假清计时；run=permit且年龄>=5s。countAfter=countBefore+int(run & !refRunBefore)，初始count=0/refRun=FALSE；每拍更新refRun。计数域0..65535，越界输入历史不在评测域。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(BLOWER_RUN <-> (permit & delayDone))
```

Run is enabled only after the full delay.

**P2**

```text
G(!permit -> (!BLOWER_RUN & X(!delayDone)))
```

Loss of demand or safety permissive clears run and its timer.

**P3**

```text
G((!runPrev & BLOWER_RUN) -> AERATION_BLOWER_CYCLE_COUNT=countPrev+1)
```

One count per genuine start.

**P4**

```text
G((runPrev | !BLOWER_RUN) -> AERATION_BLOWER_CYCLE_COUNT=countPrev)
```

No repeated count during continuous operation or stop.

**P5**

```text
(G(F(TimeTick))) -> (G((G(permit)) -> F(BLOWER_RUN)))
```

A sustained permitted demand eventually starts under advancing time. Explicit non-Zeno environment premise: physical elapsed time crosses infinitely many 1ms boundaries.

**PUB006.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Exact delay threshold, sustained operation and second counted start | 8 |
| T2 | Emergency stop discards partial and completed delay | 7 |
| V2_permit_loss_at_deadline | Permission loss at the exact deadline wins; recovery starts a fresh full interval, even after a long gap. | 5 |
| PUB006.T3 | PUB006.T3 | 12 |
| PUB006.R22.interrupted_delay | 启动延时中断后重新计时、运行后急停恢复 | 9 |
| PUB006.T4 | Exact 4999ms hold without start followed by DO_LOW drop resets 5s delay; E-stop drop keeps count unchanged. | 7 |
| PUB006.T5 | Three consecutive start-run-stop cycles increment cycle count cleanly without recounting during sustained run. | 10 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB007 Multi-Pump Switching Control System

Origin: public. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "official_course_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": {
    "group": "medium",
    "index_1based": 1
  },
  "adaptation": "Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.",
  "rationale": "Teacher-supplied PLC task; retains the specified interface and control scenario.",
  "review": "Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC."
}
```

### Natural language source

# Multi-Pump Switching Control System

- **Difficulty:** Medium (medium)

## Requirements

In an industrial water supply system, there are 5 pumps, each of which can be controlled independently. The system needs to support both manual and automatic operating modes.
Based on the value of the mode variable, switch to the corresponding operating mode.
In manual mode, control the start and stop of the selected pump based on the value of pumpGroup[1..5].selection.
In automatic mode, compare the priority of each pump, and automatically select the 3 pumps with higher priority for water supply according to the method of three in use and two on standby.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `mode` | `BOOL` | FALSE: Manual mode<br>TRUE: Automatic mode |
| Input | `start` | `BOOL` | Start button, used to start the manually selected or automatically selected pump |
| Input | `stop` | `BOOL` | Stop button, used to stop all pumps |
| Input/Output | `pumpGroup` | `ARRAY[1..5] OF ST_Pump` | Five pump records passed by reference. Read priority and selection; write only RunComd. |

**Data type `ST_Pump`**

| Field | Data Type | Description |
| --- | --- | --- |
| `priority` | `INT` | Priority; larger values have higher priority. Read-only to the function block. |
| `selection` | `BOOL` | Manual-selection state. Read-only to the function block. |
| `RunComd` | `BOOL` | Run command written by the function block; TRUE runs and FALSE stops. |

### Scenario

In an industrial water supply system, there are 5 pumps, each of which can be controlled independently. The system needs to support both manual and automatic operating modes.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | mode | BOOL | FALSE: Manual mode<br>TRUE: Automatic mode |
| INPUT | start | BOOL | Start button, used to start the manually selected or automatically selected pump |
| INPUT | stop | BOOL | Stop button, used to stop all pumps |
| IN_OUT | pumpGroup | ARRAY[1..5] OF ST_Pump | Five pump records passed by reference. Read priority and selection; write only RunComd. |

### Initial conditions

```json
{
  "pumpGroup[].RunComd": false
}
```

### Scan semantics

At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

### Safety and priorities

- Stop wins over a simultaneous start.
- Read-only priority and selection fields must be unchanged.

### Explicit assumptions

- stop has priority over start and clears all five commands.
- A start command selects the running set from current mode/configuration; commands are retained while neither button is TRUE. There is no automatic selection change until another start.
- Equal priorities are resolved by lower array index first. Selection is ignored in automatic mode.
- The caller initializes every RunComd FALSE before creating the first operational scan. Only RunComd may be written.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- V2 confirms the existing evaluation policy: start is level-sensitive and reselects each TRUE invocation; without start, mode/selection/priority changes do not reselect. Automatic top-three applies to selection events, not unconditionally to every automatic invocation.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Data types

```json
{
  "ST_Pump": {
    "kind": "STRUCT",
    "fields": [
      {
        "name": "priority",
        "type": "INT",
        "access": "read_only"
      },
      {
        "name": "selection",
        "type": "BOOL",
        "access": "read_only"
      },
      {
        "name": "RunComd",
        "type": "BOOL",
        "access": "written"
      }
    ]
  }
}
```

### Atomic propositions and monitor predicates

- `top3`: Deprecated alias for automatic top-3 selection; active P3 uses expanded TopThree1..TopThree5.
- `runPrev[i]`: The pre-scan RunComd value of pump i.
- `readOnlyPreserved`: All five priority and selection values equal their sampled values.
- `runs[i]`: Post-scan pumpGroup[i].RunComd, for i=1..5.
- `select[i]`: Sampled pumpGroup[i].selection.
- `interface names`: Identically named sampled input or output.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB007(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
数组序号j=0..4，对应PLC下标j+1。stop时全部RunComd=FALSE；否则start时手动取selection，自动取按(-priority,j)升序排列的前三项；无start保持采样RunComd。priority和selection实际扫描后必须精确等于采样值。
- `TopThree1`: (1-1) is in first three ordinal indices of sorted(range(5), key=lambda j: (-I[k].pumpGroup[j].priority,j)).
- `TopThree2`: (2-1) is in first three ordinal indices of sorted(range(5), key=lambda j: (-I[k].pumpGroup[j].priority,j)).
- `TopThree3`: (3-1) is in first three ordinal indices of sorted(range(5), key=lambda j: (-I[k].pumpGroup[j].priority,j)).
- `TopThree4`: (4-1) is in first three ordinal indices of sorted(range(5), key=lambda j: (-I[k].pumpGroup[j].priority,j)).
- `TopThree5`: (5-1) is in first three ordinal indices of sorted(range(5), key=lambda j: (-I[k].pumpGroup[j].priority,j)).
- `mode`: I[k].mode: sampled input (BOOL).
- `start`: I[k].start: sampled input (BOOL).
- `stop`: I[k].stop: sampled input (BOOL).
- `pumpGroup`: O[k].pumpGroup: independently observed post-scan candidate value (ARRAY[1..5] OF ST_Pump); never defined as expected output. I[k].pumpGroup denotes separately captured caller value before invocation.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {},
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB007",
      "array_contract": {
        "class": "ArrayContract",
        "state": {
          "task_id": "PUB007"
        }
      },
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB007'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "pumpGroup"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "stop has priority over start and clears all five commands.",
    "A start command selects the running set from current mode/configuration; commands are retained while neither button is TRUE. There is no automatic selection change until another start.",
    "Equal priorities are resolved by lower array index first. Selection is ignored in automatic mode.",
    "The caller initializes every RunComd FALSE before creating the first operational scan. Only RunComd may be written.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "V2 confirms the existing evaluation policy: start is level-sensitive and reselects each TRUE invocation; without start, mode/selection/priority changes do not reselect. Automatic top-three applies to selection events, not unconditionally to every automatic invocation.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "数组序号j=0..4，对应PLC下标j+1。stop时全部RunComd=FALSE；否则start时手动取selection，自动取按(-priority,j)升序排列的前三项；无start保持采样RunComd。priority和selection实际扫描后必须精确等于采样值。"
}
```

**P1**

```text
G((stop) -> ((!runs[1]) & (!runs[2]) & (!runs[3]) & (!runs[4]) & (!runs[5])))
```

Stop de-energizes all pumps.

**P2**

```text
G((!stop & start & !mode) -> ((runs[1]=select[1]) & (runs[2]=select[2]) & (runs[3]=select[3]) & (runs[4]=select[4]) & (runs[5]=select[5])))
```

Manual start uses exactly the selected pumps.

**P3**

```text
G((!stop & start & mode) -> (((runs[1] <-> TopThree1)) & ((runs[2] <-> TopThree2)) & ((runs[3] <-> TopThree3)) & ((runs[4] <-> TopThree4)) & ((runs[5] <-> TopThree5))))
```

Automatic start runs exactly the highest-priority three.

**P4**

```text
G((!stop & !start) -> ((runs[1]=runPrev[1]) & (runs[2]=runPrev[2]) & (runs[3]=runPrev[3]) & (runs[4]=runPrev[4]) & (runs[5]=runPrev[5])))
```

Start/stop operation latches commands.

**P5**

```text
G(readOnlyPreserved)
```

The FB may not modify priorities or selections.

**PUB007.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Manual latching, read-only fields and simultaneous stop/start | 3 |
| T2 | Automatic top-three selection and deterministic ties | 3 |
| V2_pump_reselection_history | Ties, changed priorities without start, reselection and simultaneous stop/start. | 4 |
| PUB007.T3 | PUB007.T3 | 5 |
| PUB007.R22.selection | 手动选择变化、保持与模式切换 | 7 |
| PUB007.T4 | Negative/tied priorities with lower-index tie-break in auto mode (ignoring selection), plus zero/subset manual selections. | 4 |
| PUB007.T5 | Changing priorities, selections, and mode while !stop & !start holds existing runs until next start pulse. | 4 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB008 Analog Batch Processing

Origin: public. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "official_course_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": {
    "group": "medium",
    "index_1based": 2
  },
  "adaptation": "Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.",
  "rationale": "Teacher-supplied PLC task; retains the specified interface and control scenario.",
  "review": "Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC."
}
```

### Natural language source

# Analog Batch Processing

- **Difficulty:** Medium (medium)

## Requirements

Write a PLC function block that processes analog inputs in batches and converts them into engineering values.

1. analogValues supplies the raw-value array. channels supplies per-channel settings and receives conversion results. count specifies how many channels to process from the beginning of the arrays. The caller must provide count from zero through the smaller of the two array lengths. Match channels by ordinal position starting at each array's own lower bound. Read analogValues without modifying it.
2. Each channel is enabled by its enable field and converted according to measuringMode. Read configuration fields without modifying them; write only retVal and outputValue.
3. For measuringMode 0, perform non-temperature linear scaling: when bipolar is FALSE, map raw values 0..27648 to loLIM..hiLIM; when TRUE, map -27648..27648 to loLIM..hiLIM.
4. For measuringMode 1, perform standard-temperature conversion: outputValue is one tenth of the raw analog value.
5. For measuringMode 2, perform climatic-temperature conversion: outputValue is one hundredth of the raw analog value.
6. If measuringMode is not 0, 1 or 2, set that channel's retVal to 16#8001 and skip its conversion.
7. If hiLIM is less than or equal to loLIM, set that channel's retVal to 16#8002 and skip its conversion.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `count` | `DINT` | Number of channels to be converted |
| Input/Output | `analogValues` | `ARRAY[*] OF INT` | Variable-length analog array passed by reference to preserve its bounds. Read-only to the function block; no element may be modified. |
| Input/Output | `channels` | `ARRAY[*] OF ST_AnalogChannel` | Channel records passed by reference. Configuration fields are read-only; write only retVal and outputValue. |
| Input field | `channels[].enable` | `BOOL` | Channel conversion enable. Read-only to the function block. |
| Input field | `channels[].hiLIM` | `REAL` | Upper engineering-unit limit. Read-only to the function block. |
| Input field | `channels[].loLIM` | `REAL` | Lower engineering-unit limit. Read-only to the function block. |
| Input field | `channels[].bipolar` | `BOOL` | FALSE selects unipolar and TRUE selects bipolar operation. Read-only to the function block. |
| Input field | `channels[].measuringMode` | `INT` | 0 non-temperature, 1 standard temperature, 2 climatic temperature. Read-only to the function block. |
| Output field | `channels[].retVal` | `WORD` | Per-channel status code written by the function block. |
| Output field | `channels[].outputValue` | `REAL` | Converted value written by the function block. |

Rows named `channels[].fieldName` describe the element fields of ST_AnalogChannel, rather than additional function-block parameters.

### Scenario

Write a PLC function block that processes analog inputs in batches and converts them into engineering values.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | count | DINT | Number of channels to be converted |
| IN_OUT | analogValues | ARRAY[*] OF INT | Variable-length analog array passed by reference to preserve its bounds. Read-only to the function block; no element may be modified. |
| IN_OUT | channels | ARRAY[*] OF ST_AnalogChannel | Channel records passed by reference. Configuration fields are read-only; write only retVal and outputValue. |

### Initial conditions

```json
{
  "state": "No internal history required. IN_OUT output fields retain caller-provided values when skipped."
}
```

### Scan semantics

At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

### Safety and priorities

- Process only the first count ordinal entries, pairing arrays at their independent lower bounds.
- Do not modify raw analog values or any channel configuration.

### Explicit assumptions

- Disabled and out-of-count channels retain both retVal and outputValue.
- Successful enabled conversion sets retVal=0. Invalid channels preserve outputValue while returning the error code.
- Invalid measuringMode has priority over invalid hiLIM/loLIM. Limit validation applies to enabled channels in every mode.
- Scaling extrapolates outside nominal raw range; no saturation is specified.
- Test metadata array_lower_bounds defines the physical array indices used by the caller. JSON arrays are ordered storage values, not IEC index literals. The caller satisfies count bounds.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.
- V2 array extension: successful channel outputValue is compared with abs_tol=1e-5 and rel_tol=2e-6. Read-only and skipped/error-preserved fields are exact. This explicitly supersedes uniform absolute tolerance for this task only; both agents receive this policy.
- Read-only channel fields (enable, hiLIM, loLIM, bipolar, measuringMode) and skipped/disabled/error channel outputValue retain exact caller-sampled binary values; numeric tolerance (abs<=1e-5 or rel<=2e-6) applies only to successfully converted outputValue.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Data types

```json
{
  "ST_AnalogChannel": {
    "kind": "STRUCT",
    "fields": [
      {
        "name": "enable",
        "type": "BOOL",
        "access": "read_only"
      },
      {
        "name": "hiLIM",
        "type": "REAL",
        "access": "read_only"
      },
      {
        "name": "loLIM",
        "type": "REAL",
        "access": "read_only"
      },
      {
        "name": "bipolar",
        "type": "BOOL",
        "access": "read_only"
      },
      {
        "name": "measuringMode",
        "type": "INT",
        "access": "read_only"
      },
      {
        "name": "retVal",
        "type": "WORD",
        "access": "written"
      },
      {
        "name": "outputValue",
        "type": "REAL",
        "access": "written"
      }
    ]
  }
}
```

### Atomic propositions and monitor predicates

- `j`: An ordinal position starting at zero.
- `enabled(j)`: j<count and sampled channels[j].enable.
- `modeOK(j)`: Sampled measuringMode is 0,1,2.
- `limitsOK(j)`: Sampled hiLIM>loLIM.
- `raw(j)`: Sampled analogValues at its lower bound+j.
- `scaled(j)`: loLIM+(raw/27648)*(hiLIM-loLIM) for unipolar; loLIM+((raw+27648)/55296)*(hiLIM-loLIM) for bipolar.
- `preserved(j)`: The channel retVal/outputValue equal sampled values.
- `readonlyPreserved`: analogValues and channel configuration equal all their sampled values.
- `channel output names`: Post-scan fields of the channel at the indicated ordinal position.
- `sampledOutputValue(j)`: The caller-provided outputValue before this scan.
- `measuringMode(j)`: The sampled measuringMode configuration for ordinal j.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB008(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
序号j=0..len(channels)-1；仅j<count且enable处理，0<=count<=min两数组长度。非法mode优先报8001，否则hi<=lo报8002，均保留采样outputValue；成功清码，mode0按单极raw/27648或双极(raw+27648)/55296线性映射，mode1/2分别raw/10、raw/100。其他项及配置精确保留，仅成功outputValue使用abs=1e-5、rel=2e-6。
- `AllChannels_P2`: {"operator": "finite_conjunction", "variable": "j", "lower_inclusive": 0, "upper_exclusive": "len(I[k].channels)", "empty_value": true, "body": "!enabled(j) -> preserved(j)", "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.", "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.", "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.", "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."}
- `AllChannels_P3`: {"operator": "finite_conjunction", "variable": "j", "lower_inclusive": 0, "upper_exclusive": "len(I[k].channels)", "empty_value": true, "body": "(enabled(j) & !modeOK(j)) -> (retVal(j)=16#8001 & outputValue(j)=sampledOutputValue(j))", "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.", "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.", "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.", "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."}
- `AllChannels_P4`: {"operator": "finite_conjunction", "variable": "j", "lower_inclusive": 0, "upper_exclusive": "len(I[k].channels)", "empty_value": true, "body": "(enabled(j) & modeOK(j) & !limitsOK(j)) -> (retVal(j)=16#8002 & outputValue(j)=sampledOutputValue(j))", "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.", "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.", "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.", "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."}
- `AllChannels_P5`: {"operator": "finite_conjunction", "variable": "j", "lower_inclusive": 0, "upper_exclusive": "len(I[k].channels)", "empty_value": true, "body": "(enabled(j) & modeOK(j) & limitsOK(j)) -> retVal(j)=0", "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.", "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.", "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.", "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."}
- `AllChannels_P6`: {"operator": "finite_conjunction", "variable": "j", "lower_inclusive": 0, "upper_exclusive": "len(I[k].channels)", "empty_value": true, "body": "(enabled(j) & limitsOK(j) & measuringMode(j)=0) -> outputValue(j)=scaled(j)", "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.", "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.", "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.", "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."}
- `AllChannels_P7`: {"operator": "finite_conjunction", "variable": "j", "lower_inclusive": 0, "upper_exclusive": "len(I[k].channels)", "empty_value": true, "body": "(enabled(j) & limitsOK(j) & measuringMode(j)=1) -> outputValue(j)=raw(j)/10", "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.", "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.", "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.", "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."}
- `AllChannels_P8`: {"operator": "finite_conjunction", "variable": "j", "lower_inclusive": 0, "upper_exclusive": "len(I[k].channels)", "empty_value": true, "body": "(enabled(j) & limitsOK(j) & measuringMode(j)=2) -> outputValue(j)=raw(j)/100", "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.", "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.", "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.", "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."}
- `count`: I[k].count: sampled input (DINT).
- `analogValues`: O[k].analogValues: independently observed post-scan candidate value (ARRAY[*] OF INT); never defined as expected output. I[k].analogValues denotes separately captured caller value before invocation.
- `channels`: O[k].channels: independently observed post-scan candidate value (ARRAY[*] OF ST_AnalogChannel); never defined as expected output. I[k].channels denotes separately captured caller value before invocation.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {},
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB008",
      "array_contract": {
        "class": "ArrayContract",
        "state": {
          "task_id": "PUB008"
        }
      },
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB008'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "analogValues",
    "channels"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {
    "AllChannels_P2": {
      "operator": "finite_conjunction",
      "variable": "j",
      "lower_inclusive": 0,
      "upper_exclusive": "len(I[k].channels)",
      "empty_value": true,
      "body": "!enabled(j) -> preserved(j)",
      "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.",
      "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.",
      "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.",
      "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."
    },
    "AllChannels_P3": {
      "operator": "finite_conjunction",
      "variable": "j",
      "lower_inclusive": 0,
      "upper_exclusive": "len(I[k].channels)",
      "empty_value": true,
      "body": "(enabled(j) & !modeOK(j)) -> (retVal(j)=16#8001 & outputValue(j)=sampledOutputValue(j))",
      "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.",
      "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.",
      "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.",
      "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."
    },
    "AllChannels_P4": {
      "operator": "finite_conjunction",
      "variable": "j",
      "lower_inclusive": 0,
      "upper_exclusive": "len(I[k].channels)",
      "empty_value": true,
      "body": "(enabled(j) & modeOK(j) & !limitsOK(j)) -> (retVal(j)=16#8002 & outputValue(j)=sampledOutputValue(j))",
      "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.",
      "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.",
      "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.",
      "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."
    },
    "AllChannels_P5": {
      "operator": "finite_conjunction",
      "variable": "j",
      "lower_inclusive": 0,
      "upper_exclusive": "len(I[k].channels)",
      "empty_value": true,
      "body": "(enabled(j) & modeOK(j) & limitsOK(j)) -> retVal(j)=0",
      "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.",
      "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.",
      "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.",
      "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."
    },
    "AllChannels_P6": {
      "operator": "finite_conjunction",
      "variable": "j",
      "lower_inclusive": 0,
      "upper_exclusive": "len(I[k].channels)",
      "empty_value": true,
      "body": "(enabled(j) & limitsOK(j) & measuringMode(j)=0) -> outputValue(j)=scaled(j)",
      "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.",
      "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.",
      "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.",
      "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."
    },
    "AllChannels_P7": {
      "operator": "finite_conjunction",
      "variable": "j",
      "lower_inclusive": 0,
      "upper_exclusive": "len(I[k].channels)",
      "empty_value": true,
      "body": "(enabled(j) & limitsOK(j) & measuringMode(j)=1) -> outputValue(j)=raw(j)/10",
      "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.",
      "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.",
      "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.",
      "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."
    },
    "AllChannels_P8": {
      "operator": "finite_conjunction",
      "variable": "j",
      "lower_inclusive": 0,
      "upper_exclusive": "len(I[k].channels)",
      "empty_value": true,
      "body": "(enabled(j) & limitsOK(j) & measuringMode(j)=2) -> outputValue(j)=raw(j)/100",
      "instantiation": "For concrete caller binding N, substitute j=0,...,N-1 and join the Boolean bodies with &. N is binding length, never count.",
      "index_mapping": "j is zero-based ordinal; PLC index is each array own lower bound + j.",
      "guard": "enabled(j) := j<I[k].count AND I[k].channels[j].enable; short-circuit before raw(j) access.",
      "numeric_comparison": "Converted outputValue uses the comparison policy; status/config/preserved fields are exact."
    }
  },
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "Disabled and out-of-count channels retain both retVal and outputValue.",
    "Successful enabled conversion sets retVal=0. Invalid channels preserve outputValue while returning the error code.",
    "Invalid measuringMode has priority over invalid hiLIM/loLIM. Limit validation applies to enabled channels in every mode.",
    "Scaling extrapolates outside nominal raw range; no saturation is specified.",
    "Test metadata array_lower_bounds defines the physical array indices used by the caller. JSON arrays are ordered storage values, not IEC index literals. The caller satisfies count bounds.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.",
    "V2 array extension: successful channel outputValue is compared with abs_tol=1e-5 and rel_tol=2e-6. Read-only and skipped/error-preserved fields are exact. This explicitly supersedes uniform absolute tolerance for this task only; both agents receive this policy.",
    "Read-only channel fields (enable, hiLIM, loLIM, bipolar, measuringMode) and skipped/disabled/error channel outputValue retain exact caller-sampled binary values; numeric tolerance (abs<=1e-5 or rel<=2e-6) applies only to successfully converted outputValue.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "序号j=0..len(channels)-1；仅j<count且enable处理，0<=count<=min两数组长度。非法mode优先报8001，否则hi<=lo报8002，均保留采样outputValue；成功清码，mode0按单极raw/27648或双极(raw+27648)/55296线性映射，mode1/2分别raw/10、raw/100。其他项及配置精确保留，仅成功outputValue使用abs=1e-5、rel=2e-6。"
}
```

**P1**

```text
G(readonlyPreserved)
```

Input arrays and configuration are never modified.

**P2**

```text
G(AllChannels_P2)
```

Disabled and unprocessed channels are unchanged.

**P3**

```text
G(AllChannels_P3)
```

Unsupported modes return the defined status without conversion.

**P4**

```text
G(AllChannels_P4)
```

Invalid limits return their status without conversion.

**P5**

```text
G(AllChannels_P5)
```

Successful enabled channels clear their status.

**P6**

```text
G(AllChannels_P6)
```

Linear scale uses the correct unipolar or bipolar range.

**P7**

```text
G(AllChannels_P7)
```

Standard-temperature resolution is one tenth.

**P8**

```text
G(AllChannels_P8)
```

Climatic-temperature resolution is one hundredth.

**PUB008.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Unipolar and bipolar endpoints, midpoint and temperature modes | 1 |
| T2 | Disabled channel, invalid mode priority, invalid limits and count truncation | 1 |
| T3 | count zero preserves every value and negative raw extrapolates | 2 |
| V2_unequal_arrays_wide_arithmetic | Unequal lengths and distinct lower bounds; preserve skipped channel; avoid INT intermediate overflow. | 1 |
| PUB008.T4 | PUB008.T4 | 2 |
| PUB008.R22.length_4_2 | 独立下界、不同长度与未处理字段保持 | 1 |
| PUB008.R22.length_2_4 | 独立下界、不同长度与未处理字段保持 | 1 |
| PUB008.T5 | Multi-step error-priority retention: disabled, out-of-count, invalid mode over invalid limits, and zero-span. | 2 |
| PUB008.T6 | Negative engineering ranges, bipolar saturation extrapolation below -27648, and temperature modes 1/2. | 1 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB009 Calculate Moving Average

Origin: public. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "official_course_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": {
    "group": "medium",
    "index_1based": 3
  },
  "adaptation": "Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.",
  "rationale": "Teacher-supplied PLC task; retains the specified interface and control scenario.",
  "review": "Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC."
}
```

### Natural language source

# Calculate Moving Average

- **Difficulty:** Medium (medium)

## Requirements

Write a function block FB that calculates and updates a moving arithmetic mean. The moving arithmetic mean is a method of averaging over consecutive data points, where each new data point replaces the oldest data point, and then the average is recalculated.

1. When cyclicExecution is TRUE, a new data value is automatically read and the moving average average is updated every scan cycle.
2. Provide an external trigger signal trigger, which reads a new data value and updates the moving average upon each rising edge.
3. Provide a reset function reset, which resets the moving average calculation when the reset signal is TRUE. If the window size is less than 1 or greater than 100, output an error status and status code.

The status parameter indicates the execution status of the program:
- 16#0000: Execution successful
- 16#8200: Window length setting error, please set a value between 1 and 100.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `cyclicExecution` | `BOOL` | When TRUE, periodic reading is performed, and trigger has no effect |
| Input | `trigger` | `BOOL` | External trigger signal, reads value upon each rising edge |
| Input | `value` | `LREAL` | Newly read data value |
| Input | `windowSize` | `INT` | The window size for the moving average, which must be between 1 and 100 |
| Input | `reset` | `BOOL` | Reset signal, resets the moving average calculation when TRUE |
| Output | `average` | `LREAL` | The moving average |
| Output | `windowSizeReached` | `BOOL` | FALSE: Maximum window width not yet reached TRUE: Maximum window width has been reached |
| Output | `error` | `BOOL` | FALSE: No error occurred TRUE: An error occurred during the execution of FB |
| Output | `status` | `WORD` | Status code |

### Scenario

Write a function block FB that calculates and updates a moving arithmetic mean. The moving arithmetic mean is a method of averaging over consecutive data points, where each new data point replaces the oldest data point, and then the average is recalculated.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | cyclicExecution | BOOL | When TRUE, periodic reading is performed, and trigger has no effect |
| INPUT | trigger | BOOL | External trigger signal, reads value upon each rising edge |
| INPUT | value | LREAL | Newly read data value |
| INPUT | windowSize | INT | The window size for the moving average, which must be between 1 and 100 |
| INPUT | reset | BOOL | Reset signal, resets the moving average calculation when TRUE |
| OUTPUT | average | LREAL | The moving average |
| OUTPUT | windowSizeReached | BOOL | FALSE: Maximum window width not yet reached TRUE: Maximum window width has been reached |
| OUTPUT | error | BOOL | FALSE: No error occurred TRUE: An error occurred during the execution of FB |
| OUTPUT | status | WORD | Status code |

### Initial conditions

```json
{
  "average": 0.0,
  "windowSizeReached": false,
  "error": false,
  "status": 0,
  "sampleCount": 0,
  "previousTrigger": false
}
```

### Scan semantics

At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

### Safety and priorities

- Invalid window returns an error before sampling.
- Reset overrides sample acceptance.
- Cyclic and trigger conditions cannot cause double insertion.

### Explicit assumptions

- During warm-up, average is the mean of the actual accepted samples; zero-filled unused capacity is excluded.
- reset has priority over sampling for a valid window; it clears history and sets average=0 and windowSizeReached=FALSE.
- Changing a valid windowSize clears history before any same-scan accepted sample. Invalid window sets error/status and does not accept or change history.
- An invalid-window scan preserves average/windowSizeReached. Returning to a valid window clears error/status. Trigger edge history is updated on every invocation, including reset and invalid-window scans.
- cyclicExecution accepts exactly one sample per scan and ignores the trigger. windowSizeReached becomes TRUE once the accepted sample count reaches windowSize.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.
- LREAL average comparisons allow up to abs<=1e-5 (and matching relative precision on T2). P6 initializes previousTrigger=FALSE prior to scan k=0.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `valid`: 1<=windowSize<=100
- `triggerRise`: trigger & !previousTrigger
- `accept`: valid & !reset & (cyclicExecution | triggerRise)
- `history`: Ghost ordered list of at most windowSize accepted samples, newest last.
- `historyAfter`: history after clearing on reset/window change and adding one accepted sample, discarding oldest if full.
- `unchangedMean`: average and windowSizeReached equal their pre-scan values.
- `interface names`: Identically named sampled input or observed output.
- `meanOrZero`: Arithmetic mean for a nonempty list, otherwise zero.
- `length`: Number of samples in the history list.
- `windowChanged`: Current valid windowSize differs from the last valid configured size.
- `previousTrigger`: {"kind": "previous_sampled_input", "source": "I[k-1].trigger", "initial": false, "update": "After EVERY scan k, including invalid/reset/stop, store I[k].trigger"}
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB009(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
previousTrigger初值FALSE且每次调用后=本拍trigger。valid=1<=windowSize<=100；非法时average/reached保持并报8200。有效窗口首次建立或改变、或reset时清空历史；非reset且cyclicExecution或trigger上升沿时追加value并保留最后windowSize项。average=空则0否则sum/n，reached=(n=windowSize)。初始历史空、average=0、reached=FALSE。
- `cyclicExecution`: I[k].cyclicExecution: sampled input (BOOL).
- `trigger`: I[k].trigger: sampled input (BOOL).
- `value`: I[k].value: sampled input (LREAL).
- `windowSize`: I[k].windowSize: sampled input (INT).
- `reset`: I[k].reset: sampled input (BOOL).
- `average`: O[k].average: independently observed post-scan candidate value (LREAL); never defined as expected output.
- `windowSizeReached`: O[k].windowSizeReached: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `error`: O[k].error: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `status`: O[k].status: independently observed post-scan candidate value (WORD); never defined as expected output.
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.average=0.0, O_init.windowSizeReached=false, O_init.error=false, O_init.status=0.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "average": 0.0,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB009",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": {
        "class": "DataContract",
        "state": {
          "task_id": "PUB009",
          "previous": 0,
          "high": false,
          "low": false,
          "trigger": false,
          "window": null,
          "history": [],
          "average": 0.0,
          "reached": false,
          "recipes": [
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            }
          ],
          "last_query": {
            "recipeID": 0,
            "ingredientType": 0,
            "ingredientRatio": 0.0,
            "productionTemperature": 0.0
          },
          "prev_add": false,
          "prev_delete": false,
          "prev_modify": false,
          "prev_query": false,
          "recipes_initialized": false,
          "queue": [],
          "prev_enq": false,
          "prev_deq": false
        }
      },
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB009'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "average",
    "error",
    "status",
    "windowSizeReached"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "previousTrigger": {
      "kind": "previous_sampled_input",
      "source": "I[k-1].trigger",
      "initial": false,
      "update": "After EVERY scan k, including invalid/reset/stop, store I[k].trigger"
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "During warm-up, average is the mean of the actual accepted samples; zero-filled unused capacity is excluded.",
    "reset has priority over sampling for a valid window; it clears history and sets average=0 and windowSizeReached=FALSE.",
    "Changing a valid windowSize clears history before any same-scan accepted sample. Invalid window sets error/status and does not accept or change history.",
    "An invalid-window scan preserves average/windowSizeReached. Returning to a valid window clears error/status. Trigger edge history is updated on every invocation, including reset and invalid-window scans.",
    "cyclicExecution accepts exactly one sample per scan and ignores the trigger. windowSizeReached becomes TRUE once the accepted sample count reaches windowSize.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.",
    "LREAL average comparisons allow up to abs<=1e-5 (and matching relative precision on T2). P6 initializes previousTrigger=FALSE prior to scan k=0.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "previousTrigger初值FALSE且每次调用后=本拍trigger。valid=1<=windowSize<=100；非法时average/reached保持并报8200。有效窗口首次建立或改变、或reset时清空历史；非reset且cyclicExecution或trigger上升沿时追加value并保留最后windowSize项。average=空则0否则sum/n，reached=(n=windowSize)。初始历史空、average=0、reached=FALSE。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(!valid -> (error & status=16#8200 & unchangedMean))
```

Window bounds are checked without silently accepting data.

**P2**

```text
G(valid -> (!error & status=0))
```

A valid window clears configuration error.

**P3**

```text
G((valid & reset) -> (average=0 & !windowSizeReached))
```

Reset produces an empty history.

**P4**

```text
G((valid & !reset) -> average=meanOrZero(historyAfter))
```

The result is the arithmetic mean of the active window or zero when empty.

**P5**

```text
G(valid -> (windowSizeReached <-> length(historyAfter)=windowSize))
```

Full-window indication follows history population.

**P6**

```text
G(trigger <-> X(previousTrigger))
```

Both operands are Boolean propositions. previousTrigger[0]=FALSE; previousTrigger[k+1]=I[k].trigger on every invocation, including invalid/reset.

**P7**

```text
G((valid & !reset & !cyclicExecution & !triggerRise & !windowChanged) -> unchangedMean)
```

No event means no sample update.

**PUB009.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Cyclic warm-up, sliding replacement and reset priority | 6 |
| T2 | Rising edge only, held trigger, window change and invalid bounds | 9 |
| V2_data_contract_boundaries | Independently calculated edge/history/parser boundary regression | 7 |
| PUB009.T3 | PUB009.T3 | 109 |
| PUB009.R22.window_100 | 合法最大窗口100必须被接受 | 1 |
| PUB009.R22.window100_True | 最大窗口填满、替换与双向变窗 | 109 |
| PUB009.R22.window100_False | 最大窗口填满、替换与双向变窗 | 214 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB010 Temperature Logic Control

Origin: public. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "official_course_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": {
    "group": "medium",
    "index_1based": 4
  },
  "adaptation": "Original English question is preserved verbatim in requirements. Only explicit evaluation assumptions, LTL, and tests are added.",
  "rationale": "Teacher-supplied PLC task; retains the specified interface and control scenario.",
  "review": "Reviewed against original prose and interface; ambiguities are listed explicitly. Expected traces have not been executed on a PLC."
}
```

### Natural language source

# Temperature Logic Control

- **Difficulty:** Medium (medium)

## Requirements

Write a function block FB to implement a temperature control logic. The program should include the following functions:
1. Read the value of the temperature sensor through an analog input module.
2. Compare the read temperature value TemperatureSensorInput with the set temperature value SetTemperature.
3. If the actual temperature is lower than the set temperature, start the heater HeaterOutput.
4. If the actual temperature is higher than the set temperature, turn off the heater HeaterOutput.
5. If the heater works continuously for more than a certain period (for convenience, using 5s), it should trigger an overheating protection, automatically turn off the heater, and must wait for a certain period (for convenience, using 3s) before the overheating protection can be lifted.
6. Provide status indication, displaying the current temperature, set temperature, heater status, and whether overheating protection is triggered.
7. Provide temperature sensor fault judgment, if the read temperature value TemperatureSensorInput is less than 0 or greater than 100, it is considered a sensor fault, and the heater should be turned off.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `TemperatureSensorInput` | `REAL` | The input value of the temperature sensor, i.e., the actual temperature |
| Input | `SetTemperature` | `REAL` | The set temperature value |
| Output | `CurrentTemperature` | `REAL` | Display of the current temperature |
| Output | `SetTempDisplay` | `REAL` | Display of the set temperature |
| Output | `HeaterStatus` | `BOOL` | Display of the heater status |
| Output | `OverheatProtection` | `BOOL` | Display of the overheating protection status |
| Output | `HeaterOutput` | `BOOL` | The control output of the heater |

### Scenario

Write a function block FB to implement a temperature control logic. The program should include the following functions:

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | TemperatureSensorInput | REAL | The input value of the temperature sensor, i.e., the actual temperature |
| INPUT | SetTemperature | REAL | The set temperature value |
| OUTPUT | CurrentTemperature | REAL | Display of the current temperature |
| OUTPUT | SetTempDisplay | REAL | Display of the set temperature |
| OUTPUT | HeaterStatus | BOOL | Display of the heater status |
| OUTPUT | OverheatProtection | BOOL | Display of the overheating protection status |
| OUTPUT | HeaterOutput | BOOL | The control output of the heater |

### Initial conditions

```json
{
  "HeaterOutput": false,
  "HeaterStatus": false,
  "OverheatProtection": false,
  "heatDemand": false,
  "heatElapsed_ms": 0,
  "cooldownElapsed_ms": 0,
  "CurrentTemperature": 0.0,
  "SetTempDisplay": 0.0
}
```

### Scan semantics

At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

### Safety and priorities

- Sensor fault or active overheat protection overrides the heat demand.
- Protection shutdown is evaluated before the output is finalized.

### Explicit assumptions

- At equality TemperatureSensorInput=SetTemperature, retain the last heat-demand state. On a fresh instance the retained demand is FALSE.
- The prose says "more than" a period and gives 5s. The evaluation resolves this to a 5-second threshold: protection trips at continuous heating elapsed>=5s, beginning with elapsed zero at the first energized sample.
- Protection is latched for at least 3s from its trip. At elapsed>=3s it may clear and heat can restart in the same scan if the sensor is valid and demand remains.
- A sensor fault immediately turns heat off and resets continuous-heating time. It does not clear or restart an already active cooldown.
- The display outputs mirror their corresponding sampled temperature and setpoint even during a fault. HeaterStatus equals HeaterOutput. Inputs are held stable between timed samples.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- V2 evaluation decision: retain the existing >=5s trip threshold as an explicit benchmark interpretation of the source more-than wording; cooldown MUST clear at the first observed elapsed>=3s, though a sensor fault or absent demand still prevents heating. No spontaneous protection is allowed. This benchmark interpretation is not claimed to be instructor clarification.
- Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.
- Scan k=0 initializes the internal elapsed-time clock at 0 ms (ignoring dt_ms[0]); subsequent scans advance by dt_ms[k]. During sensorFault (TemperatureSensorInput < 0 or > 100), the internal retained heat demand freezes at its prior state.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `sensorFault`: TemperatureSensorInput<0 OR TemperatureSensorInput>100
- `demand`: Ghost retained demand; when 0<=TemperatureSensorInput<=100, set below SetTemperature, clear above SetTemperature, retain at equality; frozen during sensorFault; initial FALSE.
- `heatLimitReached`: Continuous energized time has reached 5s, with first energized scan at elapsed zero.
- `cooldownDone`: When OverheatProtection was previously active, at least 3s has elapsed since its trip timestamp at the current scan clock (clock - protection_start >= 3s).
- `protectPrev`: {"kind": "previous_observed_output", "source": "O[k-1].OverheatProtection", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].OverheatProtection; never write into reference state."}
- `interface names`: Identically named sampled input or observed output.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB010(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
首拍时钟0、后续按观察dt_ms累加。正常温度0..100下demand低于设定置真、高于置假、相等保持；传感器故障期间冻结demand不变，初值FALSE。先释放年龄>=3s的旧保护；无旧保护且旧连续加热年龄>=5s则本拍触发保护。heat=传感器0..100有效 & demandAfter & 无保护；首次heat真记录当前时刻，heat假清热起点。显示值取输入；保护输出取保护状态。5.0s及以上起保护与既有评测口径一致。
- `TimeTick`: Boolean: floor(t[k]/1ms)>floor(t[k-1]/1ms), with t[0]=0, TimeTick[0]=FALSE, t[k]=sum(dt_ms[1..k]). G(F(TimeTick)) states unbounded physical time progress; merely positive dt is insufficient.
- `TemperatureSensorInput`: I[k].TemperatureSensorInput: sampled input (REAL).
- `SetTemperature`: I[k].SetTemperature: sampled input (REAL).
- `CurrentTemperature`: O[k].CurrentTemperature: independently observed post-scan candidate value (REAL); never defined as expected output.
- `SetTempDisplay`: O[k].SetTempDisplay: independently observed post-scan candidate value (REAL); never defined as expected output.
- `HeaterStatus`: O[k].HeaterStatus: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `OverheatProtection`: O[k].OverheatProtection: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `HeaterOutput`: O[k].HeaterOutput: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.CurrentTemperature=0.0, O_init.SetTempDisplay=0.0, O_init.HeaterStatus=false, O_init.OverheatProtection=false, O_init.HeaterOutput=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "HeaterOutput": false,
    "HeaterStatus": false,
    "OverheatProtection": false,
    "CurrentTemperature": 0.0,
    "SetTempDisplay": 0.0
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB010",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB010'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "CurrentTemperature",
    "HeaterOutput",
    "HeaterStatus",
    "OverheatProtection",
    "SetTempDisplay"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "protectPrev": {
      "kind": "previous_observed_output",
      "source": "O[k-1].OverheatProtection",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].OverheatProtection; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "At equality TemperatureSensorInput=SetTemperature, retain the last heat-demand state. On a fresh instance the retained demand is FALSE.",
    "The prose says \"more than\" a period and gives 5s. The evaluation resolves this to a 5-second threshold: protection trips at continuous heating elapsed>=5s, beginning with elapsed zero at the first energized sample.",
    "Protection is latched for at least 3s from its trip. At elapsed>=3s it may clear and heat can restart in the same scan if the sensor is valid and demand remains.",
    "A sensor fault immediately turns heat off and resets continuous-heating time. It does not clear or restart an already active cooldown.",
    "The display outputs mirror their corresponding sampled temperature and setpoint even during a fault. HeaterStatus equals HeaterOutput. Inputs are held stable between timed samples.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "V2 evaluation decision: retain the existing >=5s trip threshold as an explicit benchmark interpretation of the source more-than wording; cooldown MUST clear at the first observed elapsed>=3s, though a sensor fault or absent demand still prevents heating. No spontaneous protection is allowed. This benchmark interpretation is not claimed to be instructor clarification.",
    "Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.",
    "Scan k=0 initializes the internal elapsed-time clock at 0 ms (ignoring dt_ms[0]); subsequent scans advance by dt_ms[k]. During sensorFault (TemperatureSensorInput < 0 or > 100), the internal retained heat demand freezes at its prior state.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "首拍时钟0、后续按观察dt_ms累加。正常温度0..100下demand低于设定置真、高于置假、相等保持；传感器故障期间冻结demand不变，初值FALSE。先释放年龄>=3s的旧保护；无旧保护且旧连续加热年龄>=5s则本拍触发保护。heat=传感器0..100有效 & demandAfter & 无保护；首次heat真记录当前时刻，heat假清热起点。显示值取输入；保护输出取保护状态。5.0s及以上起保护与既有评测口径一致。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(sensorFault -> !HeaterOutput)
```

Invalid sensor data must never energize the heater.

**P2**

```text
G(OverheatProtection -> !HeaterOutput)
```

The heater remains off during cooldown.

**P3**

```text
G(HeaterStatus=HeaterOutput)
```

The status output reports actual commanded heat.

**P4**

```text
G((CurrentTemperature=TemperatureSensorInput) & (SetTempDisplay=SetTemperature))
```

The displays mirror sampled values.

**P5**

```text
G((!sensorFault & !OverheatProtection & demand & !heatLimitReached) -> HeaterOutput)
```

A permitted heat demand energizes the heater.

**P6**

```text
G(heatLimitReached -> (OverheatProtection & !HeaterOutput))
```

The continuous-heating threshold trips protection in the same scan.

**P7**

```text
G((protectPrev & !cooldownDone) -> OverheatProtection)
```

Protection cannot clear before its cooldown expires.

**P8**

```text
(G(F(TimeTick))) -> (G((OverheatProtection & G(!sensorFault & demand)) -> F(HeaterOutput)))
```

With advancing time and persistent valid demand, heating resumes after finite cooldown. Explicit non-Zeno environment premise: physical elapsed time crosses infinitely many 1ms boundaries.

**P9**

```text
G(!sensorFault & !OverheatProtection & !demand -> !HeaterOutput)
```

Prevents constant-ON or false heating when temperature is at or above setpoint.

**P10**

```text
G(protectPrev & cooldownDone -> !OverheatProtection)
```

Prevents permanent latch-up beyond 3s cooldown.

**PUB010.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

**PUB010.V2.1**

```text
G((TemperatureSensorInput>SetTemperature) -> !HeaterOutput)
```

Explicit correction of a demonstrated omission.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Heating threshold, cooldown boundary and safe restart | 6 |
| T2 | Sensor faults, valid endpoint values and equality retention | 7 |
| T3 | Fault during protection cannot clear the cooldown | 5 |
| V2_omission_regression | Reject the concrete wrong behavior documented in the 2026-11-06 specification review. | 3 |
| PUB010.T4 | PUB010.T4 | 11 |
| PUB010.R22.sensor_boundary | 100有效而100.1故障、冷却与重新需求 | 8 |
| PUB010.T5 | Interrupted heating resets 5000ms limit; full 5000ms after reset triggers OverheatProtection and 3000ms cooldown. | 8 |
| PUB010.T6 | Equality retains demand across sensorFault interruption while cooldown still elapses on physical clock. | 6 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB011 Automated Production Line Control

Origin: public. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "instructor_public_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": "medium[4] (zero based), flattened task 11",
  "source_sha256": "05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362",
  "adaptation": "Official en text and interface preserved verbatim; interpretations are separate assumptions.",
  "rationale": "A conveyor shares manual interlocking and an automatic three-station route.",
  "review": "Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending."
}
```

### Natural language source

# Automated Production Line Control

- **Difficulty:** Medium (medium)

## Requirements

A simple automated production line consists of three workstations: Workstation A, Workstation B, and Workstation C. The product needs to go through these three stations in sequence to be considered fully completed. There is a motor in the production line that is responsible for moving the product from one workstation to the next. The sequence of the line is from Workstation A to Workstation B, and then to Workstation C. Each workstation has a sensor (used to detect if the product has arrived) and a button (used to trigger the signal that the station's processing is complete).
Control requirements:
1. Mode Switching: The mode switch (Mode) is used to switch between manual and automatic modes of the production line.
2. Manual Mode: In manual mode, the forward rotation button (ForwardButton) controls the forward rotation of the motor, and the reverse rotation button (ReverseButton) controls the reverse rotation of the motor. Forward and reverse rotation operations need to be interlocked and cannot be performed simultaneously.
3. Automatic Mode:
   - When the product arrives at Workstation A, SensorA detects the product, and after the operator triggers the processing complete signal via ButtonA, the motor starts forward rotation to move the product to Workstation B.
   - When the product arrives at Workstation B, SensorB detects the product, the motor stops, and after the operator triggers the processing complete signal via ButtonB, the motor starts forward rotation to move the product to Workstation C.
   - When the product arrives at Workstation C, SensorC detects the product, the motor stops, and after the operator triggers the processing complete signal via ButtonC, the completion indicator light (CompletionLight) turns on, indicating that the product processing is complete. When the product is taken away, i.e., SensorC no longer detects the product, the completion indicator light (CompletionLight) turns off.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `Mode` | `BOOL` | Used to switch the production line between manual and automatic modes, 0=manual mode, 1=automatic mode |
| Input | `ForwardButton` | `BOOL` | Forward rotation button |
| Input | `ReverseButton` | `BOOL` | Reverse rotation button |
| Input | `SensorA` | `BOOL` | Sensor A |
| Input | `SensorB` | `BOOL` | Sensor B |
| Input | `SensorC` | `BOOL` | Sensor C |
| Input | `ButtonA` | `BOOL` | Button A |
| Input | `ButtonB` | `BOOL` | Button B |
| Input | `ButtonC` | `BOOL` | Button C |
| Output | `MotorForward` | `BOOL` | Motor forward rotation output |
| Output | `MotorReverse` | `BOOL` | Motor reverse rotation output |
| Output | `CompletionLight` | `BOOL` | Indicator light for product processing completion |

### Scenario

A conveyor shares manual interlocking and an automatic three-station route.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Mode | BOOL | Used to switch the production line between manual and automatic modes, 0=manual mode, 1=automatic mode |
| INPUT | ForwardButton | BOOL | Forward rotation button |
| INPUT | ReverseButton | BOOL | Reverse rotation button |
| INPUT | SensorA | BOOL | Sensor A |
| INPUT | SensorB | BOOL | Sensor B |
| INPUT | SensorC | BOOL | Sensor C |
| INPUT | ButtonA | BOOL | Button A |
| INPUT | ButtonB | BOOL | Button B |
| INPUT | ButtonC | BOOL | Button C |
| OUTPUT | MotorForward | BOOL | Motor forward rotation output |
| OUTPUT | MotorReverse | BOOL | Motor reverse rotation output |
| OUTPUT | CompletionLight | BOOL | Indicator light for product processing completion |

### Initial conditions

```json
{
  "MotorForward": false,
  "MotorReverse": false,
  "CompletionLight": false,
  "phase": "WAIT_A"
}
```

### Scan semantics

Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

### Safety and priorities

- Forward and reverse are mutually exclusive.
- Destination arrival stops movement before processing resumes.

### Explicit assumptions

- Opposing manual buttons produce neither direction.
- Buttons are level signals accepted only in their corresponding station wait. One phase transition is accepted per call.
- Entering manual mode clears automatic state and completion; return to automatic waits for A.
- Only one product is presented; station sensors are not contradictory.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `auto`: Mode
- `fwd`: MotorForward after scan
- `rev`: MotorReverse after scan
- `mf`: ForwardButton AND NOT ReverseButton
- `mr`: ReverseButton AND NOT ForwardButton
- `arrive`: pre-phase MOVE_AB AND SensorB OR pre-phase MOVE_BC AND SensorC
- `finish`: pre-phase WAIT_C AND SensorC AND ButtonC
- `light`: CompletionLight
- `removed`: NOT SensorC
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB011(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
参考阶段WAIT_A/MOVE_AB/WAIT_B/MOVE_BC/WAIT_C/DONE初始WAIT_A；按SensorA&ButtonA、SensorB、SensorB&ButtonB、SensorC、SensorC&ButtonC、!SensorC分别推进一阶。手动清参考阶段，正反转分别为ForwardButton&!ReverseButton及反向对称式，灯灭；自动仅移动阶段正转、不反转，DONE且SensorC时灯亮。
- `Mode`: I[k].Mode: sampled input (BOOL).
- `ForwardButton`: I[k].ForwardButton: sampled input (BOOL).
- `ReverseButton`: I[k].ReverseButton: sampled input (BOOL).
- `SensorA`: I[k].SensorA: sampled input (BOOL).
- `SensorB`: I[k].SensorB: sampled input (BOOL).
- `SensorC`: I[k].SensorC: sampled input (BOOL).
- `ButtonA`: I[k].ButtonA: sampled input (BOOL).
- `ButtonB`: I[k].ButtonB: sampled input (BOOL).
- `ButtonC`: I[k].ButtonC: sampled input (BOOL).
- `MotorForward`: O[k].MotorForward: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `MotorReverse`: O[k].MotorReverse: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `CompletionLight`: O[k].CompletionLight: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `init`: At the separate pre-invocation initial observation before scan k=0: Spre.phase="WAIT_A", O_init.MotorForward=false, O_init.MotorReverse=false, O_init.CompletionLight=false.
- `phase_wait`: post-phase is WAIT_A, WAIT_B, or WAIT_C
- `phase_move`: post-phase is MOVE_AB or MOVE_BC
- `wait_phase`: post-phase is WAIT_A, WAIT_B, or WAIT_C
- `move_phase`: post-phase is MOVE_AB or MOVE_BC
- `done_phase`: post-phase is DONE

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "MotorForward": false,
    "MotorReverse": false,
    "CompletionLight": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB011",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB011'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "CompletionLight",
    "MotorForward",
    "MotorReverse"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "phase": {
      "pre": "Spre.phase",
      "post": "Spost.phase",
      "enum": {
        "0": "WAIT_A",
        "1": "MOVE_AB",
        "2": "WAIT_B",
        "3": "MOVE_BC",
        "4": "WAIT_C",
        "5": "DONE"
      },
      "initial": 0
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "Opposing manual buttons produce neither direction.",
    "Buttons are level signals accepted only in their corresponding station wait. One phase transition is accepted per call.",
    "Entering manual mode clears automatic state and completion; return to automatic waits for A.",
    "Only one product is presented; station sensors are not contradictory.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "参考阶段WAIT_A/MOVE_AB/WAIT_B/MOVE_BC/WAIT_C/DONE初始WAIT_A；按SensorA&ButtonA、SensorB、SensorB&ButtonB、SensorC、SensorC&ButtonC、!SensorC分别推进一阶。手动清参考阶段，正反转分别为ForwardButton&!ReverseButton及反向对称式，灯灭；自动仅移动阶段正转、不反转，DONE且SensorC时灯亮。"
}
```

**PUB011.P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**PUB011.P1** Interlock

```text
G(!(fwd & rev))
```

Motor directions are mutually exclusive.

**PUB011.P2** Manual

```text
G(!auto -> ((fwd <-> mf) & (rev <-> mr)))
```

Manual level requests obey neutral conflict resolution.

**PUB011.P3** Auto direction

```text
G(auto -> !rev)
```

Automatic routing only moves forward.

**PUB011.P4** Arrival

```text
G(auto & arrive -> !fwd)
```

Arrival stops the motor in the observed scan.

**PUB011.P5** Completion

```text
G(auto & finish -> light)
```

C completion asserts the light.

**PUB011.P6** Removal

```text
G(auto & removed -> !light)
```

Removal clears completion.

**PUB011.P7**

```text
G(auto -> ((move_phase -> (fwd & !rev & !light)) & (wait_phase -> (!fwd & !rev & !light)) & (done_phase -> (!fwd & !rev & light))))
```

Prevents degenerate implementations that leave MotorForward FALSE in MOVE_* or mirror SensorC in DONE.

**PUB011.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB011.T1 | Neutral, forward, reverse, conflicting commands. | 3 |
| PUB011.T2 | Station waits, retained movement, completion and removal. | 10 |
| PUB011.T3 | Out-of-order confirmations cannot start the route. | 2 |
| PUB011.R22.bc_hold | B到C运输未到站的中间拍，电机应持续运行 | 7 |
| PUB011.T4 | PUB011.T4 | 12 |
| PUB011.R22.dwell_0 | 原流程各稳定状态连续保持：manual | 12 |
| PUB011.R22.dwell_1 | 原流程各稳定状态连续保持：cycle | 30 |
| PUB011.R22.dwell_2 | 原流程各稳定状态连续保持：wrong_button | 6 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB012 Slab Thickness Alarm and Fault History

Origin: public. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "instructor_public_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": "medium[5] (zero based), flattened task 12",
  "source_sha256": "05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362",
  "adaptation": "Official en text and interface preserved verbatim; interpretations are separate assumptions.",
  "rationale": "Thickness monitoring records faults, alarm minimum holding, normal-cutting time and bounded history.",
  "review": "Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending."
}
```

### Natural language source

# Slab Thickness Alarm and Fault History

- **Difficulty:** Medium (medium)

## Requirements

Monitor slab-thickness faults on a stone-cutting line, including minimum alarm holding, fault counting, normal-cutting runtime accumulation and a history of the five most recent faults.

1. When THICKNESS_SIGNAL_VALID is TRUE, THICKNESS_FAULT indicates that thickness deviation exceeds tolerance. Activate THICKNESS_ALARM immediately when the fault becomes TRUE, and hold each triggered alarm for at least 500 ms. Keep the alarm active while the fault persists.
2. On each FALSE-to-TRUE transition of a valid fault signal, increment Slab_Fault_Counter and store the current FaultTimestamp in element 0 of Slab_Fault_History. Shift older entries toward higher indices, retaining only the five most recent entries.
3. Accumulate Slab_Runtime_Accumulator using CycleTime only while CUTTING_RUN is TRUE, the thickness signal is valid and no thickness fault is present. Otherwise preserve the accumulated value.
4. At power-up or whenever THICKNESS_SIGNAL_VALID is FALSE, switch off the alarm and clear its holding state. Do not add fault records or accumulate normal runtime while the signal is invalid.
5. At power-up, initialize the fault count, accumulated runtime and all five history entries to zero. Statistics and history are for observation and maintenance only; they must not alter the cutting equipment's operating permissive, and external callers must not modify history entries.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `THICKNESS_FAULT` | `BOOL` | Thickness deviation exceeds the permitted tolerance. |
| Input | `THICKNESS_SIGNAL_VALID` | `BOOL` | Thickness-signal validity; FALSE means the signal is lost or unavailable. |
| Input | `CUTTING_RUN` | `BOOL` | Actual cutting-equipment running status. |
| Input | `FaultTimestamp` | `DINT` | Current timestamp in seconds, used as the fault-record identifier. |
| Input | `CycleTime` | `TIME` | Actual elapsed interval represented by this invocation; must be positive. |
| Output | `THICKNESS_ALARM` | `BOOL` | Thickness alarm with a minimum 500 ms hold duration. |
| Output | `Slab_Fault_Counter` | `UINT` | Number of valid thickness-fault occurrences. |
| Output | `Slab_Runtime_Accumulator` | `LTIME` | Accumulated normal-cutting runtime. |
| Output | `Slab_Fault_History` | `ARRAY[0..4] OF DINT` | Five most recent fault timestamps; index 0 is newest; read-only to callers. |

### Scenario

Thickness monitoring records faults, alarm minimum holding, normal-cutting time and bounded history.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | THICKNESS_FAULT | BOOL | Thickness deviation exceeds the permitted tolerance. |
| INPUT | THICKNESS_SIGNAL_VALID | BOOL | Thickness-signal validity; FALSE means the signal is lost or unavailable. |
| INPUT | CUTTING_RUN | BOOL | Actual cutting-equipment running status. |
| INPUT | FaultTimestamp | DINT | Current timestamp in seconds, used as the fault-record identifier. |
| INPUT | CycleTime | TIME | Actual elapsed interval represented by this invocation; must be positive. |
| OUTPUT | THICKNESS_ALARM | BOOL | Thickness alarm with a minimum 500 ms hold duration. |
| OUTPUT | Slab_Fault_Counter | UINT | Number of valid thickness-fault occurrences. |
| OUTPUT | Slab_Runtime_Accumulator | LTIME | Accumulated normal-cutting runtime. |
| OUTPUT | Slab_Fault_History | ARRAY[0..4] OF DINT | Five most recent fault timestamps; index 0 is newest; read-only to callers. |

### Initial conditions

```json
{
  "THICKNESS_ALARM": false,
  "Slab_Fault_Counter": 0,
  "Slab_Runtime_Accumulator": "LTIME#0ns",
  "Slab_Fault_History": [
    0,
    0,
    0,
    0,
    0
  ]
}
```

### Scan semantics

Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

### Safety and priorities

- Invalid signal overrides minimum alarm holding.
- A persistent valid fault keeps the alarm on.
- Statistics never control cutting permissives.

### Explicit assumptions

- The counted signal is valid AND fault; a valid fault after signal loss is a new occurrence.
- Hold starts at elapsed zero on the trigger call and releases at 500ms if the fault is absent. A fresh rising trigger restarts the hold.
- Invalid input cancels the hold immediately.
- Positive CycleTime is added on every current qualifying call, including a normal first invocation.
- UINT/LTIME overflow is outside these bounded cases and requires a separate policy.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- On timed benchmark tests, CycleTime equals dt_ms and uses exact integer nanoseconds within 32-bit unsigned TIME bounds. FaultTimestamp is a 32-bit signed DINT (-2147483648..2147483647).
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `valid`: THICKNESS_SIGNAL_VALID
- `fault`: THICKNESS_FAULT
- `alarm`: THICKNESS_ALARM
- `rise`: valid AND fault AND NOT previous(valid AND fault)
- `record`: count=pre-count+1; history[0]=FaultTimestamp; history[j]=pre-history[j-1] for j=1..4
- `same_stats`: count and history equal pre-scan values
- `hold`: Internal hold timer active (<500ms since last valid rising fault edge) while THICKNESS_SIGNAL_VALID is TRUE.
- `normal`: valid AND NOT fault AND CUTTING_RUN
- `add`: runtime=pre-runtime+CycleTime
- `same_time`: runtime=pre-runtime
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB012(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
validFault=VALID & FAULT，其新上升沿count加1，历史=[FaultTimestamp]+旧历史前4项，并记录hold起点。无效清hold；alarm=valid & (fault或hold年龄<500ms)。valid & !fault & CUTTING_RUN时runtime加CycleTime（约定与dt_ms一致），否则保持。初始count/runtime=0、历史五个0、previousValidFault=FALSE。计数/累计不得溢出，FaultTimestamp为DINT。
- `THICKNESS_FAULT`: I[k].THICKNESS_FAULT: sampled input (BOOL).
- `THICKNESS_SIGNAL_VALID`: I[k].THICKNESS_SIGNAL_VALID: sampled input (BOOL).
- `CUTTING_RUN`: I[k].CUTTING_RUN: sampled input (BOOL).
- `FaultTimestamp`: I[k].FaultTimestamp: sampled input (DINT).
- `CycleTime`: I[k].CycleTime: sampled input (TIME).
- `THICKNESS_ALARM`: O[k].THICKNESS_ALARM: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Slab_Fault_Counter`: O[k].Slab_Fault_Counter: independently observed post-scan candidate value (UINT); never defined as expected output.
- `Slab_Runtime_Accumulator`: O[k].Slab_Runtime_Accumulator: independently observed post-scan candidate value (LTIME); never defined as expected output.
- `Slab_Fault_History`: O[k].Slab_Fault_History: independently observed post-scan candidate value (ARRAY[0..4] OF DINT); never defined as expected output.
- `count`: O[k].Slab_Fault_Counter
- `history`: O[k].Slab_Fault_History
- `runtime`: O[k].Slab_Runtime_Accumulator
- `timing`: Internal hold start Sref.timed_contract.since records the most recent valid THICKNESS_FAULT rising-edge timestamp; a fresh rising edge during an active 500ms hold restarts the 500ms timer. Invalid input clears hold immediately.
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.THICKNESS_ALARM=false, O_init.Slab_Fault_Counter=0, O_init.Slab_Runtime_Accumulator="LTIME#0ns", O_init.Slab_Fault_History=[0, 0, 0, 0, 0].

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "THICKNESS_ALARM": false,
    "Slab_Fault_Counter": 0,
    "Slab_Runtime_Accumulator": "LTIME#0ns",
    "Slab_Fault_History": [
      0,
      0,
      0,
      0,
      0
    ]
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB012",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": {
        "class": "TimedContract",
        "state": {
          "task_id": "PUB012",
          "clock": {
            "decimal": "0"
          },
          "first": true,
          "since": null,
          "debounce": null,
          "runtime": 0,
          "count": 0,
          "previous_run": false,
          "previous_fault": false,
          "history": [
            0,
            0,
            0,
            0,
            0
          ]
        }
      },
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB012'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Slab_Fault_Counter",
    "Slab_Fault_History",
    "Slab_Runtime_Accumulator",
    "THICKNESS_ALARM"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "timing": {
      "clock": "Spost.timed_contract.clock (exact integer nanoseconds; first invocation 0)",
      "start": "Spost.timed_contract.since; None means inactive",
      "qualified": "start is not None AND clock-start >= duration_ns(limit)",
      "hold": "start is not None AND clock-start < 500000000",
      "initial_start": null,
      "initial_clock": 0,
      "limit": "DebounceTime for PUB004/PUB005, 5000000000ns for PUB006, 30000000000ns for PUB013",
      "previous_fault": "Spre.timed_contract.previous_fault, initially FALSE; next=THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT",
      "pre_count": "Spre.timed_contract.count",
      "pre_history": "Spre.timed_contract.history",
      "pre_runtime": "Spre.timed_contract.runtime"
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The counted signal is valid AND fault; a valid fault after signal loss is a new occurrence.",
    "Hold starts at elapsed zero on the trigger call and releases at 500ms if the fault is absent. A fresh rising trigger restarts the hold.",
    "Invalid input cancels the hold immediately.",
    "Positive CycleTime is added on every current qualifying call, including a normal first invocation.",
    "UINT/LTIME overflow is outside these bounded cases and requires a separate policy.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "On timed benchmark tests, CycleTime equals dt_ms and uses exact integer nanoseconds within 32-bit unsigned TIME bounds. FaultTimestamp is a 32-bit signed DINT (-2147483648..2147483647).",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "validFault=VALID & FAULT，其新上升沿count加1，历史=[FaultTimestamp]+旧历史前4项，并记录hold起点。无效清hold；alarm=valid & (fault或hold年龄<500ms)。valid & !fault & CUTTING_RUN时runtime加CycleTime（约定与dt_ms一致），否则保持。初始count/runtime=0、历史五个0、previousValidFault=FALSE。计数/累计不得溢出，FaultTimestamp为DINT。"
}
```

**PUB012.P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**PUB012.P1** Signal loss

```text
G(!valid -> !alarm)
```

Invalid signal cancels alarm immediately.

**PUB012.P2** Fault hold

```text
G(valid & (fault | hold) -> alarm)
```

The alarm persists during fault and hold.

**PUB012.P3** Occurrence

```text
G(rise -> record)
```

Each valid rising fault shifts the bounded history.

**PUB012.P4** No spurious record

```text
G(!rise -> same_stats)
```

Held faults and invalid inputs do not create records.

**PUB012.P5** Runtime

```text
G((normal -> add) & (!normal -> same_time))
```

Normal runtime counts only eligible intervals.

**PUB012.P6** Release

```text
G(valid & !fault & !hold -> !alarm)
```

Alarm releases when neither fault nor hold remains.

**PUB012.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB012.T1 | Check 500ms release and immediate signal-loss override. | 7 |
| PUB012.T2 | Six faults retain the five newest timestamps. | 13 |
| PUB012.T3 | Only valid fault-free running accumulates. | 5 |
| PUB012.T4 | PUB012.T4 | 11 |
| PUB012.R22.retrigger | 持续故障仅计一次、保持内重触发、信号恢复仍故障 | 11 |
| PUB012.T5 | Seven valid rising fault edges push oldest timestamps out of the 5-entry Slab_Fault_History shift window. | 14 |
| PUB012.T6 | Invalid signal suppresses alarm, count, timestamp and runtime accumulation; normal running cut accumulates time. | 5 |
| PUB012.T7 | Sustained high fault counts only once; 499ms/500ms hold window boundary releases alarm cleanly. | 4 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB013 Office HVAC Multi-mode Energy-Saving Control

Origin: public. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "instructor_public_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": "medium[6] (zero based), flattened task 13",
  "source_sha256": "05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362",
  "adaptation": "Official en text and interface preserved verbatim; interpretations are separate assumptions.",
  "rationale": "An office fan uses a restartable occupancy delay and mode-dependent temperature setback.",
  "review": "Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending."
}
```

### Natural language source

# Office HVAC Multi-mode Energy-Saving Control

- **Difficulty:** Medium (medium)

## Requirements

Control an office-building supply fan and generate a temperature-setpoint adjustment from occupancy, operating mode and the energy-saving selection.

1. Valid HVAC_MODE_SELECTOR values are 0 (Auto), 1 (Comfort), 2 (Economy) and 3 (Night).
2. Start a 30-second delay only when occupancy is detected and Night mode is not selected. SUPPLY_FAN_RUN becomes TRUE only after these conditions remain satisfied for 30 seconds. Immediately stop the fan and reset timing if occupancy is lost or Night mode is selected. Wait the full 30 seconds again when the conditions recover.
3. Auto mode: use a 0°C adjustment when occupied. When unoccupied, use +3°C in energy-saving mode or +2°C in standard mode.
4. Comfort mode: use 0°C when occupied or +1°C when unoccupied. Economy mode: use 0°C when occupied or +4°C when unoccupied.
5. Night mode: use +4°C regardless of occupancy. The energy-saving selection affects only Auto mode.
6. Keep TEMP_SETPOINT_ADJUST within ±4°C. Initialize outputs to OFF and zero at power-up; update them from current inputs when normal calculation begins.
7. The start delay controls only the BOOL fan enable; no continuous speed ramp is required.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `OCCUPANCY_DETECTED` | `BOOL` | Occupancy-detection result derived from the CO₂ sensor. |
| Input | `ENERGY_SAVING_MODE` | `BOOL` | TRUE selects energy saving; FALSE selects standard operation; affects Auto mode only. |
| Input | `HVAC_MODE_SELECTOR` | `INT` | 0 Auto, 1 Comfort, 2 Economy, 3 Night; callers supply a valid value. |
| Output | `SUPPLY_FAN_RUN` | `BOOL` | Supply-fan run enable. |
| Output | `TEMP_SETPOINT_ADJUST` | `INT` | Temperature-setpoint adjustment in °C. |

### Scenario

An office fan uses a restartable occupancy delay and mode-dependent temperature setback.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | OCCUPANCY_DETECTED | BOOL | Occupancy-detection result derived from the CO₂ sensor. |
| INPUT | ENERGY_SAVING_MODE | BOOL | TRUE selects energy saving; FALSE selects standard operation; affects Auto mode only. |
| INPUT | HVAC_MODE_SELECTOR | INT | 0 Auto, 1 Comfort, 2 Economy, 3 Night; callers supply a valid value. |
| OUTPUT | SUPPLY_FAN_RUN | BOOL | Supply-fan run enable. |
| OUTPUT | TEMP_SETPOINT_ADJUST | INT | Temperature-setpoint adjustment in °C. |

### Initial conditions

```json
{
  "SUPPLY_FAN_RUN": false,
  "TEMP_SETPOINT_ADJUST": 0
}
```

### Scan semantics

Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

### Safety and priorities

- Occupancy loss or Night immediately stops fan and resets delay.
- Energy saving affects only Auto setback.

### Explicit assumptions

- Selector values are always 0..3 as required by the official input contract.
- Outputs are initialized before the first call, which calculates adjustment immediately.
- The timer starts at elapsed zero on the first non-Night occupied call. Fan starts at the first observation at or after 30s.
- dt_ms is actual elapsed time since the preceding call; real runtime timer tests must preserve this timing.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `permit`: OCCUPANCY_DETECTED AND HVAC_MODE_SELECTOR<>3
- `mature`: continuous permit elapsed>=30s
- `fan`: SUPPLY_FAN_RUN
- `bounded`: -4<=TEMP_SETPOINT_ADJUST<=4
- `occupied`: OCCUPANCY_DETECTED AND mode<>3
- `zero`: TEMP_SETPOINT_ADJUST=0
- `night`: mode=3
- `four`: adjust=4
- `auto_save`: mode=0 AND NOT occupancy AND ENERGY_SAVING_MODE
- `three`: adjust=3
- `auto_standard`: mode=0 AND NOT occupancy AND NOT ENERGY_SAVING_MODE
- `two`: adjust=2
- `comfort`: mode=1 AND NOT occupancy
- `one`: adjust=1
- `economy`: mode=2 AND NOT occupancy
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB013(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
mode域0..3；permit=occupied & mode!=3，首次许可年龄0、失去立即清计时；fan=permit且年龄>=30s。adjust=mode3则4，否则有人则0，否则mode0取节能3/普通2、mode1取1、mode2取4。初始化adjust=0与首次调用计算分开。
- `TimeTick`: Boolean: floor(t[k]/1ms)>floor(t[k-1]/1ms), with t[0]=0, TimeTick[0]=FALSE, t[k]=sum(dt_ms[1..k]). G(F(TimeTick)) states unbounded physical time progress; merely positive dt is insufficient.
- `OCCUPANCY_DETECTED`: I[k].OCCUPANCY_DETECTED: sampled input (BOOL).
- `ENERGY_SAVING_MODE`: I[k].ENERGY_SAVING_MODE: sampled input (BOOL).
- `HVAC_MODE_SELECTOR`: I[k].HVAC_MODE_SELECTOR: sampled input (INT).
- `SUPPLY_FAN_RUN`: O[k].SUPPLY_FAN_RUN: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `TEMP_SETPOINT_ADJUST`: O[k].TEMP_SETPOINT_ADJUST: independently observed post-scan candidate value (INT); never defined as expected output.
- `mode`: I[k].HVAC_MODE_SELECTOR
- `occupancy`: I[k].OCCUPANCY_DETECTED
- `adjust`: O[k].TEMP_SETPOINT_ADJUST
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.SUPPLY_FAN_RUN=false, O_init.TEMP_SETPOINT_ADJUST=0.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "SUPPLY_FAN_RUN": false,
    "TEMP_SETPOINT_ADJUST": 0
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB013",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": {
        "class": "TimedContract",
        "state": {
          "task_id": "PUB013",
          "clock": {
            "decimal": "0"
          },
          "first": true,
          "since": null,
          "debounce": null,
          "runtime": 0,
          "count": 0,
          "previous_run": false,
          "previous_fault": false,
          "history": [
            0,
            0,
            0,
            0,
            0
          ]
        }
      },
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB013'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "SUPPLY_FAN_RUN",
    "TEMP_SETPOINT_ADJUST"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "timing": {
      "clock": "Spost.timed_contract.clock (exact integer nanoseconds; first invocation 0)",
      "start": "Spost.timed_contract.since; None means inactive",
      "qualified": "start is not None AND clock-start >= duration_ns(limit)",
      "hold": "start is not None AND clock-start < 500000000",
      "initial_start": null,
      "initial_clock": 0,
      "limit": "DebounceTime for PUB004/PUB005, 5000000000ns for PUB006, 30000000000ns for PUB013",
      "previous_fault": "Spre.timed_contract.previous_fault, initially FALSE; next=THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT",
      "pre_count": "Spre.timed_contract.count",
      "pre_history": "Spre.timed_contract.history",
      "pre_runtime": "Spre.timed_contract.runtime"
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "Selector values are always 0..3 as required by the official input contract.",
    "Outputs are initialized before the first call, which calculates adjustment immediately.",
    "The timer starts at elapsed zero on the first non-Night occupied call. Fan starts at the first observation at or after 30s.",
    "dt_ms is actual elapsed time since the preceding call; real runtime timer tests must preserve this timing.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "mode域0..3；permit=occupied & mode!=3，首次许可年龄0、失去立即清计时；fan=permit且年龄>=30s。adjust=mode3则4，否则有人则0，否则mode0取节能3/普通2、mode1取1、mode2取4。初始化adjust=0与首次调用计算分开。"
}
```

**PUB013.P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**PUB013.P1** Fan delay

```text
G(fan <-> (permit & mature))
```

Fan follows the complete uninterrupted delay.

**PUB013.P2** Bounds

```text
G(bounded)
```

Legal outputs satisfy the required range.

**PUB013.P3** Occupied and Night

```text
G((occupied -> zero) & (night -> four))
```

Night overrides occupied setback.

**PUB013.P4** Auto

```text
G((auto_save -> three) & (auto_standard -> two))
```

Auto unoccupied setback follows energy saving.

**PUB013.P5** Fixed modes

```text
G((comfort -> one) & (economy -> four))
```

Comfort and Economy ignore energy saving.

**PUB013.P6** Liveness

```text
(G(F(TimeTick))) -> (G((G permit) -> F fan))
```

If permit stays TRUE from any scan onward, the fan eventually runs, assuming continued calls and diverging physical time. Explicit non-Zeno environment premise: physical elapsed time crosses infinitely many 1ms boundaries.

**PUB013.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB013.T1 | Exercise all setback modes and energy saving scope. | 7 |
| PUB013.T2 | Check delay boundary, loss, full restart, Night override. | 8 |
| V2_permit_loss_at_deadline | Permission loss at the exact deadline wins; recovery starts a fresh full interval, even after a long gap. | 5 |
| PUB013.T3 | PUB013.T3 | 24 |
| PUB013.R22.hvac_mode_reset | 当前参考要求非夜间模式切换不重置持续有人计时；需人审其来源 | 2 |
| PUB013.R22.matrix_0 | 模式0的占用与节能四组合 | 4 |
| PUB013.R22.matrix_1 | 模式1的占用与节能四组合 | 4 |
| PUB013.R22.matrix_2 | 模式2的占用与节能四组合 | 4 |
| PUB013.R22.matrix_3 | 模式3的占用与节能四组合 | 4 |
| PUB013.R22.timer_0 | 模式0持续有人、失去占用及重新计时 | 6 |
| PUB013.R22.timer_1 | 模式1持续有人、失去占用及重新计时 | 6 |
| PUB013.R22.timer_2 | 模式2持续有人、失去占用及重新计时 | 6 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB014 IPv4 Parsing with Format and Range Checks

Origin: public. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "instructor_public_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": "medium[7] (zero based), flattened task 14",
  "source_sha256": "05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362",
  "adaptation": "Official en text and interface preserved verbatim; interpretations are separate assumptions.",
  "rationale": "Strict decimal IPv4 parsing into a network-order unsigned address.",
  "review": "Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending."
}
```

### Natural language source

# IPv4 Parsing with Format and Range Checks

- **Difficulty:** Medium (medium)

## Requirements

Design a PLC function block in Structured Text (ST) that parses a dotted-decimal IPv4 string into a 32-bit unsigned integer.

1. ipText must contain four nonempty decimal-digit segments separated by periods. Each segment must have a value from 0 through 255.
2. Assemble the address in network byte order: the first segment occupies the most significant 8 bits and the fourth occupies the least significant 8 bits. Write the result to ipValue.
3. Set ipValue to 0 for malformed input, a nondigit segment, an incorrect segment count or any out-of-range segment. The valid address 0.0.0.0 also produces 0.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `ipText` | `STRING(254)` | IPv4 text to parse, with a capacity of 254 characters. A valid dotted-decimal address requires at most 15 characters. |
| Output | `ipValue` | `UDINT` | 32-bit address in network byte order; zero for invalid input. |

### Scenario

Strict decimal IPv4 parsing into a network-order unsigned address.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | ipText | STRING(254) | IPv4 text to parse, with a capacity of 254 characters. A valid dotted-decimal address requires at most 15 characters. |
| OUTPUT | ipValue | UDINT | 32-bit address in network byte order; zero for invalid input. |

### Initial conditions

```json
{
  "ipValue": 0
}
```

### Scan semantics

Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

### Safety and priorities

- Malformed or out-of-range data forces zero in the same invocation.

### Explicit assumptions

- Leading zeros are allowed because the official text requires decimal-digit segments without prohibiting them.
- Signs, whitespace, hexadecimal notation and embedded nondigits are rejected.
- Input STRING capacity (<=254 UTF-8 bytes) is checked before truncating at the first NUL byte. Embedded NUL terminates the visible IPv4 text; arbitrary leading zeros are permitted within capacity, and each digit character must be ASCII '0'..'9'.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `valid`: exactly four nonempty decimal-digit segments separated by periods, each parsed value 0..255
- `packed`: ipValue=a*16777216+b*65536+c*256+d for the four parsed octets
- `zero`: ipValue=0
- `same_input`: k>=1 AND I[k].ipText=I[k-1].ipText
- `same_output`: k>=1 AND O[k].ipValue=O[k-1].ipValue
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB014(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
文本总长<=254字节（先检查容量上限，再按首个NUL截断，支持超过15字符的前导零）。恰四个非空ASCII('0'..'9')数字段，每段按a=10*a+digit递推，任何段>255或非数字即非法。合法期望ipValue=((a*256+b)*256+c)*256+d，否则0；无跨拍状态。
- `ipText`: I[k].ipText: sampled input (STRING(254)).
- `ipValue`: O[k].ipValue: independently observed post-scan candidate value (UDINT); never defined as expected output.
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.ipValue=0.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "ipValue": 0
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB014",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": {
        "class": "DataContract",
        "state": {
          "task_id": "PUB014",
          "previous": 0,
          "high": false,
          "low": false,
          "trigger": false,
          "window": null,
          "history": [],
          "average": 0.0,
          "reached": false,
          "recipes": [
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            }
          ],
          "last_query": {
            "recipeID": 0,
            "ingredientType": 0,
            "ingredientRatio": 0.0,
            "productionTemperature": 0.0
          },
          "prev_add": false,
          "prev_delete": false,
          "prev_modify": false,
          "prev_query": false,
          "recipes_initialized": false,
          "queue": [],
          "prev_enq": false,
          "prev_deq": false
        }
      },
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB014'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "ipValue"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "Leading zeros are allowed because the official text requires decimal-digit segments without prohibiting them.",
    "Signs, whitespace, hexadecimal notation and embedded nondigits are rejected.",
    "Input STRING capacity (<=254 UTF-8 bytes) is checked before truncating at the first NUL byte. Embedded NUL terminates the visible IPv4 text; arbitrary leading zeros are permitted within capacity, and each digit character must be ASCII '0'..'9'.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "文本总长<=254字节（先检查容量上限，再按首个NUL截断，支持超过15字符的前导零）。恰四个非空ASCII('0'..'9')数字段，每段按a=10*a+digit递推，任何段>255或非数字即非法。合法期望ipValue=((a*256+b)*256+c)*256+d，否则0；无跨拍状态。"
}
```

**PUB014.P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**PUB014.P1** Valid assembly

```text
G(valid -> packed)
```

The first octet is the most significant byte.

**PUB014.P2** Invalid input

```text
G(!valid -> zero)
```

Invalid data never preserves an old result.

**PUB014.P3** Stateless parsing

```text
G(same_input -> same_output)
```

Repeated strings produce repeated results.

**PUB014.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB014.T1 | Zero, maximum, byte order and decimal leading zeros. | 5 |
| PUB014.T2 | Malformed and overflowing segments clear a previous valid result. | 14 |
| V2_data_contract_boundaries | Independently calculated edge/history/parser boundary regression | 4 |
| PUB014.T3 | PUB014.T3 | 9 |
| PUB014.R22.clear_invalid | 合法重复调用及各类非法输入当拍清零 | 11 |
| PUB014.T4 | First-NUL truncation and ultra-long (>15 char) leading-zero valid IPv4 octets within 254-byte limit. | 4 |
| PUB014.T5 | Comprehensive syntactic rejections (whitespace, +/- sign, empty octet, 3/5 parts, 256 overflow) interleaved with valid parses. | 10 |
| PUB014.T6 | Loopback, classful masks, and high-bit (>= 2^31) unsigned 32-bit big-endian packing check. | 4 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB015 Material Proportioning Process Control

Origin: public. Difficulty: hard.

### Source and adaptation

```json
{
  "source_type": "instructor_public_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": "hard[0] (zero based), flattened task 15",
  "source_sha256": "05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362",
  "adaptation": "Official en text and interface preserved verbatim; interpretations are separate assumptions.",
  "rationale": "A mixer toggles manual actuators or sequences two/three-material filling, mixing and discharge.",
  "review": "Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending."
}
```

### Natural language source

# Material Proportioning Process Control

- **Difficulty:** Hard (hard)

## Requirements

Design a PLC program to control a material proportioning process that requires mixing three types of materials according to specific requirements and then delivering them to the next process through valve D. The system needs to support both manual and automatic operation modes and be able to safely stop all equipment when an emergency stop signal is triggered.
Control requirements:
Emergency Stop Logic: The estop(=FALSE) signal is used for emergency stopping of all equipment.
Manual Mode: opeMode=false, manually control the start/stop of valves A, B, C, D, and the mixing motor.
Automatic Mode: opeMode=true, equipment operates automatically according to the process flow.
Implement the emergency stop logic to ensure that all equipment stops immediately when the emergency stop signal is triggered.
In manual mode, manually control the start/stop of valves and the mixing motor.
For example, pressing the valve A start button valveAStart (triggering a rising edge) causes valve A to run (valveARun=TRUE); pressing the valve A start button valveAStart again (triggering a rising edge) stops valve A (valveARun=FALSE).
In automatic mode, implement the following control logic based on the process flow:
Press the autoStart button to start the automatic process, first opening valve A.
When the liquid level sensor levelSensor reaches 50cm, close valve A and open valve B.
When the liquid level sensor reaches 80cm, close valve B.
Based on processMode:
If processMode=false, start the mixing motor; after receiving the mixing complete signal, stop the mixing motor, open valve D, and the automatic process ends.
If processMode=true, open valve C; when the liquid level sensor reaches 100cm, close valve C, start the mixing motor; after receiving the mixing complete signal, stop the mixing motor, open valve D, and the automatic process ends.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `estop` | `BOOL` | Emergency Stop Signal<br>FALSE: Emergency stop triggered<br>TRUE: No emergency stop triggered |
| Input | `opeMode` | `BOOL` | Operation Mode<br>FALSE: Manual Operation Mode<br>TRUE: Automatic Operation Mode |
| Input | `valveAStart` | `BOOL` | Valve A Start Button |
| Input | `valveBStart` | `BOOL` | Valve B Start Button |
| Input | `valveCStart` | `BOOL` | Valve C Start Button |
| Input | `valveDStart` | `BOOL` | Valve D Start Button |
| Input | `mixMotorStart` | `BOOL` | Mixing Motor Start Button |
| Input | `autoStart` | `BOOL` | Automatic Start Button |
| Input | `processMode` | `BOOL` | Process Mode |
| Input | `levelSensor` | `INT` | Liquid Level Sensor (unit cm) |
| Input | `mixMotorComplete` | `BOOL` | Mixing Complete Signal |
| Output | `valveARun` | `BOOL` | Valve A Run Command |
| Output | `valveBRun` | `BOOL` | Valve B Run Command |
| Output | `valveCRun` | `BOOL` | Valve C Run Command |
| Output | `valveDRun` | `BOOL` | Valve D Run Command |
| Output | `mixMotorRun` | `BOOL` | Mixing Motor Run Command |

### Scenario

A mixer toggles manual actuators or sequences two/three-material filling, mixing and discharge.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | estop | BOOL | Emergency Stop Signal<br>FALSE: Emergency stop triggered<br>TRUE: No emergency stop triggered |
| INPUT | opeMode | BOOL | Operation Mode<br>FALSE: Manual Operation Mode<br>TRUE: Automatic Operation Mode |
| INPUT | valveAStart | BOOL | Valve A Start Button |
| INPUT | valveBStart | BOOL | Valve B Start Button |
| INPUT | valveCStart | BOOL | Valve C Start Button |
| INPUT | valveDStart | BOOL | Valve D Start Button |
| INPUT | mixMotorStart | BOOL | Mixing Motor Start Button |
| INPUT | autoStart | BOOL | Automatic Start Button |
| INPUT | processMode | BOOL | Process Mode |
| INPUT | levelSensor | INT | Liquid Level Sensor (unit cm) |
| INPUT | mixMotorComplete | BOOL | Mixing Complete Signal |
| OUTPUT | valveARun | BOOL | Valve A Run Command |
| OUTPUT | valveBRun | BOOL | Valve B Run Command |
| OUTPUT | valveCRun | BOOL | Valve C Run Command |
| OUTPUT | valveDRun | BOOL | Valve D Run Command |
| OUTPUT | mixMotorRun | BOOL | Mixing Motor Run Command |

### Initial conditions

```json
{
  "valveARun": false,
  "valveBRun": false,
  "valveCRun": false,
  "valveDRun": false,
  "mixMotorRun": false,
  "phase": "IDLE"
}
```

### Scan semantics

Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

### Safety and priorities

- estop=FALSE turns every actuator off immediately.
- Automatic phases drive only one actuator; independent manual toggles may coexist.

### Explicit assumptions

- All manual buttons use rising-edge independent toggles. Edge history updates during emergency stop so held buttons cannot restart outputs on recovery.
- Emergency stop resets all manual latches and automatic state. A fresh autoStart edge is required to restart.
- Changing operation mode clears old latches and sequence.
- autoStart is a rising edge accepted in IDLE or DRAIN to start a fresh batch from FILL_A; processMode stays latched for the active batch (phases 1..5).
- Thresholds are >=50, >=80 and >=100 cm. One logical phase transition occurs per invocation.
- In DRAIN, valveDRun remains TRUE until emergency stop (estop=FALSE), mode switch to manual (opeMode=FALSE), or a fresh autoStart rising edge starting a new batch.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- V2 mode-change priority: emergency stop first; then a change of mode after the first invocation clears sequence/latches and suppresses commands for that invocation; edge memories still update. The first invocation establishes the selected mode and executes normally. New commands are accepted on subsequent invocations subject to their edge rules.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `safe`: estop
- `off`: all actuator outputs FALSE
- `toggle`: No mode change this invocation AND (safe AND NOT opeMode AND rising(valveAStart))
- `changed`: valveARun=NOT pre-valveARun
- `held`: safe AND NOT opeMode AND NOT rising(valveAStart) AND no mode change
- `same`: valveARun=pre-valveARun
- `toB`: No mode change this invocation AND (safe AND opeMode AND pre-phase FILL_A AND levelSensor>=50)
- `B`: valveBRun only
- `toMix`: No mode change this invocation AND (safe AND opeMode AND pre-phase FILL_B AND levelSensor>=80 AND NOT latched_batch_mode)
- `Mix`: mixMotorRun only
- `toC`: No mode change this invocation AND (safe AND opeMode AND pre-phase FILL_B AND levelSensor>=80 AND latched_batch_mode)
- `C`: valveCRun only
- `fromC`: No mode change this invocation AND (safe AND opeMode AND pre-phase FILL_C AND levelSensor>=100)
- `mixed`: No mode change this invocation AND (safe AND opeMode AND pre-phase MIX AND mixMotorComplete)
- `Drain`: valveDRun only
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB015(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
五按钮及autoStart历史初值FALSE、每拍更新。急停优先，其次已建立模式的变化；二者清阶段/五锁存且当拍全关。手动逐项latchAfter=latchBefore XOR buttonRise。自动IDLE或DRAIN遇autoStartRise进A（新批次），A液位>=50进B，B>=80按批次processMode进C或MIX，C>=100进MIX，MIX完成进DRAIN；每拍一阶，DRAIN保持valveDRun=TRUE至切换手动、急停或autoStart上升沿重起。五输出对应转移后A/B/C/DRAIN/MIX。批次模式在活动批次(1..4)内固定。
- `estop`: I[k].estop: sampled input (BOOL).
- `opeMode`: I[k].opeMode: sampled input (BOOL).
- `valveAStart`: I[k].valveAStart: sampled input (BOOL).
- `valveBStart`: I[k].valveBStart: sampled input (BOOL).
- `valveCStart`: I[k].valveCStart: sampled input (BOOL).
- `valveDStart`: I[k].valveDStart: sampled input (BOOL).
- `mixMotorStart`: I[k].mixMotorStart: sampled input (BOOL).
- `autoStart`: I[k].autoStart: sampled input (BOOL).
- `processMode`: I[k].processMode: sampled input (BOOL).
- `levelSensor`: I[k].levelSensor: sampled input (INT).
- `mixMotorComplete`: I[k].mixMotorComplete: sampled input (BOOL).
- `valveARun`: O[k].valveARun: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `valveBRun`: O[k].valveBRun: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `valveCRun`: O[k].valveCRun: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `valveDRun`: O[k].valveDRun: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `mixMotorRun`: O[k].mixMotorRun: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `oneActuator`: at most one of valveARun, valveBRun, valveCRun, valveDRun, mixMotorRun is TRUE
- `manual_toggles`: Each of valveARun/B/C/D/mixMotorRun toggles XOR on its own button rising edge and holds otherwise while in Manual without modeChanged.
- `init`: At the separate pre-invocation initial observation before scan k=0: Spre.phase="IDLE", O_init.valveARun=false, O_init.valveBRun=false, O_init.valveCRun=false, O_init.valveDRun=false, O_init.mixMotorRun=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB015",
      "array_contract": null,
      "process_contract": {
        "class": "ProcessContract",
        "state": {
          "task_id": "PUB015",
          "phase": 0,
          "mode": null,
          "previous": {},
          "latches": [
            false,
            false,
            false,
            false,
            false
          ],
          "batch_mode": null,
          "route": null,
          "index": 0,
          "station": 1,
          "target": 1,
          "temperature": 0.0,
          "arm_mode": null,
          "arm_step": 0,
          "step_index": 1,
          "step_busy": false,
          "prev_start": false
        }
      },
      "timed_contract": null,
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB015'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "mixMotorRun",
    "valveARun",
    "valveBRun",
    "valveCRun",
    "valveDRun"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "phase": {
      "pre": "Spre.process_contract.phase",
      "post": "Spost.process_contract.phase",
      "enum": {
        "0": "IDLE",
        "1": "FILL_A",
        "2": "FILL_B",
        "3": "FILL_C",
        "4": "MIX",
        "5": "DRAIN"
      },
      "initial": 0
    },
    "modeChanged": "Spre.process_contract.mode is not None AND Spre.process_contract.mode != I[k].opeMode"
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "All manual buttons use rising-edge independent toggles. Edge history updates during emergency stop so held buttons cannot restart outputs on recovery.",
    "Emergency stop resets all manual latches and automatic state. A fresh autoStart edge is required to restart.",
    "Changing operation mode clears old latches and sequence.",
    "autoStart is a rising edge accepted in IDLE or DRAIN to start a fresh batch from FILL_A; processMode stays latched for the active batch (phases 1..5).",
    "Thresholds are >=50, >=80 and >=100 cm. One logical phase transition occurs per invocation.",
    "In DRAIN, valveDRun remains TRUE until emergency stop (estop=FALSE), mode switch to manual (opeMode=FALSE), or a fresh autoStart rising edge starting a new batch.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "V2 mode-change priority: emergency stop first; then a change of mode after the first invocation clears sequence/latches and suppresses commands for that invocation; edge memories still update. The first invocation establishes the selected mode and executes normally. New commands are accepted on subsequent invocations subject to their edge rules.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "五按钮及autoStart历史初值FALSE、每拍更新。急停优先，其次已建立模式的变化；二者清阶段/五锁存且当拍全关。手动逐项latchAfter=latchBefore XOR buttonRise。自动IDLE或DRAIN遇autoStartRise进A（新批次），A液位>=50进B，B>=80按批次processMode进C或MIX，C>=100进MIX，MIX完成进DRAIN；每拍一阶，DRAIN保持valveDRun=TRUE至切换手动、急停或autoStart上升沿重起。五输出对应转移后A/B/C/DRAIN/MIX。批次模式在活动批次(1..4)内固定。"
}
```

**PUB015.P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**PUB015.P1** Emergency

```text
G(!safe -> off)
```

Emergency permissive dominates mode and buttons.

**PUB015.P2** Manual toggle

```text
G((toggle -> changed) & (held -> same))
```

A held button cannot repeatedly toggle; applies independently to all five buttons.

**PUB015.P3** First fill threshold

```text
G(toB -> B)
```

A closes and B opens at or above 50cm.

**PUB015.P4** Two-material branch

```text
G(toMix -> Mix)
```

The two-material branch skips C.

**PUB015.P5** Three-material branch

```text
G((toC -> C) & (fromC -> Mix))
```

C fills to 100cm before mixing.

**PUB015.P6** Mix completion

```text
G(mixed -> Drain)
```

Mix completion stops mixing and opens D.

**PUB015.P7**

```text
G(manual_toggles)
```

Extends P2 manual coverage from valveA to all five actuators (A, B, C, D, Mix).

**PUB015.P8**

```text
G((safe & opeMode -> oneActuator) & (modeChanged -> off))
```

Guarantees single-actuator automatic progression and mode-change isolation.

**PUB015.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB015.T1 | Held signal, second edge, all actuator requests and emergency. | 7 |
| PUB015.T2 | Equality thresholds and mixing completion. | 7 |
| PUB015.T3 | Skipped thresholds advance and emergency cancels the active cycle. | 8 |
| V2_process_history_regression | Mode/edge reset, repeated station or prior-batch retained setpoint regression. | 10 |
| PUB015.T5 | PUB015.T5 | 14 |
| PUB015.R22.manual_mix_hold | 手动搅拌按钮持续按住，不能每拍翻转 | 7 |
| PUB015.R22.valveAStart | 手动独立翻转、长按与再次关闭：valveAStart | 8 |
| PUB015.R22.valveBStart | 手动独立翻转、长按与再次关闭：valveBStart | 8 |
| PUB015.R22.valveCStart | 手动独立翻转、长按与再次关闭：valveCStart | 8 |
| PUB015.R22.valveDStart | 手动独立翻转、长按与再次关闭：valveDStart | 8 |
| PUB015.R22.mixMotorStart | 手动独立翻转、长按与再次关闭：mixMotorStart | 8 |
| PUB015.R22.auto_wait_False | 配料完整路线、各阶段等待及切换模式后新批次 | 16 |
| PUB015.R22.auto_wait_True | 配料完整路线、各阶段等待及切换模式后新批次 | 18 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB016 Flexible Processing Control

Origin: public. Difficulty: hard.

### Source and adaptation

```json
{
  "source_type": "instructor_public_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": "hard[1] (zero based), flattened task 16",
  "source_sha256": "05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362",
  "adaptation": "Official en text and interface preserved verbatim; interpretations are separate assumptions.",
  "rationale": "A bidirectional conveyor follows a bounded sequence that may revisit processing stations.",
  "review": "Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending."
}
```

### Natural language source

# Flexible Processing Control

- **Difficulty:** Hard (hard)

## Requirements

An automated production line consists of 5 workstations: numbered 1# to 5# from left to right. The 1# station is used for raw material loading, stations 2# to 4# are used for product processing, and the 5# station is used for finished product output and storage.
There is a motor in the production line, responsible for moving the product from one workstation to the next. Each workstation has a sensor (used to detect if the product has arrived).
Each product has a different sequence and number of processing steps, specified by the process sequence 'processSequence'. The processSequence is an array type, storing the sequence numbers of the workstations, and the system automatically sends the raw materials to the corresponding workstation for processing based on the station number.
Control requirements:
At the start of production, when the sensor at the 1# station (sensor1) detects the raw material, the start button at the 1# station (station1Start) is pressed. The system queries the first element of the process sequence 'processSequence', starts the conveyor to move the raw material to the corresponding workstation, and stops after delivery. Upon receiving the processing completion signal from the corresponding workstation (station2Complete to station4Complete), it continues to query the next element of the process sequence 'processSequence', determines the direction of the conveyor, and starts the conveyor (conveyorLeft, conveyorRight). This continues until the product is delivered to the 5# workstation.

processLength specifies the active sequence length, from 1 through 8, starting at processSequence[1]. The final active entry is output station 5; other active entries are processing stations 2 through 4. The caller supplies a sequence satisfying this contract.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `processLength` | `USINT` | Active process-sequence length, 1..8; the final active entry must be station 5. |
| Input | `sensor1` | `BOOL` | Sensor at 1# station |
| Input | `sensor2` | `BOOL` | Sensor at 2# station |
| Input | `sensor3` | `BOOL` | Sensor at 3# station |
| Input | `sensor4` | `BOOL` | Sensor at 4# station |
| Input | `sensor5` | `BOOL` | Sensor at 5# station |
| Input | `station1Start` | `BOOL` | Start button at 1# station |
| Input | `station2Complete` | `BOOL` | Processing completion signal at 2# station |
| Input | `station3Complete` | `BOOL` | Processing completion signal at 3# station |
| Input | `station4Complete` | `BOOL` | Processing completion signal at 4# station |
| Input | `processSequence` | `ARRAY[1..8] OF USINT` | Processing sequence |
| Output | `conveyorLeft` | `BOOL` | Conveyor turns left |
| Output | `conveyorRight` | `BOOL` | Conveyor turns right |

### Scenario

A bidirectional conveyor follows a bounded sequence that may revisit processing stations.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | processLength | USINT | Active process-sequence length, 1..8; the final active entry must be station 5. |
| INPUT | sensor1 | BOOL | Sensor at 1# station |
| INPUT | sensor2 | BOOL | Sensor at 2# station |
| INPUT | sensor3 | BOOL | Sensor at 3# station |
| INPUT | sensor4 | BOOL | Sensor at 4# station |
| INPUT | sensor5 | BOOL | Sensor at 5# station |
| INPUT | station1Start | BOOL | Start button at 1# station |
| INPUT | station2Complete | BOOL | Processing completion signal at 2# station |
| INPUT | station3Complete | BOOL | Processing completion signal at 3# station |
| INPUT | station4Complete | BOOL | Processing completion signal at 4# station |
| INPUT | processSequence | ARRAY[1..8] OF USINT | Processing sequence |
| OUTPUT | conveyorLeft | BOOL | Conveyor turns left |
| OUTPUT | conveyorRight | BOOL | Conveyor turns right |

### Initial conditions

```json
{
  "conveyorLeft": false,
  "conveyorRight": false,
  "phase": "IDLE",
  "currentStation": 1,
  "sequenceIndex": 0,
  "target": 1
}
```

### Scan semantics

Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

### Safety and priorities

- Left and right are mutually exclusive.
- Target arrival stops motion before accepting processing completion.

### Explicit assumptions

- The active sequence satisfies the official contract and remains fixed throughout a product cycle.
- station1Start is a rising edge accepted with sensor1 while idle.
- Destination arrival immediately stops the motor. Completion is accepted only at the current processing wait.
- Completion signals are rising edges. Consecutive equal stations denote separate processing operations with fresh edges and no conveyor movement.
- Only one sequence-index advancement occurs per invocation. Station5 arrival returns to idle.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- Station completion edges are ignored unless post-entry phase is WAIT_PROCESS; dropping a station arrival sensor while already in WAIT_PROCESS is outside caller error injection.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `left`: conveyorLeft
- `right`: conveyorRight
- `higher`: post-phase MOVING AND targetStation>currentStation AND NOT sensor[targetStation]
- `lower`: post-phase MOVING AND targetStation<currentStation AND NOT sensor[targetStation]
- `arrive`: pre-phase MOVING AND sensor[targetStation]
- `stop`: NOT conveyorLeft AND NOT conveyorRight
- `waiting`: pre-phase WAIT_PROCESS AND no fresh completion edge
- `out`: pre-phase MOVING AND targetStation=5 AND sensor5
- `done`: post phase IDLE after station5 arrival
- `moving`: pre-phase MOVING
- `processing`: pre-phase WAIT_PROCESS
- `completion`: fresh matching processing-complete edge in the current wait
- `started`: station1Start rising edge accepted with sensor1 in idle
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB016(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
活动路线长度1..8，前项为2/3/4且末项5，活动周期内固定。初始IDLE、station=1、index=0。IDLE在station1Start上升沿且sensor1时选择首目标；MOVING到目标后进入WAIT_PROCESS或目标5回IDLE；WAIT_PROCESS仅对应完成新边沿推进index，同站继续等待。输出仅转移后MOVING且未到目标时按target与station方向开启；所有边沿历史逐拍更新。
- `processLength`: I[k].processLength: sampled input (USINT).
- `sensor1`: I[k].sensor1: sampled input (BOOL).
- `sensor2`: I[k].sensor2: sampled input (BOOL).
- `sensor3`: I[k].sensor3: sampled input (BOOL).
- `sensor4`: I[k].sensor4: sampled input (BOOL).
- `sensor5`: I[k].sensor5: sampled input (BOOL).
- `station1Start`: I[k].station1Start: sampled input (BOOL).
- `station2Complete`: I[k].station2Complete: sampled input (BOOL).
- `station3Complete`: I[k].station3Complete: sampled input (BOOL).
- `station4Complete`: I[k].station4Complete: sampled input (BOOL).
- `processSequence`: I[k].processSequence: sampled input (ARRAY[1..8] OF USINT).
- `conveyorLeft`: O[k].conveyorLeft: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `conveyorRight`: O[k].conveyorRight: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `station1Start_rejected`: pre-phase IDLE AND station1Start AND NOT sensor1
- `init`: At the separate pre-invocation initial observation before scan k=0: Spre.phase="IDLE", O_init.conveyorLeft=false, O_init.conveyorRight=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "conveyorLeft": false,
    "conveyorRight": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB016",
      "array_contract": null,
      "process_contract": {
        "class": "ProcessContract",
        "state": {
          "task_id": "PUB016",
          "phase": 0,
          "mode": null,
          "previous": {},
          "latches": [
            false,
            false,
            false,
            false,
            false
          ],
          "batch_mode": null,
          "route": null,
          "index": 0,
          "station": 1,
          "target": 1,
          "temperature": 0.0,
          "arm_mode": null,
          "arm_step": 0,
          "step_index": 1,
          "step_busy": false,
          "prev_start": false
        }
      },
      "timed_contract": null,
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB016'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "conveyorLeft",
    "conveyorRight"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "phase": {
      "pre": "Spre.process_contract.phase",
      "post": "Spost.process_contract.phase",
      "enum": {
        "0": "IDLE",
        "1": "MOVING",
        "2": "WAIT_PROCESS"
      },
      "initial": 0
    },
    "targetStation": "Spre.process_contract.target",
    "currentStation": "Spre.process_contract.station",
    "route": "Spre.process_contract.route",
    "index": "Spre.process_contract.index"
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The active sequence satisfies the official contract and remains fixed throughout a product cycle.",
    "station1Start is a rising edge accepted with sensor1 while idle.",
    "Destination arrival immediately stops the motor. Completion is accepted only at the current processing wait.",
    "Completion signals are rising edges. Consecutive equal stations denote separate processing operations with fresh edges and no conveyor movement.",
    "Only one sequence-index advancement occurs per invocation. Station5 arrival returns to idle.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "Station completion edges are ignored unless post-entry phase is WAIT_PROCESS; dropping a station arrival sensor while already in WAIT_PROCESS is outside caller error injection.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "活动路线长度1..8，前项为2/3/4且末项5，活动周期内固定。初始IDLE、station=1、index=0。IDLE在station1Start上升沿且sensor1时选择首目标；MOVING到目标后进入WAIT_PROCESS或目标5回IDLE；WAIT_PROCESS仅对应完成新边沿推进index，同站继续等待。输出仅转移后MOVING且未到目标时按target与station方向开启；所有边沿历史逐拍更新。"
}
```

**PUB016.P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**PUB016.P1** Interlock

```text
G(!(left & right))
```

Both directions can never run together.

**PUB016.P2** Direction

```text
G((higher -> (right & !left)) & (lower -> (left & !right)))
```

The target/current station order determines direction.

**PUB016.P3** Arrival

```text
G(arrive -> stop)
```

Every destination stops movement immediately.

**PUB016.P4** Wait

```text
G(waiting -> stop)
```

A processing wait does not move without completion.

**PUB016.P5** Output

```text
G(out -> (done & stop))
```

The final station completes the sequence.

**PUB016.P6** Conditional completion

```text
(G(moving -> F arrive) & G(processing -> F completion)) -> G(started -> F done)
```

Under the valid fixed-sequence input contract, eventual external feedback permits every started route to complete.

**PUB016.P7**

```text
G(station1Start_rejected -> stop)
```

Forbids starting automatic transport without a detected product at station 1.

**PUB016.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB016.T1 | Follow [4,2,5] and ignore a wrong completion input. | 8 |
| PUB016.T2 | A one-entry sequence goes directly to output. | 3 |
| PUB016.T3 | A held completion cannot skip a repeated processing operation. | 7 |
| V2_process_history_regression | Mode/edge reset, repeated station or prior-batch retained setpoint regression. | 9 |
| PUB016.T4 | PUB016.T4 | 20 |
| PUB016.R22.route8 | 八站路线、双向运输保持、工位等待与第二批次 | 92 |
| PUB016.T5 | station1Start rejected without sensor1 and mid-cycle re-triggers ignored before clean next-batch start. | 9 |
| PUB016.T6 | Multiple consecutive repeated stations [2, 2, 3, 3, 5] hold stopped until distinct fresh completion rising edges. | 12 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB017 Recipe Management System

Origin: public. Difficulty: hard.

### Source and adaptation

```json
{
  "source_type": "instructor_public_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": "hard[2] (zero based), flattened task 17",
  "source_sha256": "05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362",
  "adaptation": "Official en text and interface preserved verbatim; interpretations are separate assumptions.",
  "rationale": "A bounded recipe database supports atomic add/delete/modify/query and deterministic empty-slot selection.",
  "review": "Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending."
}
```

### Natural language source

# Recipe Management System

- **Difficulty:** Hard (hard)

## Requirements

A factory's production line needs to produce a variety of products based on different recipes. The control center of the production line requires a recipe management system that allows operators to add, delete, modify, and query recipe data.
Control requirements:
Recipe data should include recipe number, raw material type, raw material ratio, and production temperature.
The system should allow input of new recipe data and store it in the recipe database.
The system should allow deletion or modification of existing recipe data by recipe number.
The system should allow querying recipe details by recipe number and output the recipe.
Notes:
1. Recipes are constructed using the ST_Recipe data type, which includes recipe number (recipeID), raw material type (ingredientType), raw material ratio (ingredientRatio), and production temperature (productionTemperature). The recipe database can store up to 10 recipes, constructed with ARRAY[1..10] OF ST_Recipe, where recipe numbers must not be duplicated, and a recipe number of 0 indicates an empty slot.
2. When a query recipe request signal (queryRecipe) is triggered, the system first compares the recipe number (recipeID) from the input recipe (recipeIn) with all recipes in the recipe database recipe. If the number does not exist, an error status (error=true) and error code (status=16#8001) are output. If the number exists, the recipe is output to the recipe query result (recipeQueryResult).
3. When an add recipe request signal (addRecipe) is triggered, the system first compares the recipe number (recipeID) from the input recipe (recipeIn) with all recipes in the recipe database (recipe). If a duplicate number exists, an error status (error=true) and error code (status=16#8002) are output. If there is no empty slot in the recipe database (recipe), an error status (error=true) and error code (status=16#8003) are output. If there are no errors, the input recipe (recipeIn) is stored in the recipe database (recipe), prioritizing the empty slot with the smallest array index.
4. When a delete recipe request signal (deleteRecipe) is triggered, the system first compares the recipe number (recipeID) from the input recipe (recipeIn) with all recipes in the recipe database (recipe). If the number does not exist, an error status (error=true) and error code (status=16#8004) are output. If the number exists, the recipe is deleted, i.e., the recipe number (recipeID) in the recipe database (recipe) is set to 0.
5. When a modify recipe request signal (modifyRecipe) is triggered, the system first compares the recipe number (recipeID) from the input recipe (recipeIn) with all recipes in the recipe database (recipe). If the number does not exist, an error status (error=true) and error code (status=16#8005) are output. If the number exists, the recipe is replaced with the input recipe (recipeIn).

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `addRecipe` | `BOOL` | Add Recipe Request Signal |
| Input | `deleteRecipe` | `BOOL` | Delete Recipe Request Signal |
| Input | `modifyRecipe` | `BOOL` | Modify Recipe Request Signal |
| Input | `queryRecipe` | `BOOL` | Query Recipe Request Signal |
| Input | `recipeIn` | `ST_Recipe` | Input Recipe |
| Output | `recipeAdded` | `BOOL` | Recipe Added Success Indicator |
| Output | `recipeDeleted` | `BOOL` | Recipe Deleted Success Indicator |
| Output | `recipeModified` | `BOOL` | Recipe Modified Success Indicator |
| Output | `recipeQueryResult` | `ST_Recipe` | Recipe Query Result Output |
| Output | `error` | `BOOL` | Error Status Indicator<br>FALSE: No Error Occurred<br>TRUE: Execution Error |
| Output | `status` | `WORD` | Status Code |
| Input/Output | `recipe` | `ARRAY[1..10] OF ST_Recipe` | Recipe Database |

**Data type `ST_Recipe`**

| Field | Data Type | Description |
| --- | --- | --- |
| `recipeID` | `INT` | Recipe identifier; zero denotes an unused database slot. |
| `ingredientType` | `INT` | Ingredient-type identifier. |
| `ingredientRatio` | `REAL` | Ingredient proportion. |
| `productionTemperature` | `REAL` | Production temperature. |

### Scenario

A bounded recipe database supports atomic add/delete/modify/query and deterministic empty-slot selection.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | addRecipe | BOOL | Add Recipe Request Signal |
| INPUT | deleteRecipe | BOOL | Delete Recipe Request Signal |
| INPUT | modifyRecipe | BOOL | Modify Recipe Request Signal |
| INPUT | queryRecipe | BOOL | Query Recipe Request Signal |
| INPUT | recipeIn | ST_Recipe | Input Recipe |
| OUTPUT | recipeAdded | BOOL | Recipe Added Success Indicator |
| OUTPUT | recipeDeleted | BOOL | Recipe Deleted Success Indicator |
| OUTPUT | recipeModified | BOOL | Recipe Modified Success Indicator |
| OUTPUT | recipeQueryResult | ST_Recipe | Recipe Query Result Output |
| OUTPUT | error | BOOL | Error Status Indicator<br>FALSE: No Error Occurred<br>TRUE: Execution Error |
| OUTPUT | status | WORD | Status Code |
| IN_OUT | recipe | ARRAY[1..10] OF ST_Recipe | Recipe Database |

### Initial conditions

```json
{
  "recipe": [
    {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    }
  ],
  "recipeAdded": false,
  "recipeDeleted": false,
  "recipeModified": false,
  "recipeQueryResult": {
    "recipeID": 0,
    "ingredientType": 0,
    "ingredientRatio": 0.0,
    "productionTemperature": 0.0
  },
  "error": false,
  "status": 0
}
```

### Scan semantics

Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

### Safety and priorities

- Duplicate checking precedes database-full checking.
- Failed requests must not mutate the database.
- Insertion uses the lowest-index empty slot.

### Explicit assumptions

- At most one request rising edge may occur per call; simultaneous rising edges across addRecipe, deleteRecipe, modifyRecipe, and queryRecipe are outside the valid domain (rejected with ValueError).
- Any nonzero INT (-32768..32767, excluding 0) is valid as recipeID (positive or negative); zero denotes an unused slot and addRecipe with recipeID=0 is rejected with ValueError.
- Success indicators are one-invocation pulses. error/status clear on idle.
- recipeQueryResult retains the last successful query until another successful query.
- Deleting a record clears its recipeID to 0; its remaining ST_Recipe fields remain unconstrained on the deletion scan (subject to valid ST_Recipe field types and finite values) and preserve sampled caller values on later non-overwriting scans.
- The caller-owned recipe array is initialized once and persists across steps; do not overwrite it with initial values per scan.
- Compare REAL values with absolute tolerance 1e-5.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Supporting types

```json
[
  {
    "name": "ST_Recipe",
    "kind": "DUT",
    "declaration": "TYPE ST_Recipe :\nSTRUCT\n recipeID : INT;\n ingredientType : INT;\n ingredientRatio : REAL;\n productionTemperature : REAL;\nEND_STRUCT\nEND_TYPE",
    "source": "Official field table; types unchanged."
  }
]
```

### Test bindings

```json
{
  "recipe": {
    "type": "ARRAY[1..10] OF ST_Recipe",
    "initial": [
      {
        "recipeID": 0,
        "ingredientType": 0,
        "ingredientRatio": 0.0,
        "productionTemperature": 0.0
      },
      {
        "recipeID": 0,
        "ingredientType": 0,
        "ingredientRatio": 0.0,
        "productionTemperature": 0.0
      },
      {
        "recipeID": 0,
        "ingredientType": 0,
        "ingredientRatio": 0.0,
        "productionTemperature": 0.0
      },
      {
        "recipeID": 0,
        "ingredientType": 0,
        "ingredientRatio": 0.0,
        "productionTemperature": 0.0
      },
      {
        "recipeID": 0,
        "ingredientType": 0,
        "ingredientRatio": 0.0,
        "productionTemperature": 0.0
      },
      {
        "recipeID": 0,
        "ingredientType": 0,
        "ingredientRatio": 0.0,
        "productionTemperature": 0.0
      },
      {
        "recipeID": 0,
        "ingredientType": 0,
        "ingredientRatio": 0.0,
        "productionTemperature": 0.0
      },
      {
        "recipeID": 0,
        "ingredientType": 0,
        "ingredientRatio": 0.0,
        "productionTemperature": 0.0
      },
      {
        "recipeID": 0,
        "ingredientType": 0,
        "ingredientRatio": 0.0,
        "productionTemperature": 0.0
      },
      {
        "recipeID": 0,
        "ingredientType": 0,
        "ingredientRatio": 0.0,
        "productionTemperature": 0.0
      }
    ],
    "persistence": "VAR_IN_OUT caller storage retained across all steps."
  }
}
```

### Atomic propositions and monitor predicates

- `q_missing`: rising(queryRecipe) AND ID absent from pre-database
- `a_dup`: rising(addRecipe) AND ID exists
- `a_full`: rising(addRecipe) AND ID absent AND all slots full
- `d_missing`: rising(deleteRecipe) AND ID absent
- `m_missing`: rising(modifyRecipe) AND ID absent
- `e1`: error AND status=16#8001
- `e2`: error AND status=16#8002
- `e3`: error AND status=16#8003
- `e4`: error AND status=16#8004
- `e5`: error AND status=16#8005
- `error`: O[k].error: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `same`: database equals pre-database
- `add_ok`: rising(addRecipe) AND nonzero INT recipeIn.recipeID absent from pre-database AND empty slot exists
- `insert`: lowest-index pre-empty slot equals recipeIn; all other slots unchanged
- `add_success`: recipeAdded AND NOT error AND status=0
- `query_ok`: rising(queryRecipe) AND matching record exists
- `result`: recipeQueryResult equals matching pre-record
- `idle`: no rising request
- `clear`: NOT error AND status=0 AND NOT recipeAdded AND NOT recipeDeleted AND NOT recipeModified
- `unique`: all nonzero IDs are pairwise distinct
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB017(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
数据库首拍由调用前recipe初始化，之后为跨拍保留存储；非零ID唯一（允许正/负整数recipeID!=0，新增时严禁recipeID=0且每拍至多一个请求上升沿）。四请求历史初值FALSE、每拍更新。查询缺失8001；新增重复8002优先于满库8003，否则最低空位整体写入；删除缺失8004否则只清ID；修改缺失8005否则整体替换。失败/空闲库保持。三个成功输出是单拍脉冲，成功/空闲error=FALSE/status=0；查询结果仅成功查询时更新，初值零记录。成功删除槽的非ID字段当拍不受约束但须满足ST_Recipe类型与范围，此后无覆盖操作时与采样实际值比较保持；不把这些物理表示字段写回参考数据库。
- `addRecipe`: I[k].addRecipe: sampled input (BOOL).
- `deleteRecipe`: I[k].deleteRecipe: sampled input (BOOL).
- `modifyRecipe`: I[k].modifyRecipe: sampled input (BOOL).
- `queryRecipe`: I[k].queryRecipe: sampled input (BOOL).
- `recipeIn`: I[k].recipeIn: sampled input (ST_Recipe).
- `recipeAdded`: O[k].recipeAdded: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `recipeDeleted`: O[k].recipeDeleted: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `recipeModified`: O[k].recipeModified: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `recipeQueryResult`: O[k].recipeQueryResult: independently observed post-scan candidate value (ST_Recipe); never defined as expected output.
- `status`: O[k].status: independently observed post-scan candidate value (WORD); never defined as expected output.
- `recipe`: O[k].recipe: independently observed post-scan candidate value (ARRAY[1..10] OF ST_Recipe); never defined as expected output. I[k].recipe denotes separately captured caller value before invocation.
- `delete_ok`: rising(deleteRecipe) AND matching record exists in pre-database
- `deleted`: matching slot recipeID=0 AND recipeDeleted AND NOT error AND status=0 AND all other slots preserved
- `modify_ok`: rising(modifyRecipe) AND matching record exists in pre-database
- `modified`: matching slot equals recipeIn AND recipeModified AND NOT error AND status=0 AND all other slots preserved
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.recipeAdded=false, O_init.recipeDeleted=false, O_init.recipeModified=false, O_init.recipeQueryResult={"recipeID": 0, "ingredientType": 0, "ingredientRatio": 0.0, "productionTemperature": 0.0}, O_init.error=false, O_init.status=0.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "recipeAdded": false,
    "recipeDeleted": false,
    "recipeModified": false,
    "recipeQueryResult": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "error": false,
    "status": 0
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB017",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": {
        "class": "DataContract",
        "state": {
          "task_id": "PUB017",
          "previous": 0,
          "high": false,
          "low": false,
          "trigger": false,
          "window": null,
          "history": [],
          "average": 0.0,
          "reached": false,
          "recipes": [
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            }
          ],
          "last_query": {
            "recipeID": 0,
            "ingredientType": 0,
            "ingredientRatio": 0.0,
            "productionTemperature": 0.0
          },
          "prev_add": false,
          "prev_delete": false,
          "prev_modify": false,
          "prev_query": false,
          "recipes_initialized": false,
          "queue": [],
          "prev_enq": false,
          "prev_deq": false
        }
      },
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB017'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "error",
    "recipe",
    "recipeAdded",
    "recipeDeleted",
    "recipeModified",
    "recipeQueryResult",
    "status"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "storage": {
      "pre_database": "Spre.data_contract.recipes; first invocation uses separately sampled I[0].recipe",
      "actual_database": "O[k].recipe; preservation compares sampled I[k].recipe",
      "pre_queue": "Spre.data_contract.queue",
      "post_queue": "Spost.data_contract.queue",
      "pre_count": "len(Spre.data_contract.queue)",
      "capacity": "length of the actual caller buffer binding, fixed per case",
      "rise": "I[k].request AND NOT corresponding Spre.data_contract.prev_{add/delete/modify/query/enq/deq}",
      "initial_request_memories": false,
      "initial_queue": []
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "At most one request rising edge may occur per call; simultaneous rising edges across addRecipe, deleteRecipe, modifyRecipe, and queryRecipe are outside the valid domain (rejected with ValueError).",
    "Any nonzero INT (-32768..32767, excluding 0) is valid as recipeID (positive or negative); zero denotes an unused slot and addRecipe with recipeID=0 is rejected with ValueError.",
    "Success indicators are one-invocation pulses. error/status clear on idle.",
    "recipeQueryResult retains the last successful query until another successful query.",
    "Deleting a record clears its recipeID to 0; its remaining ST_Recipe fields remain unconstrained on the deletion scan (subject to valid ST_Recipe field types and finite values) and preserve sampled caller values on later non-overwriting scans.",
    "The caller-owned recipe array is initialized once and persists across steps; do not overwrite it with initial values per scan.",
    "Compare REAL values with absolute tolerance 1e-5.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "数据库首拍由调用前recipe初始化，之后为跨拍保留存储；非零ID唯一（允许正/负整数recipeID!=0，新增时严禁recipeID=0且每拍至多一个请求上升沿）。四请求历史初值FALSE、每拍更新。查询缺失8001；新增重复8002优先于满库8003，否则最低空位整体写入；删除缺失8004否则只清ID；修改缺失8005否则整体替换。失败/空闲库保持。三个成功输出是单拍脉冲，成功/空闲error=FALSE/status=0；查询结果仅成功查询时更新，初值零记录。成功删除槽的非ID字段当拍不受约束但须满足ST_Recipe类型与范围，此后无覆盖操作时与采样实际值比较保持；不把这些物理表示字段写回参考数据库。"
}
```

**PUB017.P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**PUB017.P1** Errors

```text
G((q_missing -> e1) & (a_dup -> e2) & (a_full -> e3) & (d_missing -> e4) & (m_missing -> e5))
```

Distinct failures produce the official status codes.

**PUB017.P2** No mutation

```text
G(error -> same)
```

Rejected operations preserve all records.

**PUB017.P3** Lowest insertion

```text
G(add_ok -> (insert & add_success))
```

Adds use the lowest free slot.

**PUB017.P4** Query

```text
G(query_ok -> result)
```

Query returns the complete matched record.

**PUB017.P5** Idle

```text
G(idle -> clear)
```

Indicators and invocation errors clear on idle.

**PUB017.P6** Uniqueness

```text
G(unique)
```

All operations preserve ID uniqueness from a valid initial database.

**PUB017.P7**

```text
G((delete_ok -> deleted) & (modify_ok -> modified) & (idle -> same))
```

Closes independent LTL coverage of delete, modify, and idle preservation missing in P1..P6.

**PUB017.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB017.T1 | Add, query, modify, delete and reuse the first empty slot. | 14 |
| PUB017.T2 | All missing-record errors and duplicate rejection preserve existing record. | 11 |
| PUB017.T3 | Fill ten slots; duplicate error has priority over full error. | 23 |
| PUB017.T4 | PUB017.T4 | 9 |
| PUB017.R22.storage_operations | 满库末槽读回、最小空槽复用、修改其他槽保持与请求长按 | 54 |
| PUB017.T5 | Negative nonzero recipeID lifecycle (add/query/modify/delete) and failed query retention of previous recipeQueryResult. | 8 |
| PUB017.T6 | Mid-table and high-slot (slots 8-10) deletion, adjacent slot preservation, and lowest free-slot insertion. | 29 |
| PUB017.T7 | Level-held requests after rising edges stay idle (no duplicate error, missing error, or repeat pulse). | 9 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB018 FIFO First-In-First-Out Queue

Origin: public. Difficulty: hard.

### Source and adaptation

```json
{
  "source_type": "instructor_public_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": "hard[3] (zero based), flattened task 18",
  "source_sha256": "05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362",
  "adaptation": "Official en text and interface preserved verbatim; interpretations are separate assumptions.",
  "rationale": "A generic circular FIFO derives capacity/type from caller storage and handles edge requests, wraparound and rejection.",
  "review": "Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending."
}
```

### Natural language source

# FIFO First-In-First-Out Queue

- **Difficulty:** Hard (hard)

## Requirements

Write a function block FB implementing a First-In-First-Out (FIFO) circular queue. Derive the queue capacity and element type from the caller-supplied buffer.

1. Each rising edge of enqueue requests one enqueue operation. If the queue is not full, append the current item value to its tail.
2. Each rising edge of dequeue requests one dequeue operation. If the queue is not empty, remove its front element and write that value back to item. The caller must not request enqueue and dequeue in the same invocation.
3. When reset is TRUE, empty the queue and set elementCount to zero. Reset takes priority over enqueue and dequeue; stored buffer values need not be overwritten.
4. Output the current number of valid elements through elementCount. Zero means the queue is empty; a count equal to the actual buffer array length means it is full.
5. Reject a dequeue request on an empty queue or an enqueue request on a full queue. Leave the queue and item unchanged and report the reason through status.
6. The queue is empty on its first invocation. Define head and tail positions and other internal state within the implementation; do not expose them as interface parameters.

Status codes:

- 16#0000: No error in this invocation, including idle, reset and successful operations.
- 16#8001: The dequeue request was rejected because the queue is empty.
- 16#8002: The enqueue request was rejected because the queue is full.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `enqueue` | `BOOL` | Enqueue request; one operation per rising edge. |
| Input | `dequeue` | `BOOL` | Dequeue request; one operation per rising edge. |
| Input | `reset` | `BOOL` | TRUE resets the queue to empty; takes priority over enqueue and dequeue. |
| Output | `elementCount` | `DINT` | Current number of valid elements, from zero through the queue capacity. |
| Output | `status` | `WORD` | Invocation status: 16#0000 no error, 16#8001 dequeue from an empty queue, 16#8002 enqueue into a full queue. |
| Input/Output | `item` | `VARIANT` | Mutable scalar reference: read its value when enqueuing; write the removed front value on successful dequeue. Its concrete type must match the array element type. |
| Input/Output | `buffer` | `VARIANT` | Reference to a nonempty one-dimensional array with a single concrete element type, used as queue storage. Capacity is the actual array length. |

Associate buffer with a nonempty, homogeneous one-dimensional array and item with a writable scalar of the same element type. Keep the buffer association fixed for each function-block instance. Derive capacity from the actual array length; it must fit in a positive DINT.

### Scenario

A generic circular FIFO derives capacity/type from caller storage and handles edge requests, wraparound and rejection.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | enqueue | BOOL | Enqueue request; one operation per rising edge. |
| INPUT | dequeue | BOOL | Dequeue request; one operation per rising edge. |
| INPUT | reset | BOOL | TRUE resets the queue to empty; takes priority over enqueue and dequeue. |
| OUTPUT | elementCount | DINT | Current number of valid elements, from zero through the queue capacity. |
| OUTPUT | status | WORD | Invocation status: 16#0000 no error, 16#8001 dequeue from an empty queue, 16#8002 enqueue into a full queue. |
| IN_OUT | item | VARIANT | Mutable scalar reference: read its value when enqueuing; write the removed front value on successful dequeue. Its concrete type must match the array element type. |
| IN_OUT | buffer | VARIANT | Reference to a nonempty one-dimensional array with a single concrete element type, used as queue storage. Capacity is the actual array length. |

### Initial conditions

```json
{
  "elementCount": 0,
  "status": 0,
  "head": 0,
  "tail": 0
}
```

### Scan semantics

Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

### Safety and priorities

- Reset empties the logical queue before handling requests.
- Rejected requests preserve queue and item.
- Only rising edges perform enqueue/dequeue.

### Explicit assumptions

- The official VARIANT interface is preserved. Native CODESYS compatibility and runtime type/array metadata access remain unverified; never silently replace it by a DINT-only interface.
- Binding A: item DINT, buffer ARRAY[0..1] OF DINT. Binding B: item BOOL, buffer ARRAY[1..3] OF BOOL. Both must run to substantiate genericity.
- Buffer is initialized and bound once per test; its association and contents are not externally overwritten between calls. item is caller-writable every scan.
- Simultaneous enqueue and dequeue rising edges on a non-reset scan are outside the valid domain (rejected with ValueError); reset=TRUE takes priority over both and updates edge memories.
- Edge memories update during reset; a request held afterward is not another edge.
- Reset need not clear buffer values. Unused storage arrangement is unconstrained.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Test bindings

```json
[
  {
    "id": "A",
    "item_type": "DINT",
    "buffer_type": "ARRAY[0..1] OF DINT",
    "buffer_initial": [
      0,
      0
    ],
    "capacity": 2
  },
  {
    "id": "B",
    "item_type": "BOOL",
    "buffer_type": "ARRAY[1..3] OF BOOL",
    "buffer_initial": [
      false,
      false,
      false
    ],
    "capacity": 3
  }
]
```

### Portability

```json
{
  "status": "UNVERIFIED",
  "issue": "VARIANT is an official interface but may not be a native CODESYS generic type in the selected profile. A verified variant-reflection library or explicitly disclosed adapter may be required.",
  "required_validation": "Compile the unchanged generic interface, verify two element types and different lower bounds/capacities. Adapter results must disclose deviations."
}
```

### Atomic propositions and monitor predicates

- `reset`: I[k].reset: sampled input (BOOL).
- `empty`: elementCount=0
- `ok`: status=0
- `pop_empty`: NOT reset AND rising(dequeue) AND pre-count=0
- `push_full`: NOT reset AND rising(enqueue) AND pre-count=capacity
- `e1`: status=16#8001
- `e2`: status=16#8002
- `same`: logical queue equals pre-queue AND item equals sampled item
- `push`: NOT reset AND rising(enqueue) AND pre-count<capacity
- `pushed`: post-queue=pre-queue appended with sampled item AND count=pre-count+1 AND status=0 AND item equals sampled item
- `pop`: NOT reset AND rising(dequeue) AND pre-count>0
- `popped`: item=pre-front AND post-queue=pre-queue without front AND count=pre-count-1 AND status=0
- `bounded`: 0<=elementCount<=actual buffer length
- `idle`: NOT reset AND no request rising edge
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB018(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
独立逻辑队列Q初始空、enqPrev/deqPrev=FALSE。非reset下严禁同拍enqueue/dequeue同时上升沿。reset优先QAfter=[]；否则单个enqueue新沿且未满时追加采样item，满报8002；dequeue新沿且非空时返回旧队首并去首，空报8001；其余状态0。elementCount=|QAfter|；仅成功pop改变实际item，其余等于采样item。buffer物理布局不受约束，其正确性由完整可观察出队行为约束。绑定A容量2(DINT)、B容量3(BOOL)，其余正整数容量由实际buffer元数据固定。
- `enqueue`: I[k].enqueue: sampled input (BOOL).
- `dequeue`: I[k].dequeue: sampled input (BOOL).
- `elementCount`: O[k].elementCount: independently observed post-scan candidate value (DINT); never defined as expected output.
- `status`: O[k].status: independently observed post-scan candidate value (WORD); never defined as expected output.
- `item`: O[k].item: independently observed post-scan candidate value (VARIANT); never defined as expected output. I[k].item denotes separately captured caller value before invocation.
- `buffer`: O[k].buffer: independently observed post-scan candidate value (VARIANT); never defined as expected output. I[k].buffer denotes separately captured caller value before invocation.
- `non_pop_item_preserved`: item equals sampled caller item
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.elementCount=0, O_init.status=0.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "elementCount": 0,
    "status": 0
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB018",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": {
        "class": "DataContract",
        "state": {
          "task_id": "PUB018",
          "previous": 0,
          "high": false,
          "low": false,
          "trigger": false,
          "window": null,
          "history": [],
          "average": 0.0,
          "reached": false,
          "recipes": [
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            },
            {
              "recipeID": 0,
              "ingredientType": 0,
              "ingredientRatio": 0.0,
              "productionTemperature": 0.0
            }
          ],
          "last_query": {
            "recipeID": 0,
            "ingredientType": 0,
            "ingredientRatio": 0.0,
            "productionTemperature": 0.0
          },
          "prev_add": false,
          "prev_delete": false,
          "prev_modify": false,
          "prev_query": false,
          "recipes_initialized": false,
          "queue": [],
          "prev_enq": false,
          "prev_deq": false
        }
      },
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB018'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "elementCount",
    "item",
    "status"
  ],
  "unconstrained_representation_fields": [
    "buffer"
  ],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "storage": {
      "pre_database": "Spre.data_contract.recipes; first invocation uses separately sampled I[0].recipe",
      "actual_database": "O[k].recipe; preservation compares sampled I[k].recipe",
      "pre_queue": "Spre.data_contract.queue",
      "post_queue": "Spost.data_contract.queue",
      "pre_count": "len(Spre.data_contract.queue)",
      "capacity": "length of the actual caller buffer binding, fixed per case",
      "rise": "I[k].request AND NOT corresponding Spre.data_contract.prev_{add/delete/modify/query/enq/deq}",
      "initial_request_memories": false,
      "initial_queue": []
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The official VARIANT interface is preserved. Native CODESYS compatibility and runtime type/array metadata access remain unverified; never silently replace it by a DINT-only interface.",
    "Binding A: item DINT, buffer ARRAY[0..1] OF DINT. Binding B: item BOOL, buffer ARRAY[1..3] OF BOOL. Both must run to substantiate genericity.",
    "Buffer is initialized and bound once per test; its association and contents are not externally overwritten between calls. item is caller-writable every scan.",
    "Simultaneous enqueue and dequeue rising edges on a non-reset scan are outside the valid domain (rejected with ValueError); reset=TRUE takes priority over both and updates edge memories.",
    "Edge memories update during reset; a request held afterward is not another edge.",
    "Reset need not clear buffer values. Unused storage arrangement is unconstrained.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "独立逻辑队列Q初始空、enqPrev/deqPrev=FALSE。非reset下严禁同拍enqueue/dequeue同时上升沿。reset优先QAfter=[]；否则单个enqueue新沿且未满时追加采样item，满报8002；dequeue新沿且非空时返回旧队首并去首，空报8001；其余状态0。elementCount=|QAfter|；仅成功pop改变实际item，其余等于采样item。buffer物理布局不受约束，其正确性由完整可观察出队行为约束。绑定A容量2(DINT)、B容量3(BOOL)，其余正整数容量由实际buffer元数据固定。"
}
```

**PUB018.P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**PUB018.P1** Reset

```text
G(reset -> (empty & ok))
```

Reset overrides simultaneous requests.

**PUB018.P2** Rejections

```text
G((pop_empty -> (e1 & same)) & (push_full -> (e2 & same)))
```

Full and empty failures preserve data.

**PUB018.P3** FIFO order

```text
G((push -> pushed) & (pop -> popped))
```

Accepted edges update the ordered logical queue exactly once.

**PUB018.P4** Count

```text
G(bounded)
```

Count remains within the actual caller capacity.

**PUB018.P5** Held request

```text
G(idle -> (ok & same))
```

Held levels do not perform another operation.

**PUB018.P6**

```text
G((!pop) -> non_pop_item_preserved)
```

Prevents spurious overwriting of caller item when not popping.

**PUB018.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB018.T1 | Capacity-two FIFO preserves order through wrap, full and empty rejection. | 17 |
| PUB018.T2 | Reset coincides with request; held request after reset does not execute. | 8 |
| PUB018.T3 | Second element type and lower-bound-one buffer. | 9 |
| PUB018.T4 | PUB018.T4 | 18 |
| PUB018.R22.capacity1 | 容量1入队、满、出队、回绕及复位后重用 | 11 |
| PUB018.R22.drain_T1 | 逐项排空并检查末元素：PUB018.T1 | 25 |
| PUB018.R22.drain_T2 | 逐项排空并检查末元素：PUB018.T2 | 16 |
| PUB018.R22.drain_T3 | 逐项排空并检查末元素：PUB018.T3 | 17 |
| PUB018.R22.drain_capacity1 | 逐项排空并检查末元素：PUB018.R22.capacity1 | 19 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB019 Mechanical Arm Control

Origin: public. Difficulty: hard.

### Source and adaptation

```json
{
  "source_type": "instructor_public_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": "hard[4] (zero based), flattened task 19",
  "source_sha256": "05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362",
  "adaptation": "Official en text and interface preserved verbatim; interpretations are separate assumptions.",
  "rationale": "An eight-action handling cycle shares manual, confirmed single-step, single-cycle and continuous operation.",
  "review": "Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending."
}
```

### Natural language source

# Mechanical Arm Control

- **Difficulty:** Hard (hard)

## Requirements

Design a PLC program to control an automated mechanical arm that performs handling tasks on the production line. The mechanical arm has six basic actions: down, up, left, right, grip, and release. The operating modes of the mechanical arm include four types: manual, single step, single cycle, and continuous.
Control requirements:
1. Manual mode: Allows the operator to control each action of the mechanical arm individually through the control panel, provided it is not yet in position. For example, pressing the down button (DownButton=1), if not at the down position (DownLimitSwitch=0), then move down (MoveDown=1); if at the down position (DownLimitSwitch=1), stop moving down. Releasing the down button also stops the movement down.
2. Single step mode: The mechanical arm automatically executes one action according to the preset program, and the operator needs to confirm after each action is completed to execute the next action.
The initial position of the mechanical arm is at the top left.
When the start button is pressed once, the mechanical arm executes the down command MoveDown, and stops after reaching the down position.
When the start button is pressed again, the mechanical arm executes the grip command ActivateGrip, and stops after gripping.
When the start button is pressed again, the mechanical arm executes the up command MoveUp, and stops after reaching the up position.
When the start button is pressed, the mechanical arm executes the right command MoveRight, and stops after reaching the right position.
When the start button is pressed, the mechanical arm executes the down command MoveDown, and stops after reaching the down position.
When the start button is pressed, the mechanical arm executes the release command ActivateRelease, and stops after releasing.
When the start button is pressed again, the mechanical arm executes the up command MoveUp, and stops after reaching the up position.
When the start button is pressed again, the mechanical arm executes the left command MoveLeft, and stops after reaching the left position.
Then starts the cycle again from the beginning
3. Single cycle mode: The mechanical arm automatically completes a full handling cycle, including all preset actions, and stops at the end of the cycle waiting for the operator's instruction.
The initial position of the mechanical arm is at the top left, when the start button is pressed:
The mechanical arm first moves down, then grips after reaching the down position, moves up after gripping, moves right after reaching the up position, moves down after reaching the right position, releases after reaching the down position, moves up after releasing, moves left after reaching the up position, and stops after reaching the left position.
4. Continuous mode: The initial position of the mechanical arm is at the top left, when the start button is pressed, the mechanical arm continuously executes the handling cycle of the single cycle mode.
5. The emergency stop function can stop all actions of the mechanical arm at any time.

Use GripLimitSwitch and ReleaseLimitSwitch as the completion feedback for gripping and releasing respectively. The caller keeps the four mode-selection inputs mutually exclusive.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `ManualMode` | `BOOL` | Manual mode |
| Input | `SingleStepMode` | `BOOL` | Single step mode |
| Input | `SingleCycleMode` | `BOOL` | Single cycle mode |
| Input | `ContinuousMode` | `BOOL` | Continuous mode |
| Input | `EmergencyStop` | `BOOL` | Emergency stop signal<br>FALSE: Emergency stop triggered<br>TRUE: No emergency stop triggered |
| Input | `Start` | `BOOL` | Start operation |
| Input | `DownButton` | `BOOL` | Down button |
| Input | `UpButton` | `BOOL` | Up button |
| Input | `LeftButton` | `BOOL` | Left button |
| Input | `RightButton` | `BOOL` | Right button |
| Input | `GripButton` | `BOOL` | Grip button |
| Input | `ReleaseButton` | `BOOL` | Release button |
| Input | `DownLimitSwitch` | `BOOL` | Down position limit switch |
| Input | `UpLimitSwitch` | `BOOL` | Up position limit switch |
| Input | `LeftLimitSwitch` | `BOOL` | Left position limit switch |
| Input | `RightLimitSwitch` | `BOOL` | Right position limit switch |
| Input | `GripLimitSwitch` | `BOOL` | Grip position limit switch |
| Input | `ReleaseLimitSwitch` | `BOOL` | Release position limit switch |
| Output | `MoveDown` | `BOOL` | Down command |
| Output | `MoveUp` | `BOOL` | Up command |
| Output | `MoveLeft` | `BOOL` | Left command |
| Output | `MoveRight` | `BOOL` | Right command |
| Output | `ActivateGrip` | `BOOL` | Grip command |
| Output | `ActivateRelease` | `BOOL` | Release command |

### Scenario

An eight-action handling cycle shares manual, confirmed single-step, single-cycle and continuous operation.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | ManualMode | BOOL | Manual mode |
| INPUT | SingleStepMode | BOOL | Single step mode |
| INPUT | SingleCycleMode | BOOL | Single cycle mode |
| INPUT | ContinuousMode | BOOL | Continuous mode |
| INPUT | EmergencyStop | BOOL | Emergency stop signal<br>FALSE: Emergency stop triggered<br>TRUE: No emergency stop triggered |
| INPUT | Start | BOOL | Start operation |
| INPUT | DownButton | BOOL | Down button |
| INPUT | UpButton | BOOL | Up button |
| INPUT | LeftButton | BOOL | Left button |
| INPUT | RightButton | BOOL | Right button |
| INPUT | GripButton | BOOL | Grip button |
| INPUT | ReleaseButton | BOOL | Release button |
| INPUT | DownLimitSwitch | BOOL | Down position limit switch |
| INPUT | UpLimitSwitch | BOOL | Up position limit switch |
| INPUT | LeftLimitSwitch | BOOL | Left position limit switch |
| INPUT | RightLimitSwitch | BOOL | Right position limit switch |
| INPUT | GripLimitSwitch | BOOL | Grip position limit switch |
| INPUT | ReleaseLimitSwitch | BOOL | Release position limit switch |
| OUTPUT | MoveDown | BOOL | Down command |
| OUTPUT | MoveUp | BOOL | Up command |
| OUTPUT | MoveLeft | BOOL | Left command |
| OUTPUT | MoveRight | BOOL | Right command |
| OUTPUT | ActivateGrip | BOOL | Grip command |
| OUTPUT | ActivateRelease | BOOL | Release command |

### Initial conditions

```json
{
  "MoveDown": false,
  "MoveUp": false,
  "MoveLeft": false,
  "MoveRight": false,
  "ActivateGrip": false,
  "ActivateRelease": false,
  "next_step": 1,
  "busy": false,
  "initial_pose": "top left"
}
```

### Scan semantics

Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

### Safety and priorities

- Emergency stop overrides every mode and request.
- Opposed directions and grip/release are mutually exclusive.
- A reached position suppresses its own command immediately.

### Explicit assumptions

- EmergencyStop=FALSE cancels the sequence and outputs while retaining non-empty mode selection in arm_mode; changing mode later clears outputs and resets the sequence, and recovery requires a fresh Start rising edge from top-left pose (UpLimitSwitch & LeftLimitSwitch).
- A Start press is a rising edge. Start edges during an active action are ignored; edge history still updates.
- No selected mode means all commands off and sequence reset. Changing mode also resets the sequence.
- Opposing manual commands on an axis or grip pair are both inhibited. Independent non-opposing actions may run together.
- Manual commands are combinational and stop on their matching limit/feedback. Contradictory limit switches are outside the caller contract.
- Only one phase transition occurs per invocation. In cycle modes, completion feedback switches to the next command in that scan; an already-active next limit suppresses its command but is processed as completion on the next invocation.
- Single-step completion switches all outputs off; the next action requires a fresh Start edge on a later scan.
- Continuous completion of left movement wraps to down in the same scan. Single-cycle completion returns to idle.
- At the start of a new automatic sequence (action 1, not every individual single step), UpLimitSwitch and LeftLimitSwitch must both be TRUE. Grip and release complete on the supplied feedback switches.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- V2 mode-change priority: emergency stop first; then a change of mode after the first invocation clears sequence/latches and suppresses commands for that invocation; edge memories still update. The first invocation establishes the selected mode and executes normally. New commands are accepted on subsequent invocations subject to their edge rules.
- The four mode inputs (ManualMode, SingleStepMode, SingleCycleMode, ContinuousMode) are mutually exclusive per scan (<=1 TRUE; >1 rejected with ValueError).
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `safe`: EmergencyStop input
- `off`: all six command outputs FALSE
- `no_mode`: none of the four mode selectors TRUE
- `exclusive`: NOT(MoveDown AND MoveUp) AND NOT(MoveLeft AND MoveRight) AND NOT(ActivateGrip AND ActivateRelease)
- `down_manual`: ManualMode AND DownButton AND NOT UpButton AND NOT DownLimitSwitch
- `down`: MoveDown
- `down_limit`: DownLimitSwitch
- `up_limit`: UpLimitSwitch
- `up`: MoveUp
- `left_limit`: LeftLimitSwitch
- `left`: MoveLeft
- `right_limit`: RightLimitSwitch
- `right`: MoveRight
- `grip_limit`: GripLimitSwitch
- `grip`: ActivateGrip
- `release_limit`: ReleaseLimitSwitch
- `release`: ActivateRelease
- `step_done`: SingleStepMode AND pre-busy AND matching completion feedback
- `waiting`: SingleStepMode AND NOT pre-busy AND NOT rising(Start)
- `cycle_done`: SingleCycleMode AND pre-phase LEFT AND LeftLimitSwitch
- `continuous_done`: ContinuousMode AND pre-phase LEFT AND LeftLimitSwitch
- `begin_next`: post-phase DOWN with command gated by DownLimitSwitch
- `busy`: pre-sequence is executing an action
- `feedback`: matching completion feedback for the pre-action is TRUE
- `idle`: post-sequence idle
- `start`: fresh Start edge in idle with top-left pose and selected automatic mode
- `started`: post-phase DOWN, busy TRUE
- `ordered`: the next accepted automatic phase follows DOWN, GRIP, UP1, RIGHT, DOWN2, RELEASE, UP2, LEFT
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB019(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
八动作顺序为下/夹/上/右/下/松/上/左。安全失去或无模式全关复位（急停期间仍记录当前非空模式选择），其次模式变化当拍全关复位；四模式选择互斥不可同拍并发。手动六命令分别=本按钮 & !反向按钮 & !本限位。单步完成时全关、保存下一步，新Start沿再启动；首步要求上左到位。单周期末回IDLE；连续末回第一步；自动只在本动作匹配限位时推进一阶，输出按转移后动作并由本限位门控。Start历史每拍更新。
- `modeChanged`: Selected mode differs from previous invocation; FALSE for the first invocation.
- `ManualMode`: I[k].ManualMode: sampled input (BOOL).
- `SingleStepMode`: I[k].SingleStepMode: sampled input (BOOL).
- `SingleCycleMode`: I[k].SingleCycleMode: sampled input (BOOL).
- `ContinuousMode`: I[k].ContinuousMode: sampled input (BOOL).
- `EmergencyStop`: I[k].EmergencyStop: sampled input (BOOL).
- `Start`: I[k].Start: sampled input (BOOL).
- `DownButton`: I[k].DownButton: sampled input (BOOL).
- `UpButton`: I[k].UpButton: sampled input (BOOL).
- `LeftButton`: I[k].LeftButton: sampled input (BOOL).
- `RightButton`: I[k].RightButton: sampled input (BOOL).
- `GripButton`: I[k].GripButton: sampled input (BOOL).
- `ReleaseButton`: I[k].ReleaseButton: sampled input (BOOL).
- `DownLimitSwitch`: I[k].DownLimitSwitch: sampled input (BOOL).
- `UpLimitSwitch`: I[k].UpLimitSwitch: sampled input (BOOL).
- `LeftLimitSwitch`: I[k].LeftLimitSwitch: sampled input (BOOL).
- `RightLimitSwitch`: I[k].RightLimitSwitch: sampled input (BOOL).
- `GripLimitSwitch`: I[k].GripLimitSwitch: sampled input (BOOL).
- `ReleaseLimitSwitch`: I[k].ReleaseLimitSwitch: sampled input (BOOL).
- `MoveDown`: O[k].MoveDown: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `MoveUp`: O[k].MoveUp: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `MoveLeft`: O[k].MoveLeft: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `MoveRight`: O[k].MoveRight: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `ActivateGrip`: O[k].ActivateGrip: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `ActivateRelease`: O[k].ActivateRelease: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `other_manual`: (MoveUp <-> (ManualMode & UpButton & !DownButton & !UpLimitSwitch)) & (MoveLeft <-> (ManualMode & LeftButton & !RightButton & !LeftLimitSwitch)) & (MoveRight <-> (ManualMode & RightButton & !LeftButton & !RightLimitSwitch)) & (ActivateGrip <-> (ManualMode & GripButton & !ReleaseButton & !GripLimitSwitch)) & (ActivateRelease <-> (ManualMode & ReleaseButton & !GripButton & !ReleaseLimitSwitch))
- `all_auto_steps_valid`: SingleStepMode and SingleCycleMode/ContinuousMode execute each step 1..8 cleanly with matching command & feedback only.
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.MoveDown=false, O_init.MoveUp=false, O_init.MoveLeft=false, O_init.MoveRight=false, O_init.ActivateGrip=false, O_init.ActivateRelease=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB019",
      "array_contract": null,
      "process_contract": {
        "class": "ProcessContract",
        "state": {
          "task_id": "PUB019",
          "phase": 0,
          "mode": null,
          "previous": {},
          "latches": [
            false,
            false,
            false,
            false,
            false
          ],
          "batch_mode": null,
          "route": null,
          "index": 0,
          "station": 1,
          "target": 1,
          "temperature": 0.0,
          "arm_mode": null,
          "arm_step": 0,
          "step_index": 1,
          "step_busy": false,
          "prev_start": false
        }
      },
      "timed_contract": null,
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB019'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "ActivateGrip",
    "ActivateRelease",
    "MoveDown",
    "MoveLeft",
    "MoveRight",
    "MoveUp"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "action_index": {
      "pre_cycle": "Spre.process_contract.arm_step",
      "pre_single_step": "Spre.process_contract.step_index",
      "initial_cycle": 0,
      "initial_single_step": 1,
      "enum": {
        "1": "DOWN",
        "2": "GRIP",
        "3": "UP1",
        "4": "RIGHT",
        "5": "DOWN2",
        "6": "RELEASE",
        "7": "UP2",
        "8": "LEFT"
      },
      "feedback": [
        "DownLimitSwitch",
        "GripLimitSwitch",
        "UpLimitSwitch",
        "RightLimitSwitch",
        "DownLimitSwitch",
        "ReleaseLimitSwitch",
        "UpLimitSwitch",
        "LeftLimitSwitch"
      ]
    },
    "busy": "SingleStepMode ? Spre.process_contract.step_busy : Spre.process_contract.arm_step != 0",
    "modeChanged": "Spre.process_contract.arm_mode is not None AND differs from selected input mode (manual/single_step/single_cycle/continuous/None)",
    "mode_initial": null,
    "start_memory": "Spre.process_contract.prev_start, initially FALSE; next=I[k].Start"
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "EmergencyStop=FALSE cancels the sequence and outputs while retaining non-empty mode selection in arm_mode; changing mode later clears outputs and resets the sequence, and recovery requires a fresh Start rising edge from top-left pose (UpLimitSwitch & LeftLimitSwitch).",
    "A Start press is a rising edge. Start edges during an active action are ignored; edge history still updates.",
    "No selected mode means all commands off and sequence reset. Changing mode also resets the sequence.",
    "Opposing manual commands on an axis or grip pair are both inhibited. Independent non-opposing actions may run together.",
    "Manual commands are combinational and stop on their matching limit/feedback. Contradictory limit switches are outside the caller contract.",
    "Only one phase transition occurs per invocation. In cycle modes, completion feedback switches to the next command in that scan; an already-active next limit suppresses its command but is processed as completion on the next invocation.",
    "Single-step completion switches all outputs off; the next action requires a fresh Start edge on a later scan.",
    "Continuous completion of left movement wraps to down in the same scan. Single-cycle completion returns to idle.",
    "At the start of a new automatic sequence (action 1, not every individual single step), UpLimitSwitch and LeftLimitSwitch must both be TRUE. Grip and release complete on the supplied feedback switches.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "V2 mode-change priority: emergency stop first; then a change of mode after the first invocation clears sequence/latches and suppresses commands for that invocation; edge memories still update. The first invocation establishes the selected mode and executes normally. New commands are accepted on subsequent invocations subject to their edge rules.",
    "The four mode inputs (ManualMode, SingleStepMode, SingleCycleMode, ContinuousMode) are mutually exclusive per scan (<=1 TRUE; >1 rejected with ValueError).",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "八动作顺序为下/夹/上/右/下/松/上/左。安全失去或无模式全关复位（急停期间仍记录当前非空模式选择），其次模式变化当拍全关复位；四模式选择互斥不可同拍并发。手动六命令分别=本按钮 & !反向按钮 & !本限位。单步完成时全关、保存下一步，新Start沿再启动；首步要求上左到位。单周期末回IDLE；连续末回第一步；自动只在本动作匹配限位时推进一阶，输出按转移后动作并由本限位门控。Start历史每拍更新。"
}
```

**PUB019.P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**PUB019.P1** Safety

```text
G((!safe | no_mode) -> off)
```

No command survives emergency stop or no mode.

**PUB019.P2** Interlocks

```text
G(exclusive)
```

Opposed actuators are never commanded together.

**PUB019.P3** Manual down

```text
G(safe & !modeChanged & ManualMode -> (down <-> down_manual))
```

Manual down requires the button and an unreached lower limit.

**PUB019.P4** Reached limits

```text
G((down_limit -> !down) & (up_limit -> !up) & (left_limit -> !left) & (right_limit -> !right) & (grip_limit -> !grip) & (release_limit -> !release))
```

Every corresponding completion input suppresses its command.

**PUB019.P5** Step wait

```text
G(safe & !modeChanged & (step_done | waiting) -> off)
```

A completed single step waits for another press.

**PUB019.P6** Automatic start

```text
G(safe & !modeChanged & start -> started)
```

A permitted fresh start begins down.

**PUB019.P7** Order

```text
G(ordered)
```

The eight preset actions retain their required order.

**PUB019.P8** Cycle boundary

```text
G((safe & !modeChanged) -> ((cycle_done -> (idle & off)) & (continuous_done -> begin_next)))
```

Single-cycle stops; continuous wraps.

**PUB019.P9** Conditional liveness

```text
(G(safe & SingleCycleMode) & G(busy -> F feedback)) -> G(started -> F idle)
```

With unchanged safe single-cycle mode and eventual matching feedback, every started sequence eventually returns idle.

**PUB019.P10**

```text
G((safe & !modeChanged & ManualMode -> other_manual) & ((safe & modeChanged) -> off))
```

Completes manual-mode and mode-change output coverage beyond MoveDown.

**PUB019.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB019.T1 | Manual hold-to-run, reached limits, opposing requests and emergency priority. | 10 |
| PUB019.T2 | Each new step requires a release and fresh start; held start cannot skip grip. | 9 |
| PUB019.T3 | All eight actions complete once and wait at top left. | 10 |
| PUB019.T4 | The eighth completion wraps immediately to the first action. | 10 |
| PUB019.T5 | Emergency cancels an action; releasing emergency does not auto-restart. | 6 |
| PUB019.T6 | PUB019.T6 | 25 |
| PUB019.R22.manual_up | 手动上行按钮在未到上限位时应输出上行 | 1 |
| PUB019.R22.grip_hold | 单周期夹紧尚未完成时，夹紧命令应持续 | 4 |
| PUB019.R22.DownButton | 手动动作、保持、到限位停机：DownButton | 6 |
| PUB019.R22.UpButton | 手动动作、保持、到限位停机：UpButton | 6 |
| PUB019.R22.LeftButton | 手动动作、保持、到限位停机：LeftButton | 6 |
| PUB019.R22.RightButton | 手动动作、保持、到限位停机：RightButton | 6 |
| PUB019.R22.GripButton | 手动动作、保持、到限位停机：GripButton | 6 |
| PUB019.R22.ReleaseButton | 手动动作、保持、到限位停机：ReleaseButton | 6 |
| PUB019.R22.SingleStepMode | 完整八动作、各步等待与第二轮：SingleStepMode | 65 |
| PUB019.R22.SingleCycleMode | 完整八动作、各步等待与第二轮：SingleCycleMode | 65 |
| PUB019.R22.ContinuousMode | 完整八动作、各步等待与第二轮：ContinuousMode | 65 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## PUB020 Production Control

Origin: public. Difficulty: hard.

### Source and adaptation

```json
{
  "source_type": "instructor_public_question_bank",
  "source_file": "大作业题库json/大作业题库json/大作业题库.json",
  "source_index": "hard[5] (zero based), flattened task 20",
  "source_sha256": "05170ae18c1ec7c316d8334a84b6ecd48de322c8236735d519b50f72f2d8d362",
  "adaptation": "Official en text and interface preserved verbatim; interpretations are separate assumptions.",
  "rationale": "A five-station conveyor cleans, rejects out-of-range weights, calculates a firing setpoint and signals output completion.",
  "review": "Reviewed against full source, scan convention, boundary cases and state-dependent expectations; instructor validation pending."
}
```

### Natural language source

# Production Control

- **Difficulty:** Hard (hard)

## Requirements

An automated production line consists of 5 workstations: material loading station, cleaning station, weighing station, firing station, and finished product station. The production line has a motor responsible for moving products from one workstation to the next, the sequence of the line is from the material loading station, cleaning station, weighing station, firing station, to the finished product station. Each workstation has a sensor (used to detect if the product has arrived).
Control requirements:
1. Mode Switching: The mode switch (Mode) is used to switch between manual and automatic modes of the production line. 0 = manual mode, 1 = automatic mode.
2. Manual Mode: In manual mode, the forward rotation button (ForwardButton) controls the forward rotation of the motor, and the reverse rotation button (ReverseButton) controls the reverse rotation of the motor. Forward and reverse rotation operations need to be interlocked and cannot be performed simultaneously.
3. Automatic Mode:
   - When the material arrives at the material loading station, the SensorFeed detects the material, the motor starts forward rotation, and moves the material to the cleaning station.
   - When the material arrives at the cleaning station, the SensorWash detects the material, the motor stops, and upon receiving the signal washComplete after cleaning is finished, the motor starts forward rotation, moving the material to the weighing station.
   - When the material arrives at the weighing station, the SensorWeight detects the material, the motor stops, and upon receiving weightComplete after weighing is complete, the material is judged to be qualified based on the weight value. If the weight value is greater than or equal to 100 and less than or equal to 200, it is qualified, otherwise not.
     If the material is unqualified, the rejection command kick is initiated.
     If the material is qualified, the firing temperature is calculated based on the weight value. The calculation rule is that the weight value from 100 to 200 linearly corresponds to the temperature value from 500 to 550. The firing temperature firingTemp is output. At the same time, the motor starts forward rotation, moving the material to the firing station.
   - When the product arrives at the firing station, the SensorFiring detects the material, the motor stops, and upon receiving the signal firingComplete after firing is finished, the motor starts forward rotation, moving the product to the finished product station.
   - When the product arrives at the finished product station, the SensorOutput detects the product, the motor stops, and the completion light (CompletionLight) turns on, indicating that the product processing is complete. When the product is taken away, i.e., the SensorOutput does not detect the product, the completion light (CompletionLight) turns off.

## Interface Definition

| Direction | Variable/Field | Data Type | Description |
| --- | --- | --- | --- |
| Input | `Mode` | `BOOL` | Used to switch the production line between manual and automatic modes, 0 = manual mode, 1 = automatic mode |
| Input | `ForwardButton` | `BOOL` | Forward rotation button |
| Input | `ReverseButton` | `BOOL` | Reverse rotation button |
| Input | `SensorFeed` | `BOOL` | Sensor at the material loading station detecting the arrival of materials |
| Input | `SensorWash` | `BOOL` | Sensor at the cleaning station detecting the arrival of materials |
| Input | `SensorWeight` | `BOOL` | Sensor at the weighing station detecting the arrival of materials |
| Input | `SensorFiring` | `BOOL` | Sensor at the firing station detecting the arrival of materials |
| Input | `SensorOutput` | `BOOL` | Sensor at the finished product station detecting the arrival of products |
| Input | `washComplete` | `BOOL` | Signal indicating completion of cleaning |
| Input | `weightComplete` | `BOOL` | Signal indicating completion of weighing |
| Input | `weight` | `REAL` | Weight value |
| Input | `firingComplete` | `BOOL` | Signal indicating completion of firing |
| Output | `MotorForward` | `BOOL` | Output for motor forward rotation |
| Output | `MotorReverse` | `BOOL` | Output for motor reverse rotation |
| Output | `kick` | `BOOL` | Rejection output |
| Output | `CompletionLight` | `BOOL` | Indicator light for product processing completion |
| Output | `firingTemp` | `REAL` | Firing temperature |

### Scenario

A five-station conveyor cleans, rejects out-of-range weights, calculates a firing setpoint and signals output completion.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Mode | BOOL | Used to switch the production line between manual and automatic modes, 0 = manual mode, 1 = automatic mode |
| INPUT | ForwardButton | BOOL | Forward rotation button |
| INPUT | ReverseButton | BOOL | Reverse rotation button |
| INPUT | SensorFeed | BOOL | Sensor at the material loading station detecting the arrival of materials |
| INPUT | SensorWash | BOOL | Sensor at the cleaning station detecting the arrival of materials |
| INPUT | SensorWeight | BOOL | Sensor at the weighing station detecting the arrival of materials |
| INPUT | SensorFiring | BOOL | Sensor at the firing station detecting the arrival of materials |
| INPUT | SensorOutput | BOOL | Sensor at the finished product station detecting the arrival of products |
| INPUT | washComplete | BOOL | Signal indicating completion of cleaning |
| INPUT | weightComplete | BOOL | Signal indicating completion of weighing |
| INPUT | weight | REAL | Weight value |
| INPUT | firingComplete | BOOL | Signal indicating completion of firing |
| OUTPUT | MotorForward | BOOL | Output for motor forward rotation |
| OUTPUT | MotorReverse | BOOL | Output for motor reverse rotation |
| OUTPUT | kick | BOOL | Rejection output |
| OUTPUT | CompletionLight | BOOL | Indicator light for product processing completion |
| OUTPUT | firingTemp | REAL | Firing temperature |

### Initial conditions

```json
{
  "MotorForward": false,
  "MotorReverse": false,
  "kick": false,
  "CompletionLight": false,
  "firingTemp": 0.0,
  "phase": "WAIT_FEED"
}
```

### Scan semantics

Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

### Safety and priorities

- Forward and reverse are mutually exclusive.
- Destination arrival stops forward motion.
- Unqualified weight never proceeds to firing.
- Completion commands from an unrelated station are ignored.

### Explicit assumptions

- Manual opposing requests both inhibit the motor. Entering manual clears sequence, kick and completion but retains the last firing setpoint.
- Only one product is processed; the caller does not assert contradictory station sensors.
- Mode changes reset the automatic route to WAIT_FEED. Confirmations are levels accepted only in their corresponding processing wait.
- Arrival has priority; a confirmation already TRUE on the arrival invocation is accepted no earlier than the next invocation.
- A rejected item remains at the weighing station, with kick TRUE, until SensorWeight becomes FALSE. It then returns to WAIT_FEED.
- firingTemp updates only when accepted weight satisfies 100.0 <= real32(weight) <= 200.0 (binary32 rounding applied prior to range test) and retains the last accepted value otherwise. REAL firingTemp comparisons use absolute tolerance 1e-4 to exceed 1 ULP near 550.0.
- At most one phase transition occurs per invocation. Output arrival sets CompletionLight immediately, removal clears it and resets the route.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `auto`: Mode
- `fwd`: MotorForward
- `rev`: MotorReverse
- `mf`: ForwardButton AND NOT ReverseButton
- `mr`: ReverseButton AND NOT ForwardButton
- `feed`: pre-phase WAIT_FEED AND SensorFeed
- `moving`: pre-phase is a conveyor movement (MOVE_TO_WASH, MOVE_TO_WEIGHT, MOVE_TO_FIRING, or MOVE_TO_OUTPUT)
- `arrival`: pre-phase moving AND corresponding destination sensor TRUE
- `stopped`: NOT MotorForward AND NOT MotorReverse
- `judged`: auto AND pre-phase WAIT_WEIGHT AND SensorWeight AND weightComplete
- `valid`: 100.0 <= real32(weight) <= 200.0
- `reject`: kick AND stopped
- `qualified`: NOT kick AND fwd AND firingTemp=real32(500.0+real32(real32(weight-100.0)*0.5))
- `output_arrival`: auto AND pre-phase MOVE_TO_OUTPUT AND SensorOutput
- `light`: CompletionLight
- `removed`: auto AND pre-phase OUTPUT_DONE AND NOT SensorOutput
- `clear`: NOT CompletionLight AND stopped
- `no_judgment`: NOT judged OR NOT valid
- `same_temp`: firingTemp=pre-firingTemp
- `arrival_pending`: pre-phase is a conveyor movement
- `processing_wait`: pre-phase is WAIT_WASH, WAIT_WEIGHT or WAIT_FIRING
- `matching_completion`: matching station sensor and processing completion are TRUE in the corresponding wait
- `order`: automatic route is FEED, WASH, WEIGHT, FIRING, OUTPUT; rejected weights cannot enter FIRING
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_PUB020(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
参考阶段WAIT_FEED→MOVE_WASH→WAIT_WASH→MOVE_WEIGHT→WAIT_WEIGHT→REJECT或MOVE_FIRING→WAIT_FIRING→MOVE_OUTPUT→OUTPUT_DONE；每拍按旧阶段只推进一阶。重量100..200含边界合格，合格温度real32(500+real32(real32(weight-100)*0.5))；不合格保持温度并剔除至SensorWeight假。完成取走后回初始。手动清流程、方向按钮互锁、kick/灯关闭、温度保持。自动仅运输阶段正转、不反转；kick对应REJECT、灯对应OUTPUT_DONE。
- `Mode`: I[k].Mode: sampled input (BOOL).
- `ForwardButton`: I[k].ForwardButton: sampled input (BOOL).
- `ReverseButton`: I[k].ReverseButton: sampled input (BOOL).
- `SensorFeed`: I[k].SensorFeed: sampled input (BOOL).
- `SensorWash`: I[k].SensorWash: sampled input (BOOL).
- `SensorWeight`: I[k].SensorWeight: sampled input (BOOL).
- `SensorFiring`: I[k].SensorFiring: sampled input (BOOL).
- `SensorOutput`: I[k].SensorOutput: sampled input (BOOL).
- `washComplete`: I[k].washComplete: sampled input (BOOL).
- `weightComplete`: I[k].weightComplete: sampled input (BOOL).
- `weight`: I[k].weight: sampled input (REAL).
- `firingComplete`: I[k].firingComplete: sampled input (BOOL).
- `MotorForward`: O[k].MotorForward: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `MotorReverse`: O[k].MotorReverse: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `kick`: O[k].kick: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `CompletionLight`: O[k].CompletionLight: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `firingTemp`: O[k].firingTemp: independently observed post-scan candidate value (REAL); never defined as expected output.
- `post_wait`: post-phase is WAIT_FEED, WAIT_WASH, WAIT_WEIGHT, or WAIT_FIRING
- `post_move`: post-phase is MOVE_TO_WASH, MOVE_TO_WEIGHT, MOVE_TO_FIRING, or MOVE_TO_OUTPUT
- `init`: At the separate pre-invocation initial observation before scan k=0: Spre.phase="WAIT_FEED", O_init.MotorForward=false, O_init.MotorReverse=false, O_init.kick=false, O_init.CompletionLight=false, O_init.firingTemp=0.0.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 0.0
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "PUB020",
      "array_contract": null,
      "process_contract": {
        "class": "ProcessContract",
        "state": {
          "task_id": "PUB020",
          "phase": 0,
          "mode": null,
          "previous": {},
          "latches": [
            false,
            false,
            false,
            false,
            false
          ],
          "batch_mode": null,
          "route": null,
          "index": 0,
          "station": 1,
          "target": 1,
          "temperature": 0.0,
          "arm_mode": null,
          "arm_step": 0,
          "step_index": 1,
          "step_busy": false,
          "prev_start": false
        }
      },
      "timed_contract": null,
      "data_contract": null,
      "reference": null,
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('PUB020'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "CompletionLight",
    "MotorForward",
    "MotorReverse",
    "firingTemp",
    "kick"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "phase": {
      "pre": "Spre.process_contract.phase",
      "post": "Spost.process_contract.phase",
      "enum": {
        "0": "WAIT_FEED",
        "1": "MOVE_TO_WASH",
        "2": "WAIT_WASH",
        "3": "MOVE_TO_WEIGHT",
        "4": "WAIT_WEIGHT",
        "5": "REJECT",
        "6": "MOVE_TO_FIRING",
        "7": "WAIT_FIRING",
        "8": "MOVE_TO_OUTPUT",
        "9": "OUTPUT_DONE"
      },
      "initial": 0
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "Manual opposing requests both inhibit the motor. Entering manual clears sequence, kick and completion but retains the last firing setpoint.",
    "Only one product is processed; the caller does not assert contradictory station sensors.",
    "Mode changes reset the automatic route to WAIT_FEED. Confirmations are levels accepted only in their corresponding processing wait.",
    "Arrival has priority; a confirmation already TRUE on the arrival invocation is accepted no earlier than the next invocation.",
    "A rejected item remains at the weighing station, with kick TRUE, until SensorWeight becomes FALSE. It then returns to WAIT_FEED.",
    "firingTemp updates only when accepted weight satisfies 100.0 <= real32(weight) <= 200.0 (binary32 rounding applied prior to range test) and retains the last accepted value otherwise. REAL firingTemp comparisons use absolute tolerance 1e-4 to exceed 1 ULP near 550.0.",
    "At most one phase transition occurs per invocation. Output arrival sets CompletionLight immediately, removal clears it and resets the route.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "Floating-point inputs and intermediate reference arithmetic are finite. Existing fixed traces retain their declared absolute tolerance; claims do not extend to arbitrary magnitudes without a separately specified numeric error policy.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "参考阶段WAIT_FEED→MOVE_WASH→WAIT_WASH→MOVE_WEIGHT→WAIT_WEIGHT→REJECT或MOVE_FIRING→WAIT_FIRING→MOVE_OUTPUT→OUTPUT_DONE；每拍按旧阶段只推进一阶。重量100..200含边界合格，合格温度real32(500+real32(real32(weight-100)*0.5))；不合格保持温度并剔除至SensorWeight假。完成取走后回初始。手动清流程、方向按钮互锁、kick/灯关闭、温度保持。自动仅运输阶段正转、不反转；kick对应REJECT、灯对应OUTPUT_DONE。"
}
```

**PUB020.P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**PUB020.P1** Interlock

```text
G(!(fwd & rev))
```

Motor directions cannot overlap.

**PUB020.P2** Manual

```text
G(!auto -> ((fwd <-> mf) & (rev <-> mr)))
```

Manual commands follow level inputs with neutral conflict handling.

**PUB020.P3** Automatic direction

```text
G(auto -> !rev)
```

The automatic route never reverses.

**PUB020.P4** Arrival stop

```text
G(auto & arrival -> stopped)
```

An arrived item stops before processing.

**PUB020.P5** Weight decision

```text
G(judged -> ((valid -> qualified) & (!valid -> reject)))
```

The acceptance interval is inclusive and its setpoint is linear.

**PUB020.P6** Setpoint retention

```text
G(no_judgment -> same_temp)
```

No unqualified or unrelated scan changes the last accepted setpoint.

**PUB020.P7** Completion

```text
G((output_arrival -> light) & (removed -> clear))
```

Output arrival and removal control the light.

**PUB020.P8** Route

```text
G(order)
```

Only the ordered processing route advances qualified products.

**PUB020.P9** Conditional completion

```text
(G(auto) & G(arrival_pending -> F arrival) & G(processing_wait -> F matching_completion) & G(judged -> valid)) -> G(feed -> F light)
```

With continuing automatic mode, eventual movement/processing feedback and accepted weights, each feed eventually completes.

**PUB020.P10**

```text
G((!auto -> (!kick & !CompletionLight)) & (auto & post_wait -> stopped) & (auto & post_move -> (fwd & !rev)))
```

Closes independent LTL coverage of manual/waiting/transport actuator behavior.

**PUB020.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB020.T1 | Forward, reverse, both buttons and no request. | 4 |
| PUB020.T2 | Inclusive acceptance and linear firing setpoint for weight 100.0 | 11 |
| PUB020.T3 | Inclusive acceptance and linear firing setpoint for weight 150.0 | 11 |
| PUB020.T4 | Inclusive acceptance and linear firing setpoint for weight 200.0 | 11 |
| PUB020.T5 | Reject just outside the inclusive limits, retain rejection until removal. | 9 |
| PUB020.T6 | Reject just outside the inclusive limits, retain rejection until removal. | 9 |
| PUB020.T7 | Out-of-order completions do not move an idle product. | 4 |
| V2_process_history_regression | Mode/edge reset, repeated station or prior-batch retained setpoint regression. | 16 |
| PUB020.T8 | PUB020.T8 | 14 |
| PUB020.R22.all_transport | 四段持续运输、加工等待与完整第二批次 | 58 |
| PUB020.R22.mode_reset | 运输中切手动再切自动、路线复位且温度保持 | 9 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF001 Guarded motor with retained run command

Origin: self_built. Difficulty: easy.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 1,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "A packaging motor uses a door guard as a scan-level permissive and a retained operator run request.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF001: Guarded Motor Latch

## Background
Teaching controller for a guarded single-motor latch (not a safety-rated circuit).

## Functional Requirements
1. Inputs: `Start`, `Stop`, and `GuardClosed` (`BOOL`, all level-sensitive).
2. On every scan, if `Stop = TRUE` or `GuardClosed = FALSE`, force `Run := FALSE`.
3. Otherwise, if `Start = TRUE`, set `Run := TRUE` (including when `Start` stays TRUE on the scan `GuardClosed` closes).
4. Otherwise retain the previous `Run` state.

## Interface
- **Inputs:** `Start: BOOL`, `Stop: BOOL`, `GuardClosed: BOOL`
- **Outputs:** `Run: BOOL`

## Initial Values
- `Run=false`

## Timing & Evaluation Conventions
Signals are sampled every scan (`dt_ms` is unused for logical transitions).

### Scenario

A packaging motor uses a door guard as a scan-level permissive and a retained operator run request.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Start | BOOL | Operator start request |
| INPUT | Stop | BOOL | Stop request |
| INPUT | GuardClosed | BOOL | Door permissive |
| OUTPUT | Run | BOOL | Motor run command |

### Initial conditions

```json
{
  "Run": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Open guard and Stop override Start
- Loss of permissive clears the retained latch

### Explicit assumptions

- Inputs are level-sensitive; no start edge is required.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `Start`: I[k].Start: sampled input (BOOL).
- `Stop`: I[k].Stop: sampled input (BOOL).
- `GuardClosed`: I[k].GuardClosed: sampled input (BOOL).
- `Run`: O[k].Run: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `qRun`: {"kind": "previous_observed_output", "source": "O[k-1].Run", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].Run; never write into reference state."}
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF001(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
r初值FALSE；rAfter=GuardClosed & !Stop & (Start | rBefore)；期望Run=rAfter。
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.Run=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Run": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF001",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF001",
          "state": {
            "run": false
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF001'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Run"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "qRun": {
      "kind": "previous_observed_output",
      "source": "O[k-1].Run",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].Run; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "Inputs are level-sensitive; no start edge is required.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "r初值FALSE；rAfter=GuardClosed & !Stop & (Start | rBefore)；期望Run=rAfter。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(first -> !qRun)
```

The instance starts with no retained run request.

**P2**

```text
G((Stop | !GuardClosed) -> !Run)
```

Stop and guard override every startup request in the same scan.

**P3**

```text
G((Start & !Stop & GuardClosed) -> Run)
```

A permitted start takes effect at end of the sampled scan.

**P4**

```text
G((!Start & !Stop & GuardClosed) -> (Run <-> qRun))
```

Retain the preceding run value without a new command.

**P5**

```text
G(Run -> X(Stop | !GuardClosed | Run))
```

Across invocations, run persists unless a higher-priority input intervenes.

**SELF001.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| latch | Initialize, start, hold and stop | 5 |
| priority | Simultaneous requests and guard recovery | 5 |
| SELF001.boundary_start_hold | SELF001.boundary_start_hold | 5 |
| SELF001.R22.normal_changes | 持续启动时停止解除 | 3 |
| SELF001.R22.tail_Start | 完成主流程后改变并保持 Start | 7 |
| SELF001.R22.tail_Stop | 完成主流程后改变并保持 Stop | 7 |
| SELF001.R22.tail_GuardClosed | 完成主流程后改变并保持 GuardClosed | 7 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF002 Reversing jog drive with a neutral scan

Origin: self_built. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 2,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "A reversible positioning drive must break its previous direction command for one full output scan before reversing.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF002: Bidirectional Reversing Interlock with One-Scan Stop

## Background
Forward/reverse motor interlock preventing immediate reversal on consecutive scans.

## Functional Requirements
1. Inputs: `ForwardButton`, `ReverseButton`, and `Stop` (`BOOL`).
2. Compute desired direction: `0` (stop) if `Stop = TRUE` or `ForwardButton = ReverseButton`; `+1` if only `ForwardButton = TRUE`; `-1` if only `ReverseButton = TRUE`.
3. If desired direction is nonzero and opposite to the previous scan's active direction (`-1` vs `+1`), force both outputs FALSE for this one intermediate stop scan (clearing direction memory to `0`).
4. Otherwise output the desired direction (`Forward := (dir = +1)`, `Reverse := (dir = -1)`) and store it.

## Interface
- **Inputs:** `ForwardButton: BOOL`, `ReverseButton: BOOL`, `Stop: BOOL`
- **Outputs:** `Forward: BOOL`, `Reverse: BOOL`

## Initial Values
- `previous_direction=0`, `Forward=false`, `Reverse=false`

## Timing & Evaluation Conventions
All inputs are level-sensitive; direction memory initializes to `0` (stopped).

### Scenario

A reversible positioning drive must break its previous direction command for one full output scan before reversing.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | ForwardButton | BOOL | Forward jog request |
| INPUT | ReverseButton | BOOL | Reverse jog request |
| INPUT | Stop | BOOL | Stop request |
| OUTPUT | Forward | BOOL | Forward contactor command |
| OUTPUT | Reverse | BOOL | Reverse contactor command |

### Initial conditions

```json
{
  "previous_direction": 0,
  "Forward": false,
  "Reverse": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Stop and ambiguous button combinations command neutral
- Opposite-direction request inserts neutral

### Explicit assumptions

- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `ForwardButton`: I[k].ForwardButton: sampled input (BOOL).
- `ReverseButton`: I[k].ReverseButton: sampled input (BOOL).
- `Stop`: I[k].Stop: sampled input (BOOL).
- `Forward`: O[k].Forward: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Reverse`: O[k].Reverse: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `qForward`: {"kind": "previous_observed_output", "source": "O[k-1].Forward", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].Forward; never write into reference state."}
- `qReverse`: {"kind": "previous_observed_output", "source": "O[k-1].Reverse", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].Reverse; never write into reference state."}
- `fwdOnly`: ForwardButton & !ReverseButton & !Stop.
- `revOnly`: ReverseButton & !ForwardButton & !Stop.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF002(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
d初值0；desired在Stop或两方向按钮相等时为0，否则前进1/后退-1。dAfter在desired!=0且dBefore=-desired时为0，否则desired；Forward=(dAfter=1)，Reverse=(dAfter=-1)。
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.Forward=false, O_init.Reverse=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Forward": false,
    "Reverse": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF002",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF002",
          "state": {
            "direction": 0
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF002'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Forward",
    "Reverse"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "qForward": {
      "kind": "previous_observed_output",
      "source": "O[k-1].Forward",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].Forward; never write into reference state."
    },
    "qReverse": {
      "kind": "previous_observed_output",
      "source": "O[k-1].Reverse",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].Reverse; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "d初值0；desired在Stop或两方向按钮相等时为0，否则前进1/后退-1。dAfter在desired!=0且dBefore=-desired时为0，否则desired；Forward=(dAfter=1)，Reverse=(dAfter=-1)。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(!(Forward & Reverse))
```

Direction outputs are mutually exclusive.

**P2**

```text
G((Stop | (ForwardButton <-> ReverseButton)) -> (!Forward & !Reverse))
```

Invalid or stopped requests produce neutral.

**P3**

```text
G((fwdOnly & qReverse) -> (!Forward & !Reverse))
```

Reversal from reverse has one neutral output scan.

**P4**

```text
G((revOnly & qForward) -> (!Forward & !Reverse))
```

Reversal from forward has one neutral output scan.

**P5**

```text
G((fwdOnly & !qReverse) -> Forward)
```

A permitted forward jog operates immediately.

**P6**

```text
G((revOnly & !qForward) -> Reverse)
```

A permitted reverse jog operates immediately.

**SELF002.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| reverse | Direct reversal and held reverse request | 6 |
| ambiguous | Both buttons and Stop override direction | 4 |
| SELF002.boundary_reverse_memory | SELF002.boundary_reverse_memory | 5 |
| SELF002.R22.normal_changes | 倒转停止及方向记忆清除 | 5 |
| SELF002.R22.tail_ForwardButton | 完成主流程后改变并保持 ForwardButton | 8 |
| SELF002.R22.tail_ReverseButton | 完成主流程后改变并保持 ReverseButton | 8 |
| SELF002.R22.tail_Stop | 完成主流程后改变并保持 Stop | 8 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF003 Emergency stop reset with restart inhibition

Origin: self_built. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 3,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "A workshop spindle requires a deliberate reset with Start released before a restart after emergency-stop release.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF003: Safety-Reset Latched Motor Control

## Background
Motor latch requiring explicit isolated reset after power-up or E-stop loss.

## Functional Requirements
1. Inputs: `Start`, `Stop`, `EStopNC` (`TRUE` when healthy), and `Reset` (`BOOL`).
2. If `EStopNC = FALSE`, set `ResetRequired := TRUE` and `Run := FALSE` immediately.
3. While `ResetRequired = TRUE`, `Run` stays `FALSE`; `ResetRequired` clears to `FALSE` only when `Reset = TRUE AND Start = FALSE AND Stop = FALSE`.
4. When `ResetRequired = FALSE` and `EStopNC = TRUE`: `Stop = TRUE` clears `Run := FALSE`; else `Start = TRUE` sets `Run := TRUE`; else `Run` retains.

## Interface
- **Inputs:** `Start: BOOL`, `Stop: BOOL`, `EStopNC: BOOL`, `Reset: BOOL`
- **Outputs:** `Run: BOOL`, `ResetRequired: BOOL`

## Initial Values
- `Run=false`, `ResetRequired=true`

## Timing & Evaluation Conventions
Safety-circuit logic evaluates priority strictly in the order E-stop > ResetRequired > Stop > Start.

### Scenario

A workshop spindle requires a deliberate reset with Start released before a restart after emergency-stop release.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Start | BOOL | Start request |
| INPUT | Stop | BOOL | Normal stop request |
| INPUT | EStopNC | BOOL | TRUE means emergency stop released |
| INPUT | Reset | BOOL | Reset request |
| OUTPUT | Run | BOOL | Spindle run command |
| OUTPUT | ResetRequired | BOOL | Restart inhibition latch |

### Initial conditions

```json
{
  "Run": false,
  "ResetRequired": true
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Emergency stop overrides all requests
- Restart inhibition overrides Start
- Normal stop overrides Start

### Explicit assumptions

- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `Start`: I[k].Start: sampled input (BOOL).
- `Stop`: I[k].Stop: sampled input (BOOL).
- `EStopNC`: I[k].EStopNC: sampled input (BOOL).
- `Reset`: I[k].Reset: sampled input (BOOL).
- `Run`: O[k].Run: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `ResetRequired`: O[k].ResetRequired: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `qRequired`: {"kind": "previous_observed_output", "source": "O[k-1].ResetRequired", "initial": true, "update": "After comparing scan k, store ACTUAL O[k].ResetRequired; never write into reference state."}
- `qRun`: {"kind": "previous_observed_output", "source": "O[k-1].Run", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].Run; never write into reference state."}
- `validReset`: EStopNC & Reset & !Start & !Stop.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF003(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
required初值TRUE、run初值FALSE。按顺序选择首个分支：!EStopNC置required=TRUE/run=FALSE；旧required真时run=FALSE，仅Reset & !Start & !Stop清required；否则Stop清run、否则Start置run，其余保持。两个实际输出分别比较runAfter、requiredAfter。
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.Run=false, O_init.ResetRequired=true.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Run": false,
    "ResetRequired": true
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF003",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF003",
          "state": {
            "required": true,
            "run": false
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF003'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "ResetRequired",
    "Run"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "qRun": {
      "kind": "previous_observed_output",
      "source": "O[k-1].Run",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].Run; never write into reference state."
    },
    "qRequired": {
      "kind": "previous_observed_output",
      "source": "O[k-1].ResetRequired",
      "initial": true,
      "update": "After comparing scan k, store ACTUAL O[k].ResetRequired; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "required初值TRUE、run初值FALSE。按顺序选择首个分支：!EStopNC置required=TRUE/run=FALSE；旧required真时run=FALSE，仅Reset & !Start & !Stop清required；否则Stop清run、否则Start置run，其余保持。两个实际输出分别比较runAfter、requiredAfter。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(first -> (qRequired & !qRun))
```

A fresh instance requires reset.

**P2**

```text
G(!EStopNC -> (!Run & ResetRequired))
```

Emergency stop forces safe outputs immediately.

**P3**

```text
G(qRequired -> !Run)
```

Reset acceptance and motor start cannot share one scan.

**P4**

```text
G((qRequired & EStopNC) -> (ResetRequired <-> !validReset))
```

Reset requires released Start and Stop.

**P5**

```text
G((!qRequired & EStopNC & !Stop & Start) -> Run)
```

A subsequent permitted start energizes the motor.

**P6**

```text
G((!qRequired & EStopNC & Stop) -> !Run)
```

Stop has priority after reset.

**SELF003.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

**SELF003.V2.1**

```text
G((!qRequired & EStopNC) -> !ResetRequired)
```

Explicit correction of a demonstrated omission.

**SELF003.V2.2**

```text
G((!qRequired & EStopNC & !Stop & !Start) -> (Run <-> qRun))
```

Explicit correction of a demonstrated omission.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| reset_restart | Power-up inhibition, reset, run and emergency stop | 6 |
| invalid_reset | Held Start and Stop block reset | 4 |
| V2_omission_regression | Reject the concrete wrong behavior documented in the 2026-11-06 specification review. | 4 |
| SELF003.boundary_reset_isolation | SELF003.boundary_reset_isolation | 7 |
| SELF003.R22.reset_stops_run | 按当前参考，已解除复位要求后单独Reset不停止运行 | 4 |
| SELF003.R22.normal_changes | 运行中Reset保持、停止后重启 | 5 |
| SELF003.R22.tail_Start | 完成主流程后改变并保持 Start | 8 |
| SELF003.R22.tail_Stop | 完成主流程后改变并保持 Stop | 8 |
| SELF003.R22.tail_EStopNC | 完成主流程后改变并保持 EStopNC | 8 |
| SELF003.R22.tail_Reset | 完成主流程后改变并保持 Reset | 8 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF004 Pallet indexing with a latched jam fault

Origin: self_built. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 4,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "A small conveyor indexes one pallet to an exit sensor and preserves a jam indication until a deliberate reset.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF004: Transfer Conveyor Cycle with Jam Fault

## Background
Four-state (`IDLE`, `MOVING`, `COMPLETE`, `FAULT`) transfer conveyor cycle with jam supervision.

## Functional Requirements
1. Inputs: `Start`, `Stop`, `AtExit`, `Jam`, `Reset` (`BOOL`).
2. Priority order per scan: (1) `Jam = TRUE` -> `FAULT`; (2) `Reset = TRUE` -> `IDLE`; (3) if already in `FAULT`, remain in `FAULT` until cleared by `Reset` (without `Jam`); (4) `Stop = TRUE` -> `IDLE`; (5) if in `MOVING` and `AtExit = TRUE` -> `COMPLETE`; (6) if in `IDLE`, `Start = TRUE`, and `AtExit = FALSE` -> `MOVING`; (7) otherwise hold state.
3. Outputs reflect post-transition state: `Belt <-> MOVING`, `Complete <-> COMPLETE`, `Fault <-> FAULT` (at most one active).

## Interface
- **Inputs:** `Start: BOOL`, `Stop: BOOL`, `AtExit: BOOL`, `Jam: BOOL`, `Reset: BOOL`
- **Outputs:** `Belt: BOOL`, `Complete: BOOL`, `Fault: BOOL`

## Initial Values
- `state="IDLE"`, `Belt=false`, `Complete=false`, `Fault=false`

## Timing & Evaluation Conventions
All signals are level-sensitive; a single scan executes at most one state step.

### Scenario

A small conveyor indexes one pallet to an exit sensor and preserves a jam indication until a deliberate reset.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Start | BOOL | Start one pallet |
| INPUT | Stop | BOOL | Abort cycle |
| INPUT | AtExit | BOOL | Pallet at exit |
| INPUT | Jam | BOOL | Jam detected |
| INPUT | Reset | BOOL | Clear completion or cleared jam |
| OUTPUT | Belt | BOOL | Conveyor command |
| OUTPUT | Complete | BOOL | Pallet cycle completed |
| OUTPUT | Fault | BOOL | Latched jam fault |

### Initial conditions

```json
{
  "state": "IDLE",
  "Belt": false,
  "Complete": false,
  "Fault": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Jam
- Reset when Jam is FALSE
- Latched fault
- Stop
- Normal transition

### Explicit assumptions

- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `Start`: I[k].Start: sampled input (BOOL).
- `Stop`: I[k].Stop: sampled input (BOOL).
- `AtExit`: I[k].AtExit: sampled input (BOOL).
- `Jam`: I[k].Jam: sampled input (BOOL).
- `Reset`: I[k].Reset: sampled input (BOOL).
- `Belt`: O[k].Belt: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Complete`: O[k].Complete: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Fault`: O[k].Fault: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `qIdle`: Spre.reference.state.mode=0
- `qMoving`: Spre.reference.state.mode=1
- `qComplete`: Spre.reference.state.mode=2
- `qFault`: Spre.reference.state.mode=3
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF004(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
mode初值IDLE。优先Jam→FAULT，其次Reset→IDLE，其次旧FAULT保持，其次Stop→IDLE，其次旧MOVING且AtExit→COMPLETE，其次旧IDLE且Start且!AtExit→MOVING，其余保持。Belt/Complete/Fault分别等价于新mode为MOVING/COMPLETE/FAULT。
- `init`: At the separate pre-invocation initial observation before scan k=0: Spre.mode=IDLE, O_init.Belt=false, O_init.Complete=false, O_init.Fault=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Belt": false,
    "Complete": false,
    "Fault": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF004",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF004",
          "state": {
            "mode": 0
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF004'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Belt",
    "Complete",
    "Fault"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "phase": {
      "pre": "Spre.reference.state.mode",
      "post": "Spost.reference.state.mode",
      "enum": {
        "0": "IDLE",
        "1": "MOVING",
        "2": "COMPLETE",
        "3": "FAULT"
      },
      "initial": 0
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "mode初值IDLE。优先Jam→FAULT，其次Reset→IDLE，其次旧FAULT保持，其次Stop→IDLE，其次旧MOVING且AtExit→COMPLETE，其次旧IDLE且Start且!AtExit→MOVING，其余保持。Belt/Complete/Fault分别等价于新mode为MOVING/COMPLETE/FAULT。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(Jam -> (Fault & !Belt & !Complete))
```

Jam wins over Reset and Start.

**P2**

```text
G((qFault & !Reset) -> Fault)
```

Fault requires an explicit clear operation.

**P3**

```text
G((!Jam & Reset) -> (!Belt & !Complete & !Fault))
```

A cleared-jam reset returns IDLE.

**P4**

```text
G((qIdle & !Jam & !Reset & !Stop & Start & !AtExit) -> Belt)
```

A valid idle start moves the pallet.

**P5**

```text
G((qMoving & AtExit & !Jam & !Reset & !Stop) -> (Complete & !Belt))
```

Exit arrival stops indexing in the same scan.

**P6**

```text
G(!(Belt & (Complete | Fault)))
```

Movement excludes completion and fault outputs.

**P7**

```text
G(Fault -> (G Fault | (Fault U (!Jam & Reset))))
```

A latched jam remains until a cleared-jam reset, or forever if no such reset occurs; this does not assume eventual reset.

**P8**

```text
G((!Jam & !Reset & !qFault & Stop -> (!Belt & !Complete & !Fault)) & (qIdle & !Jam & !Reset & (!Start | AtExit) -> (!Belt & !Complete & !Fault)) & (qMoving & !Jam & !Reset & !Stop & !AtExit -> (Belt & !Complete & !Fault)) & (qComplete & !Jam & !Reset & !Stop -> (Complete & !Belt & !Fault)))
```

Prevents degenerate implementations that refuse to stop or drop MOVING/COMPLETE prematurely.

**P9**

```text
G(!(Belt & Complete) & (!(Jam | qFault) -> !Fault) & ((qIdle | qFault | Stop | Reset) -> !Complete))
```

Eliminates remaining false-positive satisfaction paths on P1..P8.

**SELF004.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| index | One pallet and retained completion | 5 |
| jam | Jam priority, retained fault and safe reset | 6 |
| SELF004.boundary_stop_and_fault | SELF004.boundary_stop_and_fault | 10 |
| SELF004.R22.tail_Start | 完成主流程后改变并保持 Start | 7 |
| SELF004.R22.tail_Stop | 完成主流程后改变并保持 Stop | 7 |
| SELF004.R22.tail_AtExit | 完成主流程后改变并保持 AtExit | 7 |
| SELF004.R22.tail_Jam | 完成主流程后改变并保持 Jam | 7 |
| SELF004.R22.tail_Reset | 完成主流程后改变并保持 Reset | 7 |
| SELF004.R22.priority_recovery | 动作中停止／矛盾信号与恢复 | 5 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF005 Three phase signal with externally clocked durations

Origin: self_built. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 5,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "A training traffic signal uses a deterministic logical tick, allowing reproducible testing without wall-clock timing jitter.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF005: Three-Phase Cyclic Traffic Light Controller

## Background
Three-phase traffic signal (`RED=0`, `GREEN=1`, `AMBER=2`) stepping on logical `Tick` pulses.

## Functional Requirements
1. Inputs: `Enable` and `Tick` (`BOOL`). Phase durations are fixed logical tick thresholds: `RED: 2`, `GREEN: 3`, `AMBER: 1`.
2. Whenever `Enable = FALSE`, reset phase to `RED (0)` and elapsed tick counter `age := 0`.
3. When `Enable = TRUE` and `Tick = FALSE`, keep current phase and `age` unchanged.
4. When `Enable = TRUE` and `Tick = TRUE`, increment `age`; when `age` reaches the current phase threshold (`2`, `3`, `1`), advance `(phase + 1) mod 3` and reset `age := 0`.
5. Outputs follow post-transition phase: `Phase := phase`, `Red <-> (phase = 0)`, `Green <-> (phase = 1)`, `Amber <-> (phase = 2)`.

## Interface
- **Inputs:** `Enable: BOOL`, `Tick: BOOL`
- **Outputs:** `Red: BOOL`, `Green: BOOL`, `Amber: BOOL`, `Phase: USINT`

## Initial Values
- `phase=0`, `elapsed_ticks=0`, `Red=true`, `Green=false`, `Amber=false`, `Phase=0`

## Timing & Evaluation Conventions
`Tick` is a logical invocation count (`1` count per scan where `Tick = TRUE`), not physical `dt_ms` time.

### Scenario

A training traffic signal uses a deterministic logical tick, allowing reproducible testing without wall-clock timing jitter.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Enable | BOOL | Enable normal signal cycle |
| INPUT | Tick | BOOL | One logical tick on each TRUE invocation |
| OUTPUT | Red | BOOL | Red lamp |
| OUTPUT | Green | BOOL | Green lamp |
| OUTPUT | Amber | BOOL | Amber lamp |
| OUTPUT | Phase | USINT | Post-scan phase number |

### Initial conditions

```json
{
  "phase": 0,
  "elapsed_ticks": 0,
  "Red": true,
  "Green": false,
  "Amber": false,
  "Phase": 0
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Disable resets the cycle to RED

### Explicit assumptions

- A logical tick is not claimed to be a physical second.
- No opposite road or pedestrian signal is controlled.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `Enable`: I[k].Enable: sampled input (BOOL).
- `Tick`: I[k].Tick: sampled input (BOOL).
- `Red`: O[k].Red: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Green`: O[k].Green: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Amber`: O[k].Amber: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Phase`: O[k].Phase: independently observed post-scan candidate value (USINT); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `qRedLast`: Spre.reference.state.phase=0 AND Spre.reference.state.age=1
- `qGreenLast`: Spre.reference.state.phase=1 AND Spre.reference.state.age=2
- `qAmber`: Spre.reference.state.phase=2
- `qPhase`: Spre.reference.state.phase
- `oneColor`: int(O[k].Red)+int(O[k].Green)+int(O[k].Amber)=1
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF005(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
phase=0/age=0初值。!Enable时重置0/0；否则Tick时age加1，到当前phase的阈值(2,3,1)则phase=(phase+1)%3且age=0；其他保持。Red/Green/Amber分别等价于新phase=0/1/2，Phase等于新phase。Tick是逻辑调用计数，不是物理时间。
- `init`: At the separate pre-invocation initial observation before scan k=0: Spre.phase=0, O_init.Red=true, O_init.Green=false, O_init.Amber=false, O_init.Phase=0.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Red": true,
    "Green": false,
    "Amber": false,
    "Phase": 0
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF005",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF005",
          "state": {
            "phase": 0,
            "age": 0
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF005'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Amber",
    "Green",
    "Phase",
    "Red"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "phase": {
      "pre": "Spre.reference.state.phase",
      "post": "Spost.reference.state.phase",
      "enum": {
        "0": "RED",
        "1": "GREEN",
        "2": "AMBER"
      },
      "initial": 0
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "A logical tick is not claimed to be a physical second.",
    "No opposite road or pedestrian signal is controlled.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "phase=0/age=0初值。!Enable时重置0/0；否则Tick时age加1，到当前phase的阈值(2,3,1)则phase=(phase+1)%3且age=0；其他保持。Red/Green/Amber分别等价于新phase=0/1/2，Phase等于新phase。Tick是逻辑调用计数，不是物理时间。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(oneColor)
```

The lamp encoding is one-hot.

**P2**

```text
G(!Enable -> (Red & !Green & !Amber & Phase=0))
```

When Enable is FALSE, immediately force Red (Phase=0) with age reset to 0.

**P3**

```text
G((Enable & !Tick) -> (Phase = qPhase))
```

No tick preserves phase.

**P4**

```text
G((Enable & Tick & qRedLast) -> Green)
```

The second red tick enters green.

**P5**

```text
G((Enable & Tick & qGreenLast) -> Amber)
```

The third green tick enters amber.

**P6**

```text
G((Enable & Tick & qAmber) -> Red)
```

One amber tick returns red.

**P7**

```text
(G Enable & G(F Tick)) -> (G(F Red) & G(F Green) & G(F Amber))
```

Persistent enable plus infinitely many ticks makes every phase recur; finite traces cannot prove this liveness property.

**P8**

```text
G((Red <-> Phase=0) & (Green <-> Phase=1) & (Amber <-> Phase=2) & (Phase>=0 & Phase<=2))
```

Previously Phase was left unconstrained except for holding on !Tick.

**P9**

```text
G((Enable & Tick & !qRedLast & !qGreenLast & !qAmber) -> (Phase = qPhase))
```

Prevents single-tick skipping through Red (needs 2 ticks) or Green (needs 3 ticks).

**SELF005.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| cycle | Full phase duration boundaries and pause | 7 |
| disable | Disable clears elapsed tick progress | 5 |
| SELF005.boundary_pause_resume | SELF005.boundary_pause_resume | 10 |
| SELF005.R22.green_pause | 绿灯阶段暂停Tick应保持颜色 | 4 |
| SELF005.R22.normal_changes | 完整两轮各相位暂停并保留计龄 | 22 |
| SELF005.R22.tail_Enable | 完成主流程后改变并保持 Enable | 9 |
| SELF005.R22.tail_Tick | 完成主流程后改变并保持 Tick | 9 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF006 Tank filling with hysteresis and sensor inconsistency

Origin: self_built. Difficulty: easy.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 6,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "A refill tank avoids contactor chatter between low and high level switches and detects physically inconsistent switch combinations.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF006: Tank Hysteresis Fill Controller with Contradiction Detection

## Background
Tank fill controller using low/high float probes with contradictory sensor fault protection.

## Functional Requirements
1. Inputs: `LowWet` (`TRUE` when level >= low probe), `HighWet` (`TRUE` when level >= high probe), `Inhibit` (`BOOL`).
2. `SensorFault := HighWet AND NOT LowWet` (physically impossible probe combination).
3. If `SensorFault = TRUE` or `Inhibit = TRUE` or `HighWet = TRUE`, force `Fill := FALSE`.
4. Else if `LowWet = FALSE`, set `Fill := TRUE`; otherwise retain previous `Fill`.

## Interface
- **Inputs:** `LowWet: BOOL`, `HighWet: BOOL`, `Inhibit: BOOL`
- **Outputs:** `Fill: BOOL`, `SensorFault: BOOL`

## Initial Values
- `Fill=false`, `SensorFault=false`

## Timing & Evaluation Conventions
Both outputs reflect post-evaluation state on every scan.

### Scenario

A refill tank avoids contactor chatter between low and high level switches and detects physically inconsistent switch combinations.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | LowWet | BOOL | Water reaches lower switch |
| INPUT | HighWet | BOOL | Water reaches upper switch |
| INPUT | Inhibit | BOOL | External fill inhibit |
| OUTPUT | Fill | BOOL | Inlet valve command |
| OUTPUT | SensorFault | BOOL | Inconsistent level switches |

### Initial conditions

```json
{
  "Fill": false,
  "SensorFault": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Inconsistent sensors or Inhibit stop filling
- High switch stops
- Low switch starts
- Middle level retains

### Explicit assumptions

- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `LowWet`: I[k].LowWet: sampled input (BOOL).
- `HighWet`: I[k].HighWet: sampled input (BOOL).
- `Inhibit`: I[k].Inhibit: sampled input (BOOL).
- `Fill`: O[k].Fill: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `SensorFault`: O[k].SensorFault: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `qFill`: {"kind": "previous_observed_output", "source": "O[k-1].Fill", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].Fill; never write into reference state."}
- `middle`: LowWet & !HighWet.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF006(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
fill初值FALSE；sensorFault=HighWet & !LowWet。sensorFault或Inhibit或HighWet时fillAfter=FALSE，否则!LowWet时TRUE，其余保持；实际Fill/SensorFault分别比较这两个期望值。
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.Fill=false, O_init.SensorFault=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Fill": false,
    "SensorFault": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF006",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF006",
          "state": {
            "fill": false
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF006'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Fill",
    "SensorFault"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "qFill": {
      "kind": "previous_observed_output",
      "source": "O[k-1].Fill",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].Fill; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "fill初值FALSE；sensorFault=HighWet & !LowWet。sensorFault或Inhibit或HighWet时fillAfter=FALSE，否则!LowWet时TRUE，其余保持；实际Fill/SensorFault分别比较这两个期望值。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(SensorFault <-> (HighWet & !LowWet))
```

Fault exactly identifies inconsistent switches.

**P2**

```text
G((SensorFault | Inhibit | HighWet) -> !Fill)
```

Inhibit, fault and full tank force shutoff.

**P3**

```text
G((!LowWet & !HighWet & !Inhibit) -> Fill)
```

A low tank starts filling.

**P4**

```text
G((middle & !Inhibit) -> (Fill <-> qFill))
```

The middle band retains the prior command.

**P5**

```text
G(first -> !qFill)
```

No retained filling command exists on reset.

**SELF006.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| hysteresis | Fill cycle across both switching thresholds | 5 |
| fault_inhibit | Invalid switch pair and inhibit recovery | 5 |
| SELF006.boundary_fault_recovery | SELF006.boundary_fault_recovery | 5 |
| SELF006.R22.tail_LowWet | 完成主流程后改变并保持 LowWet | 7 |
| SELF006.R22.tail_HighWet | 完成主流程后改变并保持 HighWet | 7 |
| SELF006.R22.tail_Inhibit | 完成主流程后改变并保持 Inhibit | 7 |
| SELF006.R22.priority_recovery | 动作中停止／矛盾信号与恢复 | 3 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF007 Duty standby alternation with healthy pump fallback

Origin: self_built. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 7,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "Two sump pumps share wear by alternating the preferred pump only after a demand episode that actually delivered pumping.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF007: Duty/Standby Dual-Pump Alternation with Fault Fallback

## Background
Dual-pump (`PumpA`/`PumpB`) duty/standby alternator balancing wear across served demand episodes.

## Functional Requirements
1. Inputs: `Demand`, `FaultA`, `FaultB` (`BOOL`). Initial preference `LeadA := TRUE`, episode memory `served := FALSE`, `previous_demand := FALSE`.
2. When `Demand = FALSE`: both `PumpA := FALSE`, `PumpB := FALSE`; if `previous_demand = TRUE AND served = TRUE`, toggle `LeadA := NOT LeadA`; reset `served := FALSE`.
3. When `Demand = TRUE`: select the preferred lead pump (`PumpA` if `LeadA`, else `PumpB`) if healthy; otherwise fall back to the healthy standby pump; if both fault, run neither. If either pump runs on this scan, mark `served := TRUE`.
4. `LeadA` reflects the post-transition preference; `previous_demand` tracks `I[k].Demand` on every scan.

## Interface
- **Inputs:** `Demand: BOOL`, `FaultA: BOOL`, `FaultB: BOOL`
- **Outputs:** `PumpA: BOOL`, `PumpB: BOOL`, `LeadA: BOOL`

## Initial Values
- `LeadA=true`, `previous_demand=false`, `episode_served=false`, `PumpA=false`, `PumpB=false`

## Timing & Evaluation Conventions
If `Demand` stays FALSE for multiple scans, alternation occurs at most once on the falling edge following a served demand episode.

### Scenario

Two sump pumps share wear by alternating the preferred pump only after a demand episode that actually delivered pumping.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Demand | BOOL | Sump pumping demand |
| INPUT | FaultA | BOOL | Pump A unavailable |
| INPUT | FaultB | BOOL | Pump B unavailable |
| OUTPUT | PumpA | BOOL | Pump A run command |
| OUTPUT | PumpB | BOOL | Pump B run command |
| OUTPUT | LeadA | BOOL | TRUE selects A as preferred pump |

### Initial conditions

```json
{
  "LeadA": true,
  "previous_demand": false,
  "episode_served": false,
  "PumpA": false,
  "PumpB": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Faulted pumps never run
- No demand forces both off
- Prefer selected lead, then healthy fallback

### Explicit assumptions

- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `Demand`: I[k].Demand: sampled input (BOOL).
- `FaultA`: I[k].FaultA: sampled input (BOOL).
- `FaultB`: I[k].FaultB: sampled input (BOOL).
- `PumpA`: O[k].PumpA: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `PumpB`: O[k].PumpB: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `LeadA`: O[k].LeadA: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `qLeadA`: {"kind": "previous_observed_output", "source": "O[k-1].LeadA", "initial": true, "update": "After comparing scan k, store ACTUAL O[k].LeadA; never write into reference state."}
- `completedServed`: Spre.reference.state.demand AND NOT I[k].Demand AND Spre.reference.state.served
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF007(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
leadA=TRUE/served=FALSE/previousDemand=FALSE初值。Demand假时双泵关，仅previousDemand & served时轮换leadA，然后清served；Demand真时由leadA选择无故障主泵，主故障则无故障备用，双故障均关；served累计本需求段任一泵运行。previousDemand每拍=Demand，LeadA比较转移后偏好。
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.PumpA=false, O_init.PumpB=false, O_init.LeadA=true.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "LeadA": true,
    "PumpA": false,
    "PumpB": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF007",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF007",
          "state": {
            "lead_a": true,
            "served": false,
            "demand": false
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF007'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "LeadA",
    "PumpA",
    "PumpB"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "qLeadA": {
      "kind": "previous_observed_output",
      "source": "O[k-1].LeadA",
      "initial": true,
      "update": "After comparing scan k, store ACTUAL O[k].LeadA; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "leadA=TRUE/served=FALSE/previousDemand=FALSE初值。Demand假时双泵关，仅previousDemand & served时轮换leadA，然后清served；Demand真时由leadA选择无故障主泵，主故障则无故障备用，双故障均关；served累计本需求段任一泵运行。previousDemand每拍=Demand，LeadA比较转移后偏好。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(!(PumpA & PumpB))
```

At most one pump runs.

**P2**

```text
G((!Demand | FaultA) -> !PumpA)
```

A cannot run without demand or with its fault.

**P3**

```text
G((!Demand | FaultB) -> !PumpB)
```

B cannot run without demand or with its fault.

**P4**

```text
G((Demand & LeadA & !FaultA) -> PumpA)
```

A is selected when it is the healthy lead.

**P5**

```text
G((Demand & !LeadA & !FaultB) -> PumpB)
```

B is selected when it is the healthy lead.

**P6**

```text
G(completedServed -> (LeadA <-> !qLeadA))
```

Toggle once on a served demand's falling edge.

**P7**

```text
G(!completedServed -> (LeadA <-> qLeadA))
```

Unserved episodes and held demand preserve preference.

**SELF007.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

**SELF007.V2.1**

```text
G((Demand & FaultA & !FaultB) -> PumpB)
```

Explicit correction of a demonstrated omission.

**SELF007.V2.2**

```text
G((Demand & FaultB & !FaultA) -> PumpA)
```

Explicit correction of a demonstrated omission.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| alternate | Served episodes alternate preference | 7 |
| fallback | Fault fallback, unserved episode and recovery | 5 |
| V2_omission_regression | Reject the concrete wrong behavior documented in the 2026-11-06 specification review. | 3 |
| SELF007.boundary_alternation_edges | SELF007.boundary_alternation_edges | 6 |
| SELF007.R22.served_loss | 本轮曾经服务，随后双故障，需求结束仍应轮换主泵 | 3 |
| SELF007.R22.normal_changes | A/B双向回退、曾服务后双故障仍轮换 | 9 |
| SELF007.R22.tail_Demand | 完成主流程后改变并保持 Demand | 9 |
| SELF007.R22.tail_FaultA | 完成主流程后改变并保持 FaultA | 9 |
| SELF007.R22.tail_FaultB | 完成主流程后改变并保持 FaultB | 9 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF008 Consecutive scan qualification with an immediate trip

Origin: self_built. Difficulty: easy.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 8,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "A cyclic quality check accepts a request only after a configurable number of consecutive healthy invocations.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF008: Preset-Qualified Delay Counter

## Background
Sequential delay counter validating integer `Preset` in `1..5` across continuous `Request` scans.

## Functional Requirements
1. Inputs: `Request`, `Trip` (`BOOL`), `Preset` (`INT`, valid domain `1..5`).
2. If `Request = FALSE`, `Trip = TRUE`, or `Preset` is outside `1..5`, reset `Count := 0` and set `Ready := FALSE`.
3. Otherwise increment `Count := min(Count + 1, Preset)` and set `Ready := (Count >= Preset)`.

## Interface
- **Inputs:** `Request: BOOL`, `Trip: BOOL`, `Preset: USINT`
- **Outputs:** `Ready: BOOL`, `Count: USINT`

## Initial Values
- `Count=0`, `Ready=false`

## Timing & Evaluation Conventions
`Preset` must be an integer (`bool` rejected); each qualifying scan counts as `1`.

### Scenario

A cyclic quality check accepts a request only after a configurable number of consecutive healthy invocations.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Request | BOOL | Raw qualification request |
| INPUT | Trip | BOOL | Immediate inhibit |
| INPUT | Preset | USINT | Required consecutive scans, valid 1 through 5 |
| OUTPUT | Ready | BOOL | Qualified request |
| OUTPUT | Count | USINT | Saturated consecutive scan count |

### Initial conditions

```json
{
  "Count": 0,
  "Ready": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Trip, missing request and invalid Preset clear progress

### Explicit assumptions

- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `Request`: I[k].Request: sampled input (BOOL).
- `Trip`: I[k].Trip: sampled input (BOOL).
- `Preset`: I[k].Preset: sampled input (USINT).
- `Ready`: O[k].Ready: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Count`: O[k].Count: independently observed post-scan candidate value (USINT); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `invalid`: Preset < 1 or Preset > 5.
- `qualified`: Count >= Preset and Preset is valid.
- `qCount`: {"kind": "previous_observed_output", "source": "O[k-1].Count", "initial": 0, "update": "After comparing scan k, store ACTUAL O[k].Count; never write into reference state."}
- `nextCount`: min(qCount+1, Preset) as an integer expression.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF008(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
count初值0；Preset有效域1..5。!Request或Trip或非法Preset时countAfter=0，否则min(countBefore+1,Preset)；Count比较该值，Ready=有效且countAfter>=Preset。
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.Ready=false, O_init.Count=0.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Count": 0,
    "Ready": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF008",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF008",
          "state": {
            "count": 0
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF008'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Count",
    "Ready"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "qCount": {
      "kind": "previous_observed_output",
      "source": "O[k-1].Count",
      "initial": 0,
      "update": "After comparing scan k, store ACTUAL O[k].Count; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "count初值0；Preset有效域1..5。!Request或Trip或非法Preset时countAfter=0，否则min(countBefore+1,Preset)；Count比较该值，Ready=有效且countAfter>=Preset。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G((Trip | !Request | invalid) -> (!Ready & (Count = 0)))
```

Every interruption clears qualification immediately.

**P2**

```text
G((Request & !Trip & !invalid) -> (Count = nextCount))
```

Healthy scans increment and saturate precisely.

**P3**

```text
G(Ready <-> qualified)
```

The indication agrees with the post-scan count.

**P4**

```text
G(!invalid -> ((Count >= 0) & (Count <= Preset)))
```

The counter stays within bounds.

**P5**

```text
(G(Request & !Trip & !invalid)) -> F Ready
```

A perpetually valid request qualifies within at most five scans, even if valid Preset varies.

**SELF008.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| delay | Three scans qualify, hold saturates, trip clears | 6 |
| bounds | Invalid presets and immediate reduced threshold | 5 |
| SELF008.boundary_preset_resize | SELF008.boundary_preset_resize | 7 |
| SELF008.R22.normal_changes | Ready后提高阈值、降低阈值与非法清零 | 5 |
| SELF008.R22.tail_Request | 完成主流程后改变并保持 Request | 8 |
| SELF008.R22.tail_Trip | 完成主流程后改变并保持 Trip | 8 |
| SELF008.boundary_preset_hold_and_zero | Invalid presets (0 and 6) force zero clear, valid recovery counts to Preset=2, and live Preset reduction saturates Count while staying Ready. | 6 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF009 Rising edge batch counter with reset sampling

Origin: self_built. Difficulty: easy.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 9,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "A packaging batch counts individual sensor edges and prevents a held sensor during reset from being counted again.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF009: Rising-Edge Batch Part Counter

## Background
Rising-edge batch counter validating integer `Target` in `1..20`.

## Functional Requirements
1. Inputs: `PartPulse`, `Reset` (`BOOL`), `Target` (`INT`, valid domain `1..20`). Edge memory `previous_pulse` initializes `FALSE` and updates to `I[k].PartPulse` on EVERY scan (including `Error` or `Reset`).
2. If `Target` is outside `1..20`, set `Error := TRUE`, `Count := 0`, `Complete := FALSE`.
3. Else `Error := FALSE`: if `Reset = TRUE`, set `Count := 0` and `Complete := FALSE`; otherwise increment `Count := min(Count + 1, Target)` on `PartPulse` rising edge (`PartPulse AND NOT previous_pulse`) and set `Complete := (Count >= Target)`.

## Interface
- **Inputs:** `PartPulse: BOOL`, `Reset: BOOL`, `Target: USINT`
- **Outputs:** `Count: USINT`, `Complete: BOOL`, `Error: BOOL`

## Initial Values
- `Count=0`, `previous_pulse=false`, `Complete=false`, `Error=false`

## Timing & Evaluation Conventions
`Target` must be an integer (`bool` rejected). Shrinking `Target` clamps `Count` via `min(..., Target)` and re-evaluates `Complete`.

### Scenario

A packaging batch counts individual sensor edges and prevents a held sensor during reset from being counted again.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | PartPulse | BOOL | Part detection level |
| INPUT | Reset | BOOL | Reset batch |
| INPUT | Target | USINT | Batch target, valid 1 through 20 |
| OUTPUT | Count | USINT | Saturated part count |
| OUTPUT | Complete | BOOL | Target reached |
| OUTPUT | Error | BOOL | Invalid target |

### Initial conditions

```json
{
  "Count": 0,
  "previous_pulse": false,
  "Complete": false,
  "Error": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Invalid Target and Reset override counting
- Update edge memory on every scan

### Explicit assumptions

- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `PartPulse`: I[k].PartPulse: sampled input (BOOL).
- `Reset`: I[k].Reset: sampled input (BOOL).
- `Target`: I[k].Target: sampled input (USINT).
- `Count`: O[k].Count: independently observed post-scan candidate value (USINT); never defined as expected output.
- `Complete`: O[k].Complete: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Error`: O[k].Error: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `invalid`: Target < 1 or Target > 20.
- `rise`: PartPulse & !qPulse.
- `qPulse`: {"kind": "previous_sampled_input", "source": "I[k-1].PartPulse", "initial": false, "update": "After EVERY scan k, including invalid/reset/stop, store I[k].PartPulse"}
- `qCount`: {"kind": "previous_observed_output", "source": "O[k-1].Count", "initial": 0, "update": "After comparing scan k, store ACTUAL O[k].Count; never write into reference state."}
- `countAfterEdge`: min(qCount + (1 if rise else 0), Target).
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF009(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
count=0/pulsePrev=FALSE初值。invalid=Target不在1..20；invalid或Reset时countAfter=0，否则min(countBefore+int(PartPulse & !pulsePrev),Target)。Complete=!invalid & !Reset & countAfter>=Target，Error=invalid；pulsePrev每拍更新为PartPulse。
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.Count=0, O_init.Complete=false, O_init.Error=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Count": 0,
    "Complete": false,
    "Error": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF009",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF009",
          "state": {
            "count": 0,
            "pulse": false
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF009'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Complete",
    "Count",
    "Error"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "qCount": {
      "kind": "previous_observed_output",
      "source": "O[k-1].Count",
      "initial": 0,
      "update": "After comparing scan k, store ACTUAL O[k].Count; never write into reference state."
    },
    "qPulse": {
      "kind": "previous_sampled_input",
      "source": "I[k-1].PartPulse",
      "initial": false,
      "update": "After EVERY scan k, including invalid/reset/stop, store I[k].PartPulse"
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "count=0/pulsePrev=FALSE初值。invalid=Target不在1..20；invalid或Reset时countAfter=0，否则min(countBefore+int(PartPulse & !pulsePrev),Target)。Complete=!invalid & !Reset & countAfter>=Target，Error=invalid；pulsePrev每拍更新为PartPulse。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(Error <-> invalid)
```

Target validation is exact.

**P2**

```text
G((Reset | invalid) -> ((Count = 0) & !Complete))
```

Reset or invalid target clears the batch.

**P3**

```text
G((!Reset & !invalid) -> (Count = countAfterEdge))
```

Only rising edges add an item, with saturation.

**P4**

```text
G((!Reset & !invalid) -> (Complete <-> (Count >= Target)))
```

Complete reports the post-scan count.

**P5**

```text
G(X(qPulse) <-> PartPulse)
```

Edge memory samples the pulse even during reset.

**SELF009.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| edges | Held pulses count once and target saturates | 7 |
| reset_edge | Reset while pulse is high suppresses phantom count | 6 |
| SELF009.boundary_target_and_error | SELF009.boundary_target_and_error | 9 |
| SELF009.R22.target_latch | 计数完成后提高Target，Complete应重新变假 | 6 |
| SELF009.R22.normal_changes | 动态目标、上限20及非法后高脉冲恢复 | 10 |
| SELF009.R22.tail_PartPulse | 完成主流程后改变并保持 PartPulse | 9 |
| SELF009.R22.tail_Reset | 完成主流程后改变并保持 Reset | 9 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF010 Latched alarm with acknowledgment and reannunciation

Origin: self_built. Difficulty: medium.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 10,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "A panel alarm retains the event after a fault clears, silences the horn after acknowledgment, and sounds again for a new fault edge.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF010: Latching Alarm Annunciator with Acknowledge and Horn

## Background
ISA-style latching alarm annunciator with acknowledgment and horn silence logic.

## Functional Requirements
1. Inputs: `Fault`, `Ack`, `Reset` (`BOOL`). Edge memory `previous_fault` initializes `FALSE` and updates on EVERY scan.
2. If `Reset = TRUE AND Fault = FALSE`, clear `Alarm := FALSE` and `Acknowledged := FALSE`.
3. Else if `Fault = TRUE`: set `Alarm := TRUE`; on a new `Fault` rising edge clear `Acknowledged := FALSE`, else if `Ack = TRUE` set `Acknowledged := TRUE`.
4. Else (`Fault = FALSE` and no valid reset): retain `Alarm`, and if `Alarm = TRUE AND Ack = TRUE` set `Acknowledged := TRUE`.
5. Set `Horn := Alarm AND NOT Acknowledged` on every scan.

## Interface
- **Inputs:** `Fault: BOOL`, `Ack: BOOL`, `Reset: BOOL`
- **Outputs:** `Alarm: BOOL`, `Acknowledged: BOOL`, `Horn: BOOL`

## Initial Values
- `Alarm=false`, `Acknowledged=false`, `previous_fault=false`, `Horn=false`

## Timing & Evaluation Conventions
If `Reset = TRUE` while `Fault = TRUE`, reset is ignored and the alarm remains active.

### Scenario

A panel alarm retains the event after a fault clears, silences the horn after acknowledgment, and sounds again for a new fault edge.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Fault | BOOL | Current fault condition |
| INPUT | Ack | BOOL | Acknowledge horn |
| INPUT | Reset | BOOL | Clear a removed fault |
| OUTPUT | Alarm | BOOL | Latched visible alarm |
| OUTPUT | Acknowledged | BOOL | Alarm acknowledged |
| OUTPUT | Horn | BOOL | Unacknowledged alarm horn |

### Initial conditions

```json
{
  "Alarm": false,
  "Acknowledged": false,
  "previous_fault": false,
  "Horn": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- New fault edge reannunciates before Ack
- Reset only clears when Fault is absent
- Reset then precedes Ack

### Explicit assumptions

- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `Fault`: I[k].Fault: sampled input (BOOL).
- `Ack`: I[k].Ack: sampled input (BOOL).
- `Reset`: I[k].Reset: sampled input (BOOL).
- `Alarm`: O[k].Alarm: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Acknowledged`: O[k].Acknowledged: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Horn`: O[k].Horn: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `rise`: Fault & !qFault.
- `qFault`: {"kind": "previous_sampled_input", "source": "I[k-1].Fault", "initial": false, "update": "After EVERY scan k, including invalid/reset/stop, store I[k].Fault"}
- `qAlarm`: {"kind": "previous_observed_output", "source": "O[k-1].Alarm", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].Alarm; never write into reference state."}
- `qAck`: {"kind": "previous_observed_output", "source": "O[k-1].Acknowledged", "initial": false, "update": "After comparing scan k, store ACTUAL O[k].Acknowledged; never write into reference state."}
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF010(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
latched/ack/previousFault初值FALSE。Reset & !Fault时清latched/ack；否则Fault时置latched，若Fault新沿清ack、否则Ack置ack；否则旧latched且Ack置ack，其余保持。Alarm=latchedAfter，Acknowledged=ackAfter，Horn=latchedAfter & !ackAfter。previousFault每拍=Fault。
- `init`: At the separate pre-invocation initial observation before scan k=0: O_init.Alarm=false, O_init.Acknowledged=false, O_init.Horn=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Alarm": false,
    "Acknowledged": false,
    "Horn": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF010",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF010",
          "state": {
            "latched": false,
            "ack": false,
            "fault": false
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF010'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Acknowledged",
    "Alarm",
    "Horn"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "qAlarm": {
      "kind": "previous_observed_output",
      "source": "O[k-1].Alarm",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].Alarm; never write into reference state."
    },
    "qAck": {
      "kind": "previous_observed_output",
      "source": "O[k-1].Acknowledged",
      "initial": false,
      "update": "After comparing scan k, store ACTUAL O[k].Acknowledged; never write into reference state."
    },
    "qFault": {
      "kind": "previous_sampled_input",
      "source": "I[k-1].Fault",
      "initial": false,
      "update": "After EVERY scan k, including invalid/reset/stop, store I[k].Fault"
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O."
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "latched/ack/previousFault初值FALSE。Reset & !Fault时清latched/ack；否则Fault时置latched，若Fault新沿清ack、否则Ack置ack；否则旧latched且Ack置ack，其余保持。Alarm=latchedAfter，Acknowledged=ackAfter，Horn=latchedAfter & !ackAfter。previousFault每拍=Fault。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(Horn <-> (Alarm & !Acknowledged))
```

Horn follows the latched acknowledgment state.

**P2**

```text
G(Fault -> Alarm)
```

A present fault cannot be reset away.

**P3**

```text
G(rise -> (Alarm & !Acknowledged & Horn))
```

Every new event annunciates despite simultaneous Ack.

**P4**

```text
G((Reset & !Fault) -> (!Alarm & !Acknowledged & !Horn))
```

Reset clears a removed fault.

**P5**

```text
G((!Fault & !Reset & qAlarm) -> Alarm)
```

Fault disappearance does not clear the visible alarm.

**P6**

```text
G((!rise & !(Reset & !Fault) & Ack & qAlarm) -> Acknowledged)
```

Acknowledgment silences a retained event.

**P7**

```text
G(!Fault & !qAlarm -> (!Alarm & !Acknowledged & !Horn))
```

Forbids spontaneous alarm or pre-acknowledgment on idle scans.

**P8**

```text
G((qAlarm & !(Reset & !Fault) & !rise & !Ack) -> (Acknowledged <-> qAck))
```

Preserves acknowledgment retention without requiring CompleteBehaviorV2.

**SELF010.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| annunciate | Acknowledge, fault clear and new event | 6 |
| reset_priority | Present fault blocks reset; removed fault reset wins | 3 |
| V2_omission_regression | Reject the concrete wrong behavior documented in the 2026-11-06 specification review. | 3 |
| SELF010.boundary_ack_and_horn | SELF010.boundary_ack_and_horn | 7 |
| SELF010.R22.normal_changes | 故障消失后首次确认、复位与空闲保持 | 7 |
| SELF010.R22.tail_Fault | 完成主流程后改变并保持 Fault | 8 |
| SELF010.R22.tail_Ack | 完成主流程后改变并保持 Ack | 8 |
| SELF010.R22.tail_Reset | 完成主流程后改变并保持 Reset | 8 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF011 Single cycle actuator handshakes with one transition per scan

Origin: self_built. Difficulty: hard.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 11,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "An assembly fixture coordinates an extending slide and a clamp using explicit completion handshakes, allowing deterministic commissioning tests.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF011: Sequential Gripper-Transfer Handshake Cycle

## Background
Five-stage pick/clamp/release/retract handshake sequence (`IDLE`, `EXTEND`, `CLAMP`, `RELEASE`, `RETRACT`, `DONE`).

## Functional Requirements
1. Inputs: `Start`, `Stop`, `Reset`, `ExtendDone`, `ClampDone`, `ReleaseDone`, `RetractDone` (`BOOL`).
2. If `Stop = TRUE` or `Reset = TRUE`, return immediately to `IDLE` and clear all outputs.
3. Otherwise from `IDLE`: enter `EXTEND` iff `Start = TRUE AND RetractDone = TRUE`.
4. Advance one step per scan on matching feedback: `EXTEND & ExtendDone -> CLAMP`; `CLAMP & ClampDone -> RELEASE`; `RELEASE & ReleaseDone -> RETRACT`; `RETRACT & RetractDone -> DONE`; `DONE` holds until `Stop`/`Reset`.
5. Outputs match post-transition phase: `Extend`/`Clamp`/`Release`/`Retract` mirror their named state, `Busy` holds in active steps `1..4`, `Done` holds in `DONE`.

## Interface
- **Inputs:** `Start: BOOL`, `Stop: BOOL`, `Reset: BOOL`, `ExtendDone: BOOL`, `ClampDone: BOOL`, `ReleaseDone: BOOL`, `RetractDone: BOOL`
- **Outputs:** `Extend: BOOL`, `Clamp: BOOL`, `Release: BOOL`, `Retract: BOOL`, `Busy: BOOL`, `Done: BOOL`

## Initial Values
- `state="IDLE"`, `all_commands=false`, `Extend=false`, `Clamp=false`, `Release=false`, `Retract=false`, `Busy=false`, `Done=false`

## Timing & Evaluation Conventions
At most one transition occurs per scan; all inputs are level-sensitive.

### Scenario

An assembly fixture coordinates an extending slide and a clamp using explicit completion handshakes, allowing deterministic commissioning tests.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Start | BOOL | Begin one fixture cycle |
| INPUT | Stop | BOOL | Abort fixture cycle |
| INPUT | Reset | BOOL | Clear cycle state |
| INPUT | ExtendDone | BOOL | Extension completion handshake |
| INPUT | ClampDone | BOOL | Clamp completion handshake |
| INPUT | ReleaseDone | BOOL | Release completion handshake |
| INPUT | RetractDone | BOOL | Retracted home handshake |
| OUTPUT | Extend | BOOL | Slide extend command |
| OUTPUT | Clamp | BOOL | Clamp command |
| OUTPUT | Release | BOOL | Release command |
| OUTPUT | Retract | BOOL | Slide retract command |
| OUTPUT | Busy | BOOL | An action state is active |
| OUTPUT | Done | BOOL | Cycle completed |

### Initial conditions

```json
{
  "state": "IDLE",
  "all_commands": false,
  "Extend": false,
  "Clamp": false,
  "Release": false,
  "Retract": false,
  "Busy": false,
  "Done": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Stop or Reset overrides all transitions
- At most one state transition per invocation

### Explicit assumptions

- Completion inputs are handshake states; no mechanical safety certification is implied.
- No timeout is included; an absent handshake intentionally stalls the current action.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `Start`: I[k].Start: sampled input (BOOL).
- `Stop`: I[k].Stop: sampled input (BOOL).
- `Reset`: I[k].Reset: sampled input (BOOL).
- `ExtendDone`: I[k].ExtendDone: sampled input (BOOL).
- `ClampDone`: I[k].ClampDone: sampled input (BOOL).
- `ReleaseDone`: I[k].ReleaseDone: sampled input (BOOL).
- `RetractDone`: I[k].RetractDone: sampled input (BOOL).
- `Extend`: O[k].Extend: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Clamp`: O[k].Clamp: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Release`: O[k].Release: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Retract`: O[k].Retract: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Busy`: O[k].Busy: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Done`: O[k].Done: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `qIdle`: Spre.reference.state.mode=0
- `qExtend`: Spre.reference.state.mode=1
- `qClamp`: Spre.reference.state.mode=2
- `qRelease`: Spre.reference.state.mode=3
- `qRetract`: Spre.reference.state.mode=4
- `qDone`: Spre.reference.state.mode=5
- `normal`: !Stop & !Reset.
- `oneAction`: int(O[k].Extend)+int(O[k].Clamp)+int(O[k].Release)+int(O[k].Retract)<=1
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF011(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
mode初值IDLE。Stop或Reset优先回IDLE；IDLE且Start & RetractDone进EXTEND；EXTEND/CLAMP/RELEASE/RETRACT仅各自匹配完成信号推进一阶；DONE保持。四动作输出分别等价于转移后对应阶段，Busy等价于阶段1..4，Done等价于阶段5。
- `init`: At the separate pre-invocation initial observation before scan k=0: Spre.mode=IDLE, O_init.Extend=false, O_init.Clamp=false, O_init.Release=false, O_init.Retract=false, O_init.Busy=false, O_init.Done=false.

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Extend": false,
    "Clamp": false,
    "Release": false,
    "Retract": false,
    "Busy": false,
    "Done": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF011",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF011",
          "state": {
            "mode": 0
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF011'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Busy",
    "Clamp",
    "Done",
    "Extend",
    "Release",
    "Retract"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {},
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "phase": {
      "pre": "Spre.reference.state.mode",
      "post": "Spost.reference.state.mode",
      "enum": {
        "0": "IDLE",
        "1": "EXTEND",
        "2": "CLAMP",
        "3": "RELEASE",
        "4": "RETRACT",
        "5": "DONE"
      },
      "initial": 0
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "Completion inputs are handshake states; no mechanical safety certification is implied.",
    "No timeout is included; an absent handshake intentionally stalls the current action.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "mode初值IDLE。Stop或Reset优先回IDLE；IDLE且Start & RetractDone进EXTEND；EXTEND/CLAMP/RELEASE/RETRACT仅各自匹配完成信号推进一阶；DONE保持。四动作输出分别等价于转移后对应阶段，Busy等价于阶段1..4，Done等价于阶段5。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(oneAction)
```

Action commands never overlap.

**P2**

```text
G((Stop | Reset) -> (!Busy & !Done & !Extend & !Clamp & !Release & !Retract))
```

Abort clears every command immediately.

**P3**

```text
G((normal & qIdle & Start & RetractDone) -> Extend)
```

Home-qualified Start enters only the first action.

**P4**

```text
G((normal & qExtend & ExtendDone) -> Clamp)
```

Extension completion enters clamp.

**P5**

```text
G((normal & qClamp & ClampDone) -> Release)
```

Clamp completion enters release.

**P6**

```text
G((normal & qRelease & ReleaseDone) -> Retract)
```

Release completion enters retract.

**P7**

```text
G((normal & qRetract & RetractDone) -> Done)
```

Home arrival completes the cycle.

**P8**

```text
G((normal & qDone) -> Done)
```

A completed cycle cannot restart without an explicit clear.

**P9**

```text
G((normal & qExtend & !ExtendDone) -> Extend)
```

The fixture waits for an extension handshake rather than assuming completion.

**P10**

```text
G((Busy <-> (Extend | Clamp | Release | Retract)) & (!(Busy & Done)))
```

Previously Busy had no positive constraint during active stages.

**P11**

```text
G(((normal & qIdle & !(Start & RetractDone)) -> (!Busy & !Done)) & ((normal & qClamp & !ClampDone) -> Clamp) & ((normal & qRelease & !ReleaseDone) -> Release) & ((normal & qRetract & !RetractDone) -> Retract))
```

Completes stage-hold symmetry alongside existing P9 (EXTEND hold).

**SELF011.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| handshake | Normal cycle and completion retention | 9 |
| single_transition | All handshakes cannot skip states; Stop aborts | 5 |
| SELF011.boundary_all_waits_and_recycle | SELF011.boundary_all_waits_and_recycle | 10 |
| SELF011.R22.clamp_hold | 夹紧阶段没有完成反馈时应保持动作 | 5 |
| SELF011.R22.all_waits | 四动作逐阶段等待、完成保持与复位后第二轮 | 42 |
| SELF011.R22.tail_Start | 完成主流程后改变并保持 Start | 11 |
| SELF011.R22.tail_Stop | 完成主流程后改变并保持 Stop | 11 |
| SELF011.R22.tail_Reset | 完成主流程后改变并保持 Reset | 11 |
| SELF011.R22.tail_ExtendDone | 完成主流程后改变并保持 ExtendDone | 11 |
| SELF011.R22.tail_ClampDone | 完成主流程后改变并保持 ClampDone | 11 |
| SELF011.R22.tail_ReleaseDone | 完成主流程后改变并保持 ReleaseDone | 11 |
| SELF011.R22.tail_RetractDone | 完成主流程后改变并保持 RetractDone | 11 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.

## SELF012 Bounded automatic fault retries with a recovery dwell

Origin: self_built. Difficulty: hard.

### Source and adaptation

```json
{
  "source_type": "independent_synthesis",
  "source_file": "scripts/build_self_dataset.py",
  "source_index": 12,
  "adaptation": "Independently specified for this project; no public task was copied. The coding assistant chose the state variables, priority order and fixed scan traces, then reviewed the traces against a separate Python transition implementation.",
  "rationale": "A laboratory feeder allows two automatic retries after a transient process fault and locks out a repeatedly failing actuator.",
  "review": "Assistant consistency review of initialization, simultaneous commands, retained state and recovery boundaries; independent Python oracle checked against manual expected traces. Not an industrial safety certification or external expert review."
}
```

### Natural language source

# SELF012: Fault-Tolerant Retry and Lockout Controller

## Background
Fault-tolerant motor controller permitting up to 2 automatic restarts after a 2-scan fault-free dwell.

## Functional Requirements
1. Inputs: `Start`, `Stop`, `Fault`, `Reset` (`BOOL`). Internal state: `mode` (`IDLE`/`RUNNING`/`WAIT`/`LOCKED`), `Attempts` (`0..2`), `free_scans` (`0..2`).
2. Valid reset (`Reset = TRUE AND Fault = FALSE AND Start = FALSE`) clears `mode := IDLE`, `Attempts := 0`, `free_scans := 0`.
3. If already `LOCKED`, remain `LOCKED`. Else `Stop = TRUE` forces `mode := IDLE`, `free_scans := 0` while preserving `Attempts` across manual stop/restart.
4. In `RUNNING`: if `Fault = TRUE`, enter `LOCKED` when `Attempts >= 2`, else enter `WAIT` with `free_scans := 0`.
5. In `WAIT`: if `Fault = TRUE`, clear `free_scans := 0`; else increment `free_scans`, and when `free_scans >= 2`, increment `Attempts += 1`, clear `free_scans := 0`, and return to `RUNNING`.
6. In `IDLE`: `Start = TRUE AND Fault = FALSE` enters `RUNNING` (keeping `Attempts`). Outputs match post-transition `mode`: `Run <-> RUNNING`, `Locked <-> LOCKED`, plus `Attempts`.

## Interface
- **Inputs:** `Start: BOOL`, `Stop: BOOL`, `Fault: BOOL`, `Reset: BOOL`
- **Outputs:** `Run: BOOL`, `Locked: BOOL`, `Attempts: USINT`

## Initial Values
- `state="IDLE"`, `Attempts=0`, `recovery_free_scans=0`, `Run=false`, `Locked=false`

## Timing & Evaluation Conventions
Retries use scan-level fault-free dwell (`free_scans >= 2`); each scan executes one step.

### Scenario

A laboratory feeder allows two automatic retries after a transient process fault and locks out a repeatedly failing actuator.

### Normalized interface

| Direction | Name | Type | Description |
| --- | --- | --- | --- |
| INPUT | Start | BOOL | Operator start request |
| INPUT | Stop | BOOL | Abort without clearing retry count |
| INPUT | Fault | BOOL | Process fault |
| INPUT | Reset | BOOL | Clear retry history with Start released |
| OUTPUT | Run | BOOL | Feeder command |
| OUTPUT | Locked | BOOL | Retry exhaustion lockout |
| OUTPUT | Attempts | USINT | Automatic restarts issued, zero through two |

### Initial conditions

```json
{
  "state": "IDLE",
  "Attempts": 0,
  "recovery_free_scans": 0,
  "Run": false,
  "Locked": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Valid reset
- Latched lockout
- Stop
- Running fault
- Recovery dwell
- Idle start

### Explicit assumptions

- The fault is an educational process input, not a personnel safety function.
- Operator stop/start does not restore the automatic retry budget; only accepted Reset does.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.
- The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.

### Atomic propositions and monitor predicates

- `Start`: I[k].Start: sampled input (BOOL).
- `Stop`: I[k].Stop: sampled input (BOOL).
- `Fault`: I[k].Fault: sampled input (BOOL).
- `Reset`: I[k].Reset: sampled input (BOOL).
- `Run`: O[k].Run: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Locked`: O[k].Locked: independently observed post-scan candidate value (BOOL); never defined as expected output.
- `Attempts`: O[k].Attempts: independently observed post-scan candidate value (USINT); never defined as expected output.
- `first`: k=0; first invocation, not the pre-invocation observation
- `qLocked`: Spre.reference.state.mode=3
- `qRunning`: Spre.reference.state.mode=1
- `qWait`: Spre.reference.state.mode=2
- `qAttempts`: {"kind": "previous_observed_output", "source": "O[k-1].Attempts", "initial": 0, "update": "After comparing scan k, store ACTUAL O[k].Attempts; never write into reference state."}
- `validReset`: Reset & !Fault & !Start.
- `retryDue`: Spre.reference.state.mode=2 AND NOT I[k].Fault AND Spre.reference.state.free>=1
- `normal`: !validReset & !Stop.
- `CompleteBehaviorV2`: 令(Sref[k+1], E[k])=T_SELF012(Sref[k], deepCopy(I[k]), dt_ms[k])。T由normalized_specification.transition列出的固定Python源码和初始状态精确定义。CompleteBehaviorV2[k] 当且仅当所有constrained_observed_fields均存在于实际O[k]，且分别满足comparison关系。Sref只由采样输入推进，绝不由O或候选内部变量推进。
mode=IDLE/attempts=0/free=0初值。优先Reset & !Fault & !Start清全部；其次LOCKED保持；其次Stop回IDLE并清free但保留attempts；RUNNING且Fault转WAIT或已重试2次转LOCKED；WAIT中Fault清free否则加1，free>=2时attempts加1并回RUNNING、free=0；IDLE且Start & !Fault进RUNNING。输出Run/Locked取新mode，Attempts取新attempts。
- `init`: At the separate pre-invocation initial observation before scan k=0: Spre.mode=IDLE, O_init.Run=false, O_init.Locked=false, O_init.Attempts=0.
- `qIdle`: Spre.reference.state.mode=0
- `refAttempts`: Spre.reference.state.attempts

### LTL properties

**Normalization is not formal proof.** These are LTL clauses over typed scan predicates. Human rationality review is completed; candidate verification remains UNVERIFIED.

### Normalized state, observation and predicate definitions

```json
{
  "schema_version": 1,
  "status": "NORMALIZED_HUMAN_REVIEWED",
  "language": "LTL over typed scan predicates; finite conjunction is a binding-time macro, not native NuSMV syntax.",
  "candidate_formal_verification": "UNVERIFIED",
  "initial_observed": {
    "Attempts": 0,
    "Run": false,
    "Locked": false
  },
  "reference_state_initial": {
    "class": "ScanContract",
    "state": {
      "task_id": "SELF012",
      "array_contract": null,
      "process_contract": null,
      "timed_contract": null,
      "data_contract": null,
      "reference": {
        "class": "ReferenceController",
        "state": {
          "task_id": "SELF012",
          "state": {
            "mode": 0,
            "attempts": 0,
            "free": 0
          }
        }
      },
      "phase": 0,
      "previous_mode": null,
      "clock": 0,
      "first": true,
      "heat_start": null,
      "protection_start": null,
      "demand": false
    }
  },
  "transition": {
    "entrypoint": "plc_agent.normalized_spec.reference_step(task, reference, deepCopy(I[k]), dt_ms[k])",
    "reference_binding": "Persistent plc_agent.scan_contract.ScanContract('SELF012'); constructed once per independent case, current state is Sref[k].",
    "state_update": "Exactly once per scan; mutations of sampled IN_OUT copies are reference effects, not observations.",
    "module_sha256": {
      "scan_contract.py": "2ebdbeb0bacd3c6154e1add2fd358f1aadc9ac9c9322a9201798065154353f48",
      "array_contracts.py": "f541ffe0e28c56e84ad737b06aa8c8ee6180b1afda720b7c41cc8fccad2d8ecd",
      "data_contracts.py": "0792c46b303ce62a0a2180bcf4d7ebfe4838ccfaa18deb331780af1819377b3a",
      "timed_contracts.py": "4467a065061a3073051c271fe01aae03c9776b1c81ccb74fb85f972a2bf70e78",
      "process_contracts.py": "00fb1941d23e87f2daa82fadb16b7df4f3506cd912a85fede22b254a7dbb3ff9",
      "reference.py": "737a4c796e27f3d7d7865b86502cca4f875ed6613d9eb3a245d1815cbffaf1ed",
      "normalized_spec.py": "ab5917a7bd5820ea6c1ee18400fe8fbaf88dbb1d537cbfc32e0347c9ffdf4989"
    },
    "hash_encoding": "UTF-8 without BOM; all line endings normalized to LF before SHA256",
    "frozen_sources": "dataset/specifications/normalized_transition_v2"
  },
  "constrained_observed_fields": [
    "Attempts",
    "Locked",
    "Run"
  ],
  "unconstrained_representation_fields": [],
  "comparison": {
    "integer_boolean": "exact type and value; no tolerance",
    "float": "finite; abs error<=1e-5; dictionary/list shape and non-float values exact",
    "PUB008": "only successfully converted channels[j].outputValue: abs<=1e-5 OR rel<=2e-6; all preserved/config fields exact",
    "PUB017": "Successful deletion constrains recipeID=0; other fields of that deleted slot are unconstrained for the deletion scan. Subsequent no-write scans preserve the sampled actual representation. This observer history is separate from the logical reference database.",
    "TIME_LTIME": "exact integer nanoseconds after IEC literal parsing",
    "implementation": "plc_agent.normalized_spec.NormalizedScanMonitor.step with output_matches (pinned sources); observer histories never drive the independent logical reference"
  },
  "observation": {
    "I[k]": "deep-copied inputs immediately before invocation k",
    "O[k]": "actual outputs immediately after invocation k, supplied by independent execution backend",
    "Sref[k]": "independent reference state BEFORE k; unrelated to similarly named candidate variables",
    "initial": "fresh instance BEFORE invocation 0; never substituted by O[0]",
    "X": "next scan-sequence position; argument must be Boolean, not a numeric term",
    "time": "dt_ms is observed elapsed time; public timers use physical time, SELF Tick/count timers use logical scans"
  },
  "history_bindings": {
    "qAttempts": {
      "kind": "previous_observed_output",
      "source": "O[k-1].Attempts",
      "initial": 0,
      "update": "After comparing scan k, store ACTUAL O[k].Attempts; never write into reference state."
    }
  },
  "auxiliary_state_bindings": {
    "Spre": "Sref[k], before the invocation; initialized by reference_state_initial",
    "Spost": "Sref[k+1], after exactly one pinned transition on I[k]",
    "first": "k=0 (first invocation); distinct from the pre-invocation initial observation",
    "pre-output": "actual O[k-1] for OUTPUT (explicit history initial where declared); I[k] for caller-owned IN_OUT",
    "previous-input": "I[k-1] for k>=1; edge memory for BOOL requests initially FALSE and updated after EVERY invocation",
    "reference_warning": "Spre/Spost predicates are input-driven ghosts, not evidence that candidate internals match. Conclusions about the candidate must constrain actual O.",
    "phase": {
      "pre": "Spre.reference.state.mode",
      "post": "Spost.reference.state.mode",
      "enum": {
        "0": "IDLE",
        "1": "RUNNING",
        "2": "WAIT",
        "3": "LOCKED"
      },
      "initial": 0
    }
  },
  "finite_conjunctions": {},
  "reference_state_rule": "Initial state is the serialized constructor above; all fields update solely through the pinned transition. Ghost phase/history/queue are names for this state, not observed candidate state.",
  "primitives": {
    "bitwise": "DWORD AND/NOT and popcount operate on unsigned 32-bit values; complement is masked by 0xFFFFFFFF.",
    "time_literals": "IEC TIME/LTIME literals are exact integer durations in nanoseconds.",
    "observed_arrays": "All IN_OUT inputs are snapshots before invocation; outputs are independently acquired after invocation. Physical bounds map by ordinal, never share another array lower bound.",
    "boolean_next": "X takes a Boolean formula. Numeric history transport is bit-expanded for DWORD; Boolean histories use equivalence.",
    "time_progress": "Timed eventuality clauses explicitly require G(F(TimeTick)); TimeTick denotes crossing a new integer-ms boundary. Finite observations cannot establish this premise."
  },
  "assumptions": [
    "The fault is an educational process input, not a personnel safety function.",
    "Operator stop/start does not restore the automatic retry budget; only accepted Reset does.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values.",
    "The task interface, requirements, assumptions, and normalized LTL definitions (excluding reference-only ground truth) are supplied identically to both frameworks. Output names always denote observed candidate outputs, never precomputed expected values."
  ],
  "domain_policy": "Declared interface types and task assumptions apply. The pinned transition defines numeric/timing domains and rejects unsupported inputs. Reference exceptions are DOMAIN_OR_TOOL_ERROR, never candidate FAIL or PASS. Fairness/time-divergence assumptions concern infinite paths and are not proven by finite observations.",
  "limitations": [
    "No ST-to-model translation or infinite-trace proof is implemented here.",
    "Focused legacy LTL predicates still require backend lowering; normalization is not model-checker acceptance.",
    "Finite matching cannot establish liveness or validate runtime provenance."
  ],
  "rules_zh": "mode=IDLE/attempts=0/free=0初值。优先Reset & !Fault & !Start清全部；其次LOCKED保持；其次Stop回IDLE并清free但保留attempts；RUNNING且Fault转WAIT或已重试2次转LOCKED；WAIT中Fault清free否则加1，free>=2时attempts加1并回RUNNING、free=0；IDLE且Start & !Fault进RUNNING。输出Run/Locked取新mode，Attempts取新attempts。"
}
```

**P_init**

```text
init
```

Applies strictly to the fresh pre-invocation initial instance observation before scan k=0 (INITIAL_INSTANCE scope).

**P1**

```text
G(Fault -> !Run)
```

A present fault cannot command the feeder.

**P2**

```text
G((Attempts >= 0) & (Attempts <= 2))
```

Automatic restart count stays within the budget.

**P3**

```text
G(validReset -> (!Run & !Locked & (Attempts = 0)))
```

Accepted reset clears history and leaves the feeder stopped.

**P4**

```text
G((qLocked & !validReset) -> (Locked & !Run))
```

Lockout requires a safe explicit reset.

**P5**

```text
G((qRunning & Fault & normal & (refAttempts = 2)) -> Locked)
```

Lock out on Fault from RUNNING once reference attempts already reached 2 (uses Spre.attempts to stay immune to candidate undercounting).

**P6**

```text
G((retryDue & normal) -> (Run & (Attempts = refAttempts + 1)))
```

On fault-free retry dwell completion, restart Run and output Attempts = Spre.attempts + 1.

**P7**

```text
G((qWait & Fault & normal) -> !Run)
```

A fault during recovery clears progress and prevents restart.

**P8**

```text
G(((qIdle & normal & !(Start & !Fault)) -> (!Run & !Locked & Attempts=refAttempts)) & ((qIdle & normal & Start & !Fault) -> (Run & !Locked & Attempts=refAttempts)) & ((qRunning & !Fault & normal) -> (Run & !Locked & Attempts=refAttempts)))
```

Eliminates vacuous under-counting and missing IDLE/RUNNING forward constraints.

**P9**

```text
G(((normal & qWait & !retryDue) -> (!Run & !Locked & Attempts=refAttempts)) & ((!qLocked & !(qRunning & Fault & normal & refAttempts=2)) -> !Locked) & (!(Run & Locked)))
```

Completes SELF012 independent safety closure.

**SELF012.V2.COMPLETE**

```text
G(CompleteBehaviorV2)
```

Every constrained ACTUAL output satisfies the exact pinned input-driven reference transition and comparison policy. Finite observations can falsify this predicate; no completed unbounded proof is claimed.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| exhaustion | Two automatic retries then third fault locks | 11 |
| dwell_interrupt | Fault interrupts healthy dwell; Stop aborts wait | 9 |
| V2_omission_regression | Reject the concrete wrong behavior documented in the 2026-11-06 specification review. | 3 |
| SELF012.boundary_stop_preserve_and_reset | SELF012.boundary_stop_preserve_and_reset | 12 |
| SELF012.R22.normal_changes | 自动重试后Stop再Start保留次数、有效复位优先 | 7 |
| SELF012.R22.tail_Start | 完成主流程后改变并保持 Start | 13 |
| SELF012.R22.tail_Stop | 完成主流程后改变并保持 Stop | 13 |
| SELF012.R22.tail_Fault | 完成主流程后改变并保持 Fault | 13 |
| SELF012.R22.tail_Reset | 完成主流程后改变并保持 Reset | 13 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.
