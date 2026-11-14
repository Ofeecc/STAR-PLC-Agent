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
    phase : E_Phase := E_Phase.IDLE;
    manualLatchA : BOOL := FALSE;
    manualLatchB : BOOL := FALSE;
    manualLatchC : BOOL := FALSE;
    manualLatchD : BOOL := FALSE;
    manualLatchMix : BOOL := FALSE;
    processModeLatched : BOOL := FALSE;
    initialized : BOOL := FALSE;
    prevOpeMode : BOOL := FALSE;
    modeChange : BOOL := FALSE;
    prevValveAStart : BOOL := FALSE;
    prevValveBStart : BOOL := FALSE;
    prevValveCStart : BOOL := FALSE;
    prevValveDStart : BOOL := FALSE;
    prevMixMotorStart : BOOL := FALSE;
    prevAutoStart : BOOL := FALSE;
    edgeA : BOOL := FALSE;
    edgeB : BOOL := FALSE;
    edgeC : BOOL := FALSE;
    edgeD : BOOL := FALSE;
    edgeMix : BOOL := FALSE;
    edgeAuto : BOOL := FALSE;
END_VAR

// Edge sampling
edgeA := valveAStart AND NOT prevValveAStart;
edgeB := valveBStart AND NOT prevValveBStart;
edgeC := valveCStart AND NOT prevValveCStart;
edgeD := valveDStart AND NOT prevValveDStart;
edgeMix := mixMotorStart AND NOT prevMixMotorStart;
edgeAuto := autoStart AND NOT prevAutoStart;

prevValveAStart := valveAStart;
prevValveBStart := valveBStart;
prevValveCStart := valveCStart;
prevValveDStart := valveDStart;
prevMixMotorStart := mixMotorStart;
prevAutoStart := autoStart;

modeChange := initialized AND (opeMode <> prevOpeMode);
prevOpeMode := opeMode;
initialized := TRUE;

// Priority 1: emergency stop
IF NOT estop THEN
    phase := E_Phase.IDLE;
    manualLatchA := FALSE;
    manualLatchB := FALSE;
    manualLatchC := FALSE;
    manualLatchD := FALSE;
    manualLatchMix := FALSE;
    processModeLatched := FALSE;

// Priority 2: mode-change isolation
ELSIF modeChange THEN
    phase := E_Phase.IDLE;
    manualLatchA := FALSE;
    manualLatchB := FALSE;
    manualLatchC := FALSE;
    manualLatchD := FALSE;
    manualLatchMix := FALSE;
    processModeLatched := FALSE;

// Priority 3/4: normal operation
ELSE
    IF opeMode THEN
        CASE phase OF
            E_Phase.IDLE:
                IF edgeAuto THEN
                    phase := E_Phase.FILL_A;
                    processModeLatched := processMode;
                END_IF;

            E_Phase.FILL_A:
                IF levelSensor >= 50 THEN
                    phase := E_Phase.FILL_B;
                END_IF;

            E_Phase.FILL_B:
                IF levelSensor >= 80 THEN
                    IF processModeLatched THEN
                        phase := E_Phase.FILL_C;
                    ELSE
                        phase := E_Phase.MIX;
                    END_IF;
                END_IF;

            E_Phase.FILL_C:
                IF levelSensor >= 100 THEN
                    phase := E_Phase.MIX;
                END_IF;

            E_Phase.MIX:
                IF mixMotorComplete THEN
                    phase := E_Phase.DRAIN;
                END_IF;

            E_Phase.DRAIN:
                IF edgeAuto THEN
                    phase := E_Phase.FILL_A;
                    processModeLatched := processMode;
                END_IF;

            ELSE
                phase := E_Phase.IDLE;
        END_CASE;
    ELSE
        IF edgeA THEN
            manualLatchA := NOT manualLatchA;
        END_IF;
        IF edgeB THEN
            manualLatchB := NOT manualLatchB;
        END_IF;
        IF edgeC THEN
            manualLatchC := NOT manualLatchC;
        END_IF;
        IF edgeD THEN
            manualLatchD := NOT manualLatchD;
        END_IF;
        IF edgeMix THEN
            manualLatchMix := NOT manualLatchMix;
        END_IF;
    END_IF;
END_IF;

// Unified output assignments
IF NOT estop THEN
    valveARun := FALSE;
    valveBRun := FALSE;
    valveCRun := FALSE;
    valveDRun := FALSE;
    mixMotorRun := FALSE;
ELSIF modeChange THEN
    valveARun := FALSE;
    valveBRun := FALSE;
    valveCRun := FALSE;
    valveDRun := FALSE;
    mixMotorRun := FALSE;
ELSIF opeMode THEN
    valveARun := (phase = E_Phase.FILL_A);
    valveBRun := (phase = E_Phase.FILL_B);
    valveCRun := (phase = E_Phase.FILL_C);
    valveDRun := (phase = E_Phase.DRAIN);
    mixMotorRun := (phase = E_Phase.MIX);
ELSE
    valveARun := manualLatchA;
    valveBRun := manualLatchB;
    valveCRun := manualLatchC;
    valveDRun := manualLatchD;
    mixMotorRun := manualLatchMix;
END_IF;
END_FUNCTION_BLOCK
