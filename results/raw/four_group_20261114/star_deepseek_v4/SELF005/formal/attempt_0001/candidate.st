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
    internalPhase : USINT := 0;
    age : USINT := 0;
END_VAR

IF NOT Enable THEN
    internalPhase := 0;
    age := 0;
ELSIF Tick THEN
    CASE internalPhase OF
        0:
            age := age + 1;
            IF age >= 2 THEN
                internalPhase := 1;
                age := 0;
            END_IF;
        1:
            age := age + 1;
            IF age >= 3 THEN
                internalPhase := 2;
                age := 0;
            END_IF;
        2:
            age := age + 1;
            IF age >= 1 THEN
                internalPhase := 0;
                age := 0;
            END_IF;
        ELSE
            internalPhase := 0;
            age := 0;
    END_CASE;
END_IF;

Phase := internalPhase;
Red := (internalPhase = 0);
Green := (internalPhase = 1);
Amber := (internalPhase = 2);
END_FUNCTION_BLOCK
