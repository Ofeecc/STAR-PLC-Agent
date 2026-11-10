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
    Slab_Runtime_Accumulator : LTIME := LTIME#0NS;
    Slab_Fault_History : ARRAY[0..4] OF DINT := [0, 0, 0, 0, 0];
END_VAR
VAR
    xPreviousValidFault : BOOL := FALSE;
    xHoldActive : BOOL := FALSE;
    tonAlarmHold : TON;
END_VAR

IF NOT THICKNESS_SIGNAL_VALID THEN
    THICKNESS_ALARM := FALSE;
    xHoldActive := FALSE;
    tonAlarmHold(IN := FALSE, PT := T#500MS);
ELSE
    IF THICKNESS_FAULT AND NOT xPreviousValidFault THEN
        Slab_Fault_Counter := Slab_Fault_Counter + 1;
        Slab_Fault_History[4] := Slab_Fault_History[3];
        Slab_Fault_History[3] := Slab_Fault_History[2];
        Slab_Fault_History[2] := Slab_Fault_History[1];
        Slab_Fault_History[1] := Slab_Fault_History[0];
        Slab_Fault_History[0] := FaultTimestamp;

        xHoldActive := TRUE;
        tonAlarmHold(IN := FALSE, PT := T#500MS);
    END_IF;

    IF xHoldActive THEN
        tonAlarmHold(IN := TRUE, PT := T#500MS);
        IF tonAlarmHold.Q THEN
            xHoldActive := FALSE;
        END_IF;
    ELSE
        tonAlarmHold(IN := FALSE, PT := T#500MS);
    END_IF;

    THICKNESS_ALARM := THICKNESS_FAULT OR xHoldActive;
END_IF;

IF THICKNESS_SIGNAL_VALID AND NOT THICKNESS_FAULT AND CUTTING_RUN THEN
    Slab_Runtime_Accumulator := Slab_Runtime_Accumulator + TIME_TO_LTIME(CycleTime);
END_IF;

xPreviousValidFault := THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT;
END_FUNCTION_BLOCK
