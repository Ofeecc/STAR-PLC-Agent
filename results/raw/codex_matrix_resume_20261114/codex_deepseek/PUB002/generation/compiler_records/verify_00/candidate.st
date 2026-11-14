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
    risingWork : DWORD;
    fallingWork : DWORD;
    risingCount : USINT;
    fallingCount : USINT;
    bitIndex : USINT;
END_VAR

risingBits := value AND NOT previousValue;
fallingBits := previousValue AND NOT value;

hasChanged := value <> previousValue;
hasRisingEdges := risingBits <> DWORD#0;
hasFallingEdges := fallingBits <> DWORD#0;

risingWork := risingBits;
fallingWork := fallingBits;
risingCount := 0;
fallingCount := 0;

FOR bitIndex := 0 TO 31 DO
    IF (risingWork AND DWORD#1) <> DWORD#0 THEN
        risingCount := risingCount + USINT#1;
    END_IF
    IF (fallingWork AND DWORD#1) <> DWORD#0 THEN
        fallingCount := fallingCount + USINT#1;
    END_IF
    risingWork := SHR(risingWork, 1);
    fallingWork := SHR(fallingWork, 1);
END_FOR

noOfRisingBits := risingCount;
noOfFallingBits := fallingCount;
previousValue := value;
END_FUNCTION_BLOCK
