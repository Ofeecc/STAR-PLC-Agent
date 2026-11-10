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
    previousValue : DWORD := DWORD#0;
    risingWork : DWORD;
    fallingWork : DWORD;
END_VAR

risingBits := value AND NOT previousValue;
fallingBits := previousValue AND NOT value;

hasChanged := value <> previousValue;
hasRisingEdges := risingBits <> DWORD#0;
hasFallingEdges := fallingBits <> DWORD#0;

noOfRisingBits := USINT#0;
risingWork := risingBits;
WHILE risingWork <> DWORD#0 DO
    IF (risingWork AND DWORD#1) <> DWORD#0 THEN
        noOfRisingBits := noOfRisingBits + USINT#1;
    END_IF;
    risingWork := SHR(risingWork, 1);
END_WHILE;

noOfFallingBits := USINT#0;
fallingWork := fallingBits;
WHILE fallingWork <> DWORD#0 DO
    IF (fallingWork AND DWORD#1) <> DWORD#0 THEN
        noOfFallingBits := noOfFallingBits + USINT#1;
    END_IF;
    fallingWork := SHR(fallingWork, 1);
END_WHILE;

previousValue := value;
END_FUNCTION_BLOCK
