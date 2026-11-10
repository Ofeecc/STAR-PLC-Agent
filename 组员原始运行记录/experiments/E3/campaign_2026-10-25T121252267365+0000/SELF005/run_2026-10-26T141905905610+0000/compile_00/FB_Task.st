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
    _phase : USINT := 0;
    _elapsed : USINT := 0;
END_VAR

IF NOT Enable THEN
    _phase := 0;
    _elapsed := 0;
ELSIF Tick THEN
    _elapsed := _elapsed + 1;

    CASE _phase OF
        0:
            IF _elapsed >= 2 THEN
                _phase := 1;
                _elapsed := 0;
            END_IF
        1:
            IF _elapsed >= 3 THEN
                _phase := 2;
                _elapsed := 0;
            END_IF
        2:
            IF _elapsed >= 1 THEN
                _phase := 0;
                _elapsed := 0;
            END_IF
        ELSE
            _phase := 0;
            _elapsed := 0;
    END_CASE
END_IF

Phase := _phase;
Red := (_phase = 0);
Green := (_phase = 1);
Amber := (_phase = 2);
END_FUNCTION_BLOCK
