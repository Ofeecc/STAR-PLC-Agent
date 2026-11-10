FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    AtExit : BOOL;
    Jam : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Belt : BOOL := FALSE;
    Complete : BOOL := FALSE;
    Fault : BOOL := FALSE;
END_VAR
VAR
    State : E_TaskState := E_TaskState.IDLE;
END_VAR

IF Jam THEN
    State := E_TaskState.FAULT;
ELSIF Reset THEN
    State := E_TaskState.IDLE;
ELSIF State = E_TaskState.FAULT THEN
    State := E_TaskState.FAULT;
ELSIF Stop THEN
    State := E_TaskState.IDLE;
ELSE
    CASE State OF
        E_TaskState.IDLE:
            IF Start AND NOT AtExit THEN
                State := E_TaskState.MOVING;
            END_IF;

        E_TaskState.MOVING:
            IF AtExit THEN
                State := E_TaskState.COMPLETE;
            END_IF;

        E_TaskState.COMPLETE:
            State := E_TaskState.COMPLETE;

        E_TaskState.FAULT:
            State := E_TaskState.FAULT;
    END_CASE;
END_IF;

Belt := State = E_TaskState.MOVING;
Complete := State = E_TaskState.COMPLETE;
Fault := State = E_TaskState.FAULT;
END_FUNCTION_BLOCK
