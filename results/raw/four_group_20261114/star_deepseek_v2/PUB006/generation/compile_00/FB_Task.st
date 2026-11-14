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
    StartDelay : TON;
    State : INT := 0;
    RunPrev : BOOL := FALSE;
    Permit : BOOL := FALSE;
END_VAR

// 1) Sample inputs and retained previous output state
RunPrev := BLOWER_RUN;
Permit := DO_LOW AND AERATION_E_STOP_NC;

// 2) Safety/reset priority and state transitions
IF NOT Permit THEN
    State := 0;
ELSE
    CASE State OF
        0:
            State := 1;
        1:
            IF StartDelay.Q THEN
                State := 2;
            END_IF;
        2:
            State := 2;
    ELSE
        State := 0;
    END_CASE;
END_IF;

// 3) Unconditional top-level TON call outside CASE/IF
StartDelay(IN := (State = 1) AND Permit, PT := T#5s);

// 4) Unified output assignments and cycle counting
BLOWER_RUN := Permit AND ((State = 2) OR ((State = 1) AND StartDelay.Q));

IF (NOT RunPrev) AND BLOWER_RUN THEN
    AERATION_BLOWER_CYCLE_COUNT := AERATION_BLOWER_CYCLE_COUNT + 1;
END_IF;
END_FUNCTION_BLOCK
