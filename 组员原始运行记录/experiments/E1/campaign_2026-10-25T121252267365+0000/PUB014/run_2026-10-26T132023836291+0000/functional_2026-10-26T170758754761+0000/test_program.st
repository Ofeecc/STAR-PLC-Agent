PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn0 : ARRAY[0..18] OF STRING(254);
 TraceOut0 : ARRAY[0..18] OF UDINT;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
  BenchUut0.ipText := '0.0.0.0';
  TraceIn0[0] := BenchUut0.ipText;
  BenchUut0();
  TraceOut0[0] := BenchUut0.ipValue;
  BenchCalls := BenchCalls + 1;
 1:
  BenchUut0.ipText := '255.255.255.255';
  TraceIn0[1] := BenchUut0.ipText;
  BenchUut0();
  TraceOut0[1] := BenchUut0.ipValue;
  BenchCalls := BenchCalls + 1;
 2:
  BenchUut0.ipText := '192.168.1.10';
  TraceIn0[2] := BenchUut0.ipText;
  BenchUut0();
  TraceOut0[2] := BenchUut0.ipValue;
  BenchCalls := BenchCalls + 1;
 3:
  BenchUut0.ipText := '1.2.3.4';
  TraceIn0[3] := BenchUut0.ipText;
  BenchUut0();
  TraceOut0[3] := BenchUut0.ipValue;
  BenchCalls := BenchCalls + 1;
 4:
  BenchUut0.ipText := '001.002.003.004';
  TraceIn0[4] := BenchUut0.ipText;
  BenchUut0();
  TraceOut0[4] := BenchUut0.ipValue;
  BenchCalls := BenchCalls + 1;
 5:
  BenchUut1.ipText := '1.2.3.4';
  TraceIn0[5] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[5] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 6:
  BenchUut1.ipText := '';
  TraceIn0[6] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[6] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 7:
  BenchUut1.ipText := '1.2.3';
  TraceIn0[7] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[7] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 8:
  BenchUut1.ipText := '1.2.3.4.5';
  TraceIn0[8] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[8] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 9:
  BenchUut1.ipText := '.1.2.3';
  TraceIn0[9] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[9] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 10:
  BenchUut1.ipText := '1..2.3';
  TraceIn0[10] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[10] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 11:
  BenchUut1.ipText := '1.2.3.';
  TraceIn0[11] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[11] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 12:
  BenchUut1.ipText := '1.2.3.256';
  TraceIn0[12] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[12] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 13:
  BenchUut1.ipText := '-1.2.3.4';
  TraceIn0[13] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[13] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 14:
  BenchUut1.ipText := '1.2.3.x';
  TraceIn0[14] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[14] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 15:
  BenchUut1.ipText := ' 1.2.3.4';
  TraceIn0[15] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[15] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 16:
  BenchUut1.ipText := '1.2.3.4 ';
  TraceIn0[16] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[16] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 17:
  BenchUut1.ipText := '0x1.2.3.4';
  TraceIn0[17] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[17] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 18:
  BenchUut1.ipText := '999999999999999999999.2.3.4';
  TraceIn0[18] := BenchUut1.ipText;
  BenchUut1();
  TraceOut0[18] := BenchUut1.ipValue;
  BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 19 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
