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
    nPhase : USINT;
    nElapsed : USINT;
END_VAR

IF NOT Enable THEN
    nPhase := 0;
    nElapsed := 0;
ELSIF Tick THEN
    CASE nPhase OF
        0:
            IF nElapsed + 1 >= 2 THEN
                nPhase := 1;
                nElapsed := 0;
            ELSE
                nElapsed := nElapsed + 1;
            END_IF
        1:
            IF nElapsed + 1 >= 3 THEN
                nPhase := 2;
                nElapsed := 0;
            ELSE
                nElapsed := nElapsed + 1;
            END_IF
        2:
            nPhase := 0;
            nElapsed := 0;
        ELSE
            nPhase := 0;
            nElapsed := 0;
    END_CASE
END_IF

Phase := nPhase;
Red := (nPhase = 0);
Green := (nPhase = 1);
Amber := (nPhase = 2);
END_FUNCTION_BLOCK
