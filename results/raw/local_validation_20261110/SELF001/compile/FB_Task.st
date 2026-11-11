FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    GuardClosed : BOOL;
END_VAR
VAR_OUTPUT
    Run : BOOL := FALSE;
END_VAR


IF Stop OR NOT GuardClosed THEN
    Run := FALSE;
ELSIF Start THEN
    Run := TRUE;
END_IF;

END_FUNCTION_BLOCK
