FUNCTION_BLOCK FB_Task
VAR_INPUT
    ManualMode : BOOL;
    SingleStepMode : BOOL;
    SingleCycleMode : BOOL;
    ContinuousMode : BOOL;
    EmergencyStop : BOOL;
    Start : BOOL;
    DownButton : BOOL;
    UpButton : BOOL;
    LeftButton : BOOL;
    RightButton : BOOL;
    GripButton : BOOL;
    ReleaseButton : BOOL;
    DownLimitSwitch : BOOL;
    UpLimitSwitch : BOOL;
    LeftLimitSwitch : BOOL;
    RightLimitSwitch : BOOL;
    GripLimitSwitch : BOOL;
    ReleaseLimitSwitch : BOOL;
END_VAR
VAR_OUTPUT
    MoveDown : BOOL;
    MoveUp : BOOL;
    MoveLeft : BOOL;
    MoveRight : BOOL;
    ActivateGrip : BOOL;
    ActivateRelease : BOOL;
END_VAR
VAR
    xPhase : INT := 1;
    xBusy : BOOL := FALSE;
    xPrevStart : BOOL := FALSE;
    xPrevMode : INT := 0;
    xMode : INT;
    xStartEdge : BOOL;
    xFeedback : BOOL;
END_VAR

xStartEdge := Start AND NOT xPrevStart;
xPrevStart := Start;

xMode := 0;
IF ManualMode THEN
    xMode := 1;
ELSIF SingleStepMode THEN
    xMode := 2;
ELSIF SingleCycleMode THEN
    xMode := 3;
ELSIF ContinuousMode THEN
    xMode := 4;
END_IF;

MoveDown := FALSE;
MoveUp := FALSE;
MoveLeft := FALSE;
MoveRight := FALSE;
ActivateGrip := FALSE;
ActivateRelease := FALSE;

IF NOT EmergencyStop THEN
    xPhase := 1;
    xBusy := FALSE;
    xPrevMode := xMode;
    RETURN;
END_IF;

IF xMode = 0 THEN
    xPhase := 1;
    xBusy := FALSE;
    xPrevMode := 0;
    RETURN;
END_IF;

IF xMode <> xPrevMode THEN
    xPhase := 1;
    xBusy := FALSE;
    xPrevMode := xMode;
END_IF;

IF xMode = 1 THEN
    xPhase := 1;
    xBusy := FALSE;

    MoveDown := DownButton AND NOT UpButton AND NOT DownLimitSwitch;
    MoveUp := UpButton AND NOT DownButton AND NOT UpLimitSwitch;
    MoveLeft := LeftButton AND NOT RightButton AND NOT LeftLimitSwitch;
    MoveRight := RightButton AND NOT LeftButton AND NOT RightLimitSwitch;
    ActivateGrip := GripButton AND NOT ReleaseButton AND NOT GripLimitSwitch;
    ActivateRelease := ReleaseButton AND NOT GripButton AND NOT ReleaseLimitSwitch;
    RETURN;
END_IF;

IF NOT xBusy THEN
    IF xStartEdge THEN
        IF xPhase = 1 THEN
            IF UpLimitSwitch AND LeftLimitSwitch THEN
                xBusy := TRUE;
            END_IF;
        ELSIF xMode = 2 THEN
            xBusy := TRUE;
        END_IF;
    END_IF;
ELSE
    xFeedback := FALSE;
    CASE xPhase OF
        1, 5:
            xFeedback := DownLimitSwitch;
        2:
            xFeedback := GripLimitSwitch;
        3, 7:
            xFeedback := UpLimitSwitch;
        4:
            xFeedback := RightLimitSwitch;
        6:
            xFeedback := ReleaseLimitSwitch;
        8:
            xFeedback := LeftLimitSwitch;
    END_CASE;

    IF xFeedback THEN
        IF xMode = 2 THEN
            xBusy := FALSE;
            IF xPhase = 8 THEN
                xPhase := 1;
            ELSE
                xPhase := xPhase + 1;
            END_IF;
        ELSIF xPhase = 8 THEN
            xPhase := 1;
            IF xMode = 3 THEN
                xBusy := FALSE;
            END_IF;
        ELSE
            xPhase := xPhase + 1;
        END_IF;
    END_IF;
END_IF;

IF xBusy THEN
    CASE xPhase OF
        1, 5:
            MoveDown := NOT DownLimitSwitch;
        2:
            ActivateGrip := NOT GripLimitSwitch;
        3, 7:
            MoveUp := NOT UpLimitSwitch;
        4:
            MoveRight := NOT RightLimitSwitch;
        6:
            ActivateRelease := NOT ReleaseLimitSwitch;
        8:
            MoveLeft := NOT LeftLimitSwitch;
    END_CASE;
END_IF;
END_FUNCTION_BLOCK
