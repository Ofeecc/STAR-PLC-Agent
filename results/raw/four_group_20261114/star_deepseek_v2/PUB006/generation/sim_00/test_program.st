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
 TraceIn_DO_LOW : ARRAY[0..15] OF BOOL;
 TraceIn_AERATION_E_STOP_NC : ARRAY[0..15] OF BOOL;
 TraceOut_BLOWER_RUN : ARRAY[0..15] OF BOOL;
 TraceOut_AERATION_BLOWER_CYCLE_COUNT : ARRAY[0..15] OF UINT;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(3000) THEN
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4000) THEN
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[14] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.DO_LOW := TRUE;
   BenchUut1.AERATION_E_STOP_NC := TRUE;
   TraceIn_DO_LOW[14] := BenchUut1.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[14] := BenchUut1.AERATION_E_STOP_NC;
   BenchUut1();
   TraceOut_BLOWER_RUN[14] := BenchUut1.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[14] := BenchUut1.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 15:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[15] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.DO_LOW := TRUE;
   BenchUut1.AERATION_E_STOP_NC := FALSE;
   TraceIn_DO_LOW[15] := BenchUut1.DO_LOW;
   TraceIn_AERATION_E_STOP_NC[15] := BenchUut1.AERATION_E_STOP_NC;
   BenchUut1();
   TraceOut_BLOWER_RUN[15] := BenchUut1.BLOWER_RUN;
   TraceOut_AERATION_BLOWER_CYCLE_COUNT[15] := BenchUut1.AERATION_BLOWER_CYCLE_COUNT;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 16 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
