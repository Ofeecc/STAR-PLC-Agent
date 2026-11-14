PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchLastTime : TIME := T#0ms;
 BenchClockReady : BOOL := FALSE;
 BenchCurrentTime : TIME := T#0ms;
 TraceDt : ARRAY[0..57] OF UDINT;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 BenchUut2 : FB_Task;
 BenchUut3 : FB_Task;
 BenchUut4 : FB_Task;
 BenchUut5 : FB_Task;
 BenchUut6 : FB_Task;
 TraceIn_DO_LOW : ARRAY[0..57] OF BOOL;
 TraceIn_AERATION_E_STOP_NC : ARRAY[0..57] OF BOOL;
 TraceOut_BLOWER_RUN : ARRAY[0..57] OF BOOL;
 TraceOut_AERATION_BLOWER_CYCLE_COUNT : ARRAY[0..57] OF UINT;
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
   BenchUut0.DO_LOW := FALSE;
   BenchUut0.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[0] := BenchUut0.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[0] := BenchUut0.AERATION_E_STOP_NC;
   BenchUut0();
   TraceOut_BLOWER_RUN[0] := BenchUut0.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[0] := BenchUut0.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 1:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[1] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.DO_LOW := TRUE;
   BenchUut0.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[1] := BenchUut0.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[1] := BenchUut0.AERATION_E_STOP_NC;
   BenchUut0();
   TraceOut_BLOWER_RUN[1] := BenchUut0.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[1] := BenchUut0.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 2:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[2] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.DO_LOW := TRUE;
   BenchUut0.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[2] := BenchUut0.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[2] := BenchUut0.AERATION_E_STOP_NC;
   BenchUut0();
   TraceOut_BLOWER_RUN[2] := BenchUut0.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[2] := BenchUut0.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 3:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[3] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.DO_LOW := TRUE;
   BenchUut0.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[3] := BenchUut0.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[3] := BenchUut0.AERATION_E_STOP_NC;
   BenchUut0();
   TraceOut_BLOWER_RUN[3] := BenchUut0.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[3] := BenchUut0.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 4:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[4] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.DO_LOW := TRUE;
   BenchUut0.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[4] := BenchUut0.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[4] := BenchUut0.AERATION_E_STOP_NC;
   BenchUut0();
   TraceOut_BLOWER_RUN[4] := BenchUut0.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[4] := BenchUut0.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 5:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[5] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.DO_LOW := FALSE;
   BenchUut0.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[5] := BenchUut0.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[5] := BenchUut0.AERATION_E_STOP_NC;
   BenchUut0();
   TraceOut_BLOWER_RUN[5] := BenchUut0.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[5] := BenchUut0.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 6:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[6] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.DO_LOW := TRUE;
   BenchUut0.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[6] := BenchUut0.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[6] := BenchUut0.AERATION_E_STOP_NC;
   BenchUut0();
   TraceOut_BLOWER_RUN[6] := BenchUut0.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[6] := BenchUut0.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 7:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[7] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.DO_LOW := TRUE;
   BenchUut0.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[7] := BenchUut0.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[7] := BenchUut0.AERATION_E_STOP_NC;
   BenchUut0();
   TraceOut_BLOWER_RUN[7] := BenchUut0.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[7] := BenchUut0.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 8:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[8] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.DO_LOW := TRUE;
   BenchUut1.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[8] := BenchUut1.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[8] := BenchUut1.AERATION_E_STOP_NC;
   BenchUut1();
   TraceOut_BLOWER_RUN[8] := BenchUut1.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[8] := BenchUut1.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 9:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4000) THEN
   TraceDt[9] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.DO_LOW := TRUE;
   BenchUut1.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[9] := BenchUut1.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[9] := BenchUut1.AERATION_E_STOP_NC;
   BenchUut1();
   TraceOut_BLOWER_RUN[9] := BenchUut1.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[9] := BenchUut1.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 10:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[10] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.DO_LOW := TRUE;
   BenchUut1.AERATION_E_STOP_NC := FALSE;
   TraceIn_DO_LOW[10] := BenchUut1.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[10] := BenchUut1.AERATION_E_STOP_NC;
   BenchUut1();
   TraceOut_BLOWER_RUN[10] := BenchUut1.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[10] := BenchUut1.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 11:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[11] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.DO_LOW := TRUE;
   BenchUut1.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[11] := BenchUut1.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[11] := BenchUut1.AERATION_E_STOP_NC;
   BenchUut1();
   TraceOut_BLOWER_RUN[11] := BenchUut1.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[11] := BenchUut1.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 12:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[12] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.DO_LOW := TRUE;
   BenchUut1.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[12] := BenchUut1.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[12] := BenchUut1.AERATION_E_STOP_NC;
   BenchUut1();
   TraceOut_BLOWER_RUN[12] := BenchUut1.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[12] := BenchUut1.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 13:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[13] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.DO_LOW := TRUE;
   BenchUut1.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[13] := BenchUut1.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[13] := BenchUut1.AERATION_E_STOP_NC;
   BenchUut1();
   TraceOut_BLOWER_RUN[13] := BenchUut1.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[13] := BenchUut1.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 14:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[14] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.DO_LOW := TRUE;
   BenchUut1.AERATION_E_STOP_NC := FALSE;
   TraceIn_DO_LOW[14] := BenchUut1.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[14] := BenchUut1.AERATION_E_STOP_NC;
   BenchUut1();
   TraceOut_BLOWER_RUN[14] := BenchUut1.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[14] := BenchUut1.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 15:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[15] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.DO_LOW := TRUE;
   BenchUut2.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[15] := BenchUut2.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[15] := BenchUut2.AERATION_E_STOP_NC;
   BenchUut2();
   TraceOut_BLOWER_RUN[15] := BenchUut2.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[15] := BenchUut2.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 16:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[16] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.DO_LOW := TRUE;
   BenchUut2.AERATION_E_STOP_NC := FALSE;
   TraceIn_DO_LOW[16] := BenchUut2.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[16] := BenchUut2.AERATION_E_STOP_NC;
   BenchUut2();
   TraceOut_BLOWER_RUN[16] := BenchUut2.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[16] := BenchUut2.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 17:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(10000) THEN
   TraceDt[17] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.DO_LOW := TRUE;
   BenchUut2.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[17] := BenchUut2.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[17] := BenchUut2.AERATION_E_STOP_NC;
   BenchUut2();
   TraceOut_BLOWER_RUN[17] := BenchUut2.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[17] := BenchUut2.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 18:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[18] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.DO_LOW := TRUE;
   BenchUut2.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[18] := BenchUut2.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[18] := BenchUut2.AERATION_E_STOP_NC;
   BenchUut2();
   TraceOut_BLOWER_RUN[18] := BenchUut2.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[18] := BenchUut2.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 19:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[19] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.DO_LOW := TRUE;
   BenchUut2.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[19] := BenchUut2.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[19] := BenchUut2.AERATION_E_STOP_NC;
   BenchUut2();
   TraceOut_BLOWER_RUN[19] := BenchUut2.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[19] := BenchUut2.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 20:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[20] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := TRUE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[20] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[20] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[20] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[20] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 21:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4500) THEN
   TraceDt[21] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := TRUE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[21] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[21] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[21] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[21] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 22:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[22] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := FALSE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[22] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[22] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[22] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[22] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 23:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[23] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := TRUE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[23] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[23] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[23] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[23] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 24:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[24] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := TRUE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[24] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[24] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[24] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[24] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 25:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[25] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := TRUE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[25] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[25] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[25] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[25] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 26:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[26] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := TRUE;
   BenchUut3.AERATION_E_STOP_NC := FALSE;
   TraceIn_DO_LOW[26] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[26] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[26] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[26] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 27:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[27] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := TRUE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[27] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[27] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[27] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[27] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 28:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[28] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := TRUE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[28] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[28] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[28] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[28] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 29:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[29] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := FALSE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[29] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[29] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[29] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[29] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 30:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[30] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := TRUE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[30] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[30] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[30] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[30] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 31:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[31] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.DO_LOW := TRUE;
   BenchUut3.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[31] := BenchUut3.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[31] := BenchUut3.AERATION_E_STOP_NC;
   BenchUut3();
   TraceOut_BLOWER_RUN[31] := BenchUut3.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[31] := BenchUut3.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 32:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[32] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.DO_LOW := TRUE;
   BenchUut4.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[32] := BenchUut4.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[32] := BenchUut4.AERATION_E_STOP_NC;
   BenchUut4();
   TraceOut_BLOWER_RUN[32] := BenchUut4.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[32] := BenchUut4.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 33:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[33] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.DO_LOW := TRUE;
   BenchUut4.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[33] := BenchUut4.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[33] := BenchUut4.AERATION_E_STOP_NC;
   BenchUut4();
   TraceOut_BLOWER_RUN[33] := BenchUut4.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[33] := BenchUut4.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 34:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[34] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.DO_LOW := FALSE;
   BenchUut4.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[34] := BenchUut4.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[34] := BenchUut4.AERATION_E_STOP_NC;
   BenchUut4();
   TraceOut_BLOWER_RUN[34] := BenchUut4.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[34] := BenchUut4.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 35:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[35] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.DO_LOW := TRUE;
   BenchUut4.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[35] := BenchUut4.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[35] := BenchUut4.AERATION_E_STOP_NC;
   BenchUut4();
   TraceOut_BLOWER_RUN[35] := BenchUut4.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[35] := BenchUut4.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 36:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[36] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.DO_LOW := TRUE;
   BenchUut4.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[36] := BenchUut4.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[36] := BenchUut4.AERATION_E_STOP_NC;
   BenchUut4();
   TraceOut_BLOWER_RUN[36] := BenchUut4.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[36] := BenchUut4.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 37:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(6000) THEN
   TraceDt[37] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.DO_LOW := TRUE;
   BenchUut4.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[37] := BenchUut4.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[37] := BenchUut4.AERATION_E_STOP_NC;
   BenchUut4();
   TraceOut_BLOWER_RUN[37] := BenchUut4.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[37] := BenchUut4.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 38:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[38] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.DO_LOW := TRUE;
   BenchUut4.AERATION_E_STOP_NC := FALSE;
   TraceIn_DO_LOW[38] := BenchUut4.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[38] := BenchUut4.AERATION_E_STOP_NC;
   BenchUut4();
   TraceOut_BLOWER_RUN[38] := BenchUut4.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[38] := BenchUut4.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 39:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[39] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.DO_LOW := TRUE;
   BenchUut4.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[39] := BenchUut4.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[39] := BenchUut4.AERATION_E_STOP_NC;
   BenchUut4();
   TraceOut_BLOWER_RUN[39] := BenchUut4.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[39] := BenchUut4.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 40:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(6000) THEN
   TraceDt[40] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.DO_LOW := TRUE;
   BenchUut4.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[40] := BenchUut4.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[40] := BenchUut4.AERATION_E_STOP_NC;
   BenchUut4();
   TraceOut_BLOWER_RUN[40] := BenchUut4.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[40] := BenchUut4.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 41:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[41] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.DO_LOW := TRUE;
   BenchUut5.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[41] := BenchUut5.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[41] := BenchUut5.AERATION_E_STOP_NC;
   BenchUut5();
   TraceOut_BLOWER_RUN[41] := BenchUut5.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[41] := BenchUut5.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 42:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[42] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.DO_LOW := TRUE;
   BenchUut5.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[42] := BenchUut5.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[42] := BenchUut5.AERATION_E_STOP_NC;
   BenchUut5();
   TraceOut_BLOWER_RUN[42] := BenchUut5.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[42] := BenchUut5.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 43:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[43] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.DO_LOW := FALSE;
   BenchUut5.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[43] := BenchUut5.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[43] := BenchUut5.AERATION_E_STOP_NC;
   BenchUut5();
   TraceOut_BLOWER_RUN[43] := BenchUut5.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[43] := BenchUut5.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 44:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[44] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.DO_LOW := TRUE;
   BenchUut5.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[44] := BenchUut5.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[44] := BenchUut5.AERATION_E_STOP_NC;
   BenchUut5();
   TraceOut_BLOWER_RUN[44] := BenchUut5.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[44] := BenchUut5.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 45:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[45] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.DO_LOW := TRUE;
   BenchUut5.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[45] := BenchUut5.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[45] := BenchUut5.AERATION_E_STOP_NC;
   BenchUut5();
   TraceOut_BLOWER_RUN[45] := BenchUut5.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[45] := BenchUut5.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 46:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[46] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.DO_LOW := TRUE;
   BenchUut5.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[46] := BenchUut5.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[46] := BenchUut5.AERATION_E_STOP_NC;
   BenchUut5();
   TraceOut_BLOWER_RUN[46] := BenchUut5.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[46] := BenchUut5.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 47:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[47] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.DO_LOW := TRUE;
   BenchUut5.AERATION_E_STOP_NC := FALSE;
   TraceIn_DO_LOW[47] := BenchUut5.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[47] := BenchUut5.AERATION_E_STOP_NC;
   BenchUut5();
   TraceOut_BLOWER_RUN[47] := BenchUut5.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[47] := BenchUut5.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 48:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[48] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.DO_LOW := TRUE;
   BenchUut6.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[48] := BenchUut6.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[48] := BenchUut6.AERATION_E_STOP_NC;
   BenchUut6();
   TraceOut_BLOWER_RUN[48] := BenchUut6.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[48] := BenchUut6.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 49:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[49] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.DO_LOW := TRUE;
   BenchUut6.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[49] := BenchUut6.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[49] := BenchUut6.AERATION_E_STOP_NC;
   BenchUut6();
   TraceOut_BLOWER_RUN[49] := BenchUut6.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[49] := BenchUut6.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 50:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[50] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.DO_LOW := TRUE;
   BenchUut6.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[50] := BenchUut6.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[50] := BenchUut6.AERATION_E_STOP_NC;
   BenchUut6();
   TraceOut_BLOWER_RUN[50] := BenchUut6.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[50] := BenchUut6.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 51:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[51] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.DO_LOW := FALSE;
   BenchUut6.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[51] := BenchUut6.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[51] := BenchUut6.AERATION_E_STOP_NC;
   BenchUut6();
   TraceOut_BLOWER_RUN[51] := BenchUut6.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[51] := BenchUut6.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 52:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[52] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.DO_LOW := TRUE;
   BenchUut6.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[52] := BenchUut6.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[52] := BenchUut6.AERATION_E_STOP_NC;
   BenchUut6();
   TraceOut_BLOWER_RUN[52] := BenchUut6.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[52] := BenchUut6.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 53:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[53] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.DO_LOW := TRUE;
   BenchUut6.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[53] := BenchUut6.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[53] := BenchUut6.AERATION_E_STOP_NC;
   BenchUut6();
   TraceOut_BLOWER_RUN[53] := BenchUut6.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[53] := BenchUut6.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 54:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[54] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.DO_LOW := FALSE;
   BenchUut6.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[54] := BenchUut6.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[54] := BenchUut6.AERATION_E_STOP_NC;
   BenchUut6();
   TraceOut_BLOWER_RUN[54] := BenchUut6.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[54] := BenchUut6.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 55:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[55] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.DO_LOW := TRUE;
   BenchUut6.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[55] := BenchUut6.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[55] := BenchUut6.AERATION_E_STOP_NC;
   BenchUut6();
   TraceOut_BLOWER_RUN[55] := BenchUut6.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[55] := BenchUut6.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 56:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[56] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.DO_LOW := TRUE;
   BenchUut6.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[56] := BenchUut6.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[56] := BenchUut6.AERATION_E_STOP_NC;
   BenchUut6();
   TraceOut_BLOWER_RUN[56] := BenchUut6.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[56] := BenchUut6.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 57:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[57] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.DO_LOW := TRUE;
   BenchUut6.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[57] := BenchUut6.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[57] := BenchUut6.AERATION_E_STOP_NC;
   BenchUut6();
   TraceOut_BLOWER_RUN[57] := BenchUut6.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[57] := BenchUut6.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 58 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
