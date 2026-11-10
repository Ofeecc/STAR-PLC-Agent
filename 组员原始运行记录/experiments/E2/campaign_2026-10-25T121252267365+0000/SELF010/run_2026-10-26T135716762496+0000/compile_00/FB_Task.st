FUNCTION_BLOCK FB_Task
VAR_INPUT
    Fault : BOOL;
    Ack : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Alarm : BOOL := FALSE;
    Acknowledged : BOOL := FALSE;
    Horn : BOOL;
END_VAR
VAR
    previous_fault : BOOL := FALSE;
END_VAR

IF Fault THEN
    Alarm := TRUE;
END_IF;

IF Fault AND NOT previous_fault THEN
    Acknowledged := FALSE;
ELSIF Reset AND NOT Fault THEN
    Alarm := FALSE;
    Acknowledged := FALSE;
ELSIF Ack AND Alarm THEN
    Acknowledged := TRUE;
END_IF;

Horn := Alarm AND NOT Acknowledged;
previous_fault := Fault;
END_FUNCTION_BLOCK
