TYPE E_Phase :
(
    MANUAL := 0,
    WAIT_FEED := 1,
    MOVE_TO_WASH := 2,
    WAIT_WASH := 3,
    MOVE_TO_WEIGHT := 4,
    WAIT_WEIGHT := 5,
    REJECT_WAIT := 6,
    MOVE_TO_FIRING := 7,
    WAIT_FIRING := 8,
    MOVE_TO_OUTPUT := 9,
    OUTPUT_DONE := 10
);
END_TYPE

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
    phase : E_Phase := E_Phase.WAIT_FEED;
    firingTempState : REAL := 0.0;
    wValue : REAL := 0.0;
END_VAR

// Stage 1: mode handling and automatic state transitions
IF NOT Mode THEN
    phase := E_Phase.MANUAL;
ELSIF phase = E_Phase.MANUAL THEN
    phase := E_Phase.WAIT_FEED;
ELSE
    CASE phase OF
        E_Phase.WAIT_FEED:
            IF SensorFeed THEN
                phase := E_Phase.MOVE_TO_WASH;
            END_IF;
        E_Phase.MOVE_TO_WASH:
            IF SensorWash THEN
                phase := E_Phase.WAIT_WASH;
            END_IF;
        E_Phase.WAIT_WASH:
            IF washComplete THEN
                phase := E_Phase.MOVE_TO_WEIGHT;
            END_IF;
        E_Phase.MOVE_TO_WEIGHT:
            IF SensorWeight THEN
                phase := E_Phase.WAIT_WEIGHT;
            END_IF;
        E_Phase.WAIT_WEIGHT:
            IF SensorWeight AND weightComplete THEN
                wValue := weight;
                IF (wValue >= 100.0) AND (wValue <= 200.0) THEN
                    firingTempState := 500.0 + (wValue - 100.0) * 0.5;
                    phase := E_Phase.MOVE_TO_FIRING;
                ELSE
                    phase := E_Phase.REJECT_WAIT;
                END_IF;
            END_IF;
        E_Phase.REJECT_WAIT:
            IF NOT SensorWeight THEN
                phase := E_Phase.WAIT_FEED;
            END_IF;
        E_Phase.MOVE_TO_FIRING:
            IF SensorFiring THEN
                phase := E_Phase.WAIT_FIRING;
            END_IF;
        E_Phase.WAIT_FIRING:
            IF firingComplete THEN
                phase := E_Phase.MOVE_TO_OUTPUT;
            END_IF;
        E_Phase.MOVE_TO_OUTPUT:
            IF SensorOutput THEN
                phase := E_Phase.OUTPUT_DONE;
            END_IF;
        E_Phase.OUTPUT_DONE:
            IF NOT SensorOutput THEN
                phase := E_Phase.WAIT_FEED;
            END_IF;
        E_Phase.MANUAL:
            phase := E_Phase.WAIT_FEED;
        ELSE
            phase := E_Phase.WAIT_FEED;
    END_CASE;
END_IF;

// Stage 4: unified output assignments
firingTemp := firingTempState;

IF NOT Mode THEN
    MotorForward := ForwardButton AND NOT ReverseButton;
    MotorReverse := ReverseButton AND NOT ForwardButton;
    kick := FALSE;
    CompletionLight := FALSE;
ELSE
    MotorReverse := FALSE;
    IF (phase = E_Phase.MOVE_TO_WASH) OR (phase = E_Phase.MOVE_TO_WEIGHT) OR (phase = E_Phase.MOVE_TO_FIRING) OR (phase = E_Phase.MOVE_TO_OUTPUT) THEN
        MotorForward := TRUE;
    ELSE
        MotorForward := FALSE;
    END_IF;
    kick := (phase = E_Phase.REJECT_WAIT);
    CompletionLight := (phase = E_Phase.OUTPUT_DONE);
END_IF;

// Final safety interlock
IF MotorForward AND MotorReverse THEN
    MotorForward := FALSE;
    MotorReverse := FALSE;
END_IF;
END_FUNCTION_BLOCK
