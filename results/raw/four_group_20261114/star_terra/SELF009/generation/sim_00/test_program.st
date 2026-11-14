PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_PartPulse : ARRAY[0..15] OF BOOL;
 TraceIn_Reset : ARRAY[0..15] OF BOOL;
 TraceIn_Target : ARRAY[0..15] OF USINT;
 TraceOut_Count : ARRAY[0..15] OF USINT;
 TraceOut_Complete : ARRAY[0..15] OF BOOL;
 TraceOut_Error : ARRAY[0..15] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.PartPulse := FALSE;
   BenchUut0.Reset := FALSE;
   BenchUut0.Target := USINT#2;
   TraceIn_PartPulse[0] := BenchUut0.PartPulse;
   TraceIn_Reset[0] := BenchUut0.Reset;
   TraceIn_Target[0] := BenchUut0.Target;
   BenchUut0();
   TraceOut_Count[0] := BenchUut0.Count;
   TraceOut_Complete[0] := BenchUut0.Complete;
   TraceOut_Error[0] := BenchUut0.Error;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.PartPulse := TRUE;
   BenchUut0.Reset := FALSE;
   BenchUut0.Target := USINT#2;
   TraceIn_PartPulse[1] := BenchUut0.PartPulse;
   TraceIn_Reset[1] := BenchUut0.Reset;
   TraceIn_Target[1] := BenchUut0.Target;
   BenchUut0();
   TraceOut_Count[1] := BenchUut0.Count;
   TraceOut_Complete[1] := BenchUut0.Complete;
   TraceOut_Error[1] := BenchUut0.Error;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.PartPulse := FALSE;
   BenchUut0.Reset := FALSE;
   BenchUut0.Target := USINT#2;
   TraceIn_PartPulse[2] := BenchUut0.PartPulse;
   TraceIn_Reset[2] := BenchUut0.Reset;
   TraceIn_Target[2] := BenchUut0.Target;
   BenchUut0();
   TraceOut_Count[2] := BenchUut0.Count;
   TraceOut_Complete[2] := BenchUut0.Complete;
   TraceOut_Error[2] := BenchUut0.Error;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.PartPulse := TRUE;
   BenchUut0.Reset := FALSE;
   BenchUut0.Target := USINT#2;
   TraceIn_PartPulse[3] := BenchUut0.PartPulse;
   TraceIn_Reset[3] := BenchUut0.Reset;
   TraceIn_Target[3] := BenchUut0.Target;
   BenchUut0();
   TraceOut_Count[3] := BenchUut0.Count;
   TraceOut_Complete[3] := BenchUut0.Complete;
   TraceOut_Error[3] := BenchUut0.Error;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.PartPulse := FALSE;
   BenchUut0.Reset := FALSE;
   BenchUut0.Target := USINT#2;
   TraceIn_PartPulse[4] := BenchUut0.PartPulse;
   TraceIn_Reset[4] := BenchUut0.Reset;
   TraceIn_Target[4] := BenchUut0.Target;
   BenchUut0();
   TraceOut_Count[4] := BenchUut0.Count;
   TraceOut_Complete[4] := BenchUut0.Complete;
   TraceOut_Error[4] := BenchUut0.Error;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut0.PartPulse := TRUE;
   BenchUut0.Reset := FALSE;
   BenchUut0.Target := USINT#2;
   TraceIn_PartPulse[5] := BenchUut0.PartPulse;
   TraceIn_Reset[5] := BenchUut0.Reset;
   TraceIn_Target[5] := BenchUut0.Target;
   BenchUut0();
   TraceOut_Count[5] := BenchUut0.Count;
   TraceOut_Complete[5] := BenchUut0.Complete;
   TraceOut_Error[5] := BenchUut0.Error;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut0.PartPulse := TRUE;
   BenchUut0.Reset := TRUE;
   BenchUut0.Target := USINT#2;
   TraceIn_PartPulse[6] := BenchUut0.PartPulse;
   TraceIn_Reset[6] := BenchUut0.Reset;
   TraceIn_Target[6] := BenchUut0.Target;
   BenchUut0();
   TraceOut_Count[6] := BenchUut0.Count;
   TraceOut_Complete[6] := BenchUut0.Complete;
   TraceOut_Error[6] := BenchUut0.Error;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut0.PartPulse := TRUE;
   BenchUut0.Reset := FALSE;
   BenchUut0.Target := USINT#2;
   TraceIn_PartPulse[7] := BenchUut0.PartPulse;
   TraceIn_Reset[7] := BenchUut0.Reset;
   TraceIn_Target[7] := BenchUut0.Target;
   BenchUut0();
   TraceOut_Count[7] := BenchUut0.Count;
   TraceOut_Complete[7] := BenchUut0.Complete;
   TraceOut_Error[7] := BenchUut0.Error;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.PartPulse := FALSE;
   BenchUut1.Reset := FALSE;
   BenchUut1.Target := USINT#20;
   TraceIn_PartPulse[8] := BenchUut1.PartPulse;
   TraceIn_Reset[8] := BenchUut1.Reset;
   TraceIn_Target[8] := BenchUut1.Target;
   BenchUut1();
   TraceOut_Count[8] := BenchUut1.Count;
   TraceOut_Complete[8] := BenchUut1.Complete;
   TraceOut_Error[8] := BenchUut1.Error;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.PartPulse := TRUE;
   BenchUut1.Reset := FALSE;
   BenchUut1.Target := USINT#20;
   TraceIn_PartPulse[9] := BenchUut1.PartPulse;
   TraceIn_Reset[9] := BenchUut1.Reset;
   TraceIn_Target[9] := BenchUut1.Target;
   BenchUut1();
   TraceOut_Count[9] := BenchUut1.Count;
   TraceOut_Complete[9] := BenchUut1.Complete;
   TraceOut_Error[9] := BenchUut1.Error;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.PartPulse := FALSE;
   BenchUut1.Reset := FALSE;
   BenchUut1.Target := USINT#20;
   TraceIn_PartPulse[10] := BenchUut1.PartPulse;
   TraceIn_Reset[10] := BenchUut1.Reset;
   TraceIn_Target[10] := BenchUut1.Target;
   BenchUut1();
   TraceOut_Count[10] := BenchUut1.Count;
   TraceOut_Complete[10] := BenchUut1.Complete;
   TraceOut_Error[10] := BenchUut1.Error;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut1.PartPulse := TRUE;
   BenchUut1.Reset := FALSE;
   BenchUut1.Target := USINT#20;
   TraceIn_PartPulse[11] := BenchUut1.PartPulse;
   TraceIn_Reset[11] := BenchUut1.Reset;
   TraceIn_Target[11] := BenchUut1.Target;
   BenchUut1();
   TraceOut_Count[11] := BenchUut1.Count;
   TraceOut_Complete[11] := BenchUut1.Complete;
   TraceOut_Error[11] := BenchUut1.Error;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut1.PartPulse := TRUE;
   BenchUut1.Reset := FALSE;
   BenchUut1.Target := USINT#1;
   TraceIn_PartPulse[12] := BenchUut1.PartPulse;
   TraceIn_Reset[12] := BenchUut1.Reset;
   TraceIn_Target[12] := BenchUut1.Target;
   BenchUut1();
   TraceOut_Count[12] := BenchUut1.Count;
   TraceOut_Complete[12] := BenchUut1.Complete;
   TraceOut_Error[12] := BenchUut1.Error;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut1.PartPulse := FALSE;
   BenchUut1.Reset := FALSE;
   BenchUut1.Target := USINT#0;
   TraceIn_PartPulse[13] := BenchUut1.PartPulse;
   TraceIn_Reset[13] := BenchUut1.Reset;
   TraceIn_Target[13] := BenchUut1.Target;
   BenchUut1();
   TraceOut_Count[13] := BenchUut1.Count;
   TraceOut_Complete[13] := BenchUut1.Complete;
   TraceOut_Error[13] := BenchUut1.Error;
   BenchCalls := BenchCalls + 1;
 14:
   BenchUut1.PartPulse := TRUE;
   BenchUut1.Reset := FALSE;
   BenchUut1.Target := USINT#21;
   TraceIn_PartPulse[14] := BenchUut1.PartPulse;
   TraceIn_Reset[14] := BenchUut1.Reset;
   TraceIn_Target[14] := BenchUut1.Target;
   BenchUut1();
   TraceOut_Count[14] := BenchUut1.Count;
   TraceOut_Complete[14] := BenchUut1.Complete;
   TraceOut_Error[14] := BenchUut1.Error;
   BenchCalls := BenchCalls + 1;
 15:
   BenchUut1.PartPulse := TRUE;
   BenchUut1.Reset := FALSE;
   BenchUut1.Target := USINT#20;
   TraceIn_PartPulse[15] := BenchUut1.PartPulse;
   TraceIn_Reset[15] := BenchUut1.Reset;
   TraceIn_Target[15] := BenchUut1.Target;
   BenchUut1();
   TraceOut_Count[15] := BenchUut1.Count;
   TraceOut_Complete[15] := BenchUut1.Complete;
   TraceOut_Error[15] := BenchUut1.Error;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 16 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
