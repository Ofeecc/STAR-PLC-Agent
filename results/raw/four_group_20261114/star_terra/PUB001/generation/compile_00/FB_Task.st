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
    phase : USINT := 0;
    sampledBottle : BOOL;
    sampledCleaningConfirm : BOOL;
    sampledFillingConfirm : BOOL;
    sampledCappingConfirm : BOOL;
    sampledPackingConfirm : BOOL;
    sampledFinished : BOOL;
END_VAR

sampledBottle := bottleSensor;
sampledCleaningConfirm := cleaningConfirmButton;
sampledFillingConfirm := fillingConfirmButton;
sampledCappingConfirm := cappingConfirmButton;
sampledPackingConfirm := packingConfirmButton;
sampledFinished := finishedButton;

CASE phase OF
    0:
        IF sampledBottle THEN
            phase := 1;
        END_IF;
    1:
        IF sampledCleaningConfirm THEN
            phase := 2;
        END_IF;
    2:
        IF sampledFillingConfirm THEN
            phase := 3;
        END_IF;
    3:
        IF sampledCappingConfirm THEN
            phase := 4;
        END_IF;
    4:
        IF sampledPackingConfirm THEN
            phase := 5;
        END_IF;
    5:
        IF sampledFinished THEN
            phase := 0;
        END_IF;
    ELSE
        phase := 0;
END_CASE;

Pump_Motor := (phase = 1);
Filling_Valve := (phase = 2);
Capping_Machine := (phase = 3);
Packing_Machine := (phase = 4);
Completion_Light := (phase = 5);
END_FUNCTION_BLOCK
