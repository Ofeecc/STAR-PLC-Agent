PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_Start : ARRAY[0..13] OF BOOL;
 TraceIn_Stop : ARRAY[0..13] OF BOOL;
 TraceIn_GuardClosed : ARRAY[0..13] OF BOOL;
 TraceOut_Run : ARRAY[0..13] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.Start := TRUE;
   BenchUut0.Stop := FALSE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[0] := BenchUut0.Start;
   TraceIn_Stop[0] := BenchUut0.Stop;
   TraceIn_GuardClosed[0] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[0] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[1] := BenchUut0.Start;
   TraceIn_Stop[1] := BenchUut0.Stop;
   TraceIn_GuardClosed[1] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[1] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[2] := BenchUut0.Start;
   TraceIn_Stop[2] := BenchUut0.Stop;
   TraceIn_GuardClosed[2] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[2] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := TRUE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[3] := BenchUut0.Start;
   TraceIn_Stop[3] := BenchUut0.Stop;
   TraceIn_GuardClosed[3] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[3] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[4] := BenchUut0.Start;
   TraceIn_Stop[4] := BenchUut0.Stop;
   TraceIn_GuardClosed[4] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[4] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut0.Start := TRUE;
   BenchUut0.Stop := FALSE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[5] := BenchUut0.Start;
   TraceIn_Stop[5] := BenchUut0.Stop;
   TraceIn_GuardClosed[5] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[5] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := FALSE;
   TraceIn_Start[6] := BenchUut1.Start;
   TraceIn_Stop[6] := BenchUut1.Stop;
   TraceIn_GuardClosed[6] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[6] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := TRUE;
   TraceIn_Start[7] := BenchUut1.Start;
   TraceIn_Stop[7] := BenchUut1.Stop;
   TraceIn_GuardClosed[7] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[7] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.Start := FALSE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := TRUE;
   TraceIn_Start[8] := BenchUut1.Start;
   TraceIn_Stop[8] := BenchUut1.Stop;
   TraceIn_GuardClosed[8] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[8] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.Start := FALSE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := FALSE;
   TraceIn_Start[9] := BenchUut1.Start;
   TraceIn_Stop[9] := BenchUut1.Stop;
   TraceIn_GuardClosed[9] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[9] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.Start := FALSE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := TRUE;
   TraceIn_Start[10] := BenchUut1.Start;
   TraceIn_Stop[10] := BenchUut1.Stop;
   TraceIn_GuardClosed[10] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[10] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := TRUE;
   TraceIn_Start[11] := BenchUut1.Start;
   TraceIn_Stop[11] := BenchUut1.Stop;
   TraceIn_GuardClosed[11] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[11] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := TRUE;
   BenchUut1.GuardClosed := TRUE;
   TraceIn_Start[12] := BenchUut1.Start;
   TraceIn_Stop[12] := BenchUut1.Stop;
   TraceIn_GuardClosed[12] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[12] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut1.Start := FALSE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := TRUE;
   TraceIn_Start[13] := BenchUut1.Start;
   TraceIn_Stop[13] := BenchUut1.Stop;
   TraceIn_GuardClosed[13] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[13] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 14 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
