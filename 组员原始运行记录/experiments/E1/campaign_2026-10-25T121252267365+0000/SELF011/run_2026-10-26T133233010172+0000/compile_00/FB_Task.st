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
    State : E_TaskState := E_TaskState.IDLE;
END_VAR

// Default outputs every scan
Extend := FALSE;
Clamp := FALSE;
Release := FALSE;
Retract := FALSE;
Busy := FALSE;
Done := FALSE;

// Stop and Reset have highest priority and immediately clear the cycle
IF Stop OR Reset THEN
    State := E_TaskState.IDLE;
ELSE
    // Execute exactly one state transition, based on the retained pre-state
    CASE State OF
        E_TaskState.IDLE:
            IF Start AND RetractDone THEN
                State := E_TaskState.EXTEND;
            END_IF

        E_TaskState.EXTEND:
            IF ExtendDone THEN
                State := E_TaskState.CLAMP;
            END_IF

        E_TaskState.CLAMP:
            IF ClampDone THEN
                State := E_TaskState.RELEASE;
            END_IF

        E_TaskState.RELEASE:
            IF ReleaseDone THEN
                State := E_TaskState.RETRACT;
            END_IF

        E_TaskState.RETRACT:
            IF RetractDone THEN
                State := E_TaskState.DONE;
            END_IF

        E_TaskState.DONE:
            ; // Hold completion until Stop or Reset
    END_CASE
END_IF

// Outputs reflect the post-transition state at the end of this scan
CASE State OF
    E_TaskState.EXTEND:
        Extend := TRUE;
        Busy := TRUE;

    E_TaskState.CLAMP:
        Clamp := TRUE;
        Busy := TRUE;

    E_TaskState.RELEASE:
        Release := TRUE;
        Busy := TRUE;

    E_TaskState.RETRACT:
        Retract := TRUE;
        Busy := TRUE;

    E_TaskState.DONE:
        Done := TRUE;
END_CASE
END_FUNCTION_BLOCK
