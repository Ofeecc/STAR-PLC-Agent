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
    next_phase : INT;
END_VAR

next_phase := phase;

IF (phase = 5) AND finishedButton THEN
    next_phase := 0;
ELSIF (phase = 0) AND bottleSensor THEN
    next_phase := 1;
ELSIF (phase = 1) AND cleaningConfirmButton THEN
    next_phase := 2;
ELSIF (phase = 2) AND fillingConfirmButton THEN
    next_phase := 3;
ELSIF (phase = 3) AND cappingConfirmButton THEN
    next_phase := 4;
ELSIF (phase = 4) AND packingConfirmButton THEN
    next_phase := 5;
END_IF;

phase := next_phase;

Pump_Motor := (phase = 1);
Filling_Valve := (phase = 2);
Capping_Machine := (phase = 3);
Packing_Machine := (phase = 4);
Completion_Light := (phase = 5);
END_FUNCTION_BLOCK
