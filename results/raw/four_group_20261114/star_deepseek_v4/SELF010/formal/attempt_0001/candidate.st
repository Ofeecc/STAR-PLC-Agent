FUNCTION_BLOCK FB_Task
VAR_INPUT
    Fault : BOOL;
    Ack : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Alarm : BOOL := FALSE;
    Acknowledged : BOOL := FALSE;
    Horn : BOOL := FALSE;
END_VAR
VAR
    previous_fault : BOOL := FALSE;
    rise : BOOL := FALSE;
END_VAR

rise := Fault AND NOT previous_fault;
previous_fault := Fault;

IF Reset AND NOT Fault THEN
    Alarm := FALSE;
    Acknowledged := FALSE;
ELSIF Fault THEN
    Alarm := TRUE;
    IF rise THEN
        Acknowledged := FALSE;
    ELSIF Ack THEN
        Acknowledged := TRUE;
    END_IF;
ELSE
    IF Alarm AND Ack THEN
        Acknowledged := TRUE;
    END_IF;
END_IF;

Horn := Alarm AND NOT Acknowledged;
END_FUNCTION_BLOCK
