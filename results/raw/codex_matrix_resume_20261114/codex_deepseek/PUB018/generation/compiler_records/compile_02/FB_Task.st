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
    initialized : BOOL := FALSE;
    count : DINT := 0;
    head : DINT := 0;
    tail : DINT := 0;
    capacity : DINT := 0;
    elementSize : DINT := 0;
    pBuffer : POINTER TO BYTE;
    pItem : POINTER TO BYTE;
    prevEnqueue : BOOL := FALSE;
    prevDequeue : BOOL := FALSE;
    enqueueEdge : BOOL;
    dequeueEdge : BOOL;
    index : DINT;
    offset : DINT;
END_VAR

status := 16#0000;

IF NOT initialized THEN
    elementSize := item.diSize;
    IF elementSize <= 0 THEN
        elementSize := buffer.diElementSize;
    END_IF;
    IF buffer.diElementCount > 0 THEN
        capacity := buffer.diElementCount;
    ELSIF elementSize > 0 THEN
        capacity := buffer.diSize / elementSize;
    ELSE
        capacity := 0;
    END_IF;
    pBuffer := buffer.pData;
    count := 0;
    head := 0;
    tail := 0;
    initialized := TRUE;
END_IF;

pItem := item.pData;
enqueueEdge := enqueue AND NOT prevEnqueue;
dequeueEdge := dequeue AND NOT prevDequeue;

IF reset THEN
    count := 0;
    head := 0;
    tail := 0;
    status := 16#0000;
ELSIF enqueueEdge AND NOT dequeueEdge THEN
    IF (capacity <= 0) OR (count >= capacity) THEN
        status := 16#8002;
    ELSE
        offset := tail * elementSize;
        FOR index := 0 TO elementSize - 1 DO
            pBuffer[offset + index] := pItem[index];
        END_FOR;
        tail := tail + 1;
        IF tail >= capacity THEN
            tail := 0;
        END_IF;
        count := count + 1;
    END_IF;
ELSIF dequeueEdge AND NOT enqueueEdge THEN
    IF (capacity <= 0) OR (count <= 0) THEN
        status := 16#8001;
    ELSE
        offset := head * elementSize;
        FOR index := 0 TO elementSize - 1 DO
            pItem[index] := pBuffer[offset + index];
        END_FOR;
        head := head + 1;
        IF head >= capacity THEN
            head := 0;
        END_IF;
        count := count - 1;
        IF count = 0 THEN
            head := 0;
            tail := 0;
        END_IF;
    END_IF;
END_IF;

elementCount := count;
prevEnqueue := enqueue;
prevDequeue := dequeue;
END_FUNCTION_BLOCK
