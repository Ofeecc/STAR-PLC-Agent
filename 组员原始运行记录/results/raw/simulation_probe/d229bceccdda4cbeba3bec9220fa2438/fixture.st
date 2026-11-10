FUNCTION_BLOCK FB_Task
VAR_INPUT
 x : BOOL;
END_VAR
VAR_OUTPUT
 y : BOOL;
END_VAR
y := x;
END_FUNCTION_BLOCK

PROGRAM PLC_PRG
VAR
 uut : FB_Task;
 TestInput : BOOL := FALSE;
 TestOutput : BOOL := FALSE;
 RequestSeq : UDINT := 0;
 AckSeq : UDINT := 0;
 CallCount : UDINT := 0;
END_VAR
IF RequestSeq <> AckSeq THEN
 uut(x := TestInput);
 TestOutput := uut.y;
 CallCount := CallCount + 1;
 AckSeq := RequestSeq;
END_IF;
END_PROGRAM
