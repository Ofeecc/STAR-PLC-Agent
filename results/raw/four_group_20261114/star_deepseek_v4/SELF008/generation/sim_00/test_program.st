PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_Request : ARRAY[0..9] OF BOOL;
 TraceIn_Trip : ARRAY[0..9] OF BOOL;
 TraceIn_Preset : ARRAY[0..9] OF USINT;
 TraceOut_Ready : ARRAY[0..9] OF BOOL;
 TraceOut_Count : ARRAY[0..9] OF USINT;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.Request := TRUE;
   BenchUut0.Trip := FALSE;
   BenchUut0.Preset := USINT#3;
   TraceIn_Request[0] := BenchUut0.Request;
   TraceIn_Trip[0] := BenchUut0.Trip;
   TraceIn_Preset[0] := BenchUut0.Preset;
   BenchUut0();
   TraceOut_Ready[0] := BenchUut0.Ready;
   TraceOut_Count[0] := BenchUut0.Count;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.Request := TRUE;
   BenchUut0.Trip := FALSE;
   BenchUut0.Preset := USINT#3;
   TraceIn_Request[1] := BenchUut0.Request;
   TraceIn_Trip[1] := BenchUut0.Trip;
   TraceIn_Preset[1] := BenchUut0.Preset;
   BenchUut0();
   TraceOut_Ready[1] := BenchUut0.Ready;
   TraceOut_Count[1] := BenchUut0.Count;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.Request := TRUE;
   BenchUut0.Trip := FALSE;
   BenchUut0.Preset := USINT#3;
   TraceIn_Request[2] := BenchUut0.Request;
   TraceIn_Trip[2] := BenchUut0.Trip;
   TraceIn_Preset[2] := BenchUut0.Preset;
   BenchUut0();
   TraceOut_Ready[2] := BenchUut0.Ready;
   TraceOut_Count[2] := BenchUut0.Count;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.Request := TRUE;
   BenchUut0.Trip := FALSE;
   BenchUut0.Preset := USINT#3;
   TraceIn_Request[3] := BenchUut0.Request;
   TraceIn_Trip[3] := BenchUut0.Trip;
   TraceIn_Preset[3] := BenchUut0.Preset;
   BenchUut0();
   TraceOut_Ready[3] := BenchUut0.Ready;
   TraceOut_Count[3] := BenchUut0.Count;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut1.Request := TRUE;
   BenchUut1.Trip := FALSE;
   BenchUut1.Preset := USINT#1;
   TraceIn_Request[4] := BenchUut1.Request;
   TraceIn_Trip[4] := BenchUut1.Trip;
   TraceIn_Preset[4] := BenchUut1.Preset;
   BenchUut1();
   TraceOut_Ready[4] := BenchUut1.Ready;
   TraceOut_Count[4] := BenchUut1.Count;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut1.Request := TRUE;
   BenchUut1.Trip := FALSE;
   BenchUut1.Preset := USINT#6;
   TraceIn_Request[5] := BenchUut1.Request;
   TraceIn_Trip[5] := BenchUut1.Trip;
   TraceIn_Preset[5] := BenchUut1.Preset;
   BenchUut1();
   TraceOut_Ready[5] := BenchUut1.Ready;
   TraceOut_Count[5] := BenchUut1.Count;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.Request := TRUE;
   BenchUut1.Trip := FALSE;
   BenchUut1.Preset := USINT#5;
   TraceIn_Request[6] := BenchUut1.Request;
   TraceIn_Trip[6] := BenchUut1.Trip;
   TraceIn_Preset[6] := BenchUut1.Preset;
   BenchUut1();
   TraceOut_Ready[6] := BenchUut1.Ready;
   TraceOut_Count[6] := BenchUut1.Count;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut1.Request := TRUE;
   BenchUut1.Trip := FALSE;
   BenchUut1.Preset := USINT#5;
   TraceIn_Request[7] := BenchUut1.Request;
   TraceIn_Trip[7] := BenchUut1.Trip;
   TraceIn_Preset[7] := BenchUut1.Preset;
   BenchUut1();
   TraceOut_Ready[7] := BenchUut1.Ready;
   TraceOut_Count[7] := BenchUut1.Count;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.Request := TRUE;
   BenchUut1.Trip := TRUE;
   BenchUut1.Preset := USINT#5;
   TraceIn_Request[8] := BenchUut1.Request;
   TraceIn_Trip[8] := BenchUut1.Trip;
   TraceIn_Preset[8] := BenchUut1.Preset;
   BenchUut1();
   TraceOut_Ready[8] := BenchUut1.Ready;
   TraceOut_Count[8] := BenchUut1.Count;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.Request := FALSE;
   BenchUut1.Trip := FALSE;
   BenchUut1.Preset := USINT#5;
   TraceIn_Request[9] := BenchUut1.Request;
   TraceIn_Trip[9] := BenchUut1.Trip;
   TraceIn_Preset[9] := BenchUut1.Preset;
   BenchUut1();
   TraceOut_Ready[9] := BenchUut1.Ready;
   TraceOut_Count[9] := BenchUut1.Count;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 10 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
