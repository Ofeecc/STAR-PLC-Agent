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
    (* Phase: 0=IDLE, 1=FILL_A, 2=FILL_B, 3=FILL_C, 4=MIX, 5=DRAIN. *)
    phase : INT := 0;
    batchMode : BOOL := FALSE;
    manualA : BOOL := FALSE;
    manualB : BOOL := FALSE;
    manualC : BOOL := FALSE;
    manualD : BOOL := FALSE;
    manualMix : BOOL := FALSE;
    prevA : BOOL := FALSE;
    prevB : BOOL := FALSE;
    prevC : BOOL := FALSE;
    prevD : BOOL := FALSE;
    prevMix : BOOL := FALSE;
    prevAuto : BOOL := FALSE;
    edgeA : BOOL := FALSE;
    edgeB : BOOL := FALSE;
    edgeC : BOOL := FALSE;
    edgeD : BOOL := FALSE;
    edgeMix : BOOL := FALSE;
    edgeAuto : BOOL := FALSE;
    modeSeen : BOOL := FALSE;
    previousOpeMode : BOOL := FALSE;
    modeChanged : BOOL := FALSE;
END_VAR

(* Button and mode histories update even during a reset scan. *)
edgeA := valveAStart AND NOT prevA;
edgeB := valveBStart AND NOT prevB;
edgeC := valveCStart AND NOT prevC;
edgeD := valveDStart AND NOT prevD;
edgeMix := mixMotorStart AND NOT prevMix;
edgeAuto := autoStart AND NOT prevAuto;
prevA := valveAStart;
prevB := valveBStart;
prevC := valveCStart;
prevD := valveDStart;
prevMix := mixMotorStart;
prevAuto := autoStart;
modeChanged := modeSeen AND (opeMode <> previousOpeMode);
previousOpeMode := opeMode;
modeSeen := TRUE;

(* Physical emergency stopping requires an independent safety-rated path. *)
IF (NOT estop) OR modeChanged THEN
    phase := 0;
    batchMode := FALSE;
    manualA := FALSE;
    manualB := FALSE;
    manualC := FALSE;
    manualD := FALSE;
    manualMix := FALSE;
ELSIF NOT opeMode THEN
    phase := 0;
    batchMode := FALSE;
    IF edgeA THEN manualA := NOT manualA; END_IF;
    IF edgeB THEN manualB := NOT manualB; END_IF;
    IF edgeC THEN manualC := NOT manualC; END_IF;
    IF edgeD THEN manualD := NOT manualD; END_IF;
    IF edgeMix THEN manualMix := NOT manualMix; END_IF;
ELSE
    (* Evaluate only the phase present at entry to this CASE. *)
    CASE phase OF
        0: (* IDLE *)
            IF edgeAuto THEN
                batchMode := processMode;
                phase := 1;
            END_IF;
        1: (* FILL_A *)
            IF levelSensor >= 50 THEN
                phase := 2;
            END_IF;
        2: (* FILL_B *)
            IF levelSensor >= 80 THEN
                IF batchMode THEN
                    phase := 3;
                ELSE
                    phase := 4;
                END_IF;
            END_IF;
        3: (* FILL_C *)
            IF levelSensor >= 100 THEN
                phase := 4;
            END_IF;
        4: (* MIX *)
            IF mixMotorComplete THEN
                phase := 5;
            END_IF;
        5: (* DRAIN: no tank-empty input is provided. *)
            IF edgeAuto THEN
                batchMode := processMode;
                phase := 1;
            END_IF;
        ELSE
            phase := 0;
            batchMode := FALSE;
    END_CASE;
END_IF;

valveARun := estop AND NOT modeChanged AND ((NOT opeMode AND manualA) OR (opeMode AND (phase = 1)));
valveBRun := estop AND NOT modeChanged AND ((NOT opeMode AND manualB) OR (opeMode AND (phase = 2)));
valveCRun := estop AND NOT modeChanged AND ((NOT opeMode AND manualC) OR (opeMode AND (phase = 3)));
valveDRun := estop AND NOT modeChanged AND ((NOT opeMode AND manualD) OR (opeMode AND (phase = 5)));
mixMotorRun := estop AND NOT modeChanged AND ((NOT opeMode AND manualMix) OR (opeMode AND (phase = 4)));
END_FUNCTION_BLOCK
