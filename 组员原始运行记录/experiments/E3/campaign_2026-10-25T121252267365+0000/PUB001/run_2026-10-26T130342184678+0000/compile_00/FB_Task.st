FUNCTION_BLOCK FB_Task
VAR_INPUT
    bottleSensor : BOOL;
    cleaningConfirmButton : BOOL;
    fillingConfirmButton : BOOL;
    cappingConfirmButton : BOOL;
    packingConfirmButton : BOOL;
    finishedButton : BOOL;
END_VAR
VAR_OUTPUT
    Pump_Motor : BOOL;
    Filling_Valve : BOOL;
    Capping_Machine : BOOL;
    Packing_Machine : BOOL;
    Completion_Light : BOOL;
END_VAR
VAR
    phase : INT := 0;
END_VAR

Pump_Motor := FALSE;
Filling_Valve := FALSE;
Capping_Machine := FALSE;
Packing_Machine := FALSE;
Completion_Light := FALSE;

CASE phase OF
0:
    IF bottleSensor THEN
        Pump_Motor := TRUE;
        phase := 1;
    END_IF;
1:
    IF cleaningConfirmButton THEN
        Filling_Valve := TRUE;
        phase := 2;
    ELSE
        Pump_Motor := TRUE;
    END_IF;
2:
    IF fillingConfirmButton THEN
        Capping_Machine := TRUE;
        phase := 3;
    ELSE
        Filling_Valve := TRUE;
    END_IF;
3:
    IF cappingConfirmButton THEN
        Packing_Machine := TRUE;
        phase := 4;
    ELSE
        Capping_Machine := TRUE;
    END_IF;
4:
    IF packingConfirmButton THEN
        Completion_Light := TRUE;
        phase := 5;
    ELSE
        Packing_Machine := TRUE;
    END_IF;
5:
    IF finishedButton THEN
        phase := 0;
    ELSE
        Completion_Light := TRUE;
    END_IF;
ELSE
    phase := 0;
END_CASE;
END_FUNCTION_BLOCK
