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
    qForward : BOOL := FALSE;
    qReverse : BOOL := FALSE;
END_VAR

IF Stop OR (ForwardButton AND ReverseButton) OR (NOT ForwardButton AND NOT ReverseButton) THEN
    Forward := FALSE;
    Reverse := FALSE;
ELSIF ForwardButton THEN
    IF qReverse THEN
        Forward := FALSE;
        Reverse := FALSE;
    ELSE
        Forward := TRUE;
        Reverse := FALSE;
    END_IF;
ELSE
    IF qForward THEN
        Forward := FALSE;
        Reverse := FALSE;
    ELSE
        Forward := FALSE;
        Reverse := TRUE;
    END_IF;
END_IF;

qForward := Forward;
qReverse := Reverse;
END_FUNCTION_BLOCK
