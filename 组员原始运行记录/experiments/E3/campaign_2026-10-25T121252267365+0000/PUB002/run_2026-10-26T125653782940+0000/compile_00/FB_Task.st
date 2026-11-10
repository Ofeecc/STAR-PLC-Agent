FUNCTION_BLOCK FB_Task
VAR_INPUT
    value : DWORD;
END_VAR
VAR_OUTPUT
    hasChanged : BOOL;
    hasRisingEdges : BOOL;
    risingBits : DWORD;
    noOfRisingBits : USINT;
    hasFallingEdges : BOOL;
    fallingBits : DWORD;
    noOfFallingBits : USINT;
END_VAR
VAR
    previousValue : DWORD := 0;
    tempBits : DWORD;
    i : INT;
END_VAR

hasChanged := value <> previousValue;
risingBits := value AND NOT previousValue;
fallingBits := previousValue AND NOT value;
hasRisingEdges := risingBits <> DWORD#16#00000000;
hasFallingEdges := fallingBits <> DWORD#16#00000000;

noOfRisingBits := 0;
tempBits := risingBits;
FOR i := 0 TO 31 DO
    IF (tempBits AND DWORD#16#00000001) <> DWORD#16#00000000 THEN
        noOfRisingBits := noOfRisingBits + 1;
    END_IF;
    tempBits := SHR(tempBits, 1);
END_FOR;

noOfFallingBits := 0;
tempBits := fallingBits;
FOR i := 0 TO 31 DO
    IF (tempBits AND DWORD#16#00000001) <> DWORD#16#00000000 THEN
        noOfFallingBits := noOfFallingBits + 1;
    END_IF;
    tempBits := SHR(tempBits, 1);
END_FOR;

previousValue := value;
END_FUNCTION_BLOCK
