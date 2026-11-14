FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    GuardClosed : BOOL;
END_VAR
VAR_OUTPUT
    Run : BOOL := FALSE;
END_VAR
VAR
    running : BOOL := FALSE;
END_VAR

IF Stop OR NOT GuardClosed THEN
    running := FALSE;
ELSIF Start THEN
    running := TRUE;
END_IF;

Run := running;
END_FUNCTION_BLOCK
