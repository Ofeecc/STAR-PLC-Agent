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
    phase : E_TaskPhase := E_TaskPhase.WAIT_A;
END_VAR

IF NOT Mode THEN
    phase := E_TaskPhase.WAIT_A;
ELSE
    CASE phase OF
        E_TaskPhase.WAIT_A:
            IF SensorA AND ButtonA THEN
                phase := E_TaskPhase.MOVE_AB;
            END_IF;
        E_TaskPhase.MOVE_AB:
            IF SensorB THEN
                phase := E_TaskPhase.WAIT_B;
            END_IF;
        E_TaskPhase.WAIT_B:
            IF SensorB AND ButtonB THEN
                phase := E_TaskPhase.MOVE_BC;
            END_IF;
        E_TaskPhase.MOVE_BC:
            IF SensorC THEN
                phase := E_TaskPhase.WAIT_C;
            END_IF;
        E_TaskPhase.WAIT_C:
            IF SensorC AND ButtonC THEN
                phase := E_TaskPhase.DONE;
            END_IF;
        E_TaskPhase.DONE:
            IF NOT SensorC THEN
                phase := E_TaskPhase.WAIT_A;
            END_IF;
    ELSE
        phase := E_TaskPhase.WAIT_A;
    END_CASE;
END_IF;

MotorForward := (NOT Mode AND ForwardButton AND NOT ReverseButton)
    OR (Mode AND ((phase = E_TaskPhase.MOVE_AB) OR (phase = E_TaskPhase.MOVE_BC)));
MotorReverse := NOT Mode AND ReverseButton AND NOT ForwardButton;
CompletionLight := Mode AND (phase = E_TaskPhase.DONE);
END_FUNCTION_BLOCK
