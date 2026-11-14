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
END_VAR

IF Reset AND NOT Fault THEN
    Alarm := FALSE;
    Acknowledged := FALSE;
ELSIF Fault THEN
    Alarm := TRUE;
    IF NOT previous_fault THEN
        Acknowledged := FALSE;
    ELSIF Ack THEN
        Acknowledged := TRUE;
    END_IF;
ELSIF Alarm AND Ack THEN
    Acknowledged := TRUE;
END_IF;
Horn := Alarm AND NOT Acknowledged;
previous_fault := Fault;
END_FUNCTION_BLOCK
