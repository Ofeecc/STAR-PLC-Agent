FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    Fault : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Run : BOOL;
    Locked : BOOL;
    Attempts : USINT;
END_VAR
VAR
    State : E_State := E_State.IDLE;
    RecoveryFree : USINT := 0;
END_VAR

IF Reset AND NOT Fault AND NOT Start THEN
    State := E_State.IDLE;
    Attempts := 0;
    RecoveryFree := 0;
ELSIF State = E_State.LOCKED THEN
    ;
ELSIF Stop THEN
    State := E_State.IDLE;
    RecoveryFree := 0;
ELSIF State = E_State.RUNNING AND Fault THEN
    IF Attempts < 2 THEN
        State := E_State.WAIT;
        RecoveryFree := 0;
    ELSE
        State := E_State.LOCKED;
    END_IF
ELSIF State = E_State.WAIT AND Fault THEN
    RecoveryFree := 0;
ELSIF State = E_State.WAIT AND NOT Fault THEN
    IF RecoveryFree >= 1 THEN
        State := E_State.RUNNING;
        Attempts := Attempts + 1;
        RecoveryFree := 0;
    ELSE
        RecoveryFree := RecoveryFree + 1;
    END_IF
ELSIF State = E_State.IDLE AND Start AND NOT Fault THEN
    State := E_State.RUNNING;
    RecoveryFree := 0;
END_IF

Run := (State = E_State.RUNNING);
Locked := (State = E_State.LOCKED);
END_FUNCTION_BLOCK
