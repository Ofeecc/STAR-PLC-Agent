PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchLastTime : TIME := T#0ms;
 BenchClockReady : BOOL := FALSE;
 BenchCurrentTime : TIME := T#0ms;
 TraceDt : ARRAY[0..42] OF UDINT;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 BenchUut2 : FB_Task;
 BenchUut3 : FB_Task;
 BenchUut4 : FB_Task;
 BenchUut5 : FB_Task;
 TraceIn_VISCOSITY_OK : ARRAY[0..42] OF BOOL;
 TraceIn_PASTE_E_STOP_NC : ARRAY[0..42] OF BOOL;
 TraceIn_DebounceTime : ARRAY[0..42] OF TIME;
 TraceIn_CycleTime : ARRAY[0..42] OF TIME;
 TraceOut_VFD_RUN : ARRAY[0..42] OF BOOL;
 TraceOut_PUMP_MAINT_DUE : ARRAY[0..42] OF BOOL;
 TraceOut_PUMP_RUNTIME_ACC : ARRAY[0..42] OF LTIME;
END_VAR

IF NOT BenchDone THEN
 BenchCurrentTime := TIME();
 IF NOT BenchClockReady THEN
  BenchLastTime := BenchCurrentTime;
  BenchClockReady := TRUE;
 ELSE
 CASE BenchStep OF
 0:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[0] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := FALSE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
   BenchUut0.CycleTime := T#1s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[1] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
   BenchUut0.CycleTime := T#1s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[2] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
   BenchUut0.CycleTime := T#1s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[3] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
   BenchUut0.CycleTime := T#1s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[4] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
   BenchUut0.CycleTime := T#1s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[5] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := FALSE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
   BenchUut0.CycleTime := T#1s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[6] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
   BenchUut0.CycleTime := T#1s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[7] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
   BenchUut0.CycleTime := T#1s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[8] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.VISCOSITY_OK := TRUE;
   BenchUut0.PASTE_E_STOP_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
   BenchUut0.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[8] := BenchUut0.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[8] := BenchUut0.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[8] := BenchUut0.DebounceTime;
   TraceIn_CycleTime[8] := BenchUut0.CycleTime;
   BenchUut0();
   TraceOut_VFD_RUN[8] := BenchUut0.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[8] := BenchUut0.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[8] := BenchUut0.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 9:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[9] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.VISCOSITY_OK := TRUE;
   BenchUut1.PASTE_E_STOP_NC := TRUE;
   BenchUut1.DebounceTime := T#2s;
   BenchUut1.CycleTime := T#1s;
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
 10:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[10] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.VISCOSITY_OK := TRUE;
   BenchUut1.PASTE_E_STOP_NC := TRUE;
   BenchUut1.DebounceTime := T#2s;
   BenchUut1.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[10] := BenchUut1.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[10] := BenchUut1.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[10] := BenchUut1.DebounceTime;
   TraceIn_CycleTime[10] := BenchUut1.CycleTime;
   BenchUut1();
   TraceOut_VFD_RUN[10] := BenchUut1.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[10] := BenchUut1.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[10] := BenchUut1.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 11:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[11] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.VISCOSITY_OK := TRUE;
   BenchUut1.PASTE_E_STOP_NC := FALSE;
   BenchUut1.DebounceTime := T#2s;
   BenchUut1.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[11] := BenchUut1.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[11] := BenchUut1.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[11] := BenchUut1.DebounceTime;
   TraceIn_CycleTime[11] := BenchUut1.CycleTime;
   BenchUut1();
   TraceOut_VFD_RUN[11] := BenchUut1.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[11] := BenchUut1.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[11] := BenchUut1.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 12:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[12] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.VISCOSITY_OK := TRUE;
   BenchUut1.PASTE_E_STOP_NC := TRUE;
   BenchUut1.DebounceTime := T#2s;
   BenchUut1.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[12] := BenchUut1.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[12] := BenchUut1.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[12] := BenchUut1.DebounceTime;
   TraceIn_CycleTime[12] := BenchUut1.CycleTime;
   BenchUut1();
   TraceOut_VFD_RUN[12] := BenchUut1.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[12] := BenchUut1.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[12] := BenchUut1.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 13:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[13] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.VISCOSITY_OK := TRUE;
   BenchUut1.PASTE_E_STOP_NC := TRUE;
   BenchUut1.DebounceTime := T#2s;
   BenchUut1.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[13] := BenchUut1.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[13] := BenchUut1.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[13] := BenchUut1.DebounceTime;
   TraceIn_CycleTime[13] := BenchUut1.CycleTime;
   BenchUut1();
   TraceOut_VFD_RUN[13] := BenchUut1.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[13] := BenchUut1.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[13] := BenchUut1.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 14:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[14] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.VISCOSITY_OK := TRUE;
   BenchUut1.PASTE_E_STOP_NC := TRUE;
   BenchUut1.DebounceTime := T#2s;
   BenchUut1.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[14] := BenchUut1.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[14] := BenchUut1.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[14] := BenchUut1.DebounceTime;
   TraceIn_CycleTime[14] := BenchUut1.CycleTime;
   BenchUut1();
   TraceOut_VFD_RUN[14] := BenchUut1.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[14] := BenchUut1.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[14] := BenchUut1.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 15:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[15] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.VISCOSITY_OK := TRUE;
   BenchUut1.PASTE_E_STOP_NC := FALSE;
   BenchUut1.DebounceTime := T#2s;
   BenchUut1.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[15] := BenchUut1.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[15] := BenchUut1.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[15] := BenchUut1.DebounceTime;
   TraceIn_CycleTime[15] := BenchUut1.CycleTime;
   BenchUut1();
   TraceOut_VFD_RUN[15] := BenchUut1.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[15] := BenchUut1.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[15] := BenchUut1.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 16:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[16] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.VISCOSITY_OK := TRUE;
   BenchUut2.PASTE_E_STOP_NC := TRUE;
   BenchUut2.DebounceTime := T#1s;
   BenchUut2.CycleTime := T#100ms;
   TraceIn_VISCOSITY_OK[16] := BenchUut2.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[16] := BenchUut2.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[16] := BenchUut2.DebounceTime;
   TraceIn_CycleTime[16] := BenchUut2.CycleTime;
   BenchUut2();
   TraceOut_VFD_RUN[16] := BenchUut2.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[16] := BenchUut2.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[16] := BenchUut2.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 17:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[17] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.VISCOSITY_OK := TRUE;
   BenchUut2.PASTE_E_STOP_NC := FALSE;
   BenchUut2.DebounceTime := T#1s;
   BenchUut2.CycleTime := T#100ms;
   TraceIn_VISCOSITY_OK[17] := BenchUut2.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[17] := BenchUut2.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[17] := BenchUut2.DebounceTime;
   TraceIn_CycleTime[17] := BenchUut2.CycleTime;
   BenchUut2();
   TraceOut_VFD_RUN[17] := BenchUut2.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[17] := BenchUut2.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[17] := BenchUut2.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 18:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[18] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.VISCOSITY_OK := TRUE;
   BenchUut2.PASTE_E_STOP_NC := TRUE;
   BenchUut2.DebounceTime := T#1s;
   BenchUut2.CycleTime := T#100ms;
   TraceIn_VISCOSITY_OK[18] := BenchUut2.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[18] := BenchUut2.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[18] := BenchUut2.DebounceTime;
   TraceIn_CycleTime[18] := BenchUut2.CycleTime;
   BenchUut2();
   TraceOut_VFD_RUN[18] := BenchUut2.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[18] := BenchUut2.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[18] := BenchUut2.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 19:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(999) THEN
   TraceDt[19] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.VISCOSITY_OK := TRUE;
   BenchUut2.PASTE_E_STOP_NC := TRUE;
   BenchUut2.DebounceTime := T#1s;
   BenchUut2.CycleTime := T#100ms;
   TraceIn_VISCOSITY_OK[19] := BenchUut2.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[19] := BenchUut2.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[19] := BenchUut2.DebounceTime;
   TraceIn_CycleTime[19] := BenchUut2.CycleTime;
   BenchUut2();
   TraceOut_VFD_RUN[19] := BenchUut2.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[19] := BenchUut2.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[19] := BenchUut2.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 20:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[20] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.VISCOSITY_OK := TRUE;
   BenchUut2.PASTE_E_STOP_NC := TRUE;
   BenchUut2.DebounceTime := T#1s;
   BenchUut2.CycleTime := T#100ms;
   TraceIn_VISCOSITY_OK[20] := BenchUut2.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[20] := BenchUut2.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[20] := BenchUut2.DebounceTime;
   TraceIn_CycleTime[20] := BenchUut2.CycleTime;
   BenchUut2();
   TraceOut_VFD_RUN[20] := BenchUut2.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[20] := BenchUut2.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[20] := BenchUut2.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 21:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[21] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.VISCOSITY_OK := TRUE;
   BenchUut3.PASTE_E_STOP_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   BenchUut3.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[21] := BenchUut3.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[21] := BenchUut3.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[21] := BenchUut3.DebounceTime;
   TraceIn_CycleTime[21] := BenchUut3.CycleTime;
   BenchUut3();
   TraceOut_VFD_RUN[21] := BenchUut3.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[21] := BenchUut3.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[21] := BenchUut3.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 22:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[22] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.VISCOSITY_OK := TRUE;
   BenchUut3.PASTE_E_STOP_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   BenchUut3.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[22] := BenchUut3.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[22] := BenchUut3.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[22] := BenchUut3.DebounceTime;
   TraceIn_CycleTime[22] := BenchUut3.CycleTime;
   BenchUut3();
   TraceOut_VFD_RUN[22] := BenchUut3.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[22] := BenchUut3.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[22] := BenchUut3.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 23:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[23] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.VISCOSITY_OK := FALSE;
   BenchUut3.PASTE_E_STOP_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   BenchUut3.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[23] := BenchUut3.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[23] := BenchUut3.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[23] := BenchUut3.DebounceTime;
   TraceIn_CycleTime[23] := BenchUut3.CycleTime;
   BenchUut3();
   TraceOut_VFD_RUN[23] := BenchUut3.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[23] := BenchUut3.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[23] := BenchUut3.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 24:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[24] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.VISCOSITY_OK := TRUE;
   BenchUut3.PASTE_E_STOP_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   BenchUut3.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[24] := BenchUut3.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[24] := BenchUut3.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[24] := BenchUut3.DebounceTime;
   TraceIn_CycleTime[24] := BenchUut3.CycleTime;
   BenchUut3();
   TraceOut_VFD_RUN[24] := BenchUut3.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[24] := BenchUut3.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[24] := BenchUut3.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 25:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[25] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.VISCOSITY_OK := TRUE;
   BenchUut3.PASTE_E_STOP_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   BenchUut3.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[25] := BenchUut3.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[25] := BenchUut3.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[25] := BenchUut3.DebounceTime;
   TraceIn_CycleTime[25] := BenchUut3.CycleTime;
   BenchUut3();
   TraceOut_VFD_RUN[25] := BenchUut3.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[25] := BenchUut3.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[25] := BenchUut3.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 26:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(6000) THEN
   TraceDt[26] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.VISCOSITY_OK := TRUE;
   BenchUut3.PASTE_E_STOP_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   BenchUut3.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[26] := BenchUut3.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[26] := BenchUut3.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[26] := BenchUut3.DebounceTime;
   TraceIn_CycleTime[26] := BenchUut3.CycleTime;
   BenchUut3();
   TraceOut_VFD_RUN[26] := BenchUut3.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[26] := BenchUut3.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[26] := BenchUut3.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 27:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[27] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.VISCOSITY_OK := TRUE;
   BenchUut3.PASTE_E_STOP_NC := FALSE;
   BenchUut3.DebounceTime := T#2s;
   BenchUut3.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[27] := BenchUut3.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[27] := BenchUut3.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[27] := BenchUut3.DebounceTime;
   TraceIn_CycleTime[27] := BenchUut3.CycleTime;
   BenchUut3();
   TraceOut_VFD_RUN[27] := BenchUut3.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[27] := BenchUut3.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[27] := BenchUut3.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 28:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[28] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.VISCOSITY_OK := TRUE;
   BenchUut3.PASTE_E_STOP_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   BenchUut3.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[28] := BenchUut3.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[28] := BenchUut3.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[28] := BenchUut3.DebounceTime;
   TraceIn_CycleTime[28] := BenchUut3.CycleTime;
   BenchUut3();
   TraceOut_VFD_RUN[28] := BenchUut3.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[28] := BenchUut3.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[28] := BenchUut3.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 29:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(6000) THEN
   TraceDt[29] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.VISCOSITY_OK := TRUE;
   BenchUut3.PASTE_E_STOP_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   BenchUut3.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[29] := BenchUut3.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[29] := BenchUut3.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[29] := BenchUut3.DebounceTime;
   TraceIn_CycleTime[29] := BenchUut3.CycleTime;
   BenchUut3();
   TraceOut_VFD_RUN[29] := BenchUut3.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[29] := BenchUut3.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[29] := BenchUut3.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 30:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[30] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.VISCOSITY_OK := TRUE;
   BenchUut4.PASTE_E_STOP_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   BenchUut4.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[30] := BenchUut4.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[30] := BenchUut4.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[30] := BenchUut4.DebounceTime;
   TraceIn_CycleTime[30] := BenchUut4.CycleTime;
   BenchUut4();
   TraceOut_VFD_RUN[30] := BenchUut4.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[30] := BenchUut4.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[30] := BenchUut4.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 31:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(3000) THEN
   TraceDt[31] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.VISCOSITY_OK := TRUE;
   BenchUut4.PASTE_E_STOP_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   BenchUut4.CycleTime := T#1799999999ms;
   TraceIn_VISCOSITY_OK[31] := BenchUut4.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[31] := BenchUut4.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[31] := BenchUut4.DebounceTime;
   TraceIn_CycleTime[31] := BenchUut4.CycleTime;
   BenchUut4();
   TraceOut_VFD_RUN[31] := BenchUut4.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[31] := BenchUut4.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[31] := BenchUut4.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 32:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[32] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.VISCOSITY_OK := TRUE;
   BenchUut4.PASTE_E_STOP_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   BenchUut4.CycleTime := T#1ms;
   TraceIn_VISCOSITY_OK[32] := BenchUut4.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[32] := BenchUut4.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[32] := BenchUut4.DebounceTime;
   TraceIn_CycleTime[32] := BenchUut4.CycleTime;
   BenchUut4();
   TraceOut_VFD_RUN[32] := BenchUut4.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[32] := BenchUut4.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[32] := BenchUut4.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 33:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[33] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.VISCOSITY_OK := FALSE;
   BenchUut4.PASTE_E_STOP_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   BenchUut4.CycleTime := T#1ms;
   TraceIn_VISCOSITY_OK[33] := BenchUut4.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[33] := BenchUut4.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[33] := BenchUut4.DebounceTime;
   TraceIn_CycleTime[33] := BenchUut4.CycleTime;
   BenchUut4();
   TraceOut_VFD_RUN[33] := BenchUut4.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[33] := BenchUut4.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[33] := BenchUut4.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 34:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[34] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.VISCOSITY_OK := TRUE;
   BenchUut4.PASTE_E_STOP_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   BenchUut4.CycleTime := T#1ms;
   TraceIn_VISCOSITY_OK[34] := BenchUut4.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[34] := BenchUut4.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[34] := BenchUut4.DebounceTime;
   TraceIn_CycleTime[34] := BenchUut4.CycleTime;
   BenchUut4();
   TraceOut_VFD_RUN[34] := BenchUut4.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[34] := BenchUut4.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[34] := BenchUut4.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 35:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(3000) THEN
   TraceDt[35] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.VISCOSITY_OK := TRUE;
   BenchUut4.PASTE_E_STOP_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   BenchUut4.CycleTime := T#1ms;
   TraceIn_VISCOSITY_OK[35] := BenchUut4.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[35] := BenchUut4.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[35] := BenchUut4.DebounceTime;
   TraceIn_CycleTime[35] := BenchUut4.CycleTime;
   BenchUut4();
   TraceOut_VFD_RUN[35] := BenchUut4.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[35] := BenchUut4.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[35] := BenchUut4.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 36:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[36] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.VISCOSITY_OK := TRUE;
   BenchUut5.PASTE_E_STOP_NC := TRUE;
   BenchUut5.DebounceTime := T#1s;
   BenchUut5.CycleTime := T#500ms;
   TraceIn_VISCOSITY_OK[36] := BenchUut5.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[36] := BenchUut5.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[36] := BenchUut5.DebounceTime;
   TraceIn_CycleTime[36] := BenchUut5.CycleTime;
   BenchUut5();
   TraceOut_VFD_RUN[36] := BenchUut5.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[36] := BenchUut5.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[36] := BenchUut5.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 37:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[37] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.VISCOSITY_OK := TRUE;
   BenchUut5.PASTE_E_STOP_NC := TRUE;
   BenchUut5.DebounceTime := T#1s;
   BenchUut5.CycleTime := T#500ms;
   TraceIn_VISCOSITY_OK[37] := BenchUut5.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[37] := BenchUut5.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[37] := BenchUut5.DebounceTime;
   TraceIn_CycleTime[37] := BenchUut5.CycleTime;
   BenchUut5();
   TraceOut_VFD_RUN[37] := BenchUut5.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[37] := BenchUut5.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[37] := BenchUut5.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 38:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[38] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.VISCOSITY_OK := TRUE;
   BenchUut5.PASTE_E_STOP_NC := TRUE;
   BenchUut5.DebounceTime := T#1s;
   BenchUut5.CycleTime := T#500ms;
   TraceIn_VISCOSITY_OK[38] := BenchUut5.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[38] := BenchUut5.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[38] := BenchUut5.DebounceTime;
   TraceIn_CycleTime[38] := BenchUut5.CycleTime;
   BenchUut5();
   TraceOut_VFD_RUN[38] := BenchUut5.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[38] := BenchUut5.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[38] := BenchUut5.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 39:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[39] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.VISCOSITY_OK := TRUE;
   BenchUut5.PASTE_E_STOP_NC := TRUE;
   BenchUut5.DebounceTime := T#1s;
   BenchUut5.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[39] := BenchUut5.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[39] := BenchUut5.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[39] := BenchUut5.DebounceTime;
   TraceIn_CycleTime[39] := BenchUut5.CycleTime;
   BenchUut5();
   TraceOut_VFD_RUN[39] := BenchUut5.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[39] := BenchUut5.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[39] := BenchUut5.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 40:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[40] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.VISCOSITY_OK := FALSE;
   BenchUut5.PASTE_E_STOP_NC := TRUE;
   BenchUut5.DebounceTime := T#1s;
   BenchUut5.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[40] := BenchUut5.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[40] := BenchUut5.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[40] := BenchUut5.DebounceTime;
   TraceIn_CycleTime[40] := BenchUut5.CycleTime;
   BenchUut5();
   TraceOut_VFD_RUN[40] := BenchUut5.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[40] := BenchUut5.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[40] := BenchUut5.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 41:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[41] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.VISCOSITY_OK := TRUE;
   BenchUut5.PASTE_E_STOP_NC := TRUE;
   BenchUut5.DebounceTime := T#1s;
   BenchUut5.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[41] := BenchUut5.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[41] := BenchUut5.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[41] := BenchUut5.DebounceTime;
   TraceIn_CycleTime[41] := BenchUut5.CycleTime;
   BenchUut5();
   TraceOut_VFD_RUN[41] := BenchUut5.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[41] := BenchUut5.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[41] := BenchUut5.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 42:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[42] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.VISCOSITY_OK := TRUE;
   BenchUut5.PASTE_E_STOP_NC := TRUE;
   BenchUut5.DebounceTime := T#1s;
   BenchUut5.CycleTime := T#1s;
   TraceIn_VISCOSITY_OK[42] := BenchUut5.VISCOSITY_OK;
   TraceIn_PASTE_E_STOP_NC[42] := BenchUut5.PASTE_E_STOP_NC;
   TraceIn_DebounceTime[42] := BenchUut5.DebounceTime;
   TraceIn_CycleTime[42] := BenchUut5.CycleTime;
   BenchUut5();
   TraceOut_VFD_RUN[42] := BenchUut5.VFD_RUN;
   TraceOut_PUMP_MAINT_DUE[42] := BenchUut5.PUMP_MAINT_DUE;
   TraceOut_PUMP_RUNTIME_ACC[42] := BenchUut5.PUMP_RUNTIME_ACC;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 43 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
