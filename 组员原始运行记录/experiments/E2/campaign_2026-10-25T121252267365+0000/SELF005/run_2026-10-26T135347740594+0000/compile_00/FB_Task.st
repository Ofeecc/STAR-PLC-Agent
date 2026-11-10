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
    CurrentPhase : USINT := 0;
    ElapsedTicks : USINT := 0;
END_VAR

IF NOT Enable THEN
    CurrentPhase := 0;
    ElapsedTicks := 0;
ELSIF Tick THEN
    ElapsedTicks := ElapsedTicks + 1;
    CASE CurrentPhase OF
        0:
            IF ElapsedTicks >= 2 THEN
                CurrentPhase := 1;
                ElapsedTicks := 0;
            END_IF;
        1:
            IF ElapsedTicks >= 3 THEN
                CurrentPhase := 2;
                ElapsedTicks := 0;
            END_IF;
        2:
            CurrentPhase := 0;
            ElapsedTicks := 0;
        ELSE
            CurrentPhase := 0;
            ElapsedTicks := 0;
    END_CASE;
END_IF;

Phase := CurrentPhase;
Red := CurrentPhase = 0;
Green := CurrentPhase = 1;
Amber := CurrentPhase = 2;
END_FUNCTION_BLOCK
