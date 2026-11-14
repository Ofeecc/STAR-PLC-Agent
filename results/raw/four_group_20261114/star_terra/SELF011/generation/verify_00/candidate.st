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
    state : INT := 0; // IDLE=0, EXTEND=1, CLAMP=2, RELEASE=3, RETRACT=4, DONE=5
    sampledStart : BOOL;
    sampledStop : BOOL;
    sampledReset : BOOL;
    sampledExtendDone : BOOL;
    sampledClampDone : BOOL;
    sampledReleaseDone : BOOL;
    sampledRetractDone : BOOL;
END_VAR

sampledStart := Start;
sampledStop := Stop;
sampledReset := Reset;
sampledExtendDone := ExtendDone;
sampledClampDone := ClampDone;
sampledReleaseDone := ReleaseDone;
sampledRetractDone := RetractDone;

IF sampledStop OR sampledReset THEN
    state := 0;
ELSE
    CASE state OF
        0:
            IF sampledStart AND sampledRetractDone THEN
                state := 1;
            END_IF;
        1:
            IF sampledExtendDone THEN
                state := 2;
            END_IF;
        2:
            IF sampledClampDone THEN
                state := 3;
            END_IF;
        3:
            IF sampledReleaseDone THEN
                state := 4;
            END_IF;
        4:
            IF sampledRetractDone THEN
                state := 5;
            END_IF;
        5:
            state := 5;
        ELSE
            state := 0;
    END_CASE;
END_IF;

Extend := state = 1;
Clamp := state = 2;
Release := state = 3;
Retract := state = 4;
Busy := Extend OR Clamp OR Release OR Retract;
Done := state = 5;
END_FUNCTION_BLOCK
