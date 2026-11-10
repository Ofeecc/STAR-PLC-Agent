PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn0 : ARRAY[0..8] OF BOOL;
 TraceIn1 : ARRAY[0..8] OF BOOL;
 TraceIn2 : ARRAY[0..8] OF BOOL;
 TraceOut0 : ARRAY[0..8] OF BOOL;
 TraceOut1 : ARRAY[0..8] OF BOOL;
 TraceOut2 : ARRAY[0..8] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
  BenchUut0.Fault := FALSE;
  BenchUut0.Ack := FALSE;
  BenchUut0.Reset := FALSE;
  TraceIn0[0] := BenchUut0.Fault;
  TraceIn1[0] := BenchUut0.Ack;
  TraceIn2[0] := BenchUut0.Reset;
  BenchUut0();
  TraceOut0[0] := BenchUut0.Alarm;
  TraceOut1[0] := BenchUut0.Acknowledged;
  TraceOut2[0] := BenchUut0.Horn;
  BenchCalls := BenchCalls + 1;
 1:
  BenchUut0.Fault := TRUE;
  BenchUut0.Ack := TRUE;
  BenchUut0.Reset := FALSE;
  TraceIn0[1] := BenchUut0.Fault;
  TraceIn1[1] := BenchUut0.Ack;
  TraceIn2[1] := BenchUut0.Reset;
  BenchUut0();
  TraceOut0[1] := BenchUut0.Alarm;
  TraceOut1[1] := BenchUut0.Acknowledged;
  TraceOut2[1] := BenchUut0.Horn;
  BenchCalls := BenchCalls + 1;
 2:
  BenchUut0.Fault := TRUE;
  BenchUut0.Ack := TRUE;
  BenchUut0.Reset := FALSE;
  TraceIn0[2] := BenchUut0.Fault;
  TraceIn1[2] := BenchUut0.Ack;
  TraceIn2[2] := BenchUut0.Reset;
  BenchUut0();
  TraceOut0[2] := BenchUut0.Alarm;
  TraceOut1[2] := BenchUut0.Acknowledged;
  TraceOut2[2] := BenchUut0.Horn;
  BenchCalls := BenchCalls + 1;
 3:
  BenchUut0.Fault := FALSE;
  BenchUut0.Ack := FALSE;
  BenchUut0.Reset := FALSE;
  TraceIn0[3] := BenchUut0.Fault;
  TraceIn1[3] := BenchUut0.Ack;
  TraceIn2[3] := BenchUut0.Reset;
  BenchUut0();
  TraceOut0[3] := BenchUut0.Alarm;
  TraceOut1[3] := BenchUut0.Acknowledged;
  TraceOut2[3] := BenchUut0.Horn;
  BenchCalls := BenchCalls + 1;
 4:
  BenchUut0.Fault := TRUE;
  BenchUut0.Ack := FALSE;
  BenchUut0.Reset := FALSE;
  TraceIn0[4] := BenchUut0.Fault;
  TraceIn1[4] := BenchUut0.Ack;
  TraceIn2[4] := BenchUut0.Reset;
  BenchUut0();
  TraceOut0[4] := BenchUut0.Alarm;
  TraceOut1[4] := BenchUut0.Acknowledged;
  TraceOut2[4] := BenchUut0.Horn;
  BenchCalls := BenchCalls + 1;
 5:
  BenchUut0.Fault := FALSE;
  BenchUut0.Ack := FALSE;
  BenchUut0.Reset := TRUE;
  TraceIn0[5] := BenchUut0.Fault;
  TraceIn1[5] := BenchUut0.Ack;
  TraceIn2[5] := BenchUut0.Reset;
  BenchUut0();
  TraceOut0[5] := BenchUut0.Alarm;
  TraceOut1[5] := BenchUut0.Acknowledged;
  TraceOut2[5] := BenchUut0.Horn;
  BenchCalls := BenchCalls + 1;
 6:
  BenchUut1.Fault := TRUE;
  BenchUut1.Ack := FALSE;
  BenchUut1.Reset := TRUE;
  TraceIn0[6] := BenchUut1.Fault;
  TraceIn1[6] := BenchUut1.Ack;
  TraceIn2[6] := BenchUut1.Reset;
  BenchUut1();
  TraceOut0[6] := BenchUut1.Alarm;
  TraceOut1[6] := BenchUut1.Acknowledged;
  TraceOut2[6] := BenchUut1.Horn;
  BenchCalls := BenchCalls + 1;
 7:
  BenchUut1.Fault := TRUE;
  BenchUut1.Ack := TRUE;
  BenchUut1.Reset := TRUE;
  TraceIn0[7] := BenchUut1.Fault;
  TraceIn1[7] := BenchUut1.Ack;
  TraceIn2[7] := BenchUut1.Reset;
  BenchUut1();
  TraceOut0[7] := BenchUut1.Alarm;
  TraceOut1[7] := BenchUut1.Acknowledged;
  TraceOut2[7] := BenchUut1.Horn;
  BenchCalls := BenchCalls + 1;
 8:
  BenchUut1.Fault := FALSE;
  BenchUut1.Ack := TRUE;
  BenchUut1.Reset := TRUE;
  TraceIn0[8] := BenchUut1.Fault;
  TraceIn1[8] := BenchUut1.Ack;
  TraceIn2[8] := BenchUut1.Reset;
  BenchUut1();
  TraceOut0[8] := BenchUut1.Alarm;
  TraceOut1[8] := BenchUut1.Acknowledged;
  TraceOut2[8] := BenchUut1.Horn;
  BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 9 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
