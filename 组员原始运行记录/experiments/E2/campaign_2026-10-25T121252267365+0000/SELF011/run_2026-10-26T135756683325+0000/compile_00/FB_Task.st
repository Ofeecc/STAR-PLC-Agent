FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    Reset : BOOL;
    ExtendDone : BOOL;
    ClampDone : BOOL;
    ReleaseDone : BOOL;
    RetractDone : BOOL;
END_VAR
VAR_OUTPUT
    Extend : BOOL;
    Clamp : BOOL;
    Release : BOOL;
    Retract : BOOL;
    Busy : BOOL;
    Done : BOOL;
END_VAR
VAR
    State : INT := 0;
END_VAR

IF Stop OR Reset THEN
    State := 0;
ELSE
    CASE State OF
        0:
            IF Start AND RetractDone THEN
                State := 1;
            END_IF;
        1:
            IF ExtendDone THEN
                State := 2;
            END_IF;
        2:
            IF ClampDone THEN
                State := 3;
            END_IF;
        3:
            IF ReleaseDone THEN
                State := 4;
            END_IF;
        4:
            IF RetractDone THEN
                State := 5;
            END_IF;
        5:
            State := 5;
    ELSE
        State := 0;
    END_CASE;
END_IF;

Extend := State = 1;
Clamp := State = 2;
Release := State = 3;
Retract := State = 4;
Busy := (State >= 1) AND (State <= 4);
Done := State = 5;
END_FUNCTION_BLOCK
