PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn0 : ARRAY[0..9] OF BOOL;
 TraceIn1 : ARRAY[0..9] OF BOOL;
 TraceIn2 : ARRAY[0..9] OF BOOL;
 TraceOut0 : ARRAY[0..9] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
  BenchUut0.Start := FALSE;
  BenchUut0.Stop := FALSE;
  BenchUut0.GuardClosed := TRUE;
  TraceIn0[0] := BenchUut0.Start;
  TraceIn1[0] := BenchUut0.Stop;
  TraceIn2[0] := BenchUut0.GuardClosed;
  BenchUut0();
  TraceOut0[0] := BenchUut0.Run;
  BenchCalls := BenchCalls + 1;
 1:
  BenchUut0.Start := TRUE;
  BenchUut0.Stop := FALSE;
  BenchUut0.GuardClosed := TRUE;
  TraceIn0[1] := BenchUut0.Start;
  TraceIn1[1] := BenchUut0.Stop;
  TraceIn2[1] := BenchUut0.GuardClosed;
  BenchUut0();
  TraceOut0[1] := BenchUut0.Run;
  BenchCalls := BenchCalls + 1;
 2:
  BenchUut0.Start := FALSE;
  BenchUut0.Stop := FALSE;
  BenchUut0.GuardClosed := TRUE;
  TraceIn0[2] := BenchUut0.Start;
  TraceIn1[2] := BenchUut0.Stop;
  TraceIn2[2] := BenchUut0.GuardClosed;
  BenchUut0();
  TraceOut0[2] := BenchUut0.Run;
  BenchCalls := BenchCalls + 1;
 3:
  BenchUut0.Start := FALSE;
  BenchUut0.Stop := TRUE;
  BenchUut0.GuardClosed := TRUE;
  TraceIn0[3] := BenchUut0.Start;
  TraceIn1[3] := BenchUut0.Stop;
  TraceIn2[3] := BenchUut0.GuardClosed;
  BenchUut0();
  TraceOut0[3] := BenchUut0.Run;
  BenchCalls := BenchCalls + 1;
 4:
  BenchUut0.Start := FALSE;
  BenchUut0.Stop := FALSE;
  BenchUut0.GuardClosed := TRUE;
  TraceIn0[4] := BenchUut0.Start;
  TraceIn1[4] := BenchUut0.Stop;
  TraceIn2[4] := BenchUut0.GuardClosed;
  BenchUut0();
  TraceOut0[4] := BenchUut0.Run;
  BenchCalls := BenchCalls + 1;
 5:
  BenchUut1.Start := TRUE;
  BenchUut1.Stop := TRUE;
  BenchUut1.GuardClosed := TRUE;
  TraceIn0[5] := BenchUut1.Start;
  TraceIn1[5] := BenchUut1.Stop;
  TraceIn2[5] := BenchUut1.GuardClosed;
  BenchUut1();
  TraceOut0[5] := BenchUut1.Run;
  BenchCalls := BenchCalls + 1;
 6:
  BenchUut1.Start := TRUE;
  BenchUut1.Stop := FALSE;
  BenchUut1.GuardClosed := FALSE;
  TraceIn0[6] := BenchUut1.Start;
  TraceIn1[6] := BenchUut1.Stop;
  TraceIn2[6] := BenchUut1.GuardClosed;
  BenchUut1();
  TraceOut0[6] := BenchUut1.Run;
  BenchCalls := BenchCalls + 1;
 7:
  BenchUut1.Start := TRUE;
  BenchUut1.Stop := FALSE;
  BenchUut1.GuardClosed := TRUE;
  TraceIn0[7] := BenchUut1.Start;
  TraceIn1[7] := BenchUut1.Stop;
  TraceIn2[7] := BenchUut1.GuardClosed;
  BenchUut1();
  TraceOut0[7] := BenchUut1.Run;
  BenchCalls := BenchCalls + 1;
 8:
  BenchUut1.Start := FALSE;
  BenchUut1.Stop := FALSE;
  BenchUut1.GuardClosed := FALSE;
  TraceIn0[8] := BenchUut1.Start;
  TraceIn1[8] := BenchUut1.Stop;
  TraceIn2[8] := BenchUut1.GuardClosed;
  BenchUut1();
  TraceOut0[8] := BenchUut1.Run;
  BenchCalls := BenchCalls + 1;
 9:
  BenchUut1.Start := FALSE;
  BenchUut1.Stop := FALSE;
  BenchUut1.GuardClosed := TRUE;
  TraceIn0[9] := BenchUut1.Start;
  TraceIn1[9] := BenchUut1.Stop;
  TraceIn2[9] := BenchUut1.GuardClosed;
  BenchUut1();
  TraceOut0[9] := BenchUut1.Run;
  BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 10 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
