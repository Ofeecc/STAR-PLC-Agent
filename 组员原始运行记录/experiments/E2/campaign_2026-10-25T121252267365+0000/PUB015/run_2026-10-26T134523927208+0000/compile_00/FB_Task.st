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
    prevValveAStart : BOOL;
    prevValveBStart : BOOL;
    prevValveCStart : BOOL;
    prevValveDStart : BOOL;
    prevMixMotorStart : BOOL;
    prevAutoStart : BOOL;
    prevOpeMode : BOOL;
    edgeValveA : BOOL;
    edgeValveB : BOOL;
    edgeValveC : BOOL;
    edgeValveD : BOOL;
    edgeMixMotor : BOOL;
    edgeAutoStart : BOOL;
    phase : INT;
    batchProcessMode : BOOL;
END_VAR

edgeValveA := valveAStart AND NOT prevValveAStart;
edgeValveB := valveBStart AND NOT prevValveBStart;
edgeValveC := valveCStart AND NOT prevValveCStart;
edgeValveD := valveDStart AND NOT prevValveDStart;
edgeMixMotor := mixMotorStart AND NOT prevMixMotorStart;
edgeAutoStart := autoStart AND NOT prevAutoStart;

IF NOT estop THEN
    valveARun := FALSE;
    valveBRun := FALSE;
    valveCRun := FALSE;
    valveDRun := FALSE;
    mixMotorRun := FALSE;
    phase := 0;
    batchProcessMode := FALSE;
ELSE
    IF opeMode <> prevOpeMode THEN
        valveARun := FALSE;
        valveBRun := FALSE;
        valveCRun := FALSE;
        valveDRun := FALSE;
        mixMotorRun := FALSE;
        phase := 0;
        batchProcessMode := FALSE;
    END_IF;

    IF opeMode THEN
        valveARun := FALSE;
        valveBRun := FALSE;
        valveCRun := FALSE;
        valveDRun := FALSE;
        mixMotorRun := FALSE;

        CASE phase OF
            0:
                IF edgeAutoStart THEN
                    batchProcessMode := processMode;
                    phase := 1;
                END_IF;
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
            5:
                phase := 5;
            ELSE
                phase := 0;
        END_CASE;

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
    ELSE
        IF edgeValveA THEN
            valveARun := NOT valveARun;
        END_IF;
        IF edgeValveB THEN
            valveBRun := NOT valveBRun;
        END_IF;
        IF edgeValveC THEN
            valveCRun := NOT valveCRun;
        END_IF;
        IF edgeValveD THEN
            valveDRun := NOT valveDRun;
        END_IF;
        IF edgeMixMotor THEN
            mixMotorRun := NOT mixMotorRun;
        END_IF;
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
