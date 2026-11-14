TYPE E_Phase :
(
    MANUAL := 0,
    WAIT_A := 1,
    MOVE_AB := 2,
    WAIT_B := 3,
    MOVE_BC := 4,
    WAIT_C := 5,
    DONE := 6
);
END_TYPE

FUNCTION_BLOCK FB_Task
VAR_INPUT
    {attribute 'analysis' := '-27'}
    Mode : BOOL;
    ForwardButton : BOOL;
    ReverseButton : BOOL;
    SensorA : BOOL;
    SensorB : BOOL;
    SensorC : BOOL;
    ButtonA : BOOL;
    ButtonB : BOOL;
    ButtonC : BOOL;
END_VAR
VAR_OUTPUT
    MotorForward : BOOL := FALSE;
    MotorReverse : BOOL := FALSE;
    CompletionLight : BOOL := FALSE;
END_VAR
VAR
    phase : E_Phase := E_Phase.WAIT_A;
END_VAR

// Stage 1/2: mode reset and at most one automatic phase transition per scan
IF NOT Mode THEN
    phase := E_Phase.MANUAL;
ELSIF phase = E_Phase.MANUAL THEN
    phase := E_Phase.WAIT_A;
ELSE
    CASE phase OF
        E_Phase.WAIT_A:
            IF SensorA AND ButtonA THEN
                phase := E_Phase.MOVE_AB;
            END_IF;
        E_Phase.MOVE_AB:
            IF SensorB THEN
                phase := E_Phase.WAIT_B;
            END_IF;
        E_Phase.WAIT_B:
            IF SensorB AND ButtonB THEN
                phase := E_Phase.MOVE_BC;
            END_IF;
        E_Phase.MOVE_BC:
            IF SensorC THEN
                phase := E_Phase.WAIT_C;
            END_IF;
        E_Phase.WAIT_C:
            IF SensorC AND ButtonC THEN
                phase := E_Phase.DONE;
            END_IF;
        E_Phase.DONE:
            IF NOT SensorC THEN
                phase := E_Phase.WAIT_A;
            END_IF;
        ELSE
            phase := E_Phase.WAIT_A;
    END_CASE;
END_IF

// Stage 4: unified output assignment from post-transition state
MotorForward := FALSE;
MotorReverse := FALSE;
CompletionLight := FALSE;

IF NOT Mode THEN
    IF ForwardButton AND NOT ReverseButton THEN
        MotorForward := TRUE;
    ELSIF ReverseButton AND NOT ForwardButton THEN
        MotorReverse := TRUE;
    END_IF;
ELSE
    CASE phase OF
        E_Phase.MOVE_AB:
            MotorForward := TRUE;
        E_Phase.MOVE_BC:
            MotorForward := TRUE;
        E_Phase.DONE:
            CompletionLight := SensorC;
    END_CASE;
END_IF

// Safety interlocks: no forward in automatic mode while SensorC is present;
// forward and reverse must never be active together.
IF Mode AND SensorC THEN
    MotorForward := FALSE;
END_IF
IF MotorForward AND MotorReverse THEN
    MotorForward := FALSE;
    MotorReverse := FALSE;
END_IF
END_FUNCTION_BLOCK
