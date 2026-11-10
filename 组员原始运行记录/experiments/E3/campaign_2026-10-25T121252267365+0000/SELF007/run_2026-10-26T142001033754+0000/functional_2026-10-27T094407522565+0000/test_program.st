PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn0 : ARRAY[0..11] OF BOOL;
 TraceIn1 : ARRAY[0..11] OF BOOL;
 TraceIn2 : ARRAY[0..11] OF BOOL;
 TraceOut0 : ARRAY[0..11] OF BOOL;
 TraceOut1 : ARRAY[0..11] OF BOOL;
 TraceOut2 : ARRAY[0..11] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
  BenchUut0.Demand := FALSE;
  BenchUut0.FaultA := FALSE;
  BenchUut0.FaultB := FALSE;
  TraceIn0[0] := BenchUut0.Demand;
  TraceIn1[0] := BenchUut0.FaultA;
  TraceIn2[0] := BenchUut0.FaultB;
  BenchUut0();
  TraceOut0[0] := BenchUut0.PumpA;
  TraceOut1[0] := BenchUut0.PumpB;
  TraceOut2[0] := BenchUut0.LeadA;
  BenchCalls := BenchCalls + 1;
 1:
  BenchUut0.Demand := TRUE;
  BenchUut0.FaultA := FALSE;
  BenchUut0.FaultB := FALSE;
  TraceIn0[1] := BenchUut0.Demand;
  TraceIn1[1] := BenchUut0.FaultA;
  TraceIn2[1] := BenchUut0.FaultB;
  BenchUut0();
  TraceOut0[1] := BenchUut0.PumpA;
  TraceOut1[1] := BenchUut0.PumpB;
  TraceOut2[1] := BenchUut0.LeadA;
  BenchCalls := BenchCalls + 1;
 2:
  BenchUut0.Demand := TRUE;
  BenchUut0.FaultA := FALSE;
  BenchUut0.FaultB := FALSE;
  TraceIn0[2] := BenchUut0.Demand;
  TraceIn1[2] := BenchUut0.FaultA;
  TraceIn2[2] := BenchUut0.FaultB;
  BenchUut0();
  TraceOut0[2] := BenchUut0.PumpA;
  TraceOut1[2] := BenchUut0.PumpB;
  TraceOut2[2] := BenchUut0.LeadA;
  BenchCalls := BenchCalls + 1;
 3:
  BenchUut0.Demand := FALSE;
  BenchUut0.FaultA := FALSE;
  BenchUut0.FaultB := FALSE;
  TraceIn0[3] := BenchUut0.Demand;
  TraceIn1[3] := BenchUut0.FaultA;
  TraceIn2[3] := BenchUut0.FaultB;
  BenchUut0();
  TraceOut0[3] := BenchUut0.PumpA;
  TraceOut1[3] := BenchUut0.PumpB;
  TraceOut2[3] := BenchUut0.LeadA;
  BenchCalls := BenchCalls + 1;
 4:
  BenchUut0.Demand := FALSE;
  BenchUut0.FaultA := FALSE;
  BenchUut0.FaultB := FALSE;
  TraceIn0[4] := BenchUut0.Demand;
  TraceIn1[4] := BenchUut0.FaultA;
  TraceIn2[4] := BenchUut0.FaultB;
  BenchUut0();
  TraceOut0[4] := BenchUut0.PumpA;
  TraceOut1[4] := BenchUut0.PumpB;
  TraceOut2[4] := BenchUut0.LeadA;
  BenchCalls := BenchCalls + 1;
 5:
  BenchUut0.Demand := TRUE;
  BenchUut0.FaultA := FALSE;
  BenchUut0.FaultB := FALSE;
  TraceIn0[5] := BenchUut0.Demand;
  TraceIn1[5] := BenchUut0.FaultA;
  TraceIn2[5] := BenchUut0.FaultB;
  BenchUut0();
  TraceOut0[5] := BenchUut0.PumpA;
  TraceOut1[5] := BenchUut0.PumpB;
  TraceOut2[5] := BenchUut0.LeadA;
  BenchCalls := BenchCalls + 1;
 6:
  BenchUut0.Demand := FALSE;
  BenchUut0.FaultA := FALSE;
  BenchUut0.FaultB := FALSE;
  TraceIn0[6] := BenchUut0.Demand;
  TraceIn1[6] := BenchUut0.FaultA;
  TraceIn2[6] := BenchUut0.FaultB;
  BenchUut0();
  TraceOut0[6] := BenchUut0.PumpA;
  TraceOut1[6] := BenchUut0.PumpB;
  TraceOut2[6] := BenchUut0.LeadA;
  BenchCalls := BenchCalls + 1;
 7:
  BenchUut1.Demand := TRUE;
  BenchUut1.FaultA := TRUE;
  BenchUut1.FaultB := TRUE;
  TraceIn0[7] := BenchUut1.Demand;
  TraceIn1[7] := BenchUut1.FaultA;
  TraceIn2[7] := BenchUut1.FaultB;
  BenchUut1();
  TraceOut0[7] := BenchUut1.PumpA;
  TraceOut1[7] := BenchUut1.PumpB;
  TraceOut2[7] := BenchUut1.LeadA;
  BenchCalls := BenchCalls + 1;
 8:
  BenchUut1.Demand := FALSE;
  BenchUut1.FaultA := TRUE;
  BenchUut1.FaultB := TRUE;
  TraceIn0[8] := BenchUut1.Demand;
  TraceIn1[8] := BenchUut1.FaultA;
  TraceIn2[8] := BenchUut1.FaultB;
  BenchUut1();
  TraceOut0[8] := BenchUut1.PumpA;
  TraceOut1[8] := BenchUut1.PumpB;
  TraceOut2[8] := BenchUut1.LeadA;
  BenchCalls := BenchCalls + 1;
 9:
  BenchUut1.Demand := TRUE;
  BenchUut1.FaultA := TRUE;
  BenchUut1.FaultB := FALSE;
  TraceIn0[9] := BenchUut1.Demand;
  TraceIn1[9] := BenchUut1.FaultA;
  TraceIn2[9] := BenchUut1.FaultB;
  BenchUut1();
  TraceOut0[9] := BenchUut1.PumpA;
  TraceOut1[9] := BenchUut1.PumpB;
  TraceOut2[9] := BenchUut1.LeadA;
  BenchCalls := BenchCalls + 1;
 10:
  BenchUut1.Demand := TRUE;
  BenchUut1.FaultA := FALSE;
  BenchUut1.FaultB := FALSE;
  TraceIn0[10] := BenchUut1.Demand;
  TraceIn1[10] := BenchUut1.FaultA;
  TraceIn2[10] := BenchUut1.FaultB;
  BenchUut1();
  TraceOut0[10] := BenchUut1.PumpA;
  TraceOut1[10] := BenchUut1.PumpB;
  TraceOut2[10] := BenchUut1.LeadA;
  BenchCalls := BenchCalls + 1;
 11:
  BenchUut1.Demand := FALSE;
  BenchUut1.FaultA := TRUE;
  BenchUut1.FaultB := TRUE;
  TraceIn0[11] := BenchUut1.Demand;
  TraceIn1[11] := BenchUut1.FaultA;
  TraceIn2[11] := BenchUut1.FaultB;
  BenchUut1();
  TraceOut0[11] := BenchUut1.PumpA;
  TraceOut1[11] := BenchUut1.PumpB;
  TraceOut2[11] := BenchUut1.LeadA;
  BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 12 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
