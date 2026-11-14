FUNCTION_BLOCK FB_Task
VAR_INPUT
    value : DWORD;
END_VAR
VAR_OUTPUT
    hasChanged : BOOL := FALSE;
    hasRisingEdges : BOOL := FALSE;
    risingBits : DWORD := DWORD#0;
    noOfRisingBits : USINT := 0;
    hasFallingEdges : BOOL := FALSE;
    fallingBits : DWORD := DWORD#0;
    noOfFallingBits : USINT := 0;
END_VAR
VAR
    previousValue : DWORD := DWORD#0;
    bitMask : DWORD;
    bitIndex : USINT;
END_VAR

risingBits := value AND NOT previousValue;
fallingBits := previousValue AND NOT value;
hasRisingEdges := risingBits <> DWORD#0;
hasFallingEdges := fallingBits <> DWORD#0;
hasChanged := value <> previousValue;
noOfRisingBits := 0;
noOfFallingBits := 0;
bitMask := DWORD#1;
FOR bitIndex := 0 TO 31 DO
    IF (risingBits AND bitMask) <> DWORD#0 THEN
        noOfRisingBits := noOfRisingBits + 1;
    END_IF;
    IF (fallingBits AND bitMask) <> DWORD#0 THEN
        noOfFallingBits := noOfFallingBits + 1;
    END_IF;
    bitMask := SHL(bitMask, 1);
END_FOR;
previousValue := value;
END_FUNCTION_BLOCK
