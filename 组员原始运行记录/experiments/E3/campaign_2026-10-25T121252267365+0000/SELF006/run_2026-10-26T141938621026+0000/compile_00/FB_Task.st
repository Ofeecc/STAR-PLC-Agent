FUNCTION_BLOCK FB_Task
VAR_INPUT
    LowWet : BOOL;
    HighWet : BOOL;
    Inhibit : BOOL;
END_VAR
VAR_OUTPUT
    Fill : BOOL;
    SensorFault : BOOL;
END_VAR
VAR
    qFill : BOOL := FALSE;
END_VAR

SensorFault := HighWet AND NOT LowWet;

IF SensorFault OR Inhibit OR HighWet THEN
    Fill := FALSE;
ELSIF NOT LowWet AND NOT HighWet THEN
    Fill := TRUE;
ELSIF LowWet AND NOT HighWet AND NOT Inhibit THEN
    Fill := qFill;
ELSE
    Fill := FALSE;
END_IF;

qFill := Fill;
END_FUNCTION_BLOCK
