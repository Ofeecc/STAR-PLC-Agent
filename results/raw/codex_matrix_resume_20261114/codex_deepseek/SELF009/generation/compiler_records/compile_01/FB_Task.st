FUNCTION_BLOCK FB_Task
VAR_INPUT
    PartPulse : BOOL;
    Reset : BOOL;
    Target : USINT;
END_VAR
VAR_OUTPUT
    Count : USINT := 0;
    Complete : BOOL := FALSE;
    "Error" : BOOL := FALSE;
END_VAR
VAR
    previous_pulse : BOOL := FALSE;
END_VAR

IF (Target < 1) OR (Target > 20) THEN
    "Error" := TRUE;
    Count := 0;
    Complete := FALSE;
ELSIF Reset THEN
    "Error" := FALSE;
    Count := 0;
    Complete := FALSE;
ELSE
    "Error" := FALSE;
    IF PartPulse AND NOT previous_pulse AND (Count < Target) THEN
        Count := Count + 1;
    ELSIF Count > Target THEN
        Count := Target;
    END_IF;
    Complete := (Count >= Target);
END_IF;

previous_pulse := PartPulse;
END_FUNCTION_BLOCK
