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
    debounceElapsed : LTIME := LTIME#0ns;
    viscosityQualified : BOOL := FALSE;
END_VAR

IF NOT PASTE_E_STOP_NC THEN
    debounceElapsed := LTIME#0ns;
    viscosityQualified := FALSE;
ELSIF NOT VISCOSITY_OK THEN
    debounceElapsed := LTIME#0ns;
    viscosityQualified := FALSE;
ELSE
    IF debounceElapsed >= TIME_TO_LTIME(DebounceTime) THEN
        viscosityQualified := TRUE;
    END_IF;
END_IF;

VFD_RUN := PASTE_E_STOP_NC AND VISCOSITY_OK AND viscosityQualified;

IF VFD_RUN THEN
    PUMP_RUNTIME_ACC := PUMP_RUNTIME_ACC + TIME_TO_LTIME(CycleTime);
END_IF;

PUMP_MAINT_DUE := PUMP_RUNTIME_ACC >= LTIME#500h;

IF PASTE_E_STOP_NC AND VISCOSITY_OK AND NOT viscosityQualified THEN
    debounceElapsed := debounceElapsed + TIME_TO_LTIME(CycleTime);
END_IF;
END_FUNCTION_BLOCK
