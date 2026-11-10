FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    EStopNC : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Run : BOOL := FALSE;
    ResetRequired : BOOL := TRUE;
END_VAR

IF NOT EStopNC THEN
    Run := FALSE;
    ResetRequired := TRUE;
ELSIF ResetRequired THEN
    Run := FALSE;
    IF Reset AND NOT Start AND NOT Stop THEN
        ResetRequired := FALSE;
    ELSE
        ResetRequired := TRUE;
    END_IF;
ELSE
    IF Stop THEN
        Run := FALSE;
    ELSIF Start THEN
        Run := TRUE;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
