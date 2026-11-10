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

IF Stop OR Reset THEN
    State := E_TaskState.IDLE;
ELSE
    CASE State OF
        E_TaskState.IDLE:
            IF Start AND RetractDone THEN
                State := E_TaskState.EXTEND;
            END_IF;
        E_TaskState.EXTEND:
            IF ExtendDone THEN
                State := E_TaskState.CLAMP;
            END_IF;
        E_TaskState.CLAMP:
            IF ClampDone THEN
                State := E_TaskState.RELEASE;
            END_IF;
        E_TaskState.RELEASE:
            IF ReleaseDone THEN
                State := E_TaskState.RETRACT;
            END_IF;
        E_TaskState.RETRACT:
            IF RetractDone THEN
                State := E_TaskState.DONE;
            END_IF;
    END_CASE;
END_IF;

Extend := (State = E_TaskState.EXTEND);
Clamp := (State = E_TaskState.CLAMP);
Release := (State = E_TaskState.RELEASE);
Retract := (State = E_TaskState.RETRACT);
Busy := Extend OR Clamp OR Release OR Retract;
Done := (State = E_TaskState.DONE);
END_FUNCTION_BLOCK
