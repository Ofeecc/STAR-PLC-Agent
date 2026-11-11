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
    nextPhase : INT := 0;
END_VAR

CASE phase OF
    0:
        IF bottleSensor THEN
            nextPhase := 1;
        ELSE
            nextPhase := 0;
        END_IF;

    1:
        IF cleaningConfirmButton THEN
            nextPhase := 2;
        ELSE
            nextPhase := 1;
        END_IF;

    2:
        IF fillingConfirmButton THEN
            nextPhase := 3;
        ELSE
            nextPhase := 2;
        END_IF;

    3:
        IF cappingConfirmButton THEN
            nextPhase := 4;
        ELSE
            nextPhase := 3;
        END_IF;

    4:
        IF packingConfirmButton THEN
            nextPhase := 5;
        ELSE
            nextPhase := 4;
        END_IF;

    5:
        IF finishedButton THEN
            nextPhase := 0;
        ELSE
            nextPhase := 5;
        END_IF;

    ELSE
        nextPhase := 0;
END_CASE

Pump_Motor := (nextPhase = 1);
Filling_Valve := (nextPhase = 2);
Capping_Machine := (nextPhase = 3);
Packing_Machine := (nextPhase = 4);
Completion_Light := (nextPhase = 5);

phase := nextPhase;
END_FUNCTION_BLOCK
