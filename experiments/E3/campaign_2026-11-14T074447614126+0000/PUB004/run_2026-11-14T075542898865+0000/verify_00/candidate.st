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
    DebounceTimer : TON;
    permit : BOOL := FALSE;
    qualified : BOOL := FALSE;
    immediateSafetyReset : BOOL := FALSE;
    initialized : BOOL := FALSE;
END_VAR
VAR CONSTANT
    MAINT_LIMIT : LTIME := LTIME#500h;
END_VAR

// Stage 1: sample inputs and compute permissive
permit := VISCOSITY_OK AND PASTE_E_STOP_NC;
immediateSafetyReset := NOT permit;

// Power-up initialization on first scan
IF NOT initialized THEN
    VFD_RUN := FALSE;
    PUMP_RUNTIME_ACC := LTIME#0ns;
    PUMP_MAINT_DUE := FALSE;
    qualified := FALSE;
    initialized := TRUE;
END_IF;

// Stage 2: safety reset priority
IF immediateSafetyReset THEN
    qualified := FALSE;
END_IF;

// Stage 3: unconditional top-level TON call, exactly once per scan
DebounceTimer(IN := permit, PT := DebounceTime);

// Stage 4: unified output assignments
qualified := DebounceTimer.Q AND NOT immediateSafetyReset;
VFD_RUN := permit AND qualified;

IF VFD_RUN THEN
    PUMP_RUNTIME_ACC := PUMP_RUNTIME_ACC + TIME_TO_LTIME(CycleTime);
END_IF;

PUMP_MAINT_DUE := (PUMP_RUNTIME_ACC >= MAINT_LIMIT);
END_FUNCTION_BLOCK
