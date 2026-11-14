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
    initialized : BOOL := FALSE;
    prevMode : BOOL;
    prevValveAStart : BOOL;
    prevValveBStart : BOOL;
    prevValveCStart : BOOL;
    prevValveDStart : BOOL;
    prevMixMotorStart : BOOL;
    prevAutoStart : BOOL;
    modeChanged : BOOL;
    riseValveAStart : BOOL;
    riseValveBStart : BOOL;
    riseValveCStart : BOOL;
    riseValveDStart : BOOL;
    riseMixMotorStart : BOOL;
    riseAutoStart : BOOL;
    phase : E_Phase := E_Phase.IDLE;
    batchMode : BOOL;
    manualA : BOOL;
    manualB : BOOL;
    manualC : BOOL;
    manualD : BOOL;
    manualMix : BOOL;
END_VAR

modeChanged := initialized AND (opeMode <> prevMode);

riseValveAStart := valveAStart AND NOT prevValveAStart;
riseValveBStart := valveBStart AND NOT prevValveBStart;
riseValveCStart := valveCStart AND NOT prevValveCStart;
riseValveDStart := valveDStart AND NOT prevValveDStart;
riseMixMotorStart := mixMotorStart AND NOT prevMixMotorStart;
riseAutoStart := autoStart AND NOT prevAutoStart;

prevValveAStart := valveAStart;
prevValveBStart := valveBStart;
prevValveCStart := valveCStart;
prevValveDStart := valveDStart;
prevMixMotorStart := mixMotorStart;
prevAutoStart := autoStart;
prevMode := opeMode;
initialized := TRUE;

valveARun := FALSE;
valveBRun := FALSE;
valveCRun := FALSE;
valveDRun := FALSE;
mixMotorRun := FALSE;

IF NOT estop THEN
    phase := E_Phase.IDLE;
    batchMode := FALSE;
    manualA := FALSE;
    manualB := FALSE;
    manualC := FALSE;
    manualD := FALSE;
    manualMix := FALSE;
ELSIF modeChanged THEN
    phase := E_Phase.IDLE;
    batchMode := FALSE;
    manualA := FALSE;
    manualB := FALSE;
    manualC := FALSE;
    manualD := FALSE;
    manualMix := FALSE;
ELSIF opeMode THEN
    CASE phase OF
        E_Phase.IDLE:
            IF riseAutoStart THEN
                batchMode := processMode;
                phase := E_Phase.FILL_A;
                valveARun := TRUE;
            END_IF

        E_Phase.FILL_A:
            valveARun := TRUE;
            IF levelSensor >= 50 THEN
                valveARun := FALSE;
                valveBRun := TRUE;
                phase := E_Phase.FILL_B;
            END_IF

        E_Phase.FILL_B:
            valveBRun := TRUE;
            IF levelSensor >= 80 THEN
                valveBRun := FALSE;
                IF batchMode THEN
                    valveCRun := TRUE;
                    phase := E_Phase.FILL_C;
                ELSE
                    mixMotorRun := TRUE;
                    phase := E_Phase.MIX;
                END_IF
            END_IF

        E_Phase.FILL_C:
            valveCRun := TRUE;
            IF levelSensor >= 100 THEN
                valveCRun := FALSE;
                mixMotorRun := TRUE;
                phase := E_Phase.MIX;
            END_IF

        E_Phase.MIX:
            mixMotorRun := TRUE;
            IF mixMotorComplete THEN
                mixMotorRun := FALSE;
                valveDRun := TRUE;
                phase := E_Phase.DRAIN;
            END_IF

        E_Phase.DRAIN:
            valveDRun := TRUE;
            IF riseAutoStart THEN
                batchMode := processMode;
                valveDRun := FALSE;
                valveARun := TRUE;
                phase := E_Phase.FILL_A;
            END_IF
    END_CASE
ELSE
    phase := E_Phase.IDLE;
    batchMode := FALSE;

    IF riseValveAStart THEN
        manualA := NOT manualA;
    END_IF
    IF riseValveBStart THEN
        manualB := NOT manualB;
    END_IF
    IF riseValveCStart THEN
        manualC := NOT manualC;
    END_IF
    IF riseValveDStart THEN
        manualD := NOT manualD;
    END_IF
    IF riseMixMotorStart THEN
        manualMix := NOT manualMix;
    END_IF

    valveARun := manualA;
    valveBRun := manualB;
    valveCRun := manualC;
    valveDRun := manualD;
    mixMotorRun := manualMix;
END_IF
END_FUNCTION_BLOCK
