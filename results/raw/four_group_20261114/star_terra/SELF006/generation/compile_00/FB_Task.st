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
VAR
    LowWet_s : BOOL := FALSE;
    HighWet_s : BOOL := FALSE;
    Inhibit_s : BOOL := FALSE;
    SensorFaultCalc : BOOL := FALSE;
    FillingState : BOOL := FALSE;
END_VAR

LowWet_s := LowWet;
HighWet_s := HighWet;
Inhibit_s := Inhibit;

SensorFaultCalc := HighWet_s AND NOT LowWet_s;

IF SensorFaultCalc OR Inhibit_s OR HighWet_s THEN
    FillingState := FALSE;
ELSIF NOT LowWet_s THEN
    FillingState := TRUE;
END_IF;

Fill := FillingState;
SensorFault := SensorFaultCalc;
END_FUNCTION_BLOCK
