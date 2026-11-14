FUNCTION_BLOCK FB_Task
VAR_INPUT
    ForwardButton : BOOL;
    ReverseButton : BOOL;
    Stop : BOOL;
END_VAR
VAR_OUTPUT
    Forward : BOOL;
    Reverse : BOOL;
END_VAR
VAR
    previous_direction : INT;
    dir : INT;
END_VAR

IF Stop OR (ForwardButton = ReverseButton) THEN
    dir := 0;
ELSIF ForwardButton THEN
    dir := 1;
ELSIF ReverseButton THEN
    dir := -1;
ELSE
    dir := 0;
END_IF;

IF (dir <> 0) AND (previous_direction <> 0) AND (dir <> previous_direction) THEN
    Forward := FALSE;
    Reverse := FALSE;
    previous_direction := 0;
ELSE
    Forward := (dir = 1);
    Reverse := (dir = -1);
    previous_direction := dir;
END_IF;
END_FUNCTION_BLOCK
