PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_Fault : ARRAY[0..12] OF BOOL;
 TraceIn_Ack : ARRAY[0..12] OF BOOL;
 TraceIn_Reset : ARRAY[0..12] OF BOOL;
 TraceOut_Alarm : ARRAY[0..12] OF BOOL;
 TraceOut_Acknowledged : ARRAY[0..12] OF BOOL;
 TraceOut_Horn : ARRAY[0..12] OF BOOL;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.Fault := FALSE;
   BenchUut0.Ack := FALSE;
   BenchUut0.Reset := FALSE;
   TraceIn_Fault[0] := BenchUut0.Fault;
   TraceIn_Ack[0] := BenchUut0.Ack;
   TraceIn_Reset[0] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Alarm[0] := BenchUut0.Alarm;
   TraceOut_Acknowledged[0] := BenchUut0.Acknowledged;
   TraceOut_Horn[0] := BenchUut0.Horn;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.Fault := TRUE;
   BenchUut0.Ack := FALSE;
   BenchUut0.Reset := FALSE;
   TraceIn_Fault[1] := BenchUut0.Fault;
   TraceIn_Ack[1] := BenchUut0.Ack;
   TraceIn_Reset[1] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Alarm[1] := BenchUut0.Alarm;
   TraceOut_Acknowledged[1] := BenchUut0.Acknowledged;
   TraceOut_Horn[1] := BenchUut0.Horn;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.Fault := TRUE;
   BenchUut0.Ack := TRUE;
   BenchUut0.Reset := FALSE;
   TraceIn_Fault[2] := BenchUut0.Fault;
   TraceIn_Ack[2] := BenchUut0.Ack;
   TraceIn_Reset[2] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Alarm[2] := BenchUut0.Alarm;
   TraceOut_Acknowledged[2] := BenchUut0.Acknowledged;
   TraceOut_Horn[2] := BenchUut0.Horn;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.Fault := FALSE;
   BenchUut0.Ack := FALSE;
   BenchUut0.Reset := FALSE;
   TraceIn_Fault[3] := BenchUut0.Fault;
   TraceIn_Ack[3] := BenchUut0.Ack;
   TraceIn_Reset[3] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Alarm[3] := BenchUut0.Alarm;
   TraceOut_Acknowledged[3] := BenchUut0.Acknowledged;
   TraceOut_Horn[3] := BenchUut0.Horn;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.Fault := FALSE;
   BenchUut0.Ack := FALSE;
   BenchUut0.Reset := TRUE;
   TraceIn_Fault[4] := BenchUut0.Fault;
   TraceIn_Ack[4] := BenchUut0.Ack;
   TraceIn_Reset[4] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Alarm[4] := BenchUut0.Alarm;
   TraceOut_Acknowledged[4] := BenchUut0.Acknowledged;
   TraceOut_Horn[4] := BenchUut0.Horn;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut0.Fault := FALSE;
   BenchUut0.Ack := TRUE;
   BenchUut0.Reset := FALSE;
   TraceIn_Fault[5] := BenchUut0.Fault;
   TraceIn_Ack[5] := BenchUut0.Ack;
   TraceIn_Reset[5] := BenchUut0.Reset;
   BenchUut0();
   TraceOut_Alarm[5] := BenchUut0.Alarm;
   TraceOut_Acknowledged[5] := BenchUut0.Acknowledged;
   TraceOut_Horn[5] := BenchUut0.Horn;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.Fault := FALSE;
   BenchUut1.Ack := FALSE;
   BenchUut1.Reset := FALSE;
   TraceIn_Fault[6] := BenchUut1.Fault;
   TraceIn_Ack[6] := BenchUut1.Ack;
   TraceIn_Reset[6] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Alarm[6] := BenchUut1.Alarm;
   TraceOut_Acknowledged[6] := BenchUut1.Acknowledged;
   TraceOut_Horn[6] := BenchUut1.Horn;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut1.Fault := TRUE;
   BenchUut1.Ack := FALSE;
   BenchUut1.Reset := FALSE;
   TraceIn_Fault[7] := BenchUut1.Fault;
   TraceIn_Ack[7] := BenchUut1.Ack;
   TraceIn_Reset[7] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Alarm[7] := BenchUut1.Alarm;
   TraceOut_Acknowledged[7] := BenchUut1.Acknowledged;
   TraceOut_Horn[7] := BenchUut1.Horn;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.Fault := TRUE;
   BenchUut1.Ack := TRUE;
   BenchUut1.Reset := FALSE;
   TraceIn_Fault[8] := BenchUut1.Fault;
   TraceIn_Ack[8] := BenchUut1.Ack;
   TraceIn_Reset[8] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Alarm[8] := BenchUut1.Alarm;
   TraceOut_Acknowledged[8] := BenchUut1.Acknowledged;
   TraceOut_Horn[8] := BenchUut1.Horn;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.Fault := TRUE;
   BenchUut1.Ack := FALSE;
   BenchUut1.Reset := TRUE;
   TraceIn_Fault[9] := BenchUut1.Fault;
   TraceIn_Ack[9] := BenchUut1.Ack;
   TraceIn_Reset[9] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Alarm[9] := BenchUut1.Alarm;
   TraceOut_Acknowledged[9] := BenchUut1.Acknowledged;
   TraceOut_Horn[9] := BenchUut1.Horn;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.Fault := FALSE;
   BenchUut1.Ack := FALSE;
   BenchUut1.Reset := FALSE;
   TraceIn_Fault[10] := BenchUut1.Fault;
   TraceIn_Ack[10] := BenchUut1.Ack;
   TraceIn_Reset[10] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Alarm[10] := BenchUut1.Alarm;
   TraceOut_Acknowledged[10] := BenchUut1.Acknowledged;
   TraceOut_Horn[10] := BenchUut1.Horn;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut1.Fault := TRUE;
   BenchUut1.Ack := TRUE;
   BenchUut1.Reset := FALSE;
   TraceIn_Fault[11] := BenchUut1.Fault;
   TraceIn_Ack[11] := BenchUut1.Ack;
   TraceIn_Reset[11] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Alarm[11] := BenchUut1.Alarm;
   TraceOut_Acknowledged[11] := BenchUut1.Acknowledged;
   TraceOut_Horn[11] := BenchUut1.Horn;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut1.Fault := TRUE;
   BenchUut1.Ack := TRUE;
   BenchUut1.Reset := FALSE;
   TraceIn_Fault[12] := BenchUut1.Fault;
   TraceIn_Ack[12] := BenchUut1.Ack;
   TraceIn_Reset[12] := BenchUut1.Reset;
   BenchUut1();
   TraceOut_Alarm[12] := BenchUut1.Alarm;
   TraceOut_Acknowledged[12] := BenchUut1.Acknowledged;
   TraceOut_Horn[12] := BenchUut1.Horn;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 13 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
