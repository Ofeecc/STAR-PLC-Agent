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
    status : WORD := 16#0000;
END_VAR
VAR
    span : REAL;
    highRelease : REAL;
    lowRelease : REAL;
END_VAR

IF loLevel >= hiLevel THEN
    error := TRUE;
    status := 16#8001;
    RETURN;
END_IF;

span := hiLevel - loLevel;
IF hystWindow >= span THEN
    error := TRUE;
    status := 16#8002;
    RETURN;
END_IF;

error := FALSE;
status := 16#0000;
highRelease := hiLevel - hystWindow;
lowRelease := loLevel + hystWindow;

IF Value > hiLevel THEN
    hiAlarm := TRUE;
ELSIF Value < highRelease THEN
    hiAlarm := FALSE;
END_IF;

IF Value < loLevel THEN
    loAlarm := TRUE;
ELSIF Value > lowRelease THEN
    loAlarm := FALSE;
END_IF;
END_FUNCTION_BLOCK
