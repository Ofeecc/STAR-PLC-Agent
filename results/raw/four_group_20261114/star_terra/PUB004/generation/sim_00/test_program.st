PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchLastTime : TIME := T#0ms;
 BenchClockReady : BOOL := FALSE;
 BenchCurrentTime : TIME := T#0ms;
 TraceDt : ARRAY[0..9] OF UDINT;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_VISCOSITY_OK : ARRAY[0..9] OF BOOL;
 TraceIn_PASTE_E_STOP_NC : ARRAY[0..9] OF BOOL;
 TraceIn_DebounceTime : ARRAY[0..9] OF TIME;
 TraceIn_CycleTime : ARRAY[0..9] OF TIME;
 TraceOut_VFD_RUN : ARRAY[0..9] OF BOOL;
 TraceOut_PUMP_MAINT_DUE : ARRAY[0..9] OF BOOL;
 TraceOut_PUMP_RUNTIME_ACC : ARRAY[0..9] OF LTIME;
END_VAR

IF NOT BenchDone THEN
 BenchCurrentTime := TIME();
 IF NOT BenchClockReady THEN
  BenchLastTime := BenchCurrentTime;
  BenchClockReady := TRUE;
 ELSE
 CASE BenchStep OF
 0:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(10) THEN
   TraceDt[0] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := TIME#100ms;
   BenchUut0.CycleTime := TIME#10ms;
   TraceIn_VISCOSITY_OK[0] := BenchUut0.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[0] := BenchUut0.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[0] := BenchUut0.DebounceTime;
   TraceIn_CycleTime[0] := BenchUut0.CycleTime;
   BenchUut0();
   TraceOut_VFD_RUN[0] := BenchUut0.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[0] := BenchUut0.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[0] := BenchUut0.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 1:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(99) THEN
   TraceDt[1] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := TIME#100ms;
   BenchUut0.CycleTime := TIME#99ms;
   TraceIn_VISCOSITY_OK[1] := BenchUut0.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[1] := BenchUut0.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[1] := BenchUut0.DebounceTime;
   TraceIn_CycleTime[1] := BenchUut0.CycleTime;
   BenchUut0();
   TraceOut_VFD_RUN[1] := BenchUut0.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[1] := BenchUut0.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[1] := BenchUut0.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 2:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[2] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := TIME#100ms;
   BenchUut0.CycleTime := TIME#1ms;
   TraceIn_VISCOSITY_OK[2] := BenchUut0.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[2] := BenchUut0.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[2] := BenchUut0.DebounceTime;
   TraceIn_CycleTime[2] := BenchUut0.CycleTime;
   BenchUut0();
   TraceOut_VFD_RUN[2] := BenchUut0.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[2] := BenchUut0.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[2] := BenchUut0.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 3:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(25) THEN
   TraceDt[3] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := TIME#100ms;
   BenchUut0.CycleTime := TIME#25ms;
   TraceIn_VISCOSITY_OK[3] := BenchUut0.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[3] := BenchUut0.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[3] := BenchUut0.DebounceTime;
   TraceIn_CycleTime[3] := BenchUut0.CycleTime;
   BenchUut0();
   TraceOut_VFD_RUN[3] := BenchUut0.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[3] := BenchUut0.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[3] := BenchUut0.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 4:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5) THEN
   TraceDt[4] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := FALSE;
   BenchUut0.DebounceTime := TIME#100ms;
   BenchUut0.CycleTime := TIME#5ms;
   TraceIn_VISCOSITY_OK[4] := BenchUut0.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[4] := BenchUut0.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[4] := BenchUut0.DebounceTime;
   TraceIn_CycleTime[4] := BenchUut0.CycleTime;
   BenchUut0();
   TraceOut_VFD_RUN[4] := BenchUut0.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[4] := BenchUut0.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[4] := BenchUut0.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 5:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[5] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := TIME#100ms;
   BenchUut0.CycleTime := TIME#100ms;
   TraceIn_VISCOSITY_OK[5] := BenchUut0.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[5] := BenchUut0.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[5] := BenchUut0.DebounceTime;
   TraceIn_CycleTime[5] := BenchUut0.CycleTime;
   BenchUut0();
   TraceOut_VFD_RUN[5] := BenchUut0.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[5] := BenchUut0.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[5] := BenchUut0.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 6:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(99) THEN
   TraceDt[6] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := TIME#100ms;
   BenchUut0.CycleTime := TIME#99ms;
   TraceIn_VISCOSITY_OK[6] := BenchUut0.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[6] := BenchUut0.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[6] := BenchUut0.DebounceTime;
   TraceIn_CycleTime[6] := BenchUut0.CycleTime;
   BenchUut0();
   TraceOut_VFD_RUN[6] := BenchUut0.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[6] := BenchUut0.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[6] := BenchUut0.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 7:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[7] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := TIME#100ms;
   BenchUut0.CycleTime := TIME#1ms;
   TraceIn_VISCOSITY_OK[7] := BenchUut0.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[7] := BenchUut0.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[7] := BenchUut0.DebounceTime;
   TraceIn_CycleTime[7] := BenchUut0.CycleTime;
   BenchUut0();
   TraceOut_VFD_RUN[7] := BenchUut0.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[7] := BenchUut0.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[7] := BenchUut0.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 8:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[8] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.VISCOSITY_OK := TRUE;
   BenchUut1.PASTE_E_STOP_NC := TRUE;
   BenchUut1.DebounceTime := TIME#1ms;
   BenchUut1.CycleTime := TIME#1ms;
   TraceIn_VISCOSITY_OK[8] := BenchUut1.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[8] := BenchUut1.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[8] := BenchUut1.DebounceTime;
   TraceIn_CycleTime[8] := BenchUut1.CycleTime;
   BenchUut1();
   TraceOut_VFD_RUN[8] := BenchUut1.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[8] := BenchUut1.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[8] := BenchUut1.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 9:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[9] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.VISCOSITY_OK := TRUE;
   BenchUut1.PASTE_E_STOP_NC := TRUE;
   BenchUut1.DebounceTime := TIME#1ms;
   BenchUut1.CycleTime := TIME#1ms;
   TraceIn_VISCOSITY_OK[9] := BenchUut1.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[9] := BenchUut1.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[9] := BenchUut1.DebounceTime;
   TraceIn_CycleTime[9] := BenchUut1.CycleTime;
   BenchUut1();
   TraceOut_VFD_RUN[9] := BenchUut1.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[9] := BenchUut1.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[9] := BenchUut1.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 10 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
