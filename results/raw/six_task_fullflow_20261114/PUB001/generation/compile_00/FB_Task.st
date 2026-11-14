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

// Stage 1: edge sampling\nrise_bottleSensor := bottleSensor AND NOT prev_bottleSensor;\nrise_cleaningConfirmButton := cleaningConfirmButton AND NOT prev_cleaningConfirmButton;\nrise_fillingConfirmButton := fillingConfirmButton AND NOT prev_fillingConfirmButton;\nrise_cappingConfirmButton := cappingConfirmButton AND NOT prev_cappingConfirmButton;\nrise_packingConfirmButton := packingConfirmButton AND NOT prev_packingConfirmButton;\nrise_finishedButton := finishedButton AND NOT prev_finishedButton;\n\nprev_bottleSensor := bottleSensor;\nprev_cleaningConfirmButton := cleaningConfirmButton;\nprev_fillingConfirmButton := fillingConfirmButton;\nprev_cappingConfirmButton := cappingConfirmButton;\nprev_packingConfirmButton := packingConfirmButton;\nprev_finishedButton := finishedButton;\n\n// Stage 2: reset priority and state transitions\ntransitionTaken := FALSE;\n\nIF (phase = 5) AND finishedButton THEN\n    phase := 0;\n    transitionTaken := TRUE;\nELSIF (phase = 0) AND bottleSensor THEN\n    phase := 1;\n    transitionTaken := TRUE;\nELSIF (phase = 1) AND cleaningConfirmButton THEN\n    phase := 2;\n    transitionTaken := TRUE;\nELSIF (phase = 2) AND fillingConfirmButton THEN\n    phase := 3;\n    transitionTaken := TRUE;\nELSIF (phase = 3) AND cappingConfirmButton THEN\n    phase := 4;\n    transitionTaken := TRUE;\nELSIF (phase = 4) AND packingConfirmButton THEN\n    phase := 5;\n    transitionTaken := TRUE;\nEND_IF;\n\n// Stage 3: no timers are used\n\n// Stage 4: unified output assignments from post-transition phase\nCASE phase OF\n    0:\n        Pump_Motor := FALSE;\n        Filling_Valve := FALSE;\n        Capping_Machine := FALSE;\n        Packing_Machine := FALSE;\n        Completion_Light := FALSE;\n    1:\n        Pump_Motor := TRUE;\n        Filling_Valve := FALSE;\n        Capping_Machine := FALSE;\n        Packing_Machine := FALSE;\n        Completion_Light := FALSE;\n    2:\n        Pump_Motor := FALSE;\n        Filling_Valve := TRUE;\n        Capping_Machine := FALSE;\n        Packing_Machine := FALSE;\n        Completion_Light := FALSE;\n    3:\n        Pump_Motor := FALSE;\n        Filling_Valve := FALSE;\n        Capping_Machine := TRUE;\n        Packing_Machine := FALSE;\n        Completion_Light := FALSE;\n    4:\n        Pump_Motor := FALSE;\n        Filling_Valve := FALSE;\n        Capping_Machine := FALSE;\n        Packing_Machine := TRUE;\n        Completion_Light := FALSE;\n    5:\n        Pump_Motor := FALSE;\n        Filling_Valve := FALSE;\n        Capping_Machine := FALSE;\n        Packing_Machine := FALSE;\n        Completion_Light := TRUE;\n    ELSE\n        phase := 0;\n        Pump_Motor := FALSE;\n        Filling_Valve := FALSE;\n        Capping_Machine := FALSE;\n        Packing_Machine := FALSE;\n        Completion_Light := FALSE;\nEND_CASE;
END_FUNCTION_BLOCK
