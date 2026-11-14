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
    NormalMonitoring : BOOL;
END_VAR

StartupTimer(IN := TRUE, PT := T#5S);

NormalMonitoring := StartupTimer.Q AND Weld_E_Stop_NC;
GapTimer(IN := NormalMonitoring AND Gap_Exceeded, PT := DebounceTime);

Weld_Soft_Start_Active := NOT StartupTimer.Q;
Operator_Alert := Not StartupTimer.Q AND Weld_E_Stop_NC AND Gap_Exceeded AND GapTimer.Q;
END_FUNCTION_BLOCK
