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
    state : E_State := E_State.IDLE;
END_VAR

IF Jam THEN
    state := E_State.FAULT;
ELSIF Reset THEN
    state := E_State.IDLE;
ELSIF state = E_State.FAULT THEN
    ;
ELSIF Stop THEN
    state := E_State.IDLE;
ELSIF state = E_State.MOVING AND AtExit THEN
    state := E_State.COMPLETE;
ELSIF state = E_State.IDLE AND Start AND NOT AtExit THEN
    state := E_State.MOVING;
END_IF

Belt := state = E_State.MOVING;
Complete := state = E_State.COMPLETE;
Fault := state = E_State.FAULT;
END_FUNCTION_BLOCK
