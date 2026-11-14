PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchLastTime : TIME := T#0ms;
 BenchClockReady : BOOL := FALSE;
 BenchCurrentTime : TIME := T#0ms;
 TraceDt : ARRAY[0..8] OF UDINT;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_Enable : ARRAY[0..8] OF BOOL;
 TraceIn_Tick : ARRAY[0..8] OF BOOL;
 TraceOut_Red : ARRAY[0..8] OF BOOL;
 TraceOut_Green : ARRAY[0..8] OF BOOL;
 TraceOut_Amber : ARRAY[0..8] OF BOOL;
 TraceOut_Phase : ARRAY[0..8] OF USINT;
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
   BenchUut0.Enable := TRUE;
   BenchUut0.Tick := TRUE;
   TraceIn_Enable[0] := BenchUut0.Enable;
   TraceIn_Tick[0] := BenchUut0.Tick;
   BenchUut0();
   TraceOut_Red[0] := BenchUut0.Red;
   TraceOut_Green[0] := BenchUut0.Green;
   TraceOut_Amber[0] := BenchUut0.Amber;
   TraceOut_Phase[0] := BenchUut0.Phase;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 1:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[1] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[1] := BenchUut1.Enable;
   TraceIn_Tick[1] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[1] := BenchUut1.Red;
   TraceOut_Green[1] := BenchUut1.Green;
   TraceOut_Amber[1] := BenchUut1.Amber;
   TraceOut_Phase[1] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 2:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[2] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[2] := BenchUut1.Enable;
   TraceIn_Tick[2] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[2] := BenchUut1.Red;
   TraceOut_Green[2] := BenchUut1.Green;
   TraceOut_Amber[2] := BenchUut1.Amber;
   TraceOut_Phase[2] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 3:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[3] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[3] := BenchUut1.Enable;
   TraceIn_Tick[3] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[3] := BenchUut1.Red;
   TraceOut_Green[3] := BenchUut1.Green;
   TraceOut_Amber[3] := BenchUut1.Amber;
   TraceOut_Phase[3] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 4:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[4] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[4] := BenchUut1.Enable;
   TraceIn_Tick[4] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[4] := BenchUut1.Red;
   TraceOut_Green[4] := BenchUut1.Green;
   TraceOut_Amber[4] := BenchUut1.Amber;
   TraceOut_Phase[4] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 5:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[5] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Enable := FALSE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[5] := BenchUut1.Enable;
   TraceIn_Tick[5] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[5] := BenchUut1.Red;
   TraceOut_Green[5] := BenchUut1.Green;
   TraceOut_Amber[5] := BenchUut1.Amber;
   TraceOut_Phase[5] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 6:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[6] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[6] := BenchUut1.Enable;
   TraceIn_Tick[6] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[6] := BenchUut1.Red;
   TraceOut_Green[6] := BenchUut1.Green;
   TraceOut_Amber[6] := BenchUut1.Amber;
   TraceOut_Phase[6] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 7:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[7] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[7] := BenchUut1.Enable;
   TraceIn_Tick[7] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[7] := BenchUut1.Red;
   TraceOut_Green[7] := BenchUut1.Green;
   TraceOut_Amber[7] := BenchUut1.Amber;
   TraceOut_Phase[7] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 8:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[8] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[8] := BenchUut1.Enable;
   TraceIn_Tick[8] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[8] := BenchUut1.Red;
   TraceOut_Green[8] := BenchUut1.Green;
   TraceOut_Amber[8] := BenchUut1.Amber;
   TraceOut_Phase[8] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 9 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
