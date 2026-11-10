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
    phase : INT := 0;
    lastMode : BOOL := FALSE;
END_VAR

MotorForward := FALSE;
MotorReverse := FALSE;

IF NOT Mode THEN
    phase := 0;
    kick := FALSE;
    CompletionLight := FALSE;
    MotorForward := ForwardButton AND NOT ReverseButton;
    MotorReverse := ReverseButton AND NOT ForwardButton;
ELSE
    IF NOT lastMode THEN
        phase := 0;
        kick := FALSE;
        CompletionLight := FALSE;
    END_IF;

    CASE phase OF
        0: (* WAIT_FEED *)
            kick := FALSE;
            CompletionLight := FALSE;
            IF SensorFeed THEN
                phase := 1;
                MotorForward := TRUE;
            END_IF;

        1: (* MOVE_TO_WASH *)
            MotorForward := TRUE;
            IF SensorWash THEN
                MotorForward := FALSE;
                phase := 2;
            END_IF;

        2: (* WAIT_WASH *)
            IF SensorWash AND washComplete THEN
                phase := 3;
                MotorForward := TRUE;
            END_IF;

        3: (* MOVE_TO_WEIGHT *)
            MotorForward := TRUE;
            IF SensorWeight THEN
                MotorForward := FALSE;
                phase := 4;
            END_IF;

        4: (* WAIT_WEIGHT *)
            IF SensorWeight AND weightComplete THEN
                IF (weight >= 100.0) AND (weight <= 200.0) THEN
                    firingTemp := 500.0 + ((weight - 100.0) * 0.5);
                    kick := FALSE;
                    phase := 6;
                    MotorForward := TRUE;
                ELSE
                    kick := TRUE;
                    phase := 5;
                END_IF;
            END_IF;

        5: (* REJECTED *)
            kick := TRUE;
            IF NOT SensorWeight THEN
                kick := FALSE;
                phase := 0;
            END_IF;

        6: (* MOVE_TO_FIRING *)
            MotorForward := TRUE;
            IF SensorFiring THEN
                MotorForward := FALSE;
                phase := 7;
            END_IF;

        7: (* WAIT_FIRING *)
            IF SensorFiring AND firingComplete THEN
                phase := 8;
                MotorForward := TRUE;
            END_IF;

        8: (* MOVE_TO_OUTPUT *)
            MotorForward := TRUE;
            IF SensorOutput THEN
                MotorForward := FALSE;
                CompletionLight := TRUE;
                phase := 9;
            END_IF;

        9: (* OUTPUT_DONE *)
            CompletionLight := SensorOutput;
            IF NOT SensorOutput THEN
                phase := 0;
            END_IF;

        ELSE
            phase := 0;
            kick := FALSE;
            CompletionLight := FALSE;
    END_CASE;
END_IF;

lastMode := Mode;
END_FUNCTION_BLOCK
