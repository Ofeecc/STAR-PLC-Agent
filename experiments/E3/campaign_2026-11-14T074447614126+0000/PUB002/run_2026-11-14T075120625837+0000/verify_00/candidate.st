FUNCTION F_PopCount32 : USINT
VAR_INPUT
    bits : DWORD;
END_VAR
VAR
    result : USINT;
END_VAR

result := 0;
IF bits.0 THEN result := result + 1; END_IF;
IF bits.1 THEN result := result + 1; END_IF;
IF bits.2 THEN result := result + 1; END_IF;
IF bits.3 THEN result := result + 1; END_IF;
IF bits.4 THEN result := result + 1; END_IF;
IF bits.5 THEN result := result + 1; END_IF;
IF bits.6 THEN result := result + 1; END_IF;
IF bits.7 THEN result := result + 1; END_IF;
IF bits.8 THEN result := result + 1; END_IF;
IF bits.9 THEN result := result + 1; END_IF;
IF bits.10 THEN result := result + 1; END_IF;
IF bits.11 THEN result := result + 1; END_IF;
IF bits.12 THEN result := result + 1; END_IF;
IF bits.13 THEN result := result + 1; END_IF;
IF bits.14 THEN result := result + 1; END_IF;
IF bits.15 THEN result := result + 1; END_IF;
IF bits.16 THEN result := result + 1; END_IF;
IF bits.17 THEN result := result + 1; END_IF;
IF bits.18 THEN result := result + 1; END_IF;
IF bits.19 THEN result := result + 1; END_IF;
IF bits.20 THEN result := result + 1; END_IF;
IF bits.21 THEN result := result + 1; END_IF;
IF bits.22 THEN result := result + 1; END_IF;
IF bits.23 THEN result := result + 1; END_IF;
IF bits.24 THEN result := result + 1; END_IF;
IF bits.25 THEN result := result + 1; END_IF;
IF bits.26 THEN result := result + 1; END_IF;
IF bits.27 THEN result := result + 1; END_IF;
IF bits.28 THEN result := result + 1; END_IF;
IF bits.29 THEN result := result + 1; END_IF;
IF bits.30 THEN result := result + 1; END_IF;
IF bits.31 THEN result := result + 1; END_IF;
F_PopCount32 := result;
END_FUNCTION

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
