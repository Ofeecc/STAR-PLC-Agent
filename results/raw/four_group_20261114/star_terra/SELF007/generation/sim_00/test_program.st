PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_Demand : ARRAY[0..15] OF BOOL;
 TraceIn_FaultA : ARRAY[0..15] OF BOOL;
 TraceIn_FaultB : ARRAY[0..15] OF BOOL;
 TraceOut_PumpA : ARRAY[0..15] OF BOOL;
 TraceOut_PumpB : ARRAY[0..15] OF BOOL;
 TraceOut_LeadA : ARRAY[0..15] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.Demand := TRUE;
   BenchUut0.FaultA := FALSE;
   BenchUut0.FaultB := FALSE;
   TraceIn_Demand[0] := BenchUut0.Demand;
   TraceIn_FaultA[0] := BenchUut0.FaultA;
   TraceIn_FaultB[0] := BenchUut0.FaultB;
   BenchUut0();
   TraceOut_PumpA[0] := BenchUut0.PumpA;
   TraceOut_PumpB[0] := BenchUut0.PumpB;
   TraceOut_LeadA[0] := BenchUut0.LeadA;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.Demand := TRUE;
   BenchUut0.FaultA := TRUE;
   BenchUut0.FaultB := FALSE;
   TraceIn_Demand[1] := BenchUut0.Demand;
   TraceIn_FaultA[1] := BenchUut0.FaultA;
   TraceIn_FaultB[1] := BenchUut0.FaultB;
   BenchUut0();
   TraceOut_PumpA[1] := BenchUut0.PumpA;
   TraceOut_PumpB[1] := BenchUut0.PumpB;
   TraceOut_LeadA[1] := BenchUut0.LeadA;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.Demand := TRUE;
   BenchUut0.FaultA := FALSE;
   BenchUut0.FaultB := FALSE;
   TraceIn_Demand[2] := BenchUut0.Demand;
   TraceIn_FaultA[2] := BenchUut0.FaultA;
   TraceIn_FaultB[2] := BenchUut0.FaultB;
   BenchUut0();
   TraceOut_PumpA[2] := BenchUut0.PumpA;
   TraceOut_PumpB[2] := BenchUut0.PumpB;
   TraceOut_LeadA[2] := BenchUut0.LeadA;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.Demand := FALSE;
   BenchUut0.FaultA := FALSE;
   BenchUut0.FaultB := FALSE;
   TraceIn_Demand[3] := BenchUut0.Demand;
   TraceIn_FaultA[3] := BenchUut0.FaultA;
   TraceIn_FaultB[3] := BenchUut0.FaultB;
   BenchUut0();
   TraceOut_PumpA[3] := BenchUut0.PumpA;
   TraceOut_PumpB[3] := BenchUut0.PumpB;
   TraceOut_LeadA[3] := BenchUut0.LeadA;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.Demand := FALSE;
   BenchUut0.FaultA := FALSE;
   BenchUut0.FaultB := FALSE;
   TraceIn_Demand[4] := BenchUut0.Demand;
   TraceIn_FaultA[4] := BenchUut0.FaultA;
   TraceIn_FaultB[4] := BenchUut0.FaultB;
   BenchUut0();
   TraceOut_PumpA[4] := BenchUut0.PumpA;
   TraceOut_PumpB[4] := BenchUut0.PumpB;
   TraceOut_LeadA[4] := BenchUut0.LeadA;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut0.Demand := TRUE;
   BenchUut0.FaultA := FALSE;
   BenchUut0.FaultB := FALSE;
   TraceIn_Demand[5] := BenchUut0.Demand;
   TraceIn_FaultA[5] := BenchUut0.FaultA;
   TraceIn_FaultB[5] := BenchUut0.FaultB;
   BenchUut0();
   TraceOut_PumpA[5] := BenchUut0.PumpA;
   TraceOut_PumpB[5] := BenchUut0.PumpB;
   TraceOut_LeadA[5] := BenchUut0.LeadA;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut0.Demand := TRUE;
   BenchUut0.FaultA := FALSE;
   BenchUut0.FaultB := TRUE;
   TraceIn_Demand[6] := BenchUut0.Demand;
   TraceIn_FaultA[6] := BenchUut0.FaultA;
   TraceIn_FaultB[6] := BenchUut0.FaultB;
   BenchUut0();
   TraceOut_PumpA[6] := BenchUut0.PumpA;
   TraceOut_PumpB[6] := BenchUut0.PumpB;
   TraceOut_LeadA[6] := BenchUut0.LeadA;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut0.Demand := FALSE;
   BenchUut0.FaultA := FALSE;
   BenchUut0.FaultB := FALSE;
   TraceIn_Demand[7] := BenchUut0.Demand;
   TraceIn_FaultA[7] := BenchUut0.FaultA;
   TraceIn_FaultB[7] := BenchUut0.FaultB;
   BenchUut0();
   TraceOut_PumpA[7] := BenchUut0.PumpA;
   TraceOut_PumpB[7] := BenchUut0.PumpB;
   TraceOut_LeadA[7] := BenchUut0.LeadA;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.Demand := TRUE;
   BenchUut1.FaultA := TRUE;
   BenchUut1.FaultB := TRUE;
   TraceIn_Demand[8] := BenchUut1.Demand;
   TraceIn_FaultA[8] := BenchUut1.FaultA;
   TraceIn_FaultB[8] := BenchUut1.FaultB;
   BenchUut1();
   TraceOut_PumpA[8] := BenchUut1.PumpA;
   TraceOut_PumpB[8] := BenchUut1.PumpB;
   TraceOut_LeadA[8] := BenchUut1.LeadA;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.Demand := FALSE;
   BenchUut1.FaultA := TRUE;
   BenchUut1.FaultB := TRUE;
   TraceIn_Demand[9] := BenchUut1.Demand;
   TraceIn_FaultA[9] := BenchUut1.FaultA;
   TraceIn_FaultB[9] := BenchUut1.FaultB;
   BenchUut1();
   TraceOut_PumpA[9] := BenchUut1.PumpA;
   TraceOut_PumpB[9] := BenchUut1.PumpB;
   TraceOut_LeadA[9] := BenchUut1.LeadA;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.Demand := TRUE;
   BenchUut1.FaultA := TRUE;
   BenchUut1.FaultB := FALSE;
   TraceIn_Demand[10] := BenchUut1.Demand;
   TraceIn_FaultA[10] := BenchUut1.FaultA;
   TraceIn_FaultB[10] := BenchUut1.FaultB;
   BenchUut1();
   TraceOut_PumpA[10] := BenchUut1.PumpA;
   TraceOut_PumpB[10] := BenchUut1.PumpB;
   TraceOut_LeadA[10] := BenchUut1.LeadA;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut1.Demand := TRUE;
   BenchUut1.FaultA := TRUE;
   BenchUut1.FaultB := TRUE;
   TraceIn_Demand[11] := BenchUut1.Demand;
   TraceIn_FaultA[11] := BenchUut1.FaultA;
   TraceIn_FaultB[11] := BenchUut1.FaultB;
   BenchUut1();
   TraceOut_PumpA[11] := BenchUut1.PumpA;
   TraceOut_PumpB[11] := BenchUut1.PumpB;
   TraceOut_LeadA[11] := BenchUut1.LeadA;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut1.Demand := FALSE;
   BenchUut1.FaultA := TRUE;
   BenchUut1.FaultB := TRUE;
   TraceIn_Demand[12] := BenchUut1.Demand;
   TraceIn_FaultA[12] := BenchUut1.FaultA;
   TraceIn_FaultB[12] := BenchUut1.FaultB;
   BenchUut1();
   TraceOut_PumpA[12] := BenchUut1.PumpA;
   TraceOut_PumpB[12] := BenchUut1.PumpB;
   TraceOut_LeadA[12] := BenchUut1.LeadA;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut1.Demand := TRUE;
   BenchUut1.FaultA := TRUE;
   BenchUut1.FaultB := TRUE;
   TraceIn_Demand[13] := BenchUut1.Demand;
   TraceIn_FaultA[13] := BenchUut1.FaultA;
   TraceIn_FaultB[13] := BenchUut1.FaultB;
   BenchUut1();
   TraceOut_PumpA[13] := BenchUut1.PumpA;
   TraceOut_PumpB[13] := BenchUut1.PumpB;
   TraceOut_LeadA[13] := BenchUut1.LeadA;
   BenchCalls := BenchCalls + 1;
 14:
   BenchUut1.Demand := FALSE;
   BenchUut1.FaultA := TRUE;
   BenchUut1.FaultB := TRUE;
   TraceIn_Demand[14] := BenchUut1.Demand;
   TraceIn_FaultA[14] := BenchUut1.FaultA;
   TraceIn_FaultB[14] := BenchUut1.FaultB;
   BenchUut1();
   TraceOut_PumpA[14] := BenchUut1.PumpA;
   TraceOut_PumpB[14] := BenchUut1.PumpB;
   TraceOut_LeadA[14] := BenchUut1.LeadA;
   BenchCalls := BenchCalls + 1;
 15:
   BenchUut1.Demand := TRUE;
   BenchUut1.FaultA := FALSE;
   BenchUut1.FaultB := FALSE;
   TraceIn_Demand[15] := BenchUut1.Demand;
   TraceIn_FaultA[15] := BenchUut1.FaultA;
   TraceIn_FaultB[15] := BenchUut1.FaultB;
   BenchUut1();
   TraceOut_PumpA[15] := BenchUut1.PumpA;
   TraceOut_PumpB[15] := BenchUut1.PumpB;
   TraceOut_LeadA[15] := BenchUut1.LeadA;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 16 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
