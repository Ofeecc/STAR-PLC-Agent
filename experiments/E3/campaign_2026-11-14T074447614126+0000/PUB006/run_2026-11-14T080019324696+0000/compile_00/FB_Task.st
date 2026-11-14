FUNCTION_BLOCK FB_Task
VAR_INPUT
    DO_LOW : BOOL;
    AERATION_E_STOP_NC : BOOL;
END_VAR
VAR_OUTPUT
    BLOWER_RUN : BOOL := FALSE;
    AERATION_BLOWER_CYCLE_COUNT : UINT := 0;
END_VAR
VAR
    StartDelayTON : TON;
    state : INT := 0;
    permit : BOOL := FALSE;
    runPrev : BOOL := FALSE;
    runCmd : BOOL := FALSE;
    cycleCount : UINT := 0;
END_VAR

// Stage 1: sample inputs and previous observed output
runPrev := BLOWER_RUN;
permit := DO_LOW AND AERATION_E_STOP_NC;

// Stage 2: safety/reset priority and state transitions
IF NOT permit THEN
    state := 0;
    runCmd := FALSE;
ELSE
    CASE state OF
        0: // IDLE -> DELAY
            state := 1;
        1: // DELAY -> RUN when delay is already elapsed
            IF StartDelayTON.Q THEN
                state := 2;
            END_IF;
        2: // RUN hold
            state := 2;
        ELSE
            state := 0;
    END_CASE;
END_IF;

// Stage 3: unconditional top-level timer call
StartDelayTON(IN := permit, PT := T#5s);

// Stage 4: unified output assignments
IF NOT permit THEN
    runCmd := FALSE;
ELSE
    runCmd := (state = 2) OR ((state = 1) AND StartDelayTON.Q);
END_IF;

IF runCmd AND NOT runPrev THEN
    cycleCount := cycleCount + UINT#1;
END_IF;

BLOWER_RUN := runCmd;
AERATION_BLOWER_CYCLE_COUNT := cycleCount;
END_FUNCTION_BLOCK
