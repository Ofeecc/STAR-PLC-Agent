FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    Fault : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Run : BOOL := FALSE;
    Locked : BOOL := FALSE;
    Attempts : USINT := 0;
END_VAR
VAR
    State : E_TaskState := E_TaskState.IDLE;
    RecoveryFreeScans : USINT := 0;
END_VAR

IF Reset AND NOT Fault AND NOT Start THEN
    State := E_TaskState.IDLE;
    Attempts := 0;
    RecoveryFreeScans := 0;
ELSIF State = E_TaskState.LOCKED THEN
    RecoveryFreeScans := 0;
ELSIF Stop THEN
    State := E_TaskState.IDLE;
    RecoveryFreeScans := 0;
ELSIF (State = E_TaskState.RUNNING) AND Fault THEN
    IF Attempts < 2 THEN
        State := E_TaskState.WAIT;
        RecoveryFreeScans := 0;
    ELSE
        State := E_TaskState.LOCKED;
        RecoveryFreeScans := 0;
    END_IF
ELSIF State = E_TaskState.WAIT THEN
    IF Fault THEN
        RecoveryFreeScans := 0;
    ELSIF RecoveryFreeScans >= 1 THEN
        Attempts := Attempts + 1;
        State := E_TaskState.RUNNING;
        RecoveryFreeScans := 0;
    ELSE
        RecoveryFreeScans := RecoveryFreeScans + 1;
    END_IF
ELSIF State = E_TaskState.IDLE THEN
    IF Start AND NOT Fault THEN
        State := E_TaskState.RUNNING;
        RecoveryFreeScans := 0;
    END_IF
END_IF

Run := (State = E_TaskState.RUNNING) AND NOT Fault;
Locked := (State = E_TaskState.LOCKED);
END_FUNCTION_BLOCK
