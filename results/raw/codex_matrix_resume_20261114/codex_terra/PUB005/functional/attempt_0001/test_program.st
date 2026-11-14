PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchLastTime : TIME := T#0ms;
 BenchClockReady : BOOL := FALSE;
 BenchCurrentTime : TIME := T#0ms;
 TraceDt : ARRAY[0..47] OF UDINT;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 BenchUut2 : FB_Task;
 BenchUut3 : FB_Task;
 BenchUut4 : FB_Task;
 BenchUut5 : FB_Task;
 BenchUut6 : FB_Task;
 TraceIn_Gap_Exceeded : ARRAY[0..47] OF BOOL;
 TraceIn_Weld_E_Stop_NC : ARRAY[0..47] OF BOOL;
 TraceIn_DebounceTime : ARRAY[0..47] OF TIME;
 TraceOut_Operator_Alert : ARRAY[0..47] OF BOOL;
 TraceOut_Weld_Soft_Start_Active : ARRAY[0..47] OF BOOL;
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
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4000) THEN
   TraceDt[1] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[2] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[3] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[4] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.Gap_Exceeded := TRUE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[5] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.Gap_Exceeded := FALSE;
   BenchUut0.Weld_E_Stop_NC := TRUE;
   BenchUut0.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[6] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := FALSE;
   BenchUut1.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[6] := BenchUut1.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[6] := BenchUut1.Weld_E_Stop_NC;
   TraceIn_DebounceTime[6] := BenchUut1.DebounceTime;
   BenchUut1();
   TraceOut_Operator_Alert[6] := BenchUut1.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[6] := BenchUut1.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 7:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[7] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := FALSE;
   BenchUut1.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[7] := BenchUut1.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[7] := BenchUut1.Weld_E_Stop_NC;
   TraceIn_DebounceTime[7] := BenchUut1.DebounceTime;
   BenchUut1();
   TraceOut_Operator_Alert[7] := BenchUut1.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[7] := BenchUut1.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 8:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[8] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := TRUE;
   BenchUut1.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[9] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := TRUE;
   BenchUut1.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[10] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := FALSE;
   BenchUut1.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[11] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := TRUE;
   BenchUut1.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[12] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := TRUE;
   BenchUut1.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[13] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Gap_Exceeded := TRUE;
   BenchUut1.Weld_E_Stop_NC := TRUE;
   BenchUut1.DebounceTime := T#2s;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[14] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.Gap_Exceeded := TRUE;
   BenchUut2.Weld_E_Stop_NC := TRUE;
   BenchUut2.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[14] := BenchUut2.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[14] := BenchUut2.Weld_E_Stop_NC;
   TraceIn_DebounceTime[14] := BenchUut2.DebounceTime;
   BenchUut2();
   TraceOut_Operator_Alert[14] := BenchUut2.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[14] := BenchUut2.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 15:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[15] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.Gap_Exceeded := TRUE;
   BenchUut2.Weld_E_Stop_NC := TRUE;
   BenchUut2.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[15] := BenchUut2.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[15] := BenchUut2.Weld_E_Stop_NC;
   TraceIn_DebounceTime[15] := BenchUut2.DebounceTime;
   BenchUut2();
   TraceOut_Operator_Alert[15] := BenchUut2.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[15] := BenchUut2.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 16:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[16] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.Gap_Exceeded := TRUE;
   BenchUut2.Weld_E_Stop_NC := TRUE;
   BenchUut2.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[16] := BenchUut2.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[16] := BenchUut2.Weld_E_Stop_NC;
   TraceIn_DebounceTime[16] := BenchUut2.DebounceTime;
   BenchUut2();
   TraceOut_Operator_Alert[16] := BenchUut2.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[16] := BenchUut2.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 17:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1500) THEN
   TraceDt[17] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.Gap_Exceeded := TRUE;
   BenchUut2.Weld_E_Stop_NC := TRUE;
   BenchUut2.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[17] := BenchUut2.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[17] := BenchUut2.Weld_E_Stop_NC;
   TraceIn_DebounceTime[17] := BenchUut2.DebounceTime;
   BenchUut2();
   TraceOut_Operator_Alert[17] := BenchUut2.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[17] := BenchUut2.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 18:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[18] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.Gap_Exceeded := FALSE;
   BenchUut2.Weld_E_Stop_NC := TRUE;
   BenchUut2.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[18] := BenchUut2.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[18] := BenchUut2.Weld_E_Stop_NC;
   TraceIn_DebounceTime[18] := BenchUut2.DebounceTime;
   BenchUut2();
   TraceOut_Operator_Alert[18] := BenchUut2.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[18] := BenchUut2.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 19:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[19] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.Gap_Exceeded := TRUE;
   BenchUut2.Weld_E_Stop_NC := TRUE;
   BenchUut2.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[19] := BenchUut2.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[19] := BenchUut2.Weld_E_Stop_NC;
   TraceIn_DebounceTime[19] := BenchUut2.DebounceTime;
   BenchUut2();
   TraceOut_Operator_Alert[19] := BenchUut2.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[19] := BenchUut2.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 20:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1999) THEN
   TraceDt[20] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.Gap_Exceeded := TRUE;
   BenchUut2.Weld_E_Stop_NC := TRUE;
   BenchUut2.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[20] := BenchUut2.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[20] := BenchUut2.Weld_E_Stop_NC;
   TraceIn_DebounceTime[20] := BenchUut2.DebounceTime;
   BenchUut2();
   TraceOut_Operator_Alert[20] := BenchUut2.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[20] := BenchUut2.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 21:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[21] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.Gap_Exceeded := TRUE;
   BenchUut2.Weld_E_Stop_NC := FALSE;
   BenchUut2.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[21] := BenchUut2.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[21] := BenchUut2.Weld_E_Stop_NC;
   TraceIn_DebounceTime[21] := BenchUut2.DebounceTime;
   BenchUut2();
   TraceOut_Operator_Alert[21] := BenchUut2.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[21] := BenchUut2.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 22:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[22] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.Gap_Exceeded := TRUE;
   BenchUut2.Weld_E_Stop_NC := TRUE;
   BenchUut2.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[22] := BenchUut2.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[22] := BenchUut2.Weld_E_Stop_NC;
   TraceIn_DebounceTime[22] := BenchUut2.DebounceTime;
   BenchUut2();
   TraceOut_Operator_Alert[22] := BenchUut2.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[22] := BenchUut2.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 23:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[23] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.Gap_Exceeded := TRUE;
   BenchUut2.Weld_E_Stop_NC := TRUE;
   BenchUut2.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[23] := BenchUut2.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[23] := BenchUut2.Weld_E_Stop_NC;
   TraceIn_DebounceTime[23] := BenchUut2.DebounceTime;
   BenchUut2();
   TraceOut_Operator_Alert[23] := BenchUut2.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[23] := BenchUut2.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 24:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[24] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.Gap_Exceeded := TRUE;
   BenchUut3.Weld_E_Stop_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[24] := BenchUut3.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[24] := BenchUut3.Weld_E_Stop_NC;
   TraceIn_DebounceTime[24] := BenchUut3.DebounceTime;
   BenchUut3();
   TraceOut_Operator_Alert[24] := BenchUut3.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[24] := BenchUut3.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 25:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[25] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.Gap_Exceeded := TRUE;
   BenchUut3.Weld_E_Stop_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[25] := BenchUut3.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[25] := BenchUut3.Weld_E_Stop_NC;
   TraceIn_DebounceTime[25] := BenchUut3.DebounceTime;
   BenchUut3();
   TraceOut_Operator_Alert[25] := BenchUut3.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[25] := BenchUut3.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 26:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[26] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.Gap_Exceeded := TRUE;
   BenchUut3.Weld_E_Stop_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[26] := BenchUut3.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[26] := BenchUut3.Weld_E_Stop_NC;
   TraceIn_DebounceTime[26] := BenchUut3.DebounceTime;
   BenchUut3();
   TraceOut_Operator_Alert[26] := BenchUut3.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[26] := BenchUut3.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 27:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[27] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.Gap_Exceeded := FALSE;
   BenchUut3.Weld_E_Stop_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[27] := BenchUut3.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[27] := BenchUut3.Weld_E_Stop_NC;
   TraceIn_DebounceTime[27] := BenchUut3.DebounceTime;
   BenchUut3();
   TraceOut_Operator_Alert[27] := BenchUut3.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[27] := BenchUut3.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 28:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[28] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.Gap_Exceeded := TRUE;
   BenchUut3.Weld_E_Stop_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[28] := BenchUut3.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[28] := BenchUut3.Weld_E_Stop_NC;
   TraceIn_DebounceTime[28] := BenchUut3.DebounceTime;
   BenchUut3();
   TraceOut_Operator_Alert[28] := BenchUut3.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[28] := BenchUut3.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 29:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[29] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.Gap_Exceeded := TRUE;
   BenchUut3.Weld_E_Stop_NC := TRUE;
   BenchUut3.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[29] := BenchUut3.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[29] := BenchUut3.Weld_E_Stop_NC;
   TraceIn_DebounceTime[29] := BenchUut3.DebounceTime;
   BenchUut3();
   TraceOut_Operator_Alert[29] := BenchUut3.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[29] := BenchUut3.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 30:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[30] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.Gap_Exceeded := TRUE;
   BenchUut4.Weld_E_Stop_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[30] := BenchUut4.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[30] := BenchUut4.Weld_E_Stop_NC;
   TraceIn_DebounceTime[30] := BenchUut4.DebounceTime;
   BenchUut4();
   TraceOut_Operator_Alert[30] := BenchUut4.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[30] := BenchUut4.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 31:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[31] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.Gap_Exceeded := TRUE;
   BenchUut4.Weld_E_Stop_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[31] := BenchUut4.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[31] := BenchUut4.Weld_E_Stop_NC;
   TraceIn_DebounceTime[31] := BenchUut4.DebounceTime;
   BenchUut4();
   TraceOut_Operator_Alert[31] := BenchUut4.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[31] := BenchUut4.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 32:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[32] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.Gap_Exceeded := TRUE;
   BenchUut4.Weld_E_Stop_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[32] := BenchUut4.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[32] := BenchUut4.Weld_E_Stop_NC;
   TraceIn_DebounceTime[32] := BenchUut4.DebounceTime;
   BenchUut4();
   TraceOut_Operator_Alert[32] := BenchUut4.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[32] := BenchUut4.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 33:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1999) THEN
   TraceDt[33] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.Gap_Exceeded := TRUE;
   BenchUut4.Weld_E_Stop_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[33] := BenchUut4.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[33] := BenchUut4.Weld_E_Stop_NC;
   TraceIn_DebounceTime[33] := BenchUut4.DebounceTime;
   BenchUut4();
   TraceOut_Operator_Alert[33] := BenchUut4.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[33] := BenchUut4.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 34:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[34] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.Gap_Exceeded := TRUE;
   BenchUut4.Weld_E_Stop_NC := TRUE;
   BenchUut4.DebounceTime := T#2s;
   TraceIn_Gap_Exceeded[34] := BenchUut4.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[34] := BenchUut4.Weld_E_Stop_NC;
   TraceIn_DebounceTime[34] := BenchUut4.DebounceTime;
   BenchUut4();
   TraceOut_Operator_Alert[34] := BenchUut4.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[34] := BenchUut4.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 35:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[35] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.Gap_Exceeded := TRUE;
   BenchUut5.Weld_E_Stop_NC := TRUE;
   BenchUut5.DebounceTime := T#1ms;
   TraceIn_Gap_Exceeded[35] := BenchUut5.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[35] := BenchUut5.Weld_E_Stop_NC;
   TraceIn_DebounceTime[35] := BenchUut5.DebounceTime;
   BenchUut5();
   TraceOut_Operator_Alert[35] := BenchUut5.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[35] := BenchUut5.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 36:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[36] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.Gap_Exceeded := TRUE;
   BenchUut5.Weld_E_Stop_NC := TRUE;
   BenchUut5.DebounceTime := T#1ms;
   TraceIn_Gap_Exceeded[36] := BenchUut5.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[36] := BenchUut5.Weld_E_Stop_NC;
   TraceIn_DebounceTime[36] := BenchUut5.DebounceTime;
   BenchUut5();
   TraceOut_Operator_Alert[36] := BenchUut5.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[36] := BenchUut5.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 37:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[37] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.Gap_Exceeded := TRUE;
   BenchUut5.Weld_E_Stop_NC := TRUE;
   BenchUut5.DebounceTime := T#1ms;
   TraceIn_Gap_Exceeded[37] := BenchUut5.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[37] := BenchUut5.Weld_E_Stop_NC;
   TraceIn_DebounceTime[37] := BenchUut5.DebounceTime;
   BenchUut5();
   TraceOut_Operator_Alert[37] := BenchUut5.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[37] := BenchUut5.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 38:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[38] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.Gap_Exceeded := TRUE;
   BenchUut5.Weld_E_Stop_NC := FALSE;
   BenchUut5.DebounceTime := T#1ms;
   TraceIn_Gap_Exceeded[38] := BenchUut5.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[38] := BenchUut5.Weld_E_Stop_NC;
   TraceIn_DebounceTime[38] := BenchUut5.DebounceTime;
   BenchUut5();
   TraceOut_Operator_Alert[38] := BenchUut5.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[38] := BenchUut5.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 39:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[39] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.Gap_Exceeded := TRUE;
   BenchUut5.Weld_E_Stop_NC := TRUE;
   BenchUut5.DebounceTime := T#1ms;
   TraceIn_Gap_Exceeded[39] := BenchUut5.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[39] := BenchUut5.Weld_E_Stop_NC;
   TraceIn_DebounceTime[39] := BenchUut5.DebounceTime;
   BenchUut5();
   TraceOut_Operator_Alert[39] := BenchUut5.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[39] := BenchUut5.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 40:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[40] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.Gap_Exceeded := TRUE;
   BenchUut5.Weld_E_Stop_NC := TRUE;
   BenchUut5.DebounceTime := T#1ms;
   TraceIn_Gap_Exceeded[40] := BenchUut5.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[40] := BenchUut5.Weld_E_Stop_NC;
   TraceIn_DebounceTime[40] := BenchUut5.DebounceTime;
   BenchUut5();
   TraceOut_Operator_Alert[40] := BenchUut5.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[40] := BenchUut5.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 41:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[41] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.Gap_Exceeded := FALSE;
   BenchUut6.Weld_E_Stop_NC := TRUE;
   BenchUut6.DebounceTime := T#500ms;
   TraceIn_Gap_Exceeded[41] := BenchUut6.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[41] := BenchUut6.Weld_E_Stop_NC;
   TraceIn_DebounceTime[41] := BenchUut6.DebounceTime;
   BenchUut6();
   TraceOut_Operator_Alert[41] := BenchUut6.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[41] := BenchUut6.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 42:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[42] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.Gap_Exceeded := FALSE;
   BenchUut6.Weld_E_Stop_NC := TRUE;
   BenchUut6.DebounceTime := T#500ms;
   TraceIn_Gap_Exceeded[42] := BenchUut6.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[42] := BenchUut6.Weld_E_Stop_NC;
   TraceIn_DebounceTime[42] := BenchUut6.DebounceTime;
   BenchUut6();
   TraceOut_Operator_Alert[42] := BenchUut6.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[42] := BenchUut6.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 43:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[43] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.Gap_Exceeded := TRUE;
   BenchUut6.Weld_E_Stop_NC := TRUE;
   BenchUut6.DebounceTime := T#500ms;
   TraceIn_Gap_Exceeded[43] := BenchUut6.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[43] := BenchUut6.Weld_E_Stop_NC;
   TraceIn_DebounceTime[43] := BenchUut6.DebounceTime;
   BenchUut6();
   TraceOut_Operator_Alert[43] := BenchUut6.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[43] := BenchUut6.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 44:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(400) THEN
   TraceDt[44] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.Gap_Exceeded := FALSE;
   BenchUut6.Weld_E_Stop_NC := TRUE;
   BenchUut6.DebounceTime := T#500ms;
   TraceIn_Gap_Exceeded[44] := BenchUut6.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[44] := BenchUut6.Weld_E_Stop_NC;
   TraceIn_DebounceTime[44] := BenchUut6.DebounceTime;
   BenchUut6();
   TraceOut_Operator_Alert[44] := BenchUut6.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[44] := BenchUut6.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 45:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[45] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.Gap_Exceeded := TRUE;
   BenchUut6.Weld_E_Stop_NC := TRUE;
   BenchUut6.DebounceTime := T#500ms;
   TraceIn_Gap_Exceeded[45] := BenchUut6.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[45] := BenchUut6.Weld_E_Stop_NC;
   TraceIn_DebounceTime[45] := BenchUut6.DebounceTime;
   BenchUut6();
   TraceOut_Operator_Alert[45] := BenchUut6.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[45] := BenchUut6.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 46:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(499) THEN
   TraceDt[46] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.Gap_Exceeded := TRUE;
   BenchUut6.Weld_E_Stop_NC := TRUE;
   BenchUut6.DebounceTime := T#500ms;
   TraceIn_Gap_Exceeded[46] := BenchUut6.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[46] := BenchUut6.Weld_E_Stop_NC;
   TraceIn_DebounceTime[46] := BenchUut6.DebounceTime;
   BenchUut6();
   TraceOut_Operator_Alert[46] := BenchUut6.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[46] := BenchUut6.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 47:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[47] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.Gap_Exceeded := TRUE;
   BenchUut6.Weld_E_Stop_NC := TRUE;
   BenchUut6.DebounceTime := T#500ms;
   TraceIn_Gap_Exceeded[47] := BenchUut6.Gap_Exceeded;
   TraceIn_Weld_E_Stop_NC[47] := BenchUut6.Weld_E_Stop_NC;
   TraceIn_DebounceTime[47] := BenchUut6.DebounceTime;
   BenchUut6();
   TraceOut_Operator_Alert[47] := BenchUut6.Operator_Alert;
   TraceOut_Weld_Soft_Start_Active[47] := BenchUut6.Weld_Soft_Start_Active;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 48 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
