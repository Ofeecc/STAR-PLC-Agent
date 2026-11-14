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
    state : INT := 0;
END_VAR

IF Jam THEN
    state := 3;
ELSIF Reset THEN
    state := 0;
ELSIF state = 3 THEN
    state := 3;
ELSIF Stop THEN
    state := 0;
ELSIF (state = 1) AND AtExit THEN
    state := 2;
ELSIF (state = 0) AND Start AND NOT AtExit THEN
    state := 1;
END_IF;

Belt := state = 1;
Complete := state = 2;
Fault := state = 3;
END_FUNCTION_BLOCK
