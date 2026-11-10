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
    qPulse : BOOL := FALSE;
END_VAR

// Exact target validation
Error := (Target < 1) OR (Target > 20);

// Safety priority: invalid target or reset clears the batch
IF Error OR Reset THEN
    Count := 0;
    Complete := FALSE;
ELSE
    // Count only FALSE-to-TRUE transitions, saturating at Target
    IF PartPulse AND NOT qPulse THEN
        IF Count < Target THEN
            Count := Count + 1;
        END_IF;
    END_IF;
    // Complete reports the post-scan count; higher target clears it
    IF Count >= Target THEN
        Complete := TRUE;
    ELSE
        Complete := FALSE;
    END_IF;
END_IF;

// Edge memory samples the pulse on every scan, including reset/invalid scans
qPulse := PartPulse;
END_FUNCTION_BLOCK
