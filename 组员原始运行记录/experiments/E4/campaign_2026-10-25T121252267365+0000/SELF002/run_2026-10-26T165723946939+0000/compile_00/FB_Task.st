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
    qForward : BOOL := FALSE;
    qReverse : BOOL := FALSE;
END_VAR

Forward := FALSE;
Reverse := FALSE;

IF NOT Stop THEN
    IF ForwardButton AND NOT ReverseButton THEN
        IF NOT qReverse THEN
            Forward := TRUE;
        END_IF;
    ELSIF ReverseButton AND NOT ForwardButton THEN
        IF NOT qForward THEN
            Reverse := TRUE;
        END_IF;
    END_IF;
END_IF;

qForward := Forward;
qReverse := Reverse;
END_FUNCTION_BLOCK
