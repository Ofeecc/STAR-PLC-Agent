TYPE E_TaskPhase :
(
    WAIT_A,
    MOVE_AB,
    WAIT_B,
    MOVE_BC,
    WAIT_C,
    DONE
);
END_TYPE

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
    phase : E_TaskPhase := E_TaskPhase.WAIT_A;
END_VAR

IF NOT Mode THEN
    phase := E_TaskPhase.WAIT_A;
    MotorReverse := ReverseButton AND NOT ForwardButton;
    MotorForward := ForwardButton AND NOT ReverseButton;
    CompletionLight := FALSE;
ELSE
    MotorForward := FALSE;
    MotorReverse := FALSE;
    CompletionLight := FALSE;

    CASE phase OF
        E_TaskPhase.WAIT_A:
            IF SensorA AND ButtonA THEN
                phase := E_TaskPhase.MOVE_AB;
                MotorForward := TRUE;
            END_IF;

        E_TaskPhase.MOVE_AB:
            IF SensorB THEN
                phase := E_TaskPhase.WAIT_B;
            ELSE
                MotorForward := TRUE;
            END_IF;

        E_TaskPhase.WAIT_B:
            IF SensorB AND ButtonB THEN
                phase := E_TaskPhase.MOVE_BC;
                MotorForward := TRUE;
            END_IF;

        E_TaskPhase.MOVE_BC:
            IF SensorC THEN
                phase := E_TaskPhase.WAIT_C;
            ELSE
                MotorForward := TRUE;
            END_IF;

        E_TaskPhase.WAIT_C:
            IF SensorC AND ButtonC THEN
                phase := E_TaskPhase.DONE;
                CompletionLight := TRUE;
            END_IF;

        E_TaskPhase.DONE:
            IF SensorC THEN
                CompletionLight := TRUE;
            ELSE
                phase := E_TaskPhase.WAIT_A;
            END_IF;
    END_CASE;
END_IF;
END_FUNCTION_BLOCK
