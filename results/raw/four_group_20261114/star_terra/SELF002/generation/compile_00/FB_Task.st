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
    output_direction : INT := 0;
    sampledForwardButton : BOOL := FALSE;
    sampledReverseButton : BOOL := FALSE;
    sampledStop : BOOL := FALSE;
END_VAR

sampledForwardButton := ForwardButton;
sampledReverseButton := ReverseButton;
sampledStop := Stop;

IF sampledStop OR (sampledForwardButton = sampledReverseButton) THEN
    desired_direction := 0;
ELSIF sampledForwardButton THEN
    desired_direction := 1;
ELSE
    desired_direction := -1;
END_IF;

IF ((desired_direction = 1) AND (previous_direction = -1)) OR
   ((desired_direction = -1) AND (previous_direction = 1)) THEN
    output_direction := 0;
ELSE
    output_direction := desired_direction;
END_IF;

previous_direction := output_direction;
Forward := (output_direction = 1);
Reverse := (output_direction = -1);
END_FUNCTION_BLOCK
