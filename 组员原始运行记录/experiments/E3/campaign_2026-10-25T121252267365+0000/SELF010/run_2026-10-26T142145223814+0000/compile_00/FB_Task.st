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
    previousFault : BOOL := FALSE;
END_VAR

// New Fault rising edge has top priority over Ack and reannunciates.
IF Fault AND NOT previousFault THEN
    Alarm := TRUE;
    Acknowledged := FALSE;

// While Fault is present, Alarm remains set and Ack can silence it.
ELSIF Fault THEN
    Alarm := TRUE;
    IF Ack THEN
        Acknowledged := TRUE;
    END_IF;

// Reset clears only when Fault is absent and takes priority over Ack.
ELSIF Reset THEN
    Alarm := FALSE;
    Acknowledged := FALSE;

// Ack can acknowledge a retained Alarm when Fault is absent.
ELSIF Ack THEN
    IF Alarm THEN
        Acknowledged := TRUE;
    END_IF;
END_IF;

Horn := Alarm AND NOT Acknowledged;

// Always update the previous Fault sample for the next scan.
previousFault := Fault;
END_FUNCTION_BLOCK
