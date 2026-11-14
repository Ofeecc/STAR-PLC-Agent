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
    sampledValue : DWORD;
    i : INT;
END_VAR

sampledValue := value;

risingBits := sampledValue AND NOT previousValue;
fallingBits := previousValue AND NOT sampledValue;

noOfRisingBits := 0;
noOfFallingBits := 0;

FOR i := 0 TO 31 DO
    IF ((risingBits SHR i) AND DWORD#1) <> DWORD#0 THEN
        noOfRisingBits := noOfRisingBits + USINT#1;
    END_IF;
    IF ((fallingBits SHR i) AND DWORD#1) <> DWORD#0 THEN
        noOfFallingBits := noOfFallingBits + USINT#1;
    END_IF;
END_FOR;

hasRisingEdges := (risingBits <> DWORD#0);
hasFallingEdges := (fallingBits <> DWORD#0);
hasChanged := (sampledValue <> previousValue);

previousValue := sampledValue;
END_FUNCTION_BLOCK
