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
    PhaseState : USINT := 0;
    ElapsedTicks : USINT := 0;
END_VAR

IF NOT Enable THEN
    PhaseState := 0;
    ElapsedTicks := 0;
ELSIF Tick THEN
    ElapsedTicks := ElapsedTicks + 1;

    CASE PhaseState OF
        0:
            IF ElapsedTicks >= 2 THEN
                PhaseState := 1;
                ElapsedTicks := 0;
            END_IF;
        1:
            IF ElapsedTicks >= 3 THEN
                PhaseState := 2;
                ElapsedTicks := 0;
            END_IF;
        2:
            IF ElapsedTicks >= 1 THEN
                PhaseState := 0;
                ElapsedTicks := 0;
            END_IF;
    ELSE
        PhaseState := 0;
        ElapsedTicks := 0;
    END_CASE;
END_IF;

Phase := PhaseState;
Red := PhaseState = 0;
Green := PhaseState = 1;
Amber := PhaseState = 2;
END_FUNCTION_BLOCK
