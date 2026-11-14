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
    state : E_TransferState := E_TransferState.IDLE;
END_VAR

IF Jam THEN
    state := E_TransferState.FAULT;
ELSIF Reset THEN
    state := E_TransferState.IDLE;
ELSIF state = E_TransferState.FAULT THEN
    state := E_TransferState.FAULT;
ELSIF Stop THEN
    state := E_TransferState.IDLE;
ELSIF (state = E_TransferState.MOVING) AND AtExit THEN
    state := E_TransferState.COMPLETE;
ELSIF (state = E_TransferState.IDLE) AND Start AND NOT AtExit THEN
    state := E_TransferState.MOVING;
END_IF;

Belt := (state = E_TransferState.MOVING);
Complete := (state = E_TransferState.COMPLETE);
Fault := (state = E_TransferState.FAULT);
END_FUNCTION_BLOCK
