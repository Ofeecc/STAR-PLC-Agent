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
 TraceOut1 : ARRAY[0..9] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
  BenchUut0.LowWet := FALSE;
  BenchUut0.HighWet := FALSE;
  BenchUut0.Inhibit := FALSE;
  TraceIn0[0] := BenchUut0.LowWet;
  TraceIn1[0] := BenchUut0.HighWet;
  TraceIn2[0] := BenchUut0.Inhibit;
  BenchUut0();
  TraceOut0[0] := BenchUut0.Fill;
  TraceOut1[0] := BenchUut0.SensorFault;
  BenchCalls := BenchCalls + 1;
 1:
  BenchUut0.LowWet := TRUE;
  BenchUut0.HighWet := FALSE;
  BenchUut0.Inhibit := FALSE;
  TraceIn0[1] := BenchUut0.LowWet;
  TraceIn1[1] := BenchUut0.HighWet;
  TraceIn2[1] := BenchUut0.Inhibit;
  BenchUut0();
  TraceOut0[1] := BenchUut0.Fill;
  TraceOut1[1] := BenchUut0.SensorFault;
  BenchCalls := BenchCalls + 1;
 2:
  BenchUut0.LowWet := TRUE;
  BenchUut0.HighWet := TRUE;
  BenchUut0.Inhibit := FALSE;
  TraceIn0[2] := BenchUut0.LowWet;
  TraceIn1[2] := BenchUut0.HighWet;
  TraceIn2[2] := BenchUut0.Inhibit;
  BenchUut0();
  TraceOut0[2] := BenchUut0.Fill;
  TraceOut1[2] := BenchUut0.SensorFault;
  BenchCalls := BenchCalls + 1;
 3:
  BenchUut0.LowWet := TRUE;
  BenchUut0.HighWet := FALSE;
  BenchUut0.Inhibit := FALSE;
  TraceIn0[3] := BenchUut0.LowWet;
  TraceIn1[3] := BenchUut0.HighWet;
  TraceIn2[3] := BenchUut0.Inhibit;
  BenchUut0();
  TraceOut0[3] := BenchUut0.Fill;
  TraceOut1[3] := BenchUut0.SensorFault;
  BenchCalls := BenchCalls + 1;
 4:
  BenchUut0.LowWet := FALSE;
  BenchUut0.HighWet := FALSE;
  BenchUut0.Inhibit := FALSE;
  TraceIn0[4] := BenchUut0.LowWet;
  TraceIn1[4] := BenchUut0.HighWet;
  TraceIn2[4] := BenchUut0.Inhibit;
  BenchUut0();
  TraceOut0[4] := BenchUut0.Fill;
  TraceOut1[4] := BenchUut0.SensorFault;
  BenchCalls := BenchCalls + 1;
 5:
  BenchUut1.LowWet := TRUE;
  BenchUut1.HighWet := FALSE;
  BenchUut1.Inhibit := FALSE;
  TraceIn0[5] := BenchUut1.LowWet;
  TraceIn1[5] := BenchUut1.HighWet;
  TraceIn2[5] := BenchUut1.Inhibit;
  BenchUut1();
  TraceOut0[5] := BenchUut1.Fill;
  TraceOut1[5] := BenchUut1.SensorFault;
  BenchCalls := BenchCalls + 1;
 6:
  BenchUut1.LowWet := FALSE;
  BenchUut1.HighWet := TRUE;
  BenchUut1.Inhibit := FALSE;
  TraceIn0[6] := BenchUut1.LowWet;
  TraceIn1[6] := BenchUut1.HighWet;
  TraceIn2[6] := BenchUut1.Inhibit;
  BenchUut1();
  TraceOut0[6] := BenchUut1.Fill;
  TraceOut1[6] := BenchUut1.SensorFault;
  BenchCalls := BenchCalls + 1;
 7:
  BenchUut1.LowWet := FALSE;
  BenchUut1.HighWet := FALSE;
  BenchUut1.Inhibit := FALSE;
  TraceIn0[7] := BenchUut1.LowWet;
  TraceIn1[7] := BenchUut1.HighWet;
  TraceIn2[7] := BenchUut1.Inhibit;
  BenchUut1();
  TraceOut0[7] := BenchUut1.Fill;
  TraceOut1[7] := BenchUut1.SensorFault;
  BenchCalls := BenchCalls + 1;
 8:
  BenchUut1.LowWet := TRUE;
  BenchUut1.HighWet := FALSE;
  BenchUut1.Inhibit := TRUE;
  TraceIn0[8] := BenchUut1.LowWet;
  TraceIn1[8] := BenchUut1.HighWet;
  TraceIn2[8] := BenchUut1.Inhibit;
  BenchUut1();
  TraceOut0[8] := BenchUut1.Fill;
  TraceOut1[8] := BenchUut1.SensorFault;
  BenchCalls := BenchCalls + 1;
 9:
  BenchUut1.LowWet := TRUE;
  BenchUut1.HighWet := FALSE;
  BenchUut1.Inhibit := FALSE;
  TraceIn0[9] := BenchUut1.LowWet;
  TraceIn1[9] := BenchUut1.HighWet;
  TraceIn2[9] := BenchUut1.Inhibit;
  BenchUut1();
  TraceOut0[9] := BenchUut1.Fill;
  TraceOut1[9] := BenchUut1.SensorFault;
  BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 10 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
