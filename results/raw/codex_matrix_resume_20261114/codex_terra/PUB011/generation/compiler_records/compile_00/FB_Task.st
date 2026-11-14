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
    MotorForward : BOOL := FALSE;
    MotorReverse : BOOL := FALSE;
    CompletionLight : BOOL := FALSE;
END_VAR
VAR
    Phase : INT := 0;
END_VAR

IF NOT Mode THEN
    Phase := 0;
    MotorForward := ForwardButton AND NOT ReverseButton;
    MotorReverse := ReverseButton AND NOT ForwardButton;
    CompletionLight := FALSE;
ELSE
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
                Phase := 5;
            END_IF;
        5:
            IF NOT SensorC THEN
                Phase := 0;
            END_IF;
    ELSE
        Phase := 0;
    END_CASE;
    MotorForward := (Phase = 1) OR (Phase = 3);
    MotorReverse := FALSE;
    CompletionLight := (Phase = 5);
END_IF;
END_FUNCTION_BLOCK
