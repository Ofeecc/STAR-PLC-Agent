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
    MoveDown : BOOL := FALSE;
    MoveUp : BOOL := FALSE;
    MoveLeft : BOOL := FALSE;
    MoveRight : BOOL := FALSE;
    ActivateGrip : BOOL := FALSE;
    ActivateRelease : BOOL := FALSE;
END_VAR
VAR
    previousStart : BOOL := FALSE;
    startEdge : BOOL := FALSE;
    modeInitialized : BOOL := FALSE;
    arm_mode : USINT := 0;
    selectedMode : USINT := 0;
    modeCount : USINT := 0;
    modeChanged : BOOL := FALSE;
    next_step : USINT := 1;
    busy : BOOL := FALSE;
    completion : BOOL := FALSE;
    outputEnable : BOOL := FALSE;
END_VAR

(* Ordinary PLC logic does not replace a safety-rated emergency-stop system. *)
startEdge := Start AND NOT previousStart;
previousStart := Start;

(* Mode codes: 0 none, 1 manual, 2 step, 3 cycle, 4 continuous, 5 invalid. *)
selectedMode := 0;
modeCount := 0;
IF ManualMode THEN
    selectedMode := 1;
    modeCount := modeCount + 1;
END_IF;
IF SingleStepMode THEN
    selectedMode := 2;
    modeCount := modeCount + 1;
END_IF;
IF SingleCycleMode THEN
    selectedMode := 3;
    modeCount := modeCount + 1;
END_IF;
IF ContinuousMode THEN
    selectedMode := 4;
    modeCount := modeCount + 1;
END_IF;
IF modeCount > 1 THEN
    selectedMode := 5;
END_IF;

modeChanged := modeInitialized AND (selectedMode <> arm_mode);
arm_mode := selectedMode;
modeInitialized := TRUE;
completion := FALSE;

IF NOT EmergencyStop OR modeChanged OR (selectedMode = 0) OR (selectedMode = 5) THEN
    busy := FALSE;
    next_step := 1;
ELSIF selectedMode = 1 THEN
    busy := FALSE;
    next_step := 1;
ELSE
    IF busy THEN
        (* Evaluate only the action that was active at the start of this scan. *)
        CASE next_step OF
            1, 5: completion := DownLimitSwitch;
            2: completion := GripLimitSwitch;
            3, 7: completion := UpLimitSwitch;
            4: completion := RightLimitSwitch;
            6: completion := ReleaseLimitSwitch;
            8: completion := LeftLimitSwitch;
        ELSE
            (* Invalid internal state fails off. *)
            busy := FALSE;
            next_step := 1;
        END_CASE;

        IF completion THEN
            IF SingleStepMode THEN
                busy := FALSE;
                IF next_step = 8 THEN
                    next_step := 1;
                ELSE
                    next_step := next_step + 1;
                END_IF;
            ELSIF next_step = 8 THEN
                next_step := 1;
                IF SingleCycleMode THEN
                    busy := FALSE;
                END_IF;
            ELSE
                next_step := next_step + 1;
            END_IF;
        END_IF;
    ELSIF startEdge THEN
        (* Pose confirmation is required at the beginning of each sequence. *)
        IF (next_step <> 1) OR (UpLimitSwitch AND LeftLimitSwitch) THEN
            busy := TRUE;
        END_IF;
    END_IF;
END_IF;

(* Outputs are derived from the post-transition state and current feedback. *)
outputEnable := EmergencyStop AND NOT modeChanged AND (modeCount = 1);
MoveDown := outputEnable AND NOT DownLimitSwitch AND
    ((ManualMode AND DownButton AND NOT UpButton) OR
     (NOT ManualMode AND busy AND ((next_step = 1) OR (next_step = 5))));
MoveUp := outputEnable AND NOT UpLimitSwitch AND
    ((ManualMode AND UpButton AND NOT DownButton) OR
     (NOT ManualMode AND busy AND ((next_step = 3) OR (next_step = 7))));
MoveLeft := outputEnable AND NOT LeftLimitSwitch AND
    ((ManualMode AND LeftButton AND NOT RightButton) OR
     (NOT ManualMode AND busy AND (next_step = 8)));
MoveRight := outputEnable AND NOT RightLimitSwitch AND
    ((ManualMode AND RightButton AND NOT LeftButton) OR
     (NOT ManualMode AND busy AND (next_step = 4)));
ActivateGrip := outputEnable AND NOT GripLimitSwitch AND
    ((ManualMode AND GripButton AND NOT ReleaseButton) OR
     (NOT ManualMode AND busy AND (next_step = 2)));
ActivateRelease := outputEnable AND NOT ReleaseLimitSwitch AND
    ((ManualMode AND ReleaseButton AND NOT GripButton) OR
     (NOT ManualMode AND busy AND (next_step = 6)));
END_FUNCTION_BLOCK
