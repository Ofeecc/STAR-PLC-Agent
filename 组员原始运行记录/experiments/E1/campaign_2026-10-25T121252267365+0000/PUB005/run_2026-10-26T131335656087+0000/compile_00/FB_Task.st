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
    tonStartup : TON;
    tonGap : TON;
    xStartupActive : BOOL := TRUE;
END_VAR

// 5-second power-up monitoring inhibition.
// Starts on first invocation and continues through E-stop (never restarted).
tonStartup(IN := TRUE, PT := T#5S);
xStartupActive := NOT tonStartup.Q;

// Gap debounce timer: only accumulates while monitoring is permitted.
// IN=FALSE resets elapsed time (startup, E-stop or raw gap FALSE).
tonGap(IN := (NOT xStartupActive) AND Weld_E_Stop_NC AND Gap_Exceeded,
       PT := DebounceTime);

// Outputs
Weld_Soft_Start_Active := xStartupActive;
Operator_Alert := (NOT xStartupActive) AND Weld_E_Stop_NC AND Gap_Exceeded AND tonGap.Q;
END_FUNCTION_BLOCK
