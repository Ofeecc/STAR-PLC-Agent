PROGRAM PLC_PRG
VAR
 BenchStep : UDINT := 0;
 BenchCalls : UDINT := 0;
 BenchDone : BOOL := FALSE;
 BenchUut0 : FB_Task;
 BenchUut1 : FB_Task;
 TraceIn_value : ARRAY[0..13] OF DWORD;
 TraceOut_hasChanged : ARRAY[0..13] OF BOOL;
 TraceOut_hasRisingEdges : ARRAY[0..13] OF BOOL;
 TraceOut_risingBits : ARRAY[0..13] OF DWORD;
 TraceOut_noOfRisingBits : ARRAY[0..13] OF USINT;
 TraceOut_hasFallingEdges : ARRAY[0..13] OF BOOL;
 TraceOut_fallingBits : ARRAY[0..13] OF DWORD;
 TraceOut_noOfFallingBits : ARRAY[0..13] OF USINT;
END_VAR

IF NOT BenchDone THEN
 CASE BenchStep OF
 0:
   BenchUut0.value := DWORD#0;
   TraceIn_value[0] := BenchUut0.value;
   BenchUut0();
   TraceOut_hasChanged[0] := BenchUut0.hasChanged;
   TraceOut_hasRisingEdges[0] := BenchUut0.hasRisingEdges;
   TraceOut_risingBits[0] := BenchUut0.risingBits;
   TraceOut_noOfRisingBits[0] := BenchUut0.noOfRisingBits;
   TraceOut_hasFallingEdges[0] := BenchUut0.hasFallingEdges;
   TraceOut_fallingBits[0] := BenchUut0.fallingBits;
   TraceOut_noOfFallingBits[0] := BenchUut0.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 1:
   BenchUut0.value := DWORD#1;
   TraceIn_value[1] := BenchUut0.value;
   BenchUut0();
   TraceOut_hasChanged[1] := BenchUut0.hasChanged;
   TraceOut_hasRisingEdges[1] := BenchUut0.hasRisingEdges;
   TraceOut_risingBits[1] := BenchUut0.risingBits;
   TraceOut_noOfRisingBits[1] := BenchUut0.noOfRisingBits;
   TraceOut_hasFallingEdges[1] := BenchUut0.hasFallingEdges;
   TraceOut_fallingBits[1] := BenchUut0.fallingBits;
   TraceOut_noOfFallingBits[1] := BenchUut0.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 2:
   BenchUut0.value := DWORD#1;
   TraceIn_value[2] := BenchUut0.value;
   BenchUut0();
   TraceOut_hasChanged[2] := BenchUut0.hasChanged;
   TraceOut_hasRisingEdges[2] := BenchUut0.hasRisingEdges;
   TraceOut_risingBits[2] := BenchUut0.risingBits;
   TraceOut_noOfRisingBits[2] := BenchUut0.noOfRisingBits;
   TraceOut_hasFallingEdges[2] := BenchUut0.hasFallingEdges;
   TraceOut_fallingBits[2] := BenchUut0.fallingBits;
   TraceOut_noOfFallingBits[2] := BenchUut0.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 3:
   BenchUut0.value := DWORD#2;
   TraceIn_value[3] := BenchUut0.value;
   BenchUut0();
   TraceOut_hasChanged[3] := BenchUut0.hasChanged;
   TraceOut_hasRisingEdges[3] := BenchUut0.hasRisingEdges;
   TraceOut_risingBits[3] := BenchUut0.risingBits;
   TraceOut_noOfRisingBits[3] := BenchUut0.noOfRisingBits;
   TraceOut_hasFallingEdges[3] := BenchUut0.hasFallingEdges;
   TraceOut_fallingBits[3] := BenchUut0.fallingBits;
   TraceOut_noOfFallingBits[3] := BenchUut0.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 4:
   BenchUut0.value := DWORD#3;
   TraceIn_value[4] := BenchUut0.value;
   BenchUut0();
   TraceOut_hasChanged[4] := BenchUut0.hasChanged;
   TraceOut_hasRisingEdges[4] := BenchUut0.hasRisingEdges;
   TraceOut_risingBits[4] := BenchUut0.risingBits;
   TraceOut_noOfRisingBits[4] := BenchUut0.noOfRisingBits;
   TraceOut_hasFallingEdges[4] := BenchUut0.hasFallingEdges;
   TraceOut_fallingBits[4] := BenchUut0.fallingBits;
   TraceOut_noOfFallingBits[4] := BenchUut0.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 5:
   BenchUut0.value := DWORD#0;
   TraceIn_value[5] := BenchUut0.value;
   BenchUut0();
   TraceOut_hasChanged[5] := BenchUut0.hasChanged;
   TraceOut_hasRisingEdges[5] := BenchUut0.hasRisingEdges;
   TraceOut_risingBits[5] := BenchUut0.risingBits;
   TraceOut_noOfRisingBits[5] := BenchUut0.noOfRisingBits;
   TraceOut_hasFallingEdges[5] := BenchUut0.hasFallingEdges;
   TraceOut_fallingBits[5] := BenchUut0.fallingBits;
   TraceOut_noOfFallingBits[5] := BenchUut0.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 6:
   BenchUut1.value := DWORD#4294967295;
   TraceIn_value[6] := BenchUut1.value;
   BenchUut1();
   TraceOut_hasChanged[6] := BenchUut1.hasChanged;
   TraceOut_hasRisingEdges[6] := BenchUut1.hasRisingEdges;
   TraceOut_risingBits[6] := BenchUut1.risingBits;
   TraceOut_noOfRisingBits[6] := BenchUut1.noOfRisingBits;
   TraceOut_hasFallingEdges[6] := BenchUut1.hasFallingEdges;
   TraceOut_fallingBits[6] := BenchUut1.fallingBits;
   TraceOut_noOfFallingBits[6] := BenchUut1.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 7:
   BenchUut1.value := DWORD#4294967295;
   TraceIn_value[7] := BenchUut1.value;
   BenchUut1();
   TraceOut_hasChanged[7] := BenchUut1.hasChanged;
   TraceOut_hasRisingEdges[7] := BenchUut1.hasRisingEdges;
   TraceOut_risingBits[7] := BenchUut1.risingBits;
   TraceOut_noOfRisingBits[7] := BenchUut1.noOfRisingBits;
   TraceOut_hasFallingEdges[7] := BenchUut1.hasFallingEdges;
   TraceOut_fallingBits[7] := BenchUut1.fallingBits;
   TraceOut_noOfFallingBits[7] := BenchUut1.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 8:
   BenchUut1.value := DWORD#0;
   TraceIn_value[8] := BenchUut1.value;
   BenchUut1();
   TraceOut_hasChanged[8] := BenchUut1.hasChanged;
   TraceOut_hasRisingEdges[8] := BenchUut1.hasRisingEdges;
   TraceOut_risingBits[8] := BenchUut1.risingBits;
   TraceOut_noOfRisingBits[8] := BenchUut1.noOfRisingBits;
   TraceOut_hasFallingEdges[8] := BenchUut1.hasFallingEdges;
   TraceOut_fallingBits[8] := BenchUut1.fallingBits;
   TraceOut_noOfFallingBits[8] := BenchUut1.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 9:
   BenchUut1.value := DWORD#2147483648;
   TraceIn_value[9] := BenchUut1.value;
   BenchUut1();
   TraceOut_hasChanged[9] := BenchUut1.hasChanged;
   TraceOut_hasRisingEdges[9] := BenchUut1.hasRisingEdges;
   TraceOut_risingBits[9] := BenchUut1.risingBits;
   TraceOut_noOfRisingBits[9] := BenchUut1.noOfRisingBits;
   TraceOut_hasFallingEdges[9] := BenchUut1.hasFallingEdges;
   TraceOut_fallingBits[9] := BenchUut1.fallingBits;
   TraceOut_noOfFallingBits[9] := BenchUut1.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 10:
   BenchUut1.value := DWORD#0;
   TraceIn_value[10] := BenchUut1.value;
   BenchUut1();
   TraceOut_hasChanged[10] := BenchUut1.hasChanged;
   TraceOut_hasRisingEdges[10] := BenchUut1.hasRisingEdges;
   TraceOut_risingBits[10] := BenchUut1.risingBits;
   TraceOut_noOfRisingBits[10] := BenchUut1.noOfRisingBits;
   TraceOut_hasFallingEdges[10] := BenchUut1.hasFallingEdges;
   TraceOut_fallingBits[10] := BenchUut1.fallingBits;
   TraceOut_noOfFallingBits[10] := BenchUut1.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 11:
   BenchUut1.value := DWORD#1;
   TraceIn_value[11] := BenchUut1.value;
   BenchUut1();
   TraceOut_hasChanged[11] := BenchUut1.hasChanged;
   TraceOut_hasRisingEdges[11] := BenchUut1.hasRisingEdges;
   TraceOut_risingBits[11] := BenchUut1.risingBits;
   TraceOut_noOfRisingBits[11] := BenchUut1.noOfRisingBits;
   TraceOut_hasFallingEdges[11] := BenchUut1.hasFallingEdges;
   TraceOut_fallingBits[11] := BenchUut1.fallingBits;
   TraceOut_noOfFallingBits[11] := BenchUut1.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 12:
   BenchUut1.value := DWORD#2147483648;
   TraceIn_value[12] := BenchUut1.value;
   BenchUut1();
   TraceOut_hasChanged[12] := BenchUut1.hasChanged;
   TraceOut_hasRisingEdges[12] := BenchUut1.hasRisingEdges;
   TraceOut_risingBits[12] := BenchUut1.risingBits;
   TraceOut_noOfRisingBits[12] := BenchUut1.noOfRisingBits;
   TraceOut_hasFallingEdges[12] := BenchUut1.hasFallingEdges;
   TraceOut_fallingBits[12] := BenchUut1.fallingBits;
   TraceOut_noOfFallingBits[12] := BenchUut1.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 13:
   BenchUut1.value := DWORD#0;
   TraceIn_value[13] := BenchUut1.value;
   BenchUut1();
   TraceOut_hasChanged[13] := BenchUut1.hasChanged;
   TraceOut_hasRisingEdges[13] := BenchUut1.hasRisingEdges;
   TraceOut_risingBits[13] := BenchUut1.risingBits;
   TraceOut_noOfRisingBits[13] := BenchUut1.noOfRisingBits;
   TraceOut_hasFallingEdges[13] := BenchUut1.hasFallingEdges;
   TraceOut_fallingBits[13] := BenchUut1.fallingBits;
   TraceOut_noOfFallingBits[13] := BenchUut1.noOfFallingBits;
   BenchCalls := BenchCalls + 1;
 END_CASE;
 BenchStep := BenchStep + 1;
 IF BenchStep >= 14 THEN BenchDone := TRUE; END_IF;
END_IF;
END_PROGRAM
