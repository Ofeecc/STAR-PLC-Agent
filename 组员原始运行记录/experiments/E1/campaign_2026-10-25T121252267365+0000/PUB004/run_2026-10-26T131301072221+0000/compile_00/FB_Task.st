FUNCTION_BLOCK FB_Task
VAR_INPUT
  VISCOSITY_OK : BOOL;
  PASTE_E_STOP_NC : BOOL;
  DebounceTime : TIME;
  CycleTime : TIME;
END_VAR
VAR_OUTPUT
  VFD_RUN : BOOL;
  PUMP_MAINT_DUE : BOOL;
  PUMP_RUNTIME_ACC : LTIME;
END_VAR
VAR
  debounceElapsed : LTIME;
  prevPermit : BOOL;
  permit : BOOL;
  qualified : BOOL;
END_VAR

permit := VISCOSITY_OK AND PASTE_E_STOP_NC;

IF NOT permit THEN
  debounceElapsed := LTIME#0ns;
  prevPermit := FALSE;
ELSE
  IF NOT prevPermit THEN
    debounceElapsed := LTIME#0ns;
    prevPermit := TRUE;
  ELSE
    debounceElapsed := debounceElapsed + TIME_TO_LTIME(CycleTime);
  END_IF
END_IF

qualified := permit AND (debounceElapsed >= TIME_TO_LTIME(DebounceTime));

VFD_RUN := permit AND qualified;

IF VFD_RUN THEN
  PUMP_RUNTIME_ACC := PUMP_RUNTIME_ACC + TIME_TO_LTIME(CycleTime);
END_IF

PUMP_MAINT_DUE := PUMP_RUNTIME_ACC >= LTIME#500h;
END_FUNCTION_BLOCK
