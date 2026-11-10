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
    phase : E_PUB015_Phase := E_PUB015_Phase.IDLE;
    manualValveARun : BOOL;
    manualValveBRun : BOOL;
    manualValveCRun : BOOL;
    manualValveDRun : BOOL;
    manualMixMotorRun : BOOL;
    prevValveAStart : BOOL;
    prevValveBStart : BOOL;
    prevValveCStart : BOOL;
    prevValveDStart : BOOL;
    prevMixMotorStart : BOOL;
    prevAutoStart : BOOL;
    prevOpeMode : BOOL;
    riseValveAStart : BOOL;
    riseValveBStart : BOOL;
    riseValveCStart : BOOL;
    riseValveDStart : BOOL;
    riseMixMotorStart : BOOL;
    riseAutoStart : BOOL;
    modeChanged : BOOL;
END_VAR

// Edge detection
riseValveAStart := valveAStart AND NOT prevValveAStart;
riseValveBStart := valveBStart AND NOT prevValveBStart;
riseValveCStart := valveCStart AND NOT prevValveCStart;
riseValveDStart := valveDStart AND NOT prevValveDStart;
riseMixMotorStart := mixMotorStart AND NOT prevMixMotorStart;
riseAutoStart := autoStart AND NOT prevAutoStart;
modeChanged := opeMode <> prevOpeMode;

IF NOT estop THEN
    valveARun := FALSE;
    valveBRun := FALSE;
    valveCRun := FALSE;
    valveDRun := FALSE;
    mixMotorRun := FALSE;
    manualValveARun := FALSE;
    manualValveBRun := FALSE;
    manualValveCRun := FALSE;
    manualValveDRun := FALSE;
    manualMixMotorRun := FALSE;
    phase := E_PUB015_Phase.IDLE;
ELSE
    IF modeChanged THEN
        manualValveARun := FALSE;
        manualValveBRun := FALSE;
        manualValveCRun := FALSE;
        manualValveDRun := FALSE;
        manualMixMotorRun := FALSE;
        phase := E_PUB015_Phase.IDLE;
    END_IF;

    IF opeMode THEN
        IF phase = E_PUB015_Phase.IDLE THEN
            IF riseAutoStart THEN
                phase := E_PUB015_Phase.FILL_A;
            END_IF;
        ELSE
            CASE phase OF
                E_PUB015_Phase.FILL_A:
                    IF levelSensor >= 50 THEN
                        phase := E_PUB015_Phase.FILL_B;
                    END_IF;
                E_PUB015_Phase.FILL_B:
                    IF levelSensor >= 80 THEN
                        IF processMode THEN
                            phase := E_PUB015_Phase.FILL_C;
                        ELSE
                            phase := E_PUB015_Phase.MIX;
                        END_IF;
                    END_IF;
                E_PUB015_Phase.FILL_C:
                    IF levelSensor >= 100 THEN
                        phase := E_PUB015_Phase.MIX;
                    END_IF;
                E_PUB015_Phase.MIX:
                    IF mixMotorComplete THEN
                        phase := E_PUB015_Phase.DRAIN;
                    END_IF;
                E_PUB015_Phase.DRAIN:
                    ;
            END_CASE;
        END_IF;

        valveARun := (phase = E_PUB015_Phase.FILL_A);
        valveBRun := (phase = E_PUB015_Phase.FILL_B);
        valveCRun := (phase = E_PUB015_Phase.FILL_C);
        valveDRun := (phase = E_PUB015_Phase.DRAIN);
        mixMotorRun := (phase = E_PUB015_Phase.MIX);
    ELSE
        phase := E_PUB015_Phase.IDLE;

        IF riseValveAStart THEN
            manualValveARun := NOT manualValveARun;
        END_IF;
        IF riseValveBStart THEN
            manualValveBRun := NOT manualValveBRun;
        END_IF;
        IF riseValveCStart THEN
            manualValveCRun := NOT manualValveCRun;
        END_IF;
        IF riseValveDStart THEN
            manualValveDRun := NOT manualValveDRun;
        END_IF;
        IF riseMixMotorStart THEN
            manualMixMotorRun := NOT manualMixMotorRun;
        END_IF;

        valveARun := manualValveARun;
        valveBRun := manualValveBRun;
        valveCRun := manualValveCRun;
        valveDRun := manualValveDRun;
        mixMotorRun := manualMixMotorRun;
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
