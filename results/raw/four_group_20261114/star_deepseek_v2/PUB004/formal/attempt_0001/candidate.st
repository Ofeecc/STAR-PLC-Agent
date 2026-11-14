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
    state : INT := 0;
    permit : BOOL := FALSE;
    prevPermit : BOOL := FALSE;
    debounceElapsed : LTIME := LTIME#0ns;
    debounceQualified : BOOL := FALSE;
END_VAR

permit := VISCOSITY_OK AND PASTE_E_STOP_NC;

IF NOT permit THEN
    state := 0;
    debounceElapsed := LTIME#0ns;
    debounceQualified := FALSE;
END_IF;

CASE state OF
    0:
        IF permit THEN
            state := 1;
            debounceElapsed := LTIME#0ns;
            debounceQualified := FALSE;
        END_IF;
    1:
        IF NOT permit THEN
            state := 0;
            debounceElapsed := LTIME#0ns;
            debounceQualified := FALSE;
        ELSIF prevPermit THEN
            debounceElapsed := debounceElapsed + TIME_TO_LTIME(CycleTime);
            IF debounceElapsed >= TIME_TO_LTIME(DebounceTime) THEN
                debounceQualified := TRUE;
                state := 2;
            END_IF;
        END_IF;
    2:
        IF NOT permit THEN
            state := 0;
            debounceElapsed := LTIME#0ns;
            debounceQualified := FALSE;
        END_IF;
    ELSE
        state := 0;
        debounceElapsed := LTIME#0ns;
        debounceQualified := FALSE;
END_CASE;

VFD_RUN := permit AND debounceQualified;

IF VFD_RUN THEN
    PUMP_RUNTIME_ACC := PUMP_RUNTIME_ACC + TIME_TO_LTIME(CycleTime);
END_IF;

PUMP_MAINT_DUE := PUMP_RUNTIME_ACC >= LTIME#500h;

prevPermit := permit;
END_FUNCTION_BLOCK
