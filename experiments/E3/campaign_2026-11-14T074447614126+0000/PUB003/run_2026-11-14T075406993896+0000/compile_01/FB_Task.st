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
    error : BOOL := FALSE;
    status : WORD := 0;
END_VAR
VAR
    hiAlarmState : BOOL := FALSE;
    loAlarmState : BOOL := FALSE;
    span : REAL;
    hiRelease : REAL;
    loRelease : REAL;
END_VAR

span := hiLevel - loLevel;
hiRelease := hiLevel - hystWindow;
loRelease := loLevel + hystWindow;

IF loLevel >= hiLevel THEN
    error := TRUE;
    status := 16#8001;
ELSIF hystWindow >= span THEN
    error := TRUE;
    status := 16#8002;
ELSE
    error := FALSE;
    status := 0;

    IF Value > hiLevel THEN
        hiAlarmState := TRUE;
    ELSIF Value < hiRelease THEN
        hiAlarmState := FALSE;
    END_IF;

    IF Value < loLevel THEN
        loAlarmState := TRUE;
    ELSIF Value > loRelease THEN
        loAlarmState := FALSE;
    END_IF;
END_IF;

hiAlarm := hiAlarmState;
loAlarm := loAlarmState;
END_FUNCTION_BLOCK
