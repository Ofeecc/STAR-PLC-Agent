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
    debounceStarted : BOOL := FALSE;
    debounceElapsed : LTIME := LTIME#0ns;
    viscosityQualified : BOOL := FALSE;
END_VAR

IF (NOT PASTE_E_STOP_NC) OR (NOT VISCOSITY_OK) THEN
    debounceStarted := FALSE;
    debounceElapsed := LTIME#0ns;
    viscosityQualified := FALSE;
ELSE
    IF NOT debounceStarted THEN
        debounceStarted := TRUE;
        debounceElapsed := LTIME#0ns;
        IF DebounceTime <= T#0ms THEN
            viscosityQualified := TRUE;
        ELSE
            viscosityQualified := FALSE;
        END_IF
    ELSIF NOT viscosityQualified THEN
        debounceElapsed := debounceElapsed + TIME_TO_LTIME(CycleTime);
        IF debounceElapsed >= TIME_TO_LTIME(DebounceTime) THEN
            viscosityQualified := TRUE;
        END_IF
    END_IF
END_IF

VFD_RUN := PASTE_E_STOP_NC AND VISCOSITY_OK AND viscosityQualified;

IF VFD_RUN THEN
    PUMP_RUNTIME_ACC := PUMP_RUNTIME_ACC + TIME_TO_LTIME(CycleTime);
END_IF

PUMP_MAINT_DUE := PUMP_RUNTIME_ACC >= LTIME#500h;
END_FUNCTION_BLOCK
