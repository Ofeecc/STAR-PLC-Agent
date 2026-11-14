PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchLastTime : TIME := T#0ms;
 BenchClockReady : BOOL := FALSE;
 BenchCurrentTime : TIME := T#0ms;
 TraceDt : ARRAY[0..15] OF UDINT;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_TemperatureSensorInput : ARRAY[0..15] OF REAL;
 TraceIn_SetTemperature : ARRAY[0..15] OF REAL;
 TraceOut_CurrentTemperature : ARRAY[0..15] OF REAL;
 TraceOut_SetTempDisplay : ARRAY[0..15] OF REAL;
 TraceOut_HeaterStatus : ARRAY[0..15] OF BOOL;
 TraceOut_OverheatProtection : ARRAY[0..15] OF BOOL;
 TraceOut_HeaterOutput : ARRAY[0..15] OF BOOL;
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
   BenchUut0.SetTemperature := REAL#25.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[1] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#20.0;
   BenchUut0.SetTemperature := REAL#25.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[2] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#25.0;
   BenchUut0.SetTemperature := REAL#25.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[3] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#30.0;
   BenchUut0.SetTemperature := REAL#25.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[4] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#24.0;
   BenchUut0.SetTemperature := REAL#25.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[5] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#20.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[6] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#35.0;
   BenchUut0.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[6] := BenchUut0.TemperatureSensorInput;
   TraceIn_SetTemperature[6] := BenchUut0.SetTemperature;
   BenchUut0();
   TraceOut_CurrentTemperature[6] := BenchUut0.CurrentTemperature;
   TraceOut_SetTempDisplay[6] := BenchUut0.SetTempDisplay;
   TraceOut_HeaterStatus[6] := BenchUut0.HeaterStatus;
   TraceOut_OverheatProtection[6] := BenchUut0.OverheatProtection;
   TraceOut_HeaterOutput[6] := BenchUut0.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 7:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[7] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.TemperatureSensorInput := REAL#30.0;
   BenchUut0.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[7] := BenchUut0.TemperatureSensorInput;
   TraceIn_SetTemperature[7] := BenchUut0.SetTemperature;
   BenchUut0();
   TraceOut_CurrentTemperature[7] := BenchUut0.CurrentTemperature;
   TraceOut_SetTempDisplay[7] := BenchUut0.SetTempDisplay;
   TraceOut_HeaterStatus[7] := BenchUut0.HeaterStatus;
   TraceOut_OverheatProtection[7] := BenchUut0.OverheatProtection;
   TraceOut_HeaterOutput[7] := BenchUut0.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 8:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[8] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#20.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(5000) THEN
   TraceDt[9] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#20.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[10] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#20.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[11] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#20.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[12] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#20.0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[13] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#20.0;
   BenchUut1.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[13] := BenchUut1.TemperatureSensorInput;
   TraceIn_SetTemperature[13] := BenchUut1.SetTemperature;
   BenchUut1();
   TraceOut_CurrentTemperature[13] := BenchUut1.CurrentTemperature;
   TraceOut_SetTempDisplay[13] := BenchUut1.SetTempDisplay;
   TraceOut_HeaterStatus[13] := BenchUut1.HeaterStatus;
   TraceOut_OverheatProtection[13] := BenchUut1.OverheatProtection;
   TraceOut_HeaterOutput[13] := BenchUut1.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 14:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[14] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#-5.0;
   BenchUut1.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[14] := BenchUut1.TemperatureSensorInput;
   TraceIn_SetTemperature[14] := BenchUut1.SetTemperature;
   BenchUut1();
   TraceOut_CurrentTemperature[14] := BenchUut1.CurrentTemperature;
   TraceOut_SetTempDisplay[14] := BenchUut1.SetTempDisplay;
   TraceOut_HeaterStatus[14] := BenchUut1.HeaterStatus;
   TraceOut_OverheatProtection[14] := BenchUut1.OverheatProtection;
   TraceOut_HeaterOutput[14] := BenchUut1.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 15:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1000) THEN
   TraceDt[15] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.TemperatureSensorInput := REAL#20.0;
   BenchUut1.SetTemperature := REAL#30.0;
   TraceIn_TemperatureSensorInput[15] := BenchUut1.TemperatureSensorInput;
   TraceIn_SetTemperature[15] := BenchUut1.SetTemperature;
   BenchUut1();
   TraceOut_CurrentTemperature[15] := BenchUut1.CurrentTemperature;
   TraceOut_SetTempDisplay[15] := BenchUut1.SetTempDisplay;
   TraceOut_HeaterStatus[15] := BenchUut1.HeaterStatus;
   TraceOut_OverheatProtection[15] := BenchUut1.OverheatProtection;
   TraceOut_HeaterOutput[15] := BenchUut1.HeaterOutput;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 16 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
