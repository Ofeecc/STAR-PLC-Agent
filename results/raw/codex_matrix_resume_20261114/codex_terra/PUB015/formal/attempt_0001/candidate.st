FUNCTION_BLOCK FB_Task
VAR_INPUT
    estop : BOOL;
    opeMode : BOOL;
    valveAStart : BOOL;
    valveBStart : BOOL;
    valveCStart : BOOL;
    valveDStart : BOOL;
    mixMotorStart : BOOL;
    autoStart : BOOL;
    processMode : BOOL;
    levelSensor : INT;
    mixMotorComplete : BOOL;
END_VAR
VAR_OUTPUT
    valveARun : BOOL := FALSE;
    valveBRun : BOOL := FALSE;
    valveCRun : BOOL := FALSE;
    valveDRun : BOOL := FALSE;
    mixMotorRun : BOOL := FALSE;
END_VAR
VAR
    phase : INT := 0;
    batchMode : BOOL := FALSE;
    previousMode : BOOL := FALSE;
    modeInitialized : BOOL := FALSE;
    previousAStart : BOOL := FALSE;
    previousBStart : BOOL := FALSE;
    previousCStart : BOOL := FALSE;
    previousDStart : BOOL := FALSE;
    previousMixStart : BOOL := FALSE;
    previousAutoStart : BOOL := FALSE;
END_VAR

IF NOT estop OR (modeInitialized AND (opeMode <> previousMode)) THEN
    phase := 0;
    batchMode := FALSE;
    valveARun := FALSE;
    valveBRun := FALSE;
    valveCRun := FALSE;
    valveDRun := FALSE;
    mixMotorRun := FALSE;
ELSIF NOT opeMode THEN
    IF valveAStart AND NOT previousAStart THEN
        valveARun := NOT valveARun;
    END_IF;
    IF valveBStart AND NOT previousBStart THEN
        valveBRun := NOT valveBRun;
    END_IF;
    IF valveCStart AND NOT previousCStart THEN
        valveCRun := NOT valveCRun;
    END_IF;
    IF valveDStart AND NOT previousDStart THEN
        valveDRun := NOT valveDRun;
    END_IF;
    IF mixMotorStart AND NOT previousMixStart THEN
        mixMotorRun := NOT mixMotorRun;
    END_IF;
ELSE
    CASE phase OF
        0, 5:
            IF autoStart AND NOT previousAutoStart THEN
                batchMode := processMode;
                phase := 1;
            END_IF;
        1:
            IF levelSensor >= 50 THEN
                phase := 2;
            END_IF;
        2:
            IF levelSensor >= 80 THEN
                IF batchMode THEN
                    phase := 3;
                ELSE
                    phase := 4;
                END_IF;
            END_IF;
        3:
            IF levelSensor >= 100 THEN
                phase := 4;
            END_IF;
        4:
            IF mixMotorComplete THEN
                phase := 5;
            END_IF;
    ELSE
        phase := 0;
    END_CASE;
    valveARun := phase = 1;
    valveBRun := phase = 2;
    valveCRun := phase = 3;
    mixMotorRun := phase = 4;
    valveDRun := phase = 5;
END_IF;
previousAStart := valveAStart;
previousBStart := valveBStart;
previousCStart := valveCStart;
previousDStart := valveDStart;
previousMixStart := mixMotorStart;
previousAutoStart := autoStart;
previousMode := opeMode;
modeInitialized := TRUE;
END_FUNCTION_BLOCK
