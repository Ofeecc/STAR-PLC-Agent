FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    AtExit : BOOL;
    Jam : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Belt : BOOL;
    Complete : BOOL;
    Fault : BOOL;
END_VAR
VAR
    State : INT := 0; // 0 = IDLE, 1 = MOVING, 2 = COMPLETE, 3 = FAULT
END_VAR

IF Jam THEN
    State := 3;
ELSIF Reset THEN
    State := 0;
ELSIF State = 3 THEN
    State := 3;
ELSIF Stop THEN
    State := 0;
ELSE
    CASE State OF
        0:
            IF Start AND NOT AtExit THEN
                State := 1;
            END_IF;
        1:
            IF AtExit THEN
                State := 2;
            END_IF;
        2:
            State := 2;
    END_CASE;
END_IF;

Belt := State = 1;
Complete := State = 2;
Fault := State = 3;
END_FUNCTION_BLOCK
