PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_Enable : ARRAY[0..13] OF BOOL;
 TraceIn_Tick : ARRAY[0..13] OF BOOL;
 TraceOut_Red : ARRAY[0..13] OF BOOL;
 TraceOut_Green : ARRAY[0..13] OF BOOL;
 TraceOut_Amber : ARRAY[0..13] OF BOOL;
 TraceOut_Phase : ARRAY[0..13] OF USINT;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.Enable := TRUE;
   BenchUut0.Tick := FALSE;
   TraceIn_Enable[0] := BenchUut0.Enable;
   TraceIn_Tick[0] := BenchUut0.Tick;
   BenchUut0();
   TraceOut_Red[0] := BenchUut0.Red;
   TraceOut_Green[0] := BenchUut0.Green;
   TraceOut_Amber[0] := BenchUut0.Amber;
   TraceOut_Phase[0] := BenchUut0.Phase;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.Enable := TRUE;
   BenchUut0.Tick := TRUE;
   TraceIn_Enable[1] := BenchUut0.Enable;
   TraceIn_Tick[1] := BenchUut0.Tick;
   BenchUut0();
   TraceOut_Red[1] := BenchUut0.Red;
   TraceOut_Green[1] := BenchUut0.Green;
   TraceOut_Amber[1] := BenchUut0.Amber;
   TraceOut_Phase[1] := BenchUut0.Phase;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.Enable := TRUE;
   BenchUut0.Tick := TRUE;
   TraceIn_Enable[2] := BenchUut0.Enable;
   TraceIn_Tick[2] := BenchUut0.Tick;
   BenchUut0();
   TraceOut_Red[2] := BenchUut0.Red;
   TraceOut_Green[2] := BenchUut0.Green;
   TraceOut_Amber[2] := BenchUut0.Amber;
   TraceOut_Phase[2] := BenchUut0.Phase;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.Enable := TRUE;
   BenchUut0.Tick := TRUE;
   TraceIn_Enable[3] := BenchUut0.Enable;
   TraceIn_Tick[3] := BenchUut0.Tick;
   BenchUut0();
   TraceOut_Red[3] := BenchUut0.Red;
   TraceOut_Green[3] := BenchUut0.Green;
   TraceOut_Amber[3] := BenchUut0.Amber;
   TraceOut_Phase[3] := BenchUut0.Phase;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.Enable := TRUE;
   BenchUut0.Tick := TRUE;
   TraceIn_Enable[4] := BenchUut0.Enable;
   TraceIn_Tick[4] := BenchUut0.Tick;
   BenchUut0();
   TraceOut_Red[4] := BenchUut0.Red;
   TraceOut_Green[4] := BenchUut0.Green;
   TraceOut_Amber[4] := BenchUut0.Amber;
   TraceOut_Phase[4] := BenchUut0.Phase;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut0.Enable := TRUE;
   BenchUut0.Tick := TRUE;
   TraceIn_Enable[5] := BenchUut0.Enable;
   TraceIn_Tick[5] := BenchUut0.Tick;
   BenchUut0();
   TraceOut_Red[5] := BenchUut0.Red;
   TraceOut_Green[5] := BenchUut0.Green;
   TraceOut_Amber[5] := BenchUut0.Amber;
   TraceOut_Phase[5] := BenchUut0.Phase;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut0.Enable := TRUE;
   BenchUut0.Tick := TRUE;
   TraceIn_Enable[6] := BenchUut0.Enable;
   TraceIn_Tick[6] := BenchUut0.Tick;
   BenchUut0();
   TraceOut_Red[6] := BenchUut0.Red;
   TraceOut_Green[6] := BenchUut0.Green;
   TraceOut_Amber[6] := BenchUut0.Amber;
   TraceOut_Phase[6] := BenchUut0.Phase;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[7] := BenchUut1.Enable;
   TraceIn_Tick[7] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[7] := BenchUut1.Red;
   TraceOut_Green[7] := BenchUut1.Green;
   TraceOut_Amber[7] := BenchUut1.Amber;
   TraceOut_Phase[7] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[8] := BenchUut1.Enable;
   TraceIn_Tick[8] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[8] := BenchUut1.Red;
   TraceOut_Green[8] := BenchUut1.Green;
   TraceOut_Amber[8] := BenchUut1.Amber;
   TraceOut_Phase[8] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.Enable := FALSE;
   BenchUut1.Tick := FALSE;
   TraceIn_Enable[9] := BenchUut1.Enable;
   TraceIn_Tick[9] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[9] := BenchUut1.Red;
   TraceOut_Green[9] := BenchUut1.Green;
   TraceOut_Amber[9] := BenchUut1.Amber;
   TraceOut_Phase[9] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.Enable := FALSE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[10] := BenchUut1.Enable;
   TraceIn_Tick[10] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[10] := BenchUut1.Red;
   TraceOut_Green[10] := BenchUut1.Green;
   TraceOut_Amber[10] := BenchUut1.Amber;
   TraceOut_Phase[10] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := FALSE;
   TraceIn_Enable[11] := BenchUut1.Enable;
   TraceIn_Tick[11] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[11] := BenchUut1.Red;
   TraceOut_Green[11] := BenchUut1.Green;
   TraceOut_Amber[11] := BenchUut1.Amber;
   TraceOut_Phase[11] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[12] := BenchUut1.Enable;
   TraceIn_Tick[12] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[12] := BenchUut1.Red;
   TraceOut_Green[12] := BenchUut1.Green;
   TraceOut_Amber[12] := BenchUut1.Amber;
   TraceOut_Phase[12] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut1.Enable := TRUE;
   BenchUut1.Tick := TRUE;
   TraceIn_Enable[13] := BenchUut1.Enable;
   TraceIn_Tick[13] := BenchUut1.Tick;
   BenchUut1();
   TraceOut_Red[13] := BenchUut1.Red;
   TraceOut_Green[13] := BenchUut1.Green;
   TraceOut_Amber[13] := BenchUut1.Amber;
   TraceOut_Phase[13] := BenchUut1.Phase;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 14 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
