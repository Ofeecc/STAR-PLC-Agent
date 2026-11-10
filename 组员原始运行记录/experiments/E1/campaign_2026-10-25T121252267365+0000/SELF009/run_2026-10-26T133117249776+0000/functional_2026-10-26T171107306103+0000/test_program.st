PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn0 : ARRAY[0..12] OF BOOL;
 TraceIn1 : ARRAY[0..12] OF BOOL;
 TraceIn2 : ARRAY[0..12] OF USINT;
 TraceOut0 : ARRAY[0..12] OF USINT;
 TraceOut1 : ARRAY[0..12] OF BOOL;
 TraceOut2 : ARRAY[0..12] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
  BenchUut0.PartPulse := FALSE;
  BenchUut0.Reset := FALSE;
  BenchUut0.Target := USINT#2;
  TraceIn0[0] := BenchUut0.PartPulse;
  TraceIn1[0] := BenchUut0.Reset;
  TraceIn2[0] := BenchUut0.Target;
  BenchUut0();
  TraceOut0[0] := BenchUut0.Count;
  TraceOut1[0] := BenchUut0.Complete;
  TraceOut2[0] := BenchUut0.Error;
  BenchCalls := BenchCalls + 1;
 1:
  BenchUut0.PartPulse := TRUE;
  BenchUut0.Reset := FALSE;
  BenchUut0.Target := USINT#2;
  TraceIn0[1] := BenchUut0.PartPulse;
  TraceIn1[1] := BenchUut0.Reset;
  TraceIn2[1] := BenchUut0.Target;
  BenchUut0();
  TraceOut0[1] := BenchUut0.Count;
  TraceOut1[1] := BenchUut0.Complete;
  TraceOut2[1] := BenchUut0.Error;
  BenchCalls := BenchCalls + 1;
 2:
  BenchUut0.PartPulse := TRUE;
  BenchUut0.Reset := FALSE;
  BenchUut0.Target := USINT#2;
  TraceIn0[2] := BenchUut0.PartPulse;
  TraceIn1[2] := BenchUut0.Reset;
  TraceIn2[2] := BenchUut0.Target;
  BenchUut0();
  TraceOut0[2] := BenchUut0.Count;
  TraceOut1[2] := BenchUut0.Complete;
  TraceOut2[2] := BenchUut0.Error;
  BenchCalls := BenchCalls + 1;
 3:
  BenchUut0.PartPulse := FALSE;
  BenchUut0.Reset := FALSE;
  BenchUut0.Target := USINT#2;
  TraceIn0[3] := BenchUut0.PartPulse;
  TraceIn1[3] := BenchUut0.Reset;
  TraceIn2[3] := BenchUut0.Target;
  BenchUut0();
  TraceOut0[3] := BenchUut0.Count;
  TraceOut1[3] := BenchUut0.Complete;
  TraceOut2[3] := BenchUut0.Error;
  BenchCalls := BenchCalls + 1;
 4:
  BenchUut0.PartPulse := TRUE;
  BenchUut0.Reset := FALSE;
  BenchUut0.Target := USINT#2;
  TraceIn0[4] := BenchUut0.PartPulse;
  TraceIn1[4] := BenchUut0.Reset;
  TraceIn2[4] := BenchUut0.Target;
  BenchUut0();
  TraceOut0[4] := BenchUut0.Count;
  TraceOut1[4] := BenchUut0.Complete;
  TraceOut2[4] := BenchUut0.Error;
  BenchCalls := BenchCalls + 1;
 5:
  BenchUut0.PartPulse := FALSE;
  BenchUut0.Reset := FALSE;
  BenchUut0.Target := USINT#2;
  TraceIn0[5] := BenchUut0.PartPulse;
  TraceIn1[5] := BenchUut0.Reset;
  TraceIn2[5] := BenchUut0.Target;
  BenchUut0();
  TraceOut0[5] := BenchUut0.Count;
  TraceOut1[5] := BenchUut0.Complete;
  TraceOut2[5] := BenchUut0.Error;
  BenchCalls := BenchCalls + 1;
 6:
  BenchUut0.PartPulse := TRUE;
  BenchUut0.Reset := FALSE;
  BenchUut0.Target := USINT#2;
  TraceIn0[6] := BenchUut0.PartPulse;
  TraceIn1[6] := BenchUut0.Reset;
  TraceIn2[6] := BenchUut0.Target;
  BenchUut0();
  TraceOut0[6] := BenchUut0.Count;
  TraceOut1[6] := BenchUut0.Complete;
  TraceOut2[6] := BenchUut0.Error;
  BenchCalls := BenchCalls + 1;
 7:
  BenchUut1.PartPulse := TRUE;
  BenchUut1.Reset := TRUE;
  BenchUut1.Target := USINT#1;
  TraceIn0[7] := BenchUut1.PartPulse;
  TraceIn1[7] := BenchUut1.Reset;
  TraceIn2[7] := BenchUut1.Target;
  BenchUut1();
  TraceOut0[7] := BenchUut1.Count;
  TraceOut1[7] := BenchUut1.Complete;
  TraceOut2[7] := BenchUut1.Error;
  BenchCalls := BenchCalls + 1;
 8:
  BenchUut1.PartPulse := TRUE;
  BenchUut1.Reset := FALSE;
  BenchUut1.Target := USINT#1;
  TraceIn0[8] := BenchUut1.PartPulse;
  TraceIn1[8] := BenchUut1.Reset;
  TraceIn2[8] := BenchUut1.Target;
  BenchUut1();
  TraceOut0[8] := BenchUut1.Count;
  TraceOut1[8] := BenchUut1.Complete;
  TraceOut2[8] := BenchUut1.Error;
  BenchCalls := BenchCalls + 1;
 9:
  BenchUut1.PartPulse := FALSE;
  BenchUut1.Reset := FALSE;
  BenchUut1.Target := USINT#1;
  TraceIn0[9] := BenchUut1.PartPulse;
  TraceIn1[9] := BenchUut1.Reset;
  TraceIn2[9] := BenchUut1.Target;
  BenchUut1();
  TraceOut0[9] := BenchUut1.Count;
  TraceOut1[9] := BenchUut1.Complete;
  TraceOut2[9] := BenchUut1.Error;
  BenchCalls := BenchCalls + 1;
 10:
  BenchUut1.PartPulse := TRUE;
  BenchUut1.Reset := FALSE;
  BenchUut1.Target := USINT#1;
  TraceIn0[10] := BenchUut1.PartPulse;
  TraceIn1[10] := BenchUut1.Reset;
  TraceIn2[10] := BenchUut1.Target;
  BenchUut1();
  TraceOut0[10] := BenchUut1.Count;
  TraceOut1[10] := BenchUut1.Complete;
  TraceOut2[10] := BenchUut1.Error;
  BenchCalls := BenchCalls + 1;
 11:
  BenchUut1.PartPulse := TRUE;
  BenchUut1.Reset := FALSE;
  BenchUut1.Target := USINT#0;
  TraceIn0[11] := BenchUut1.PartPulse;
  TraceIn1[11] := BenchUut1.Reset;
  TraceIn2[11] := BenchUut1.Target;
  BenchUut1();
  TraceOut0[11] := BenchUut1.Count;
  TraceOut1[11] := BenchUut1.Complete;
  TraceOut2[11] := BenchUut1.Error;
  BenchCalls := BenchCalls + 1;
 12:
  BenchUut1.PartPulse := TRUE;
  BenchUut1.Reset := FALSE;
  BenchUut1.Target := USINT#21;
  TraceIn0[12] := BenchUut1.PartPulse;
  TraceIn1[12] := BenchUut1.Reset;
  TraceIn2[12] := BenchUut1.Target;
  BenchUut1();
  TraceOut0[12] := BenchUut1.Count;
  TraceOut1[12] := BenchUut1.Complete;
  TraceOut2[12] := BenchUut1.Error;
  BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 13 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
