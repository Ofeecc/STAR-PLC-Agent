FUNCTION_BLOCK FB_Task
VAR_INPUT
    Enable : BOOL;
    Tick : BOOL;
END_VAR
VAR_OUTPUT
    Red : BOOL := TRUE;
    Green : BOOL := FALSE;
    Amber : BOOL := FALSE;
    Phase : USINT := 0;
END_VAR
VAR
    state : USINT := 0;
    elapsed_ticks : USINT := 0;
END_VAR

IF NOT Enable THEN
    state := 0;
    elapsed_ticks := 0;
ELSIF Tick THEN
    elapsed_ticks := elapsed_ticks + 1;
    IF state = 0 AND elapsed_ticks >= 2 THEN
        state := 1;
        elapsed_ticks := 0;
    ELSIF state = 1 AND elapsed_ticks >= 3 THEN
        state := 2;
        elapsed_ticks := 0;
    ELSIF state = 2 AND elapsed_ticks >= 1 THEN
        state := 0;
        elapsed_ticks := 0;
    END_IF;
END_IF

Phase := state;
Red := (state = 0);
Green := (state = 1);
Amber := (state = 2);
END_FUNCTION_BLOCK
