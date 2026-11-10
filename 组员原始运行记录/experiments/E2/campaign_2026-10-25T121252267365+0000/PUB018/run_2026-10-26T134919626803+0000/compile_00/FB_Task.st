FUNCTION_BLOCK FB_Task
VAR_INPUT
    enqueue : BOOL;
    dequeue : BOOL;
    reset : BOOL;
END_VAR
VAR_OUTPUT
    elementCount : DINT;
    status : WORD;
END_VAR
VAR_IN_OUT
    item : VARIANT;
    buffer : VARIANT;
END_VAR
VAR
    prevEnqueue : BOOL;
    prevDequeue : BOOL;
    head : DINT;
    tail : DINT;
    capacity : DINT;
END_VAR

status := WORD#16#0000;
IF reset THEN
    elementCount := 0;
    head := 0;
    tail := 0;
ELSE
    IF dequeue AND NOT prevDequeue THEN
        IF elementCount = 0 THEN
            status := WORD#16#8001;
        ELSE
            elementCount := elementCount - 1;
        END_IF
    ELSIF enqueue AND NOT prevEnqueue THEN
        IF elementCount >= capacity THEN
            status := WORD#16#8002;
        ELSE
            elementCount := elementCount + 1;
        END_IF
    END_IF
END_IF
prevEnqueue := enqueue;
prevDequeue := dequeue;
END_FUNCTION_BLOCK
