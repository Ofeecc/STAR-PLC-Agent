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
