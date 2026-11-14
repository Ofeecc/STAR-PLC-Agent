FUNCTION_BLOCK FB_Task
VAR_INPUT
    LowWet : BOOL;
    HighWet : BOOL;
    Inhibit : BOOL;
END_VAR
VAR_OUTPUT
    Fill : BOOL := FALSE;
    SensorFault : BOOL := FALSE;
END_VAR

SensorFault := HighWet AND NOT LowWet;

IF SensorFault OR Inhibit OR HighWet THEN
    Fill := FALSE;
ELSIF NOT LowWet THEN
    Fill := TRUE;
END_IF
END_FUNCTION_BLOCK
