TYPE E_TransferState :
(
    ST_IDLE := 0,
    ST_MOVING := 1,
    ST_COMPLETE := 2,
    ST_FAULT := 3
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
    state : E_TransferState := E_TransferState.ST_IDLE;
END_VAR

IF Jam THEN
    state := E_TransferState.ST_FAULT;
ELSIF Reset THEN
    state := E_TransferState.ST_IDLE;
ELSIF state = E_TransferState.ST_FAULT THEN
    state := E_TransferState.ST_FAULT;
ELSIF Stop THEN
    state := E_TransferState.ST_IDLE;
ELSIF (state = E_TransferState.ST_MOVING) AND AtExit THEN
    state := E_TransferState.ST_COMPLETE;
ELSIF (state = E_TransferState.ST_IDLE) AND Start AND NOT AtExit THEN
    state := E_TransferState.ST_MOVING;
END_IF;

Belt := (state = E_TransferState.ST_MOVING);
Complete := (state = E_TransferState.ST_COMPLETE);
Fault := (state = E_TransferState.ST_FAULT);
END_FUNCTION_BLOCK
