FUNCTION_BLOCK FB_Task
VAR_INPUT
    Fault : BOOL;
    Ack : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Alarm : BOOL;
    Acknowledged : BOOL;
    Horn : BOOL;
END_VAR
VAR
    prevFault : BOOL;
    rise : BOOL;
END_VAR

rise := Fault AND NOT prevFault;

IF rise THEN
    Alarm := TRUE;
    Acknowledged := FALSE;
ELSIF Reset AND NOT Fault THEN
    Alarm := FALSE;
    Acknowledged := FALSE;
ELSE
    IF Fault THEN
        Alarm := TRUE;
    END_IF
    IF Ack AND Alarm THEN
        Acknowledged := TRUE;
    END_IF
END_IF

Horn := Alarm AND NOT Acknowledged;
prevFault := Fault;
END_FUNCTION_BLOCK
