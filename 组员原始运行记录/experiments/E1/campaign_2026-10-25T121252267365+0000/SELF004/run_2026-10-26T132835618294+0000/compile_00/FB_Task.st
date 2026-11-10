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
    State : E_TaskState := E_TaskState.eIdle;
END_VAR

IF Jam THEN
    State := E_TaskState.eFault;
ELSIF Reset THEN
    State := E_TaskState.eIdle;
ELSE
    CASE State OF
        E_TaskState.eIdle:
            IF Start AND NOT AtExit THEN
                State := E_TaskState.eMoving;
            END_IF

        E_TaskState.eMoving:
            IF Stop THEN
                State := E_TaskState.eIdle;
            ELSIF AtExit THEN
                State := E_TaskState.eComplete;
            END_IF

        E_TaskState.eComplete:
            IF Stop THEN
                State := E_TaskState.eIdle;
            END_IF

        E_TaskState.eFault:
            ;
    END_CASE
END_IF

Belt := (State = E_TaskState.eMoving);
Complete := (State = E_TaskState.eComplete);
Fault := (State = E_TaskState.eFault);
END_FUNCTION_BLOCK
