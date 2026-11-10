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
    State : E_TaskState := IDLE;
    RecoveryFreeScans : USINT := 0;
END_VAR

IF Reset AND NOT Fault AND NOT Start THEN
    State := IDLE;
    Attempts := 0;
    RecoveryFreeScans := 0;
ELSIF State = LOCKED THEN
    RecoveryFreeScans := 0;
ELSIF Stop THEN
    State := IDLE;
    RecoveryFreeScans := 0;
ELSE
    CASE State OF
        IDLE:
            RecoveryFreeScans := 0;
            IF Start AND NOT Fault THEN
                State := RUNNING;
            END_IF;
        RUNNING:
            IF Fault THEN
                RecoveryFreeScans := 0;
                IF Attempts < 2 THEN
                    State := WAIT;
                ELSE
                    State := LOCKED;
                END_IF;
            END_IF;
        WAIT:
            IF Fault THEN
                RecoveryFreeScans := 0;
            ELSIF RecoveryFreeScans >= 1 THEN
                Attempts := Attempts + 1;
                RecoveryFreeScans := 0;
                State := RUNNING;
            ELSE
                RecoveryFreeScans := 1;
            END_IF;
    END_CASE;
END_IF;

Run := State = RUNNING;
Locked := State = LOCKED;
END_FUNCTION_BLOCK
