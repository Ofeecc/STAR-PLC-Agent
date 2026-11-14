FUNCTION PopCountDword : USINT
VAR_INPUT
    x : DWORD;
END_VAR
VAR
    temp : DWORD;
    count : USINT;
END_VAR

count := 0;
temp := x;
WHILE temp <> DWORD#0 DO
    count := count + 1;
    temp := temp AND (temp - DWORD#1);
END_WHILE;
PopCountDword := count;
END_FUNCTION

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
    sampledValue : DWORD := DWORD#0;
END_VAR

sampledValue := value;

risingBits := sampledValue AND (NOT previousValue);
fallingBits := previousValue AND (NOT sampledValue);

noOfRisingBits := PopCountDword(risingBits);
noOfFallingBits := PopCountDword(fallingBits);

hasRisingEdges := (risingBits <> DWORD#0);
hasFallingEdges := (fallingBits <> DWORD#0);
hasChanged := (sampledValue <> previousValue);

previousValue := sampledValue;
END_FUNCTION_BLOCK
