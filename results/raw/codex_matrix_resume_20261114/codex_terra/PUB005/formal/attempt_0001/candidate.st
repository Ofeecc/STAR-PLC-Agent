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
    GapTimer : TON;
END_VAR

StartupTimer(IN := TRUE, PT := T#5s);
Weld_Soft_Start_Active := NOT StartupTimer.Q;
GapTimer(IN := NOT Weld_Soft_Start_Active AND Weld_E_Stop_NC AND Gap_Exceeded, PT := DebounceTime);
Operator_Alert := GapTimer.Q;
END_FUNCTION_BLOCK
