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
    state : E_FbTaskState := E_FbTaskState.eIDLE;
    iStart : BOOL;
    iStop : BOOL;
    iReset : BOOL;
    iExtendDone : BOOL;
    iClampDone : BOOL;
    iReleaseDone : BOOL;
    iRetractDone : BOOL;
END_VAR

// Stage 1: sample each input once per scan
    iStart := Start;
    iStop := Stop;
    iReset := Reset;
    iExtendDone := ExtendDone;
    iClampDone := ClampDone;
    iReleaseDone := ReleaseDone;
    iRetractDone := RetractDone;

    // Stage 2: safety/reset priority; exactly one normal transition per scan
    IF iStop OR iReset THEN
        state := E_FbTaskState.eIDLE;
    ELSE
        CASE state OF
            E_FbTaskState.eIDLE:
                IF iStart AND iRetractDone THEN
                    state := E_FbTaskState.eEXTEND;
                END_IF;

            E_FbTaskState.eEXTEND:
                IF iExtendDone THEN
                    state := E_FbTaskState.eCLAMP;
                END_IF;

            E_FbTaskState.eCLAMP:
                IF iClampDone THEN
                    state := E_FbTaskState.eRELEASE;
                END_IF;

            E_FbTaskState.eRELEASE:
                IF iReleaseDone THEN
                    state := E_FbTaskState.eRETRACT;
                END_IF;

            E_FbTaskState.eRETRACT:
                IF iRetractDone THEN
                    state := E_FbTaskState.eDONE;
                END_IF;

            E_FbTaskState.eDONE:
                state := E_FbTaskState.eDONE; // hold DONE until Stop or Reset

            ELSE
                state := E_FbTaskState.eIDLE;
        END_CASE;
    END_IF;

    // Stage 3: no timers required; no unconditional timer FB calls exist

    // Stage 4: unified output assignments from scan-final state
    Extend := (state = E_FbTaskState.eEXTEND);
    Clamp := (state = E_FbTaskState.eCLAMP);
    Release := (state = E_FbTaskState.eRELEASE);
    Retract := (state = E_FbTaskState.eRETRACT);
    Busy := (state = E_FbTaskState.eEXTEND) OR (state = E_FbTaskState.eCLAMP) OR (state = E_FbTaskState.eRELEASE) OR (state = E_FbTaskState.eRETRACT);
    Done := (state = E_FbTaskState.eDONE);
END_FUNCTION_BLOCK
