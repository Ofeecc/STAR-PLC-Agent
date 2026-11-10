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
    Pump_Motor : BOOL := FALSE;
    Filling_Valve : BOOL := FALSE;
    Capping_Machine : BOOL := FALSE;
    Packing_Machine : BOOL := FALSE;
    Completion_Light : BOOL := FALSE;
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
            phase := 1;
            Pump_Motor := TRUE;
        END_IF;

    1:
        Pump_Motor := TRUE;
        IF cleaningConfirmButton THEN
            phase := 2;
            Pump_Motor := FALSE;
            Filling_Valve := TRUE;
        END_IF;

    2:
        Filling_Valve := TRUE;
        IF fillingConfirmButton THEN
            phase := 3;
            Filling_Valve := FALSE;
            Capping_Machine := TRUE;
        END_IF;

    3:
        Capping_Machine := TRUE;
        IF cappingConfirmButton THEN
            phase := 4;
            Capping_Machine := FALSE;
            Packing_Machine := TRUE;
        END_IF;

    4:
        Packing_Machine := TRUE;
        IF packingConfirmButton THEN
            phase := 5;
            Packing_Machine := FALSE;
            Completion_Light := TRUE;
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
