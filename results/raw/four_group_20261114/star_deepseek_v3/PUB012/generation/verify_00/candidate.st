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
        RuntimeAccumulator_Int := RuntimeAccumulator_Int + TIME_TO_LTIME(CycleTime);
    END_IF;

    IF (NOT THICKNESS_FAULT) AND AlarmHoldTimer.Q THEN
        holdActive := FALSE;
    END_IF;

    prevValidFault := validFault;
END_IF;

// Stage 3: unconditional timer call
AlarmHoldTimer(IN := THICKNESS_SIGNAL_VALID AND holdActive AND NOT holdRestart, PT := T#500ms);

// Stage 4: unified outputs
THICKNESS_ALARM := THICKNESS_SIGNAL_VALID AND (THICKNESS_FAULT OR (holdActive AND NOT AlarmHoldTimer.Q));
Slab_Fault_Counter := FaultCounter_Int;
Slab_Runtime_Accumulator := RuntimeAccumulator_Int;
FOR i := 0 TO 4 DO
    Slab_Fault_History[i] := FaultHistory_Int[i];
END_FOR;
END_FUNCTION_BLOCK
