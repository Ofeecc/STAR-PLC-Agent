FUNCTION_BLOCK FB_Task
VAR_INPUT
    Mode : BOOL;
    ForwardButton : BOOL;
    ReverseButton : BOOL;
    SensorFeed : BOOL;
    SensorWash : BOOL;
    SensorWeight : BOOL;
    SensorFiring : BOOL;
    SensorOutput : BOOL;
    washComplete : BOOL;
    weightComplete : BOOL;
    weight : REAL;
    firingComplete : BOOL;
END_VAR
VAR_OUTPUT
    MotorForward : BOOL;
    MotorReverse : BOOL;
    kick : BOOL;
    CompletionLight : BOOL;
    firingTemp : REAL;
END_VAR
VAR
    phase : E_ProductionPhase := E_ProductionPhase.WAIT_FEED;
    rejected : BOOL := FALSE;
    ModePrev : BOOL := FALSE;
END_VAR

IF Mode <> ModePrev THEN
    ModePrev := Mode;
    phase := E_ProductionPhase.WAIT_FEED;
    rejected := FALSE;
    kick := FALSE;
    CompletionLight := FALSE;
END_IF

IF NOT Mode THEN
    MotorForward := ForwardButton AND NOT ReverseButton;
    MotorReverse := ReverseButton AND NOT ForwardButton;
    kick := FALSE;
    CompletionLight := FALSE;
    phase := E_ProductionPhase.WAIT_FEED;
    rejected := FALSE;
ELSE
    MotorReverse := FALSE;

    CASE phase OF
        E_ProductionPhase.WAIT_FEED:
            MotorForward := FALSE;
            kick := FALSE;
            CompletionLight := FALSE;
            rejected := FALSE;
            IF SensorFeed THEN
                MotorForward := TRUE;
                phase := E_ProductionPhase.MOVE_TO_WASH;
            END_IF

        E_ProductionPhase.MOVE_TO_WASH:
            MotorForward := TRUE;
            kick := FALSE;
            CompletionLight := FALSE;
            IF SensorWash THEN
                MotorForward := FALSE;
                phase := E_ProductionPhase.WAIT_WASH;
            END_IF

        E_ProductionPhase.WAIT_WASH:
            MotorForward := FALSE;
            kick := FALSE;
            CompletionLight := FALSE;
            IF washComplete THEN
                MotorForward := TRUE;
                phase := E_ProductionPhase.MOVE_TO_WEIGHT;
            END_IF

        E_ProductionPhase.MOVE_TO_WEIGHT:
            MotorForward := TRUE;
            kick := FALSE;
            CompletionLight := FALSE;
            IF SensorWeight THEN
                MotorForward := FALSE;
                phase := E_ProductionPhase.WAIT_WEIGHT;
            END_IF

        E_ProductionPhase.WAIT_WEIGHT:
            MotorForward := FALSE;
            CompletionLight := FALSE;
            IF rejected THEN
                kick := TRUE;
                IF NOT SensorWeight THEN
                    kick := FALSE;
                    rejected := FALSE;
                    phase := E_ProductionPhase.WAIT_FEED;
                END_IF
            ELSE
                kick := FALSE;
                IF SensorWeight AND weightComplete THEN
                    IF (weight >= 100.0) AND (weight <= 200.0) THEN
                        firingTemp := 500.0 + (weight - 100.0) * 0.5;
                        MotorForward := TRUE;
                        phase := E_ProductionPhase.MOVE_TO_FIRING;
                    ELSE
                        kick := TRUE;
                        rejected := TRUE;
                    END_IF
                END_IF
            END_IF

        E_ProductionPhase.MOVE_TO_FIRING:
            MotorForward := TRUE;
            kick := FALSE;
            CompletionLight := FALSE;
            IF SensorFiring THEN
                MotorForward := FALSE;
                phase := E_ProductionPhase.WAIT_FIRING;
            END_IF

        E_ProductionPhase.WAIT_FIRING:
            MotorForward := FALSE;
            kick := FALSE;
            CompletionLight := FALSE;
            IF firingComplete THEN
                MotorForward := TRUE;
                phase := E_ProductionPhase.MOVE_TO_OUTPUT;
            END_IF

        E_ProductionPhase.MOVE_TO_OUTPUT:
            MotorForward := TRUE;
            kick := FALSE;
            CompletionLight := FALSE;
            IF SensorOutput THEN
                MotorForward := FALSE;
                CompletionLight := TRUE;
                phase := E_ProductionPhase.OUTPUT_DONE;
            END_IF

        E_ProductionPhase.OUTPUT_DONE:
            MotorForward := FALSE;
            kick := FALSE;
            IF SensorOutput THEN
                CompletionLight := TRUE;
            ELSE
                CompletionLight := FALSE;
                phase := E_ProductionPhase.WAIT_FEED;
            END_IF
    END_CASE
END_IF
END_FUNCTION_BLOCK
