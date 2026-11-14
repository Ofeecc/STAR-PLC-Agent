PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_ForwardButton : ARRAY[0..12] OF BOOL;
 TraceIn_ReverseButton : ARRAY[0..12] OF BOOL;
 TraceIn_Stop : ARRAY[0..12] OF BOOL;
 TraceOut_Forward : ARRAY[0..12] OF BOOL;
 TraceOut_Reverse : ARRAY[0..12] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.ForwardButton := TRUE;
   BenchUut0.ReverseButton := FALSE;
   BenchUut0.Stop := FALSE;
   TraceIn_ForwardButton[0] := BenchUut0.ForwardButton;
   TraceIn_ReverseButton[0] := BenchUut0.ReverseButton;
   TraceIn_Stop[0] := BenchUut0.Stop;
   BenchUut0();
   TraceOut_Forward[0] := BenchUut0.Forward;
   TraceOut_Reverse[0] := BenchUut0.Reverse;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.ForwardButton := FALSE;
   BenchUut0.ReverseButton := TRUE;
   BenchUut0.Stop := FALSE;
   TraceIn_ForwardButton[1] := BenchUut0.ForwardButton;
   TraceIn_ReverseButton[1] := BenchUut0.ReverseButton;
   TraceIn_Stop[1] := BenchUut0.Stop;
   BenchUut0();
   TraceOut_Forward[1] := BenchUut0.Forward;
   TraceOut_Reverse[1] := BenchUut0.Reverse;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.ForwardButton := FALSE;
   BenchUut0.ReverseButton := TRUE;
   BenchUut0.Stop := FALSE;
   TraceIn_ForwardButton[2] := BenchUut0.ForwardButton;
   TraceIn_ReverseButton[2] := BenchUut0.ReverseButton;
   TraceIn_Stop[2] := BenchUut0.Stop;
   BenchUut0();
   TraceOut_Forward[2] := BenchUut0.Forward;
   TraceOut_Reverse[2] := BenchUut0.Reverse;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.ForwardButton := FALSE;
   BenchUut0.ReverseButton := FALSE;
   BenchUut0.Stop := FALSE;
   TraceIn_ForwardButton[3] := BenchUut0.ForwardButton;
   TraceIn_ReverseButton[3] := BenchUut0.ReverseButton;
   TraceIn_Stop[3] := BenchUut0.Stop;
   BenchUut0();
   TraceOut_Forward[3] := BenchUut0.Forward;
   TraceOut_Reverse[3] := BenchUut0.Reverse;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.ForwardButton := TRUE;
   BenchUut0.ReverseButton := FALSE;
   BenchUut0.Stop := FALSE;
   TraceIn_ForwardButton[4] := BenchUut0.ForwardButton;
   TraceIn_ReverseButton[4] := BenchUut0.ReverseButton;
   TraceIn_Stop[4] := BenchUut0.Stop;
   BenchUut0();
   TraceOut_Forward[4] := BenchUut0.Forward;
   TraceOut_Reverse[4] := BenchUut0.Reverse;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut0.ForwardButton := TRUE;
   BenchUut0.ReverseButton := FALSE;
   BenchUut0.Stop := TRUE;
   TraceIn_ForwardButton[5] := BenchUut0.ForwardButton;
   TraceIn_ReverseButton[5] := BenchUut0.ReverseButton;
   TraceIn_Stop[5] := BenchUut0.Stop;
   BenchUut0();
   TraceOut_Forward[5] := BenchUut0.Forward;
   TraceOut_Reverse[5] := BenchUut0.Reverse;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.ForwardButton := TRUE;
   BenchUut1.ReverseButton := FALSE;
   BenchUut1.Stop := FALSE;
   TraceIn_ForwardButton[6] := BenchUut1.ForwardButton;
   TraceIn_ReverseButton[6] := BenchUut1.ReverseButton;
   TraceIn_Stop[6] := BenchUut1.Stop;
   BenchUut1();
   TraceOut_Forward[6] := BenchUut1.Forward;
   TraceOut_Reverse[6] := BenchUut1.Reverse;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut1.ForwardButton := TRUE;
   BenchUut1.ReverseButton := TRUE;
   BenchUut1.Stop := FALSE;
   TraceIn_ForwardButton[7] := BenchUut1.ForwardButton;
   TraceIn_ReverseButton[7] := BenchUut1.ReverseButton;
   TraceIn_Stop[7] := BenchUut1.Stop;
   BenchUut1();
   TraceOut_Forward[7] := BenchUut1.Forward;
   TraceOut_Reverse[7] := BenchUut1.Reverse;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.ForwardButton := FALSE;
   BenchUut1.ReverseButton := TRUE;
   BenchUut1.Stop := FALSE;
   TraceIn_ForwardButton[8] := BenchUut1.ForwardButton;
   TraceIn_ReverseButton[8] := BenchUut1.ReverseButton;
   TraceIn_Stop[8] := BenchUut1.Stop;
   BenchUut1();
   TraceOut_Forward[8] := BenchUut1.Forward;
   TraceOut_Reverse[8] := BenchUut1.Reverse;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.ForwardButton := FALSE;
   BenchUut1.ReverseButton := TRUE;
   BenchUut1.Stop := TRUE;
   TraceIn_ForwardButton[9] := BenchUut1.ForwardButton;
   TraceIn_ReverseButton[9] := BenchUut1.ReverseButton;
   TraceIn_Stop[9] := BenchUut1.Stop;
   BenchUut1();
   TraceOut_Forward[9] := BenchUut1.Forward;
   TraceOut_Reverse[9] := BenchUut1.Reverse;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.ForwardButton := TRUE;
   BenchUut1.ReverseButton := FALSE;
   BenchUut1.Stop := FALSE;
   TraceIn_ForwardButton[10] := BenchUut1.ForwardButton;
   TraceIn_ReverseButton[10] := BenchUut1.ReverseButton;
   TraceIn_Stop[10] := BenchUut1.Stop;
   BenchUut1();
   TraceOut_Forward[10] := BenchUut1.Forward;
   TraceOut_Reverse[10] := BenchUut1.Reverse;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut1.ForwardButton := FALSE;
   BenchUut1.ReverseButton := TRUE;
   BenchUut1.Stop := FALSE;
   TraceIn_ForwardButton[11] := BenchUut1.ForwardButton;
   TraceIn_ReverseButton[11] := BenchUut1.ReverseButton;
   TraceIn_Stop[11] := BenchUut1.Stop;
   BenchUut1();
   TraceOut_Forward[11] := BenchUut1.Forward;
   TraceOut_Reverse[11] := BenchUut1.Reverse;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut1.ForwardButton := FALSE;
   BenchUut1.ReverseButton := TRUE;
   BenchUut1.Stop := FALSE;
   TraceIn_ForwardButton[12] := BenchUut1.ForwardButton;
   TraceIn_ReverseButton[12] := BenchUut1.ReverseButton;
   TraceIn_Stop[12] := BenchUut1.Stop;
   BenchUut1();
   TraceOut_Forward[12] := BenchUut1.Forward;
   TraceOut_Reverse[12] := BenchUut1.Reverse;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 13 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
