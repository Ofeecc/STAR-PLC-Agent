FUNCTION_BLOCK FB_Task
VAR_INPUT
    value : DWORD;
END_VAR
VAR_OUTPUT
    hasChanged : BOOL := FALSE;
    hasRisingEdges : BOOL := FALSE;
    risingBits : DWORD := DWORD#0;
    noOfRisingBits : USINT := USINT#0;
    hasFallingEdges : BOOL := FALSE;
    fallingBits : DWORD := DWORD#0;
    noOfFallingBits : USINT := USINT#0;
END_VAR
VAR
    previousValue : DWORD := DWORD#0;
    sampledValue : DWORD;
    risingMask : DWORD;
    fallingMask : DWORD;
    risingWork : DWORD;
    fallingWork : DWORD;
    bitIndex : INT;
END_VAR

sampledValue := value;
risingMask := sampledValue AND NOT previousValue;
fallingMask := previousValue AND NOT sampledValue;
previousValue := sampledValue;

risingBits := risingMask;
fallingBits := fallingMask;
hasRisingEdges := risingMask <> DWORD#0;
hasFallingEdges := fallingMask <> DWORD#0;
hasChanged := hasRisingEdges OR hasFallingEdges;

noOfRisingBits := USINT#0;
noOfFallingBits := USINT#0;
risingWork := risingMask;
fallingWork := fallingMask;
FOR bitIndex := 0 TO 31 DO
    IF (risingWork AND DWORD#1) <> DWORD#0 THEN
        noOfRisingBits := noOfRisingBits + USINT#1;
    END_IF;
    IF (fallingWork AND DWORD#1) <> DWORD#0 THEN
        noOfFallingBits := noOfFallingBits + USINT#1;
    END_IF;
    risingWork := SHR(risingWork, 1);
    fallingWork := SHR(fallingWork, 1);
END_FOR;
END_FUNCTION_BLOCK
