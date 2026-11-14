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
    phase : INT := 0;
    busy : BOOL := FALSE;
    step_wait : BOOL := FALSE;
    next_step : INT := 1;
    start_mem : BOOL := FALSE;
    mode_prev : INT := 0;
    first_scan : BOOL := TRUE;
    arm_mode : INT := 0;
    mode_changed : BOOL := FALSE;
    start_rise : BOOL := FALSE;
    selected_mode : INT := 0;
    mode_count : INT := 0;
    invalid_mode : BOOL := FALSE;
    safe : BOOL := FALSE;
    reset_active : BOOL := FALSE;
    cmd_down : BOOL := FALSE;
    cmd_up : BOOL := FALSE;
    cmd_left : BOOL := FALSE;
    cmd_right : BOOL := FALSE;
    cmd_grip : BOOL := FALSE;
    cmd_release : BOOL := FALSE;
    auto_complete : BOOL := FALSE;
    can_manual : BOOL := FALSE;
END_VAR

// Stage 1: edge sampling and mode selection
selected_mode := 0;
mode_count := 0;
IF ManualMode THEN mode_count := mode_count + 1; END_IF;
IF SingleStepMode THEN mode_count := mode_count + 1; END_IF;
IF SingleCycleMode THEN mode_count := mode_count + 1; END_IF;
IF ContinuousMode THEN mode_count := mode_count + 1; END_IF;
invalid_mode := (mode_count > 1);
IF invalid_mode THEN
    selected_mode := 0;
ELSIF ManualMode THEN
    selected_mode := 1;
ELSIF SingleStepMode THEN
    selected_mode := 2;
ELSIF SingleCycleMode THEN
    selected_mode := 3;
ELSIF ContinuousMode THEN
    selected_mode := 4;
ELSE
    selected_mode := 0;
END_IF;
safe := EmergencyStop;
start_rise := Start AND NOT start_mem;
IF first_scan THEN
    mode_changed := FALSE;
ELSE
    mode_changed := (selected_mode <> mode_prev);
END_IF;
start_mem := Start;
mode_prev := selected_mode;
first_scan := FALSE;
arm_mode := selected_mode;

// Stage 2: reset priority and state transitions
reset_active := (NOT safe) OR (selected_mode = 0) OR mode_changed;
IF reset_active THEN
    phase := 0;
    busy := FALSE;
    step_wait := FALSE;
    next_step := 1;
ELSIF selected_mode = 1 THEN
    phase := 0;
    busy := FALSE;
    step_wait := FALSE;
    next_step := 1;
ELSE
    auto_complete := FALSE;
    CASE phase OF
        1: auto_complete := DownLimitSwitch;
        2: auto_complete := GripLimitSwitch;
        3: auto_complete := UpLimitSwitch;
        4: auto_complete := RightLimitSwitch;
        5: auto_complete := DownLimitSwitch;
        6: auto_complete := ReleaseLimitSwitch;
        7: auto_complete := UpLimitSwitch;
        8: auto_complete := LeftLimitSwitch;
    ELSE
        auto_complete := FALSE;
    END_CASE;
    IF phase = 0 THEN
        IF start_rise AND UpLimitSwitch AND LeftLimitSwitch THEN
            phase := 1;
            busy := TRUE;
            step_wait := FALSE;
            next_step := 2;
        END_IF;
    ELSIF phase = 9 THEN
        IF (selected_mode = 2) AND start_rise AND ((next_step <> 1) OR (UpLimitSwitch AND LeftLimitSwitch)) THEN
            phase := next_step;
            busy := TRUE;
            step_wait := FALSE;
        END_IF;
    ELSIF (phase >= 1) AND (phase <= 8) AND busy AND auto_complete THEN
        IF phase = 8 THEN
            IF selected_mode = 2 THEN
                next_step := 1;
                phase := 9;
                busy := FALSE;
                step_wait := TRUE;
            ELSIF selected_mode = 3 THEN
                next_step := 1;
                phase := 0;
                busy := FALSE;
                step_wait := FALSE;
            ELSE
                next_step := 2;
                phase := 1;
                busy := TRUE;
                step_wait := FALSE;
            END_IF;
        ELSE
            IF selected_mode = 2 THEN
                next_step := phase + 1;
                phase := 9;
                busy := FALSE;
                step_wait := TRUE;
            ELSIF selected_mode = 3 THEN
                next_step := phase + 1;
                phase := phase + 1;
                busy := TRUE;
                step_wait := FALSE;
            ELSE
                next_step := phase + 1;
                phase := phase + 1;
                busy := TRUE;
                step_wait := FALSE;
            END_IF;
        END_IF;
    END_IF;
END_IF;

// Stage 3: no IEC timers are used.

// Stage 4: unified output assignment with same-scan safety gates
cmd_down := FALSE;
cmd_up := FALSE;
cmd_left := FALSE;
cmd_right := FALSE;
cmd_grip := FALSE;
cmd_release := FALSE;
can_manual := FALSE;
IF safe AND (NOT mode_changed) AND (selected_mode <> 0) THEN
    IF selected_mode = 1 THEN
        can_manual := TRUE;
        cmd_down := DownButton AND NOT UpButton AND NOT DownLimitSwitch;
        cmd_up := UpButton AND NOT DownButton AND NOT UpLimitSwitch;
        cmd_left := LeftButton AND NOT RightButton AND NOT LeftLimitSwitch;
        cmd_right := RightButton AND NOT LeftButton AND NOT RightLimitSwitch;
        cmd_grip := GripButton AND NOT ReleaseButton AND NOT GripLimitSwitch;
        cmd_release := ReleaseButton AND NOT GripButton AND NOT ReleaseLimitSwitch;
    ELSE
        CASE phase OF
            1: cmd_down := TRUE;
            2: cmd_grip := TRUE;
            3: cmd_up := TRUE;
            4: cmd_right := TRUE;
            5: cmd_down := TRUE;
            6: cmd_release := TRUE;
            7: cmd_up := TRUE;
            8: cmd_left := TRUE;
        ELSE
            cmd_down := FALSE;
        END_CASE;
    END_IF;
END_IF;
IF DownLimitSwitch THEN cmd_down := FALSE; END_IF;
IF UpLimitSwitch THEN cmd_up := FALSE; END_IF;
IF LeftLimitSwitch THEN cmd_left := FALSE; END_IF;
IF RightLimitSwitch THEN cmd_right := FALSE; END_IF;
IF GripLimitSwitch THEN cmd_grip := FALSE; END_IF;
IF ReleaseLimitSwitch THEN cmd_release := FALSE; END_IF;
IF cmd_down AND cmd_up THEN
    cmd_down := FALSE;
    cmd_up := FALSE;
END_IF;
IF cmd_left AND cmd_right THEN
    cmd_left := FALSE;
    cmd_right := FALSE;
END_IF;
IF cmd_grip AND cmd_release THEN
    cmd_grip := FALSE;
    cmd_release := FALSE;
END_IF;
IF (NOT safe) OR mode_changed OR (selected_mode = 0) THEN
    cmd_down := FALSE;
    cmd_up := FALSE;
    cmd_left := FALSE;
    cmd_right := FALSE;
    cmd_grip := FALSE;
    cmd_release := FALSE;
END_IF;
MoveDown := cmd_down;
MoveUp := cmd_up;
MoveLeft := cmd_left;
MoveRight := cmd_right;
ActivateGrip := cmd_grip;
ActivateRelease := cmd_release;
END_FUNCTION_BLOCK
