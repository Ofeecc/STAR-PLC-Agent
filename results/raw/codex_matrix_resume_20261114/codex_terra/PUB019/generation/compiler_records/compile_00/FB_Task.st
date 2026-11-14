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
    selectedMode : INT := 0;
    previousMode : INT := 0;
    modeInitialized : BOOL := FALSE;
    previousStart : BOOL := FALSE;
    startEdge : BOOL := FALSE;
    phase : INT := 1;
    busy : BOOL := FALSE;
    completed : BOOL := FALSE;
END_VAR

MoveDown := FALSE;
MoveUp := FALSE;
MoveLeft := FALSE;
MoveRight := FALSE;
ActivateGrip := FALSE;
ActivateRelease := FALSE;

selectedMode := 0;
IF ManualMode THEN
    selectedMode := 1;
ELSIF SingleStepMode THEN
    selectedMode := 2;
ELSIF SingleCycleMode THEN
    selectedMode := 3;
ELSIF ContinuousMode THEN
    selectedMode := 4;
END_IF;

startEdge := Start AND NOT previousStart;
previousStart := Start;
IF NOT modeInitialized THEN
    modeInitialized := TRUE;
    previousMode := selectedMode;
END_IF;

IF NOT EmergencyStop THEN
    phase := 1;
    busy := FALSE;
ELSIF selectedMode <> previousMode THEN
    previousMode := selectedMode;
    phase := 1;
    busy := FALSE;
ELSIF selectedMode = 0 THEN
    phase := 1;
    busy := FALSE;
ELSIF selectedMode = 1 THEN
    phase := 1;
    busy := FALSE;
    MoveDown := DownButton AND NOT UpButton AND NOT DownLimitSwitch;
    MoveUp := UpButton AND NOT DownButton AND NOT UpLimitSwitch;
    MoveLeft := LeftButton AND NOT RightButton AND NOT LeftLimitSwitch;
    MoveRight := RightButton AND NOT LeftButton AND NOT RightLimitSwitch;
    ActivateGrip := GripButton AND NOT ReleaseButton AND NOT GripLimitSwitch;
    ActivateRelease := ReleaseButton AND NOT GripButton AND NOT ReleaseLimitSwitch;
ELSE
    IF busy THEN
        completed := FALSE;
        CASE phase OF
            1, 5: completed := DownLimitSwitch;
            2: completed := GripLimitSwitch;
            3, 7: completed := UpLimitSwitch;
            4: completed := RightLimitSwitch;
            6: completed := ReleaseLimitSwitch;
            8: completed := LeftLimitSwitch;
        END_CASE;
        IF completed THEN
            IF phase = 8 THEN
                phase := 1;
                IF selectedMode <> 4 THEN
                    busy := FALSE;
                END_IF;
            ELSE
                phase := phase + 1;
                IF selectedMode = 2 THEN
                    busy := FALSE;
                END_IF;
            END_IF;
        END_IF;
    ELSIF startEdge AND ((phase <> 1) OR (UpLimitSwitch AND LeftLimitSwitch)) THEN
        busy := TRUE;
    END_IF;

    IF busy THEN
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
