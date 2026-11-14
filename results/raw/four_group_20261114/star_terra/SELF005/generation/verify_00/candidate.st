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
    phaseState : USINT := 0;
    elapsed_ticks : USINT := 0;
    enableSample : BOOL;
    tickSample : BOOL;
END_VAR

enableSample := Enable;
tickSample := Tick;

IF NOT enableSample THEN
    phaseState := 0;
    elapsed_ticks := 0;
ELSIF tickSample THEN
    elapsed_ticks := elapsed_ticks + 1;
    CASE phaseState OF
        0:
            IF elapsed_ticks >= 2 THEN
                phaseState := 1;
                elapsed_ticks := 0;
            END_IF;
        1:
            IF elapsed_ticks >= 3 THEN
                phaseState := 2;
                elapsed_ticks := 0;
            END_IF;
        2:
            IF elapsed_ticks >= 1 THEN
                phaseState := 0;
                elapsed_ticks := 0;
            END_IF;
    END_CASE;
END_IF;

Phase := phaseState;
Red := (phaseState = 0);
Green := (phaseState = 1);
Amber := (phaseState = 2);
END_FUNCTION_BLOCK
