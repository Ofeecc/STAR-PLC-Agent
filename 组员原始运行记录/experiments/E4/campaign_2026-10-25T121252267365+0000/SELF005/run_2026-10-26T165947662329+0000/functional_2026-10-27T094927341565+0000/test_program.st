PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn0 : ARRAY[0..11] OF BOOL;
 TraceIn1 : ARRAY[0..11] OF BOOL;
 TraceOut0 : ARRAY[0..11] OF BOOL;
 TraceOut1 : ARRAY[0..11] OF BOOL;
 TraceOut2 : ARRAY[0..11] OF BOOL;
 TraceOut3 : ARRAY[0..11] OF USINT;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
  BenchUut0.Enable := TRUE;
  BenchUut0.Tick := TRUE;
  TraceIn0[0] := BenchUut0.Enable;
  TraceIn1[0] := BenchUut0.Tick;
  BenchUut0();
  TraceOut0[0] := BenchUut0.Red;
  TraceOut1[0] := BenchUut0.Green;
  TraceOut2[0] := BenchUut0.Amber;
  TraceOut3[0] := BenchUut0.Phase;
  BenchCalls := BenchCalls + 1;
 1:
  BenchUut0.Enable := TRUE;
  BenchUut0.Tick := FALSE;
  TraceIn0[1] := BenchUut0.Enable;
  TraceIn1[1] := BenchUut0.Tick;
  BenchUut0();
  TraceOut0[1] := BenchUut0.Red;
  TraceOut1[1] := BenchUut0.Green;
  TraceOut2[1] := BenchUut0.Amber;
  TraceOut3[1] := BenchUut0.Phase;
  BenchCalls := BenchCalls + 1;
 2:
  BenchUut0.Enable := TRUE;
  BenchUut0.Tick := TRUE;
  TraceIn0[2] := BenchUut0.Enable;
  TraceIn1[2] := BenchUut0.Tick;
  BenchUut0();
  TraceOut0[2] := BenchUut0.Red;
  TraceOut1[2] := BenchUut0.Green;
  TraceOut2[2] := BenchUut0.Amber;
  TraceOut3[2] := BenchUut0.Phase;
  BenchCalls := BenchCalls + 1;
 3:
  BenchUut0.Enable := TRUE;
  BenchUut0.Tick := TRUE;
  TraceIn0[3] := BenchUut0.Enable;
  TraceIn1[3] := BenchUut0.Tick;
  BenchUut0();
  TraceOut0[3] := BenchUut0.Red;
  TraceOut1[3] := BenchUut0.Green;
  TraceOut2[3] := BenchUut0.Amber;
  TraceOut3[3] := BenchUut0.Phase;
  BenchCalls := BenchCalls + 1;
 4:
  BenchUut0.Enable := TRUE;
  BenchUut0.Tick := TRUE;
  TraceIn0[4] := BenchUut0.Enable;
  TraceIn1[4] := BenchUut0.Tick;
  BenchUut0();
  TraceOut0[4] := BenchUut0.Red;
  TraceOut1[4] := BenchUut0.Green;
  TraceOut2[4] := BenchUut0.Amber;
  TraceOut3[4] := BenchUut0.Phase;
  BenchCalls := BenchCalls + 1;
 5:
  BenchUut0.Enable := TRUE;
  BenchUut0.Tick := TRUE;
  TraceIn0[5] := BenchUut0.Enable;
  TraceIn1[5] := BenchUut0.Tick;
  BenchUut0();
  TraceOut0[5] := BenchUut0.Red;
  TraceOut1[5] := BenchUut0.Green;
  TraceOut2[5] := BenchUut0.Amber;
  TraceOut3[5] := BenchUut0.Phase;
  BenchCalls := BenchCalls + 1;
 6:
  BenchUut0.Enable := TRUE;
  BenchUut0.Tick := TRUE;
  TraceIn0[6] := BenchUut0.Enable;
  TraceIn1[6] := BenchUut0.Tick;
  BenchUut0();
  TraceOut0[6] := BenchUut0.Red;
  TraceOut1[6] := BenchUut0.Green;
  TraceOut2[6] := BenchUut0.Amber;
  TraceOut3[6] := BenchUut0.Phase;
  BenchCalls := BenchCalls + 1;
 7:
  BenchUut1.Enable := TRUE;
  BenchUut1.Tick := TRUE;
  TraceIn0[7] := BenchUut1.Enable;
  TraceIn1[7] := BenchUut1.Tick;
  BenchUut1();
  TraceOut0[7] := BenchUut1.Red;
  TraceOut1[7] := BenchUut1.Green;
  TraceOut2[7] := BenchUut1.Amber;
  TraceOut3[7] := BenchUut1.Phase;
  BenchCalls := BenchCalls + 1;
 8:
  BenchUut1.Enable := TRUE;
  BenchUut1.Tick := TRUE;
  TraceIn0[8] := BenchUut1.Enable;
  TraceIn1[8] := BenchUut1.Tick;
  BenchUut1();
  TraceOut0[8] := BenchUut1.Red;
  TraceOut1[8] := BenchUut1.Green;
  TraceOut2[8] := BenchUut1.Amber;
  TraceOut3[8] := BenchUut1.Phase;
  BenchCalls := BenchCalls + 1;
 9:
  BenchUut1.Enable := FALSE;
  BenchUut1.Tick := TRUE;
  TraceIn0[9] := BenchUut1.Enable;
  TraceIn1[9] := BenchUut1.Tick;
  BenchUut1();
  TraceOut0[9] := BenchUut1.Red;
  TraceOut1[9] := BenchUut1.Green;
  TraceOut2[9] := BenchUut1.Amber;
  TraceOut3[9] := BenchUut1.Phase;
  BenchCalls := BenchCalls + 1;
 10:
  BenchUut1.Enable := TRUE;
  BenchUut1.Tick := TRUE;
  TraceIn0[10] := BenchUut1.Enable;
  TraceIn1[10] := BenchUut1.Tick;
  BenchUut1();
  TraceOut0[10] := BenchUut1.Red;
  TraceOut1[10] := BenchUut1.Green;
  TraceOut2[10] := BenchUut1.Amber;
  TraceOut3[10] := BenchUut1.Phase;
  BenchCalls := BenchCalls + 1;
 11:
  BenchUut1.Enable := TRUE;
  BenchUut1.Tick := TRUE;
  TraceIn0[11] := BenchUut1.Enable;
  TraceIn1[11] := BenchUut1.Tick;
  BenchUut1();
  TraceOut0[11] := BenchUut1.Red;
  TraceOut1[11] := BenchUut1.Green;
  TraceOut2[11] := BenchUut1.Amber;
  TraceOut3[11] := BenchUut1.Phase;
  BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 12 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
