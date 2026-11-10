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
    Phase : INT := 0;
END_VAR

MotorForward := FALSE;
MotorReverse := FALSE;

IF NOT Mode THEN
    Phase := 0;
    CompletionLight := FALSE;
    MotorForward := ForwardButton AND NOT ReverseButton;
    MotorReverse := ReverseButton AND NOT ForwardButton;
ELSE
    MotorReverse := FALSE;

    IF NOT SensorC THEN
        CompletionLight := FALSE;
    END_IF;

    CASE Phase OF
        0:
            IF SensorA AND ButtonA THEN
                Phase := 1;
            END_IF;
        1:
            IF SensorB THEN
                Phase := 2;
            END_IF;
        2:
            IF SensorB AND ButtonB THEN
                Phase := 3;
            END_IF;
        3:
            IF SensorC THEN
                Phase := 4;
            END_IF;
        4:
            IF SensorC AND ButtonC THEN
                CompletionLight := TRUE;
            END_IF;
    ELSE
        Phase := 0;
        CompletionLight := FALSE;
    END_CASE;

    MotorForward := (Phase = 1) OR (Phase = 3);
END_IF;
END_FUNCTION_BLOCK
