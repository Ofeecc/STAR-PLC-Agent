PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_LowWet : ARRAY[0..15] OF BOOL;
 TraceIn_HighWet : ARRAY[0..15] OF BOOL;
 TraceIn_Inhibit : ARRAY[0..15] OF BOOL;
 TraceOut_Fill : ARRAY[0..15] OF BOOL;
 TraceOut_SensorFault : ARRAY[0..15] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.LowWet := TRUE;
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
   BenchUut0.LowWet := FALSE;
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
   BenchUut0.HighWet := FALSE;
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
   BenchUut0.HighWet := TRUE;
   BenchUut0.Inhibit := FALSE;
   TraceIn_LowWet[3] := BenchUut0.LowWet;
   TraceIn_HighWet[3] := BenchUut0.HighWet;
   TraceIn_Inhibit[3] := BenchUut0.Inhibit;
   BenchUut0();
   TraceOut_Fill[3] := BenchUut0.Fill;
   TraceOut_SensorFault[3] := BenchUut0.SensorFault;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.LowWet := TRUE;
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
   BenchUut0.LowWet := FALSE;
   BenchUut0.HighWet := FALSE;
   BenchUut0.Inhibit := FALSE;
   TraceIn_LowWet[5] := BenchUut0.LowWet;
   TraceIn_HighWet[5] := BenchUut0.HighWet;
   TraceIn_Inhibit[5] := BenchUut0.Inhibit;
   BenchUut0();
   TraceOut_Fill[5] := BenchUut0.Fill;
   TraceOut_SensorFault[5] := BenchUut0.SensorFault;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut0.LowWet := TRUE;
   BenchUut0.HighWet := FALSE;
   BenchUut0.Inhibit := TRUE;
   TraceIn_LowWet[6] := BenchUut0.LowWet;
   TraceIn_HighWet[6] := BenchUut0.HighWet;
   TraceIn_Inhibit[6] := BenchUut0.Inhibit;
   BenchUut0();
   TraceOut_Fill[6] := BenchUut0.Fill;
   TraceOut_SensorFault[6] := BenchUut0.SensorFault;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut0.LowWet := TRUE;
   BenchUut0.HighWet := FALSE;
   BenchUut0.Inhibit := FALSE;
   TraceIn_LowWet[7] := BenchUut0.LowWet;
   TraceIn_HighWet[7] := BenchUut0.HighWet;
   TraceIn_Inhibit[7] := BenchUut0.Inhibit;
   BenchUut0();
   TraceOut_Fill[7] := BenchUut0.Fill;
   TraceOut_SensorFault[7] := BenchUut0.SensorFault;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.LowWet := FALSE;
   BenchUut1.HighWet := FALSE;
   BenchUut1.Inhibit := FALSE;
   TraceIn_LowWet[8] := BenchUut1.LowWet;
   TraceIn_HighWet[8] := BenchUut1.HighWet;
   TraceIn_Inhibit[8] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[8] := BenchUut1.Fill;
   TraceOut_SensorFault[8] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.LowWet := FALSE;
   BenchUut1.HighWet := TRUE;
   BenchUut1.Inhibit := FALSE;
   TraceIn_LowWet[9] := BenchUut1.LowWet;
   TraceIn_HighWet[9] := BenchUut1.HighWet;
   TraceIn_Inhibit[9] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[9] := BenchUut1.Fill;
   TraceOut_SensorFault[9] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.LowWet := TRUE;
   BenchUut1.HighWet := FALSE;
   BenchUut1.Inhibit := FALSE;
   TraceIn_LowWet[10] := BenchUut1.LowWet;
   TraceIn_HighWet[10] := BenchUut1.HighWet;
   TraceIn_Inhibit[10] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[10] := BenchUut1.Fill;
   TraceOut_SensorFault[10] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut1.LowWet := FALSE;
   BenchUut1.HighWet := FALSE;
   BenchUut1.Inhibit := FALSE;
   TraceIn_LowWet[11] := BenchUut1.LowWet;
   TraceIn_HighWet[11] := BenchUut1.HighWet;
   TraceIn_Inhibit[11] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[11] := BenchUut1.Fill;
   TraceOut_SensorFault[11] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut1.LowWet := FALSE;
   BenchUut1.HighWet := FALSE;
   BenchUut1.Inhibit := TRUE;
   TraceIn_LowWet[12] := BenchUut1.LowWet;
   TraceIn_HighWet[12] := BenchUut1.HighWet;
   TraceIn_Inhibit[12] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[12] := BenchUut1.Fill;
   TraceOut_SensorFault[12] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut1.LowWet := FALSE;
   BenchUut1.HighWet := FALSE;
   BenchUut1.Inhibit := FALSE;
   TraceIn_LowWet[13] := BenchUut1.LowWet;
   TraceIn_HighWet[13] := BenchUut1.HighWet;
   TraceIn_Inhibit[13] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[13] := BenchUut1.Fill;
   TraceOut_SensorFault[13] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 14:
   BenchUut1.LowWet := FALSE;
   BenchUut1.HighWet := TRUE;
   BenchUut1.Inhibit := TRUE;
   TraceIn_LowWet[14] := BenchUut1.LowWet;
   TraceIn_HighWet[14] := BenchUut1.HighWet;
   TraceIn_Inhibit[14] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[14] := BenchUut1.Fill;
   TraceOut_SensorFault[14] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 15:
   BenchUut1.LowWet := TRUE;
   BenchUut1.HighWet := TRUE;
   BenchUut1.Inhibit := TRUE;
   TraceIn_LowWet[15] := BenchUut1.LowWet;
   TraceIn_HighWet[15] := BenchUut1.HighWet;
   TraceIn_Inhibit[15] := BenchUut1.Inhibit;
   BenchUut1();
   TraceOut_Fill[15] := BenchUut1.Fill;
   TraceOut_SensorFault[15] := BenchUut1.SensorFault;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 16 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
