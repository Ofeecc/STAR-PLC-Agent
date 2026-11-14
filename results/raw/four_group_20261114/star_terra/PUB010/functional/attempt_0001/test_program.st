PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchLastTime : TIME := T#0ms;
 BenchClockReady : BOOL := FALSE;
 BenchCurrentTime : TIME := T#0ms;
 TraceDt : ARRAY[0..53] OF UDINT;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 BenchUut2 : FB_Task;
 BenchUut3 : FB_Task;
 BenchUut4 : FB_Task;
 BenchUut5 : FB_Task;
 BenchUut6 : FB_Task;
 BenchUut7 : FB_Task;
 TraceIn_TemperatureSensorInput : ARRAY[0..53] OF REAL;
 TraceIn_SetTemperature : ARRAY[0..53] OF REAL;
 TraceOut_CurrentTemperature : ARRAY[0..53] OF REAL;
 TraceOut_SetTempDisplay : ARRAY[0..53] OF REAL;
 TraceOut_HeaterStatus : ARRAY[0..53] OF BOOL;
 TraceOut_OverheatProtection : ARRAY[0..53] OF BOOL;
 TraceOut_HeaterOutput : ARRAY[0..53] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 BenchCurrentTime := TIME();
 IF NOT BenchClockReady THEN
  BenchLastTime := BenchCurrentTime;
  BenchClockReady := TRUE;
 ELSE
 CASE BenchStep OF
 0:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[0] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#20.0;
   BenchUut0.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[0] := BenchUut0.TemperatureSensorInput;
   TraceIn_SetTemperature[0] := BenchUut0.SetTemperature;
   BenchUut0();
   TraceOut_CurrentTemperature[0] := BenchUut0.CurrentTemperature;
   TraceOut_SetTempDisplay[0] := BenchUut0.SetTempDisplay;
   TraceOut_HeaterStatus[0] := BenchUut0.HeaterStatus;
   TraceOut_OverheatProtection[0] := BenchUut0.OverheatProtection;
   TraceOut_HeaterOutput[0] := BenchUut0.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 1:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[1] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#20.0;
   BenchUut0.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[1] := BenchUut0.TemperatureSensorInput;
   TraceIn_SetTemperature[1] := BenchUut0.SetTemperature;
   BenchUut0();
   TraceOut_CurrentTemperature[1] := BenchUut0.CurrentTemperature;
   TraceOut_SetTempDisplay[1] := BenchUut0.SetTempDisplay;
   TraceOut_HeaterStatus[1] := BenchUut0.HeaterStatus;
   TraceOut_OverheatProtection[1] := BenchUut0.OverheatProtection;
   TraceOut_HeaterOutput[1] := BenchUut0.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 2:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[2] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#20.0;
   BenchUut0.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[2] := BenchUut0.TemperatureSensorInput;
   TraceIn_SetTemperature[2] := BenchUut0.SetTemperature;
   BenchUut0();
   TraceOut_CurrentTemperature[2] := BenchUut0.CurrentTemperature;
   TraceOut_SetTempDisplay[2] := BenchUut0.SetTempDisplay;
   TraceOut_HeaterStatus[2] := BenchUut0.HeaterStatus;
   TraceOut_OverheatProtection[2] := BenchUut0.OverheatProtection;
   TraceOut_HeaterOutput[2] := BenchUut0.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 3:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2999) THEN
   TraceDt[3] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#20.0;
   BenchUut0.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[3] := BenchUut0.TemperatureSensorInput;
   TraceIn_SetTemperature[3] := BenchUut0.SetTemperature;
   BenchUut0();
   TraceOut_CurrentTemperature[3] := BenchUut0.CurrentTemperature;
   TraceOut_SetTempDisplay[3] := BenchUut0.SetTempDisplay;
   TraceOut_HeaterStatus[3] := BenchUut0.HeaterStatus;
   TraceOut_OverheatProtection[3] := BenchUut0.OverheatProtection;
   TraceOut_HeaterOutput[3] := BenchUut0.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 4:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[4] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#20.0;
   BenchUut0.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[4] := BenchUut0.TemperatureSensorInput;
   TraceIn_SetTemperature[4] := BenchUut0.SetTemperature;
   BenchUut0();
   TraceOut_CurrentTemperature[4] := BenchUut0.CurrentTemperature;
   TraceOut_SetTempDisplay[4] := BenchUut0.SetTempDisplay;
   TraceOut_HeaterStatus[4] := BenchUut0.HeaterStatus;
   TraceOut_OverheatProtection[4] := BenchUut0.OverheatProtection;
   TraceOut_HeaterOutput[4] := BenchUut0.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 5:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[5] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#31.0;
   BenchUut0.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[5] := BenchUut0.TemperatureSensorInput;
   TraceIn_SetTemperature[5] := BenchUut0.SetTemperature;
   BenchUut0();
   TraceOut_CurrentTemperature[5] := BenchUut0.CurrentTemperature;
   TraceOut_SetTempDisplay[5] := BenchUut0.SetTempDisplay;
   TraceOut_HeaterStatus[5] := BenchUut0.HeaterStatus;
   TraceOut_OverheatProtection[5] := BenchUut0.OverheatProtection;
   TraceOut_HeaterOutput[5] := BenchUut0.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 6:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[6] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#30.0;
   BenchUut1.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[6] := BenchUut1.TemperatureSensorInput;
   TraceIn_SetTemperature[6] := BenchUut1.SetTemperature;
   BenchUut1();
   TraceOut_CurrentTemperature[6] := BenchUut1.CurrentTemperature;
   TraceOut_SetTempDisplay[6] := BenchUut1.SetTempDisplay;
   TraceOut_HeaterStatus[6] := BenchUut1.HeaterStatus;
   TraceOut_OverheatProtection[6] := BenchUut1.OverheatProtection;
   TraceOut_HeaterOutput[6] := BenchUut1.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 7:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[7] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#0.0;
   BenchUut1.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[7] := BenchUut1.TemperatureSensorInput;
   TraceIn_SetTemperature[7] := BenchUut1.SetTemperature;
   BenchUut1();
   TraceOut_CurrentTemperature[7] := BenchUut1.CurrentTemperature;
   TraceOut_SetTempDisplay[7] := BenchUut1.SetTempDisplay;
   TraceOut_HeaterStatus[7] := BenchUut1.HeaterStatus;
   TraceOut_OverheatProtection[7] := BenchUut1.OverheatProtection;
   TraceOut_HeaterOutput[7] := BenchUut1.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 8:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[8] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#30.0;
   BenchUut1.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[8] := BenchUut1.TemperatureSensorInput;
   TraceIn_SetTemperature[8] := BenchUut1.SetTemperature;
   BenchUut1();
   TraceOut_CurrentTemperature[8] := BenchUut1.CurrentTemperature;
   TraceOut_SetTempDisplay[8] := BenchUut1.SetTempDisplay;
   TraceOut_HeaterStatus[8] := BenchUut1.HeaterStatus;
   TraceOut_OverheatProtection[8] := BenchUut1.OverheatProtection;
   TraceOut_HeaterOutput[8] := BenchUut1.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 9:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[9] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#-0.1;
   BenchUut1.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[9] := BenchUut1.TemperatureSensorInput;
   TraceIn_SetTemperature[9] := BenchUut1.SetTemperature;
   BenchUut1();
   TraceOut_CurrentTemperature[9] := BenchUut1.CurrentTemperature;
   TraceOut_SetTempDisplay[9] := BenchUut1.SetTempDisplay;
   TraceOut_HeaterStatus[9] := BenchUut1.HeaterStatus;
   TraceOut_OverheatProtection[9] := BenchUut1.OverheatProtection;
   TraceOut_HeaterOutput[9] := BenchUut1.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 10:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[10] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#100.0;
   BenchUut1.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[10] := BenchUut1.TemperatureSensorInput;
   TraceIn_SetTemperature[10] := BenchUut1.SetTemperature;
   BenchUut1();
   TraceOut_CurrentTemperature[10] := BenchUut1.CurrentTemperature;
   TraceOut_SetTempDisplay[10] := BenchUut1.SetTempDisplay;
   TraceOut_HeaterStatus[10] := BenchUut1.HeaterStatus;
   TraceOut_OverheatProtection[10] := BenchUut1.OverheatProtection;
   TraceOut_HeaterOutput[10] := BenchUut1.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 11:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[11] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#100.1;
   BenchUut1.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[11] := BenchUut1.TemperatureSensorInput;
   TraceIn_SetTemperature[11] := BenchUut1.SetTemperature;
   BenchUut1();
   TraceOut_CurrentTemperature[11] := BenchUut1.CurrentTemperature;
   TraceOut_SetTempDisplay[11] := BenchUut1.SetTempDisplay;
   TraceOut_HeaterStatus[11] := BenchUut1.HeaterStatus;
   TraceOut_OverheatProtection[11] := BenchUut1.OverheatProtection;
   TraceOut_HeaterOutput[11] := BenchUut1.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 12:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[12] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#30.0;
   BenchUut1.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[12] := BenchUut1.TemperatureSensorInput;
   TraceIn_SetTemperature[12] := BenchUut1.SetTemperature;
   BenchUut1();
   TraceOut_CurrentTemperature[12] := BenchUut1.CurrentTemperature;
   TraceOut_SetTempDisplay[12] := BenchUut1.SetTempDisplay;
   TraceOut_HeaterStatus[12] := BenchUut1.HeaterStatus;
   TraceOut_OverheatProtection[12] := BenchUut1.OverheatProtection;
   TraceOut_HeaterOutput[12] := BenchUut1.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 13:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[13] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.TemperatureSensorInput := REAL#20.0;
   BenchUut2.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[13] := BenchUut2.TemperatureSensorInput;
   TraceIn_SetTemperature[13] := BenchUut2.SetTemperature;
   BenchUut2();
   TraceOut_CurrentTemperature[13] := BenchUut2.CurrentTemperature;
   TraceOut_SetTempDisplay[13] := BenchUut2.SetTempDisplay;
   TraceOut_HeaterStatus[13] := BenchUut2.HeaterStatus;
   TraceOut_OverheatProtection[13] := BenchUut2.OverheatProtection;
   TraceOut_HeaterOutput[13] := BenchUut2.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 14:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[14] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.TemperatureSensorInput := REAL#20.0;
   BenchUut2.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[14] := BenchUut2.TemperatureSensorInput;
   TraceIn_SetTemperature[14] := BenchUut2.SetTemperature;
   BenchUut2();
   TraceOut_CurrentTemperature[14] := BenchUut2.CurrentTemperature;
   TraceOut_SetTempDisplay[14] := BenchUut2.SetTempDisplay;
   TraceOut_HeaterStatus[14] := BenchUut2.HeaterStatus;
   TraceOut_OverheatProtection[14] := BenchUut2.OverheatProtection;
   TraceOut_HeaterOutput[14] := BenchUut2.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 15:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[15] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.TemperatureSensorInput := REAL#-1.0;
   BenchUut2.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[15] := BenchUut2.TemperatureSensorInput;
   TraceIn_SetTemperature[15] := BenchUut2.SetTemperature;
   BenchUut2();
   TraceOut_CurrentTemperature[15] := BenchUut2.CurrentTemperature;
   TraceOut_SetTempDisplay[15] := BenchUut2.SetTempDisplay;
   TraceOut_HeaterStatus[15] := BenchUut2.HeaterStatus;
   TraceOut_OverheatProtection[15] := BenchUut2.OverheatProtection;
   TraceOut_HeaterOutput[15] := BenchUut2.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 16:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[16] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.TemperatureSensorInput := REAL#20.0;
   BenchUut2.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[16] := BenchUut2.TemperatureSensorInput;
   TraceIn_SetTemperature[16] := BenchUut2.SetTemperature;
   BenchUut2();
   TraceOut_CurrentTemperature[16] := BenchUut2.CurrentTemperature;
   TraceOut_SetTempDisplay[16] := BenchUut2.SetTempDisplay;
   TraceOut_HeaterStatus[16] := BenchUut2.HeaterStatus;
   TraceOut_OverheatProtection[16] := BenchUut2.OverheatProtection;
   TraceOut_HeaterOutput[16] := BenchUut2.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 17:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[17] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.TemperatureSensorInput := REAL#20.0;
   BenchUut2.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[17] := BenchUut2.TemperatureSensorInput;
   TraceIn_SetTemperature[17] := BenchUut2.SetTemperature;
   BenchUut2();
   TraceOut_CurrentTemperature[17] := BenchUut2.CurrentTemperature;
   TraceOut_SetTempDisplay[17] := BenchUut2.SetTempDisplay;
   TraceOut_HeaterStatus[17] := BenchUut2.HeaterStatus;
   TraceOut_OverheatProtection[17] := BenchUut2.OverheatProtection;
   TraceOut_HeaterOutput[17] := BenchUut2.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 18:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[18] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.TemperatureSensorInput := REAL#40.0;
   BenchUut3.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[18] := BenchUut3.TemperatureSensorInput;
   TraceIn_SetTemperature[18] := BenchUut3.SetTemperature;
   BenchUut3();
   TraceOut_CurrentTemperature[18] := BenchUut3.CurrentTemperature;
   TraceOut_SetTempDisplay[18] := BenchUut3.SetTempDisplay;
   TraceOut_HeaterStatus[18] := BenchUut3.HeaterStatus;
   TraceOut_OverheatProtection[18] := BenchUut3.OverheatProtection;
   TraceOut_HeaterOutput[18] := BenchUut3.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 19:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[19] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.TemperatureSensorInput := REAL#40.0;
   BenchUut3.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[19] := BenchUut3.TemperatureSensorInput;
   TraceIn_SetTemperature[19] := BenchUut3.SetTemperature;
   BenchUut3();
   TraceOut_CurrentTemperature[19] := BenchUut3.CurrentTemperature;
   TraceOut_SetTempDisplay[19] := BenchUut3.SetTempDisplay;
   TraceOut_HeaterStatus[19] := BenchUut3.HeaterStatus;
   TraceOut_OverheatProtection[19] := BenchUut3.OverheatProtection;
   TraceOut_HeaterOutput[19] := BenchUut3.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 20:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[20] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.TemperatureSensorInput := REAL#40.0;
   BenchUut3.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[20] := BenchUut3.TemperatureSensorInput;
   TraceIn_SetTemperature[20] := BenchUut3.SetTemperature;
   BenchUut3();
   TraceOut_CurrentTemperature[20] := BenchUut3.CurrentTemperature;
   TraceOut_SetTempDisplay[20] := BenchUut3.SetTempDisplay;
   TraceOut_HeaterStatus[20] := BenchUut3.HeaterStatus;
   TraceOut_OverheatProtection[20] := BenchUut3.OverheatProtection;
   TraceOut_HeaterOutput[20] := BenchUut3.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 21:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[21] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#50.0;
   BenchUut4.SetTemperature := REAL#80.0;
   TraceIn_TemperatureSensorInput[21] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[21] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[21] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[21] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[21] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[21] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[21] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 22:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[22] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#50.0;
   BenchUut4.SetTemperature := REAL#80.0;
   TraceIn_TemperatureSensorInput[22] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[22] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[22] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[22] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[22] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[22] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[22] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 23:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[23] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#85.0;
   BenchUut4.SetTemperature := REAL#80.0;
   TraceIn_TemperatureSensorInput[23] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[23] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[23] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[23] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[23] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[23] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[23] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 24:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[24] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#80.0;
   BenchUut4.SetTemperature := REAL#80.0;
   TraceIn_TemperatureSensorInput[24] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[24] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[24] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[24] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[24] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[24] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[24] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 25:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[25] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#50.0;
   BenchUut4.SetTemperature := REAL#80.0;
   TraceIn_TemperatureSensorInput[25] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[25] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[25] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[25] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[25] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[25] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[25] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 26:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[26] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#100.0;
   BenchUut4.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[26] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[26] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[26] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[26] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[26] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[26] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[26] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 27:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[27] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#100.1;
   BenchUut4.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[27] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[27] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[27] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[27] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[27] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[27] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[27] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 28:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[28] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#100.0;
   BenchUut4.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[28] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[28] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[28] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[28] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[28] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[28] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[28] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 29:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[29] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#100.0;
   BenchUut4.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[29] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[29] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[29] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[29] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[29] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[29] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[29] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 30:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(3000) THEN
   TraceDt[30] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#100.1;
   BenchUut4.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[30] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[30] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[30] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[30] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[30] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[30] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[30] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 31:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[31] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.TemperatureSensorInput := REAL#100.0;
   BenchUut4.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[31] := BenchUut4.TemperatureSensorInput;
   TraceIn_SetTemperature[31] := BenchUut4.SetTemperature;
   BenchUut4();
   TraceOut_CurrentTemperature[31] := BenchUut4.CurrentTemperature;
   TraceOut_SetTempDisplay[31] := BenchUut4.SetTempDisplay;
   TraceOut_HeaterStatus[31] := BenchUut4.HeaterStatus;
   TraceOut_OverheatProtection[31] := BenchUut4.OverheatProtection;
   TraceOut_HeaterOutput[31] := BenchUut4.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 32:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[32] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.TemperatureSensorInput := REAL#100.0;
   BenchUut5.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[32] := BenchUut5.TemperatureSensorInput;
   TraceIn_SetTemperature[32] := BenchUut5.SetTemperature;
   BenchUut5();
   TraceOut_CurrentTemperature[32] := BenchUut5.CurrentTemperature;
   TraceOut_SetTempDisplay[32] := BenchUut5.SetTempDisplay;
   TraceOut_HeaterStatus[32] := BenchUut5.HeaterStatus;
   TraceOut_OverheatProtection[32] := BenchUut5.OverheatProtection;
   TraceOut_HeaterOutput[32] := BenchUut5.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 33:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[33] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.TemperatureSensorInput := REAL#100.1;
   BenchUut5.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[33] := BenchUut5.TemperatureSensorInput;
   TraceIn_SetTemperature[33] := BenchUut5.SetTemperature;
   BenchUut5();
   TraceOut_CurrentTemperature[33] := BenchUut5.CurrentTemperature;
   TraceOut_SetTempDisplay[33] := BenchUut5.SetTempDisplay;
   TraceOut_HeaterStatus[33] := BenchUut5.HeaterStatus;
   TraceOut_OverheatProtection[33] := BenchUut5.OverheatProtection;
   TraceOut_HeaterOutput[33] := BenchUut5.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 34:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[34] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.TemperatureSensorInput := REAL#99.0;
   BenchUut5.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[34] := BenchUut5.TemperatureSensorInput;
   TraceIn_SetTemperature[34] := BenchUut5.SetTemperature;
   BenchUut5();
   TraceOut_CurrentTemperature[34] := BenchUut5.CurrentTemperature;
   TraceOut_SetTempDisplay[34] := BenchUut5.SetTempDisplay;
   TraceOut_HeaterStatus[34] := BenchUut5.HeaterStatus;
   TraceOut_OverheatProtection[34] := BenchUut5.OverheatProtection;
   TraceOut_HeaterOutput[34] := BenchUut5.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 35:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[35] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.TemperatureSensorInput := REAL#99.0;
   BenchUut5.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[35] := BenchUut5.TemperatureSensorInput;
   TraceIn_SetTemperature[35] := BenchUut5.SetTemperature;
   BenchUut5();
   TraceOut_CurrentTemperature[35] := BenchUut5.CurrentTemperature;
   TraceOut_SetTempDisplay[35] := BenchUut5.SetTempDisplay;
   TraceOut_HeaterStatus[35] := BenchUut5.HeaterStatus;
   TraceOut_OverheatProtection[35] := BenchUut5.OverheatProtection;
   TraceOut_HeaterOutput[35] := BenchUut5.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 36:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[36] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.TemperatureSensorInput := REAL#100.0;
   BenchUut5.SetTemperature := REAL#90.0;
   TraceIn_TemperatureSensorInput[36] := BenchUut5.TemperatureSensorInput;
   TraceIn_SetTemperature[36] := BenchUut5.SetTemperature;
   BenchUut5();
   TraceOut_CurrentTemperature[36] := BenchUut5.CurrentTemperature;
   TraceOut_SetTempDisplay[36] := BenchUut5.SetTempDisplay;
   TraceOut_HeaterStatus[36] := BenchUut5.HeaterStatus;
   TraceOut_OverheatProtection[36] := BenchUut5.OverheatProtection;
   TraceOut_HeaterOutput[36] := BenchUut5.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 37:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[37] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.TemperatureSensorInput := REAL#100.0;
   BenchUut5.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[37] := BenchUut5.TemperatureSensorInput;
   TraceIn_SetTemperature[37] := BenchUut5.SetTemperature;
   BenchUut5();
   TraceOut_CurrentTemperature[37] := BenchUut5.CurrentTemperature;
   TraceOut_SetTempDisplay[37] := BenchUut5.SetTempDisplay;
   TraceOut_HeaterStatus[37] := BenchUut5.HeaterStatus;
   TraceOut_OverheatProtection[37] := BenchUut5.OverheatProtection;
   TraceOut_HeaterOutput[37] := BenchUut5.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 38:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[38] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.TemperatureSensorInput := REAL#100.0;
   BenchUut5.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[38] := BenchUut5.TemperatureSensorInput;
   TraceIn_SetTemperature[38] := BenchUut5.SetTemperature;
   BenchUut5();
   TraceOut_CurrentTemperature[38] := BenchUut5.CurrentTemperature;
   TraceOut_SetTempDisplay[38] := BenchUut5.SetTempDisplay;
   TraceOut_HeaterStatus[38] := BenchUut5.HeaterStatus;
   TraceOut_OverheatProtection[38] := BenchUut5.OverheatProtection;
   TraceOut_HeaterOutput[38] := BenchUut5.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 39:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(3100) THEN
   TraceDt[39] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.TemperatureSensorInput := REAL#100.0;
   BenchUut5.SetTemperature := REAL#101.0;
   TraceIn_TemperatureSensorInput[39] := BenchUut5.TemperatureSensorInput;
   TraceIn_SetTemperature[39] := BenchUut5.SetTemperature;
   BenchUut5();
   TraceOut_CurrentTemperature[39] := BenchUut5.CurrentTemperature;
   TraceOut_SetTempDisplay[39] := BenchUut5.SetTempDisplay;
   TraceOut_HeaterStatus[39] := BenchUut5.HeaterStatus;
   TraceOut_OverheatProtection[39] := BenchUut5.OverheatProtection;
   TraceOut_HeaterOutput[39] := BenchUut5.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 40:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[40] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.TemperatureSensorInput := REAL#20.0;
   BenchUut6.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[40] := BenchUut6.TemperatureSensorInput;
   TraceIn_SetTemperature[40] := BenchUut6.SetTemperature;
   BenchUut6();
   TraceOut_CurrentTemperature[40] := BenchUut6.CurrentTemperature;
   TraceOut_SetTempDisplay[40] := BenchUut6.SetTempDisplay;
   TraceOut_HeaterStatus[40] := BenchUut6.HeaterStatus;
   TraceOut_OverheatProtection[40] := BenchUut6.OverheatProtection;
   TraceOut_HeaterOutput[40] := BenchUut6.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 41:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4500) THEN
   TraceDt[41] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.TemperatureSensorInput := REAL#20.0;
   BenchUut6.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[41] := BenchUut6.TemperatureSensorInput;
   TraceIn_SetTemperature[41] := BenchUut6.SetTemperature;
   BenchUut6();
   TraceOut_CurrentTemperature[41] := BenchUut6.CurrentTemperature;
   TraceOut_SetTempDisplay[41] := BenchUut6.SetTempDisplay;
   TraceOut_HeaterStatus[41] := BenchUut6.HeaterStatus;
   TraceOut_OverheatProtection[41] := BenchUut6.OverheatProtection;
   TraceOut_HeaterOutput[41] := BenchUut6.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 42:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(499) THEN
   TraceDt[42] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.TemperatureSensorInput := REAL#31.0;
   BenchUut6.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[42] := BenchUut6.TemperatureSensorInput;
   TraceIn_SetTemperature[42] := BenchUut6.SetTemperature;
   BenchUut6();
   TraceOut_CurrentTemperature[42] := BenchUut6.CurrentTemperature;
   TraceOut_SetTempDisplay[42] := BenchUut6.SetTempDisplay;
   TraceOut_HeaterStatus[42] := BenchUut6.HeaterStatus;
   TraceOut_OverheatProtection[42] := BenchUut6.OverheatProtection;
   TraceOut_HeaterOutput[42] := BenchUut6.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 43:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(101) THEN
   TraceDt[43] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.TemperatureSensorInput := REAL#20.0;
   BenchUut6.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[43] := BenchUut6.TemperatureSensorInput;
   TraceIn_SetTemperature[43] := BenchUut6.SetTemperature;
   BenchUut6();
   TraceOut_CurrentTemperature[43] := BenchUut6.CurrentTemperature;
   TraceOut_SetTempDisplay[43] := BenchUut6.SetTempDisplay;
   TraceOut_HeaterStatus[43] := BenchUut6.HeaterStatus;
   TraceOut_OverheatProtection[43] := BenchUut6.OverheatProtection;
   TraceOut_HeaterOutput[43] := BenchUut6.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 44:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(4999) THEN
   TraceDt[44] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.TemperatureSensorInput := REAL#20.0;
   BenchUut6.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[44] := BenchUut6.TemperatureSensorInput;
   TraceIn_SetTemperature[44] := BenchUut6.SetTemperature;
   BenchUut6();
   TraceOut_CurrentTemperature[44] := BenchUut6.CurrentTemperature;
   TraceOut_SetTempDisplay[44] := BenchUut6.SetTempDisplay;
   TraceOut_HeaterStatus[44] := BenchUut6.HeaterStatus;
   TraceOut_OverheatProtection[44] := BenchUut6.OverheatProtection;
   TraceOut_HeaterOutput[44] := BenchUut6.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 45:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[45] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.TemperatureSensorInput := REAL#20.0;
   BenchUut6.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[45] := BenchUut6.TemperatureSensorInput;
   TraceIn_SetTemperature[45] := BenchUut6.SetTemperature;
   BenchUut6();
   TraceOut_CurrentTemperature[45] := BenchUut6.CurrentTemperature;
   TraceOut_SetTempDisplay[45] := BenchUut6.SetTempDisplay;
   TraceOut_HeaterStatus[45] := BenchUut6.HeaterStatus;
   TraceOut_OverheatProtection[45] := BenchUut6.OverheatProtection;
   TraceOut_HeaterOutput[45] := BenchUut6.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 46:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2999) THEN
   TraceDt[46] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.TemperatureSensorInput := REAL#20.0;
   BenchUut6.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[46] := BenchUut6.TemperatureSensorInput;
   TraceIn_SetTemperature[46] := BenchUut6.SetTemperature;
   BenchUut6();
   TraceOut_CurrentTemperature[46] := BenchUut6.CurrentTemperature;
   TraceOut_SetTempDisplay[46] := BenchUut6.SetTempDisplay;
   TraceOut_HeaterStatus[46] := BenchUut6.HeaterStatus;
   TraceOut_OverheatProtection[46] := BenchUut6.OverheatProtection;
   TraceOut_HeaterOutput[46] := BenchUut6.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 47:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[47] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.TemperatureSensorInput := REAL#20.0;
   BenchUut6.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[47] := BenchUut6.TemperatureSensorInput;
   TraceIn_SetTemperature[47] := BenchUut6.SetTemperature;
   BenchUut6();
   TraceOut_CurrentTemperature[47] := BenchUut6.CurrentTemperature;
   TraceOut_SetTempDisplay[47] := BenchUut6.SetTempDisplay;
   TraceOut_HeaterStatus[47] := BenchUut6.HeaterStatus;
   TraceOut_OverheatProtection[47] := BenchUut6.OverheatProtection;
   TraceOut_HeaterOutput[47] := BenchUut6.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 48:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[48] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut7.TemperatureSensorInput := REAL#25.0;
   BenchUut7.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[48] := BenchUut7.TemperatureSensorInput;
   TraceIn_SetTemperature[48] := BenchUut7.SetTemperature;
   BenchUut7();
   TraceOut_CurrentTemperature[48] := BenchUut7.CurrentTemperature;
   TraceOut_SetTempDisplay[48] := BenchUut7.SetTempDisplay;
   TraceOut_HeaterStatus[48] := BenchUut7.HeaterStatus;
   TraceOut_OverheatProtection[48] := BenchUut7.OverheatProtection;
   TraceOut_HeaterOutput[48] := BenchUut7.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 49:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[49] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut7.TemperatureSensorInput := REAL#30.0;
   BenchUut7.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[49] := BenchUut7.TemperatureSensorInput;
   TraceIn_SetTemperature[49] := BenchUut7.SetTemperature;
   BenchUut7();
   TraceOut_CurrentTemperature[49] := BenchUut7.CurrentTemperature;
   TraceOut_SetTempDisplay[49] := BenchUut7.SetTempDisplay;
   TraceOut_HeaterStatus[49] := BenchUut7.HeaterStatus;
   TraceOut_OverheatProtection[49] := BenchUut7.OverheatProtection;
   TraceOut_HeaterOutput[49] := BenchUut7.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 50:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[50] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut7.TemperatureSensorInput := REAL#-5.0;
   BenchUut7.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[50] := BenchUut7.TemperatureSensorInput;
   TraceIn_SetTemperature[50] := BenchUut7.SetTemperature;
   BenchUut7();
   TraceOut_CurrentTemperature[50] := BenchUut7.CurrentTemperature;
   TraceOut_SetTempDisplay[50] := BenchUut7.SetTempDisplay;
   TraceOut_HeaterStatus[50] := BenchUut7.HeaterStatus;
   TraceOut_OverheatProtection[50] := BenchUut7.OverheatProtection;
   TraceOut_HeaterOutput[50] := BenchUut7.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 51:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(2000) THEN
   TraceDt[51] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut7.TemperatureSensorInput := REAL#30.0;
   BenchUut7.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[51] := BenchUut7.TemperatureSensorInput;
   TraceIn_SetTemperature[51] := BenchUut7.SetTemperature;
   BenchUut7();
   TraceOut_CurrentTemperature[51] := BenchUut7.CurrentTemperature;
   TraceOut_SetTempDisplay[51] := BenchUut7.SetTempDisplay;
   TraceOut_HeaterStatus[51] := BenchUut7.HeaterStatus;
   TraceOut_OverheatProtection[51] := BenchUut7.OverheatProtection;
   TraceOut_HeaterOutput[51] := BenchUut7.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 52:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[52] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut7.TemperatureSensorInput := REAL#30.5;
   BenchUut7.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[52] := BenchUut7.TemperatureSensorInput;
   TraceIn_SetTemperature[52] := BenchUut7.SetTemperature;
   BenchUut7();
   TraceOut_CurrentTemperature[52] := BenchUut7.CurrentTemperature;
   TraceOut_SetTempDisplay[52] := BenchUut7.SetTempDisplay;
   TraceOut_HeaterStatus[52] := BenchUut7.HeaterStatus;
   TraceOut_OverheatProtection[52] := BenchUut7.OverheatProtection;
   TraceOut_HeaterOutput[52] := BenchUut7.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 53:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[53] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut7.TemperatureSensorInput := REAL#30.0;
   BenchUut7.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[53] := BenchUut7.TemperatureSensorInput;
   TraceIn_SetTemperature[53] := BenchUut7.SetTemperature;
   BenchUut7();
   TraceOut_CurrentTemperature[53] := BenchUut7.CurrentTemperature;
   TraceOut_SetTempDisplay[53] := BenchUut7.SetTempDisplay;
   TraceOut_HeaterStatus[53] := BenchUut7.HeaterStatus;
   TraceOut_OverheatProtection[53] := BenchUut7.OverheatProtection;
   TraceOut_HeaterOutput[53] := BenchUut7.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 54 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
