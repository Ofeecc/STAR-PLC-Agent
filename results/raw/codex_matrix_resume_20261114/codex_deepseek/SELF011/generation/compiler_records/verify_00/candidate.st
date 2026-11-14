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
    Extend : BOOL := FALSE;
    Clamp : BOOL := FALSE;
    Release : BOOL := FALSE;
    Retract : BOOL := FALSE;
    Busy : BOOL := FALSE;
    Done : BOOL := FALSE;
END_VAR
VAR
    state : INT := 0;
END_VAR

IF Stop OR Reset THEN
    state := 0;
ELSE
    CASE state OF
        0: IF Start AND RetractDone THEN state := 1; END_IF
        1: IF ExtendDone THEN state := 2; END_IF
        2: IF ClampDone THEN state := 3; END_IF
        3: IF ReleaseDone THEN state := 4; END_IF
        4: IF RetractDone THEN state := 5; END_IF
        5: state := 5;
    ELSE
        state := 0;
    END_CASE
END_IF

Extend := (state = 1);
Clamp := (state = 2);
Release := (state = 3);
Retract := (state = 4);
Busy := (state >= 1) AND (state <= 4);
Done := (state = 5);
END_FUNCTION_BLOCK
