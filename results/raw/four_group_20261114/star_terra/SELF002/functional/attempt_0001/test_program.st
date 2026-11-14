PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 BenchUut2 : FB_Task;
 BenchUut3 : FB_Task;
 BenchUut4 : FB_Task;
 BenchUut5 : FB_Task;
 BenchUut6 : FB_Task;
 TraceIn_ForwardButton : ARRAY[0..43] OF BOOL;
 TraceIn_ReverseButton : ARRAY[0..43] OF BOOL;
 TraceIn_Stop : ARRAY[0..43] OF BOOL;
 TraceOut_Forward : ARRAY[0..43] OF BOOL;
 TraceOut_Reverse : ARRAY[0..43] OF BOOL;
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
   BenchUut0.ForwardButton := TRUE;
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
   BenchUut0.ForwardButton := FALSE;
   BenchUut0.ReverseButton := FALSE;
   BenchUut0.Stop := FALSE;
   TraceIn_ForwardButton[5] := BenchUut0.ForwardButton;
   TraceIn_ReverseButton[5] := BenchUut0.ReverseButton;
   TraceIn_Stop[5] := BenchUut0.Stop;
   BenchUut0();
   TraceOut_Forward[5] := BenchUut0.Forward;
   TraceOut_Reverse[5] := BenchUut0.Reverse;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.ForwardButton := TRUE;
   BenchUut1.ReverseButton := TRUE;
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
   BenchUut1.ReverseButton := FALSE;
   BenchUut1.Stop := FALSE;
   TraceIn_ForwardButton[7] := BenchUut1.ForwardButton;
   TraceIn_ReverseButton[7] := BenchUut1.ReverseButton;
   TraceIn_Stop[7] := BenchUut1.Stop;
   BenchUut1();
   TraceOut_Forward[7] := BenchUut1.Forward;
   TraceOut_Reverse[7] := BenchUut1.Reverse;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.ForwardButton := TRUE;
   BenchUut1.ReverseButton := FALSE;
   BenchUut1.Stop := TRUE;
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
   BenchUut1.Stop := FALSE;
   TraceIn_ForwardButton[9] := BenchUut1.ForwardButton;
   TraceIn_ReverseButton[9] := BenchUut1.ReverseButton;
   TraceIn_Stop[9] := BenchUut1.Stop;
   BenchUut1();
   TraceOut_Forward[9] := BenchUut1.Forward;
   TraceOut_Reverse[9] := BenchUut1.Reverse;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut2.ForwardButton := FALSE;
   BenchUut2.ReverseButton := TRUE;
   BenchUut2.Stop := FALSE;
   TraceIn_ForwardButton[10] := BenchUut2.ForwardButton;
   TraceIn_ReverseButton[10] := BenchUut2.ReverseButton;
   TraceIn_Stop[10] := BenchUut2.Stop;
   BenchUut2();
   TraceOut_Forward[10] := BenchUut2.Forward;
   TraceOut_Reverse[10] := BenchUut2.Reverse;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut2.ForwardButton := TRUE;
   BenchUut2.ReverseButton := FALSE;
   BenchUut2.Stop := TRUE;
   TraceIn_ForwardButton[11] := BenchUut2.ForwardButton;
   TraceIn_ReverseButton[11] := BenchUut2.ReverseButton;
   TraceIn_Stop[11] := BenchUut2.Stop;
   BenchUut2();
   TraceOut_Forward[11] := BenchUut2.Forward;
   TraceOut_Reverse[11] := BenchUut2.Reverse;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut2.ForwardButton := TRUE;
   BenchUut2.ReverseButton := FALSE;
   BenchUut2.Stop := FALSE;
   TraceIn_ForwardButton[12] := BenchUut2.ForwardButton;
   TraceIn_ReverseButton[12] := BenchUut2.ReverseButton;
   TraceIn_Stop[12] := BenchUut2.Stop;
   BenchUut2();
   TraceOut_Forward[12] := BenchUut2.Forward;
   TraceOut_Reverse[12] := BenchUut2.Reverse;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut2.ForwardButton := TRUE;
   BenchUut2.ReverseButton := TRUE;
   BenchUut2.Stop := FALSE;
   TraceIn_ForwardButton[13] := BenchUut2.ForwardButton;
   TraceIn_ReverseButton[13] := BenchUut2.ReverseButton;
   TraceIn_Stop[13] := BenchUut2.Stop;
   BenchUut2();
   TraceOut_Forward[13] := BenchUut2.Forward;
   TraceOut_Reverse[13] := BenchUut2.Reverse;
   BenchCalls := BenchCalls + 1;
 14:
   BenchUut2.ForwardButton := FALSE;
   BenchUut2.ReverseButton := TRUE;
   BenchUut2.Stop := FALSE;
   TraceIn_ForwardButton[14] := BenchUut2.ForwardButton;
   TraceIn_ReverseButton[14] := BenchUut2.ReverseButton;
   TraceIn_Stop[14] := BenchUut2.Stop;
   BenchUut2();
   TraceOut_Forward[14] := BenchUut2.Forward;
   TraceOut_Reverse[14] := BenchUut2.Reverse;
   BenchCalls := BenchCalls + 1;
 15:
   BenchUut3.ForwardButton := FALSE;
   BenchUut3.ReverseButton := TRUE;
   BenchUut3.Stop := FALSE;
   TraceIn_ForwardButton[15] := BenchUut3.ForwardButton;
   TraceIn_ReverseButton[15] := BenchUut3.ReverseButton;
   TraceIn_Stop[15] := BenchUut3.Stop;
   BenchUut3();
   TraceOut_Forward[15] := BenchUut3.Forward;
   TraceOut_Reverse[15] := BenchUut3.Reverse;
   BenchCalls := BenchCalls + 1;
 16:
   BenchUut3.ForwardButton := FALSE;
   BenchUut3.ReverseButton := TRUE;
   BenchUut3.Stop := TRUE;
   TraceIn_ForwardButton[16] := BenchUut3.ForwardButton;
   TraceIn_ReverseButton[16] := BenchUut3.ReverseButton;
   TraceIn_Stop[16] := BenchUut3.Stop;
   BenchUut3();
   TraceOut_Forward[16] := BenchUut3.Forward;
   TraceOut_Reverse[16] := BenchUut3.Reverse;
   BenchCalls := BenchCalls + 1;
 17:
   BenchUut3.ForwardButton := FALSE;
   BenchUut3.ReverseButton := TRUE;
   BenchUut3.Stop := FALSE;
   TraceIn_ForwardButton[17] := BenchUut3.ForwardButton;
   TraceIn_ReverseButton[17] := BenchUut3.ReverseButton;
   TraceIn_Stop[17] := BenchUut3.Stop;
   BenchUut3();
   TraceOut_Forward[17] := BenchUut3.Forward;
   TraceOut_Reverse[17] := BenchUut3.Reverse;
   BenchCalls := BenchCalls + 1;
 18:
   BenchUut3.ForwardButton := FALSE;
   BenchUut3.ReverseButton := FALSE;
   BenchUut3.Stop := FALSE;
   TraceIn_ForwardButton[18] := BenchUut3.ForwardButton;
   TraceIn_ReverseButton[18] := BenchUut3.ReverseButton;
   TraceIn_Stop[18] := BenchUut3.Stop;
   BenchUut3();
   TraceOut_Forward[18] := BenchUut3.Forward;
   TraceOut_Reverse[18] := BenchUut3.Reverse;
   BenchCalls := BenchCalls + 1;
 19:
   BenchUut3.ForwardButton := TRUE;
   BenchUut3.ReverseButton := FALSE;
   BenchUut3.Stop := FALSE;
   TraceIn_ForwardButton[19] := BenchUut3.ForwardButton;
   TraceIn_ReverseButton[19] := BenchUut3.ReverseButton;
   TraceIn_Stop[19] := BenchUut3.Stop;
   BenchUut3();
   TraceOut_Forward[19] := BenchUut3.Forward;
   TraceOut_Reverse[19] := BenchUut3.Reverse;
   BenchCalls := BenchCalls + 1;
 20:
   BenchUut4.ForwardButton := TRUE;
   BenchUut4.ReverseButton := FALSE;
   BenchUut4.Stop := FALSE;
   TraceIn_ForwardButton[20] := BenchUut4.ForwardButton;
   TraceIn_ReverseButton[20] := BenchUut4.ReverseButton;
   TraceIn_Stop[20] := BenchUut4.Stop;
   BenchUut4();
   TraceOut_Forward[20] := BenchUut4.Forward;
   TraceOut_Reverse[20] := BenchUut4.Reverse;
   BenchCalls := BenchCalls + 1;
 21:
   BenchUut4.ForwardButton := FALSE;
   BenchUut4.ReverseButton := TRUE;
   BenchUut4.Stop := FALSE;
   TraceIn_ForwardButton[21] := BenchUut4.ForwardButton;
   TraceIn_ReverseButton[21] := BenchUut4.ReverseButton;
   TraceIn_Stop[21] := BenchUut4.Stop;
   BenchUut4();
   TraceOut_Forward[21] := BenchUut4.Forward;
   TraceOut_Reverse[21] := BenchUut4.Reverse;
   BenchCalls := BenchCalls + 1;
 22:
   BenchUut4.ForwardButton := FALSE;
   BenchUut4.ReverseButton := TRUE;
   BenchUut4.Stop := FALSE;
   TraceIn_ForwardButton[22] := BenchUut4.ForwardButton;
   TraceIn_ReverseButton[22] := BenchUut4.ReverseButton;
   TraceIn_Stop[22] := BenchUut4.Stop;
   BenchUut4();
   TraceOut_Forward[22] := BenchUut4.Forward;
   TraceOut_Reverse[22] := BenchUut4.Reverse;
   BenchCalls := BenchCalls + 1;
 23:
   BenchUut4.ForwardButton := TRUE;
   BenchUut4.ReverseButton := FALSE;
   BenchUut4.Stop := FALSE;
   TraceIn_ForwardButton[23] := BenchUut4.ForwardButton;
   TraceIn_ReverseButton[23] := BenchUut4.ReverseButton;
   TraceIn_Stop[23] := BenchUut4.Stop;
   BenchUut4();
   TraceOut_Forward[23] := BenchUut4.Forward;
   TraceOut_Reverse[23] := BenchUut4.Reverse;
   BenchCalls := BenchCalls + 1;
 24:
   BenchUut4.ForwardButton := TRUE;
   BenchUut4.ReverseButton := FALSE;
   BenchUut4.Stop := FALSE;
   TraceIn_ForwardButton[24] := BenchUut4.ForwardButton;
   TraceIn_ReverseButton[24] := BenchUut4.ReverseButton;
   TraceIn_Stop[24] := BenchUut4.Stop;
   BenchUut4();
   TraceOut_Forward[24] := BenchUut4.Forward;
   TraceOut_Reverse[24] := BenchUut4.Reverse;
   BenchCalls := BenchCalls + 1;
 25:
   BenchUut4.ForwardButton := FALSE;
   BenchUut4.ReverseButton := FALSE;
   BenchUut4.Stop := FALSE;
   TraceIn_ForwardButton[25] := BenchUut4.ForwardButton;
   TraceIn_ReverseButton[25] := BenchUut4.ReverseButton;
   TraceIn_Stop[25] := BenchUut4.Stop;
   BenchUut4();
   TraceOut_Forward[25] := BenchUut4.Forward;
   TraceOut_Reverse[25] := BenchUut4.Reverse;
   BenchCalls := BenchCalls + 1;
 26:
   BenchUut4.ForwardButton := TRUE;
   BenchUut4.ReverseButton := FALSE;
   BenchUut4.Stop := FALSE;
   TraceIn_ForwardButton[26] := BenchUut4.ForwardButton;
   TraceIn_ReverseButton[26] := BenchUut4.ReverseButton;
   TraceIn_Stop[26] := BenchUut4.Stop;
   BenchUut4();
   TraceOut_Forward[26] := BenchUut4.Forward;
   TraceOut_Reverse[26] := BenchUut4.Reverse;
   BenchCalls := BenchCalls + 1;
 27:
   BenchUut4.ForwardButton := TRUE;
   BenchUut4.ReverseButton := FALSE;
   BenchUut4.Stop := FALSE;
   TraceIn_ForwardButton[27] := BenchUut4.ForwardButton;
   TraceIn_ReverseButton[27] := BenchUut4.ReverseButton;
   TraceIn_Stop[27] := BenchUut4.Stop;
   BenchUut4();
   TraceOut_Forward[27] := BenchUut4.Forward;
   TraceOut_Reverse[27] := BenchUut4.Reverse;
   BenchCalls := BenchCalls + 1;
 28:
   BenchUut5.ForwardButton := TRUE;
   BenchUut5.ReverseButton := FALSE;
   BenchUut5.Stop := FALSE;
   TraceIn_ForwardButton[28] := BenchUut5.ForwardButton;
   TraceIn_ReverseButton[28] := BenchUut5.ReverseButton;
   TraceIn_Stop[28] := BenchUut5.Stop;
   BenchUut5();
   TraceOut_Forward[28] := BenchUut5.Forward;
   TraceOut_Reverse[28] := BenchUut5.Reverse;
   BenchCalls := BenchCalls + 1;
 29:
   BenchUut5.ForwardButton := FALSE;
   BenchUut5.ReverseButton := TRUE;
   BenchUut5.Stop := FALSE;
   TraceIn_ForwardButton[29] := BenchUut5.ForwardButton;
   TraceIn_ReverseButton[29] := BenchUut5.ReverseButton;
   TraceIn_Stop[29] := BenchUut5.Stop;
   BenchUut5();
   TraceOut_Forward[29] := BenchUut5.Forward;
   TraceOut_Reverse[29] := BenchUut5.Reverse;
   BenchCalls := BenchCalls + 1;
 30:
   BenchUut5.ForwardButton := FALSE;
   BenchUut5.ReverseButton := TRUE;
   BenchUut5.Stop := FALSE;
   TraceIn_ForwardButton[30] := BenchUut5.ForwardButton;
   TraceIn_ReverseButton[30] := BenchUut5.ReverseButton;
   TraceIn_Stop[30] := BenchUut5.Stop;
   BenchUut5();
   TraceOut_Forward[30] := BenchUut5.Forward;
   TraceOut_Reverse[30] := BenchUut5.Reverse;
   BenchCalls := BenchCalls + 1;
 31:
   BenchUut5.ForwardButton := TRUE;
   BenchUut5.ReverseButton := FALSE;
   BenchUut5.Stop := FALSE;
   TraceIn_ForwardButton[31] := BenchUut5.ForwardButton;
   TraceIn_ReverseButton[31] := BenchUut5.ReverseButton;
   TraceIn_Stop[31] := BenchUut5.Stop;
   BenchUut5();
   TraceOut_Forward[31] := BenchUut5.Forward;
   TraceOut_Reverse[31] := BenchUut5.Reverse;
   BenchCalls := BenchCalls + 1;
 32:
   BenchUut5.ForwardButton := TRUE;
   BenchUut5.ReverseButton := FALSE;
   BenchUut5.Stop := FALSE;
   TraceIn_ForwardButton[32] := BenchUut5.ForwardButton;
   TraceIn_ReverseButton[32] := BenchUut5.ReverseButton;
   TraceIn_Stop[32] := BenchUut5.Stop;
   BenchUut5();
   TraceOut_Forward[32] := BenchUut5.Forward;
   TraceOut_Reverse[32] := BenchUut5.Reverse;
   BenchCalls := BenchCalls + 1;
 33:
   BenchUut5.ForwardButton := FALSE;
   BenchUut5.ReverseButton := FALSE;
   BenchUut5.Stop := FALSE;
   TraceIn_ForwardButton[33] := BenchUut5.ForwardButton;
   TraceIn_ReverseButton[33] := BenchUut5.ReverseButton;
   TraceIn_Stop[33] := BenchUut5.Stop;
   BenchUut5();
   TraceOut_Forward[33] := BenchUut5.Forward;
   TraceOut_Reverse[33] := BenchUut5.Reverse;
   BenchCalls := BenchCalls + 1;
 34:
   BenchUut5.ForwardButton := FALSE;
   BenchUut5.ReverseButton := TRUE;
   BenchUut5.Stop := FALSE;
   TraceIn_ForwardButton[34] := BenchUut5.ForwardButton;
   TraceIn_ReverseButton[34] := BenchUut5.ReverseButton;
   TraceIn_Stop[34] := BenchUut5.Stop;
   BenchUut5();
   TraceOut_Forward[34] := BenchUut5.Forward;
   TraceOut_Reverse[34] := BenchUut5.Reverse;
   BenchCalls := BenchCalls + 1;
 35:
   BenchUut5.ForwardButton := FALSE;
   BenchUut5.ReverseButton := TRUE;
   BenchUut5.Stop := FALSE;
   TraceIn_ForwardButton[35] := BenchUut5.ForwardButton;
   TraceIn_ReverseButton[35] := BenchUut5.ReverseButton;
   TraceIn_Stop[35] := BenchUut5.Stop;
   BenchUut5();
   TraceOut_Forward[35] := BenchUut5.Forward;
   TraceOut_Reverse[35] := BenchUut5.Reverse;
   BenchCalls := BenchCalls + 1;
 36:
   BenchUut6.ForwardButton := TRUE;
   BenchUut6.ReverseButton := FALSE;
   BenchUut6.Stop := FALSE;
   TraceIn_ForwardButton[36] := BenchUut6.ForwardButton;
   TraceIn_ReverseButton[36] := BenchUut6.ReverseButton;
   TraceIn_Stop[36] := BenchUut6.Stop;
   BenchUut6();
   TraceOut_Forward[36] := BenchUut6.Forward;
   TraceOut_Reverse[36] := BenchUut6.Reverse;
   BenchCalls := BenchCalls + 1;
 37:
   BenchUut6.ForwardButton := FALSE;
   BenchUut6.ReverseButton := TRUE;
   BenchUut6.Stop := FALSE;
   TraceIn_ForwardButton[37] := BenchUut6.ForwardButton;
   TraceIn_ReverseButton[37] := BenchUut6.ReverseButton;
   TraceIn_Stop[37] := BenchUut6.Stop;
   BenchUut6();
   TraceOut_Forward[37] := BenchUut6.Forward;
   TraceOut_Reverse[37] := BenchUut6.Reverse;
   BenchCalls := BenchCalls + 1;
 38:
   BenchUut6.ForwardButton := FALSE;
   BenchUut6.ReverseButton := TRUE;
   BenchUut6.Stop := FALSE;
   TraceIn_ForwardButton[38] := BenchUut6.ForwardButton;
   TraceIn_ReverseButton[38] := BenchUut6.ReverseButton;
   TraceIn_Stop[38] := BenchUut6.Stop;
   BenchUut6();
   TraceOut_Forward[38] := BenchUut6.Forward;
   TraceOut_Reverse[38] := BenchUut6.Reverse;
   BenchCalls := BenchCalls + 1;
 39:
   BenchUut6.ForwardButton := TRUE;
   BenchUut6.ReverseButton := FALSE;
   BenchUut6.Stop := FALSE;
   TraceIn_ForwardButton[39] := BenchUut6.ForwardButton;
   TraceIn_ReverseButton[39] := BenchUut6.ReverseButton;
   TraceIn_Stop[39] := BenchUut6.Stop;
   BenchUut6();
   TraceOut_Forward[39] := BenchUut6.Forward;
   TraceOut_Reverse[39] := BenchUut6.Reverse;
   BenchCalls := BenchCalls + 1;
 40:
   BenchUut6.ForwardButton := TRUE;
   BenchUut6.ReverseButton := FALSE;
   BenchUut6.Stop := FALSE;
   TraceIn_ForwardButton[40] := BenchUut6.ForwardButton;
   TraceIn_ReverseButton[40] := BenchUut6.ReverseButton;
   TraceIn_Stop[40] := BenchUut6.Stop;
   BenchUut6();
   TraceOut_Forward[40] := BenchUut6.Forward;
   TraceOut_Reverse[40] := BenchUut6.Reverse;
   BenchCalls := BenchCalls + 1;
 41:
   BenchUut6.ForwardButton := FALSE;
   BenchUut6.ReverseButton := FALSE;
   BenchUut6.Stop := FALSE;
   TraceIn_ForwardButton[41] := BenchUut6.ForwardButton;
   TraceIn_ReverseButton[41] := BenchUut6.ReverseButton;
   TraceIn_Stop[41] := BenchUut6.Stop;
   BenchUut6();
   TraceOut_Forward[41] := BenchUut6.Forward;
   TraceOut_Reverse[41] := BenchUut6.Reverse;
   BenchCalls := BenchCalls + 1;
 42:
   BenchUut6.ForwardButton := FALSE;
   BenchUut6.ReverseButton := FALSE;
   BenchUut6.Stop := TRUE;
   TraceIn_ForwardButton[42] := BenchUut6.ForwardButton;
   TraceIn_ReverseButton[42] := BenchUut6.ReverseButton;
   TraceIn_Stop[42] := BenchUut6.Stop;
   BenchUut6();
   TraceOut_Forward[42] := BenchUut6.Forward;
   TraceOut_Reverse[42] := BenchUut6.Reverse;
   BenchCalls := BenchCalls + 1;
 43:
   BenchUut6.ForwardButton := FALSE;
   BenchUut6.ReverseButton := FALSE;
   BenchUut6.Stop := TRUE;
   TraceIn_ForwardButton[43] := BenchUut6.ForwardButton;
   TraceIn_ReverseButton[43] := BenchUut6.ReverseButton;
   TraceIn_Stop[43] := BenchUut6.Stop;
   BenchUut6();
   TraceOut_Forward[43] := BenchUut6.Forward;
   TraceOut_Reverse[43] := BenchUut6.Reverse;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 44 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
