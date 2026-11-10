FUNCTION_BLOCK FB_Task
VAR_INPUT
    PartPulse : BOOL;
    Reset : BOOL;
    Target : USINT;
END_VAR
VAR_OUTPUT
    Count : USINT := 0;
    Complete : BOOL := FALSE;
    Error : BOOL := FALSE;
END_VAR
VAR
    qPulse : BOOL := FALSE;
    edge : BOOL;
END_VAR

edge := PartPulse AND NOT qPulse;
qPulse := PartPulse;

IF (Target < 1) OR (Target > 20) THEN
    Error := TRUE;
    Count := 0;
    Complete := FALSE;
ELSIF Reset THEN
    Error := FALSE;
    Count := 0;
    Complete := FALSE;
ELSE
    Error := FALSE;
    IF Count > Target THEN
        Count := Target;
    END_IF;
    IF edge AND (Count < Target) THEN
        Count := Count + 1;
    END_IF;
    Complete := (Count >= Target);
END_IF;
END_FUNCTION_BLOCK
