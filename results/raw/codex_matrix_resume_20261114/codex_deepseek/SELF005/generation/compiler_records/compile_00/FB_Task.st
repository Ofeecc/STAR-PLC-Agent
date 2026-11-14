FUNCTION_BLOCK FB_Task
VAR_INPUT
    Enable : BOOL;
    Tick : BOOL;
END_VAR
VAR_OUTPUT
    Red : BOOL;
    Green : BOOL;
    Amber : BOOL;
    Phase : USINT;
END_VAR
VAR
    phase : USINT := 0;
    elapsed_ticks : USINT := 0;
END_VAR

IF NOT Enable THEN
    phase := 0;
    elapsed_ticks := 0;
ELSIF Tick THEN
    elapsed_ticks := elapsed_ticks + 1;
    IF phase = 0 AND elapsed_ticks >= 2 THEN
        phase := 1;
        elapsed_ticks := 0;
    ELSIF phase = 1 AND elapsed_ticks >= 3 THEN
        phase := 2;
        elapsed_ticks := 0;
    ELSIF phase = 2 AND elapsed_ticks >= 1 THEN
        phase := 0;
        elapsed_ticks := 0;
    END_IF;
END_IF

Phase := phase;
Red := (phase = 0);
Green := (phase = 1);
Amber := (phase = 2);
END_FUNCTION_BLOCK
