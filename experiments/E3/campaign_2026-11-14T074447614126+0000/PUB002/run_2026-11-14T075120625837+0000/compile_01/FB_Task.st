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
END_VAR

sampledValue := value;

risingBits := sampledValue AND (NOT previousValue);
fallingBits := previousValue AND (NOT sampledValue);

noOfRisingBits := F_PopCount32(bits := risingBits);
noOfFallingBits := F_PopCount32(bits := fallingBits);

hasRisingEdges := (risingBits <> 0);
hasFallingEdges := (fallingBits <> 0);
hasChanged := (sampledValue <> previousValue);

previousValue := sampledValue;
END_FUNCTION_BLOCK
