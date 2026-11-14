FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    EStopNC : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Run : BOOL := FALSE;
    ResetRequired : BOOL := TRUE;
END_VAR
VAR
    state : USINT := 0; // 0: inhibited, 1: ready, 2: running
    nextState : USINT;
    sampledStart : BOOL;
    sampledStop : BOOL;
    sampledEStopNC : BOOL;
    sampledReset : BOOL;
END_VAR

sampledStart := Start;
sampledStop := Stop;
sampledEStopNC := EStopNC;
sampledReset := Reset;

nextState := state;
IF NOT sampledEStopNC THEN
    nextState := 0;
ELSE
    CASE state OF
        0:
            IF sampledReset AND NOT sampledStart AND NOT sampledStop THEN
                nextState := 1;
            END_IF;
        1:
            IF sampledStop THEN
                nextState := 1;
            ELSIF sampledStart THEN
                nextState := 2;
            END_IF;
        2:
            IF sampledStop THEN
                nextState := 1;
            END_IF;
        ELSE
            nextState := 0;
    END_CASE;
END_IF;

state := nextState;
Run := (state = 2);
ResetRequired := (state = 0);
END_FUNCTION_BLOCK
