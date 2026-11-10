FUNCTION_BLOCK FB_Task
VAR_INPUT
    PartPulse : BOOL;
    Reset : BOOL;
    Target : USINT;
END_VAR
VAR_OUTPUT
    Count : USINT;
    Complete : BOOL;
    Error : BOOL;
END_VAR
VAR
    PreviousPulse : BOOL := FALSE;
END_VAR

Error := (Target < 1) OR (Target > 20);

IF Error OR Reset THEN
    Count := 0;
    Complete := FALSE;
ELSE
    IF PartPulse AND NOT PreviousPulse THEN
        IF Count < Target THEN
            Count := Count + 1;
        END_IF;
    END_IF;
    Complete := Count >= Target;
END_IF;

PreviousPulse := PartPulse;
END_FUNCTION_BLOCK
