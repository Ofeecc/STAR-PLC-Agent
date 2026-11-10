# Dataset source specifications and test catalog
This document is generated from the task JSON files. It records requirements, provenance, formal specifications and planned test expectations. It contains no actual CODESYS execution results.
Regenerate after a deliberate dataset revision with `python scripts/build_dataset_docs.py`, then prepare a new campaign when the frozen hash has changed.
| ID | Origin | Difficulty | Title | LTL properties | Cases | Scan observations |
| --- | --- | --- | --- | ---: | ---: | ---: |
| PUB001 | public | easy | Automated Filling Line Control | 10 | 2 | 16 |
| PUB002 | public | easy | Dual-Word Edge Detection | 6 | 2 | 12 |
| PUB003 | public | easy | Alarm Handling | 9 | 2 | 13 |
| PUB004 | public | easy | Jam Pump Debouncing and Runtime Maintenance | 7 | 3 | 20 |
| PUB005 | public | easy | Weld Gap Alarm and Startup Inhibition | 5 | 2 | 14 |
| PUB006 | public | easy | Aeration Blower Delayed Start | 5 | 2 | 15 |
| PUB007 | public | medium | Multi-Pump Switching Control System | 5 | 2 | 6 |
| PUB008 | public | medium | Analog Batch Processing | 8 | 3 | 4 |
| PUB009 | public | medium | Calculate Moving Average | 7 | 2 | 15 |
| PUB010 | public | medium | Temperature Logic Control | 8 | 3 | 18 |
| PUB011 | public | medium | Automated Production Line Control | 6 | 3 | 16 |
| PUB012 | public | medium | Slab Thickness Alarm and Fault History | 6 | 3 | 25 |
| PUB013 | public | medium | Office HVAC Multi-mode Energy-Saving Control | 6 | 2 | 15 |
| PUB014 | public | medium | IPv4 Parsing with Format and Range Checks | 3 | 2 | 19 |
| PUB015 | public | hard | Material Proportioning Process Control | 6 | 3 | 22 |
| PUB016 | public | hard | Flexible Processing Control | 6 | 3 | 18 |
| PUB017 | public | hard | Recipe Management System | 6 | 3 | 48 |
| PUB018 | public | hard | FIFO First-In-First-Out Queue | 5 | 3 | 34 |
| PUB019 | public | hard | Mechanical Arm Control | 9 | 5 | 45 |
| PUB020 | public | hard | Production Control | 9 | 7 | 59 |
| SELF001 | self_built | easy | Guarded motor with retained run command | 5 | 2 | 10 |
| SELF002 | self_built | medium | Reversing jog drive with a neutral scan | 6 | 2 | 10 |
| SELF003 | self_built | medium | Emergency stop reset with restart inhibition | 6 | 2 | 10 |
| SELF004 | self_built | medium | Pallet indexing with a latched jam fault | 7 | 2 | 11 |
| SELF005 | self_built | medium | Three phase signal with externally clocked durations | 7 | 2 | 12 |
| SELF006 | self_built | easy | Tank filling with hysteresis and sensor inconsistency | 5 | 2 | 10 |
| SELF007 | self_built | medium | Duty standby alternation with healthy pump fallback | 7 | 2 | 12 |
| SELF008 | self_built | easy | Consecutive scan qualification with an immediate trip | 5 | 2 | 11 |
| SELF009 | self_built | easy | Rising edge batch counter with reset sampling | 5 | 2 | 13 |
| SELF010 | self_built | medium | Latched alarm with acknowledgment and reannunciation | 6 | 2 | 9 |
| SELF011 | self_built | hard | Single cycle actuator handshakes with one transition per scan | 9 | 2 | 14 |
| SELF012 | self_built | hard | Bounded automatic fault retries with a recovery dwell | 7 | 2 | 20 |

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

### Atomic propositions and monitor predicates

- `phase`: Ghost pre-scan state 0 idle, 1 cleaning, 2 filling, 3 capping, 4 packing, 5 complete; phase is updated once per scan.
- `oneHotOutputs`: At most one of Pump_Motor, Filling_Valve, Capping_Machine, Packing_Machine, Completion_Light is TRUE.
- `init`: Before the first scan, phase=0 and all outputs FALSE.
- `all variable names`: The identically named sampled input or end-of-scan output in interface.

### LTL properties

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

Pickup confirmation rearms the line.

**P10** 

```text
G((phase=1 & G((phase=1) -> F(cleaningConfirmButton)) & G((phase=2) -> F(fillingConfirmButton)) & G((phase=3) -> F(cappingConfirmButton)) & G((phase=4) -> F(packingConfirmButton))) -> F(Completion_Light))
```

Conditional progress: from cleaning, if every active phase eventually receives its matching confirmation, completion eventually occurs.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Full bottle cycle and stable completion | 10 |
| T2 | Out-of-order confirmations cannot skip phases | 6 |

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

### Atomic propositions and monitor predicates

- `prev`: Ghost pre-scan previous DWORD; initialized to zero.
- `risingBits`: End-of-scan mask value & NOT prev, restricted to DWORD width.
- `fallingBits`: End-of-scan mask prev & NOT value, restricted to DWORD width.
- `popcount`: Number of set bits in the unsigned 32-bit argument.
- `other interface names`: Identically named sampled inputs or observed outputs.

### LTL properties

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
G(X(prev)=value)
```

The current value is the next scan history.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | No change, mixed edges, full width and bit 31 | 10 |
| T2 | First nonzero invocation is compared with initialized zero | 2 |

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

### Atomic propositions and monitor predicates

- `badRange`: loLevel >= hiLevel
- `badWindow`: hystWindow >= hiLevel-loLevel
- `valid`: !badRange & !badWindow & hystWindow>=0
- `hiPrev`: Pre-scan retained hiAlarm
- `loPrev`: Pre-scan retained loAlarm
- `sameAlarms`: hiAlarm=hiPrev & loAlarm=loPrev
- `interface names`: Identically named sampled input or observed output.

### LTL properties

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
G((valid & Value<hiLevel-hystWindow) -> !hiAlarm)
```

Below the strict release boundary, high alarm clears.

**P6** 

```text
G((valid & hiLevel-hystWindow<=Value & Value<=hiLevel) -> (hiAlarm=hiPrev))
```

The high hysteresis band retains history.

**P7** 

```text
G((valid & Value<loLevel) -> loAlarm)
```

A low excursion activates the low alarm.

**P8** 

```text
G((valid & Value>loLevel+hystWindow) -> !loAlarm)
```

Above the strict low release boundary, low alarm clears.

**P9** 

```text
G((valid & loLevel<=Value & Value<=loLevel+hystWindow) -> (loAlarm=loPrev))
```

The low hysteresis band retains history.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Strict high and low hysteresis boundaries | 9 |
| T2 | Configuration priority, output retention and recovery | 4 |

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

### Atomic propositions and monitor predicates

- `permit`: VISCOSITY_OK & PASTE_E_STOP_NC
- `qualified`: Continuous permitted raw TRUE duration >= DebounceTime, with first sampled TRUE at elapsed zero.
- `accPrev`: Pre-scan PUMP_RUNTIME_ACC as nonnegative LTIME.
- `accNext`: End-of-scan PUMP_RUNTIME_ACC.
- `interface names`: Identically named sampled input or end-of-scan output.

### LTL properties

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
G((G(permit) & DebounceTime>TIME#0ms) -> F(VFD_RUN))
```

A continuously permitted demand eventually starts under advancing time.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Qualification boundary, accumulation, stop retention and restart | 9 |
| T2 | E-stop clears incomplete debounce and completed permission | 7 |
| T3 | Long-duration maintenance arithmetic boundary | 4 |

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

### Atomic propositions and monitor predicates

- `startup`: Elapsed time since the first invocation is less than 5 seconds.
- `gapQualified`: Gap_Exceeded has remained TRUE with Weld_E_Stop_NC TRUE and !startup for at least DebounceTime, measured from first eligible invocation.
- `interface names`: Identically named sampled input or observed output.

### LTL properties

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
G((G(Weld_E_Stop_NC & Gap_Exceeded)) -> F(Operator_Alert))
```

Persistent gap eventually alarms after startup and debounce, assuming advancing time.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Initialization excludes gap timing and debounce starts at 5s | 6 |
| T2 | E-stop suppresses startup and normal alerts without restarting inhibition | 8 |

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

### Atomic propositions and monitor predicates

- `permit`: DO_LOW & AERATION_E_STOP_NC
- `delayDone`: Permissive has continuously remained true for >=5s after its first sampled TRUE.
- `runPrev`: Pre-scan retained BLOWER_RUN.
- `countPrev`: Pre-scan AERATION_BLOWER_CYCLE_COUNT.
- `interface names`: Identically named sampled input or observed output.

### LTL properties

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
G((G(permit)) -> F(BLOWER_RUN))
```

A sustained permitted demand eventually starts under advancing time.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Exact delay threshold, sustained operation and second counted start | 8 |
| T2 | Emergency stop discards partial and completed delay | 7 |

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
  "running": false,
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

- `top3`: The three indices with highest priority, lower index winning a tie.
- `runPrev[i]`: The pre-scan RunComd value of pump i.
- `readOnlyPreserved`: All five priority and selection values equal their sampled values.
- `runs[i]`: Post-scan pumpGroup[i].RunComd, for i=1..5.
- `select[i]`: Sampled pumpGroup[i].selection.
- `interface names`: Identically named sampled input or output.

### LTL properties

**P1** 

```text
G(stop -> (forall i in 1..5: !runs[i]))
```

Stop de-energizes all pumps.

**P2** 

```text
G((!stop & start & !mode) -> (forall i in 1..5: runs[i]=select[i]))
```

Manual start uses exactly the selected pumps.

**P3** 

```text
G((!stop & start & mode) -> (forall i in 1..5: runs[i]=(i in top3)))
```

Automatic start runs exactly the highest-priority three.

**P4** 

```text
G((!stop & !start) -> (forall i in 1..5: runs[i]=runPrev[i]))
```

Start/stop operation latches commands.

**P5** 

```text
G(readOnlyPreserved)
```

The FB may not modify priorities or selections.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Manual latching, read-only fields and simultaneous stop/start | 3 |
| T2 | Automatic top-three selection and deterministic ties | 3 |

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

### LTL properties

**P1** 

```text
G(readonlyPreserved)
```

Input arrays and configuration are never modified.

**P2** 

```text
G(forall j: !enabled(j) -> preserved(j))
```

Disabled and unprocessed channels are unchanged.

**P3** 

```text
G(forall j: (enabled(j) & !modeOK(j)) -> (retVal(j)=16#8001 & outputValue(j)=sampledOutputValue(j)))
```

Unsupported modes return the defined status without conversion.

**P4** 

```text
G(forall j: (enabled(j) & modeOK(j) & !limitsOK(j)) -> (retVal(j)=16#8002 & outputValue(j)=sampledOutputValue(j)))
```

Invalid limits return their status without conversion.

**P5** 

```text
G(forall j: (enabled(j) & modeOK(j) & limitsOK(j)) -> retVal(j)=0)
```

Successful enabled channels clear their status.

**P6** 

```text
G(forall j: (enabled(j) & limitsOK(j) & measuringMode(j)=0) -> outputValue(j)=scaled(j))
```

Linear scale uses the correct unipolar or bipolar range.

**P7** 

```text
G(forall j: (enabled(j) & limitsOK(j) & measuringMode(j)=1) -> outputValue(j)=raw(j)/10)
```

Standard-temperature resolution is one tenth.

**P8** 

```text
G(forall j: (enabled(j) & limitsOK(j) & measuringMode(j)=2) -> outputValue(j)=raw(j)/100)
```

Climatic-temperature resolution is one hundredth.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Unipolar and bipolar endpoints, midpoint and temperature modes | 1 |
| T2 | Disabled channel, invalid mode priority, invalid limits and count truncation | 1 |
| T3 | count zero preserves every value and negative raw extrapolates | 2 |

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
- `previousTrigger`: Pre-scan retained trigger, initialized FALSE.

### LTL properties

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
G(X(previousTrigger)=trigger)
```

Rising-edge memory updates even if sampling is inhibited.

**P7** 

```text
G((valid & !reset & !cyclicExecution & !triggerRise & !windowChanged) -> unchangedMean)
```

No event means no sample update.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Cyclic warm-up, sliding replacement and reset priority | 6 |
| T2 | Rising edge only, held trigger, window change and invalid bounds | 9 |

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
  "cooldownElapsed_ms": 0
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

### Atomic propositions and monitor predicates

- `sensorFault`: TemperatureSensorInput<0 OR TemperatureSensorInput>100
- `demand`: Ghost retained demand; set below setpoint, clear above, retain at equality.
- `heatLimitReached`: Continuous energized time has reached 5s, with first energized scan at elapsed zero.
- `cooldownDone`: At least 3s has elapsed since protection trip.
- `protectPrev`: Pre-scan retained OverheatProtection.
- `interface names`: Identically named sampled input or observed output.

### LTL properties

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
G((OverheatProtection & G(!sensorFault & demand)) -> F(HeaterOutput))
```

With advancing time and persistent valid demand, heating resumes after finite cooldown.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| T1 | Heating threshold, cooldown boundary and safe restart | 6 |
| T2 | Sensor faults, valid endpoint values and equality retention | 7 |
| T3 | Fault during protection cannot clear the cooldown | 5 |

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

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB011.T1 | Neutral, forward, reverse, conflicting commands. | 4 |
| PUB011.T2 | Station waits, retained movement, completion and removal. | 10 |
| PUB011.T3 | Out-of-order confirmations cannot start the route. | 2 |

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

### Atomic propositions and monitor predicates

- `valid`: THICKNESS_SIGNAL_VALID
- `fault`: THICKNESS_FAULT
- `alarm`: THICKNESS_ALARM
- `rise`: valid AND fault AND NOT previous(valid AND fault)
- `record`: count=pre-count+1; history[0]=FaultTimestamp; history[j]=pre-history[j-1] for j=1..4
- `same_stats`: count and history equal pre-scan values
- `hold`: trigger age<500ms with no intervening signal loss
- `normal`: valid AND NOT fault AND CUTTING_RUN
- `add`: runtime=pre-runtime+CycleTime
- `same_time`: runtime=pre-runtime

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB012.T1 | Check 500ms release and immediate signal-loss override. | 7 |
| PUB012.T2 | Six faults retain the five newest timestamps. | 13 |
| PUB012.T3 | Only valid fault-free running accumulates. | 5 |

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

### LTL properties

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
G((G permit) -> F fan)
```

If permit stays TRUE from any scan onward, the fan eventually runs, assuming continued calls and diverging physical time.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB013.T1 | Exercise all setback modes and energy saving scope. | 7 |
| PUB013.T2 | Check delay boundary, loss, full restart, Night override. | 8 |

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
- Embedded NUL is a PLC string terminator; visible input is constrained to declared STRING capacity.

### Atomic propositions and monitor predicates

- `valid`: exactly four nonempty decimal-digit segments separated by periods, each parsed value 0..255
- `packed`: ipValue=a*16777216+b*65536+c*256+d for the four parsed octets
- `zero`: ipValue=0
- `same_input`: input equals previous scan input (not initial call)
- `same_output`: output equals previous scan output

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB014.T1 | Zero, maximum, byte order and decimal leading zeros. | 5 |
| PUB014.T2 | Malformed and overflowing segments clear a previous valid result. | 14 |

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
- autoStart is a rising edge accepted in IDLE; processMode stays fixed during the batch.
- Thresholds are >=50, >=80 and >=100 cm. One logical phase transition occurs per invocation.
- Valve D stays open after discharge is initiated until emergency stop or mode reset; no drain-complete signal is supplied.

### Atomic propositions and monitor predicates

- `safe`: estop
- `off`: all actuator outputs FALSE
- `toggle`: safe AND NOT opeMode AND rising(valveAStart)
- `changed`: valveARun=NOT pre-valveARun
- `held`: safe AND NOT opeMode AND NOT rising(valveAStart) AND no mode change
- `same`: valveARun=pre-valveARun
- `toB`: safe AND opeMode AND pre-phase FILL_A AND levelSensor>=50
- `B`: valveBRun only
- `toMix`: safe AND opeMode AND pre-phase FILL_B AND levelSensor>=80 AND NOT processMode
- `Mix`: mixMotorRun only
- `toC`: safe AND opeMode AND pre-phase FILL_B AND levelSensor>=80 AND processMode
- `C`: valveCRun only
- `fromC`: safe AND opeMode AND pre-phase FILL_C AND levelSensor>=100
- `mixed`: safe AND opeMode AND pre-phase MIX AND mixMotorComplete
- `Drain`: valveDRun only

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB015.T1 | Held signal, second edge, all actuator requests and emergency. | 7 |
| PUB015.T2 | Equality thresholds and mixing completion. | 7 |
| PUB015.T3 | Skipped thresholds advance and emergency cancels the active cycle. | 8 |

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
  "sequenceIndex": 1
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

### Atomic propositions and monitor predicates

- `left`: conveyorLeft
- `right`: conveyorRight
- `higher`: pre-phase MOVING AND targetStation>currentStation AND NOT sensor[targetStation]
- `lower`: pre-phase MOVING AND targetStation<currentStation AND NOT sensor[targetStation]
- `arrive`: pre-phase MOVING AND sensor[targetStation]
- `stop`: NOT conveyorLeft AND NOT conveyorRight
- `waiting`: pre-phase WAIT_PROCESS AND no fresh completion edge
- `out`: pre-phase MOVING AND targetStation=5 AND sensor5
- `done`: post phase IDLE after station5 arrival
- `moving`: pre-phase MOVING
- `processing`: pre-phase WAIT_PROCESS
- `completion`: fresh matching processing-complete edge in the current wait
- `started`: station1Start rising edge accepted with sensor1 in idle

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB016.T1 | Follow [4,2,5] and ignore a wrong completion input. | 8 |
| PUB016.T2 | A one-entry sequence goes directly to output. | 3 |
| PUB016.T3 | A held completion cannot skip a repeated processing operation. | 7 |

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

- At most one request rises per call. Requests use rising edges; simultaneous request priority is unspecified by the source.
- Only positive nonzero IDs are submitted; zero denotes an unused slot.
- Success indicators are one-invocation pulses. error/status clear on idle.
- recipeQueryResult retains the last successful query until another successful query.
- Deleting a record clears only its recipeID; its other fields become unconstrained.
- The caller-owned recipe array is initialized once and persists across steps; do not overwrite it with initial values per scan.
- Compare REAL values with absolute tolerance 1e-5.

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
- `error`: error output
- `same`: database equals pre-database
- `add_ok`: rising(addRecipe) AND positive ID absent AND empty slot exists
- `insert`: lowest-index pre-empty slot equals recipeIn; all other slots unchanged
- `add_success`: recipeAdded AND NOT error AND status=0
- `query_ok`: rising(queryRecipe) AND matching record exists
- `result`: recipeQueryResult equals matching pre-record
- `idle`: no rising request
- `clear`: NOT error AND status=0 AND NOT recipeAdded AND NOT recipeDeleted AND NOT recipeModified
- `unique`: all nonzero IDs are pairwise distinct

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB017.T1 | Add, query, modify, delete and reuse the first empty slot. | 14 |
| PUB017.T2 | All missing-record errors and duplicate rejection preserve existing record. | 11 |
| PUB017.T3 | Fill ten slots; duplicate error has priority over full error. | 23 |

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
- Enqueue and dequeue are never requested together. Reset may coincide with either and wins.
- Edge memories update during reset; a request held afterward is not another edge.
- Reset need not clear buffer values. Unused storage arrangement is unconstrained.

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

- `reset`: reset input
- `empty`: elementCount=0
- `ok`: status=0
- `pop_empty`: NOT reset AND rising(dequeue) AND pre-count=0
- `push_full`: NOT reset AND rising(enqueue) AND pre-count=capacity
- `e1`: status=16#8001
- `e2`: status=16#8002
- `same`: logical queue equals pre-queue AND item equals sampled item
- `push`: NOT reset AND rising(enqueue) AND pre-count<capacity
- `pushed`: post-queue=pre-queue appended with sampled item AND count=pre-count+1 AND status=0
- `pop`: NOT reset AND rising(dequeue) AND pre-count>0
- `popped`: item=pre-front AND post-queue=pre-queue without front AND count=pre-count-1 AND status=0
- `bounded`: 0<=elementCount<=actual buffer length
- `idle`: NOT reset AND no request rising edge

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB018.T1 | Capacity-two FIFO preserves order through wrap, full and empty rejection. | 17 |
| PUB018.T2 | Reset coincides with request; held request after reset does not execute. | 8 |
| PUB018.T3 | Second element type and lower-bound-one buffer. | 9 |

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

- EmergencyStop=FALSE cancels the sequence and outputs; recovery requires a fresh Start edge from a verified top-left pose.
- A Start press is a rising edge. Start edges during an active action are ignored; edge history still updates.
- No selected mode means all commands off and sequence reset. Changing mode also resets the sequence.
- Opposing manual commands on an axis or grip pair are both inhibited. Independent non-opposing actions may run together.
- Manual commands are combinational and stop on their matching limit/feedback. Contradictory limit switches are outside the caller contract.
- Only one phase transition occurs per invocation. In cycle modes, completion feedback switches to the next command in that scan; an already-active next limit suppresses its command but is processed as completion on the next invocation.
- Single-step completion switches all outputs off; the next action requires a fresh Start edge on a later scan.
- Continuous completion of left movement wraps to down in the same scan. Single-cycle completion returns to idle.
- At the start of a new automatic sequence (action 1, not every individual single step), UpLimitSwitch and LeftLimitSwitch must both be TRUE. Grip and release complete on the supplied feedback switches.

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

### LTL properties

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
G(safe & ManualMode -> (down <-> down_manual))
```

Manual down requires the button and an unreached lower limit.

**PUB019.P4** Reached limits

```text
G((down_limit -> !down) & (up_limit -> !up) & (left_limit -> !left) & (right_limit -> !right) & (grip_limit -> !grip) & (release_limit -> !release))
```

Every corresponding completion input suppresses its command.

**PUB019.P5** Step wait

```text
G(safe & (step_done | waiting) -> off)
```

A completed single step waits for another press.

**PUB019.P6** Automatic start

```text
G(safe & start -> started)
```

A permitted fresh start begins down.

**PUB019.P7** Order

```text
G(ordered)
```

The eight preset actions retain their required order.

**PUB019.P8** Cycle boundary

```text
G(safe -> ((cycle_done -> (idle & off)) & (continuous_done -> begin_next)))
```

Single-cycle stops; continuous wraps.

**PUB019.P9** Conditional liveness

```text
(G(safe & SingleCycleMode) & G(busy -> F feedback)) -> G(started -> F idle)
```

With unchanged safe single-cycle mode and eventual matching feedback, every started sequence eventually returns idle.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| PUB019.T1 | Manual hold-to-run, reached limits, opposing requests and emergency priority. | 10 |
| PUB019.T2 | Each new step requires a release and fresh start; held start cannot skip grip. | 9 |
| PUB019.T3 | All eight actions complete once and wait at top left. | 10 |
| PUB019.T4 | The eighth completion wraps immediately to the first action. | 10 |
| PUB019.T5 | Emergency cancels an action; releasing emergency does not auto-restart. | 6 |

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
- firingTemp updates only for accepted weight and retains the last accepted value otherwise. REAL comparisons use absolute tolerance 1e-5.
- At most one phase transition occurs per invocation. Output arrival sets CompletionLight immediately, removal clears it and resets the route.

### Atomic propositions and monitor predicates

- `auto`: Mode
- `fwd`: MotorForward
- `rev`: MotorReverse
- `mf`: ForwardButton AND NOT ReverseButton
- `mr`: ReverseButton AND NOT ForwardButton
- `feed`: pre-phase WAIT_FEED AND SensorFeed
- `moving`: post-phase MOVE_TO_WASH
- `arrival`: pre-phase moving AND corresponding destination sensor TRUE
- `stopped`: NOT MotorForward AND NOT MotorReverse
- `judged`: auto AND pre-phase WAIT_WEIGHT AND SensorWeight AND weightComplete
- `valid`: 100<=weight<=200
- `reject`: kick AND stopped
- `qualified`: NOT kick AND fwd AND firingTemp=500+(weight-100)*0.5
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

### LTL properties

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

Implement a guarded motor latch. Inputs are Start, Stop and GuardClosed. Run initially is FALSE. On every scan, Stop or an open guard forces Run FALSE. Otherwise Start sets Run TRUE; without Start retain Run. If Start remains held while the guard closes, starting on that closing scan is permitted. This is logic for a teaching controller, not a replacement for a safety-rated guard circuit.

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

### Atomic propositions and monitor predicates

- `Start`: Operator start request Boolean names are propositions; numeric names appear only inside defined predicates.
- `Stop`: Stop request Boolean names are propositions; numeric names appear only inside defined predicates.
- `GuardClosed`: Door permissive Boolean names are propositions; numeric names appear only inside defined predicates.
- `Run`: Motor run command Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `qRun`: Run retained from the preceding invocation, initially FALSE.

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| latch | Initialize, start, hold and stop | 5 |
| priority | Simultaneous requests and guard recovery | 5 |

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

ForwardButton and ReverseButton are jog commands. Stop, both buttons, or neither button gives both outputs FALSE. Exactly one button requests that direction. If the previous scan output commanded the opposite direction, give a neutral scan with both outputs FALSE; a request held into the following scan can then run. At initialization the previous direction is neutral. Never energize Forward and Reverse together.

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


### Atomic propositions and monitor predicates

- `ForwardButton`: Forward jog request Boolean names are propositions; numeric names appear only inside defined predicates.
- `ReverseButton`: Reverse jog request Boolean names are propositions; numeric names appear only inside defined predicates.
- `Stop`: Stop request Boolean names are propositions; numeric names appear only inside defined predicates.
- `Forward`: Forward contactor command Boolean names are propositions; numeric names appear only inside defined predicates.
- `Reverse`: Reverse contactor command Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `qForward`: Previous scan Forward output; initially FALSE.
- `qReverse`: Previous scan Reverse output; initially FALSE.
- `fwdOnly`: ForwardButton & !ReverseButton & !Stop.
- `revOnly`: ReverseButton & !ForwardButton & !Stop.

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| reverse | Direct reversal and held reverse request | 6 |
| ambiguous | Both buttons and Stop override direction | 4 |

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

Run initially is FALSE and ResetRequired initially is TRUE. EStopNC=FALSE immediately forces Run FALSE and sets ResetRequired TRUE. While ResetRequired is TRUE, keep Run FALSE. Clear ResetRequired only when EStopNC is TRUE, Reset is TRUE, Start is FALSE and Stop is FALSE. That clearing scan cannot start the motor. Once reset, Stop stops the motor, Start starts it, otherwise retain Run. Start held during reset must not clear the restart inhibition. This educational logic does not implement a certified emergency-stop chain.

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


### Atomic propositions and monitor predicates

- `Start`: Start request Boolean names are propositions; numeric names appear only inside defined predicates.
- `Stop`: Normal stop request Boolean names are propositions; numeric names appear only inside defined predicates.
- `EStopNC`: TRUE means emergency stop released Boolean names are propositions; numeric names appear only inside defined predicates.
- `Reset`: Reset request Boolean names are propositions; numeric names appear only inside defined predicates.
- `Run`: Spindle run command Boolean names are propositions; numeric names appear only inside defined predicates.
- `ResetRequired`: Restart inhibition latch Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `qRequired`: Pre-scan ResetRequired, initially TRUE.
- `qRun`: Pre-scan Run, initially FALSE.
- `validReset`: EStopNC & Reset & !Start & !Stop.

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| reset_restart | Power-up inhibition, reset, run and emergency stop | 6 |
| invalid_reset | Held Start and Stop block reset | 4 |

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

Use states IDLE, MOVING, COMPLETE and FAULT, initially IDLE. Jam forces FAULT from any state; Belt and Complete are FALSE there. With Jam FALSE, Reset returns any state to IDLE. Without Reset, FAULT is latched. Stop aborts a non-fault cycle to IDLE. In IDLE accept Start only if AtExit is FALSE and enter MOVING. In MOVING, AtExit enters COMPLETE. COMPLETE is held until Reset or Stop; Start alone does not clear it. Belt is TRUE only in MOVING, Complete only in COMPLETE and Fault only in FAULT. Execute at most one state transition per scan.

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


### Atomic propositions and monitor predicates

- `Start`: Start one pallet Boolean names are propositions; numeric names appear only inside defined predicates.
- `Stop`: Abort cycle Boolean names are propositions; numeric names appear only inside defined predicates.
- `AtExit`: Pallet at exit Boolean names are propositions; numeric names appear only inside defined predicates.
- `Jam`: Jam detected Boolean names are propositions; numeric names appear only inside defined predicates.
- `Reset`: Clear completion or cleared jam Boolean names are propositions; numeric names appear only inside defined predicates.
- `Belt`: Conveyor command Boolean names are propositions; numeric names appear only inside defined predicates.
- `Complete`: Pallet cycle completed Boolean names are propositions; numeric names appear only inside defined predicates.
- `Fault`: Latched jam fault Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `qIdle`: Pre-state IDLE.
- `qMoving`: Pre-state MOVING.
- `qComplete`: Pre-state COMPLETE.
- `qFault`: Pre-state FAULT.

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| index | One pallet and retained completion | 5 |
| jam | Jam priority, retained fault and safe reset | 6 |

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

Phase 0 is RED for 2 Tick=TRUE invocations, phase 1 GREEN for 3, and phase 2 AMBER for 1. At initialization set phase RED and elapsed ticks zero. With Enable FALSE force RED and clear elapsed ticks every scan. With Enable TRUE and Tick FALSE retain phase and elapsed ticks. A TRUE Tick adds one; upon reaching that phase's duration transition RED->GREEN->AMBER->RED and clear elapsed ticks. Output Phase is 0,1,2 and exactly one color describes the post-transition phase. Tick is an enable level per invocation, not a rising-edge detector.

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
  "elapsed_ticks": 0
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Disable resets the cycle to RED

### Explicit assumptions

- A logical tick is not claimed to be a physical second.
- No opposite road or pedestrian signal is controlled.

### Atomic propositions and monitor predicates

- `Enable`: Enable normal signal cycle Boolean names are propositions; numeric names appear only inside defined predicates.
- `Tick`: One logical tick on each TRUE invocation Boolean names are propositions; numeric names appear only inside defined predicates.
- `Red`: Red lamp Boolean names are propositions; numeric names appear only inside defined predicates.
- `Green`: Green lamp Boolean names are propositions; numeric names appear only inside defined predicates.
- `Amber`: Amber lamp Boolean names are propositions; numeric names appear only inside defined predicates.
- `Phase`: Post-scan phase number Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `qRedLast`: Pre-state is RED with one elapsed tick.
- `qGreenLast`: Pre-state is GREEN with two elapsed ticks.
- `qAmber`: Pre-state is AMBER.
- `qPhase`: Pre-state phase number.
- `oneColor`: Exactly one of Red, Green and Amber is TRUE.

### LTL properties

**P1** 

```text
G(oneColor)
```

The lamp encoding is one-hot.

**P2** 

```text
G(!Enable -> (Red & !Green & !Amber))
```

Disabled operation is a steady red.

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| cycle | Full phase duration boundaries and pause | 7 |
| disable | Disable clears elapsed tick progress | 5 |

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

LowWet and HighWet indicate water covering the respective lower and upper switches. HighWet TRUE with LowWet FALSE is inconsistent: SensorFault TRUE and Fill FALSE. SensorFault is combinational and clears when inputs become consistent. Inhibit or HighWet also forces Fill FALSE. Otherwise LowWet FALSE starts Fill; LowWet TRUE and HighWet FALSE retains Fill. Fill initializes FALSE. Clearing Inhibit at a middle level retains the resulting stopped state until water falls below the low switch.

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
  "Fill": false
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


### Atomic propositions and monitor predicates

- `LowWet`: Water reaches lower switch Boolean names are propositions; numeric names appear only inside defined predicates.
- `HighWet`: Water reaches upper switch Boolean names are propositions; numeric names appear only inside defined predicates.
- `Inhibit`: External fill inhibit Boolean names are propositions; numeric names appear only inside defined predicates.
- `Fill`: Inlet valve command Boolean names are propositions; numeric names appear only inside defined predicates.
- `SensorFault`: Inconsistent level switches Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `qFill`: Pre-scan retained Fill, initially FALSE.
- `middle`: LowWet & !HighWet.

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| hysteresis | Fill cycle across both switching thresholds | 5 |
| fault_inhibit | Invalid switch pair and inhibit recovery | 5 |

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

LeadA initializes TRUE. During Demand choose preferred healthy pump, falling back to the other if the preferred pump is faulted. Both faulty means neither runs. Fault changes cause immediate fallback within the episode. Never run both. When Demand falls FALSE, toggle LeadA exactly once if any pump ran during that just-ended continuous demand episode. An all-faulted episode with no running scan does not toggle the lead. Without Demand both pumps are FALSE. LeadA is the retained preference for the current or next episode, not a report of which fallback pump is presently running.

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
  "episode_served": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Faulted pumps never run
- No demand forces both off
- Prefer selected lead, then healthy fallback

### Explicit assumptions


### Atomic propositions and monitor predicates

- `Demand`: Sump pumping demand Boolean names are propositions; numeric names appear only inside defined predicates.
- `FaultA`: Pump A unavailable Boolean names are propositions; numeric names appear only inside defined predicates.
- `FaultB`: Pump B unavailable Boolean names are propositions; numeric names appear only inside defined predicates.
- `PumpA`: Pump A run command Boolean names are propositions; numeric names appear only inside defined predicates.
- `PumpB`: Pump B run command Boolean names are propositions; numeric names appear only inside defined predicates.
- `LeadA`: TRUE selects A as preferred pump Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `qLeadA`: Pre-scan lead preference, initially TRUE.
- `completedServed`: Pre-scan Demand was TRUE, current Demand is FALSE and a pump ran in that episode.

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| alternate | Served episodes alternate preference | 7 |
| fallback | Fault fallback, unserved episode and recovery | 5 |

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

Preset is valid from 1 through 5. Initialize Count=0. If Trip TRUE, Request FALSE, or Preset invalid, clear Count and Ready. Otherwise Count becomes min(previous Count+1, Preset); Ready is TRUE exactly when Count reaches Preset. Count saturates. Changes of Preset take effect immediately using the same rule, so reducing Preset can qualify on that scan. This counts invocations, not elapsed milliseconds.

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


### Atomic propositions and monitor predicates

- `Request`: Raw qualification request Boolean names are propositions; numeric names appear only inside defined predicates.
- `Trip`: Immediate inhibit Boolean names are propositions; numeric names appear only inside defined predicates.
- `Preset`: Required consecutive scans, valid 1 through 5 Boolean names are propositions; numeric names appear only inside defined predicates.
- `Ready`: Qualified request Boolean names are propositions; numeric names appear only inside defined predicates.
- `Count`: Saturated consecutive scan count Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `invalid`: Preset < 1 or Preset > 5.
- `qualified`: Count >= Preset and Preset is valid.
- `qCount`: Pre-scan Count, initially zero.
- `nextCount`: min(qCount+1, Preset) as an integer expression.

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| delay | Three scans qualify, hold saturates, trip clears | 6 |
| bounds | Invalid presets and immediate reduced threshold | 5 |

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

Target is valid 1..20. Initialize Count=0 and previous PartPulse FALSE. Error is TRUE exactly when Target is invalid. An invalid Target or Reset clears Count and Complete. Otherwise count only a FALSE-to-TRUE PartPulse transition, then clamp Count to Target. Complete is TRUE when Count reaches Target and remains TRUE until reset or an invalid target; a higher Target can clear it. Every scan, including reset and invalid-target scans, samples PartPulse into its edge memory. A held TRUE pulse after reset therefore cannot cause a phantom count.

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
  "previous_pulse": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- Invalid Target and Reset override counting
- Update edge memory on every scan

### Explicit assumptions


### Atomic propositions and monitor predicates

- `PartPulse`: Part detection level Boolean names are propositions; numeric names appear only inside defined predicates.
- `Reset`: Reset batch Boolean names are propositions; numeric names appear only inside defined predicates.
- `Target`: Batch target, valid 1 through 20 Boolean names are propositions; numeric names appear only inside defined predicates.
- `Count`: Saturated part count Boolean names are propositions; numeric names appear only inside defined predicates.
- `Complete`: Target reached Boolean names are propositions; numeric names appear only inside defined predicates.
- `Error`: Invalid target Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `invalid`: Target < 1 or Target > 20.
- `rise`: PartPulse & !qPulse.
- `qPulse`: Previous scan PartPulse, initially FALSE.
- `qCount`: Pre-scan Count, initially zero.
- `countAfterEdge`: min(qCount + (1 if rise else 0), Target).

### LTL properties

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
G(PartPulse -> X qPulse)
```

Edge memory samples the pulse even during reset.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| edges | Held pulses count once and target saturates | 7 |
| reset_edge | Reset while pulse is high suppresses phantom count | 6 |

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

Initialize Alarm and Acknowledged FALSE and previous Fault FALSE. A Fault sets Alarm. A rising Fault also clears Acknowledged, taking priority over Ack on that scan. While Fault remains TRUE, Ack can set Acknowledged. When Fault is FALSE the alarm remains latched; Ack can acknowledge that retained alarm. Reset clears both values only when Fault is FALSE, taking priority over Ack then. A new Fault rising edge reannunciates even if an old alarm was already latched. Horn equals Alarm AND NOT Acknowledged. Always update the previous Fault sample.

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
  "previous_fault": false
}
```

### Scan semantics

At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

### Safety and priorities

- New fault edge reannunciates before Ack
- Reset only clears when Fault is absent
- Reset then precedes Ack

### Explicit assumptions


### Atomic propositions and monitor predicates

- `Fault`: Current fault condition Boolean names are propositions; numeric names appear only inside defined predicates.
- `Ack`: Acknowledge horn Boolean names are propositions; numeric names appear only inside defined predicates.
- `Reset`: Clear a removed fault Boolean names are propositions; numeric names appear only inside defined predicates.
- `Alarm`: Latched visible alarm Boolean names are propositions; numeric names appear only inside defined predicates.
- `Acknowledged`: Alarm acknowledged Boolean names are propositions; numeric names appear only inside defined predicates.
- `Horn`: Unacknowledged alarm horn Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `rise`: Fault & !qFault.
- `qFault`: Previous Fault sample, initially FALSE.
- `qAlarm`: Pre-scan Alarm.
- `qAck`: Pre-scan Acknowledged.

### LTL properties

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
G((!rise & !Reset & Ack & qAlarm) -> Acknowledged)
```

Acknowledgment silences a retained event.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| annunciate | Acknowledge, fault clear and new event | 6 |
| reset_priority | Present fault blocks reset; removed fault reset wins | 3 |

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

Use IDLE, EXTEND, CLAMP, RELEASE, RETRACT and DONE states, initially IDLE. Stop or Reset immediately returns IDLE. Start is accepted in IDLE only if RetractDone indicates the home position. Then enter EXTEND; ExtendDone enters CLAMP, ClampDone enters RELEASE, ReleaseDone enters RETRACT, and RetractDone enters DONE. Execute at most one transition per scan, so even all feedbacks TRUE cannot skip a state. DONE holds until Reset or Stop. Each of Extend, Clamp, Release and Retract is TRUE exactly in its corresponding post-transition state. Busy is TRUE in those four action states; Done is TRUE only in DONE. Start during Busy or DONE is ignored.

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
  "all_commands": false
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

### Atomic propositions and monitor predicates

- `Start`: Begin one fixture cycle Boolean names are propositions; numeric names appear only inside defined predicates.
- `Stop`: Abort fixture cycle Boolean names are propositions; numeric names appear only inside defined predicates.
- `Reset`: Clear cycle state Boolean names are propositions; numeric names appear only inside defined predicates.
- `ExtendDone`: Extension completion handshake Boolean names are propositions; numeric names appear only inside defined predicates.
- `ClampDone`: Clamp completion handshake Boolean names are propositions; numeric names appear only inside defined predicates.
- `ReleaseDone`: Release completion handshake Boolean names are propositions; numeric names appear only inside defined predicates.
- `RetractDone`: Retracted home handshake Boolean names are propositions; numeric names appear only inside defined predicates.
- `Extend`: Slide extend command Boolean names are propositions; numeric names appear only inside defined predicates.
- `Clamp`: Clamp command Boolean names are propositions; numeric names appear only inside defined predicates.
- `Release`: Release command Boolean names are propositions; numeric names appear only inside defined predicates.
- `Retract`: Slide retract command Boolean names are propositions; numeric names appear only inside defined predicates.
- `Busy`: An action state is active Boolean names are propositions; numeric names appear only inside defined predicates.
- `Done`: Cycle completed Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `qIdle`: Pre-state IDLE.
- `qExtend`: Pre-state EXTEND.
- `qClamp`: Pre-state CLAMP.
- `qRelease`: Pre-state RELEASE.
- `qRetract`: Pre-state RETRACT.
- `qDone`: Pre-state DONE.
- `normal`: !Stop & !Reset.
- `oneAction`: At most one of Extend, Clamp, Release, Retract is TRUE.

### LTL properties

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

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| handshake | Normal cycle and completion retention | 9 |
| single_transition | All handshakes cannot skip states; Stop aborts | 5 |

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

States are IDLE, RUNNING, WAIT and LOCKED, initially IDLE with Attempts=0. Start in IDLE starts only when Fault FALSE. A Fault while RUNNING immediately switches off Run. If Attempts<2 enter WAIT, else enter LOCKED. WAIT requires two consecutive Fault=FALSE scans before automatically restarting; a TRUE Fault clears the recovery dwell. Each automatic restart increments Attempts once. LOCKED persists despite Start or Stop. A Reset is accepted only when Fault FALSE and Start FALSE; it returns any state to IDLE and clears Attempts. Otherwise Stop aborts a non-locked state to IDLE and clears its dwell, retaining Attempts. Reset acceptance takes priority over Stop. Run is TRUE only in RUNNING and Locked only in LOCKED. Attempts counts automatic restarts, not the initial operator start. No scan may perform more than one transition.

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
  "recovery_free_scans": 0
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

### Atomic propositions and monitor predicates

- `Start`: Operator start request Boolean names are propositions; numeric names appear only inside defined predicates.
- `Stop`: Abort without clearing retry count Boolean names are propositions; numeric names appear only inside defined predicates.
- `Fault`: Process fault Boolean names are propositions; numeric names appear only inside defined predicates.
- `Reset`: Clear retry history with Start released Boolean names are propositions; numeric names appear only inside defined predicates.
- `Run`: Feeder command Boolean names are propositions; numeric names appear only inside defined predicates.
- `Locked`: Retry exhaustion lockout Boolean names are propositions; numeric names appear only inside defined predicates.
- `Attempts`: Automatic restarts issued, zero through two Boolean names are propositions; numeric names appear only inside defined predicates.
- `first`: True only on the first invocation after resetting the FB instance.
- `qLocked`: Pre-state LOCKED.
- `qRunning`: Pre-state RUNNING.
- `qWait`: Pre-state WAIT.
- `qAttempts`: Pre-scan Attempts, initially zero.
- `validReset`: Reset & !Fault & !Start.
- `retryDue`: qWait & !Fault and one preceding consecutive fault-free WAIT scan.
- `normal`: !validReset & !Stop.

### LTL properties

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
G((qRunning & Fault & normal & (qAttempts = 2)) -> Locked)
```

Failure after the second retry exhausts the budget.

**P6** 

```text
G((retryDue & normal) -> (Run & (Attempts = qAttempts + 1)))
```

Only the second consecutive healthy WAIT scan restarts.

**P7** 

```text
G((qWait & Fault & normal) -> !Run)
```

A fault during recovery clears progress and prevents restart.

### Fixed test index

| Case | Purpose | Steps |
| --- | --- | ---: |
| exhaustion | Two automatic retries then third fault locks | 11 |
| dwell_interrupt | Fault interrupts healthy dwell; Stop aborts wait | 9 |

Full step inputs/expectations are in `dataset/test_cases/manual_tests.md` and the task JSON.
