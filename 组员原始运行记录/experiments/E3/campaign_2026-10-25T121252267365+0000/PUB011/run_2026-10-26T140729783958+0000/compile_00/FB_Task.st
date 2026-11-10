FUNCTION_BLOCK FB_Task
VAR_INPUT
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
    MotorForward : BOOL;
    MotorReverse : BOOL;
    CompletionLight : BOOL;
END_VAR
VAR
    phase : E_Phase := E_Phase.WAIT_A;
    CompletionLatched : BOOL := FALSE;
END_VAR

MotorForward := FALSE;
MotorReverse := FALSE;

IF NOT Mode THEN
    phase := E_Phase.WAIT_A;
    CompletionLatched := FALSE;
    IF ForwardButton AND NOT ReverseButton THEN
        MotorForward := TRUE;
    ELSIF ReverseButton AND NOT ForwardButton THEN
        MotorReverse := TRUE;
    END_IF;
ELSE
    MotorReverse := FALSE;
    CASE phase OF
        E_Phase.WAIT_A:
            IF SensorA AND ButtonA THEN
                phase := E_Phase.MOVE_AB;
                MotorForward := TRUE;
            END_IF;

        E_Phase.MOVE_AB:
            IF SensorB THEN
                phase := E_Phase.WAIT_B;
                MotorForward := FALSE;
            ELSE
                MotorForward := TRUE;
            END_IF;

        E_Phase.WAIT_B:
            IF SensorB AND ButtonB THEN
                phase := E_Phase.MOVE_BC;
                MotorForward := TRUE;
            END_IF;

        E_Phase.MOVE_BC:
            IF SensorC THEN
                phase := E_Phase.WAIT_C;
                MotorForward := FALSE;
            ELSE
                MotorForward := TRUE;
            END_IF;

        E_Phase.WAIT_C:
            IF NOT SensorC THEN
                CompletionLatched := FALSE;
                phase := E_Phase.WAIT_A;
            ELSE
                IF ButtonC THEN
                    CompletionLatched := TRUE;
                END_IF;
            END_IF;

        ELSE
            phase := E_Phase.WAIT_A;
            CompletionLatched := FALSE;
    END_CASE;
END_IF;

IF Mode THEN
    CompletionLight := CompletionLatched AND SensorC;
ELSE
    CompletionLight := FALSE;
END_IF;
END_FUNCTION_BLOCK
