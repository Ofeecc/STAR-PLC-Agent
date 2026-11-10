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
    first : BOOL := TRUE;
    fwdOnly : BOOL;
    revOnly : BOOL;
END_VAR

fwdOnly := ForwardButton AND NOT ReverseButton AND NOT Stop;
revOnly := ReverseButton AND NOT ForwardButton AND NOT Stop;

Forward := FALSE;
Reverse := FALSE;

IF NOT Stop AND NOT (ForwardButton AND ReverseButton) THEN
    IF fwdOnly AND NOT qReverse THEN
        Forward := TRUE;
    ELSIF revOnly AND NOT qForward THEN
        Reverse := TRUE;
    END_IF;
END_IF;

qForward := Forward;
qReverse := Reverse;
first := FALSE;
END_FUNCTION_BLOCK
