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
 TraceIn_LowWet : ARRAY[0..38] OF BOOL;
 TraceIn_HighWet : ARRAY[0..38] OF BOOL;
 TraceIn_Inhibit : ARRAY[0..38] OF BOOL;
 TraceOut_Fill : ARRAY[0..38] OF BOOL;
 TraceOut_SensorFault : ARRAY[0..38] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.LowWet := FALSE;
   BenchUut0.HighWet := FALSE;
   BenchUut0.Inhibit := FALSE;
   TraceIn_LowWet[0] := BenchUut0.LowWet;
   TraceIn_HighWet[0] := BenchUut0.HighWet;
   TraceIn_Inhibit[0] := BenchUut0.Inhibit;
   BenchUut0();
   TraceOut_Fill[0] := BenchUut0.Fill;
   TraceOut_SensorFault[0] := BenchUut0.SensorFault;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.LowWet := TRUE;
   BenchUut0.HighWet := FALSE;
   BenchUut0.Inhibit := FALSE;
   TraceIn_LowWet[1] := BenchUut0.LowWet;
   TraceIn_HighWet[1] := BenchUut0.HighWet;
   TraceIn_Inhibit[1] := BenchUut0.Inhibit;
   BenchUut0();
   TraceOut_Fill[1] := BenchUut0.Fill;
   TraceOut_SensorFault[1] := BenchUut0.SensorFault;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.LowWet := TRUE;
   BenchUut0.HighWet := TRUE;
   BenchUut0.Inhibit := FALSE;
   TraceIn_LowWet[2] := BenchUut0.LowWet;
   TraceIn_HighWet[2] := BenchUut0.HighWet;
   TraceIn_Inhibit[2] := BenchUut0.Inhibit;
   BenchUut0();
   TraceOut_Fill[2] := BenchUut0.Fill;
   TraceOut_SensorFault[2] := BenchUut0.SensorFault;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.LowWet := TRUE;
   BenchUut0.HighWet := FALSE;
   BenchUut0.Inhibit := FALSE;
   TraceIn_LowWet[3] := BenchUut0.LowWet;
   TraceIn_HighWet[3] := BenchUut0.HighWet;
   TraceIn_Inhibit[3] := BenchUut0.Inhibit;
   BenchUut0();
   TraceOut_Fill[3] := BenchUut0.Fill;
   TraceOut_SensorFault[3] := BenchUut0.SensorFault;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.LowWet := FALSE;
   BenchUut0.HighWet := FALSE;
   BenchUut0.Inhibit := FALSE;
   TraceIn_LowWet[4] := BenchUut0.LowWet;
   TraceIn_HighWet[4] := BenchUut0.HighWet;
   TraceIn_Inhibit[4] := BenchUut0.Inhibit;
   BenchUut0();
   TraceOut_Fill[4] := BenchUut0.Fill;
   TraceOut_SensorFault[4] := BenchUut0.SensorFault;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut1.LowWet := TRUE;
   BenchUut1.HighWet := FALSE;
   BenchUut1.Inhibit := FALSE;
   TraceIn_LowWet[5] := BenchUut1.LowWet;
   TraceIn_HighWet[5] := BenchUut1.HighWet;
   TraceIn_Inhibit[5] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[5] := BenchUut1.Fill;
   TraceOut_SensorFault[5] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.LowWet := FALSE;
   BenchUut1.HighWet := TRUE;
   BenchUut1.Inhibit := FALSE;
   TraceIn_LowWet[6] := BenchUut1.LowWet;
   TraceIn_HighWet[6] := BenchUut1.HighWet;
   TraceIn_Inhibit[6] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[6] := BenchUut1.Fill;
   TraceOut_SensorFault[6] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut1.LowWet := FALSE;
   BenchUut1.HighWet := FALSE;
   BenchUut1.Inhibit := FALSE;
   TraceIn_LowWet[7] := BenchUut1.LowWet;
   TraceIn_HighWet[7] := BenchUut1.HighWet;
   TraceIn_Inhibit[7] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[7] := BenchUut1.Fill;
   TraceOut_SensorFault[7] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.LowWet := TRUE;
   BenchUut1.HighWet := FALSE;
   BenchUut1.Inhibit := TRUE;
   TraceIn_LowWet[8] := BenchUut1.LowWet;
   TraceIn_HighWet[8] := BenchUut1.HighWet;
   TraceIn_Inhibit[8] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[8] := BenchUut1.Fill;
   TraceOut_SensorFault[8] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.LowWet := TRUE;
   BenchUut1.HighWet := FALSE;
   BenchUut1.Inhibit := FALSE;
   TraceIn_LowWet[9] := BenchUut1.LowWet;
   TraceIn_HighWet[9] := BenchUut1.HighWet;
   TraceIn_Inhibit[9] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[9] := BenchUut1.Fill;
   TraceOut_SensorFault[9] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut2.LowWet := FALSE;
   BenchUut2.HighWet := FALSE;
   BenchUut2.Inhibit := FALSE;
   TraceIn_LowWet[10] := BenchUut2.LowWet;
   TraceIn_HighWet[10] := BenchUut2.HighWet;
   TraceIn_Inhibit[10] := BenchUut2.Inhibit;
   BenchUut2();
   TraceOut_Fill[10] := BenchUut2.Fill;
   TraceOut_SensorFault[10] := BenchUut2.SensorFault;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut2.LowWet := FALSE;
   BenchUut2.HighWet := TRUE;
   BenchUut2.Inhibit := TRUE;
   TraceIn_LowWet[11] := BenchUut2.LowWet;
   TraceIn_HighWet[11] := BenchUut2.HighWet;
   TraceIn_Inhibit[11] := BenchUut2.Inhibit;
   BenchUut2();
   TraceOut_Fill[11] := BenchUut2.Fill;
   TraceOut_SensorFault[11] := BenchUut2.SensorFault;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut2.LowWet := TRUE;
   BenchUut2.HighWet := FALSE;
   BenchUut2.Inhibit := FALSE;
   TraceIn_LowWet[12] := BenchUut2.LowWet;
   TraceIn_HighWet[12] := BenchUut2.HighWet;
   TraceIn_Inhibit[12] := BenchUut2.Inhibit;
   BenchUut2();
   TraceOut_Fill[12] := BenchUut2.Fill;
   TraceOut_SensorFault[12] := BenchUut2.SensorFault;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut2.LowWet := FALSE;
   BenchUut2.HighWet := FALSE;
   BenchUut2.Inhibit := FALSE;
   TraceIn_LowWet[13] := BenchUut2.LowWet;
   TraceIn_HighWet[13] := BenchUut2.HighWet;
   TraceIn_Inhibit[13] := BenchUut2.Inhibit;
   BenchUut2();
   TraceOut_Fill[13] := BenchUut2.Fill;
   TraceOut_SensorFault[13] := BenchUut2.SensorFault;
   BenchCalls := BenchCalls + 1;
 14:
   BenchUut2.LowWet := TRUE;
   BenchUut2.HighWet := TRUE;
   BenchUut2.Inhibit := FALSE;
   TraceIn_LowWet[14] := BenchUut2.LowWet;
   TraceIn_HighWet[14] := BenchUut2.HighWet;
   TraceIn_Inhibit[14] := BenchUut2.Inhibit;
   BenchUut2();
   TraceOut_Fill[14] := BenchUut2.Fill;
   TraceOut_SensorFault[14] := BenchUut2.SensorFault;
   BenchCalls := BenchCalls + 1;
 15:
   BenchUut3.LowWet := FALSE;
   BenchUut3.HighWet := FALSE;
   BenchUut3.Inhibit := FALSE;
   TraceIn_LowWet[15] := BenchUut3.LowWet;
   TraceIn_HighWet[15] := BenchUut3.HighWet;
   TraceIn_Inhibit[15] := BenchUut3.Inhibit;
   BenchUut3();
   TraceOut_Fill[15] := BenchUut3.Fill;
   TraceOut_SensorFault[15] := BenchUut3.SensorFault;
   BenchCalls := BenchCalls + 1;
 16:
   BenchUut3.LowWet := TRUE;
   BenchUut3.HighWet := FALSE;
   BenchUut3.Inhibit := FALSE;
   TraceIn_LowWet[16] := BenchUut3.LowWet;
   TraceIn_HighWet[16] := BenchUut3.HighWet;
   TraceIn_Inhibit[16] := BenchUut3.Inhibit;
   BenchUut3();
   TraceOut_Fill[16] := BenchUut3.Fill;
   TraceOut_SensorFault[16] := BenchUut3.SensorFault;
   BenchCalls := BenchCalls + 1;
 17:
   BenchUut3.LowWet := TRUE;
   BenchUut3.HighWet := TRUE;
   BenchUut3.Inhibit := FALSE;
   TraceIn_LowWet[17] := BenchUut3.LowWet;
   TraceIn_HighWet[17] := BenchUut3.HighWet;
   TraceIn_Inhibit[17] := BenchUut3.Inhibit;
   BenchUut3();
   TraceOut_Fill[17] := BenchUut3.Fill;
   TraceOut_SensorFault[17] := BenchUut3.SensorFault;
   BenchCalls := BenchCalls + 1;
 18:
   BenchUut3.LowWet := TRUE;
   BenchUut3.HighWet := FALSE;
   BenchUut3.Inhibit := FALSE;
   TraceIn_LowWet[18] := BenchUut3.LowWet;
   TraceIn_HighWet[18] := BenchUut3.HighWet;
   TraceIn_Inhibit[18] := BenchUut3.Inhibit;
   BenchUut3();
   TraceOut_Fill[18] := BenchUut3.Fill;
   TraceOut_SensorFault[18] := BenchUut3.SensorFault;
   BenchCalls := BenchCalls + 1;
 19:
   BenchUut3.LowWet := FALSE;
   BenchUut3.HighWet := FALSE;
   BenchUut3.Inhibit := FALSE;
   TraceIn_LowWet[19] := BenchUut3.LowWet;
   TraceIn_HighWet[19] := BenchUut3.HighWet;
   TraceIn_Inhibit[19] := BenchUut3.Inhibit;
   BenchUut3();
   TraceOut_Fill[19] := BenchUut3.Fill;
   TraceOut_SensorFault[19] := BenchUut3.SensorFault;
   BenchCalls := BenchCalls + 1;
 20:
   BenchUut3.LowWet := TRUE;
   BenchUut3.HighWet := FALSE;
   BenchUut3.Inhibit := FALSE;
   TraceIn_LowWet[20] := BenchUut3.LowWet;
   TraceIn_HighWet[20] := BenchUut3.HighWet;
   TraceIn_Inhibit[20] := BenchUut3.Inhibit;
   BenchUut3();
   TraceOut_Fill[20] := BenchUut3.Fill;
   TraceOut_SensorFault[20] := BenchUut3.SensorFault;
   BenchCalls := BenchCalls + 1;
 21:
   BenchUut3.LowWet := TRUE;
   BenchUut3.HighWet := FALSE;
   BenchUut3.Inhibit := FALSE;
   TraceIn_LowWet[21] := BenchUut3.LowWet;
   TraceIn_HighWet[21] := BenchUut3.HighWet;
   TraceIn_Inhibit[21] := BenchUut3.Inhibit;
   BenchUut3();
   TraceOut_Fill[21] := BenchUut3.Fill;
   TraceOut_SensorFault[21] := BenchUut3.SensorFault;
   BenchCalls := BenchCalls + 1;
 22:
   BenchUut4.LowWet := FALSE;
   BenchUut4.HighWet := FALSE;
   BenchUut4.Inhibit := FALSE;
   TraceIn_LowWet[22] := BenchUut4.LowWet;
   TraceIn_HighWet[22] := BenchUut4.HighWet;
   TraceIn_Inhibit[22] := BenchUut4.Inhibit;
   BenchUut4();
   TraceOut_Fill[22] := BenchUut4.Fill;
   TraceOut_SensorFault[22] := BenchUut4.SensorFault;
   BenchCalls := BenchCalls + 1;
 23:
   BenchUut4.LowWet := TRUE;
   BenchUut4.HighWet := FALSE;
   BenchUut4.Inhibit := FALSE;
   TraceIn_LowWet[23] := BenchUut4.LowWet;
   TraceIn_HighWet[23] := BenchUut4.HighWet;
   TraceIn_Inhibit[23] := BenchUut4.Inhibit;
   BenchUut4();
   TraceOut_Fill[23] := BenchUut4.Fill;
   TraceOut_SensorFault[23] := BenchUut4.SensorFault;
   BenchCalls := BenchCalls + 1;
 24:
   BenchUut4.LowWet := TRUE;
   BenchUut4.HighWet := TRUE;
   BenchUut4.Inhibit := FALSE;
   TraceIn_LowWet[24] := BenchUut4.LowWet;
   TraceIn_HighWet[24] := BenchUut4.HighWet;
   TraceIn_Inhibit[24] := BenchUut4.Inhibit;
   BenchUut4();
   TraceOut_Fill[24] := BenchUut4.Fill;
   TraceOut_SensorFault[24] := BenchUut4.SensorFault;
   BenchCalls := BenchCalls + 1;
 25:
   BenchUut4.LowWet := TRUE;
   BenchUut4.HighWet := FALSE;
   BenchUut4.Inhibit := FALSE;
   TraceIn_LowWet[25] := BenchUut4.LowWet;
   TraceIn_HighWet[25] := BenchUut4.HighWet;
   TraceIn_Inhibit[25] := BenchUut4.Inhibit;
   BenchUut4();
   TraceOut_Fill[25] := BenchUut4.Fill;
   TraceOut_SensorFault[25] := BenchUut4.SensorFault;
   BenchCalls := BenchCalls + 1;
 26:
   BenchUut4.LowWet := FALSE;
   BenchUut4.HighWet := FALSE;
   BenchUut4.Inhibit := FALSE;
   TraceIn_LowWet[26] := BenchUut4.LowWet;
   TraceIn_HighWet[26] := BenchUut4.HighWet;
   TraceIn_Inhibit[26] := BenchUut4.Inhibit;
   BenchUut4();
   TraceOut_Fill[26] := BenchUut4.Fill;
   TraceOut_SensorFault[26] := BenchUut4.SensorFault;
   BenchCalls := BenchCalls + 1;
 27:
   BenchUut4.LowWet := FALSE;
   BenchUut4.HighWet := TRUE;
   BenchUut4.Inhibit := FALSE;
   TraceIn_LowWet[27] := BenchUut4.LowWet;
   TraceIn_HighWet[27] := BenchUut4.HighWet;
   TraceIn_Inhibit[27] := BenchUut4.Inhibit;
   BenchUut4();
   TraceOut_Fill[27] := BenchUut4.Fill;
   TraceOut_SensorFault[27] := BenchUut4.SensorFault;
   BenchCalls := BenchCalls + 1;
 28:
   BenchUut4.LowWet := FALSE;
   BenchUut4.HighWet := TRUE;
   BenchUut4.Inhibit := FALSE;
   TraceIn_LowWet[28] := BenchUut4.LowWet;
   TraceIn_HighWet[28] := BenchUut4.HighWet;
   TraceIn_Inhibit[28] := BenchUut4.Inhibit;
   BenchUut4();
   TraceOut_Fill[28] := BenchUut4.Fill;
   TraceOut_SensorFault[28] := BenchUut4.SensorFault;
   BenchCalls := BenchCalls + 1;
 29:
   BenchUut5.LowWet := FALSE;
   BenchUut5.HighWet := FALSE;
   BenchUut5.Inhibit := FALSE;
   TraceIn_LowWet[29] := BenchUut5.LowWet;
   TraceIn_HighWet[29] := BenchUut5.HighWet;
   TraceIn_Inhibit[29] := BenchUut5.Inhibit;
   BenchUut5();
   TraceOut_Fill[29] := BenchUut5.Fill;
   TraceOut_SensorFault[29] := BenchUut5.SensorFault;
   BenchCalls := BenchCalls + 1;
 30:
   BenchUut5.LowWet := TRUE;
   BenchUut5.HighWet := FALSE;
   BenchUut5.Inhibit := FALSE;
   TraceIn_LowWet[30] := BenchUut5.LowWet;
   TraceIn_HighWet[30] := BenchUut5.HighWet;
   TraceIn_Inhibit[30] := BenchUut5.Inhibit;
   BenchUut5();
   TraceOut_Fill[30] := BenchUut5.Fill;
   TraceOut_SensorFault[30] := BenchUut5.SensorFault;
   BenchCalls := BenchCalls + 1;
 31:
   BenchUut5.LowWet := TRUE;
   BenchUut5.HighWet := TRUE;
   BenchUut5.Inhibit := FALSE;
   TraceIn_LowWet[31] := BenchUut5.LowWet;
   TraceIn_HighWet[31] := BenchUut5.HighWet;
   TraceIn_Inhibit[31] := BenchUut5.Inhibit;
   BenchUut5();
   TraceOut_Fill[31] := BenchUut5.Fill;
   TraceOut_SensorFault[31] := BenchUut5.SensorFault;
   BenchCalls := BenchCalls + 1;
 32:
   BenchUut5.LowWet := TRUE;
   BenchUut5.HighWet := FALSE;
   BenchUut5.Inhibit := FALSE;
   TraceIn_LowWet[32] := BenchUut5.LowWet;
   TraceIn_HighWet[32] := BenchUut5.HighWet;
   TraceIn_Inhibit[32] := BenchUut5.Inhibit;
   BenchUut5();
   TraceOut_Fill[32] := BenchUut5.Fill;
   TraceOut_SensorFault[32] := BenchUut5.SensorFault;
   BenchCalls := BenchCalls + 1;
 33:
   BenchUut5.LowWet := FALSE;
   BenchUut5.HighWet := FALSE;
   BenchUut5.Inhibit := FALSE;
   TraceIn_LowWet[33] := BenchUut5.LowWet;
   TraceIn_HighWet[33] := BenchUut5.HighWet;
   TraceIn_Inhibit[33] := BenchUut5.Inhibit;
   BenchUut5();
   TraceOut_Fill[33] := BenchUut5.Fill;
   TraceOut_SensorFault[33] := BenchUut5.SensorFault;
   BenchCalls := BenchCalls + 1;
 34:
   BenchUut5.LowWet := FALSE;
   BenchUut5.HighWet := FALSE;
   BenchUut5.Inhibit := TRUE;
   TraceIn_LowWet[34] := BenchUut5.LowWet;
   TraceIn_HighWet[34] := BenchUut5.HighWet;
   TraceIn_Inhibit[34] := BenchUut5.Inhibit;
   BenchUut5();
   TraceOut_Fill[34] := BenchUut5.Fill;
   TraceOut_SensorFault[34] := BenchUut5.SensorFault;
   BenchCalls := BenchCalls + 1;
 35:
   BenchUut5.LowWet := FALSE;
   BenchUut5.HighWet := FALSE;
   BenchUut5.Inhibit := TRUE;
   TraceIn_LowWet[35] := BenchUut5.LowWet;
   TraceIn_HighWet[35] := BenchUut5.HighWet;
   TraceIn_Inhibit[35] := BenchUut5.Inhibit;
   BenchUut5();
   TraceOut_Fill[35] := BenchUut5.Fill;
   TraceOut_SensorFault[35] := BenchUut5.SensorFault;
   BenchCalls := BenchCalls + 1;
 36:
   BenchUut6.LowWet := FALSE;
   BenchUut6.HighWet := FALSE;
   BenchUut6.Inhibit := FALSE;
   TraceIn_LowWet[36] := BenchUut6.LowWet;
   TraceIn_HighWet[36] := BenchUut6.HighWet;
   TraceIn_Inhibit[36] := BenchUut6.Inhibit;
   BenchUut6();
   TraceOut_Fill[36] := BenchUut6.Fill;
   TraceOut_SensorFault[36] := BenchUut6.SensorFault;
   BenchCalls := BenchCalls + 1;
 37:
   BenchUut6.LowWet := FALSE;
   BenchUut6.HighWet := TRUE;
   BenchUut6.Inhibit := TRUE;
   TraceIn_LowWet[37] := BenchUut6.LowWet;
   TraceIn_HighWet[37] := BenchUut6.HighWet;
   TraceIn_Inhibit[37] := BenchUut6.Inhibit;
   BenchUut6();
   TraceOut_Fill[37] := BenchUut6.Fill;
   TraceOut_SensorFault[37] := BenchUut6.SensorFault;
   BenchCalls := BenchCalls + 1;
 38:
   BenchUut6.LowWet := TRUE;
   BenchUut6.HighWet := FALSE;
   BenchUut6.Inhibit := FALSE;
   TraceIn_LowWet[38] := BenchUut6.LowWet;
   TraceIn_HighWet[38] := BenchUut6.HighWet;
   TraceIn_Inhibit[38] := BenchUut6.Inhibit;
   BenchUut6();
   TraceOut_Fill[38] := BenchUut6.Fill;
   TraceOut_SensorFault[38] := BenchUut6.SensorFault;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 39 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
