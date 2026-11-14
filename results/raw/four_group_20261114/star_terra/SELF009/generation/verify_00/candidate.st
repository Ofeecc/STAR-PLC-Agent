FUNCTION_BLOCK FB_Task
VAR_INPUT
    PartPulse : BOOL;
    Reset : BOOL;
    Target : USINT;
END_VAR
VAR_OUTPUT
    Count : USINT := 0;
    Complete : BOOL := FALSE;
    {attribute 'analysis' := '-27'}
    Error : BOOL := FALSE;
END_VAR
VAR
    previous_pulse : BOOL := FALSE;
    rising : BOOL;
    nextCount : USINT;
    nextComplete : BOOL;
    nextError : BOOL;
END_VAR

rising := PartPulse AND NOT previous_pulse;
previous_pulse := PartPulse;

IF (Target < USINT#1) OR (Target > USINT#20) THEN
    nextCount := USINT#0;
    nextComplete := FALSE;
    nextError := TRUE;
ELSIF Reset THEN
    nextCount := USINT#0;
    nextComplete := FALSE;
    nextError := FALSE;
ELSE
    nextCount := Count;
    IF rising AND (nextCount < Target) THEN
        nextCount := nextCount + USINT#1;
    END_IF;
    IF nextCount > Target THEN
        nextCount := Target;
    END_IF;
    nextComplete := nextCount >= Target;
    nextError := FALSE;
END_IF;

Count := nextCount;
Complete := nextComplete;
Error := nextError;
END_FUNCTION_BLOCK
