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
    state : E_TaskState := E_TaskState.IDLE;
END_VAR

IF Jam THEN
    state := E_TaskState.FAULT;
ELSIF Reset THEN
    state := E_TaskState.IDLE;
ELSIF state = E_TaskState.FAULT THEN
    state := E_TaskState.FAULT;
ELSIF Stop THEN
    state := E_TaskState.IDLE;
ELSE
    CASE state OF
        E_TaskState.IDLE:
            IF Start AND NOT AtExit THEN
                state := E_TaskState.MOVING;
            END_IF;
        E_TaskState.MOVING:
            IF AtExit THEN
                state := E_TaskState.COMPLETE;
            END_IF;
        E_TaskState.COMPLETE:
            ;
        E_TaskState.FAULT:
            ;
    END_CASE;
END_IF;

Belt := (state = E_TaskState.MOVING);
Complete := (state = E_TaskState.COMPLETE);
Fault := (state = E_TaskState.FAULT);
END_FUNCTION_BLOCK
