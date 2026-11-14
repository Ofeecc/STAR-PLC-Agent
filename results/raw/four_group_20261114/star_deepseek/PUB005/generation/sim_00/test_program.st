PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchLastTime : TIME := T#0ms;
 BenchClockReady : BOOL := FALSE;
 BenchCurrentTime : TIME := T#0ms;
 TraceDt : ARRAY[0..15] OF UDINT;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_Gap_Exceeded : ARRAY[0..15] OF BOOL;
 TraceIn_Weld_E_Stop_NC : ARRAY[0..15] OF BOOL;
 TraceIn_DebounceTime : ARRAY[0..15] OF TIME;
 TraceOut_Operator_Alert : ARRAY[0..15] OF BOOL;
 TraceOut_Weld_Soft_Start_Active : ARRAY[0..15] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 BenchCurrentTime := TIME();
 IF NOT BenchClockReady THEN
  BenchLastTime := BenchCurrentTime;
  BenchClockReady := TRUE;
 ELSE
 CASE BenchStep OF
 0:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[0] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut0.Gap_Exceeded := FALSE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[0] := BenchUut0.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[0] := BenchUut0.Weld_E_Stop_NC;
   TraceIn_DebounceTime[0] := BenchUut0.DebounceTime;
   BenchUut0();
   TraceOut_Operator_Alert[0] := BenchUut0.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[0] := BenchUut0.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 1:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[1] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[1] := BenchUut0.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[1] := BenchUut0.Weld_E_Stop_NC;
   TraceIn_DebounceTime[1] := BenchUut0.DebounceTime;
   BenchUut0();
   TraceOut_Operator_Alert[1] := BenchUut0.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[1] := BenchUut0.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 2:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(4000) THEN
   TraceDt[2] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[2] := BenchUut0.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[2] := BenchUut0.Weld_E_Stop_NC;
   TraceIn_DebounceTime[2] := BenchUut0.DebounceTime;
   BenchUut0();
   TraceOut_Operator_Alert[2] := BenchUut0.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[2] := BenchUut0.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 3:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[3] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[3] := BenchUut0.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[3] := BenchUut0.Weld_E_Stop_NC;
   TraceIn_DebounceTime[3] := BenchUut0.DebounceTime;
   BenchUut0();
   TraceOut_Operator_Alert[3] := BenchUut0.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[3] := BenchUut0.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 4:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[4] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[4] := BenchUut0.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[4] := BenchUut0.Weld_E_Stop_NC;
   TraceIn_DebounceTime[4] := BenchUut0.DebounceTime;
   BenchUut0();
   TraceOut_Operator_Alert[4] := BenchUut0.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[4] := BenchUut0.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 5:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[5] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut0.Gap_Exceeded := FALSE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[5] := BenchUut0.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[5] := BenchUut0.Weld_E_Stop_NC;
   TraceIn_DebounceTime[5] := BenchUut0.DebounceTime;
   BenchUut0();
   TraceOut_Operator_Alert[5] := BenchUut0.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[5] := BenchUut0.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 6:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[6] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[6] := BenchUut0.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[6] := BenchUut0.Weld_E_Stop_NC;
   TraceIn_DebounceTime[6] := BenchUut0.DebounceTime;
   BenchUut0();
   TraceOut_Operator_Alert[6] := BenchUut0.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[6] := BenchUut0.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 7:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[7] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[7] := BenchUut0.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[7] := BenchUut0.Weld_E_Stop_NC;
   TraceIn_DebounceTime[7] := BenchUut0.DebounceTime;
   BenchUut0();
   TraceOut_Operator_Alert[7] := BenchUut0.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[7] := BenchUut0.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 8:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[8] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := FALSE;
   BenchUut1.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[8] := BenchUut1.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[8] := BenchUut1.Weld_E_Stop_NC;
   TraceIn_DebounceTime[8] := BenchUut1.DebounceTime;
   BenchUut1();
   TraceOut_Operator_Alert[8] := BenchUut1.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[8] := BenchUut1.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 9:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[9] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := FALSE;
   BenchUut1.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[9] := BenchUut1.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[9] := BenchUut1.Weld_E_Stop_NC;
   TraceIn_DebounceTime[9] := BenchUut1.DebounceTime;
   BenchUut1();
   TraceOut_Operator_Alert[9] := BenchUut1.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[9] := BenchUut1.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 10:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(3000) THEN
   TraceDt[10] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := FALSE;
   BenchUut1.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[10] := BenchUut1.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[10] := BenchUut1.Weld_E_Stop_NC;
   TraceIn_DebounceTime[10] := BenchUut1.DebounceTime;
   BenchUut1();
   TraceOut_Operator_Alert[10] := BenchUut1.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[10] := BenchUut1.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 11:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[11] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := FALSE;
   BenchUut1.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[11] := BenchUut1.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[11] := BenchUut1.Weld_E_Stop_NC;
   TraceIn_DebounceTime[11] := BenchUut1.DebounceTime;
   BenchUut1();
   TraceOut_Operator_Alert[11] := BenchUut1.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[11] := BenchUut1.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 12:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[12] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := TRUE;
   BenchUut1.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[12] := BenchUut1.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[12] := BenchUut1.Weld_E_Stop_NC;
   TraceIn_DebounceTime[12] := BenchUut1.DebounceTime;
   BenchUut1();
   TraceOut_Operator_Alert[12] := BenchUut1.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[12] := BenchUut1.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 13:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[13] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := TRUE;
   BenchUut1.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[13] := BenchUut1.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[13] := BenchUut1.Weld_E_Stop_NC;
   TraceIn_DebounceTime[13] := BenchUut1.DebounceTime;
   BenchUut1();
   TraceOut_Operator_Alert[13] := BenchUut1.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[13] := BenchUut1.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 14:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[14] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := TRUE;
   BenchUut1.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[14] := BenchUut1.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[14] := BenchUut1.Weld_E_Stop_NC;
   TraceIn_DebounceTime[14] := BenchUut1.DebounceTime;
   BenchUut1();
   TraceOut_Operator_Alert[14] := BenchUut1.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[14] := BenchUut1.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 15:
  IF TIME() - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[15] := TIME_TO_UDINT(TIME() - BenchLastTime);
   BenchLastTime := TIME();
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := FALSE;
   BenchUut1.DebounceTime := T#1000ms;
   TraceIn_Gap_Exceeded[15] := BenchUut1.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[15] := BenchUut1.Weld_E_Stop_NC;
   TraceIn_DebounceTime[15] := BenchUut1.DebounceTime;
   BenchUut1();
   TraceOut_Operator_Alert[15] := BenchUut1.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[15] := BenchUut1.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 16 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
