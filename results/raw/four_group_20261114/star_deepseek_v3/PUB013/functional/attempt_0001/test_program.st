PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchLastTime : TIME := T#0ms;
 BenchClockReady : BOOL := FALSE;
 BenchCurrentTime : TIME := T#0ms;
 TraceDt : ARRAY[0..79] OF UDINT;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 BenchUut2 : FB_Task;
 BenchUut3 : FB_Task;
 BenchUut4 : FB_Task;
 BenchUut5 : FB_Task;
 BenchUut6 : FB_Task;
 BenchUut7 : FB_Task;
 BenchUut8 : FB_Task;
 BenchUut9 : FB_Task;
 BenchUut10 : FB_Task;
 BenchUut11 : FB_Task;
 TraceIn_OCCUPANCY_DETECTED : ARRAY[0..79] OF BOOL;
 TraceIn_ENERGY_SAVING_MODE : ARRAY[0..79] OF BOOL;
 TraceIn_HVAC_MODE_SELECTOR : ARRAY[0..79] OF INT;
 TraceOut_SUPPLY_FAN_RUN : ARRAY[0..79] OF BOOL;
 TraceOut_TEMP_SETPOINT_ADJUST : ARRAY[0..79] OF INT;
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
   BenchUut0.OCCUPANCY_DETECTED := FALSE;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[1] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.OCCUPANCY_DETECTED := FALSE;
   BenchUut0.ENERGY_SAVING_MODE := TRUE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[2] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.OCCUPANCY_DETECTED := FALSE;
   BenchUut0.ENERGY_SAVING_MODE := FALSE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#1;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[3] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.OCCUPANCY_DETECTED := FALSE;
   BenchUut0.ENERGY_SAVING_MODE := TRUE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#1;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[4] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.OCCUPANCY_DETECTED := FALSE;
   BenchUut0.ENERGY_SAVING_MODE := FALSE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#2;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[5] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.OCCUPANCY_DETECTED := TRUE;
   BenchUut0.ENERGY_SAVING_MODE := FALSE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[5] := BenchUut0.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[5] := BenchUut0.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[5] := BenchUut0.HVAC_MODE_SELECTOR;
   BenchUut0();
   TraceOut_SUPPLY_FAN_RUN[5] := BenchUut0.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[5] := BenchUut0.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 6:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[6] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut0.OCCUPANCY_DETECTED := TRUE;
   BenchUut0.ENERGY_SAVING_MODE := FALSE;
   BenchUut0.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[6] := BenchUut0.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[6] := BenchUut0.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[6] := BenchUut0.HVAC_MODE_SELECTOR;
   BenchUut0();
   TraceOut_SUPPLY_FAN_RUN[6] := BenchUut0.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[6] := BenchUut0.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 7:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[7] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := TRUE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(29900) THEN
   TraceDt[8] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := TRUE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[9] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := TRUE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[10] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := FALSE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[11] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := TRUE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#0;
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
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(29900) THEN
   TraceDt[12] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := TRUE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[12] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[12] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[12] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[12] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[12] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 13:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[13] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := TRUE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[13] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[13] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[13] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[13] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[13] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 14:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[14] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut1.OCCUPANCY_DETECTED := TRUE;
   BenchUut1.ENERGY_SAVING_MODE := FALSE;
   BenchUut1.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[14] := BenchUut1.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[14] := BenchUut1.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[14] := BenchUut1.HVAC_MODE_SELECTOR;
   BenchUut1();
   TraceOut_SUPPLY_FAN_RUN[14] := BenchUut1.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[14] := BenchUut1.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 15:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[15] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.OCCUPANCY_DETECTED := TRUE;
   BenchUut2.ENERGY_SAVING_MODE := FALSE;
   BenchUut2.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[15] := BenchUut2.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[15] := BenchUut2.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[15] := BenchUut2.HVAC_MODE_SELECTOR;
   BenchUut2();
   TraceOut_SUPPLY_FAN_RUN[15] := BenchUut2.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[15] := BenchUut2.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 16:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(30000) THEN
   TraceDt[16] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.OCCUPANCY_DETECTED := TRUE;
   BenchUut2.ENERGY_SAVING_MODE := FALSE;
   BenchUut2.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[16] := BenchUut2.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[16] := BenchUut2.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[16] := BenchUut2.HVAC_MODE_SELECTOR;
   BenchUut2();
   TraceOut_SUPPLY_FAN_RUN[16] := BenchUut2.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[16] := BenchUut2.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 17:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(60000) THEN
   TraceDt[17] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.OCCUPANCY_DETECTED := TRUE;
   BenchUut2.ENERGY_SAVING_MODE := FALSE;
   BenchUut2.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[17] := BenchUut2.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[17] := BenchUut2.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[17] := BenchUut2.HVAC_MODE_SELECTOR;
   BenchUut2();
   TraceOut_SUPPLY_FAN_RUN[17] := BenchUut2.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[17] := BenchUut2.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 18:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(29999) THEN
   TraceDt[18] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.OCCUPANCY_DETECTED := TRUE;
   BenchUut2.ENERGY_SAVING_MODE := FALSE;
   BenchUut2.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[18] := BenchUut2.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[18] := BenchUut2.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[18] := BenchUut2.HVAC_MODE_SELECTOR;
   BenchUut2();
   TraceOut_SUPPLY_FAN_RUN[18] := BenchUut2.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[18] := BenchUut2.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 19:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[19] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut2.OCCUPANCY_DETECTED := TRUE;
   BenchUut2.ENERGY_SAVING_MODE := FALSE;
   BenchUut2.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[19] := BenchUut2.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[19] := BenchUut2.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[19] := BenchUut2.HVAC_MODE_SELECTOR;
   BenchUut2();
   TraceOut_SUPPLY_FAN_RUN[19] := BenchUut2.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[19] := BenchUut2.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 20:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[20] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[20] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[20] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[20] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[20] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[20] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 21:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(10000) THEN
   TraceDt[21] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := TRUE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[21] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[21] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[21] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[21] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[21] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 22:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(19999) THEN
   TraceDt[22] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[22] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[22] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[22] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[22] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[22] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 23:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[23] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := TRUE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[23] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[23] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[23] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[23] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[23] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 24:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[24] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := FALSE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[24] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[24] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[24] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[24] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[24] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 25:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(500) THEN
   TraceDt[25] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[25] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[25] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[25] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[25] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[25] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 26:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(29999) THEN
   TraceDt[26] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[26] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[26] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[26] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[26] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[26] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 27:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(1) THEN
   TraceDt[27] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[27] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[27] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[27] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[27] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[27] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 28:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[28] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := FALSE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[28] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[28] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[28] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[28] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[28] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 29:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[29] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := FALSE;
   BenchUut3.ENERGY_SAVING_MODE := TRUE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[29] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[29] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[29] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[29] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[29] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 30:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[30] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[30] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[30] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[30] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[30] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[30] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 31:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[31] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := TRUE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[31] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[31] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[31] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[31] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[31] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 32:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[32] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := FALSE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[32] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[32] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[32] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[32] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[32] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 33:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[33] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := FALSE;
   BenchUut3.ENERGY_SAVING_MODE := TRUE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[33] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[33] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[33] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[33] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[33] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 34:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[34] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[34] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[34] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[34] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[34] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[34] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 35:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[35] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := TRUE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[35] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[35] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[35] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[35] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[35] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 36:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[36] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := FALSE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[36] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[36] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[36] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[36] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[36] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 37:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[37] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := FALSE;
   BenchUut3.ENERGY_SAVING_MODE := TRUE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[37] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[37] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[37] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[37] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[37] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 38:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[38] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[38] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[38] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[38] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[38] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[38] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 39:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[39] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := TRUE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[39] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[39] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[39] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[39] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[39] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 40:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[40] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := FALSE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[40] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[40] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[40] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[40] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[40] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 41:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[41] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := FALSE;
   BenchUut3.ENERGY_SAVING_MODE := TRUE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[41] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[41] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[41] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[41] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[41] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 42:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[42] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := FALSE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[42] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[42] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[42] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[42] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[42] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 43:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[43] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut3.OCCUPANCY_DETECTED := TRUE;
   BenchUut3.ENERGY_SAVING_MODE := TRUE;
   BenchUut3.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[43] := BenchUut3.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[43] := BenchUut3.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[43] := BenchUut3.HVAC_MODE_SELECTOR;
   BenchUut3();
   TraceOut_SUPPLY_FAN_RUN[43] := BenchUut3.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[43] := BenchUut3.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 44:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[44] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.OCCUPANCY_DETECTED := TRUE;
   BenchUut4.ENERGY_SAVING_MODE := FALSE;
   BenchUut4.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[44] := BenchUut4.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[44] := BenchUut4.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[44] := BenchUut4.HVAC_MODE_SELECTOR;
   BenchUut4();
   TraceOut_SUPPLY_FAN_RUN[44] := BenchUut4.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[44] := BenchUut4.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 45:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(30000) THEN
   TraceDt[45] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut4.OCCUPANCY_DETECTED := TRUE;
   BenchUut4.ENERGY_SAVING_MODE := FALSE;
   BenchUut4.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[45] := BenchUut4.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[45] := BenchUut4.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[45] := BenchUut4.HVAC_MODE_SELECTOR;
   BenchUut4();
   TraceOut_SUPPLY_FAN_RUN[45] := BenchUut4.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[45] := BenchUut4.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 46:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[46] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.OCCUPANCY_DETECTED := FALSE;
   BenchUut5.ENERGY_SAVING_MODE := FALSE;
   BenchUut5.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[46] := BenchUut5.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[46] := BenchUut5.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[46] := BenchUut5.HVAC_MODE_SELECTOR;
   BenchUut5();
   TraceOut_SUPPLY_FAN_RUN[46] := BenchUut5.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[46] := BenchUut5.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 47:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[47] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.OCCUPANCY_DETECTED := FALSE;
   BenchUut5.ENERGY_SAVING_MODE := TRUE;
   BenchUut5.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[47] := BenchUut5.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[47] := BenchUut5.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[47] := BenchUut5.HVAC_MODE_SELECTOR;
   BenchUut5();
   TraceOut_SUPPLY_FAN_RUN[47] := BenchUut5.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[47] := BenchUut5.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 48:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[48] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.OCCUPANCY_DETECTED := TRUE;
   BenchUut5.ENERGY_SAVING_MODE := FALSE;
   BenchUut5.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[48] := BenchUut5.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[48] := BenchUut5.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[48] := BenchUut5.HVAC_MODE_SELECTOR;
   BenchUut5();
   TraceOut_SUPPLY_FAN_RUN[48] := BenchUut5.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[48] := BenchUut5.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 49:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[49] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut5.OCCUPANCY_DETECTED := TRUE;
   BenchUut5.ENERGY_SAVING_MODE := TRUE;
   BenchUut5.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[49] := BenchUut5.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[49] := BenchUut5.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[49] := BenchUut5.HVAC_MODE_SELECTOR;
   BenchUut5();
   TraceOut_SUPPLY_FAN_RUN[49] := BenchUut5.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[49] := BenchUut5.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 50:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[50] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.OCCUPANCY_DETECTED := FALSE;
   BenchUut6.ENERGY_SAVING_MODE := FALSE;
   BenchUut6.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[50] := BenchUut6.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[50] := BenchUut6.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[50] := BenchUut6.HVAC_MODE_SELECTOR;
   BenchUut6();
   TraceOut_SUPPLY_FAN_RUN[50] := BenchUut6.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[50] := BenchUut6.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 51:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[51] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.OCCUPANCY_DETECTED := FALSE;
   BenchUut6.ENERGY_SAVING_MODE := TRUE;
   BenchUut6.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[51] := BenchUut6.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[51] := BenchUut6.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[51] := BenchUut6.HVAC_MODE_SELECTOR;
   BenchUut6();
   TraceOut_SUPPLY_FAN_RUN[51] := BenchUut6.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[51] := BenchUut6.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 52:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[52] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.OCCUPANCY_DETECTED := TRUE;
   BenchUut6.ENERGY_SAVING_MODE := FALSE;
   BenchUut6.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[52] := BenchUut6.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[52] := BenchUut6.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[52] := BenchUut6.HVAC_MODE_SELECTOR;
   BenchUut6();
   TraceOut_SUPPLY_FAN_RUN[52] := BenchUut6.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[52] := BenchUut6.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 53:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[53] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut6.OCCUPANCY_DETECTED := TRUE;
   BenchUut6.ENERGY_SAVING_MODE := TRUE;
   BenchUut6.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[53] := BenchUut6.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[53] := BenchUut6.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[53] := BenchUut6.HVAC_MODE_SELECTOR;
   BenchUut6();
   TraceOut_SUPPLY_FAN_RUN[53] := BenchUut6.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[53] := BenchUut6.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 54:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[54] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut7.OCCUPANCY_DETECTED := FALSE;
   BenchUut7.ENERGY_SAVING_MODE := FALSE;
   BenchUut7.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[54] := BenchUut7.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[54] := BenchUut7.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[54] := BenchUut7.HVAC_MODE_SELECTOR;
   BenchUut7();
   TraceOut_SUPPLY_FAN_RUN[54] := BenchUut7.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[54] := BenchUut7.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 55:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[55] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut7.OCCUPANCY_DETECTED := FALSE;
   BenchUut7.ENERGY_SAVING_MODE := TRUE;
   BenchUut7.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[55] := BenchUut7.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[55] := BenchUut7.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[55] := BenchUut7.HVAC_MODE_SELECTOR;
   BenchUut7();
   TraceOut_SUPPLY_FAN_RUN[55] := BenchUut7.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[55] := BenchUut7.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 56:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[56] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut7.OCCUPANCY_DETECTED := TRUE;
   BenchUut7.ENERGY_SAVING_MODE := FALSE;
   BenchUut7.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[56] := BenchUut7.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[56] := BenchUut7.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[56] := BenchUut7.HVAC_MODE_SELECTOR;
   BenchUut7();
   TraceOut_SUPPLY_FAN_RUN[56] := BenchUut7.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[56] := BenchUut7.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 57:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[57] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut7.OCCUPANCY_DETECTED := TRUE;
   BenchUut7.ENERGY_SAVING_MODE := TRUE;
   BenchUut7.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[57] := BenchUut7.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[57] := BenchUut7.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[57] := BenchUut7.HVAC_MODE_SELECTOR;
   BenchUut7();
   TraceOut_SUPPLY_FAN_RUN[57] := BenchUut7.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[57] := BenchUut7.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 58:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[58] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut8.OCCUPANCY_DETECTED := FALSE;
   BenchUut8.ENERGY_SAVING_MODE := FALSE;
   BenchUut8.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[58] := BenchUut8.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[58] := BenchUut8.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[58] := BenchUut8.HVAC_MODE_SELECTOR;
   BenchUut8();
   TraceOut_SUPPLY_FAN_RUN[58] := BenchUut8.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[58] := BenchUut8.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 59:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[59] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut8.OCCUPANCY_DETECTED := FALSE;
   BenchUut8.ENERGY_SAVING_MODE := TRUE;
   BenchUut8.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[59] := BenchUut8.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[59] := BenchUut8.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[59] := BenchUut8.HVAC_MODE_SELECTOR;
   BenchUut8();
   TraceOut_SUPPLY_FAN_RUN[59] := BenchUut8.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[59] := BenchUut8.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 60:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[60] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut8.OCCUPANCY_DETECTED := TRUE;
   BenchUut8.ENERGY_SAVING_MODE := FALSE;
   BenchUut8.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[60] := BenchUut8.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[60] := BenchUut8.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[60] := BenchUut8.HVAC_MODE_SELECTOR;
   BenchUut8();
   TraceOut_SUPPLY_FAN_RUN[60] := BenchUut8.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[60] := BenchUut8.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 61:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[61] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut8.OCCUPANCY_DETECTED := TRUE;
   BenchUut8.ENERGY_SAVING_MODE := TRUE;
   BenchUut8.HVAC_MODE_SELECTOR := INT#3;
   TraceIn_OCCUPANCY_DETECTED[61] := BenchUut8.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[61] := BenchUut8.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[61] := BenchUut8.HVAC_MODE_SELECTOR;
   BenchUut8();
   TraceOut_SUPPLY_FAN_RUN[61] := BenchUut8.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[61] := BenchUut8.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 62:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[62] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut9.OCCUPANCY_DETECTED := TRUE;
   BenchUut9.ENERGY_SAVING_MODE := FALSE;
   BenchUut9.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[62] := BenchUut9.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[62] := BenchUut9.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[62] := BenchUut9.HVAC_MODE_SELECTOR;
   BenchUut9();
   TraceOut_SUPPLY_FAN_RUN[62] := BenchUut9.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[62] := BenchUut9.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 63:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(29900) THEN
   TraceDt[63] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut9.OCCUPANCY_DETECTED := TRUE;
   BenchUut9.ENERGY_SAVING_MODE := FALSE;
   BenchUut9.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[63] := BenchUut9.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[63] := BenchUut9.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[63] := BenchUut9.HVAC_MODE_SELECTOR;
   BenchUut9();
   TraceOut_SUPPLY_FAN_RUN[63] := BenchUut9.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[63] := BenchUut9.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 64:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(200) THEN
   TraceDt[64] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut9.OCCUPANCY_DETECTED := TRUE;
   BenchUut9.ENERGY_SAVING_MODE := FALSE;
   BenchUut9.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[64] := BenchUut9.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[64] := BenchUut9.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[64] := BenchUut9.HVAC_MODE_SELECTOR;
   BenchUut9();
   TraceOut_SUPPLY_FAN_RUN[64] := BenchUut9.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[64] := BenchUut9.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 65:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[65] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut9.OCCUPANCY_DETECTED := FALSE;
   BenchUut9.ENERGY_SAVING_MODE := FALSE;
   BenchUut9.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[65] := BenchUut9.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[65] := BenchUut9.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[65] := BenchUut9.HVAC_MODE_SELECTOR;
   BenchUut9();
   TraceOut_SUPPLY_FAN_RUN[65] := BenchUut9.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[65] := BenchUut9.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 66:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[66] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut9.OCCUPANCY_DETECTED := TRUE;
   BenchUut9.ENERGY_SAVING_MODE := FALSE;
   BenchUut9.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[66] := BenchUut9.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[66] := BenchUut9.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[66] := BenchUut9.HVAC_MODE_SELECTOR;
   BenchUut9();
   TraceOut_SUPPLY_FAN_RUN[66] := BenchUut9.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[66] := BenchUut9.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 67:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(30100) THEN
   TraceDt[67] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut9.OCCUPANCY_DETECTED := TRUE;
   BenchUut9.ENERGY_SAVING_MODE := FALSE;
   BenchUut9.HVAC_MODE_SELECTOR := INT#0;
   TraceIn_OCCUPANCY_DETECTED[67] := BenchUut9.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[67] := BenchUut9.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[67] := BenchUut9.HVAC_MODE_SELECTOR;
   BenchUut9();
   TraceOut_SUPPLY_FAN_RUN[67] := BenchUut9.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[67] := BenchUut9.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 68:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[68] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut10.OCCUPANCY_DETECTED := TRUE;
   BenchUut10.ENERGY_SAVING_MODE := FALSE;
   BenchUut10.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[68] := BenchUut10.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[68] := BenchUut10.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[68] := BenchUut10.HVAC_MODE_SELECTOR;
   BenchUut10();
   TraceOut_SUPPLY_FAN_RUN[68] := BenchUut10.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[68] := BenchUut10.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 69:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(29900) THEN
   TraceDt[69] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut10.OCCUPANCY_DETECTED := TRUE;
   BenchUut10.ENERGY_SAVING_MODE := FALSE;
   BenchUut10.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[69] := BenchUut10.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[69] := BenchUut10.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[69] := BenchUut10.HVAC_MODE_SELECTOR;
   BenchUut10();
   TraceOut_SUPPLY_FAN_RUN[69] := BenchUut10.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[69] := BenchUut10.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 70:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(200) THEN
   TraceDt[70] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut10.OCCUPANCY_DETECTED := TRUE;
   BenchUut10.ENERGY_SAVING_MODE := FALSE;
   BenchUut10.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[70] := BenchUut10.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[70] := BenchUut10.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[70] := BenchUut10.HVAC_MODE_SELECTOR;
   BenchUut10();
   TraceOut_SUPPLY_FAN_RUN[70] := BenchUut10.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[70] := BenchUut10.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 71:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[71] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut10.OCCUPANCY_DETECTED := FALSE;
   BenchUut10.ENERGY_SAVING_MODE := FALSE;
   BenchUut10.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[71] := BenchUut10.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[71] := BenchUut10.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[71] := BenchUut10.HVAC_MODE_SELECTOR;
   BenchUut10();
   TraceOut_SUPPLY_FAN_RUN[71] := BenchUut10.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[71] := BenchUut10.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 72:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[72] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut10.OCCUPANCY_DETECTED := TRUE;
   BenchUut10.ENERGY_SAVING_MODE := FALSE;
   BenchUut10.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[72] := BenchUut10.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[72] := BenchUut10.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[72] := BenchUut10.HVAC_MODE_SELECTOR;
   BenchUut10();
   TraceOut_SUPPLY_FAN_RUN[72] := BenchUut10.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[72] := BenchUut10.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 73:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(30100) THEN
   TraceDt[73] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut10.OCCUPANCY_DETECTED := TRUE;
   BenchUut10.ENERGY_SAVING_MODE := FALSE;
   BenchUut10.HVAC_MODE_SELECTOR := INT#1;
   TraceIn_OCCUPANCY_DETECTED[73] := BenchUut10.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[73] := BenchUut10.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[73] := BenchUut10.HVAC_MODE_SELECTOR;
   BenchUut10();
   TraceOut_SUPPLY_FAN_RUN[73] := BenchUut10.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[73] := BenchUut10.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 74:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(0) THEN
   TraceDt[74] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut11.OCCUPANCY_DETECTED := TRUE;
   BenchUut11.ENERGY_SAVING_MODE := FALSE;
   BenchUut11.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[74] := BenchUut11.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[74] := BenchUut11.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[74] := BenchUut11.HVAC_MODE_SELECTOR;
   BenchUut11();
   TraceOut_SUPPLY_FAN_RUN[74] := BenchUut11.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[74] := BenchUut11.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 75:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(29900) THEN
   TraceDt[75] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut11.OCCUPANCY_DETECTED := TRUE;
   BenchUut11.ENERGY_SAVING_MODE := FALSE;
   BenchUut11.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[75] := BenchUut11.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[75] := BenchUut11.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[75] := BenchUut11.HVAC_MODE_SELECTOR;
   BenchUut11();
   TraceOut_SUPPLY_FAN_RUN[75] := BenchUut11.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[75] := BenchUut11.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 76:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(200) THEN
   TraceDt[76] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut11.OCCUPANCY_DETECTED := TRUE;
   BenchUut11.ENERGY_SAVING_MODE := FALSE;
   BenchUut11.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[76] := BenchUut11.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[76] := BenchUut11.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[76] := BenchUut11.HVAC_MODE_SELECTOR;
   BenchUut11();
   TraceOut_SUPPLY_FAN_RUN[76] := BenchUut11.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[76] := BenchUut11.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 77:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[77] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut11.OCCUPANCY_DETECTED := FALSE;
   BenchUut11.ENERGY_SAVING_MODE := FALSE;
   BenchUut11.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[77] := BenchUut11.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[77] := BenchUut11.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[77] := BenchUut11.HVAC_MODE_SELECTOR;
   BenchUut11();
   TraceOut_SUPPLY_FAN_RUN[77] := BenchUut11.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[77] := BenchUut11.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 78:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(100) THEN
   TraceDt[78] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut11.OCCUPANCY_DETECTED := TRUE;
   BenchUut11.ENERGY_SAVING_MODE := FALSE;
   BenchUut11.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[78] := BenchUut11.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[78] := BenchUut11.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[78] := BenchUut11.HVAC_MODE_SELECTOR;
   BenchUut11();
   TraceOut_SUPPLY_FAN_RUN[78] := BenchUut11.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[78] := BenchUut11.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 79:
  IF BenchCurrentTime - BenchLastTime >= UDINT_TO_TIME(30100) THEN
   TraceDt[79] := TIME_TO_UDINT(BenchCurrentTime - BenchLastTime);
   BenchLastTime := BenchCurrentTime;
   BenchUut11.OCCUPANCY_DETECTED := TRUE;
   BenchUut11.ENERGY_SAVING_MODE := FALSE;
   BenchUut11.HVAC_MODE_SELECTOR := INT#2;
   TraceIn_OCCUPANCY_DETECTED[79] := BenchUut11.OCCUPANCY_DETECTED;
   TraceIn_ENERGY_SAVING_MODE[79] := BenchUut11.ENERGY_SAVING_MODE;
   TraceIn_HVAC_MODE_SELECTOR[79] := BenchUut11.HVAC_MODE_SELECTOR;
   BenchUut11();
   TraceOut_SUPPLY_FAN_RUN[79] := BenchUut11.SUPPLY_FAN_RUN;
   TraceOut_TEMP_SETPOINT_ADJUST[79] := BenchUut11.TEMP_SETPOINT_ADJUST;
   BenchCalls := BenchCalls + 1;
   BenchStep := BenchStep + 1;
  END_IF;
 END_CASE;
 END_IF;
 IF BenchStep >= 80 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
