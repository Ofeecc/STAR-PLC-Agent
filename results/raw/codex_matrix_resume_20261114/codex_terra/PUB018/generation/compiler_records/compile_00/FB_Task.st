FUNCTION_BLOCK FB_Task
VAR_INPUT
    enqueue : BOOL;
    dequeue : BOOL;
    reset : BOOL;
END_VAR
VAR_OUTPUT
    elementCount : DINT := 0;
    status : WORD := 0;
END_VAR
VAR_IN_OUT
    item : VARIANT;
    buffer : VARIANT;
END_VAR
VAR
    head : DINT := 0;
    tail : DINT := 0;
    capacity : DINT;
    itemSize : DINT;
    byteIndex : DINT;
    itemBytes : POINTER TO BYTE;
    bufferBytes : POINTER TO BYTE;
    enqueuePrevious : BOOL := FALSE;
    dequeuePrevious : BOOL := FALSE;
    enqueueEdge : BOOL;
    dequeueEdge : BOOL;
END_VAR

enqueueEdge := enqueue AND NOT enqueuePrevious;
dequeueEdge := dequeue AND NOT dequeuePrevious;
enqueuePrevious := enqueue;
dequeuePrevious := dequeue;
status := 16#0000;
itemSize := item.diSize;
capacity := buffer.diSize / itemSize;
itemBytes := item.pValue;
bufferBytes := buffer.pValue;
IF reset THEN
    elementCount := 0;
    head := 0;
    tail := 0;
ELSIF enqueueEdge THEN
    IF elementCount = capacity THEN
        status := 16#8002;
    ELSE
        FOR byteIndex := 0 TO itemSize - 1 DO
            bufferBytes[tail * itemSize + byteIndex] := itemBytes[byteIndex];
        END_FOR;
        IF tail = capacity - 1 THEN
            tail := 0;
        ELSE
            tail := tail + 1;
        END_IF;
        elementCount := elementCount + 1;
    END_IF;
ELSIF dequeueEdge THEN
    IF elementCount = 0 THEN
        status := 16#8001;
    ELSE
        FOR byteIndex := 0 TO itemSize - 1 DO
            itemBytes[byteIndex] := bufferBytes[head * itemSize + byteIndex];
        END_FOR;
        IF head = capacity - 1 THEN
            head := 0;
        ELSE
            head := head + 1;
        END_IF;
        elementCount := elementCount - 1;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
