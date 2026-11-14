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
    state : E_TaskState := E_TaskState.IDLE;
    startSample : BOOL;
    stopSample : BOOL;
    atExitSample : BOOL;
    jamSample : BOOL;
    resetSample : BOOL;
END_VAR

startSample := Start;
stopSample := Stop;
atExitSample := AtExit;
jamSample := Jam;
resetSample := Reset;

IF jamSample THEN
    state := E_TaskState.FAULT;
ELSIF resetSample THEN
    state := E_TaskState.IDLE;
ELSIF state = E_TaskState.FAULT THEN
    state := E_TaskState.FAULT;
ELSIF stopSample THEN
    state := E_TaskState.IDLE;
ELSIF (state = E_TaskState.MOVING) AND atExitSample THEN
    state := E_TaskState.COMPLETE;
ELSIF (state = E_TaskState.IDLE) AND startSample AND NOT atExitSample THEN
    state := E_TaskState.MOVING;
END_IF;

Belt := (state = E_TaskState.MOVING);
Complete := (state = E_TaskState.COMPLETE);
Fault := (state = E_TaskState.FAULT);
END_FUNCTION_BLOCK
