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
    state_phase : USINT := 0;
    elapsed_ticks : USINT := 0;
END_VAR

IF NOT Enable THEN
    state_phase := 0;
    elapsed_ticks := 0;
ELSIF Tick THEN
    elapsed_ticks := elapsed_ticks + 1;
    CASE state_phase OF
        0:
            IF elapsed_ticks >= 2 THEN
                state_phase := 1;
                elapsed_ticks := 0;
            END_IF;
        1:
            IF elapsed_ticks >= 3 THEN
                state_phase := 2;
                elapsed_ticks := 0;
            END_IF;
        2:
            IF elapsed_ticks >= 1 THEN
                state_phase := 0;
                elapsed_ticks := 0;
            END_IF;
    END_CASE;
END_IF;
Phase := state_phase;
Red := state_phase = 0;
Green := state_phase = 1;
Amber := state_phase = 2;
END_FUNCTION_BLOCK
