FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    GuardClosed : BOOL;
END_VAR
VAR_OUTPUT
    Run : BOOL;
END_VAR
VAR
    qRun : BOOL := FALSE;
    first : BOOL := TRUE;
END_VAR

IF first THEN
    qRun := FALSE;
    first := FALSE;
END_IF

IF Stop OR NOT GuardClosed THEN
    Run := FALSE;
ELSIF Start THEN
    Run := TRUE;
ELSE
    Run := qRun;
END_IF

qRun := Run;
END_FUNCTION_BLOCK
