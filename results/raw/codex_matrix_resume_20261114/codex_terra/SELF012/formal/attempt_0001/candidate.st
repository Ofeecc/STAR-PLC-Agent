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
    mode : USINT := 0;
    free_scans : USINT := 0;
END_VAR

IF Reset AND NOT Fault AND NOT Start THEN
    mode := 0;
    Attempts := 0;
    free_scans := 0;
ELSIF mode = 3 THEN
    mode := 3;
ELSIF Stop THEN
    mode := 0;
    free_scans := 0;
ELSE
    CASE mode OF
        0:
            IF Start AND NOT Fault THEN
                mode := 1;
            END_IF;
        1:
            IF Fault THEN
                IF Attempts >= 2 THEN
                    mode := 3;
                ELSE
                    mode := 2;
                    free_scans := 0;
                END_IF;
            END_IF;
        2:
            IF Fault THEN
                free_scans := 0;
            ELSE
                free_scans := free_scans + 1;
                IF free_scans >= 2 THEN
                    Attempts := Attempts + 1;
                    free_scans := 0;
                    mode := 1;
                END_IF;
            END_IF;
    END_CASE;
END_IF;
Run := mode = 1;
Locked := mode = 3;
END_FUNCTION_BLOCK
