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
    wasPermitted : BOOL := FALSE;
    debounceElapsed : LTIME := LTIME#0ns;
    debounceLimit : LTIME := LTIME#0ns;
    runNext : BOOL := FALSE;
    accNext : LTIME := LTIME#0ns;
END_VAR

permitted := PASTE_E_STOP_NC AND VISCOSITY_OK;
debounceLimit := TIME_TO_LTIME(DebounceTime);

IF NOT permitted THEN
    debounceElapsed := LTIME#0ns;
    wasPermitted := FALSE;
ELSIF NOT wasPermitted THEN
    debounceElapsed := LTIME#0ns;
    wasPermitted := TRUE;
ELSIF debounceElapsed < debounceLimit THEN
    debounceElapsed := debounceElapsed + TIME_TO_LTIME(CycleTime);
    IF debounceElapsed > debounceLimit THEN
        debounceElapsed := debounceLimit;
    END_IF;
END_IF;

runNext := permitted AND (debounceElapsed >= debounceLimit);
accNext := PUMP_RUNTIME_ACC;
IF runNext THEN
    accNext := accNext + TIME_TO_LTIME(CycleTime);
END_IF;

VFD_RUN := runNext;
PUMP_RUNTIME_ACC := accNext;
PUMP_MAINT_DUE := accNext >= LTIME#500h;
END_FUNCTION_BLOCK
