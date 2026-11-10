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
    prevValue : DWORD := DWORD#0;
    tmpRise : DWORD;
    tmpFall : DWORD;
    i : INT;
END_VAR

risingBits := value AND NOT prevValue;
fallingBits := prevValue AND NOT value;

hasChanged := (value <> prevValue);
hasRisingEdges := (risingBits <> DWORD#0);
hasFallingEdges := (fallingBits <> DWORD#0);

tmpRise := risingBits;
tmpFall := fallingBits;
noOfRisingBits := USINT#0;
noOfFallingBits := USINT#0;

FOR i := 0 TO 31 DO
    IF (tmpRise AND DWORD#1) <> DWORD#0 THEN
        noOfRisingBits := noOfRisingBits + USINT#1;
    END_IF
    IF (tmpFall AND DWORD#1) <> DWORD#0 THEN
        noOfFallingBits := noOfFallingBits + USINT#1;
    END_IF
    tmpRise := SHR(tmpRise, 1);
    tmpFall := SHR(tmpFall, 1);
END_FOR

prevValue := value;
END_FUNCTION_BLOCK
