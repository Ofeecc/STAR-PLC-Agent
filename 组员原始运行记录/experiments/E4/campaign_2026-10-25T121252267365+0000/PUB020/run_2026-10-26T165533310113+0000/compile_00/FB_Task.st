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
END_VAR

IF NOT Mode THEN
    phase := 0;
    kick := FALSE;
    CompletionLight := FALSE;
    MotorForward := ForwardButton AND NOT ReverseButton;
    MotorReverse := ReverseButton AND NOT ForwardButton;
ELSE
    MotorForward := FALSE;
    MotorReverse := FALSE;
    kick := FALSE;

    CASE phase OF
        0:
            IF SensorFeed THEN
                phase := 1;
            END_IF;

        1:
            IF SensorWash THEN
                phase := 2;
            END_IF;

        2:
            IF SensorWash AND washComplete THEN
                phase := 3;
            END_IF;

        3:
            IF SensorWeight THEN
                phase := 4;
            END_IF;

        4:
            IF SensorWeight AND weightComplete THEN
                IF (weight >= 100.0) AND (weight <= 200.0) THEN
                    firingTemp := 500.0 + ((weight - 100.0) * 0.5);
                    phase := 5;
                ELSE
                    phase := 9;
                END_IF;
            END_IF;

        5:
            IF SensorFiring THEN
                phase := 6;
            END_IF;

        6:
            IF SensorFiring AND firingComplete THEN
                phase := 7;
            END_IF;

        7:
            IF SensorOutput THEN
                phase := 8;
                CompletionLight := TRUE;
            END_IF;

        8:
            IF SensorOutput THEN
                CompletionLight := TRUE;
            ELSE
                CompletionLight := FALSE;
                phase := 0;
            END_IF;

        9:
            IF NOT SensorWeight THEN
                phase := 0;
            END_IF;

        ELSE
            phase := 0;
            CompletionLight := FALSE;
    END_CASE;

    IF (phase = 1) OR (phase = 3) OR (phase = 5) OR (phase = 7) THEN
        MotorForward := TRUE;
    END_IF;

    IF phase = 9 THEN
        kick := TRUE;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
