TYPE E_TaskState :
(
    Idle,
    Moving,
    Completed,
    Faulted
);
END_TYPE

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
    state : E_TaskState := E_TaskState.Idle;
END_VAR

IF Jam THEN
    state := E_TaskState.Faulted;
ELSIF Reset THEN
    state := E_TaskState.Idle;
ELSIF state = E_TaskState.Faulted THEN
    ;
ELSIF Stop THEN
    state := E_TaskState.Idle;
ELSIF state = E_TaskState.Moving AND AtExit THEN
    state := E_TaskState.Completed;
ELSIF state = E_TaskState.Idle AND Start AND NOT AtExit THEN
    state := E_TaskState.Moving;
END_IF

Belt := state = E_TaskState.Moving;
Complete := state = E_TaskState.Completed;
Fault := state = E_TaskState.Faulted;
END_FUNCTION_BLOCK
