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
    MotorForward : BOOL := FALSE;
    MotorReverse : BOOL := FALSE;
    kick : BOOL := FALSE;
    CompletionLight : BOOL := FALSE;
    firingTemp : REAL := 0.0;
END_VAR
VAR
    phase : USINT := 0;
END_VAR

MotorForward := FALSE;
MotorReverse := FALSE;
kick := FALSE;
CompletionLight := FALSE;

IF NOT Mode THEN
    phase := 0;
    MotorForward := ForwardButton AND NOT ReverseButton;
    MotorReverse := ReverseButton AND NOT ForwardButton;
ELSE
    CASE phase OF
        0:
            IF SensorFeed THEN
                phase := 1;
                MotorForward := TRUE;
            END_IF;
        1:
            IF SensorWash THEN
                phase := 2;
            ELSE
                MotorForward := TRUE;
            END_IF;
        2:
            IF SensorWash AND washComplete THEN
                phase := 3;
                MotorForward := TRUE;
            END_IF;
        3:
            IF SensorWeight THEN
                phase := 4;
            ELSE
                MotorForward := TRUE;
            END_IF;
        4:
            IF SensorWeight AND weightComplete THEN
                IF (weight >= 100.0) AND (weight <= 200.0) THEN
                    firingTemp := 500.0 + (weight - 100.0) * 0.5;
                    phase := 5;
                    MotorForward := TRUE;
                ELSE
                    phase := 9;
                    kick := TRUE;
                END_IF;
            END_IF;
        5:
            IF SensorFiring THEN
                phase := 6;
            ELSE
                MotorForward := TRUE;
            END_IF;
        6:
            IF SensorFiring AND firingComplete THEN
                phase := 7;
                MotorForward := TRUE;
            END_IF;
        7:
            IF SensorOutput THEN
                phase := 8;
                CompletionLight := TRUE;
            ELSE
                MotorForward := TRUE;
            END_IF;
        8:
            IF SensorOutput THEN
                CompletionLight := TRUE;
            ELSE
                phase := 0;
            END_IF;
        9:
            IF SensorWeight THEN
                kick := TRUE;
            ELSE
                phase := 0;
            END_IF;
    ELSE
        phase := 0;
    END_CASE;
END_IF;
END_FUNCTION_BLOCK
