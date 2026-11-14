FUNCTION_BLOCK FB_Task
VAR_INPUT
    VISCOSITY_OK : BOOL;
    PASTE_E_STOP_NC : BOOL;
    DebounceTime : TIME;
    CycleTime : TIME;
END_VAR
VAR_OUTPUT
    VFD_RUN : BOOL := FALSE;
    PUMP_MAINT_DUE : BOOL := FALSE;
    PUMP_RUNTIME_ACC : LTIME := LTIME#0ns;
END_VAR
VAR
    permitted : BOOL := FALSE;
    ViscosityDebounce : TON;
    runNext : BOOL := FALSE;
    accNext : LTIME := LTIME#0ns;
END_VAR

permitted := PASTE_E_STOP_NC AND VISCOSITY_OK;
ViscosityDebounce(IN := permitted, PT := DebounceTime);

runNext := permitted AND ViscosityDebounce.Q;
accNext := PUMP_RUNTIME_ACC;
IF runNext THEN
    accNext := accNext + TIME_TO_LTIME(CycleTime);
END_IF;

VFD_RUN := runNext;
PUMP_RUNTIME_ACC := accNext;
PUMP_MAINT_DUE := accNext >= LTIME#500h;
END_FUNCTION_BLOCK
