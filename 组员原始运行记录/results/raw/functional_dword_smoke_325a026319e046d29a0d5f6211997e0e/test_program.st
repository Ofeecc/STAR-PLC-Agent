PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn0 : ARRAY[0..11] OF DWORD;
 TraceOut0 : ARRAY[0..11] OF BOOL;
 TraceOut1 : ARRAY[0..11] OF BOOL;
 TraceOut2 : ARRAY[0..11] OF DWORD;
 TraceOut3 : ARRAY[0..11] OF USINT;
 TraceOut4 : ARRAY[0..11] OF BOOL;
 TraceOut5 : ARRAY[0..11] OF DWORD;
 TraceOut6 : ARRAY[0..11] OF USINT;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
  BenchUut0.value := DWORD#0;
  TraceIn0[0] := BenchUut0.value;
  BenchUut0();
  TraceOut0[0] := BenchUut0.hasChanged;
  TraceOut1[0] := BenchUut0.hasRisingEdges;
  TraceOut2[0] := BenchUut0.risingBits;
  TraceOut3[0] := BenchUut0.noOfRisingBits;
  TraceOut4[0] := BenchUut0.hasFallingEdges;
  TraceOut5[0] := BenchUut0.fallingBits;
  TraceOut6[0] := BenchUut0.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 1:
  BenchUut0.value := DWORD#1;
  TraceIn0[1] := BenchUut0.value;
  BenchUut0();
  TraceOut0[1] := BenchUut0.hasChanged;
  TraceOut1[1] := BenchUut0.hasRisingEdges;
  TraceOut2[1] := BenchUut0.risingBits;
  TraceOut3[1] := BenchUut0.noOfRisingBits;
  TraceOut4[1] := BenchUut0.hasFallingEdges;
  TraceOut5[1] := BenchUut0.fallingBits;
  TraceOut6[1] := BenchUut0.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 2:
  BenchUut0.value := DWORD#1;
  TraceIn0[2] := BenchUut0.value;
  BenchUut0();
  TraceOut0[2] := BenchUut0.hasChanged;
  TraceOut1[2] := BenchUut0.hasRisingEdges;
  TraceOut2[2] := BenchUut0.risingBits;
  TraceOut3[2] := BenchUut0.noOfRisingBits;
  TraceOut4[2] := BenchUut0.hasFallingEdges;
  TraceOut5[2] := BenchUut0.fallingBits;
  TraceOut6[2] := BenchUut0.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 3:
  BenchUut0.value := DWORD#3;
  TraceIn0[3] := BenchUut0.value;
  BenchUut0();
  TraceOut0[3] := BenchUut0.hasChanged;
  TraceOut1[3] := BenchUut0.hasRisingEdges;
  TraceOut2[3] := BenchUut0.risingBits;
  TraceOut3[3] := BenchUut0.noOfRisingBits;
  TraceOut4[3] := BenchUut0.hasFallingEdges;
  TraceOut5[3] := BenchUut0.fallingBits;
  TraceOut6[3] := BenchUut0.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 4:
  BenchUut0.value := DWORD#2;
  TraceIn0[4] := BenchUut0.value;
  BenchUut0();
  TraceOut0[4] := BenchUut0.hasChanged;
  TraceOut1[4] := BenchUut0.hasRisingEdges;
  TraceOut2[4] := BenchUut0.risingBits;
  TraceOut3[4] := BenchUut0.noOfRisingBits;
  TraceOut4[4] := BenchUut0.hasFallingEdges;
  TraceOut5[4] := BenchUut0.fallingBits;
  TraceOut6[4] := BenchUut0.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 5:
  BenchUut0.value := DWORD#0;
  TraceIn0[5] := BenchUut0.value;
  BenchUut0();
  TraceOut0[5] := BenchUut0.hasChanged;
  TraceOut1[5] := BenchUut0.hasRisingEdges;
  TraceOut2[5] := BenchUut0.risingBits;
  TraceOut3[5] := BenchUut0.noOfRisingBits;
  TraceOut4[5] := BenchUut0.hasFallingEdges;
  TraceOut5[5] := BenchUut0.fallingBits;
  TraceOut6[5] := BenchUut0.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 6:
  BenchUut0.value := DWORD#4294967295;
  TraceIn0[6] := BenchUut0.value;
  BenchUut0();
  TraceOut0[6] := BenchUut0.hasChanged;
  TraceOut1[6] := BenchUut0.hasRisingEdges;
  TraceOut2[6] := BenchUut0.risingBits;
  TraceOut3[6] := BenchUut0.noOfRisingBits;
  TraceOut4[6] := BenchUut0.hasFallingEdges;
  TraceOut5[6] := BenchUut0.fallingBits;
  TraceOut6[6] := BenchUut0.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 7:
  BenchUut0.value := DWORD#0;
  TraceIn0[7] := BenchUut0.value;
  BenchUut0();
  TraceOut0[7] := BenchUut0.hasChanged;
  TraceOut1[7] := BenchUut0.hasRisingEdges;
  TraceOut2[7] := BenchUut0.risingBits;
  TraceOut3[7] := BenchUut0.noOfRisingBits;
  TraceOut4[7] := BenchUut0.hasFallingEdges;
  TraceOut5[7] := BenchUut0.fallingBits;
  TraceOut6[7] := BenchUut0.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 8:
  BenchUut0.value := DWORD#2147483648;
  TraceIn0[8] := BenchUut0.value;
  BenchUut0();
  TraceOut0[8] := BenchUut0.hasChanged;
  TraceOut1[8] := BenchUut0.hasRisingEdges;
  TraceOut2[8] := BenchUut0.risingBits;
  TraceOut3[8] := BenchUut0.noOfRisingBits;
  TraceOut4[8] := BenchUut0.hasFallingEdges;
  TraceOut5[8] := BenchUut0.fallingBits;
  TraceOut6[8] := BenchUut0.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 9:
  BenchUut0.value := DWORD#2147483647;
  TraceIn0[9] := BenchUut0.value;
  BenchUut0();
  TraceOut0[9] := BenchUut0.hasChanged;
  TraceOut1[9] := BenchUut0.hasRisingEdges;
  TraceOut2[9] := BenchUut0.risingBits;
  TraceOut3[9] := BenchUut0.noOfRisingBits;
  TraceOut4[9] := BenchUut0.hasFallingEdges;
  TraceOut5[9] := BenchUut0.fallingBits;
  TraceOut6[9] := BenchUut0.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 10:
  BenchUut1.value := DWORD#4294967295;
  TraceIn0[10] := BenchUut1.value;
  BenchUut1();
  TraceOut0[10] := BenchUut1.hasChanged;
  TraceOut1[10] := BenchUut1.hasRisingEdges;
  TraceOut2[10] := BenchUut1.risingBits;
  TraceOut3[10] := BenchUut1.noOfRisingBits;
  TraceOut4[10] := BenchUut1.hasFallingEdges;
  TraceOut5[10] := BenchUut1.fallingBits;
  TraceOut6[10] := BenchUut1.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 11:
  BenchUut1.value := DWORD#4294967295;
  TraceIn0[11] := BenchUut1.value;
  BenchUut1();
  TraceOut0[11] := BenchUut1.hasChanged;
  TraceOut1[11] := BenchUut1.hasRisingEdges;
  TraceOut2[11] := BenchUut1.risingBits;
  TraceOut3[11] := BenchUut1.noOfRisingBits;
  TraceOut4[11] := BenchUut1.hasFallingEdges;
  TraceOut5[11] := BenchUut1.fallingBits;
  TraceOut6[11] := BenchUut1.noOfFallingBits;
  BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 12 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
