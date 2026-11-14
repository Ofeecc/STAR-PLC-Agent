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
    rise : BOOL := FALSE;
    invalidTarget : BOOL := FALSE;
    nextCount : USINT := 0;
    nextComplete : BOOL := FALSE;
    nextError : BOOL := FALSE;
END_VAR

rise := PartPulse AND NOT previous_pulse;
previous_pulse := PartPulse;

invalidTarget := (Target < 1) OR (Target > 20);

IF invalidTarget THEN
    nextCount := 0;
    nextComplete := FALSE;
    nextError := TRUE;
ELSIF Reset THEN
    nextCount := 0;
    nextComplete := FALSE;
    nextError := FALSE;
ELSE
    nextCount := Count;
    IF rise THEN
        IF nextCount < Target THEN
            nextCount := nextCount + 1;
        ELSE
            nextCount := Target;
        END_IF;
    ELSE
        IF nextCount > Target THEN
            nextCount := Target;
        END_IF;
    END_IF;
    nextComplete := (nextCount >= Target);
    nextError := FALSE;
END_IF;

Count := nextCount;
Complete := nextComplete;
Error := nextError;
END_FUNCTION_BLOCK
