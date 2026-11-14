FUNCTION_BLOCK FB_Task
VAR_INPUT
    {attribute 'analysis' := '-27'}
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
    phase : INT := 0;
    lastSetpoint : REAL := 0.0;
    weightOffset : REAL := 0.0;
    scaledOffset : REAL := 0.0;
END_VAR

IF NOT Mode THEN
    // Manual operation resets the automatic route but retains the setpoint.
    phase := 0;
ELSE
    // Exactly one transition is evaluated from the current phase.
    CASE phase OF
        0: // WAIT_FEED
            IF SensorFeed THEN
                phase := 1;
            END_IF;
        1: // MOVE_TO_WASH
            IF SensorWash THEN
                phase := 2;
            END_IF;
        2: // WAIT_WASH
            IF SensorWash AND washComplete THEN
                phase := 3;
            END_IF;
        3: // MOVE_TO_WEIGHT
            IF SensorWeight THEN
                phase := 4;
            END_IF;
        4: // WAIT_WEIGHT
            IF SensorWeight AND weightComplete THEN
                IF (weight >= REAL#100.0) AND (weight <= REAL#200.0) THEN
                    weightOffset := weight - REAL#100.0;
                    scaledOffset := weightOffset * REAL#0.5;
                    lastSetpoint := REAL#500.0 + scaledOffset;
                    phase := 6;
                ELSE
                    phase := 5;
                END_IF;
            END_IF;
        5: // REJECT
            IF NOT SensorWeight THEN
                phase := 0;
            END_IF;
        6: // MOVE_TO_FIRING
            IF SensorFiring THEN
                phase := 7;
            END_IF;
        7: // WAIT_FIRING
            IF SensorFiring AND firingComplete THEN
                phase := 8;
            END_IF;
        8: // MOVE_TO_OUTPUT
            IF SensorOutput THEN
                phase := 9;
            END_IF;
        9: // OUTPUT_DONE
            IF NOT SensorOutput THEN
                phase := 0;
            END_IF;
        ELSE
            phase := 0;
    END_CASE;
END_IF;

IF Mode THEN
    MotorForward := (phase = 1) OR (phase = 3) OR (phase = 6) OR (phase = 8);
    MotorReverse := FALSE;
    kick := phase = 5;
    CompletionLight := phase = 9;
ELSE
    MotorForward := ForwardButton AND NOT ReverseButton;
    MotorReverse := ReverseButton AND NOT ForwardButton;
    kick := FALSE;
    CompletionLight := FALSE;
END_IF;
firingTemp := lastSetpoint;
END_FUNCTION_BLOCK
