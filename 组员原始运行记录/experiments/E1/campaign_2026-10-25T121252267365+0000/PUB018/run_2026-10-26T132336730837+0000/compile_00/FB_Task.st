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
    enqueuePrev : BOOL;
    dequeuePrev : BOOL;
    head : DINT;
    tail : DINT;
    capacity : DINT;
    itemInfo : VAR_INFO;
    bufferInfo : VAR_INFO;
    elementSize : UDINT;
    pItem : POINTER TO BYTE;
    pBuffer : POINTER TO BYTE;
    pSrc : POINTER TO BYTE;
    pDst : POINTER TO BYTE;
    enqEdge : BOOL;
    deqEdge : BOOL;
    i : UDINT;
END_VAR

status := 0;

IF reset THEN
    elementCount := 0;
    head := 0;
    tail := 0;
    enqueuePrev := enqueue;
    dequeuePrev := dequeue;
ELSE
    enqEdge := enqueue AND NOT enqueuePrev;
    deqEdge := dequeue AND NOT dequeuePrev;
    enqueuePrev := enqueue;
    dequeuePrev := dequeue;

    itemInfo := __VARINFO(item);
    bufferInfo := __VARINFO(buffer);
    elementSize := itemInfo.Size;
    IF elementSize > 0 THEN
        capacity := DINT(bufferInfo.Size / elementSize);
    ELSE
        capacity := 0;
    END_IF;
    pItem := itemInfo.pData;
    pBuffer := bufferInfo.pData;

    IF enqEdge THEN
        IF (capacity <= 0) OR (elementCount >= capacity) THEN
            status := 16#8002;
        ELSE
            pSrc := pItem;
            pDst := pBuffer + (DINT_TO_UDINT(tail) * elementSize);
            FOR i := 0 TO elementSize - 1 DO
                (pDst + i)^ := (pSrc + i)^;
            END_FOR;
            tail := (tail + 1) MOD capacity;
            elementCount := elementCount + 1;
        END_IF;
    ELSIF deqEdge THEN
        IF (capacity <= 0) OR (elementCount <= 0) THEN
            status := 16#8001;
        ELSE
            pSrc := pBuffer + (DINT_TO_UDINT(head) * elementSize);
            pDst := pItem;
            FOR i := 0 TO elementSize - 1 DO
                (pDst + i)^ := (pSrc + i)^;
            END_FOR;
            head := (head + 1) MOD capacity;
            elementCount := elementCount - 1;
        END_IF;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
