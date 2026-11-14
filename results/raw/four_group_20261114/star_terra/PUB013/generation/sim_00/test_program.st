PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchLastTime : TIME := T#0ms;
 BenchClockReady : BOOL := FALSE;
 BenchCurrentTime : TIME := T#0ms;
 TraceDt : ARRAY[0..12] OF UDINT;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_OCCUPANCY_DETECTED : ARRAY[0..12] OF BOOL;
 TraceIn_ENERGY_SAVING_MODE : ARRAY[0..12] OF BOOL;
 TraceIn_HVAC_MODE_SELECTOR : ARRAY[0..12] OF INT;
 TraceOut_SUPPLY_FAN_RUN : ARRAY[0..12] OF BOOL;
 TraceOut_TEMP_SETPOINT_ADJUST : ARRAY[0..12] OF INT;
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
   BenchUut0.OCCUPANCY_DETECTED := TRUE;
   BenchUut0.ENERGY_SAVING_MODE := FALSE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[0] := BenchUut0.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[0] := BenchUut0.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[0] := BenchUut0.HVAC_MODE_SELECTOR;
   BenchUut0();
   TraceOut_SUPPLY_FAN_RUN[0] := BenchUut0.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[0] := BenchUut0.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 1:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(29999) THEN
   TraceDt[1] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.OCCUPANCY_DETECTED := TRUE;
   BenchUut0.ENERGY_SAVING_MODE := TRUE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[1] := BenchUut0.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[1] := BenchUut0.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[1] := BenchUut0.HVAC_MODE_SELECTOR;
   BenchUut0();
   TraceOut_SUPPLY_FAN_RUN[1] := BenchUut0.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[1] := BenchUut0.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 2:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[2] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.OCCUPANCY_DETECTED := TRUE;
   BenchUut0.ENERGY_SAVING_MODE := TRUE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[2] := BenchUut0.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[2] := BenchUut0.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[2] := BenchUut0.HVAC_MODE_SELECTOR;
   BenchUut0();
   TraceOut_SUPPLY_FAN_RUN[2] := BenchUut0.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[2] := BenchUut0.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 3:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[3] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.OCCUPANCY_DETECTED := TRUE;
   BenchUut0.ENERGY_SAVING_MODE := TRUE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[3] := BenchUut0.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[3] := BenchUut0.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[3] := BenchUut0.HVAC_MODE_SELECTOR;
   BenchUut0();
   TraceOut_SUPPLY_FAN_RUN[3] := BenchUut0.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[3] := BenchUut0.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 4:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[4] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.OCCUPANCY_DETECTED := TRUE;
   BenchUut0.ENERGY_SAVING_MODE := TRUE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[4] := BenchUut0.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[4] := BenchUut0.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[4] := BenchUut0.HVAC_MODE_SELECTOR;
   BenchUut0();
   TraceOut_SUPPLY_FAN_RUN[4] := BenchUut0.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[4] := BenchUut0.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 5:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[5] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := FALSE;
   BenchUut1.ENERGY_SAVING_MODE := TRUE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[5] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[5] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[5] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[5] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[5] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 6:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[6] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := FALSE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[6] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[6] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[6] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[6] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[6] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 7:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[7] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := FALSE;
   BenchUut1.ENERGY_SAVING_MODE := TRUE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[7] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[7] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[7] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[7] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[7] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 8:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[8] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := FALSE;
   BenchUut1.ENERGY_SAVING_MODE := TRUE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[8] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[8] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[8] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[8] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[8] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 9:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[9] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := FALSE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[9] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[9] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[9] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[9] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[9] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 10:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[10] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := FALSE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[10] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[10] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[10] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[10] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[10] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 11:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[11] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := FALSE;
   BenchUut1.ENERGY_SAVING_MODE := TRUE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[11] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[11] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[11] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[11] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[11] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 12:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[12] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := TRUE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[12] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[12] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[12] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[12] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[12] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 13 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
