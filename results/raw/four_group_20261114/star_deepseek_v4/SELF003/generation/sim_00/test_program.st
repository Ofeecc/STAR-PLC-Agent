PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_Start : ARRAY[0..15] OF BOOL;
 TraceIn_Stop : ARRAY[0..15] OF BOOL;
 TraceIn_EStopNC : ARRAY[0..15] OF BOOL;
 TraceIn_Reset : ARRAY[0..15] OF BOOL;
 TraceOut_Run : ARRAY[0..15] OF BOOL;
 TraceOut_ResetRequired : ARRAY[0..15] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.EStopNC := TRUE;
   BenchUut0.Reset := TRUE;
   TraceIn_Start[0] := BenchUut0.Start;
   TraceIn_Stop[0] := BenchUut0.Stop;
   TraceIn_EStopNC[0] := BenchUut0.EStopNC;
   TraceIn_Reset[0] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Run[0] := BenchUut0.Run;
   TraceOut_ResetRequired[0] := BenchUut0.ResetRequired;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.Start := TRUE;
   BenchUut0.Stop := FALSE;
   BenchUut0.EStopNC := TRUE;
   BenchUut0.Reset := FALSE;
   TraceIn_Start[1] := BenchUut0.Start;
   TraceIn_Stop[1] := BenchUut0.Stop;
   TraceIn_EStopNC[1] := BenchUut0.EStopNC;
   TraceIn_Reset[1] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Run[1] := BenchUut0.Run;
   TraceOut_ResetRequired[1] := BenchUut0.ResetRequired;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.EStopNC := TRUE;
   BenchUut0.Reset := FALSE;
   TraceIn_Start[2] := BenchUut0.Start;
   TraceIn_Stop[2] := BenchUut0.Stop;
   TraceIn_EStopNC[2] := BenchUut0.EStopNC;
   TraceIn_Reset[2] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Run[2] := BenchUut0.Run;
   TraceOut_ResetRequired[2] := BenchUut0.ResetRequired;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := TRUE;
   BenchUut0.EStopNC := TRUE;
   BenchUut0.Reset := FALSE;
   TraceIn_Start[3] := BenchUut0.Start;
   TraceIn_Stop[3] := BenchUut0.Stop;
   TraceIn_EStopNC[3] := BenchUut0.EStopNC;
   TraceIn_Reset[3] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Run[3] := BenchUut0.Run;
   TraceOut_ResetRequired[3] := BenchUut0.ResetRequired;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.Start := TRUE;
   BenchUut0.Stop := FALSE;
   BenchUut0.EStopNC := TRUE;
   BenchUut0.Reset := FALSE;
   TraceIn_Start[4] := BenchUut0.Start;
   TraceIn_Stop[4] := BenchUut0.Stop;
   TraceIn_EStopNC[4] := BenchUut0.EStopNC;
   TraceIn_Reset[4] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Run[4] := BenchUut0.Run;
   TraceOut_ResetRequired[4] := BenchUut0.ResetRequired;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.EStopNC := FALSE;
   BenchUut0.Reset := FALSE;
   TraceIn_Start[5] := BenchUut0.Start;
   TraceIn_Stop[5] := BenchUut0.Stop;
   TraceIn_EStopNC[5] := BenchUut0.EStopNC;
   TraceIn_Reset[5] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Run[5] := BenchUut0.Run;
   TraceOut_ResetRequired[5] := BenchUut0.ResetRequired;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.EStopNC := TRUE;
   BenchUut0.Reset := FALSE;
   TraceIn_Start[6] := BenchUut0.Start;
   TraceIn_Stop[6] := BenchUut0.Stop;
   TraceIn_EStopNC[6] := BenchUut0.EStopNC;
   TraceIn_Reset[6] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Run[6] := BenchUut0.Run;
   TraceOut_ResetRequired[6] := BenchUut0.ResetRequired;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.EStopNC := TRUE;
   BenchUut0.Reset := TRUE;
   TraceIn_Start[7] := BenchUut0.Start;
   TraceIn_Stop[7] := BenchUut0.Stop;
   TraceIn_EStopNC[7] := BenchUut0.EStopNC;
   TraceIn_Reset[7] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Run[7] := BenchUut0.Run;
   TraceOut_ResetRequired[7] := BenchUut0.ResetRequired;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.Start := FALSE;
   BenchUut1.Stop := FALSE;
   BenchUut1.EStopNC := TRUE;
   BenchUut1.Reset := TRUE;
   TraceIn_Start[8] := BenchUut1.Start;
   TraceIn_Stop[8] := BenchUut1.Stop;
   TraceIn_EStopNC[8] := BenchUut1.EStopNC;
   TraceIn_Reset[8] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Run[8] := BenchUut1.Run;
   TraceOut_ResetRequired[8] := BenchUut1.ResetRequired;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := FALSE;
   BenchUut1.EStopNC := TRUE;
   BenchUut1.Reset := FALSE;
   TraceIn_Start[9] := BenchUut1.Start;
   TraceIn_Stop[9] := BenchUut1.Stop;
   TraceIn_EStopNC[9] := BenchUut1.EStopNC;
   TraceIn_Reset[9] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Run[9] := BenchUut1.Run;
   TraceOut_ResetRequired[9] := BenchUut1.ResetRequired;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := FALSE;
   BenchUut1.EStopNC := FALSE;
   BenchUut1.Reset := FALSE;
   TraceIn_Start[10] := BenchUut1.Start;
   TraceIn_Stop[10] := BenchUut1.Stop;
   TraceIn_EStopNC[10] := BenchUut1.EStopNC;
   TraceIn_Reset[10] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Run[10] := BenchUut1.Run;
   TraceOut_ResetRequired[10] := BenchUut1.ResetRequired;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := FALSE;
   BenchUut1.EStopNC := TRUE;
   BenchUut1.Reset := TRUE;
   TraceIn_Start[11] := BenchUut1.Start;
   TraceIn_Stop[11] := BenchUut1.Stop;
   TraceIn_EStopNC[11] := BenchUut1.EStopNC;
   TraceIn_Reset[11] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Run[11] := BenchUut1.Run;
   TraceOut_ResetRequired[11] := BenchUut1.ResetRequired;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := FALSE;
   BenchUut1.EStopNC := TRUE;
   BenchUut1.Reset := FALSE;
   TraceIn_Start[12] := BenchUut1.Start;
   TraceIn_Stop[12] := BenchUut1.Stop;
   TraceIn_EStopNC[12] := BenchUut1.EStopNC;
   TraceIn_Reset[12] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Run[12] := BenchUut1.Run;
   TraceOut_ResetRequired[12] := BenchUut1.ResetRequired;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut1.Start := FALSE;
   BenchUut1.Stop := FALSE;
   BenchUut1.EStopNC := TRUE;
   BenchUut1.Reset := TRUE;
   TraceIn_Start[13] := BenchUut1.Start;
   TraceIn_Stop[13] := BenchUut1.Stop;
   TraceIn_EStopNC[13] := BenchUut1.EStopNC;
   TraceIn_Reset[13] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Run[13] := BenchUut1.Run;
   TraceOut_ResetRequired[13] := BenchUut1.ResetRequired;
   BenchCalls := BenchCalls + 1;
 14:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := FALSE;
   BenchUut1.EStopNC := TRUE;
   BenchUut1.Reset := FALSE;
   TraceIn_Start[14] := BenchUut1.Start;
   TraceIn_Stop[14] := BenchUut1.Stop;
   TraceIn_EStopNC[14] := BenchUut1.EStopNC;
   TraceIn_Reset[14] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Run[14] := BenchUut1.Run;
   TraceOut_ResetRequired[14] := BenchUut1.ResetRequired;
   BenchCalls := BenchCalls + 1;
 15:
   BenchUut1.Start := FALSE;
   BenchUut1.Stop := TRUE;
   BenchUut1.EStopNC := TRUE;
   BenchUut1.Reset := FALSE;
   TraceIn_Start[15] := BenchUut1.Start;
   TraceIn_Stop[15] := BenchUut1.Stop;
   TraceIn_EStopNC[15] := BenchUut1.EStopNC;
   TraceIn_Reset[15] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Run[15] := BenchUut1.Run;
   TraceOut_ResetRequired[15] := BenchUut1.ResetRequired;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 16 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
