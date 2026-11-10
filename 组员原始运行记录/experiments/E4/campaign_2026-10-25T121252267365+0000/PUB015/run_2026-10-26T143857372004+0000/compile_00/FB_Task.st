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
    valveARun : BOOL;
    valveBRun : BOOL;
    valveCRun : BOOL;
    valveDRun : BOOL;
    mixMotorRun : BOOL;
END_VAR
VAR
    phase : INT;
    batchProcessMode : BOOL;
    initDone : BOOL;
    prevOpeMode : BOOL;
    prevValveAStart : BOOL;
    prevValveBStart : BOOL;
    prevValveCStart : BOOL;
    prevValveDStart : BOOL;
    prevMixMotorStart : BOOL;
    prevAutoStart : BOOL;
END_VAR

IF NOT initDone THEN
    initDone := TRUE;
    prevOpeMode := opeMode;
    phase := 0;
    batchProcessMode := FALSE;
    valveARun := FALSE;
    valveBRun := FALSE;
    valveCRun := FALSE;
    valveDRun := FALSE;
    mixMotorRun := FALSE;
END_IF;

IF NOT estop THEN
    valveARun := FALSE;
    valveBRun := FALSE;
    valveCRun := FALSE;
    valveDRun := FALSE;
    mixMotorRun := FALSE;
    phase := 0;
    batchProcessMode := FALSE;
ELSIF opeMode <> prevOpeMode THEN
    valveARun := FALSE;
    valveBRun := FALSE;
    valveCRun := FALSE;
    valveDRun := FALSE;
    mixMotorRun := FALSE;
    phase := 0;
    batchProcessMode := FALSE;
ELSE
    IF NOT opeMode THEN
        IF valveAStart AND NOT prevValveAStart THEN
            valveARun := NOT valveARun;
        END_IF;
        IF valveBStart AND NOT prevValveBStart THEN
            valveBRun := NOT valveBRun;
        END_IF;
        IF valveCStart AND NOT prevValveCStart THEN
            valveCRun := NOT valveCRun;
        END_IF;
        IF valveDStart AND NOT prevValveDStart THEN
            valveDRun := NOT valveDRun;
        END_IF;
        IF mixMotorStart AND NOT prevMixMotorStart THEN
            mixMotorRun := NOT mixMotorRun;
        END_IF;
    ELSE
        IF (phase = 0) AND autoStart AND NOT prevAutoStart THEN
            batchProcessMode := processMode;
            phase := 1;
        ELSE
            CASE phase OF
                1:
                    IF levelSensor >= 50 THEN
                        phase := 2;
                    END_IF;
                2:
                    IF levelSensor >= 80 THEN
                        IF batchProcessMode THEN
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
            END_CASE;
        END_IF;

        valveARun := FALSE;
        valveBRun := FALSE;
        valveCRun := FALSE;
        valveDRun := FALSE;
        mixMotorRun := FALSE;

        CASE phase OF
            1:
                valveARun := TRUE;
            2:
                valveBRun := TRUE;
            3:
                valveCRun := TRUE;
            4:
                mixMotorRun := TRUE;
            5:
                valveDRun := TRUE;
        END_CASE;
    END_IF;
END_IF;

prevValveAStart := valveAStart;
prevValveBStart := valveBStart;
prevValveCStart := valveCStart;
prevValveDStart := valveDStart;
prevMixMotorStart := mixMotorStart;
prevAutoStart := autoStart;
prevOpeMode := opeMode;
END_FUNCTION_BLOCK
