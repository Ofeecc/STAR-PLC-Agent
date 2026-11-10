FUNCTION_BLOCK FB_Task
VAR_INPUT
    THICKNESS_FAULT : BOOL;
    THICKNESS_SIGNAL_VALID : BOOL;
    CUTTING_RUN : BOOL;
    FaultTimestamp : DINT;
    CycleTime : TIME;
END_VAR
VAR_OUTPUT
    THICKNESS_ALARM : BOOL;
    Slab_Fault_Counter : UINT;
    Slab_Runtime_Accumulator : LTIME;
    Slab_Fault_History : ARRAY[0..4] OF DINT;
END_VAR
VAR
    prevValidFault : BOOL;
    holdActive : BOOL;
    holdTimer : TON;
    i : INT;
END_VAR

IF NOT THICKNESS_SIGNAL_VALID THEN
    THICKNESS_ALARM := FALSE;
    holdActive := FALSE;
    holdTimer(IN := FALSE);
    prevValidFault := FALSE;
ELSE
    IF THICKNESS_FAULT AND NOT prevValidFault THEN
        Slab_Fault_Counter := Slab_Fault_Counter + 1;
        FOR i := 4 TO 1 BY -1 DO
            Slab_Fault_History[i] := Slab_Fault_History[i - 1];
        END_FOR
        Slab_Fault_History[0] := FaultTimestamp;
        holdActive := TRUE;
        holdTimer(IN := FALSE);
    ELSE
        holdTimer(IN := holdActive);
        IF holdTimer.Q THEN
            holdActive := FALSE;
        END_IF
    END_IF

    THICKNESS_ALARM := THICKNESS_FAULT OR holdActive;

    IF CUTTING_RUN AND NOT THICKNESS_FAULT THEN
        Slab_Runtime_Accumulator := Slab_Runtime_Accumulator + TO_LTIME(CycleTime);
    END_IF

    prevValidFault := THICKNESS_FAULT;
END_IF
END_FUNCTION_BLOCK
