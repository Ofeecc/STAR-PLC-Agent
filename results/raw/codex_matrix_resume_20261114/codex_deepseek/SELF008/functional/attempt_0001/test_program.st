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
 TraceIn_Request : ARRAY[0..44] OF BOOL;
 TraceIn_Trip : ARRAY[0..44] OF BOOL;
 TraceIn_Preset : ARRAY[0..44] OF USINT;
 TraceOut_Ready : ARRAY[0..44] OF BOOL;
 TraceOut_Count : ARRAY[0..44] OF USINT;
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
   BenchUut0.Request := TRUE;
   BenchUut0.Trip := TRUE;
   BenchUut0.Preset := USINT#3;
   TraceIn_Request[4] := BenchUut0.Request;
   TraceIn_Trip[4] := BenchUut0.Trip;
   TraceIn_Preset[4] := BenchUut0.Preset;
   BenchUut0();
   TraceOut_Ready[4] := BenchUut0.Ready;
   TraceOut_Count[4] := BenchUut0.Count;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut0.Request := TRUE;
   BenchUut0.Trip := FALSE;
   BenchUut0.Preset := USINT#3;
   TraceIn_Request[5] := BenchUut0.Request;
   TraceIn_Trip[5] := BenchUut0.Trip;
   TraceIn_Preset[5] := BenchUut0.Preset;
   BenchUut0();
   TraceOut_Ready[5] := BenchUut0.Ready;
   TraceOut_Count[5] := BenchUut0.Count;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.Request := TRUE;
   BenchUut1.Trip := FALSE;
   BenchUut1.Preset := USINT#0;
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
   BenchUut1.Preset := USINT#6;
   TraceIn_Request[7] := BenchUut1.Request;
   TraceIn_Trip[7] := BenchUut1.Trip;
   TraceIn_Preset[7] := BenchUut1.Preset;
   BenchUut1();
   TraceOut_Ready[7] := BenchUut1.Ready;
   TraceOut_Count[7] := BenchUut1.Count;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.Request := TRUE;
   BenchUut1.Trip := FALSE;
   BenchUut1.Preset := USINT#5;
   TraceIn_Request[8] := BenchUut1.Request;
   TraceIn_Trip[8] := BenchUut1.Trip;
   TraceIn_Preset[8] := BenchUut1.Preset;
   BenchUut1();
   TraceOut_Ready[8] := BenchUut1.Ready;
   TraceOut_Count[8] := BenchUut1.Count;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.Request := TRUE;
   BenchUut1.Trip := FALSE;
   BenchUut1.Preset := USINT#1;
   TraceIn_Request[9] := BenchUut1.Request;
   TraceIn_Trip[9] := BenchUut1.Trip;
   TraceIn_Preset[9] := BenchUut1.Preset;
   BenchUut1();
   TraceOut_Ready[9] := BenchUut1.Ready;
   TraceOut_Count[9] := BenchUut1.Count;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.Request := FALSE;
   BenchUut1.Trip := FALSE;
   BenchUut1.Preset := USINT#5;
   TraceIn_Request[10] := BenchUut1.Request;
   TraceIn_Trip[10] := BenchUut1.Trip;
   TraceIn_Preset[10] := BenchUut1.Preset;
   BenchUut1();
   TraceOut_Ready[10] := BenchUut1.Ready;
   TraceOut_Count[10] := BenchUut1.Count;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut2.Request := TRUE;
   BenchUut2.Trip := FALSE;
   BenchUut2.Preset := USINT#1;
   TraceIn_Request[11] := BenchUut2.Request;
   TraceIn_Trip[11] := BenchUut2.Trip;
   TraceIn_Preset[11] := BenchUut2.Preset;
   BenchUut2();
   TraceOut_Ready[11] := BenchUut2.Ready;
   TraceOut_Count[11] := BenchUut2.Count;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut2.Request := TRUE;
   BenchUut2.Trip := FALSE;
   BenchUut2.Preset := USINT#4;
   TraceIn_Request[12] := BenchUut2.Request;
   TraceIn_Trip[12] := BenchUut2.Trip;
   TraceIn_Preset[12] := BenchUut2.Preset;
   BenchUut2();
   TraceOut_Ready[12] := BenchUut2.Ready;
   TraceOut_Count[12] := BenchUut2.Count;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut2.Request := TRUE;
   BenchUut2.Trip := FALSE;
   BenchUut2.Preset := USINT#4;
   TraceIn_Request[13] := BenchUut2.Request;
   TraceIn_Trip[13] := BenchUut2.Trip;
   TraceIn_Preset[13] := BenchUut2.Preset;
   BenchUut2();
   TraceOut_Ready[13] := BenchUut2.Ready;
   TraceOut_Count[13] := BenchUut2.Count;
   BenchCalls := BenchCalls + 1;
 14:
   BenchUut2.Request := TRUE;
   BenchUut2.Trip := FALSE;
   BenchUut2.Preset := USINT#4;
   TraceIn_Request[14] := BenchUut2.Request;
   TraceIn_Trip[14] := BenchUut2.Trip;
   TraceIn_Preset[14] := BenchUut2.Preset;
   BenchUut2();
   TraceOut_Ready[14] := BenchUut2.Ready;
   TraceOut_Count[14] := BenchUut2.Count;
   BenchCalls := BenchCalls + 1;
 15:
   BenchUut2.Request := TRUE;
   BenchUut2.Trip := FALSE;
   BenchUut2.Preset := USINT#2;
   TraceIn_Request[15] := BenchUut2.Request;
   TraceIn_Trip[15] := BenchUut2.Trip;
   TraceIn_Preset[15] := BenchUut2.Preset;
   BenchUut2();
   TraceOut_Ready[15] := BenchUut2.Ready;
   TraceOut_Count[15] := BenchUut2.Count;
   BenchCalls := BenchCalls + 1;
 16:
   BenchUut2.Request := TRUE;
   BenchUut2.Trip := FALSE;
   BenchUut2.Preset := USINT#255;
   TraceIn_Request[16] := BenchUut2.Request;
   TraceIn_Trip[16] := BenchUut2.Trip;
   TraceIn_Preset[16] := BenchUut2.Preset;
   BenchUut2();
   TraceOut_Ready[16] := BenchUut2.Ready;
   TraceOut_Count[16] := BenchUut2.Count;
   BenchCalls := BenchCalls + 1;
 17:
   BenchUut2.Request := TRUE;
   BenchUut2.Trip := FALSE;
   BenchUut2.Preset := USINT#2;
   TraceIn_Request[17] := BenchUut2.Request;
   TraceIn_Trip[17] := BenchUut2.Trip;
   TraceIn_Preset[17] := BenchUut2.Preset;
   BenchUut2();
   TraceOut_Ready[17] := BenchUut2.Ready;
   TraceOut_Count[17] := BenchUut2.Count;
   BenchCalls := BenchCalls + 1;
 18:
   BenchUut3.Request := TRUE;
   BenchUut3.Trip := FALSE;
   BenchUut3.Preset := USINT#1;
   TraceIn_Request[18] := BenchUut3.Request;
   TraceIn_Trip[18] := BenchUut3.Trip;
   TraceIn_Preset[18] := BenchUut3.Preset;
   BenchUut3();
   TraceOut_Ready[18] := BenchUut3.Ready;
   TraceOut_Count[18] := BenchUut3.Count;
   BenchCalls := BenchCalls + 1;
 19:
   BenchUut3.Request := TRUE;
   BenchUut3.Trip := FALSE;
   BenchUut3.Preset := USINT#5;
   TraceIn_Request[19] := BenchUut3.Request;
   TraceIn_Trip[19] := BenchUut3.Trip;
   TraceIn_Preset[19] := BenchUut3.Preset;
   BenchUut3();
   TraceOut_Ready[19] := BenchUut3.Ready;
   TraceOut_Count[19] := BenchUut3.Count;
   BenchCalls := BenchCalls + 1;
 20:
   BenchUut3.Request := TRUE;
   BenchUut3.Trip := FALSE;
   BenchUut3.Preset := USINT#2;
   TraceIn_Request[20] := BenchUut3.Request;
   TraceIn_Trip[20] := BenchUut3.Trip;
   TraceIn_Preset[20] := BenchUut3.Preset;
   BenchUut3();
   TraceOut_Ready[20] := BenchUut3.Ready;
   TraceOut_Count[20] := BenchUut3.Count;
   BenchCalls := BenchCalls + 1;
 21:
   BenchUut3.Request := TRUE;
   BenchUut3.Trip := FALSE;
   BenchUut3.Preset := USINT#0;
   TraceIn_Request[21] := BenchUut3.Request;
   TraceIn_Trip[21] := BenchUut3.Trip;
   TraceIn_Preset[21] := BenchUut3.Preset;
   BenchUut3();
   TraceOut_Ready[21] := BenchUut3.Ready;
   TraceOut_Count[21] := BenchUut3.Count;
   BenchCalls := BenchCalls + 1;
 22:
   BenchUut3.Request := TRUE;
   BenchUut3.Trip := FALSE;
   BenchUut3.Preset := USINT#5;
   TraceIn_Request[22] := BenchUut3.Request;
   TraceIn_Trip[22] := BenchUut3.Trip;
   TraceIn_Preset[22] := BenchUut3.Preset;
   BenchUut3();
   TraceOut_Ready[22] := BenchUut3.Ready;
   TraceOut_Count[22] := BenchUut3.Count;
   BenchCalls := BenchCalls + 1;
 23:
   BenchUut4.Request := TRUE;
   BenchUut4.Trip := FALSE;
   BenchUut4.Preset := USINT#3;
   TraceIn_Request[23] := BenchUut4.Request;
   TraceIn_Trip[23] := BenchUut4.Trip;
   TraceIn_Preset[23] := BenchUut4.Preset;
   BenchUut4();
   TraceOut_Ready[23] := BenchUut4.Ready;
   TraceOut_Count[23] := BenchUut4.Count;
   BenchCalls := BenchCalls + 1;
 24:
   BenchUut4.Request := TRUE;
   BenchUut4.Trip := FALSE;
   BenchUut4.Preset := USINT#3;
   TraceIn_Request[24] := BenchUut4.Request;
   TraceIn_Trip[24] := BenchUut4.Trip;
   TraceIn_Preset[24] := BenchUut4.Preset;
   BenchUut4();
   TraceOut_Ready[24] := BenchUut4.Ready;
   TraceOut_Count[24] := BenchUut4.Count;
   BenchCalls := BenchCalls + 1;
 25:
   BenchUut4.Request := TRUE;
   BenchUut4.Trip := FALSE;
   BenchUut4.Preset := USINT#3;
   TraceIn_Request[25] := BenchUut4.Request;
   TraceIn_Trip[25] := BenchUut4.Trip;
   TraceIn_Preset[25] := BenchUut4.Preset;
   BenchUut4();
   TraceOut_Ready[25] := BenchUut4.Ready;
   TraceOut_Count[25] := BenchUut4.Count;
   BenchCalls := BenchCalls + 1;
 26:
   BenchUut4.Request := TRUE;
   BenchUut4.Trip := FALSE;
   BenchUut4.Preset := USINT#3;
   TraceIn_Request[26] := BenchUut4.Request;
   TraceIn_Trip[26] := BenchUut4.Trip;
   TraceIn_Preset[26] := BenchUut4.Preset;
   BenchUut4();
   TraceOut_Ready[26] := BenchUut4.Ready;
   TraceOut_Count[26] := BenchUut4.Count;
   BenchCalls := BenchCalls + 1;
 27:
   BenchUut4.Request := TRUE;
   BenchUut4.Trip := TRUE;
   BenchUut4.Preset := USINT#3;
   TraceIn_Request[27] := BenchUut4.Request;
   TraceIn_Trip[27] := BenchUut4.Trip;
   TraceIn_Preset[27] := BenchUut4.Preset;
   BenchUut4();
   TraceOut_Ready[27] := BenchUut4.Ready;
   TraceOut_Count[27] := BenchUut4.Count;
   BenchCalls := BenchCalls + 1;
 28:
   BenchUut4.Request := TRUE;
   BenchUut4.Trip := FALSE;
   BenchUut4.Preset := USINT#3;
   TraceIn_Request[28] := BenchUut4.Request;
   TraceIn_Trip[28] := BenchUut4.Trip;
   TraceIn_Preset[28] := BenchUut4.Preset;
   BenchUut4();
   TraceOut_Ready[28] := BenchUut4.Ready;
   TraceOut_Count[28] := BenchUut4.Count;
   BenchCalls := BenchCalls + 1;
 29:
   BenchUut4.Request := FALSE;
   BenchUut4.Trip := FALSE;
   BenchUut4.Preset := USINT#3;
   TraceIn_Request[29] := BenchUut4.Request;
   TraceIn_Trip[29] := BenchUut4.Trip;
   TraceIn_Preset[29] := BenchUut4.Preset;
   BenchUut4();
   TraceOut_Ready[29] := BenchUut4.Ready;
   TraceOut_Count[29] := BenchUut4.Count;
   BenchCalls := BenchCalls + 1;
 30:
   BenchUut4.Request := FALSE;
   BenchUut4.Trip := FALSE;
   BenchUut4.Preset := USINT#3;
   TraceIn_Request[30] := BenchUut4.Request;
   TraceIn_Trip[30] := BenchUut4.Trip;
   TraceIn_Preset[30] := BenchUut4.Preset;
   BenchUut4();
   TraceOut_Ready[30] := BenchUut4.Ready;
   TraceOut_Count[30] := BenchUut4.Count;
   BenchCalls := BenchCalls + 1;
 31:
   BenchUut5.Request := TRUE;
   BenchUut5.Trip := FALSE;
   BenchUut5.Preset := USINT#3;
   TraceIn_Request[31] := BenchUut5.Request;
   TraceIn_Trip[31] := BenchUut5.Trip;
   TraceIn_Preset[31] := BenchUut5.Preset;
   BenchUut5();
   TraceOut_Ready[31] := BenchUut5.Ready;
   TraceOut_Count[31] := BenchUut5.Count;
   BenchCalls := BenchCalls + 1;
 32:
   BenchUut5.Request := TRUE;
   BenchUut5.Trip := FALSE;
   BenchUut5.Preset := USINT#3;
   TraceIn_Request[32] := BenchUut5.Request;
   TraceIn_Trip[32] := BenchUut5.Trip;
   TraceIn_Preset[32] := BenchUut5.Preset;
   BenchUut5();
   TraceOut_Ready[32] := BenchUut5.Ready;
   TraceOut_Count[32] := BenchUut5.Count;
   BenchCalls := BenchCalls + 1;
 33:
   BenchUut5.Request := TRUE;
   BenchUut5.Trip := FALSE;
   BenchUut5.Preset := USINT#3;
   TraceIn_Request[33] := BenchUut5.Request;
   TraceIn_Trip[33] := BenchUut5.Trip;
   TraceIn_Preset[33] := BenchUut5.Preset;
   BenchUut5();
   TraceOut_Ready[33] := BenchUut5.Ready;
   TraceOut_Count[33] := BenchUut5.Count;
   BenchCalls := BenchCalls + 1;
 34:
   BenchUut5.Request := TRUE;
   BenchUut5.Trip := FALSE;
   BenchUut5.Preset := USINT#3;
   TraceIn_Request[34] := BenchUut5.Request;
   TraceIn_Trip[34] := BenchUut5.Trip;
   TraceIn_Preset[34] := BenchUut5.Preset;
   BenchUut5();
   TraceOut_Ready[34] := BenchUut5.Ready;
   TraceOut_Count[34] := BenchUut5.Count;
   BenchCalls := BenchCalls + 1;
 35:
   BenchUut5.Request := TRUE;
   BenchUut5.Trip := TRUE;
   BenchUut5.Preset := USINT#3;
   TraceIn_Request[35] := BenchUut5.Request;
   TraceIn_Trip[35] := BenchUut5.Trip;
   TraceIn_Preset[35] := BenchUut5.Preset;
   BenchUut5();
   TraceOut_Ready[35] := BenchUut5.Ready;
   TraceOut_Count[35] := BenchUut5.Count;
   BenchCalls := BenchCalls + 1;
 36:
   BenchUut5.Request := TRUE;
   BenchUut5.Trip := FALSE;
   BenchUut5.Preset := USINT#3;
   TraceIn_Request[36] := BenchUut5.Request;
   TraceIn_Trip[36] := BenchUut5.Trip;
   TraceIn_Preset[36] := BenchUut5.Preset;
   BenchUut5();
   TraceOut_Ready[36] := BenchUut5.Ready;
   TraceOut_Count[36] := BenchUut5.Count;
   BenchCalls := BenchCalls + 1;
 37:
   BenchUut5.Request := TRUE;
   BenchUut5.Trip := TRUE;
   BenchUut5.Preset := USINT#3;
   TraceIn_Request[37] := BenchUut5.Request;
   TraceIn_Trip[37] := BenchUut5.Trip;
   TraceIn_Preset[37] := BenchUut5.Preset;
   BenchUut5();
   TraceOut_Ready[37] := BenchUut5.Ready;
   TraceOut_Count[37] := BenchUut5.Count;
   BenchCalls := BenchCalls + 1;
 38:
   BenchUut5.Request := TRUE;
   BenchUut5.Trip := TRUE;
   BenchUut5.Preset := USINT#3;
   TraceIn_Request[38] := BenchUut5.Request;
   TraceIn_Trip[38] := BenchUut5.Trip;
   TraceIn_Preset[38] := BenchUut5.Preset;
   BenchUut5();
   TraceOut_Ready[38] := BenchUut5.Ready;
   TraceOut_Count[38] := BenchUut5.Count;
   BenchCalls := BenchCalls + 1;
 39:
   BenchUut6.Request := TRUE;
   BenchUut6.Trip := FALSE;
   BenchUut6.Preset := USINT#0;
   TraceIn_Request[39] := BenchUut6.Request;
   TraceIn_Trip[39] := BenchUut6.Trip;
   TraceIn_Preset[39] := BenchUut6.Preset;
   BenchUut6();
   TraceOut_Ready[39] := BenchUut6.Ready;
   TraceOut_Count[39] := BenchUut6.Count;
   BenchCalls := BenchCalls + 1;
 40:
   BenchUut6.Request := TRUE;
   BenchUut6.Trip := FALSE;
   BenchUut6.Preset := USINT#6;
   TraceIn_Request[40] := BenchUut6.Request;
   TraceIn_Trip[40] := BenchUut6.Trip;
   TraceIn_Preset[40] := BenchUut6.Preset;
   BenchUut6();
   TraceOut_Ready[40] := BenchUut6.Ready;
   TraceOut_Count[40] := BenchUut6.Count;
   BenchCalls := BenchCalls + 1;
 41:
   BenchUut6.Request := TRUE;
   BenchUut6.Trip := FALSE;
   BenchUut6.Preset := USINT#2;
   TraceIn_Request[41] := BenchUut6.Request;
   TraceIn_Trip[41] := BenchUut6.Trip;
   TraceIn_Preset[41] := BenchUut6.Preset;
   BenchUut6();
   TraceOut_Ready[41] := BenchUut6.Ready;
   TraceOut_Count[41] := BenchUut6.Count;
   BenchCalls := BenchCalls + 1;
 42:
   BenchUut6.Request := TRUE;
   BenchUut6.Trip := FALSE;
   BenchUut6.Preset := USINT#2;
   TraceIn_Request[42] := BenchUut6.Request;
   TraceIn_Trip[42] := BenchUut6.Trip;
   TraceIn_Preset[42] := BenchUut6.Preset;
   BenchUut6();
   TraceOut_Ready[42] := BenchUut6.Ready;
   TraceOut_Count[42] := BenchUut6.Count;
   BenchCalls := BenchCalls + 1;
 43:
   BenchUut6.Request := TRUE;
   BenchUut6.Trip := FALSE;
   BenchUut6.Preset := USINT#1;
   TraceIn_Request[43] := BenchUut6.Request;
   TraceIn_Trip[43] := BenchUut6.Trip;
   TraceIn_Preset[43] := BenchUut6.Preset;
   BenchUut6();
   TraceOut_Ready[43] := BenchUut6.Ready;
   TraceOut_Count[43] := BenchUut6.Count;
   BenchCalls := BenchCalls + 1;
 44:
   BenchUut6.Request := FALSE;
   BenchUut6.Trip := FALSE;
   BenchUut6.Preset := USINT#2;
   TraceIn_Request[44] := BenchUut6.Request;
   TraceIn_Trip[44] := BenchUut6.Trip;
   TraceIn_Preset[44] := BenchUut6.Preset;
   BenchUut6();
   TraceOut_Ready[44] := BenchUut6.Ready;
   TraceOut_Count[44] := BenchUut6.Count;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 45 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
