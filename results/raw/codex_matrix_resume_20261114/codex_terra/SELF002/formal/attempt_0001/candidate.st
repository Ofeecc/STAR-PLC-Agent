FUNCTION_BLOCK FB_Task
VAR_INPUT
    ForwardButton : BOOL;
    ReverseButton : BOOL;
    Stop : BOOL;
END_VAR
VAR_OUTPUT
    Forward : BOOL := FALSE;
    Reverse : BOOL := FALSE;
END_VAR
VAR
    previous_direction : INT := 0;
    desired_direction : INT := 0;
END_VAR

IF Stop OR (ForwardButton = ReverseButton) THEN
    desired_direction := 0;
ELSIF ForwardButton THEN
    desired_direction := 1;
ELSE
    desired_direction := -1;
END_IF;

IF ((desired_direction = 1) AND (previous_direction = -1)) OR
   ((desired_direction = -1) AND (previous_direction = 1)) THEN
    desired_direction := 0;
END_IF;

Forward := (desired_direction = 1);
Reverse := (desired_direction = -1);
previous_direction := desired_direction;
END_FUNCTION_BLOCK
