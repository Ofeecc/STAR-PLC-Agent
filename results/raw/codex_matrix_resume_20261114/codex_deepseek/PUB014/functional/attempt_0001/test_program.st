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
 BenchUut7 : FB_Task;
 TraceIn_ipText : ARRAY[0..60] OF STRING(254);
 TraceOut_ipValue : ARRAY[0..60] OF UDINT;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.ipText := '0.0.0.0';
   TraceIn_ipText[0] := BenchUut0.ipText;
   BenchUut0();
   TraceOut_ipValue[0] := BenchUut0.ipValue;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.ipText := '255.255.255.255';
   TraceIn_ipText[1] := BenchUut0.ipText;
   BenchUut0();
   TraceOut_ipValue[1] := BenchUut0.ipValue;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.ipText := '192.168.1.10';
   TraceIn_ipText[2] := BenchUut0.ipText;
   BenchUut0();
   TraceOut_ipValue[2] := BenchUut0.ipValue;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.ipText := '1.2.3.4';
   TraceIn_ipText[3] := BenchUut0.ipText;
   BenchUut0();
   TraceOut_ipValue[3] := BenchUut0.ipValue;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.ipText := '001.002.003.004';
   TraceIn_ipText[4] := BenchUut0.ipText;
   BenchUut0();
   TraceOut_ipValue[4] := BenchUut0.ipValue;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut1.ipText := '1.2.3.4';
   TraceIn_ipText[5] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[5] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.ipText := '';
   TraceIn_ipText[6] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[6] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut1.ipText := '1.2.3';
   TraceIn_ipText[7] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[7] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.ipText := '1.2.3.4.5';
   TraceIn_ipText[8] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[8] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.ipText := '.1.2.3';
   TraceIn_ipText[9] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[9] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.ipText := '1..2.3';
   TraceIn_ipText[10] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[10] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut1.ipText := '1.2.3.';
   TraceIn_ipText[11] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[11] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut1.ipText := '1.2.3.256';
   TraceIn_ipText[12] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[12] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut1.ipText := '-1.2.3.4';
   TraceIn_ipText[13] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[13] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 14:
   BenchUut1.ipText := '1.2.3.x';
   TraceIn_ipText[14] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[14] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 15:
   BenchUut1.ipText := ' 1.2.3.4';
   TraceIn_ipText[15] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[15] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 16:
   BenchUut1.ipText := '1.2.3.4 ';
   TraceIn_ipText[16] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[16] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 17:
   BenchUut1.ipText := '0x1.2.3.4';
   TraceIn_ipText[17] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[17] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 18:
   BenchUut1.ipText := '999999999999999999999.2.3.4';
   TraceIn_ipText[18] := BenchUut1.ipText;
   BenchUut1();
   TraceOut_ipValue[18] := BenchUut1.ipValue;
   BenchCalls := BenchCalls + 1;
 19:
   BenchUut2.ipText := '+1.2.3.4';
   TraceIn_ipText[19] := BenchUut2.ipText;
   BenchUut2();
   TraceOut_ipValue[19] := BenchUut2.ipValue;
   BenchCalls := BenchCalls + 1;
 20:
   BenchUut2.ipText := '1.2.3.4$N';
   TraceIn_ipText[20] := BenchUut2.ipText;
   BenchUut2();
   TraceOut_ipValue[20] := BenchUut2.ipValue;
   BenchCalls := BenchCalls + 1;
 21:
   BenchUut2.ipText := '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001.2.3.4';
   TraceIn_ipText[21] := BenchUut2.ipText;
   BenchUut2();
   TraceOut_ipValue[21] := BenchUut2.ipValue;
   BenchCalls := BenchCalls + 1;
 22:
   BenchUut2.ipText := '1.2.3.4294967296';
   TraceIn_ipText[22] := BenchUut2.ipText;
   BenchUut2();
   TraceOut_ipValue[22] := BenchUut2.ipValue;
   BenchCalls := BenchCalls + 1;
 23:
   BenchUut3.ipText := '192.168.1.2$00ignored_tail';
   TraceIn_ipText[23] := BenchUut3.ipText;
   BenchUut3();
   TraceOut_ipValue[23] := BenchUut3.ipValue;
   BenchCalls := BenchCalls + 1;
 24:
   BenchUut3.ipText := '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001.2.3.4';
   TraceIn_ipText[24] := BenchUut3.ipText;
   BenchUut3();
   TraceOut_ipValue[24] := BenchUut3.ipValue;
   BenchCalls := BenchCalls + 1;
 25:
   BenchUut3.ipText := '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001.2.3.4';
   TraceIn_ipText[25] := BenchUut3.ipText;
   BenchUut3();
   TraceOut_ipValue[25] := BenchUut3.ipValue;
   BenchCalls := BenchCalls + 1;
 26:
   BenchUut3.ipText := ' 1.2.3.4';
   TraceIn_ipText[26] := BenchUut3.ipText;
   BenchUut3();
   TraceOut_ipValue[26] := BenchUut3.ipValue;
   BenchCalls := BenchCalls + 1;
 27:
   BenchUut3.ipText := '1.2.3.４';
   TraceIn_ipText[27] := BenchUut3.ipText;
   BenchUut3();
   TraceOut_ipValue[27] := BenchUut3.ipValue;
   BenchCalls := BenchCalls + 1;
 28:
   BenchUut3.ipText := '10.20.30.40';
   TraceIn_ipText[28] := BenchUut3.ipText;
   BenchUut3();
   TraceOut_ipValue[28] := BenchUut3.ipValue;
   BenchCalls := BenchCalls + 1;
 29:
   BenchUut3.ipText := '10.20.30.40';
   TraceIn_ipText[29] := BenchUut3.ipText;
   BenchUut3();
   TraceOut_ipValue[29] := BenchUut3.ipValue;
   BenchCalls := BenchCalls + 1;
 30:
   BenchUut3.ipText := '10.20.30.256';
   TraceIn_ipText[30] := BenchUut3.ipText;
   BenchUut3();
   TraceOut_ipValue[30] := BenchUut3.ipValue;
   BenchCalls := BenchCalls + 1;
 31:
   BenchUut3.ipText := '1.2.3.4';
   TraceIn_ipText[31] := BenchUut3.ipText;
   BenchUut3();
   TraceOut_ipValue[31] := BenchUut3.ipValue;
   BenchCalls := BenchCalls + 1;
 32:
   BenchUut4.ipText := '1.2.3.4';
   TraceIn_ipText[32] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[32] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 33:
   BenchUut4.ipText := '1.2.3.4';
   TraceIn_ipText[33] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[33] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 34:
   BenchUut4.ipText := '1.2.3';
   TraceIn_ipText[34] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[34] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 35:
   BenchUut4.ipText := '1.2.3.4';
   TraceIn_ipText[35] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[35] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 36:
   BenchUut4.ipText := '256.1.2.3';
   TraceIn_ipText[36] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[36] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 37:
   BenchUut4.ipText := '1.2.3.4';
   TraceIn_ipText[37] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[37] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 38:
   BenchUut4.ipText := '1..2.3';
   TraceIn_ipText[38] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[38] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 39:
   BenchUut4.ipText := '1.2.3.4';
   TraceIn_ipText[39] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[39] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 40:
   BenchUut4.ipText := 'a.1.2.3';
   TraceIn_ipText[40] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[40] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 41:
   BenchUut4.ipText := '1.2.3.4';
   TraceIn_ipText[41] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[41] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 42:
   BenchUut4.ipText := '1.2.3.4.5';
   TraceIn_ipText[42] := BenchUut4.ipText;
   BenchUut4();
   TraceOut_ipValue[42] := BenchUut4.ipValue;
   BenchCalls := BenchCalls + 1;
 43:
   BenchUut5.ipText := '00000000192.00000168.00000001.00000001';
   TraceIn_ipText[43] := BenchUut5.ipText;
   BenchUut5();
   TraceOut_ipValue[43] := BenchUut5.ipValue;
   BenchCalls := BenchCalls + 1;
 44:
   BenchUut5.ipText := '10.0.0.1$00999.999.999';
   TraceIn_ipText[44] := BenchUut5.ipText;
   BenchUut5();
   TraceOut_ipValue[44] := BenchUut5.ipValue;
   BenchCalls := BenchCalls + 1;
 45:
   BenchUut5.ipText := '000.000.000.000$00invalid';
   TraceIn_ipText[45] := BenchUut5.ipText;
   BenchUut5();
   TraceOut_ipValue[45] := BenchUut5.ipValue;
   BenchCalls := BenchCalls + 1;
 46:
   BenchUut5.ipText := '$001.2.3.4';
   TraceIn_ipText[46] := BenchUut5.ipText;
   BenchUut5();
   TraceOut_ipValue[46] := BenchUut5.ipValue;
   BenchCalls := BenchCalls + 1;
 47:
   BenchUut6.ipText := '172.16.254.1';
   TraceIn_ipText[47] := BenchUut6.ipText;
   BenchUut6();
   TraceOut_ipValue[47] := BenchUut6.ipValue;
   BenchCalls := BenchCalls + 1;
 48:
   BenchUut6.ipText := ' 172.16.254.1';
   TraceIn_ipText[48] := BenchUut6.ipText;
   BenchUut6();
   TraceOut_ipValue[48] := BenchUut6.ipValue;
   BenchCalls := BenchCalls + 1;
 49:
   BenchUut6.ipText := '+172.16.254.1';
   TraceIn_ipText[49] := BenchUut6.ipText;
   BenchUut6();
   TraceOut_ipValue[49] := BenchUut6.ipValue;
   BenchCalls := BenchCalls + 1;
 50:
   BenchUut6.ipText := '172.16.254.1 ';
   TraceIn_ipText[50] := BenchUut6.ipText;
   BenchUut6();
   TraceOut_ipValue[50] := BenchUut6.ipValue;
   BenchCalls := BenchCalls + 1;
 51:
   BenchUut6.ipText := '172..254.1';
   TraceIn_ipText[51] := BenchUut6.ipText;
   BenchUut6();
   TraceOut_ipValue[51] := BenchUut6.ipValue;
   BenchCalls := BenchCalls + 1;
 52:
   BenchUut6.ipText := '172.16.254';
   TraceIn_ipText[52] := BenchUut6.ipText;
   BenchUut6();
   TraceOut_ipValue[52] := BenchUut6.ipValue;
   BenchCalls := BenchCalls + 1;
 53:
   BenchUut6.ipText := '172.16.254.1.0';
   TraceIn_ipText[53] := BenchUut6.ipText;
   BenchUut6();
   TraceOut_ipValue[53] := BenchUut6.ipValue;
   BenchCalls := BenchCalls + 1;
 54:
   BenchUut6.ipText := '172.16.254.256';
   TraceIn_ipText[54] := BenchUut6.ipText;
   BenchUut6();
   TraceOut_ipValue[54] := BenchUut6.ipValue;
   BenchCalls := BenchCalls + 1;
 55:
   BenchUut6.ipText := '172.16.254.1.';
   TraceIn_ipText[55] := BenchUut6.ipText;
   BenchUut6();
   TraceOut_ipValue[55] := BenchUut6.ipValue;
   BenchCalls := BenchCalls + 1;
 56:
   BenchUut6.ipText := '172.16.254.2';
   TraceIn_ipText[56] := BenchUut6.ipText;
   BenchUut6();
   TraceOut_ipValue[56] := BenchUut6.ipValue;
   BenchCalls := BenchCalls + 1;
 57:
   BenchUut7.ipText := '127.0.0.1';
   TraceIn_ipText[57] := BenchUut7.ipText;
   BenchUut7();
   TraceOut_ipValue[57] := BenchUut7.ipValue;
   BenchCalls := BenchCalls + 1;
 58:
   BenchUut7.ipText := '255.255.255.0';
   TraceIn_ipText[58] := BenchUut7.ipText;
   BenchUut7();
   TraceOut_ipValue[58] := BenchUut7.ipValue;
   BenchCalls := BenchCalls + 1;
 59:
   BenchUut7.ipText := '192.168.255.254';
   TraceIn_ipText[59] := BenchUut7.ipText;
   BenchUut7();
   TraceOut_ipValue[59] := BenchUut7.ipValue;
   BenchCalls := BenchCalls + 1;
 60:
   BenchUut7.ipText := '0.0.0.255';
   TraceIn_ipText[60] := BenchUut7.ipText;
   BenchUut7();
   TraceOut_ipValue[60] := BenchUut7.ipValue;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 61 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
