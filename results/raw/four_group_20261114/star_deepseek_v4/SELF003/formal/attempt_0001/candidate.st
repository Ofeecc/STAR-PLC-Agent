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
VAR
    bPrevRun : BOOL;
    bPrevResetRequired : BOOL;
    bNextRun : BOOL;
    bNextResetRequired : BOOL;
END_VAR

bPrevRun := Run;
bPrevResetRequired := ResetRequired;

IF NOT EStopNC THEN
    bNextRun := FALSE;
    bNextResetRequired := TRUE;
ELSIF bPrevResetRequired THEN
    bNextRun := FALSE;
    IF Reset AND NOT Start AND NOT Stop THEN
        bNextResetRequired := FALSE;
    ELSE
        bNextResetRequired := TRUE;
    END_IF;
ELSE
    bNextResetRequired := FALSE;
    IF Stop THEN
        bNextRun := FALSE;
    ELSIF Start THEN
        bNextRun := TRUE;
    ELSE
        bNextRun := bPrevRun;
    END_IF;
END_IF;

Run := bNextRun;
ResetRequired := bNextResetRequired;
END_FUNCTION_BLOCK
