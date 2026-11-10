FUNCTION_BLOCK FB_Task
VAR_INPUT
    Gap_Exceeded : BOOL;
    Weld_E_Stop_NC : BOOL;
    DebounceTime : TIME;
END_VAR
VAR_OUTPUT
    Operator_Alert : BOOL;
    Weld_Soft_Start_Active : BOOL;
END_VAR
VAR
    StartupTimer : TON;
    GapTimer : TON;
    StartupInhibition : BOOL;
END_VAR

StartupTimer(IN := TRUE, PT := T#5S);

Weld_Soft_Start_Active := NOT StartupTimer.Q;
StartupInhibition := Weld_Soft_Start_Active;

IF NOT Weld_E_Stop_NC THEN
    Operator_Alert := FALSE;
    GapTimer(IN := FALSE, PT := DebounceTime);
ELSIF StartupInhibition THEN
    Operator_Alert := FALSE;
    GapTimer(IN := FALSE, PT := DebounceTime);
ELSIF NOT Gap_Exceeded THEN
    Operator_Alert := FALSE;
    GapTimer(IN := FALSE, PT := DebounceTime);
ELSE
    GapTimer(IN := TRUE, PT := DebounceTime);
    Operator_Alert := GapTimer.Q;
END_IF;
END_FUNCTION_BLOCK
