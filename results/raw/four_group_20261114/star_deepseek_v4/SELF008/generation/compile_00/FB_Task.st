FUNCTION_BLOCK FB_Task
VAR_INPUT
    Request : BOOL;
    Trip : BOOL;
    Preset : USINT;
END_VAR
VAR_OUTPUT
    Ready : BOOL := FALSE;
    Count : USINT := 0;
END_VAR
VAR
    validPreset : BOOL;
END_VAR

validPreset := (Preset >= 1) AND (Preset <= 5);

IF Trip OR (NOT Request) OR (NOT validPreset) THEN
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
