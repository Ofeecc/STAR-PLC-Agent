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
    state : USINT := 0;
    previous_valid_fault : BOOL := FALSE;
    valid_fault : BOOL := FALSE;
    rise : BOOL := FALSE;
    select_A : BOOL := FALSE;
    hold_active : BOOL := FALSE;
    HoldA : TON;
    HoldB : TON;
    fault_count : UINT := 0;
    runtime : LTIME := LTIME#0ns;
    history : ARRAY[0..4] OF DINT := [0, 0, 0, 0, 0];
    i : INT;
END_VAR
VAR CONSTANT
    STATE_INHIBITED : USINT := 0;
    STATE_READY : USINT := 1;
    STATE_TRACKING : USINT := 2;
END_VAR

valid_fault := THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT;
rise := valid_fault AND NOT previous_valid_fault;
previous_valid_fault := valid_fault;

IF NOT THICKNESS_SIGNAL_VALID THEN
    state := STATE_INHIBITED;
ELSIF rise THEN
    state := STATE_TRACKING;
    select_A := NOT select_A;
    fault_count := fault_count + UINT#1;
    FOR i := 4 TO 1 BY -1 DO
        history[i] := history[i - 1];
    END_FOR;
    history[0] := FaultTimestamp;
ELSIF state = STATE_INHIBITED THEN
    state := STATE_READY;
END_IF;

IF THICKNESS_SIGNAL_VALID AND NOT THICKNESS_FAULT AND CUTTING_RUN AND (CycleTime > T#0ms) THEN
    runtime := runtime + TIME_TO_LTIME(CycleTime);
END_IF;

HoldA(IN := THICKNESS_SIGNAL_VALID AND (state = STATE_TRACKING) AND select_A, PT := T#500ms);
HoldB(IN := THICKNESS_SIGNAL_VALID AND (state = STATE_TRACKING) AND NOT select_A, PT := T#500ms);

hold_active := (state = STATE_TRACKING) AND
    ((select_A AND NOT HoldA.Q) OR (NOT select_A AND NOT HoldB.Q));
THICKNESS_ALARM := THICKNESS_SIGNAL_VALID AND (THICKNESS_FAULT OR hold_active);
Slab_Fault_Counter := fault_count;
Slab_Runtime_Accumulator := runtime;
FOR i := 0 TO 4 DO
    Slab_Fault_History[i] := history[i];
END_FOR;
END_FUNCTION_BLOCK
