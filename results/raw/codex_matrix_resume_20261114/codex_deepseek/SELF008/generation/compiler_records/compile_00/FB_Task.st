FUNCTION_BLOCK FB_Task
VAR_INPUT
    Request : BOOL;
    Trip : BOOL;
    Preset : USINT;
END_VAR
VAR_OUTPUT
    Ready : BOOL;
    Count : USINT;
END_VAR

IF Trip OR NOT Request OR (Preset < 1) OR (Preset > 5) THEN
    Count := 0;
    Ready := FALSE;
ELSE
    IF Count < Preset THEN
        Count := Count + 1;
    ELSE
        Count := Preset;
    END_IF;
    Ready := (Count >= Preset);
END_IF;
END_FUNCTION_BLOCK
