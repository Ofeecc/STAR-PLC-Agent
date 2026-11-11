# Fixed manual functional tests
These are the complete planned input sequences and expected observations, not measured runtime outputs. Follow docs/functional_testing.md and preserve actual observations separately.
Before each case, initialize a fresh FB instance and its caller storage. Before each step, apply all listed sampled inputs, invoke the generated FB exactly once at the prescribed timing, then observe outputs at the end of that call. Only listed expected outputs are constrained. Never copy an expected output into an actual trace without running the program.
A `$binding` input object means the same caller-owned IN_OUT storage reference is retained; it is not a new data assignment per scan. Binding definitions and timing conventions appear in each task and the testing guide.

## PUB001 Automated Filling Line Control

Scan convention: At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

Initial state:

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

### T1

Full bottle cycle and stable completion

**Step 0**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": false,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "bottleSensor": true,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": false,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": true,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": false,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": true,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": true,
    "fillingConfirmButton": false,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": true,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": true,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": false,
    "Capping_Machine": true,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": false,
    "cappingConfirmButton": true,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": true,
    "Completion_Light": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": false,
    "cappingConfirmButton": false,
    "packingConfirmButton": true,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": true
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": false,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": true
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": false,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": true
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": false,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```


### T2

Out-of-order confirmations cannot skip phases

**Step 0**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": true,
    "cappingConfirmButton": false,
    "packingConfirmButton": true,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "bottleSensor": true,
    "cleaningConfirmButton": true,
    "fillingConfirmButton": true,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": true,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": true,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": true,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": false,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": true
  },
  "expected": {
    "Pump_Motor": true,
    "Filling_Valve": false,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": true,
    "fillingConfirmButton": true,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": true,
    "Capping_Machine": false,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "bottleSensor": false,
    "cleaningConfirmButton": false,
    "fillingConfirmButton": true,
    "cappingConfirmButton": false,
    "packingConfirmButton": false,
    "finishedButton": false
  },
  "expected": {
    "Pump_Motor": false,
    "Filling_Valve": false,
    "Capping_Machine": true,
    "Packing_Machine": false,
    "Completion_Light": false
  }
}
```


## PUB002 Dual-Word Edge Detection

Scan convention: At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

Initial state:

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

### T1

No change, mixed edges, full width and bit 31

**Step 0**.

```json
{
  "inputs": {
    "value": 0
  },
  "expected": {
    "hasChanged": false,
    "hasRisingEdges": false,
    "risingBits": 0,
    "noOfRisingBits": 0,
    "hasFallingEdges": false,
    "fallingBits": 0,
    "noOfFallingBits": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "value": 1
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": true,
    "risingBits": 1,
    "noOfRisingBits": 1,
    "hasFallingEdges": false,
    "fallingBits": 0,
    "noOfFallingBits": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "value": 1
  },
  "expected": {
    "hasChanged": false,
    "hasRisingEdges": false,
    "risingBits": 0,
    "noOfRisingBits": 0,
    "hasFallingEdges": false,
    "fallingBits": 0,
    "noOfFallingBits": 0
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "value": 3
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": true,
    "risingBits": 2,
    "noOfRisingBits": 1,
    "hasFallingEdges": false,
    "fallingBits": 0,
    "noOfFallingBits": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "value": 2
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": false,
    "risingBits": 0,
    "noOfRisingBits": 0,
    "hasFallingEdges": true,
    "fallingBits": 1,
    "noOfFallingBits": 1
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "value": 0
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": false,
    "risingBits": 0,
    "noOfRisingBits": 0,
    "hasFallingEdges": true,
    "fallingBits": 2,
    "noOfFallingBits": 1
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "value": 4294967295
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": true,
    "risingBits": 4294967295,
    "noOfRisingBits": 32,
    "hasFallingEdges": false,
    "fallingBits": 0,
    "noOfFallingBits": 0
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "value": 0
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": false,
    "risingBits": 0,
    "noOfRisingBits": 0,
    "hasFallingEdges": true,
    "fallingBits": 4294967295,
    "noOfFallingBits": 32
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "value": 2147483648
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": true,
    "risingBits": 2147483648,
    "noOfRisingBits": 1,
    "hasFallingEdges": false,
    "fallingBits": 0,
    "noOfFallingBits": 0
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "value": 2147483647
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": true,
    "risingBits": 2147483647,
    "noOfRisingBits": 31,
    "hasFallingEdges": true,
    "fallingBits": 2147483648,
    "noOfFallingBits": 1
  }
}
```


### T2

First nonzero invocation is compared with initialized zero

**Step 0**.

```json
{
  "inputs": {
    "value": 4294967295
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": true,
    "risingBits": 4294967295,
    "noOfRisingBits": 32,
    "hasFallingEdges": false,
    "fallingBits": 0,
    "noOfFallingBits": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "value": 4294967295
  },
  "expected": {
    "hasChanged": false,
    "hasRisingEdges": false,
    "risingBits": 0,
    "noOfRisingBits": 0,
    "hasFallingEdges": false,
    "fallingBits": 0,
    "noOfFallingBits": 0
  }
}
```


### V2_data_contract_boundaries

Independently calculated edge/history/parser boundary regression

**Step 0**.

```json
{
  "inputs": {
    "value": 2863311530
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": true,
    "risingBits": 2863311530,
    "noOfRisingBits": 16,
    "hasFallingEdges": false,
    "fallingBits": 0,
    "noOfFallingBits": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "value": 1431655765
  },
  "expected": {
    "hasChanged": true,
    "hasRisingEdges": true,
    "risingBits": 1431655765,
    "noOfRisingBits": 16,
    "hasFallingEdges": true,
    "fallingBits": 2863311530,
    "noOfFallingBits": 16
  }
}
```


## PUB003 Alarm Handling

Scan convention: At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

Initial state:

```json
{
  "hiAlarm": false,
  "loAlarm": false,
  "error": false,
  "status": 0
}
```

### T1

Strict high and low hysteresis boundaries

**Step 0**.

```json
{
  "inputs": {
    "Value": 50.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": false,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Value": 80.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": false,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Value": 81.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": true,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Value": 75.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": true,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Value": 74.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": false,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Value": 20.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": false,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Value": 19.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": false,
    "loAlarm": true,
    "error": false,
    "status": 0
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Value": 25.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": false,
    "loAlarm": true,
    "error": false,
    "status": 0
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Value": 26.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": false,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```


### T2

Configuration priority, output retention and recovery

**Step 0**.

```json
{
  "inputs": {
    "Value": 90.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": true,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Value": 50.0,
    "hiLevel": 80.0,
    "loLevel": 80.0,
    "hystWindow": 80.0
  },
  "expected": {
    "hiAlarm": true,
    "loAlarm": false,
    "error": true,
    "status": 32769
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Value": 50.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 60.0
  },
  "expected": {
    "hiAlarm": true,
    "loAlarm": false,
    "error": true,
    "status": 32770
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Value": 50.0,
    "hiLevel": 80.0,
    "loLevel": 20.0,
    "hystWindow": 5.0
  },
  "expected": {
    "hiAlarm": false,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```


### V2_data_contract_boundaries

Independently calculated edge/history/parser boundary regression

**Step 0**.

```json
{
  "inputs": {
    "Value": 101,
    "hiLevel": 100,
    "loLevel": 0,
    "hystWindow": 90
  },
  "expected": {
    "hiAlarm": true,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Value": 50,
    "hiLevel": 100,
    "loLevel": 0,
    "hystWindow": 90
  },
  "expected": {
    "hiAlarm": true,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Value": 50,
    "hiLevel": 100,
    "loLevel": 100,
    "hystWindow": 90
  },
  "expected": {
    "hiAlarm": true,
    "loAlarm": false,
    "error": true,
    "status": 32769
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Value": 10,
    "hiLevel": 100,
    "loLevel": 0,
    "hystWindow": 90
  },
  "expected": {
    "hiAlarm": true,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Value": 9,
    "hiLevel": 100,
    "loLevel": 0,
    "hystWindow": 90
  },
  "expected": {
    "hiAlarm": false,
    "loAlarm": false,
    "error": false,
    "status": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Value": -1,
    "hiLevel": 100,
    "loLevel": 0,
    "hystWindow": 90
  },
  "expected": {
    "hiAlarm": false,
    "loAlarm": true,
    "error": false,
    "status": 0
  }
}
```


## PUB004 Jam Pump Debouncing and Runtime Maintenance

Scan convention: At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

Initial state:

```json
{
  "VFD_RUN": false,
  "PUMP_RUNTIME_ACC": "LTIME#0ns",
  "PUMP_MAINT_DUE": false,
  "debounceElapsed_ms": 0
}
```

### T1

Qualification boundary, accumulation, stop retention and restart

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": false,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 2**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 3**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": true,
    "PUMP_RUNTIME_ACC": "LTIME#1000ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 4**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": true,
    "PUMP_RUNTIME_ACC": "LTIME#2000ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 5**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": false,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#2000ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 6**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#2000ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 7**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#2000ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 8**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": true,
    "PUMP_RUNTIME_ACC": "LTIME#3000ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```


### T2

E-stop clears incomplete debounce and completed permission

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 2**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": false,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 3**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 4**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 5**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": true,
    "PUMP_RUNTIME_ACC": "LTIME#1000ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 6**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": false,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#1000ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```


### T3

Long-duration maintenance arithmetic boundary

notes: This expected trace contains a genuine 500-hour elapsed interval matching CycleTime; it is not a short physical-runtime test or evidence of 500 hours of operation. Automated execution needs a separately validated virtual-clock mechanism, otherwise perform only as a long-duration test. TIME#500h is 1.8e9 ms and fits unsigned 32-bit TIME.

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `1800000000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#500h"
  },
  "expected": {
    "VFD_RUN": true,
    "PUMP_RUNTIME_ACC": "LTIME#1800000000ms",
    "PUMP_MAINT_DUE": true
  },
  "dt_ms": 1800000000
}
```

**Step 2**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": true,
    "PUMP_RUNTIME_ACC": "LTIME#1800001000ms",
    "PUMP_MAINT_DUE": true
  },
  "dt_ms": 1000
}
```

**Step 3**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": false,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#2s",
    "CycleTime": "T#1s"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#1800001000ms",
    "PUMP_MAINT_DUE": true
  },
  "dt_ms": 1000
}
```


### V2_permit_loss_at_deadline

Permission loss at the exact deadline wins; recovery starts a fresh full interval, even after a long gap.

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#1s",
    "CycleTime": "T#100ms"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": false,
    "DebounceTime": "T#1s",
    "CycleTime": "T#100ms"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1000
}
```

**Step 2**; elapsed interval `2000 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#1s",
    "CycleTime": "T#100ms"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 2000
}
```

**Step 3**; elapsed interval `999 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#1s",
    "CycleTime": "T#100ms"
  },
  "expected": {
    "VFD_RUN": false,
    "PUMP_RUNTIME_ACC": "LTIME#0ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 999
}
```

**Step 4**; elapsed interval `1 ms`.

```json
{
  "inputs": {
    "VISCOSITY_OK": true,
    "PASTE_E_STOP_NC": true,
    "DebounceTime": "T#1s",
    "CycleTime": "T#100ms"
  },
  "expected": {
    "VFD_RUN": true,
    "PUMP_RUNTIME_ACC": "LTIME#100ms",
    "PUMP_MAINT_DUE": false
  },
  "dt_ms": 1
}
```


## PUB005 Weld Gap Alarm and Startup Inhibition

Scan convention: At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

Initial state:

```json
{
  "Operator_Alert": false,
  "Weld_Soft_Start_Active": true,
  "startupElapsed_ms": 0,
  "gapElapsed_ms": 0
}
```

### T1

Initialization excludes gap timing and debounce starts at 5s

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": true
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `4000 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": true
  },
  "dt_ms": 4000
}
```

**Step 2**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 1000
}
```

**Step 3**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 1000
}
```

**Step 4**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": true,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 1000
}
```

**Step 5**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": false,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 100
}
```


### T2

E-stop suppresses startup and normal alerts without restarting inhibition

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": false,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": true
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `5000 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": false,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 5000
}
```

**Step 2**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 100
}
```

**Step 3**; elapsed interval `2000 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": true,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 2000
}
```

**Step 4**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": false,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 100
}
```

**Step 5**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 100
}
```

**Step 6**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": false,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 1000
}
```

**Step 7**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "Gap_Exceeded": true,
    "Weld_E_Stop_NC": true,
    "DebounceTime": "T#2s"
  },
  "expected": {
    "Operator_Alert": true,
    "Weld_Soft_Start_Active": false
  },
  "dt_ms": 1000
}
```


## PUB006 Aeration Blower Delayed Start

Scan convention: At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

Initial state:

```json
{
  "BLOWER_RUN": false,
  "AERATION_BLOWER_CYCLE_COUNT": 0,
  "delayElapsed_ms": 0
}
```

### T1

Exact delay threshold, sustained operation and second counted start

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "DO_LOW": false,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 100
}
```

**Step 2**; elapsed interval `4999 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 4999
}
```

**Step 3**; elapsed interval `1 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": true,
    "AERATION_BLOWER_CYCLE_COUNT": 1
  },
  "dt_ms": 1
}
```

**Step 4**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": true,
    "AERATION_BLOWER_CYCLE_COUNT": 1
  },
  "dt_ms": 1000
}
```

**Step 5**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "DO_LOW": false,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 1
  },
  "dt_ms": 100
}
```

**Step 6**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 1
  },
  "dt_ms": 100
}
```

**Step 7**; elapsed interval `5000 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": true,
    "AERATION_BLOWER_CYCLE_COUNT": 2
  },
  "dt_ms": 5000
}
```


### T2

Emergency stop discards partial and completed delay

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `4000 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 4000
}
```

**Step 2**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": false
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 1000
}
```

**Step 3**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 100
}
```

**Step 4**; elapsed interval `4999 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 4999
}
```

**Step 5**; elapsed interval `1 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": true,
    "AERATION_BLOWER_CYCLE_COUNT": 1
  },
  "dt_ms": 1
}
```

**Step 6**; elapsed interval `1 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": false
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 1
  },
  "dt_ms": 1
}
```


### V2_permit_loss_at_deadline

Permission loss at the exact deadline wins; recovery starts a fresh full interval, even after a long gap.

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `5000 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": false
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 5000
}
```

**Step 2**; elapsed interval `10000 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 10000
}
```

**Step 3**; elapsed interval `4999 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": false,
    "AERATION_BLOWER_CYCLE_COUNT": 0
  },
  "dt_ms": 4999
}
```

**Step 4**; elapsed interval `1 ms`.

```json
{
  "inputs": {
    "DO_LOW": true,
    "AERATION_E_STOP_NC": true
  },
  "expected": {
    "BLOWER_RUN": true,
    "AERATION_BLOWER_CYCLE_COUNT": 1
  },
  "dt_ms": 1
}
```


## PUB007 Multi-Pump Switching Control System

Scan convention: At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

Initial state:

```json
{
  "running": false,
  "pumpGroup[].RunComd": false
}
```

### T1

Manual latching, read-only fields and simultaneous stop/start

**Step 0**.

```json
{
  "inputs": {
    "mode": false,
    "start": true,
    "stop": false,
    "pumpGroup": [
      {
        "priority": 10,
        "selection": true,
        "RunComd": false
      },
      {
        "priority": 20,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 30,
        "selection": true,
        "RunComd": false
      },
      {
        "priority": 40,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 50,
        "selection": false,
        "RunComd": false
      }
    ]
  },
  "expected": {
    "pumpGroup": [
      {
        "priority": 10,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 20,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 30,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 40,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 50,
        "selection": false,
        "RunComd": false
      }
    ]
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "mode": false,
    "start": false,
    "stop": false,
    "pumpGroup": [
      {
        "priority": 10,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 20,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 30,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 40,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 50,
        "selection": false,
        "RunComd": false
      }
    ]
  },
  "expected": {
    "pumpGroup": [
      {
        "priority": 10,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 20,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 30,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 40,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 50,
        "selection": false,
        "RunComd": false
      }
    ]
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "mode": false,
    "start": true,
    "stop": true,
    "pumpGroup": [
      {
        "priority": 10,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 20,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 30,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 40,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 50,
        "selection": false,
        "RunComd": false
      }
    ]
  },
  "expected": {
    "pumpGroup": [
      {
        "priority": 10,
        "selection": true,
        "RunComd": false
      },
      {
        "priority": 20,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 30,
        "selection": true,
        "RunComd": false
      },
      {
        "priority": 40,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 50,
        "selection": false,
        "RunComd": false
      }
    ]
  }
}
```


### T2

Automatic top-three selection and deterministic ties

**Step 0**.

```json
{
  "inputs": {
    "mode": true,
    "start": true,
    "stop": false,
    "pumpGroup": [
      {
        "priority": 10,
        "selection": true,
        "RunComd": false
      },
      {
        "priority": 20,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 30,
        "selection": true,
        "RunComd": false
      },
      {
        "priority": 40,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 50,
        "selection": false,
        "RunComd": false
      }
    ]
  },
  "expected": {
    "pumpGroup": [
      {
        "priority": 10,
        "selection": true,
        "RunComd": false
      },
      {
        "priority": 20,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 30,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 40,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 50,
        "selection": false,
        "RunComd": true
      }
    ]
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "mode": true,
    "start": true,
    "stop": false,
    "pumpGroup": [
      {
        "priority": 5,
        "selection": true,
        "RunComd": false
      },
      {
        "priority": 5,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 5,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 5,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 5,
        "selection": false,
        "RunComd": true
      }
    ]
  },
  "expected": {
    "pumpGroup": [
      {
        "priority": 5,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 5,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 5,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 5,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 5,
        "selection": false,
        "RunComd": false
      }
    ]
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "mode": true,
    "start": true,
    "stop": false,
    "pumpGroup": [
      {
        "priority": -3,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": 0,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": -1,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": -2,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 4,
        "selection": false,
        "RunComd": false
      }
    ]
  },
  "expected": {
    "pumpGroup": [
      {
        "priority": -3,
        "selection": true,
        "RunComd": false
      },
      {
        "priority": 0,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": -1,
        "selection": true,
        "RunComd": true
      },
      {
        "priority": -2,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 4,
        "selection": false,
        "RunComd": true
      }
    ]
  }
}
```


### V2_pump_reselection_history

Ties, changed priorities without start, reselection and simultaneous stop/start.

**Step 0**.

```json
{
  "inputs": {
    "mode": true,
    "start": true,
    "stop": false,
    "pumpGroup": [
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      }
    ]
  },
  "expected": {
    "pumpGroup": [
      {
        "priority": 1,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      }
    ]
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "mode": true,
    "start": false,
    "stop": false,
    "pumpGroup": [
      {
        "priority": 1,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 2,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 3,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 4,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 5,
        "selection": false,
        "RunComd": false
      }
    ]
  },
  "expected": {
    "pumpGroup": [
      {
        "priority": 1,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 2,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 3,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 4,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 5,
        "selection": false,
        "RunComd": false
      }
    ]
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "mode": true,
    "start": true,
    "stop": false,
    "pumpGroup": [
      {
        "priority": 1,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 2,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 3,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 4,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 5,
        "selection": false,
        "RunComd": false
      }
    ]
  },
  "expected": {
    "pumpGroup": [
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 2,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 3,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 4,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 5,
        "selection": false,
        "RunComd": true
      }
    ]
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "mode": true,
    "start": true,
    "stop": true,
    "pumpGroup": [
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": true
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": true
      }
    ]
  },
  "expected": {
    "pumpGroup": [
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      },
      {
        "priority": 1,
        "selection": false,
        "RunComd": false
      }
    ]
  }
}
```


## PUB008 Analog Batch Processing

Scan convention: At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

Initial state:

```json
{
  "state": "No internal history required. IN_OUT output fields retain caller-provided values when skipped."
}
```

### T1

Unipolar and bipolar endpoints, midpoint and temperature modes

array_lower_bounds: {
  "analogValues": -2,
  "channels": 7
}

tolerance: {
  "absolute": 0.0001,
  "relative": 1e-05
}

**Step 0**.

```json
{
  "inputs": {
    "count": 7,
    "analogValues": [
      0,
      27648,
      -27648,
      0,
      27648,
      1234,
      -1234
    ],
    "channels": [
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": true,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": true,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": true,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 1,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 2,
        "retVal": 7,
        "outputValue": -999.0
      }
    ]
  },
  "expected": {
    "analogValues": [
      0,
      27648,
      -27648,
      0,
      27648,
      1234,
      -1234
    ],
    "channels": [
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 0,
        "outputValue": 0.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 0,
        "outputValue": 100.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": true,
        "measuringMode": 0,
        "retVal": 0,
        "outputValue": 0.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": true,
        "measuringMode": 0,
        "retVal": 0,
        "outputValue": 50.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": true,
        "measuringMode": 0,
        "retVal": 0,
        "outputValue": 100.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 1,
        "retVal": 0,
        "outputValue": 123.4
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 2,
        "retVal": 0,
        "outputValue": -12.34
      }
    ]
  }
}
```


### T2

Disabled channel, invalid mode priority, invalid limits and count truncation

**Step 0**.

```json
{
  "inputs": {
    "count": 4,
    "analogValues": [
      1,
      2,
      3,
      4,
      5
    ],
    "channels": [
      {
        "enable": false,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 0,
        "loLIM": 10,
        "bipolar": false,
        "measuringMode": 9,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 10,
        "loLIM": 10,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 2,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      }
    ]
  },
  "expected": {
    "analogValues": [
      1,
      2,
      3,
      4,
      5
    ],
    "channels": [
      {
        "enable": false,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 0,
        "loLIM": 10,
        "bipolar": false,
        "measuringMode": 9,
        "retVal": 32769,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 10,
        "loLIM": 10,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 32770,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 2,
        "retVal": 0,
        "outputValue": 0.04
      },
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      }
    ]
  }
}
```


### T3

count zero preserves every value and negative raw extrapolates

**Step 0**.

```json
{
  "inputs": {
    "count": 0,
    "analogValues": [
      -27648
    ],
    "channels": [
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      }
    ]
  },
  "expected": {
    "analogValues": [
      -27648
    ],
    "channels": [
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      }
    ]
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "count": 1,
    "analogValues": [
      -27648
    ],
    "channels": [
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      }
    ]
  },
  "expected": {
    "analogValues": [
      -27648
    ],
    "channels": [
      {
        "enable": true,
        "hiLIM": 100.0,
        "loLIM": 0.0,
        "bipolar": false,
        "measuringMode": 0,
        "retVal": 0,
        "outputValue": -100.0
      }
    ]
  }
}
```


### V2_unequal_arrays_wide_arithmetic

Unequal lengths and distinct lower bounds; preserve skipped channel; avoid INT intermediate overflow.

array_lower_bounds: {
  "analogValues": -3,
  "channels": 9
}

**Step 0**.

```json
{
  "inputs": {
    "count": 1,
    "analogValues": [
      32767
    ],
    "channels": [
      {
        "enable": true,
        "hiLIM": 27648.0,
        "loLIM": -27648.0,
        "bipolar": true,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": -999.0
      },
      {
        "enable": true,
        "hiLIM": 27648.0,
        "loLIM": -27648.0,
        "bipolar": true,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": 33.0
      }
    ]
  },
  "expected": {
    "analogValues": [
      32767
    ],
    "channels": [
      {
        "enable": true,
        "hiLIM": 27648.0,
        "loLIM": -27648.0,
        "bipolar": true,
        "measuringMode": 0,
        "retVal": 0,
        "outputValue": 32767.0
      },
      {
        "enable": true,
        "hiLIM": 27648.0,
        "loLIM": -27648.0,
        "bipolar": true,
        "measuringMode": 0,
        "retVal": 7,
        "outputValue": 33.0
      }
    ]
  }
}
```


## PUB009 Calculate Moving Average

Scan convention: At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

Initial state:

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

### T1

Cyclic warm-up, sliding replacement and reset priority

**Step 0**.

```json
{
  "inputs": {
    "cyclicExecution": true,
    "trigger": false,
    "value": 3.0,
    "windowSize": 3,
    "reset": false
  },
  "expected": {
    "average": 3.0,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "cyclicExecution": true,
    "trigger": false,
    "value": 6.0,
    "windowSize": 3,
    "reset": false
  },
  "expected": {
    "average": 4.5,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "cyclicExecution": true,
    "trigger": false,
    "value": 9.0,
    "windowSize": 3,
    "reset": false
  },
  "expected": {
    "average": 6.0,
    "windowSizeReached": true,
    "error": false,
    "status": 0
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "cyclicExecution": true,
    "trigger": true,
    "value": 12.0,
    "windowSize": 3,
    "reset": false
  },
  "expected": {
    "average": 9.0,
    "windowSizeReached": true,
    "error": false,
    "status": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "cyclicExecution": true,
    "trigger": false,
    "value": 99.0,
    "windowSize": 3,
    "reset": true
  },
  "expected": {
    "average": 0.0,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "cyclicExecution": true,
    "trigger": false,
    "value": -6.0,
    "windowSize": 3,
    "reset": false
  },
  "expected": {
    "average": -6.0,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```


### T2

Rising edge only, held trigger, window change and invalid bounds

tolerance: {
  "absolute": 1e-09,
  "relative": 1e-09
}

**Step 0**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": true,
    "value": 2.0,
    "windowSize": 3,
    "reset": false
  },
  "expected": {
    "average": 2.0,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": true,
    "value": 100.0,
    "windowSize": 3,
    "reset": false
  },
  "expected": {
    "average": 2.0,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": false,
    "value": 100.0,
    "windowSize": 3,
    "reset": false
  },
  "expected": {
    "average": 2.0,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": true,
    "value": 4.0,
    "windowSize": 3,
    "reset": false
  },
  "expected": {
    "average": 3.0,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "cyclicExecution": true,
    "trigger": false,
    "value": 8.0,
    "windowSize": 1,
    "reset": false
  },
  "expected": {
    "average": 8.0,
    "windowSizeReached": true,
    "error": false,
    "status": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": false,
    "value": 0.0,
    "windowSize": 0,
    "reset": false
  },
  "expected": {
    "average": 8.0,
    "windowSizeReached": true,
    "error": true,
    "status": 33280
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": false,
    "value": 0.0,
    "windowSize": 101,
    "reset": false
  },
  "expected": {
    "average": 8.0,
    "windowSizeReached": true,
    "error": true,
    "status": 33280
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": false,
    "value": 0.0,
    "windowSize": 1,
    "reset": true
  },
  "expected": {
    "average": 0.0,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": true,
    "value": 5.0,
    "windowSize": 1,
    "reset": false
  },
  "expected": {
    "average": 5.0,
    "windowSizeReached": true,
    "error": false,
    "status": 0
  }
}
```


### V2_data_contract_boundaries

Independently calculated edge/history/parser boundary regression

**Step 0**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": true,
    "value": 8,
    "windowSize": 2,
    "reset": false
  },
  "expected": {
    "average": 8,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": false,
    "value": 8,
    "windowSize": 2,
    "reset": false
  },
  "expected": {
    "average": 8,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": true,
    "value": 99,
    "windowSize": 0,
    "reset": false
  },
  "expected": {
    "average": 8,
    "windowSizeReached": false,
    "error": true,
    "status": 33280
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": true,
    "value": 100,
    "windowSize": 2,
    "reset": false
  },
  "expected": {
    "average": 8,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": false,
    "value": 8,
    "windowSize": 2,
    "reset": false
  },
  "expected": {
    "average": 8,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": true,
    "value": 4,
    "windowSize": 2,
    "reset": false
  },
  "expected": {
    "average": 6,
    "windowSizeReached": true,
    "error": false,
    "status": 0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "cyclicExecution": false,
    "trigger": false,
    "value": 8,
    "windowSize": 3,
    "reset": false
  },
  "expected": {
    "average": 0,
    "windowSizeReached": false,
    "error": false,
    "status": 0
  }
}
```


## PUB010 Temperature Logic Control

Scan convention: At scan k, inputs I[k] are sampled once, q[k] is pre-scan retained state, outputs O[k] are observed after execution, and q[k+1] is the updated state. Each test creates a fresh FB instance before step 0. An initialized instance has not yet executed a scan. Timer elapsed time is zero on the first eligible sampled invocation; dt_ms is elapsed wall time since the previous invocation, not automatically a synthetic input to the FB. No unobserved past input stability is assumed. All sequences here are expected values.

Initial state:

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

### T1

Heating threshold, cooldown boundary and safe restart

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 20.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 20.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": true,
    "OverheatProtection": false,
    "HeaterOutput": true
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `4999 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 20.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 20.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": true,
    "OverheatProtection": false,
    "HeaterOutput": true
  },
  "dt_ms": 4999
}
```

**Step 2**; elapsed interval `1 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 20.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 20.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": true,
    "HeaterOutput": false
  },
  "dt_ms": 1
}
```

**Step 3**; elapsed interval `2999 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 20.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 20.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": true,
    "HeaterOutput": false
  },
  "dt_ms": 2999
}
```

**Step 4**; elapsed interval `1 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 20.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 20.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": true,
    "OverheatProtection": false,
    "HeaterOutput": true
  },
  "dt_ms": 1
}
```

**Step 5**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 31.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 31.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": false,
    "HeaterOutput": false
  },
  "dt_ms": 100
}
```


### T2

Sensor faults, valid endpoint values and equality retention

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 30.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 30.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": false,
    "HeaterOutput": false
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 0.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 0.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": true,
    "OverheatProtection": false,
    "HeaterOutput": true
  },
  "dt_ms": 100
}
```

**Step 2**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 30.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 30.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": true,
    "OverheatProtection": false,
    "HeaterOutput": true
  },
  "dt_ms": 100
}
```

**Step 3**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": -0.1,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": -0.1,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": false,
    "HeaterOutput": false
  },
  "dt_ms": 100
}
```

**Step 4**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 100.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 100.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": false,
    "HeaterOutput": false
  },
  "dt_ms": 100
}
```

**Step 5**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 100.1,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 100.1,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": false,
    "HeaterOutput": false
  },
  "dt_ms": 100
}
```

**Step 6**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 30.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 30.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": false,
    "HeaterOutput": false
  },
  "dt_ms": 100
}
```


### T3

Fault during protection cannot clear the cooldown

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 20.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 20.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": true,
    "OverheatProtection": false,
    "HeaterOutput": true
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `5000 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 20.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 20.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": true,
    "HeaterOutput": false
  },
  "dt_ms": 5000
}
```

**Step 2**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": -1.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": -1.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": true,
    "HeaterOutput": false
  },
  "dt_ms": 1000
}
```

**Step 3**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 20.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 20.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": true,
    "HeaterOutput": false
  },
  "dt_ms": 1000
}
```

**Step 4**; elapsed interval `1000 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 20.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 20.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": true,
    "OverheatProtection": false,
    "HeaterOutput": true
  },
  "dt_ms": 1000
}
```


### V2_omission_regression

Reject the concrete wrong behavior documented in the 2026-11-06 specification review.

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 40.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 40.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": false,
    "HeaterOutput": false
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 40.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 40.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": false,
    "HeaterOutput": false
  },
  "dt_ms": 100
}
```

**Step 2**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "TemperatureSensorInput": 40.0,
    "SetTemperature": 30.0
  },
  "expected": {
    "CurrentTemperature": 40.0,
    "SetTempDisplay": 30.0,
    "HeaterStatus": false,
    "OverheatProtection": false,
    "HeaterOutput": false
  },
  "dt_ms": 100
}
```


## PUB011 Automated Production Line Control

Scan convention: Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

Initial state:

```json
{
  "MotorForward": false,
  "MotorReverse": false,
  "CompletionLight": false,
  "phase": "WAIT_A"
}
```

### PUB011.T1 manual

Neutral, forward, reverse, conflicting commands.

**Step 0**.

```json
{
  "inputs": {
    "Mode": false,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": false,
    "ForwardButton": true,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": false,
    "ForwardButton": false,
    "ReverseButton": true,
    "SensorA": false,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": true
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Mode": false,
    "ForwardButton": true,
    "ReverseButton": true,
    "SensorA": false,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false
  }
}
```


### PUB011.T2 cycle

Station waits, retained movement, completion and removal.

**Step 0**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": false,
    "CompletionLight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": true,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": true,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": true,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": true
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": true
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": true,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": true,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": true,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": true
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": false,
    "SensorC": true,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": false,
    "CompletionLight": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": false,
    "SensorC": true,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": true
  },
  "expected": {
    "CompletionLight": true
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": false,
    "SensorC": true,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "CompletionLight": true
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "CompletionLight": false
  }
}
```


### PUB011.T3 wrong_button

Out-of-order confirmations cannot start the route.

**Step 0**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": false,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": true,
    "ButtonC": true
  },
  "expected": {
    "MotorForward": false,
    "CompletionLight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": true,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": false,
    "ButtonB": true,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": false
  }
}
```


### V2_omission_regression

Reject the concrete wrong behavior documented in the 2026-11-06 specification review.

**Step 0**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": true,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": true,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "CompletionLight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": true,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": true,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "CompletionLight": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorA": true,
    "SensorB": false,
    "SensorC": false,
    "ButtonA": true,
    "ButtonB": false,
    "ButtonC": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "CompletionLight": false
  }
}
```


## PUB012 Slab Thickness Alarm and Fault History

Scan convention: Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

Initial state:

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

### PUB012.T1 hold

Check 500ms release and immediate signal-loss override.

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "THICKNESS_ALARM": false,
    "Slab_Fault_Counter": 0
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": true,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 101,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "THICKNESS_ALARM": true,
    "Slab_Fault_Counter": 1,
    "Slab_Fault_History": [
      101,
      0,
      0,
      0,
      0
    ]
  },
  "dt_ms": 100
}
```

**Step 2**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "THICKNESS_ALARM": true
  },
  "dt_ms": 100
}
```

**Step 3**; elapsed interval `300 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "THICKNESS_ALARM": true
  },
  "dt_ms": 300
}
```

**Step 4**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "THICKNESS_ALARM": false
  },
  "dt_ms": 100
}
```

**Step 5**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": true,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 102,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "THICKNESS_ALARM": true,
    "Slab_Fault_Counter": 2
  },
  "dt_ms": 100
}
```

**Step 6**; elapsed interval `10 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": true,
    "THICKNESS_SIGNAL_VALID": false,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "THICKNESS_ALARM": false,
    "Slab_Fault_Counter": 2
  },
  "dt_ms": 10
}
```


### PUB012.T2 history

Six faults retain the five newest timestamps.

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 0
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": true,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 1,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 1,
    "Slab_Fault_History": [
      1,
      0,
      0,
      0,
      0
    ]
  },
  "dt_ms": 100
}
```

**Step 2**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 1
  },
  "dt_ms": 100
}
```

**Step 3**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": true,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 2,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 2,
    "Slab_Fault_History": [
      2,
      1,
      0,
      0,
      0
    ]
  },
  "dt_ms": 100
}
```

**Step 4**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 2
  },
  "dt_ms": 100
}
```

**Step 5**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": true,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 3,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 3,
    "Slab_Fault_History": [
      3,
      2,
      1,
      0,
      0
    ]
  },
  "dt_ms": 100
}
```

**Step 6**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 3
  },
  "dt_ms": 100
}
```

**Step 7**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": true,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 4,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 4,
    "Slab_Fault_History": [
      4,
      3,
      2,
      1,
      0
    ]
  },
  "dt_ms": 100
}
```

**Step 8**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 4
  },
  "dt_ms": 100
}
```

**Step 9**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": true,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 5,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 5,
    "Slab_Fault_History": [
      5,
      4,
      3,
      2,
      1
    ]
  },
  "dt_ms": 100
}
```

**Step 10**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 5
  },
  "dt_ms": 100
}
```

**Step 11**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": true,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 6,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 6,
    "Slab_Fault_History": [
      6,
      5,
      4,
      3,
      2
    ]
  },
  "dt_ms": 100
}
```

**Step 12**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Fault_Counter": 6
  },
  "dt_ms": 100
}
```


### PUB012.T3 runtime

Only valid fault-free running accumulates.

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": true,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Runtime_Accumulator": "LTIME#100ms"
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": true,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Runtime_Accumulator": "LTIME#200ms"
  },
  "dt_ms": 100
}
```

**Step 2**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": true,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": true,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Runtime_Accumulator": "LTIME#200ms"
  },
  "dt_ms": 100
}
```

**Step 3**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": false,
    "CUTTING_RUN": true,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Runtime_Accumulator": "LTIME#200ms"
  },
  "dt_ms": 100
}
```

**Step 4**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "THICKNESS_FAULT": false,
    "THICKNESS_SIGNAL_VALID": true,
    "CUTTING_RUN": false,
    "FaultTimestamp": 0,
    "CycleTime": "T#100ms"
  },
  "expected": {
    "Slab_Runtime_Accumulator": "LTIME#200ms"
  },
  "dt_ms": 100
}
```


## PUB013 Office HVAC Multi-mode Energy-Saving Control

Scan convention: Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

Initial state:

```json
{
  "SUPPLY_FAN_RUN": false,
  "TEMP_SETPOINT_ADJUST": 0
}
```

### PUB013.T1 mode_table

Exercise all setback modes and energy saving scope.

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": false,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": false,
    "TEMP_SETPOINT_ADJUST": 2
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": false,
    "ENERGY_SAVING_MODE": true,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "TEMP_SETPOINT_ADJUST": 3
  },
  "dt_ms": 100
}
```

**Step 2**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": false,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 1
  },
  "expected": {
    "TEMP_SETPOINT_ADJUST": 1
  },
  "dt_ms": 100
}
```

**Step 3**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": false,
    "ENERGY_SAVING_MODE": true,
    "HVAC_MODE_SELECTOR": 1
  },
  "expected": {
    "TEMP_SETPOINT_ADJUST": 1
  },
  "dt_ms": 100
}
```

**Step 4**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": false,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 2
  },
  "expected": {
    "TEMP_SETPOINT_ADJUST": 4
  },
  "dt_ms": 100
}
```

**Step 5**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 3
  },
  "expected": {
    "TEMP_SETPOINT_ADJUST": 4,
    "SUPPLY_FAN_RUN": false
  },
  "dt_ms": 100
}
```

**Step 6**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 2
  },
  "expected": {
    "TEMP_SETPOINT_ADJUST": 0,
    "SUPPLY_FAN_RUN": false
  },
  "dt_ms": 100
}
```


### PUB013.T2 delay_restart

Check delay boundary, loss, full restart, Night override.

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": false
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `29900 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": false
  },
  "dt_ms": 29900
}
```

**Step 2**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": true
  },
  "dt_ms": 100
}
```

**Step 3**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": false,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": false
  },
  "dt_ms": 100
}
```

**Step 4**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": false
  },
  "dt_ms": 100
}
```

**Step 5**; elapsed interval `29900 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": false
  },
  "dt_ms": 29900
}
```

**Step 6**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": true
  },
  "dt_ms": 100
}
```

**Step 7**; elapsed interval `100 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 3
  },
  "expected": {
    "SUPPLY_FAN_RUN": false
  },
  "dt_ms": 100
}
```


### V2_permit_loss_at_deadline

Permission loss at the exact deadline wins; recovery starts a fresh full interval, even after a long gap.

**Step 0**; elapsed interval `0 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": false,
    "TEMP_SETPOINT_ADJUST": 0
  },
  "dt_ms": 0
}
```

**Step 1**; elapsed interval `30000 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 3
  },
  "expected": {
    "SUPPLY_FAN_RUN": false,
    "TEMP_SETPOINT_ADJUST": 4
  },
  "dt_ms": 30000
}
```

**Step 2**; elapsed interval `60000 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": false,
    "TEMP_SETPOINT_ADJUST": 0
  },
  "dt_ms": 60000
}
```

**Step 3**; elapsed interval `29999 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": false,
    "TEMP_SETPOINT_ADJUST": 0
  },
  "dt_ms": 29999
}
```

**Step 4**; elapsed interval `1 ms`.

```json
{
  "inputs": {
    "OCCUPANCY_DETECTED": true,
    "ENERGY_SAVING_MODE": false,
    "HVAC_MODE_SELECTOR": 0
  },
  "expected": {
    "SUPPLY_FAN_RUN": true,
    "TEMP_SETPOINT_ADJUST": 0
  },
  "dt_ms": 1
}
```


## PUB014 IPv4 Parsing with Format and Range Checks

Scan convention: Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

Initial state:

```json
{
  "ipValue": 0
}
```

### PUB014.T1 valid

Zero, maximum, byte order and decimal leading zeros.

**Step 0**.

```json
{
  "inputs": {
    "ipText": "0.0.0.0"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "ipText": "255.255.255.255"
  },
  "expected": {
    "ipValue": 4294967295
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "ipText": "192.168.1.10"
  },
  "expected": {
    "ipValue": 3232235786
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "ipText": "1.2.3.4"
  },
  "expected": {
    "ipValue": 16909060
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "ipText": "001.002.003.004"
  },
  "expected": {
    "ipValue": 16909060
  }
}
```


### PUB014.T2 invalid

Malformed and overflowing segments clear a previous valid result.

**Step 0**.

```json
{
  "inputs": {
    "ipText": "1.2.3.4"
  },
  "expected": {
    "ipValue": 16909060
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "ipText": ""
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "ipText": "1.2.3"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "ipText": "1.2.3.4.5"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "ipText": ".1.2.3"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "ipText": "1..2.3"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "ipText": "1.2.3."
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "ipText": "1.2.3.256"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "ipText": "-1.2.3.4"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "ipText": "1.2.3.x"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 10**.

```json
{
  "inputs": {
    "ipText": " 1.2.3.4"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 11**.

```json
{
  "inputs": {
    "ipText": "1.2.3.4 "
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 12**.

```json
{
  "inputs": {
    "ipText": "0x1.2.3.4"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 13**.

```json
{
  "inputs": {
    "ipText": "999999999999999999999.2.3.4"
  },
  "expected": {
    "ipValue": 0
  }
}
```


### V2_data_contract_boundaries

Independently calculated edge/history/parser boundary regression

**Step 0**.

```json
{
  "inputs": {
    "ipText": "+1.2.3.4"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "ipText": "1.2.3.4\n"
  },
  "expected": {
    "ipValue": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "ipText": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001.2.3.4"
  },
  "expected": {
    "ipValue": 16909060
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "ipText": "1.2.3.4294967296"
  },
  "expected": {
    "ipValue": 0
  }
}
```


## PUB015 Material Proportioning Process Control

Scan convention: Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

Initial state:

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

### PUB015.T1 manual_edges

Held signal, second edge, all actuator requests and emergency.

**Step 0**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": false,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": false,
    "valveAStart": true,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": true,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": false,
    "valveAStart": true,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": true,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": false,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": true,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": false,
    "valveAStart": true,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": false,
    "valveAStart": false,
    "valveBStart": true,
    "valveCStart": true,
    "valveDStart": true,
    "mixMotorStart": true,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": true,
    "valveCRun": true,
    "valveDRun": true,
    "mixMotorRun": true
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "estop": false,
    "opeMode": false,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```


### PUB015.T2 two_material

Equality thresholds and mixing completion.

**Step 0**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": true,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": true,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 49,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": true,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 50,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": true,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 80,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": true
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 80,
    "mixMotorComplete": true
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": true,
    "mixMotorRun": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "estop": false,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```


### PUB015.T3 three_material

Skipped thresholds advance and emergency cancels the active cycle.

**Step 0**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": true,
    "processMode": true,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": true,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": true,
    "levelSensor": 55,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": true,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": true,
    "levelSensor": 85,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": true,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": true,
    "levelSensor": 99,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": true,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": true,
    "levelSensor": 100,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": true
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "estop": false,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": true,
    "levelSensor": 0,
    "mixMotorComplete": true
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": true,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```


### V2_process_history_regression

Mode/edge reset, repeated station or prior-batch retained setpoint regression.

**Step 0**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": false,
    "valveAStart": false,
    "valveBStart": true,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": true,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": false,
    "valveAStart": false,
    "valveBStart": true,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": true,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": true,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": true,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": true,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": true,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 50,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": true,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 80,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": false,
    "mixMotorRun": true
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": true
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": true,
    "mixMotorRun": false
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "estop": true,
    "opeMode": true,
    "valveAStart": false,
    "valveBStart": false,
    "valveCStart": false,
    "valveDStart": false,
    "mixMotorStart": false,
    "autoStart": false,
    "processMode": false,
    "levelSensor": 0,
    "mixMotorComplete": false
  },
  "expected": {
    "valveARun": false,
    "valveBRun": false,
    "valveCRun": false,
    "valveDRun": true,
    "mixMotorRun": false
  }
}
```


## PUB016 Flexible Processing Control

Scan convention: Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

Initial state:

```json
{
  "conveyorLeft": false,
  "conveyorRight": false,
  "phase": "IDLE",
  "currentStation": 1,
  "sequenceIndex": 1
}
```

### PUB016.T1 bidirectional_route

Follow [4,2,5] and ignore a wrong completion input.

**Step 0**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": false,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      4,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": true,
    "sensor2": false,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": true,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      4,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": true,
    "conveyorLeft": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": false,
    "sensor3": false,
    "sensor4": true,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      4,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": false,
    "conveyorLeft": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": false,
    "sensor3": false,
    "sensor4": true,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": true,
    "station4Complete": false,
    "processSequence": [
      4,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": false,
    "conveyorLeft": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": false,
    "sensor3": false,
    "sensor4": true,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": true,
    "processSequence": [
      4,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": true,
    "conveyorRight": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      4,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": true,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      4,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": true,
    "conveyorLeft": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": false,
    "sensor3": false,
    "sensor4": false,
    "sensor5": true,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      4,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": false
  }
}
```


### PUB016.T2 minimum_length

A one-entry sequence goes directly to output.

**Step 0**.

```json
{
  "inputs": {
    "processLength": 1,
    "sensor1": false,
    "sensor2": false,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      5,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "processLength": 1,
    "sensor1": true,
    "sensor2": false,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": true,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      5,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": true,
    "conveyorLeft": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "processLength": 1,
    "sensor1": false,
    "sensor2": false,
    "sensor3": false,
    "sensor4": false,
    "sensor5": true,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      5,
      0,
      0,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": false,
    "conveyorLeft": false
  }
}
```


### PUB016.T3 repeat_station

A held completion cannot skip a repeated processing operation.

**Step 0**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": false,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": true,
    "sensor2": false,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": true,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": true
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": true,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": true,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": true,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorRight": true,
    "conveyorLeft": false
  }
}
```


### V2_process_history_regression

Mode/edge reset, repeated station or prior-batch retained setpoint regression.

**Step 0**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": true,
    "sensor2": false,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": true,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": true
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": true,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": true,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": true,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": true,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": true,
    "sensor3": false,
    "sensor4": false,
    "sensor5": false,
    "station1Start": false,
    "station2Complete": true,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": true
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "processLength": 3,
    "sensor1": false,
    "sensor2": false,
    "sensor3": false,
    "sensor4": false,
    "sensor5": true,
    "station1Start": false,
    "station2Complete": false,
    "station3Complete": false,
    "station4Complete": false,
    "processSequence": [
      2,
      2,
      5,
      0,
      0,
      0,
      0,
      0
    ]
  },
  "expected": {
    "conveyorLeft": false,
    "conveyorRight": false
  }
}
```


## PUB017 Recipe Management System

Scan convention: Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

Initial state:

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

Caller bindings:

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

### PUB017.T1 CRUD

Add, query, modify, delete and reuse the first empty slot.

notes: Bind persistent recipe storage once. Inspect recipe[1].recipeID=2 after reuse; deleted non-ID fields are unconstrained.

**Step 0**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "error": false,
    "status": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "error": false,
    "status": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": true,
    "recipeIn": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeQueryResult": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "error": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": true,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.75,
      "productionTemperature": 90.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeModified": true,
    "error": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeModified": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": true,
    "recipeIn": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeQueryResult": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.75,
      "productionTemperature": 90.0
    }
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": true,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeDeleted": true,
    "error": false
  }
}
```

**Step 10**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeDeleted": false
  }
}
```

**Step 11**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 2,
      "ingredientType": 2,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "error": false
  }
}
```

**Step 12**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 13**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": true,
    "recipeIn": {
      "recipeID": 2,
      "ingredientType": 2,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeQueryResult": {
      "recipeID": 2,
      "ingredientType": 2,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    }
  }
}
```


### PUB017.T2 missing_duplicate

All missing-record errors and duplicate rejection preserve existing record.

**Step 0**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": true,
    "recipeIn": {
      "recipeID": 9,
      "ingredientType": 9,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "error": true,
    "status": 32769
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "error": false,
    "status": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": true,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 9,
      "ingredientType": 9,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "error": true,
    "status": 32772
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": true,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 9,
      "ingredientType": 9,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "error": true,
    "status": 32773
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "error": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.9,
      "productionTemperature": 100.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "error": true,
    "status": 32770,
    "recipeAdded": false
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 10**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": true,
    "recipeIn": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeQueryResult": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "error": false
  }
}
```


### PUB017.T3 capacity_priority

Fill ten slots; duplicate error has priority over full error.

**Step 0**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "status": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false,
    "status": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 2,
      "ingredientType": 2,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "status": 0
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false,
    "status": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 3,
      "ingredientType": 3,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "status": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false,
    "status": 0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 4,
      "ingredientType": 4,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "status": 0
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false,
    "status": 0
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 5,
      "ingredientType": 5,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "status": 0
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false,
    "status": 0
  }
}
```

**Step 10**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 6,
      "ingredientType": 6,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "status": 0
  }
}
```

**Step 11**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false,
    "status": 0
  }
}
```

**Step 12**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 7,
      "ingredientType": 7,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "status": 0
  }
}
```

**Step 13**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false,
    "status": 0
  }
}
```

**Step 14**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 8,
      "ingredientType": 8,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "status": 0
  }
}
```

**Step 15**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false,
    "status": 0
  }
}
```

**Step 16**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 9,
      "ingredientType": 9,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "status": 0
  }
}
```

**Step 17**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false,
    "status": 0
  }
}
```

**Step 18**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 10,
      "ingredientType": 10,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": true,
    "status": 0
  }
}
```

**Step 19**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "recipeAdded": false,
    "status": 0
  }
}
```

**Step 20**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 11,
      "ingredientType": 11,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "error": true,
    "status": 32771
  }
}
```

**Step 21**.

```json
{
  "inputs": {
    "addRecipe": false,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 0,
      "ingredientType": 0,
      "ingredientRatio": 0.0,
      "productionTemperature": 0.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 22**.

```json
{
  "inputs": {
    "addRecipe": true,
    "deleteRecipe": false,
    "modifyRecipe": false,
    "queryRecipe": false,
    "recipeIn": {
      "recipeID": 1,
      "ingredientType": 1,
      "ingredientRatio": 0.5,
      "productionTemperature": 80.0
    },
    "recipe": {
      "$binding": "recipe",
      "binding_id": "default",
      "retain_storage": true
    }
  },
  "expected": {
    "error": true,
    "status": 32770
  }
}
```


## PUB018 FIFO First-In-First-Out Queue

Scan convention: Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

Initial state:

```json
{
  "elementCount": 0,
  "status": 0,
  "head": 0,
  "tail": 0
}
```

Caller bindings:

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

### PUB018.T1 wrap_full_empty

Capacity-two FIFO preserves order through wrap, full and empty rejection.

binding_id: A

**Step 0**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 0,
    "status": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": 10,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 1
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": 99,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 1
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": 20,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 2
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": 30,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 2,
    "status": 32770,
    "item": 30
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": true,
    "reset": false,
    "item": -1,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 1,
    "status": 0,
    "item": 10
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 10**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": 30,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 2
  }
}
```

**Step 11**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 12**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": true,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 1,
    "item": 20
  }
}
```

**Step 13**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 14**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": true,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 0,
    "item": 30
  }
}
```

**Step 15**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 16**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": true,
    "reset": false,
    "item": 77,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 0,
    "status": 32769,
    "item": 77
  }
}
```


### PUB018.T2 reset_priority

Reset coincides with request; held request after reset does not execute.

binding_id: A

**Step 0**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": 10,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 1
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": true,
    "item": 20,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 0,
    "status": 0,
    "item": 20
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": 30,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 0,
    "status": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": 40,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 1
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": 0,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": true,
    "reset": true,
    "item": 50,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "A",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 0,
    "status": 0,
    "item": 50
  }
}
```


### PUB018.T3 generic_BOOL

Second element type and lower-bound-one buffer.

binding_id: B

**Step 0**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": true,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "B",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 1
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": false,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "B",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": false,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "B",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 2
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": false,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "B",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "enqueue": true,
    "dequeue": false,
    "reset": false,
    "item": true,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "B",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 3
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": false,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "B",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": true,
    "reset": false,
    "item": false,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "B",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 2,
    "item": true
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": false,
    "reset": false,
    "item": false,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "B",
      "retain_storage": true
    }
  },
  "expected": {
    "status": 0
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "enqueue": false,
    "dequeue": true,
    "reset": false,
    "item": true,
    "buffer": {
      "$binding": "buffer",
      "binding_id": "B",
      "retain_storage": true
    }
  },
  "expected": {
    "elementCount": 1,
    "item": false
  }
}
```


## PUB019 Mechanical Arm Control

Scan convention: Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

Initial state:

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

### PUB019.T1 manual_limits

Manual hold-to-run, reached limits, opposing requests and emergency priority.

**Step 0**.

```json
{
  "inputs": {
    "ManualMode": true,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": true,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": true,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "ManualMode": true,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": true,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "ManualMode": true,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "ManualMode": true,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": true,
    "UpButton": true,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "ManualMode": true,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": true,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": true,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "ManualMode": true,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": true,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": false,
    "RightLimitSwitch": true,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "ManualMode": true,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": true,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": true,
    "ActivateRelease": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "ManualMode": true,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": true,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": true,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "ManualMode": true,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": true,
    "ReleaseButton": true,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "ManualMode": true,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": false,
    "Start": false,
    "DownButton": true,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": true,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```


### PUB019.T2 single_step

Each new step requires a release and fresh start; held start cannot skip grip.

**Step 0**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": true,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": true,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": true,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": true,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": true,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": true,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": true,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": true,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": true,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": true,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": true,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": true,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": true,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": true,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": true,
    "ActivateRelease": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": true,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": true,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": true,
    "SingleCycleMode": false,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": true,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": true,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": true,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```


### PUB019.T3 single_cycle

All eight actions complete once and wait at top left.

**Step 0**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": true,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": true,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": true,
    "ActivateRelease": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": true,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": true,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": true,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": true,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": false,
    "RightLimitSwitch": true,
    "GripLimitSwitch": true,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": true,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": false,
    "RightLimitSwitch": true,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": true
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": false,
    "RightLimitSwitch": true,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": true,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": false,
    "RightLimitSwitch": true,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": true,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```


### PUB019.T4 continuous

The eighth completion wraps immediately to the first action.

**Step 0**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": true,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": true,
    "EmergencyStop": true,
    "Start": true,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": true,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": true,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": true,
    "ActivateRelease": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": true,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": true,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": true,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": true,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": true,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": true,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": true,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": false,
    "RightLimitSwitch": true,
    "GripLimitSwitch": true,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": true,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": true,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": false,
    "RightLimitSwitch": true,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": false
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": true
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": true,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": true,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": false,
    "RightLimitSwitch": true,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": true,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": true,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": false,
    "RightLimitSwitch": true,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": true,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": false,
    "ContinuousMode": true,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": true,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```


### PUB019.T5 emergency_reset

Emergency cancels an action; releasing emergency does not auto-restart.

**Step 0**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": true,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": true,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": false,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": false,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": false,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": false,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "ManualMode": false,
    "SingleStepMode": false,
    "SingleCycleMode": true,
    "ContinuousMode": false,
    "EmergencyStop": true,
    "Start": true,
    "DownButton": false,
    "UpButton": false,
    "LeftButton": false,
    "RightButton": false,
    "GripButton": false,
    "ReleaseButton": false,
    "DownLimitSwitch": false,
    "UpLimitSwitch": true,
    "LeftLimitSwitch": true,
    "RightLimitSwitch": false,
    "GripLimitSwitch": false,
    "ReleaseLimitSwitch": true
  },
  "expected": {
    "MoveDown": true,
    "MoveUp": false,
    "MoveLeft": false,
    "MoveRight": false,
    "ActivateGrip": false,
    "ActivateRelease": false
  }
}
```


## PUB020 Production Control

Scan convention: Inputs I[k] are sampled at invocation; outputs O[k] are observed after the call. Retained pre-state q[k] becomes q[k+1]. Each test resets the instance. A transition affects the same observed scan. dt_ms is elapsed time since the preceding invocation; the first invocation starts IEC timers at elapsed zero. CycleTime inputs, where supplied, are attributed to the current invocation rather than inferred from dt_ms.

Initial state:

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

### PUB020.T1 manual

Forward, reverse, both buttons and no request.

**Step 0**.

```json
{
  "inputs": {
    "Mode": false,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 0.0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": false,
    "ForwardButton": true,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": false,
    "ForwardButton": false,
    "ReverseButton": true,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": true,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Mode": false,
    "ForwardButton": true,
    "ReverseButton": true,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```


### PUB020.T2 qualified_100

Inclusive acceptance and linear firing setpoint for weight 100.0

**Step 0**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": true,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": true,
    "weight": 100.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 500.0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": true,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 500.0
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": true,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": true
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 500.0
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": true,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": true,
    "firingTemp": 500.0
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": true,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": true
  }
}
```

**Step 10**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 500.0
  }
}
```


### PUB020.T3 qualified_150

Inclusive acceptance and linear firing setpoint for weight 150.0

**Step 0**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": true,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": true,
    "weight": 150.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525.0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": true,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525.0
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": true,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": true
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525.0
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": true,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": true,
    "firingTemp": 525.0
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": true,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": true
  }
}
```

**Step 10**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525.0
  }
}
```


### PUB020.T4 qualified_200

Inclusive acceptance and linear firing setpoint for weight 200.0

**Step 0**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": true,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": true,
    "weight": 200.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 550.0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": true,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 550.0
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": true,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": true
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 550.0
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": true,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": true,
    "firingTemp": 550.0
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": true,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": true
  }
}
```

**Step 10**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 550.0
  }
}
```


### PUB020.T5 rejected_99_9

Reject just outside the inclusive limits, retain rejection until removal.

**Step 0**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": true,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": true,
    "weight": 99.9,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": true,
    "CompletionLight": false,
    "firingTemp": 0.0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": true,
    "CompletionLight": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": true,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```


### PUB020.T6 rejected_200_1

Reject just outside the inclusive limits, retain rejection until removal.

**Step 0**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": true,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": true,
    "weight": 200.1,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": true,
    "CompletionLight": false,
    "firingTemp": 0.0
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": true,
    "CompletionLight": false
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": true,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```


### PUB020.T7 wrong_feedback

Out-of-order completions do not move an idle product.

**Step 0**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": true,
    "weight": 0.0,
    "firingComplete": true
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": true,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": true,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": false,
    "weight": 0.0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false
  }
}
```


### V2_process_history_regression

Mode/edge reset, repeated station or prior-batch retained setpoint regression.

**Step 0**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": true,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 0
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": true,
    "weight": 150,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": true,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": true,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": true
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": true,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": true,
    "firingTemp": 525
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": true,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```

**Step 10**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```

**Step 11**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": true,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": true,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": true,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```

**Step 12**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```

**Step 13**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": true,
    "weight": 99.9,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": true,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```

**Step 14**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": true,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": true,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```

**Step 15**.

```json
{
  "inputs": {
    "Mode": true,
    "ForwardButton": false,
    "ReverseButton": false,
    "SensorFeed": false,
    "SensorWash": false,
    "SensorWeight": false,
    "SensorFiring": false,
    "SensorOutput": false,
    "washComplete": false,
    "weightComplete": false,
    "weight": 0,
    "firingComplete": false
  },
  "expected": {
    "MotorForward": false,
    "MotorReverse": false,
    "kick": false,
    "CompletionLight": false,
    "firingTemp": 525
  }
}
```


## SELF001 Guarded motor with retained run command

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "Run": false
}
```

### latch

Initialize, start, hold and stop

**Step 0**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "GuardClosed": true
  },
  "expected": {
    "Run": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "GuardClosed": true
  },
  "expected": {
    "Run": true
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "GuardClosed": true
  },
  "expected": {
    "Run": true
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": true,
    "GuardClosed": true
  },
  "expected": {
    "Run": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "GuardClosed": true
  },
  "expected": {
    "Run": false
  }
}
```


### priority

Simultaneous requests and guard recovery

**Step 0**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": true,
    "GuardClosed": true
  },
  "expected": {
    "Run": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "GuardClosed": false
  },
  "expected": {
    "Run": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "GuardClosed": true
  },
  "expected": {
    "Run": true
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "GuardClosed": false
  },
  "expected": {
    "Run": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "GuardClosed": true
  },
  "expected": {
    "Run": false
  }
}
```


## SELF002 Reversing jog drive with a neutral scan

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "previous_direction": 0,
  "Forward": false,
  "Reverse": false
}
```

### reverse

Direct reversal and held reverse request

**Step 0**.

```json
{
  "inputs": {
    "ForwardButton": true,
    "ReverseButton": false,
    "Stop": false
  },
  "expected": {
    "Forward": true,
    "Reverse": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "ForwardButton": false,
    "ReverseButton": true,
    "Stop": false
  },
  "expected": {
    "Forward": false,
    "Reverse": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "ForwardButton": false,
    "ReverseButton": true,
    "Stop": false
  },
  "expected": {
    "Forward": false,
    "Reverse": true
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "ForwardButton": true,
    "ReverseButton": false,
    "Stop": false
  },
  "expected": {
    "Forward": false,
    "Reverse": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "ForwardButton": true,
    "ReverseButton": false,
    "Stop": false
  },
  "expected": {
    "Forward": true,
    "Reverse": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "ForwardButton": false,
    "ReverseButton": false,
    "Stop": false
  },
  "expected": {
    "Forward": false,
    "Reverse": false
  }
}
```


### ambiguous

Both buttons and Stop override direction

**Step 0**.

```json
{
  "inputs": {
    "ForwardButton": true,
    "ReverseButton": true,
    "Stop": false
  },
  "expected": {
    "Forward": false,
    "Reverse": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "ForwardButton": true,
    "ReverseButton": false,
    "Stop": false
  },
  "expected": {
    "Forward": true,
    "Reverse": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "ForwardButton": true,
    "ReverseButton": false,
    "Stop": true
  },
  "expected": {
    "Forward": false,
    "Reverse": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "ForwardButton": false,
    "ReverseButton": true,
    "Stop": false
  },
  "expected": {
    "Forward": false,
    "Reverse": true
  }
}
```


## SELF003 Emergency stop reset with restart inhibition

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "Run": false,
  "ResetRequired": true
}
```

### reset_restart

Power-up inhibition, reset, run and emergency stop

**Step 0**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "EStopNC": true,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "ResetRequired": true
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "EStopNC": true,
    "Reset": true
  },
  "expected": {
    "Run": false,
    "ResetRequired": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "EStopNC": true,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "ResetRequired": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "EStopNC": true,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "ResetRequired": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "EStopNC": false,
    "Reset": true
  },
  "expected": {
    "Run": false,
    "ResetRequired": true
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "EStopNC": true,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "ResetRequired": true
  }
}
```


### invalid_reset

Held Start and Stop block reset

**Step 0**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "EStopNC": true,
    "Reset": true
  },
  "expected": {
    "Run": false,
    "ResetRequired": true
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": true,
    "EStopNC": true,
    "Reset": true
  },
  "expected": {
    "Run": false,
    "ResetRequired": true
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "EStopNC": true,
    "Reset": true
  },
  "expected": {
    "Run": false,
    "ResetRequired": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": true,
    "EStopNC": true,
    "Reset": true
  },
  "expected": {
    "Run": false,
    "ResetRequired": false
  }
}
```


### V2_omission_regression

Reject the concrete wrong behavior documented in the 2026-11-06 specification review.

**Step 0**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "EStopNC": true,
    "Reset": true
  },
  "expected": {
    "Run": false,
    "ResetRequired": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "EStopNC": true,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "ResetRequired": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "EStopNC": true,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "ResetRequired": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "EStopNC": true,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "ResetRequired": false
  }
}
```


## SELF004 Pallet indexing with a latched jam fault

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "state": "IDLE",
  "Belt": false,
  "Complete": false,
  "Fault": false
}
```

### index

One pallet and retained completion

**Step 0**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "AtExit": false,
    "Jam": false,
    "Reset": false
  },
  "expected": {
    "Belt": true,
    "Complete": false,
    "Fault": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "AtExit": false,
    "Jam": false,
    "Reset": false
  },
  "expected": {
    "Belt": true,
    "Complete": false,
    "Fault": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "AtExit": true,
    "Jam": false,
    "Reset": false
  },
  "expected": {
    "Belt": false,
    "Complete": true,
    "Fault": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "AtExit": false,
    "Jam": false,
    "Reset": false
  },
  "expected": {
    "Belt": false,
    "Complete": true,
    "Fault": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "AtExit": false,
    "Jam": false,
    "Reset": true
  },
  "expected": {
    "Belt": false,
    "Complete": false,
    "Fault": false
  }
}
```


### jam

Jam priority, retained fault and safe reset

**Step 0**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "AtExit": false,
    "Jam": false,
    "Reset": false
  },
  "expected": {
    "Belt": true,
    "Complete": false,
    "Fault": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "AtExit": false,
    "Jam": true,
    "Reset": true
  },
  "expected": {
    "Belt": false,
    "Complete": false,
    "Fault": true
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "AtExit": false,
    "Jam": false,
    "Reset": false
  },
  "expected": {
    "Belt": false,
    "Complete": false,
    "Fault": true
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "AtExit": false,
    "Jam": false,
    "Reset": true
  },
  "expected": {
    "Belt": false,
    "Complete": false,
    "Fault": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "AtExit": true,
    "Jam": false,
    "Reset": false
  },
  "expected": {
    "Belt": false,
    "Complete": false,
    "Fault": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": true,
    "AtExit": false,
    "Jam": false,
    "Reset": false
  },
  "expected": {
    "Belt": false,
    "Complete": false,
    "Fault": false
  }
}
```


## SELF005 Three phase signal with externally clocked durations

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "phase": 0,
  "elapsed_ticks": 0
}
```

### cycle

Full phase duration boundaries and pause

**Step 0**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": true
  },
  "expected": {
    "Red": true,
    "Green": false,
    "Amber": false,
    "Phase": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": false
  },
  "expected": {
    "Red": true,
    "Green": false,
    "Amber": false,
    "Phase": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": true
  },
  "expected": {
    "Red": false,
    "Green": true,
    "Amber": false,
    "Phase": 1
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": true
  },
  "expected": {
    "Red": false,
    "Green": true,
    "Amber": false,
    "Phase": 1
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": true
  },
  "expected": {
    "Red": false,
    "Green": true,
    "Amber": false,
    "Phase": 1
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": true
  },
  "expected": {
    "Red": false,
    "Green": false,
    "Amber": true,
    "Phase": 2
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": true
  },
  "expected": {
    "Red": true,
    "Green": false,
    "Amber": false,
    "Phase": 0
  }
}
```


### disable

Disable clears elapsed tick progress

**Step 0**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": true
  },
  "expected": {
    "Red": true,
    "Green": false,
    "Amber": false,
    "Phase": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": true
  },
  "expected": {
    "Red": false,
    "Green": true,
    "Amber": false,
    "Phase": 1
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Enable": false,
    "Tick": true
  },
  "expected": {
    "Red": true,
    "Green": false,
    "Amber": false,
    "Phase": 0
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": true
  },
  "expected": {
    "Red": true,
    "Green": false,
    "Amber": false,
    "Phase": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Enable": true,
    "Tick": true
  },
  "expected": {
    "Red": false,
    "Green": true,
    "Amber": false,
    "Phase": 1
  }
}
```


## SELF006 Tank filling with hysteresis and sensor inconsistency

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "Fill": false
}
```

### hysteresis

Fill cycle across both switching thresholds

**Step 0**.

```json
{
  "inputs": {
    "LowWet": false,
    "HighWet": false,
    "Inhibit": false
  },
  "expected": {
    "Fill": true,
    "SensorFault": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "LowWet": true,
    "HighWet": false,
    "Inhibit": false
  },
  "expected": {
    "Fill": true,
    "SensorFault": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "LowWet": true,
    "HighWet": true,
    "Inhibit": false
  },
  "expected": {
    "Fill": false,
    "SensorFault": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "LowWet": true,
    "HighWet": false,
    "Inhibit": false
  },
  "expected": {
    "Fill": false,
    "SensorFault": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "LowWet": false,
    "HighWet": false,
    "Inhibit": false
  },
  "expected": {
    "Fill": true,
    "SensorFault": false
  }
}
```


### fault_inhibit

Invalid switch pair and inhibit recovery

**Step 0**.

```json
{
  "inputs": {
    "LowWet": true,
    "HighWet": false,
    "Inhibit": false
  },
  "expected": {
    "Fill": false,
    "SensorFault": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "LowWet": false,
    "HighWet": true,
    "Inhibit": false
  },
  "expected": {
    "Fill": false,
    "SensorFault": true
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "LowWet": false,
    "HighWet": false,
    "Inhibit": false
  },
  "expected": {
    "Fill": true,
    "SensorFault": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "LowWet": true,
    "HighWet": false,
    "Inhibit": true
  },
  "expected": {
    "Fill": false,
    "SensorFault": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "LowWet": true,
    "HighWet": false,
    "Inhibit": false
  },
  "expected": {
    "Fill": false,
    "SensorFault": false
  }
}
```


## SELF007 Duty standby alternation with healthy pump fallback

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "LeadA": true,
  "previous_demand": false,
  "episode_served": false
}
```

### alternate

Served episodes alternate preference

**Step 0**.

```json
{
  "inputs": {
    "Demand": false,
    "FaultA": false,
    "FaultB": false
  },
  "expected": {
    "PumpA": false,
    "PumpB": false,
    "LeadA": true
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Demand": true,
    "FaultA": false,
    "FaultB": false
  },
  "expected": {
    "PumpA": true,
    "PumpB": false,
    "LeadA": true
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Demand": true,
    "FaultA": false,
    "FaultB": false
  },
  "expected": {
    "PumpA": true,
    "PumpB": false,
    "LeadA": true
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Demand": false,
    "FaultA": false,
    "FaultB": false
  },
  "expected": {
    "PumpA": false,
    "PumpB": false,
    "LeadA": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Demand": false,
    "FaultA": false,
    "FaultB": false
  },
  "expected": {
    "PumpA": false,
    "PumpB": false,
    "LeadA": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Demand": true,
    "FaultA": false,
    "FaultB": false
  },
  "expected": {
    "PumpA": false,
    "PumpB": true,
    "LeadA": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Demand": false,
    "FaultA": false,
    "FaultB": false
  },
  "expected": {
    "PumpA": false,
    "PumpB": false,
    "LeadA": true
  }
}
```


### fallback

Fault fallback, unserved episode and recovery

**Step 0**.

```json
{
  "inputs": {
    "Demand": true,
    "FaultA": true,
    "FaultB": true
  },
  "expected": {
    "PumpA": false,
    "PumpB": false,
    "LeadA": true
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Demand": false,
    "FaultA": true,
    "FaultB": true
  },
  "expected": {
    "PumpA": false,
    "PumpB": false,
    "LeadA": true
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Demand": true,
    "FaultA": true,
    "FaultB": false
  },
  "expected": {
    "PumpA": false,
    "PumpB": true,
    "LeadA": true
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Demand": true,
    "FaultA": false,
    "FaultB": false
  },
  "expected": {
    "PumpA": true,
    "PumpB": false,
    "LeadA": true
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Demand": false,
    "FaultA": true,
    "FaultB": true
  },
  "expected": {
    "PumpA": false,
    "PumpB": false,
    "LeadA": false
  }
}
```


### V2_omission_regression

Reject the concrete wrong behavior documented in the 2026-11-06 specification review.

**Step 0**.

```json
{
  "inputs": {
    "Demand": true,
    "FaultA": true,
    "FaultB": false
  },
  "expected": {
    "PumpA": false,
    "PumpB": true,
    "LeadA": true
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Demand": true,
    "FaultA": true,
    "FaultB": false
  },
  "expected": {
    "PumpA": false,
    "PumpB": true,
    "LeadA": true
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Demand": true,
    "FaultA": true,
    "FaultB": false
  },
  "expected": {
    "PumpA": false,
    "PumpB": true,
    "LeadA": true
  }
}
```


## SELF008 Consecutive scan qualification with an immediate trip

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "Count": 0,
  "Ready": false
}
```

### delay

Three scans qualify, hold saturates, trip clears

**Step 0**.

```json
{
  "inputs": {
    "Request": true,
    "Trip": false,
    "Preset": 3
  },
  "expected": {
    "Ready": false,
    "Count": 1
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Request": true,
    "Trip": false,
    "Preset": 3
  },
  "expected": {
    "Ready": false,
    "Count": 2
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Request": true,
    "Trip": false,
    "Preset": 3
  },
  "expected": {
    "Ready": true,
    "Count": 3
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Request": true,
    "Trip": false,
    "Preset": 3
  },
  "expected": {
    "Ready": true,
    "Count": 3
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Request": true,
    "Trip": true,
    "Preset": 3
  },
  "expected": {
    "Ready": false,
    "Count": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Request": true,
    "Trip": false,
    "Preset": 3
  },
  "expected": {
    "Ready": false,
    "Count": 1
  }
}
```


### bounds

Invalid presets and immediate reduced threshold

**Step 0**.

```json
{
  "inputs": {
    "Request": true,
    "Trip": false,
    "Preset": 0
  },
  "expected": {
    "Ready": false,
    "Count": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Request": true,
    "Trip": false,
    "Preset": 6
  },
  "expected": {
    "Ready": false,
    "Count": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Request": true,
    "Trip": false,
    "Preset": 5
  },
  "expected": {
    "Ready": false,
    "Count": 1
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Request": true,
    "Trip": false,
    "Preset": 1
  },
  "expected": {
    "Ready": true,
    "Count": 1
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Request": false,
    "Trip": false,
    "Preset": 5
  },
  "expected": {
    "Ready": false,
    "Count": 0
  }
}
```


## SELF009 Rising edge batch counter with reset sampling

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "Count": 0,
  "previous_pulse": false
}
```

### edges

Held pulses count once and target saturates

**Step 0**.

```json
{
  "inputs": {
    "PartPulse": false,
    "Reset": false,
    "Target": 2
  },
  "expected": {
    "Count": 0,
    "Complete": false,
    "Error": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "PartPulse": true,
    "Reset": false,
    "Target": 2
  },
  "expected": {
    "Count": 1,
    "Complete": false,
    "Error": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "PartPulse": true,
    "Reset": false,
    "Target": 2
  },
  "expected": {
    "Count": 1,
    "Complete": false,
    "Error": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "PartPulse": false,
    "Reset": false,
    "Target": 2
  },
  "expected": {
    "Count": 1,
    "Complete": false,
    "Error": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "PartPulse": true,
    "Reset": false,
    "Target": 2
  },
  "expected": {
    "Count": 2,
    "Complete": true,
    "Error": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "PartPulse": false,
    "Reset": false,
    "Target": 2
  },
  "expected": {
    "Count": 2,
    "Complete": true,
    "Error": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "PartPulse": true,
    "Reset": false,
    "Target": 2
  },
  "expected": {
    "Count": 2,
    "Complete": true,
    "Error": false
  }
}
```


### reset_edge

Reset while pulse is high suppresses phantom count

**Step 0**.

```json
{
  "inputs": {
    "PartPulse": true,
    "Reset": true,
    "Target": 1
  },
  "expected": {
    "Count": 0,
    "Complete": false,
    "Error": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "PartPulse": true,
    "Reset": false,
    "Target": 1
  },
  "expected": {
    "Count": 0,
    "Complete": false,
    "Error": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "PartPulse": false,
    "Reset": false,
    "Target": 1
  },
  "expected": {
    "Count": 0,
    "Complete": false,
    "Error": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "PartPulse": true,
    "Reset": false,
    "Target": 1
  },
  "expected": {
    "Count": 1,
    "Complete": true,
    "Error": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "PartPulse": true,
    "Reset": false,
    "Target": 0
  },
  "expected": {
    "Count": 0,
    "Complete": false,
    "Error": true
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "PartPulse": true,
    "Reset": false,
    "Target": 21
  },
  "expected": {
    "Count": 0,
    "Complete": false,
    "Error": true
  }
}
```


## SELF010 Latched alarm with acknowledgment and reannunciation

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "Alarm": false,
  "Acknowledged": false,
  "previous_fault": false
}
```

### annunciate

Acknowledge, fault clear and new event

**Step 0**.

```json
{
  "inputs": {
    "Fault": false,
    "Ack": false,
    "Reset": false
  },
  "expected": {
    "Alarm": false,
    "Acknowledged": false,
    "Horn": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Fault": true,
    "Ack": true,
    "Reset": false
  },
  "expected": {
    "Alarm": true,
    "Acknowledged": false,
    "Horn": true
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Fault": true,
    "Ack": true,
    "Reset": false
  },
  "expected": {
    "Alarm": true,
    "Acknowledged": true,
    "Horn": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Fault": false,
    "Ack": false,
    "Reset": false
  },
  "expected": {
    "Alarm": true,
    "Acknowledged": true,
    "Horn": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Fault": true,
    "Ack": false,
    "Reset": false
  },
  "expected": {
    "Alarm": true,
    "Acknowledged": false,
    "Horn": true
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Fault": false,
    "Ack": false,
    "Reset": true
  },
  "expected": {
    "Alarm": false,
    "Acknowledged": false,
    "Horn": false
  }
}
```


### reset_priority

Present fault blocks reset; removed fault reset wins

**Step 0**.

```json
{
  "inputs": {
    "Fault": true,
    "Ack": false,
    "Reset": true
  },
  "expected": {
    "Alarm": true,
    "Acknowledged": false,
    "Horn": true
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Fault": true,
    "Ack": true,
    "Reset": true
  },
  "expected": {
    "Alarm": true,
    "Acknowledged": true,
    "Horn": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Fault": false,
    "Ack": true,
    "Reset": true
  },
  "expected": {
    "Alarm": false,
    "Acknowledged": false,
    "Horn": false
  }
}
```


### V2_omission_regression

Reject the concrete wrong behavior documented in the 2026-11-06 specification review.

**Step 0**.

```json
{
  "inputs": {
    "Fault": true,
    "Ack": false,
    "Reset": true
  },
  "expected": {
    "Alarm": true,
    "Acknowledged": false,
    "Horn": true
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Fault": true,
    "Ack": true,
    "Reset": true
  },
  "expected": {
    "Alarm": true,
    "Acknowledged": true,
    "Horn": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Fault": true,
    "Ack": true,
    "Reset": true
  },
  "expected": {
    "Alarm": true,
    "Acknowledged": true,
    "Horn": false
  }
}
```


## SELF011 Single cycle actuator handshakes with one transition per scan

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "state": "IDLE",
  "all_commands": false
}
```

### handshake

Normal cycle and completion retention

**Step 0**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Reset": false,
    "ExtendDone": false,
    "ClampDone": false,
    "ReleaseDone": false,
    "RetractDone": false
  },
  "expected": {
    "Extend": false,
    "Clamp": false,
    "Release": false,
    "Retract": false,
    "Busy": false,
    "Done": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Reset": false,
    "ExtendDone": false,
    "ClampDone": false,
    "ReleaseDone": false,
    "RetractDone": true
  },
  "expected": {
    "Extend": true,
    "Clamp": false,
    "Release": false,
    "Retract": false,
    "Busy": true,
    "Done": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Reset": false,
    "ExtendDone": false,
    "ClampDone": false,
    "ReleaseDone": false,
    "RetractDone": false
  },
  "expected": {
    "Extend": true,
    "Clamp": false,
    "Release": false,
    "Retract": false,
    "Busy": true,
    "Done": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Reset": false,
    "ExtendDone": true,
    "ClampDone": false,
    "ReleaseDone": false,
    "RetractDone": false
  },
  "expected": {
    "Extend": false,
    "Clamp": true,
    "Release": false,
    "Retract": false,
    "Busy": true,
    "Done": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Reset": false,
    "ExtendDone": false,
    "ClampDone": true,
    "ReleaseDone": false,
    "RetractDone": false
  },
  "expected": {
    "Extend": false,
    "Clamp": false,
    "Release": true,
    "Retract": false,
    "Busy": true,
    "Done": false
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Reset": false,
    "ExtendDone": false,
    "ClampDone": false,
    "ReleaseDone": true,
    "RetractDone": false
  },
  "expected": {
    "Extend": false,
    "Clamp": false,
    "Release": false,
    "Retract": true,
    "Busy": true,
    "Done": false
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Reset": false,
    "ExtendDone": false,
    "ClampDone": false,
    "ReleaseDone": false,
    "RetractDone": true
  },
  "expected": {
    "Extend": false,
    "Clamp": false,
    "Release": false,
    "Retract": false,
    "Busy": false,
    "Done": true
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Reset": false,
    "ExtendDone": false,
    "ClampDone": false,
    "ReleaseDone": false,
    "RetractDone": false
  },
  "expected": {
    "Extend": false,
    "Clamp": false,
    "Release": false,
    "Retract": false,
    "Busy": false,
    "Done": true
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Reset": true,
    "ExtendDone": false,
    "ClampDone": false,
    "ReleaseDone": false,
    "RetractDone": false
  },
  "expected": {
    "Extend": false,
    "Clamp": false,
    "Release": false,
    "Retract": false,
    "Busy": false,
    "Done": false
  }
}
```


### single_transition

All handshakes cannot skip states; Stop aborts

**Step 0**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Reset": false,
    "ExtendDone": true,
    "ClampDone": true,
    "ReleaseDone": true,
    "RetractDone": true
  },
  "expected": {
    "Extend": true,
    "Clamp": false,
    "Release": false,
    "Retract": false,
    "Busy": true,
    "Done": false
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Reset": false,
    "ExtendDone": true,
    "ClampDone": true,
    "ReleaseDone": true,
    "RetractDone": true
  },
  "expected": {
    "Extend": false,
    "Clamp": true,
    "Release": false,
    "Retract": false,
    "Busy": true,
    "Done": false
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Reset": false,
    "ExtendDone": true,
    "ClampDone": true,
    "ReleaseDone": true,
    "RetractDone": true
  },
  "expected": {
    "Extend": false,
    "Clamp": false,
    "Release": true,
    "Retract": false,
    "Busy": true,
    "Done": false
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": true,
    "Reset": false,
    "ExtendDone": true,
    "ClampDone": true,
    "ReleaseDone": true,
    "RetractDone": true
  },
  "expected": {
    "Extend": false,
    "Clamp": false,
    "Release": false,
    "Retract": false,
    "Busy": false,
    "Done": false
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Reset": true,
    "ExtendDone": true,
    "ClampDone": true,
    "ReleaseDone": true,
    "RetractDone": true
  },
  "expected": {
    "Extend": false,
    "Clamp": false,
    "Release": false,
    "Retract": false,
    "Busy": false,
    "Done": false
  }
}
```


## SELF012 Bounded automatic fault retries with a recovery dwell

Scan convention: At scan k, sample every input once, read retained pre-state q[k], execute one transition, and observe outputs O[k] at the end of that same scan. Updated state becomes q[k+1]. Reset the instance before each test. Step 0 executes normally; initial conditions describe pre-state, not an extra delayed scan. All timing in this task is explicitly counted in invocations, not wall time.

Initial state:

```json
{
  "state": "IDLE",
  "Attempts": 0,
  "recovery_free_scans": 0
}
```

### exhaustion

Two automatic retries then third fault locks

**Step 0**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "Locked": false,
    "Attempts": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": true,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 0
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "Locked": false,
    "Attempts": 1
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": true,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 1
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 1
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "Locked": false,
    "Attempts": 2
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": true,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": true,
    "Attempts": 2
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": true,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": true,
    "Attempts": 2
  }
}
```

**Step 9**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Fault": false,
    "Reset": true
  },
  "expected": {
    "Run": false,
    "Locked": true,
    "Attempts": 2
  }
}
```

**Step 10**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": true
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 0
  }
}
```


### dwell_interrupt

Fault interrupts healthy dwell; Stop aborts wait

**Step 0**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "Locked": false,
    "Attempts": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": true,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 0
  }
}
```

**Step 3**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": true,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 0
  }
}
```

**Step 4**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 0
  }
}
```

**Step 5**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "Locked": false,
    "Attempts": 1
  }
}
```

**Step 6**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": true,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 1
  }
}
```

**Step 7**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": true,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 1
  }
}
```

**Step 8**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": false,
    "Locked": false,
    "Attempts": 1
  }
}
```


### V2_omission_regression

Reject the concrete wrong behavior documented in the 2026-11-06 specification review.

**Step 0**.

```json
{
  "inputs": {
    "Start": true,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "Locked": false,
    "Attempts": 0
  }
}
```

**Step 1**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "Locked": false,
    "Attempts": 0
  }
}
```

**Step 2**.

```json
{
  "inputs": {
    "Start": false,
    "Stop": false,
    "Fault": false,
    "Reset": false
  },
  "expected": {
    "Run": true,
    "Locked": false,
    "Attempts": 0
  }
}
```

