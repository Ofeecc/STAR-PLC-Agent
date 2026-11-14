FUNCTION_BLOCK FB_Task
VAR_INPUT
    Value : REAL;
    hiLevel : REAL;
    loLevel : REAL;
    hystWindow : REAL;
END_VAR
VAR_OUTPUT
    hiAlarm : BOOL := FALSE;
    loAlarm : BOOL := FALSE;
    {attribute 'analysis' := '-27'}
    error : BOOL := FALSE;
    {attribute 'analysis' := '-27'}
    status : WORD := 0;
END_VAR
VAR
    hiAlarmPrev : BOOL := FALSE;
    loAlarmPrev : BOOL := FALSE;
    hiAlarmNext : BOOL := FALSE;
    loAlarmNext : BOOL := FALSE;
    errorNext : BOOL := FALSE;
    statusNext : WORD := 0;
    span : REAL := 0.0;
    highRelease : REAL := 0.0;
    lowRelease : REAL := 0.0;
END_VAR

// Stage 1: capture previous observed alarm history
hiAlarmPrev := hiAlarm;
loAlarmPrev := loAlarm;

// Stage 2: validate configuration; badRange has priority over badWindow
IF loLevel >= hiLevel THEN
    errorNext := TRUE;
    statusNext := WORD#16#8001;
    hiAlarmNext := hiAlarmPrev;
    loAlarmNext := loAlarmPrev;
ELSE
    span := hiLevel - loLevel;
    IF hystWindow >= span THEN
        errorNext := TRUE;
        statusNext := WORD#16#8002;
        hiAlarmNext := hiAlarmPrev;
        loAlarmNext := loAlarmPrev;
    ELSE
        errorNext := FALSE;
        statusNext := WORD#0;
        highRelease := hiLevel - hystWindow;
        lowRelease := loLevel + hystWindow;

        // High alarm with strict trigger/release and retained history
        IF Value > hiLevel THEN
            hiAlarmNext := TRUE;
        ELSIF Value < highRelease THEN
            hiAlarmNext := FALSE;
        ELSE
            hiAlarmNext := hiAlarmPrev;
        END_IF;

        // Low alarm with strict trigger/release and retained history
        IF Value < loLevel THEN
            loAlarmNext := TRUE;
        ELSIF Value > lowRelease THEN
            loAlarmNext := FALSE;
        ELSE
            loAlarmNext := loAlarmPrev;
        END_IF;
    END_IF;
END_IF;

// Stage 4: unified output assignments
hiAlarm := hiAlarmNext;
loAlarm := loAlarmNext;
error := errorNext;
status := statusNext;

// Update retained alarm history from actual assigned outputs
hiAlarmPrev := hiAlarm;
loAlarmPrev := loAlarm;
END_FUNCTION_BLOCK
