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
    prev_bottleSensor : BOOL := FALSE;
    prev_cleaningConfirmButton : BOOL := FALSE;
    prev_fillingConfirmButton : BOOL := FALSE;
    prev_cappingConfirmButton : BOOL := FALSE;
    prev_packingConfirmButton : BOOL := FALSE;
    prev_finishedButton : BOOL := FALSE;
    rise_bottleSensor : BOOL := FALSE;
    rise_cleaningConfirmButton : BOOL := FALSE;
    rise_fillingConfirmButton : BOOL := FALSE;
    rise_cappingConfirmButton : BOOL := FALSE;
    rise_packingConfirmButton : BOOL := FALSE;
    rise_finishedButton : BOOL := FALSE;
    transitionTaken : BOOL := FALSE;
END_VAR

// Stage 1: edge sampling (diagnostic only; transitions use level-sampled inputs)
rise_bottleSensor := bottleSensor AND NOT prev_bottleSensor;
rise_cleaningConfirmButton := cleaningConfirmButton AND NOT prev_cleaningConfirmButton;
rise_fillingConfirmButton := fillingConfirmButton AND NOT prev_fillingConfirmButton;
rise_cappingConfirmButton := cappingConfirmButton AND NOT prev_cappingConfirmButton;
rise_packingConfirmButton := packingConfirmButton AND NOT prev_packingConfirmButton;
rise_finishedButton := finishedButton AND NOT prev_finishedButton;

prev_bottleSensor := bottleSensor;
prev_cleaningConfirmButton := cleaningConfirmButton;
prev_fillingConfirmButton := fillingConfirmButton;
prev_cappingConfirmButton := cappingConfirmButton;
prev_packingConfirmButton := packingConfirmButton;
prev_finishedButton := finishedButton;

// Stage 2: reset priority first, then at most one phase transition per scan
transitionTaken := FALSE;

IF (phase = 5) AND finishedButton THEN
    phase := 0;
    transitionTaken := TRUE;
ELSIF (phase = 0) AND bottleSensor THEN
    phase := 1;
    transitionTaken := TRUE;
ELSIF (phase = 1) AND cleaningConfirmButton THEN
    phase := 2;
    transitionTaken := TRUE;
ELSIF (phase = 2) AND fillingConfirmButton THEN
    phase := 3;
    transitionTaken := TRUE;
ELSIF (phase = 3) AND cappingConfirmButton THEN
    phase := 4;
    transitionTaken := TRUE;
ELSIF (phase = 4) AND packingConfirmButton THEN
    phase := 5;
    transitionTaken := TRUE;
END_IF;

// Sanity clamp of phase
IF (phase < 0) OR (phase > 5) THEN
    phase := 0;
END_IF;

// Stage 3: no timers are used in this design

// Stage 4: unified output assignments from the post-transition phase
Pump_Motor := FALSE;
Filling_Valve := FALSE;
Capping_Machine := FALSE;
Packing_Machine := FALSE;
Completion_Light := FALSE;

CASE phase OF
    0:
        ; // IDLE: all outputs off
    1:
        Pump_Motor := TRUE;
    2:
        Filling_Valve := TRUE;
    3:
        Capping_Machine := TRUE;
    4:
        Packing_Machine := TRUE;
    5:
        Completion_Light := TRUE;
ELSE
    phase := 0;
END_CASE;
END_FUNCTION_BLOCK
