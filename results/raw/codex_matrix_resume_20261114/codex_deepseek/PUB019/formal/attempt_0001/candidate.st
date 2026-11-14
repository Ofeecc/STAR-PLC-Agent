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
    PrevMode : INT := 0;
    FirstScan : BOOL := TRUE;
    NextAction : INT := 1;
    Busy : BOOL := FALSE;
    StartPrev : BOOL := FALSE;
    SelectedMode : INT;
    ModeChanged : BOOL;
    StartEdge : BOOL;
    Done : BOOL;
    ReqDown : BOOL;
    ReqUp : BOOL;
    ReqLeft : BOOL;
    ReqRight : BOOL;
    ReqGrip : BOOL;
    ReqRelease : BOOL;
END_VAR

SelectedMode := 0;
IF ManualMode THEN
    SelectedMode := 1;
ELSIF SingleStepMode THEN
    SelectedMode := 2;
ELSIF SingleCycleMode THEN
    SelectedMode := 3;
ELSIF ContinuousMode THEN
    SelectedMode := 4;
END_IF

ModeChanged := (NOT FirstScan) AND (SelectedMode <> PrevMode);
StartEdge := Start AND NOT StartPrev;

ReqDown := FALSE;
ReqUp := FALSE;
ReqLeft := FALSE;
ReqRight := FALSE;
ReqGrip := FALSE;
ReqRelease := FALSE;
Done := FALSE;

IF NOT EmergencyStop THEN
    Busy := FALSE;
    NextAction := 1;
ELSIF SelectedMode = 0 THEN
    Busy := FALSE;
    NextAction := 1;
ELSIF ModeChanged THEN
    Busy := FALSE;
    NextAction := 1;
ELSE
    CASE SelectedMode OF
    1:
        Busy := FALSE;
        NextAction := 1;
        ReqDown := DownButton AND NOT UpButton;
        ReqUp := UpButton AND NOT DownButton;
        ReqLeft := LeftButton AND NOT RightButton;
        ReqRight := RightButton AND NOT LeftButton;
        ReqGrip := GripButton AND NOT ReleaseButton;
        ReqRelease := ReleaseButton AND NOT GripButton;
    2:
        IF Busy THEN
            CASE NextAction OF
            1: Done := DownLimitSwitch;
            2: Done := GripLimitSwitch;
            3: Done := UpLimitSwitch;
            4: Done := RightLimitSwitch;
            5: Done := DownLimitSwitch;
            6: Done := ReleaseLimitSwitch;
            7: Done := UpLimitSwitch;
            8: Done := LeftLimitSwitch;
            ELSE Done := FALSE;
            END_CASE
            IF Done THEN
                Busy := FALSE;
                NextAction := NextAction + 1;
                IF NextAction > 8 THEN
                    NextAction := 1;
                END_IF
            ELSE
                CASE NextAction OF
                1: ReqDown := TRUE;
                2: ReqGrip := TRUE;
                3: ReqUp := TRUE;
                4: ReqRight := TRUE;
                5: ReqDown := TRUE;
                6: ReqRelease := TRUE;
                7: ReqUp := TRUE;
                8: ReqLeft := TRUE;
                END_CASE
            END_IF
        ELSE
            IF StartEdge AND ((NextAction <> 1) OR (UpLimitSwitch AND LeftLimitSwitch)) THEN
                Busy := TRUE;
                CASE NextAction OF
                1: ReqDown := TRUE;
                2: ReqGrip := TRUE;
                3: ReqUp := TRUE;
                4: ReqRight := TRUE;
                5: ReqDown := TRUE;
                6: ReqRelease := TRUE;
                7: ReqUp := TRUE;
                8: ReqLeft := TRUE;
                END_CASE
            END_IF
        END_IF
    3:
        IF Busy THEN
            CASE NextAction OF
            1: Done := DownLimitSwitch;
            2: Done := GripLimitSwitch;
            3: Done := UpLimitSwitch;
            4: Done := RightLimitSwitch;
            5: Done := DownLimitSwitch;
            6: Done := ReleaseLimitSwitch;
            7: Done := UpLimitSwitch;
            8: Done := LeftLimitSwitch;
            ELSE Done := FALSE;
            END_CASE
            IF Done THEN
                IF NextAction = 8 THEN
                    Busy := FALSE;
                    NextAction := 1;
                ELSE
                    NextAction := NextAction + 1;
                    CASE NextAction OF
                    1: ReqDown := TRUE;
                    2: ReqGrip := TRUE;
                    3: ReqUp := TRUE;
                    4: ReqRight := TRUE;
                    5: ReqDown := TRUE;
                    6: ReqRelease := TRUE;
                    7: ReqUp := TRUE;
                    8: ReqLeft := TRUE;
                    END_CASE
                END_IF
            ELSE
                CASE NextAction OF
                1: ReqDown := TRUE;
                2: ReqGrip := TRUE;
                3: ReqUp := TRUE;
                4: ReqRight := TRUE;
                5: ReqDown := TRUE;
                6: ReqRelease := TRUE;
                7: ReqUp := TRUE;
                8: ReqLeft := TRUE;
                END_CASE
            END_IF
        ELSE
            IF StartEdge AND UpLimitSwitch AND LeftLimitSwitch THEN
                Busy := TRUE;
                NextAction := 1;
                ReqDown := TRUE;
            END_IF
        END_IF
    4:
        IF Busy THEN
            CASE NextAction OF
            1: Done := DownLimitSwitch;
            2: Done := GripLimitSwitch;
            3: Done := UpLimitSwitch;
            4: Done := RightLimitSwitch;
            5: Done := DownLimitSwitch;
            6: Done := ReleaseLimitSwitch;
            7: Done := UpLimitSwitch;
            8: Done := LeftLimitSwitch;
            ELSE Done := FALSE;
            END_CASE
            IF Done THEN
                IF NextAction = 8 THEN
                    NextAction := 1;
                    Busy := TRUE;
                    ReqDown := TRUE;
                ELSE
                    NextAction := NextAction + 1;
                    CASE NextAction OF
                    1: ReqDown := TRUE;
                    2: ReqGrip := TRUE;
                    3: ReqUp := TRUE;
                    4: ReqRight := TRUE;
                    5: ReqDown := TRUE;
                    6: ReqRelease := TRUE;
                    7: ReqUp := TRUE;
                    8: ReqLeft := TRUE;
                    END_CASE
                END_IF
            ELSE
                CASE NextAction OF
                1: ReqDown := TRUE;
                2: ReqGrip := TRUE;
                3: ReqUp := TRUE;
                4: ReqRight := TRUE;
                5: ReqDown := TRUE;
                6: ReqRelease := TRUE;
                7: ReqUp := TRUE;
                8: ReqLeft := TRUE;
                END_CASE
            END_IF
        ELSE
            IF StartEdge AND UpLimitSwitch AND LeftLimitSwitch THEN
                Busy := TRUE;
                NextAction := 1;
                ReqDown := TRUE;
            END_IF
        END_IF
    END_CASE
END_IF

MoveDown := ReqDown AND EmergencyStop AND (SelectedMode <> 0) AND NOT ModeChanged AND NOT DownLimitSwitch;
MoveUp := ReqUp AND EmergencyStop AND (SelectedMode <> 0) AND NOT ModeChanged AND NOT UpLimitSwitch;
MoveLeft := ReqLeft AND EmergencyStop AND (SelectedMode <> 0) AND NOT ModeChanged AND NOT LeftLimitSwitch;
MoveRight := ReqRight AND EmergencyStop AND (SelectedMode <> 0) AND NOT ModeChanged AND NOT RightLimitSwitch;
ActivateGrip := ReqGrip AND EmergencyStop AND (SelectedMode <> 0) AND NOT ModeChanged AND NOT GripLimitSwitch;
ActivateRelease := ReqRelease AND EmergencyStop AND (SelectedMode <> 0) AND NOT ModeChanged AND NOT ReleaseLimitSwitch;

PrevMode := SelectedMode;
FirstScan := FALSE;
StartPrev := Start;
END_FUNCTION_BLOCK
