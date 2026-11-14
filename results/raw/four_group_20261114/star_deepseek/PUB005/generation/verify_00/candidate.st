FUNCTION_BLOCK FB_Task
VAR_INPUT
    Gap_Exceeded : BOOL;
    Weld_E_Stop_NC : BOOL;
    DebounceTime : TIME;
END_VAR
VAR_OUTPUT
    Operator_Alert : BOOL := FALSE;
    Weld_Soft_Start_Active : BOOL := TRUE;
END_VAR
VAR
    StartupTimer : TON;
    GapDebounceTimer : TON;
    startupActive : BOOL := TRUE;
    state : INT := 0;
END_VAR

// Stage 2: safety/reset priority and supervisory state transition.
IF NOT Weld_E_Stop_NC THEN
    Operator_Alert := FALSE;
END_IF;

IF state = 0 THEN
    IF StartupTimer.Q THEN
        state := 1;
    END_IF;
ELSE
    state := 1;
END_IF;

// Stage 3: unconditional top-level timer calls.
StartupTimer(IN := TRUE, PT := T#5s);
startupActive := NOT StartupTimer.Q;
GapDebounceTimer(IN := (NOT startupActive) AND Weld_E_Stop_NC AND Gap_Exceeded, PT := DebounceTime);

// Stage 4: unified output assignments.
Operator_Alert := (NOT startupActive) AND Weld_E_Stop_NC AND Gap_Exceeded AND GapDebounceTimer.Q;
Weld_Soft_Start_Active := startupActive;
END_FUNCTION_BLOCK
