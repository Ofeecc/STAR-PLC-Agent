FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    GuardClosed : BOOL;
END_VAR
VAR_OUTPUT
    Run : BOOL := FALSE;
END_VAR


Run := FALSE;
END_FUNCTION_BLOCK
