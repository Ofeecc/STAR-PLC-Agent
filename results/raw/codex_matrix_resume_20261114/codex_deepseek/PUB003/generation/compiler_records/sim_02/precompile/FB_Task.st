FUNCTION_BLOCK FB_Task
VAR_INPUT
    Value : REAL;
    hiLevel : REAL;
    loLevel : REAL;
    hystWindow : REAL;
END_VAR
{attribute 'no_check'}
{attribute 'qualified_only'}
VAR_OUTPUT
    hiAlarm : BOOL;
    loAlarm : BOOL;
    error : BOOL;
    status : WORD;
END_VAR

THIS^.error := FALSE;
THIS^.status := 16#0000;

IF loLevel >= hiLevel THEN
    THIS^.error := TRUE;
    THIS^.status := 16#8001;
    RETURN;
END_IF

IF hystWindow >= (hiLevel - loLevel) THEN
    THIS^.error := TRUE;
    THIS^.status := 16#8002;
    RETURN;
END_IF

IF Value > hiLevel THEN
    THIS^.hiAlarm := TRUE;
ELSIF Value < (hiLevel - hystWindow) THEN
    THIS^.hiAlarm := FALSE;
END_IF

IF Value < loLevel THEN
    THIS^.loAlarm := TRUE;
ELSIF Value > (loLevel + hystWindow) THEN
    THIS^.loAlarm := FALSE;
END_IF
END_FUNCTION_BLOCK
