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
    State : E_TaskState := TASK_IDLE;
    RecoveryFreeScans : USINT := 0;
END_VAR

IF Reset AND NOT Fault AND NOT Start THEN
    State := TASK_IDLE;
    Attempts := 0;
    RecoveryFreeScans := 0;
ELSIF State = TASK_LOCKED THEN
    RecoveryFreeScans := 0;
ELSIF Stop THEN
    State := TASK_IDLE;
    RecoveryFreeScans := 0;
ELSE
    CASE State OF
        TASK_IDLE:
            RecoveryFreeScans := 0;
            IF Start AND NOT Fault THEN
                State := TASK_RUNNING;
            END_IF;
        TASK_RUNNING:
            IF Fault THEN
                RecoveryFreeScans := 0;
                IF Attempts < 2 THEN
                    State := TASK_WAIT;
                ELSE
                    State := TASK_LOCKED;
                END_IF;
            END_IF;
        TASK_WAIT:
            IF Fault THEN
                RecoveryFreeScans := 0;
            ELSIF RecoveryFreeScans >= 1 THEN
                Attempts := Attempts + 1;
                RecoveryFreeScans := 0;
                State := TASK_RUNNING;
            ELSE
                RecoveryFreeScans := 1;
            END_IF;
        TASK_LOCKED:
            RecoveryFreeScans := 0;
    END_CASE;
END_IF;

Run := (State = TASK_RUNNING);
Locked := (State = TASK_LOCKED);
END_FUNCTION_BLOCK
