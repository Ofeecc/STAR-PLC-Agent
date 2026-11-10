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
    phase : USINT := 1;
    busy : BOOL := FALSE;
    previousStart : BOOL := FALSE;
    previousMode : USINT := 0;
    currentMode : USINT;
    startRising : BOOL;
    actionDone : BOOL;
END_VAR

startRising := Start AND NOT previousStart;
previousStart := Start;

MoveDown := FALSE;
MoveUp := FALSE;
MoveLeft := FALSE;
MoveRight := FALSE;
ActivateGrip := FALSE;
ActivateRelease := FALSE;

currentMode := 0;
IF ManualMode THEN
    currentMode := 1;
ELSIF SingleStepMode THEN
    currentMode := 2;
ELSIF SingleCycleMode THEN
    currentMode := 3;
ELSIF ContinuousMode THEN
    currentMode := 4;
END_IF;

IF NOT EmergencyStop OR (currentMode = 0) OR (currentMode <> previousMode) THEN
    phase := 1;
    busy := FALSE;
END_IF;
previousMode := currentMode;

IF EmergencyStop THEN
    IF currentMode = 1 THEN
        MoveDown := DownButton AND NOT UpButton AND NOT DownLimitSwitch;
        MoveUp := UpButton AND NOT DownButton AND NOT UpLimitSwitch;
        MoveLeft := LeftButton AND NOT RightButton AND NOT LeftLimitSwitch;
        MoveRight := RightButton AND NOT LeftButton AND NOT RightLimitSwitch;
        ActivateGrip := GripButton AND NOT ReleaseButton AND NOT GripLimitSwitch;
        ActivateRelease := ReleaseButton AND NOT GripButton AND NOT ReleaseLimitSwitch;
    ELSIF currentMode = 2 THEN
        IF busy THEN
            actionDone := FALSE;
            CASE phase OF
                1, 5: actionDone := DownLimitSwitch;
                2: actionDone := GripLimitSwitch;
                3, 7: actionDone := UpLimitSwitch;
                4: actionDone := RightLimitSwitch;
                6: actionDone := ReleaseLimitSwitch;
                8: actionDone := LeftLimitSwitch;
            END_CASE;
            IF actionDone THEN
                busy := FALSE;
                IF phase = 8 THEN
                    phase := 1;
                ELSE
                    phase := phase + 1;
                END_IF;
            END_IF;
        ELSIF startRising AND ((phase <> 1) OR (UpLimitSwitch AND LeftLimitSwitch)) THEN
            busy := TRUE;
        END_IF;
    ELSIF (currentMode = 3) OR (currentMode = 4) THEN
        IF busy THEN
            actionDone := FALSE;
            CASE phase OF
                1, 5: actionDone := DownLimitSwitch;
                2: actionDone := GripLimitSwitch;
                3, 7: actionDone := UpLimitSwitch;
                4: actionDone := RightLimitSwitch;
                6: actionDone := ReleaseLimitSwitch;
                8: actionDone := LeftLimitSwitch;
            END_CASE;
            IF actionDone THEN
                IF phase = 8 THEN
                    phase := 1;
                    IF currentMode = 3 THEN
                        busy := FALSE;
                    END_IF;
                ELSE
                    phase := phase + 1;
                END_IF;
            END_IF;
        ELSIF startRising AND UpLimitSwitch AND LeftLimitSwitch THEN
            phase := 1;
            busy := TRUE;
        END_IF;
    END_IF;

    IF busy AND (currentMode >= 2) THEN
        CASE phase OF
            1, 5: MoveDown := NOT DownLimitSwitch;
            2: ActivateGrip := NOT GripLimitSwitch;
            3, 7: MoveUp := NOT UpLimitSwitch;
            4: MoveRight := NOT RightLimitSwitch;
            6: ActivateRelease := NOT ReleaseLimitSwitch;
            8: MoveLeft := NOT LeftLimitSwitch;
        END_CASE;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
