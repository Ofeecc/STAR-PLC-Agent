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
    StartupComplete : BOOL := FALSE;
    SampledGap : BOOL;
    SampledEStopNC : BOOL;
    SampledDebounceTime : TIME;
END_VAR

SampledGap := Gap_Exceeded;
SampledEStopNC := Weld_E_Stop_NC;
SampledDebounceTime := DebounceTime;

// Use elapsed time rather than the timer's done output for the 5-second boundary.
T_Startup(IN := TRUE, PT := T#10000ms);
IF T_Startup.ET >= T#5000ms THEN
    StartupComplete := TRUE;
END_IF;

T_Gap(IN := StartupComplete AND SampledEStopNC AND SampledGap,
      PT := SampledDebounceTime);

Weld_Soft_Start_Active := NOT StartupComplete;
Operator_Alert := StartupComplete AND SampledEStopNC AND SampledGap AND T_Gap.Q;
END_FUNCTION_BLOCK
