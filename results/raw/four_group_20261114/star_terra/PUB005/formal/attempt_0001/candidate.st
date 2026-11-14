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
    state : INT := 0; // 0 = E_STOP, 1 = READY
    sampledGap : BOOL;
    sampledEStopNC : BOOL;
    sampledDebounceTime : TIME;
END_VAR

sampledGap := Gap_Exceeded;
sampledEStopNC := Weld_E_Stop_NC;
sampledDebounceTime := DebounceTime;

IF sampledEStopNC THEN
    state := 1;
ELSE
    state := 0;
END_IF;

T_Startup(IN := TRUE, PT := T#5s);
T_Gap(IN := T_Startup.Q AND (state = 1) AND sampledGap, PT := sampledDebounceTime);

Weld_Soft_Start_Active := NOT T_Startup.Q;
Operator_Alert := T_Startup.Q AND (state = 1) AND sampledGap AND T_Gap.Q;
END_FUNCTION_BLOCK
