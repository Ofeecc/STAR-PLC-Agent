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
 TraceIn_Start : ARRAY[0..38] OF BOOL;
 TraceIn_Stop : ARRAY[0..38] OF BOOL;
 TraceIn_GuardClosed : ARRAY[0..38] OF BOOL;
 TraceOut_Run : ARRAY[0..38] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[0] := BenchUut0.Start;
   TraceIn_Stop[0] := BenchUut0.Stop;
   TraceIn_GuardClosed[0] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[0] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.Start := TRUE;
   BenchUut0.Stop := FALSE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[1] := BenchUut0.Start;
   TraceIn_Stop[1] := BenchUut0.Stop;
   TraceIn_GuardClosed[1] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[1] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[2] := BenchUut0.Start;
   TraceIn_Stop[2] := BenchUut0.Stop;
   TraceIn_GuardClosed[2] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[2] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := TRUE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[3] := BenchUut0.Start;
   TraceIn_Stop[3] := BenchUut0.Stop;
   TraceIn_GuardClosed[3] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[3] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.Start := FALSE;
   BenchUut0.Stop := FALSE;
   BenchUut0.GuardClosed := TRUE;
   TraceIn_Start[4] := BenchUut0.Start;
   TraceIn_Stop[4] := BenchUut0.Stop;
   TraceIn_GuardClosed[4] := BenchUut0.GuardClosed;
   BenchUut0();
   TraceOut_Run[4] := BenchUut0.Run;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := TRUE;
   BenchUut1.GuardClosed := TRUE;
   TraceIn_Start[5] := BenchUut1.Start;
   TraceIn_Stop[5] := BenchUut1.Stop;
   TraceIn_GuardClosed[5] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[5] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := FALSE;
   TraceIn_Start[6] := BenchUut1.Start;
   TraceIn_Stop[6] := BenchUut1.Stop;
   TraceIn_GuardClosed[6] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[6] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut1.Start := TRUE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := TRUE;
   TraceIn_Start[7] := BenchUut1.Start;
   TraceIn_Stop[7] := BenchUut1.Stop;
   TraceIn_GuardClosed[7] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[7] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.Start := FALSE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := FALSE;
   TraceIn_Start[8] := BenchUut1.Start;
   TraceIn_Stop[8] := BenchUut1.Stop;
   TraceIn_GuardClosed[8] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[8] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.Start := FALSE;
   BenchUut1.Stop := FALSE;
   BenchUut1.GuardClosed := TRUE;
   TraceIn_Start[9] := BenchUut1.Start;
   TraceIn_Stop[9] := BenchUut1.Stop;
   TraceIn_GuardClosed[9] := BenchUut1.GuardClosed;
   BenchUut1();
   TraceOut_Run[9] := BenchUut1.Run;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut2.Start := TRUE;
   BenchUut2.Stop := FALSE;
   BenchUut2.GuardClosed := TRUE;
   TraceIn_Start[10] := BenchUut2.Start;
   TraceIn_Stop[10] := BenchUut2.Stop;
   TraceIn_GuardClosed[10] := BenchUut2.GuardClosed;
   BenchUut2();
   TraceOut_Run[10] := BenchUut2.Run;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut2.Start := FALSE;
   BenchUut2.Stop := TRUE;
   BenchUut2.GuardClosed := TRUE;
   TraceIn_Start[11] := BenchUut2.Start;
   TraceIn_Stop[11] := BenchUut2.Stop;
   TraceIn_GuardClosed[11] := BenchUut2.GuardClosed;
   BenchUut2();
   TraceOut_Run[11] := BenchUut2.Run;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut2.Start := TRUE;
   BenchUut2.Stop := FALSE;
   BenchUut2.GuardClosed := FALSE;
   TraceIn_Start[12] := BenchUut2.Start;
   TraceIn_Stop[12] := BenchUut2.Stop;
   TraceIn_GuardClosed[12] := BenchUut2.GuardClosed;
   BenchUut2();
   TraceOut_Run[12] := BenchUut2.Run;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut2.Start := TRUE;
   BenchUut2.Stop := FALSE;
   BenchUut2.GuardClosed := TRUE;
   TraceIn_Start[13] := BenchUut2.Start;
   TraceIn_Stop[13] := BenchUut2.Stop;
   TraceIn_GuardClosed[13] := BenchUut2.GuardClosed;
   BenchUut2();
   TraceOut_Run[13] := BenchUut2.Run;
   BenchCalls := BenchCalls + 1;
 14:
   BenchUut2.Start := TRUE;
   BenchUut2.Stop := TRUE;
   BenchUut2.GuardClosed := TRUE;
   TraceIn_Start[14] := BenchUut2.Start;
   TraceIn_Stop[14] := BenchUut2.Stop;
   TraceIn_GuardClosed[14] := BenchUut2.GuardClosed;
   BenchUut2();
   TraceOut_Run[14] := BenchUut2.Run;
   BenchCalls := BenchCalls + 1;
 15:
   BenchUut3.Start := TRUE;
   BenchUut3.Stop := FALSE;
   BenchUut3.GuardClosed := TRUE;
   TraceIn_Start[15] := BenchUut3.Start;
   TraceIn_Stop[15] := BenchUut3.Stop;
   TraceIn_GuardClosed[15] := BenchUut3.GuardClosed;
   BenchUut3();
   TraceOut_Run[15] := BenchUut3.Run;
   BenchCalls := BenchCalls + 1;
 16:
   BenchUut3.Start := TRUE;
   BenchUut3.Stop := TRUE;
   BenchUut3.GuardClosed := TRUE;
   TraceIn_Start[16] := BenchUut3.Start;
   TraceIn_Stop[16] := BenchUut3.Stop;
   TraceIn_GuardClosed[16] := BenchUut3.GuardClosed;
   BenchUut3();
   TraceOut_Run[16] := BenchUut3.Run;
   BenchCalls := BenchCalls + 1;
 17:
   BenchUut3.Start := TRUE;
   BenchUut3.Stop := FALSE;
   BenchUut3.GuardClosed := TRUE;
   TraceIn_Start[17] := BenchUut3.Start;
   TraceIn_Stop[17] := BenchUut3.Stop;
   TraceIn_GuardClosed[17] := BenchUut3.GuardClosed;
   BenchUut3();
   TraceOut_Run[17] := BenchUut3.Run;
   BenchCalls := BenchCalls + 1;
 18:
   BenchUut4.Start := FALSE;
   BenchUut4.Stop := FALSE;
   BenchUut4.GuardClosed := TRUE;
   TraceIn_Start[18] := BenchUut4.Start;
   TraceIn_Stop[18] := BenchUut4.Stop;
   TraceIn_GuardClosed[18] := BenchUut4.GuardClosed;
   BenchUut4();
   TraceOut_Run[18] := BenchUut4.Run;
   BenchCalls := BenchCalls + 1;
 19:
   BenchUut4.Start := TRUE;
   BenchUut4.Stop := FALSE;
   BenchUut4.GuardClosed := TRUE;
   TraceIn_Start[19] := BenchUut4.Start;
   TraceIn_Stop[19] := BenchUut4.Stop;
   TraceIn_GuardClosed[19] := BenchUut4.GuardClosed;
   BenchUut4();
   TraceOut_Run[19] := BenchUut4.Run;
   BenchCalls := BenchCalls + 1;
 20:
   BenchUut4.Start := FALSE;
   BenchUut4.Stop := FALSE;
   BenchUut4.GuardClosed := TRUE;
   TraceIn_Start[20] := BenchUut4.Start;
   TraceIn_Stop[20] := BenchUut4.Stop;
   TraceIn_GuardClosed[20] := BenchUut4.GuardClosed;
   BenchUut4();
   TraceOut_Run[20] := BenchUut4.Run;
   BenchCalls := BenchCalls + 1;
 21:
   BenchUut4.Start := FALSE;
   BenchUut4.Stop := TRUE;
   BenchUut4.GuardClosed := TRUE;
   TraceIn_Start[21] := BenchUut4.Start;
   TraceIn_Stop[21] := BenchUut4.Stop;
   TraceIn_GuardClosed[21] := BenchUut4.GuardClosed;
   BenchUut4();
   TraceOut_Run[21] := BenchUut4.Run;
   BenchCalls := BenchCalls + 1;
 22:
   BenchUut4.Start := FALSE;
   BenchUut4.Stop := FALSE;
   BenchUut4.GuardClosed := TRUE;
   TraceIn_Start[22] := BenchUut4.Start;
   TraceIn_Stop[22] := BenchUut4.Stop;
   TraceIn_GuardClosed[22] := BenchUut4.GuardClosed;
   BenchUut4();
   TraceOut_Run[22] := BenchUut4.Run;
   BenchCalls := BenchCalls + 1;
 23:
   BenchUut4.Start := TRUE;
   BenchUut4.Stop := FALSE;
   BenchUut4.GuardClosed := TRUE;
   TraceIn_Start[23] := BenchUut4.Start;
   TraceIn_Stop[23] := BenchUut4.Stop;
   TraceIn_GuardClosed[23] := BenchUut4.GuardClosed;
   BenchUut4();
   TraceOut_Run[23] := BenchUut4.Run;
   BenchCalls := BenchCalls + 1;
 24:
   BenchUut4.Start := TRUE;
   BenchUut4.Stop := FALSE;
   BenchUut4.GuardClosed := TRUE;
   TraceIn_Start[24] := BenchUut4.Start;
   TraceIn_Stop[24] := BenchUut4.Stop;
   TraceIn_GuardClosed[24] := BenchUut4.GuardClosed;
   BenchUut4();
   TraceOut_Run[24] := BenchUut4.Run;
   BenchCalls := BenchCalls + 1;
 25:
   BenchUut5.Start := FALSE;
   BenchUut5.Stop := FALSE;
   BenchUut5.GuardClosed := TRUE;
   TraceIn_Start[25] := BenchUut5.Start;
   TraceIn_Stop[25] := BenchUut5.Stop;
   TraceIn_GuardClosed[25] := BenchUut5.GuardClosed;
   BenchUut5();
   TraceOut_Run[25] := BenchUut5.Run;
   BenchCalls := BenchCalls + 1;
 26:
   BenchUut5.Start := TRUE;
   BenchUut5.Stop := FALSE;
   BenchUut5.GuardClosed := TRUE;
   TraceIn_Start[26] := BenchUut5.Start;
   TraceIn_Stop[26] := BenchUut5.Stop;
   TraceIn_GuardClosed[26] := BenchUut5.GuardClosed;
   BenchUut5();
   TraceOut_Run[26] := BenchUut5.Run;
   BenchCalls := BenchCalls + 1;
 27:
   BenchUut5.Start := FALSE;
   BenchUut5.Stop := FALSE;
   BenchUut5.GuardClosed := TRUE;
   TraceIn_Start[27] := BenchUut5.Start;
   TraceIn_Stop[27] := BenchUut5.Stop;
   TraceIn_GuardClosed[27] := BenchUut5.GuardClosed;
   BenchUut5();
   TraceOut_Run[27] := BenchUut5.Run;
   BenchCalls := BenchCalls + 1;
 28:
   BenchUut5.Start := FALSE;
   BenchUut5.Stop := TRUE;
   BenchUut5.GuardClosed := TRUE;
   TraceIn_Start[28] := BenchUut5.Start;
   TraceIn_Stop[28] := BenchUut5.Stop;
   TraceIn_GuardClosed[28] := BenchUut5.GuardClosed;
   BenchUut5();
   TraceOut_Run[28] := BenchUut5.Run;
   BenchCalls := BenchCalls + 1;
 29:
   BenchUut5.Start := FALSE;
   BenchUut5.Stop := FALSE;
   BenchUut5.GuardClosed := TRUE;
   TraceIn_Start[29] := BenchUut5.Start;
   TraceIn_Stop[29] := BenchUut5.Stop;
   TraceIn_GuardClosed[29] := BenchUut5.GuardClosed;
   BenchUut5();
   TraceOut_Run[29] := BenchUut5.Run;
   BenchCalls := BenchCalls + 1;
 30:
   BenchUut5.Start := FALSE;
   BenchUut5.Stop := TRUE;
   BenchUut5.GuardClosed := TRUE;
   TraceIn_Start[30] := BenchUut5.Start;
   TraceIn_Stop[30] := BenchUut5.Stop;
   TraceIn_GuardClosed[30] := BenchUut5.GuardClosed;
   BenchUut5();
   TraceOut_Run[30] := BenchUut5.Run;
   BenchCalls := BenchCalls + 1;
 31:
   BenchUut5.Start := FALSE;
   BenchUut5.Stop := TRUE;
   BenchUut5.GuardClosed := TRUE;
   TraceIn_Start[31] := BenchUut5.Start;
   TraceIn_Stop[31] := BenchUut5.Stop;
   TraceIn_GuardClosed[31] := BenchUut5.GuardClosed;
   BenchUut5();
   TraceOut_Run[31] := BenchUut5.Run;
   BenchCalls := BenchCalls + 1;
 32:
   BenchUut6.Start := FALSE;
   BenchUut6.Stop := FALSE;
   BenchUut6.GuardClosed := TRUE;
   TraceIn_Start[32] := BenchUut6.Start;
   TraceIn_Stop[32] := BenchUut6.Stop;
   TraceIn_GuardClosed[32] := BenchUut6.GuardClosed;
   BenchUut6();
   TraceOut_Run[32] := BenchUut6.Run;
   BenchCalls := BenchCalls + 1;
 33:
   BenchUut6.Start := TRUE;
   BenchUut6.Stop := FALSE;
   BenchUut6.GuardClosed := TRUE;
   TraceIn_Start[33] := BenchUut6.Start;
   TraceIn_Stop[33] := BenchUut6.Stop;
   TraceIn_GuardClosed[33] := BenchUut6.GuardClosed;
   BenchUut6();
   TraceOut_Run[33] := BenchUut6.Run;
   BenchCalls := BenchCalls + 1;
 34:
   BenchUut6.Start := FALSE;
   BenchUut6.Stop := FALSE;
   BenchUut6.GuardClosed := TRUE;
   TraceIn_Start[34] := BenchUut6.Start;
   TraceIn_Stop[34] := BenchUut6.Stop;
   TraceIn_GuardClosed[34] := BenchUut6.GuardClosed;
   BenchUut6();
   TraceOut_Run[34] := BenchUut6.Run;
   BenchCalls := BenchCalls + 1;
 35:
   BenchUut6.Start := FALSE;
   BenchUut6.Stop := TRUE;
   BenchUut6.GuardClosed := TRUE;
   TraceIn_Start[35] := BenchUut6.Start;
   TraceIn_Stop[35] := BenchUut6.Stop;
   TraceIn_GuardClosed[35] := BenchUut6.GuardClosed;
   BenchUut6();
   TraceOut_Run[35] := BenchUut6.Run;
   BenchCalls := BenchCalls + 1;
 36:
   BenchUut6.Start := FALSE;
   BenchUut6.Stop := FALSE;
   BenchUut6.GuardClosed := TRUE;
   TraceIn_Start[36] := BenchUut6.Start;
   TraceIn_Stop[36] := BenchUut6.Stop;
   TraceIn_GuardClosed[36] := BenchUut6.GuardClosed;
   BenchUut6();
   TraceOut_Run[36] := BenchUut6.Run;
   BenchCalls := BenchCalls + 1;
 37:
   BenchUut6.Start := FALSE;
   BenchUut6.Stop := FALSE;
   BenchUut6.GuardClosed := FALSE;
   TraceIn_Start[37] := BenchUut6.Start;
   TraceIn_Stop[37] := BenchUut6.Stop;
   TraceIn_GuardClosed[37] := BenchUut6.GuardClosed;
   BenchUut6();
   TraceOut_Run[37] := BenchUut6.Run;
   BenchCalls := BenchCalls + 1;
 38:
   BenchUut6.Start := FALSE;
   BenchUut6.Stop := FALSE;
   BenchUut6.GuardClosed := FALSE;
   TraceIn_Start[38] := BenchUut6.Start;
   TraceIn_Stop[38] := BenchUut6.Stop;
   TraceIn_GuardClosed[38] := BenchUut6.GuardClosed;
   BenchUut6();
   TraceOut_Run[38] := BenchUut6.Run;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 39 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
