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
    m_A : BOOL;
    m_B : BOOL;
    m_C : BOOL;
    m_D : BOOL;
    m_Mix : BOOL;
    pA : BOOL;
    pB : BOOL;
    pC : BOOL;
    pD : BOOL;
    pMix : BOOL;
    pAuto : BOOL;
    prevMode : BOOL;
    rA : BOOL;
    rB : BOOL;
    rC : BOOL;
    rD : BOOL;
    rMix : BOOL;
    rAuto : BOOL;
    phase : INT;
END_VAR

rA := valveAStart AND NOT pA;
rB := valveBStart AND NOT pB;
rC := valveCStart AND NOT pC;
rD := valveDStart AND NOT pD;
rMix := mixMotorStart AND NOT pMix;
rAuto := autoStart AND NOT pAuto;

IF NOT estop THEN
    m_A := FALSE; m_B := FALSE; m_C := FALSE; m_D := FALSE; m_Mix := FALSE;
    phase := 0;
    valveARun := FALSE; valveBRun := FALSE; valveCRun := FALSE; valveDRun := FALSE; mixMotorRun := FALSE;
ELSIF opeMode <> prevMode THEN
    m_A := FALSE; m_B := FALSE; m_C := FALSE; m_D := FALSE; m_Mix := FALSE;
    phase := 0;
    valveARun := FALSE; valveBRun := FALSE; valveCRun := FALSE; valveDRun := FALSE; mixMotorRun := FALSE;
ELSIF NOT opeMode THEN
    IF rA THEN m_A := NOT m_A; END_IF
    IF rB THEN m_B := NOT m_B; END_IF
    IF rC THEN m_C := NOT m_C; END_IF
    IF rD THEN m_D := NOT m_D; END_IF
    IF rMix THEN m_Mix := NOT m_Mix; END_IF
    valveARun := m_A; valveBRun := m_B; valveCRun := m_C; valveDRun := m_D; mixMotorRun := m_Mix;
ELSE
    CASE phase OF
    0:
        IF rAuto THEN phase := 1; END_IF
    1:
        IF levelSensor >= 50 THEN phase := 2; END_IF
    2:
        IF levelSensor >= 80 THEN
            IF processMode THEN phase := 3; ELSE phase := 4; END_IF
        END_IF
    3:
        IF levelSensor >= 100 THEN phase := 4; END_IF
    4:
        IF mixMotorComplete THEN phase := 5; END_IF
    5:
        ;
    END_CASE
    valveARun := (phase = 1);
    valveBRun := (phase = 2);
    valveCRun := (phase = 3);
    valveDRun := (phase = 5);
    mixMotorRun := (phase = 4);
END_IF

pA := valveAStart;
pB := valveBStart;
pC := valveCStart;
pD := valveDStart;
pMix := mixMotorStart;
pAuto := autoStart;
prevMode := opeMode;
END_FUNCTION_BLOCK
