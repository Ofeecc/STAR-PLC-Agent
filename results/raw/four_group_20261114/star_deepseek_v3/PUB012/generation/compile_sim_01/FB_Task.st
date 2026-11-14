FUNCTION_BLOCK FB_Task
VAR_INPUT
    THICKNESS_FAULT : BOOL;
    THICKNESS_SIGNAL_VALID : BOOL;
    CUTTING_RUN : BOOL;
    FaultTimestamp : DINT;
    CycleTime : TIME;
END_VAR
VAR_OUTPUT
    THICKNESS_ALARM : BOOL := FALSE;
    Slab_Fault_Counter : UINT := 0;
    Slab_Runtime_Accumulator : LTIME := LTIME#0ns;
    Slab_Fault_History : ARRAY[0..4] OF DINT := [0,0,0,0,0];
END_VAR
VAR
    prevValidFault : BOOL := FALSE;
    holdActive : BOOL := FALSE;
    holdRestart : BOOL := FALSE;
    validFault : BOOL := FALSE;
    validFaultRise : BOOL := FALSE;
    FaultCounter_Int : UINT := 0;
    RuntimeAccumulator_Int : LTIME := LTIME#0ns;
    FaultHistory_Int : ARRAY[0..4] OF DINT := [0,0,0,0,0];
    AlarmHoldTimer : TON;
    holdBase : TIME := T#0ms;
    holdElapsed : TIME;
    timeConv : U_TIME_MS;
    i : INT;
END_VAR

// Stage 1: edge sampling
holdRestart := FALSE;
validFault := THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT;
validFaultRise := validFault AND NOT prevValidFault;

// Stage 2: safety/reset priority and state transitions
IF NOT THICKNESS_SIGNAL_VALID THEN
    holdActive := FALSE;
    holdRestart := FALSE;
    prevValidFault := FALSE;
    // Statistics and history are preserved.
ELSE
    IF validFaultRise THEN
        FaultCounter_Int := FaultCounter_Int + 1;
        FaultHistory_Int[4] := FaultHistory_Int[3];
        FaultHistory_Int[3] := FaultHistory_Int[2];
        FaultHistory_Int[2] := FaultHistory_Int[1];
        FaultHistory_Int[1] := FaultHistory_Int[0];
        FaultHistory_Int[0] := FaultTimestamp;
        holdActive := TRUE;
        holdRestart := TRUE;
    END_IF;

    IF (NOT THICKNESS_FAULT) AND CUTTING_RUN THEN
        timeConv.t := CycleTime;
        RuntimeAccumulator_Int := RuntimeAccumulator_Int + (LTIME#1ms * timeConv.ms);
    END_IF;

    prevValidFault := validFault;
END_IF;

// Stage 3: unconditional timer call
AlarmHoldTimer(IN := THICKNESS_SIGNAL_VALID AND holdActive, PT := T#49d);

// Stage 4: hold restart and expiration handling
IF holdRestart THEN
    holdBase := AlarmHoldTimer.ET;
    holdRestart := FALSE;
END_IF;

IF holdActive THEN
    holdElapsed := AlarmHoldTimer.ET - holdBase;
    IF holdElapsed >= T#500ms THEN
        holdActive := FALSE;
    END_IF;
END_IF;

// Stage 5: unified outputs
THICKNESS_ALARM := THICKNESS_SIGNAL_VALID AND (THICKNESS_FAULT OR holdActive);
Slab_Fault_Counter := FaultCounter_Int;
Slab_Runtime_Accumulator := RuntimeAccumulator_Int;
FOR i := 0 TO 4 DO
    Slab_Fault_History[i] := FaultHistory_Int[i];
END_FOR;
END_FUNCTION_BLOCK
