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
    Slab_Fault_History : ARRAY[0..4] OF DINT := [0, 0, 0, 0, 0];
END_VAR
VAR
    PreviousFault : BOOL := FALSE;
    HoldActive : BOOL := FALSE;
    HoldTimer : TON;
    HistoryInternal : ARRAY[0..4] OF DINT := [0, 0, 0, 0, 0];
END_VAR

IF NOT THICKNESS_SIGNAL_VALID THEN
    THICKNESS_ALARM := FALSE;
    PreviousFault := FALSE;
    HoldActive := FALSE;
    HoldTimer(IN := FALSE, PT := T#500ms);
ELSE
    IF THICKNESS_FAULT AND NOT PreviousFault THEN
        Slab_Fault_Counter := Slab_Fault_Counter + 1;
        HistoryInternal[4] := HistoryInternal[3];
        HistoryInternal[3] := HistoryInternal[2];
        HistoryInternal[2] := HistoryInternal[1];
        HistoryInternal[1] := HistoryInternal[0];
        HistoryInternal[0] := FaultTimestamp;
        HoldTimer(IN := FALSE, PT := T#500ms);
        HoldActive := TRUE;
    END_IF;

    IF HoldActive THEN
        HoldTimer(IN := TRUE, PT := T#500ms);
        IF HoldTimer.Q THEN
            HoldActive := FALSE;
        END_IF;
    ELSE
        HoldTimer(IN := FALSE, PT := T#500ms);
    END_IF;

    THICKNESS_ALARM := THICKNESS_FAULT OR HoldActive;
    PreviousFault := THICKNESS_FAULT;
END_IF;

IF THICKNESS_SIGNAL_VALID AND NOT THICKNESS_FAULT AND CUTTING_RUN AND (CycleTime > T#0ms) THEN
    Slab_Runtime_Accumulator := Slab_Runtime_Accumulator + TIME_TO_LTIME(CycleTime);
END_IF;

Slab_Fault_History[0] := HistoryInternal[0];
Slab_Fault_History[1] := HistoryInternal[1];
Slab_Fault_History[2] := HistoryInternal[2];
Slab_Fault_History[3] := HistoryInternal[3];
Slab_Fault_History[4] := HistoryInternal[4];
END_FUNCTION_BLOCK
