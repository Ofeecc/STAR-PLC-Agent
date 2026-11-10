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
    Attempts : USINT := 0;
END_VAR
VAR
    State : USINT := 0;
    RecoveryFreeScans : USINT := 0;
END_VAR
VAR CONSTANT
    STATE_IDLE : USINT := 0;
    STATE_RUNNING : USINT := 1;
    STATE_WAIT : USINT := 2;
    STATE_LOCKED : USINT := 3;
END_VAR

IF Reset AND NOT Fault AND NOT Start THEN
    State := STATE_IDLE;
    Attempts := 0;
    RecoveryFreeScans := 0;
ELSIF State = STATE_LOCKED THEN
    RecoveryFreeScans := 0;
ELSIF Stop THEN
    State := STATE_IDLE;
    RecoveryFreeScans := 0;
ELSIF (State = STATE_RUNNING) AND Fault THEN
    RecoveryFreeScans := 0;
    IF Attempts < 2 THEN
        State := STATE_WAIT;
    ELSE
        State := STATE_LOCKED;
    END_IF;
ELSIF State = STATE_WAIT THEN
    IF Fault THEN
        RecoveryFreeScans := 0;
    ELSIF RecoveryFreeScans >= 1 THEN
        Attempts := Attempts + 1;
        RecoveryFreeScans := 0;
        State := STATE_RUNNING;
    ELSE
        RecoveryFreeScans := 1;
    END_IF;
ELSIF (State = STATE_IDLE) AND Start AND NOT Fault THEN
    State := STATE_RUNNING;
    RecoveryFreeScans := 0;
END_IF;

Run := State = STATE_RUNNING;
Locked := State = STATE_LOCKED;
END_FUNCTION_BLOCK
