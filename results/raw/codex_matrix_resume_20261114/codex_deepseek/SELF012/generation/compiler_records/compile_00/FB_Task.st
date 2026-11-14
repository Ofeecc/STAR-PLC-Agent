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
    mode : E_Mode := E_Mode.IDLE;
    free_scans : USINT := 0;
END_VAR

IF Reset AND NOT Fault AND NOT Start THEN
    mode := E_Mode.IDLE;
    Attempts := 0;
    free_scans := 0;
ELSIF mode = E_Mode.LOCKED THEN
    mode := E_Mode.LOCKED;
ELSIF Stop THEN
    mode := E_Mode.IDLE;
    free_scans := 0;
ELSE
    CASE mode OF
        E_Mode.RUNNING:
            IF Fault THEN
                IF Attempts >= 2 THEN
                    mode := E_Mode.LOCKED;
                    free_scans := 0;
                ELSE
                    mode := E_Mode.WAIT;
                    free_scans := 0;
                END_IF
            END_IF

        E_Mode.WAIT:
            IF Fault THEN
                free_scans := 0;
            ELSE
                IF free_scans < 2 THEN
                    free_scans := free_scans + 1;
                END_IF
                IF free_scans >= 2 THEN
                    IF Attempts < 2 THEN
                        Attempts := Attempts + 1;
                    END_IF
                    free_scans := 0;
                    mode := E_Mode.RUNNING;
                END_IF
            END_IF

        E_Mode.IDLE:
            IF Start AND NOT Fault THEN
                mode := E_Mode.RUNNING;
            END_IF

        E_Mode.LOCKED:
            mode := E_Mode.LOCKED;
    END_CASE
END_IF

Run := (mode = E_Mode.RUNNING);
Locked := (mode = E_Mode.LOCKED);
END_FUNCTION_BLOCK
