PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn0 : ARRAY[0..10] OF BOOL;
 TraceIn1 : ARRAY[0..10] OF BOOL;
 TraceIn2 : ARRAY[0..10] OF USINT;
 TraceOut0 : ARRAY[0..10] OF BOOL;
 TraceOut1 : ARRAY[0..10] OF USINT;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
  BenchUut0.Request := TRUE;
  BenchUut0.Trip := FALSE;
  BenchUut0.Preset := USINT#3;
  TraceIn0[0] := BenchUut0.Request;
  TraceIn1[0] := BenchUut0.Trip;
  TraceIn2[0] := BenchUut0.Preset;
  BenchUut0();
  TraceOut0[0] := BenchUut0.Ready;
  TraceOut1[0] := BenchUut0.Count;
  BenchCalls := BenchCalls + 1;
 1:
  BenchUut0.Request := TRUE;
  BenchUut0.Trip := FALSE;
  BenchUut0.Preset := USINT#3;
  TraceIn0[1] := BenchUut0.Request;
  TraceIn1[1] := BenchUut0.Trip;
  TraceIn2[1] := BenchUut0.Preset;
  BenchUut0();
  TraceOut0[1] := BenchUut0.Ready;
  TraceOut1[1] := BenchUut0.Count;
  BenchCalls := BenchCalls + 1;
 2:
  BenchUut0.Request := TRUE;
  BenchUut0.Trip := FALSE;
  BenchUut0.Preset := USINT#3;
  TraceIn0[2] := BenchUut0.Request;
  TraceIn1[2] := BenchUut0.Trip;
  TraceIn2[2] := BenchUut0.Preset;
  BenchUut0();
  TraceOut0[2] := BenchUut0.Ready;
  TraceOut1[2] := BenchUut0.Count;
  BenchCalls := BenchCalls + 1;
 3:
  BenchUut0.Request := TRUE;
  BenchUut0.Trip := FALSE;
  BenchUut0.Preset := USINT#3;
  TraceIn0[3] := BenchUut0.Request;
  TraceIn1[3] := BenchUut0.Trip;
  TraceIn2[3] := BenchUut0.Preset;
  BenchUut0();
  TraceOut0[3] := BenchUut0.Ready;
  TraceOut1[3] := BenchUut0.Count;
  BenchCalls := BenchCalls + 1;
 4:
  BenchUut0.Request := TRUE;
  BenchUut0.Trip := TRUE;
  BenchUut0.Preset := USINT#3;
  TraceIn0[4] := BenchUut0.Request;
  TraceIn1[4] := BenchUut0.Trip;
  TraceIn2[4] := BenchUut0.Preset;
  BenchUut0();
  TraceOut0[4] := BenchUut0.Ready;
  TraceOut1[4] := BenchUut0.Count;
  BenchCalls := BenchCalls + 1;
 5:
  BenchUut0.Request := TRUE;
  BenchUut0.Trip := FALSE;
  BenchUut0.Preset := USINT#3;
  TraceIn0[5] := BenchUut0.Request;
  TraceIn1[5] := BenchUut0.Trip;
  TraceIn2[5] := BenchUut0.Preset;
  BenchUut0();
  TraceOut0[5] := BenchUut0.Ready;
  TraceOut1[5] := BenchUut0.Count;
  BenchCalls := BenchCalls + 1;
 6:
  BenchUut1.Request := TRUE;
  BenchUut1.Trip := FALSE;
  BenchUut1.Preset := USINT#0;
  TraceIn0[6] := BenchUut1.Request;
  TraceIn1[6] := BenchUut1.Trip;
  TraceIn2[6] := BenchUut1.Preset;
  BenchUut1();
  TraceOut0[6] := BenchUut1.Ready;
  TraceOut1[6] := BenchUut1.Count;
  BenchCalls := BenchCalls + 1;
 7:
  BenchUut1.Request := TRUE;
  BenchUut1.Trip := FALSE;
  BenchUut1.Preset := USINT#6;
  TraceIn0[7] := BenchUut1.Request;
  TraceIn1[7] := BenchUut1.Trip;
  TraceIn2[7] := BenchUut1.Preset;
  BenchUut1();
  TraceOut0[7] := BenchUut1.Ready;
  TraceOut1[7] := BenchUut1.Count;
  BenchCalls := BenchCalls + 1;
 8:
  BenchUut1.Request := TRUE;
  BenchUut1.Trip := FALSE;
  BenchUut1.Preset := USINT#5;
  TraceIn0[8] := BenchUut1.Request;
  TraceIn1[8] := BenchUut1.Trip;
  TraceIn2[8] := BenchUut1.Preset;
  BenchUut1();
  TraceOut0[8] := BenchUut1.Ready;
  TraceOut1[8] := BenchUut1.Count;
  BenchCalls := BenchCalls + 1;
 9:
  BenchUut1.Request := TRUE;
  BenchUut1.Trip := FALSE;
  BenchUut1.Preset := USINT#1;
  TraceIn0[9] := BenchUut1.Request;
  TraceIn1[9] := BenchUut1.Trip;
  TraceIn2[9] := BenchUut1.Preset;
  BenchUut1();
  TraceOut0[9] := BenchUut1.Ready;
  TraceOut1[9] := BenchUut1.Count;
  BenchCalls := BenchCalls + 1;
 10:
  BenchUut1.Request := FALSE;
  BenchUut1.Trip := FALSE;
  BenchUut1.Preset := USINT#5;
  TraceIn0[10] := BenchUut1.Request;
  TraceIn1[10] := BenchUut1.Trip;
  TraceIn2[10] := BenchUut1.Preset;
  BenchUut1();
  TraceOut0[10] := BenchUut1.Ready;
  TraceOut1[10] := BenchUut1.Count;
  BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 11 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
