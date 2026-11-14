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
    T_Startup : TON;
    T_Gap : TON;
END_VAR

T_Startup(IN := TRUE, PT := T#5s);
T_Gap(IN := T_Startup.Q AND Weld_E_Stop_NC AND Gap_Exceeded,
      PT := DebounceTime);

Weld_Soft_Start_Active := NOT T_Startup.Q;
Operator_Alert := T_Startup.Q AND Weld_E_Stop_NC AND Gap_Exceeded AND T_Gap.Q;
END_FUNCTION_BLOCK
