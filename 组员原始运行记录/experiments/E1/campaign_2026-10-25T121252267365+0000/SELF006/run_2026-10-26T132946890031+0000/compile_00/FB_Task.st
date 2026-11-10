FUNCTION_BLOCK FB_Task
VAR_INPUT
    LowWet : BOOL;
    HighWet : BOOL;
    Inhibit : BOOL;
END_VAR
VAR_OUTPUT
    Fill : BOOL := FALSE;
    SensorFault : BOOL;
END_VAR
VAR
    qFill : BOOL := FALSE;
END_VAR

SensorFault := HighWet AND NOT LowWet;

IF SensorFault OR Inhibit OR HighWet THEN
    Fill := FALSE;
ELSIF NOT LowWet THEN
    Fill := TRUE;
ELSE
    Fill := qFill;
END_IF

qFill := Fill;
END_FUNCTION_BLOCK
