PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_ipText : ARRAY[0..6] OF STRING(254);
 TraceOut_ipValue : ARRAY[0..6] OF UDINT;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.ipText := '192.168.1.10';
   TraceIn_ipText[0] := BenchUut0.ipText;
   BenchUut0();
   TraceOut_ipValue[0] := BenchUut0.ipValue;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.ipText := '192.168.1.10';
   TraceIn_ipText[1] := BenchUut0.ipText;
   BenchUut0();
   TraceOut_ipValue[1] := BenchUut0.ipValue;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut1.ipText := '255.255.255.255';
   TraceIn_ipText[2] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[2] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut1.ipText := '0.0.0.0';
   TraceIn_ipText[3] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[3] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut1.ipText := '001.002.003.004';
   TraceIn_ipText[4] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[4] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut1.ipText := '256.0.0.1';
   TraceIn_ipText[5] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[5] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.ipText := '1.2.3';
   TraceIn_ipText[6] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[6] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 7 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
