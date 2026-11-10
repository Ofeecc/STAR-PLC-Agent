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
    elemSize : UDINT;
    pSrc : POINTER TO BYTE;
    pDst : POINTER TO BYTE;
    udiCount : UDINT;
    udiOffset : UDINT;
    bEnqEdge : BOOL;
    bDeqEdge : BOOL;
END_VAR

status := 16#0000;

IF reset THEN
    elementCount := 0;
    head := 0;
    tail := 0;
    enqueuePrev := enqueue;
    dequeuePrev := dequeue;
ELSE
    bEnqEdge := enqueue AND NOT enqueuePrev;
    bDeqEdge := dequeue AND NOT dequeuePrev;
    enqueuePrev := enqueue;
    dequeuePrev := dequeue;

    elemSize := item.udiSize;
    IF elemSize = 0 THEN
        elemSize := buffer.udiSize;
    END_IF
    IF elemSize > 0 THEN
        capacity := UDINT_TO_DINT(buffer.udiSize / elemSize);
    ELSE
        capacity := 0;
    END_IF
    IF capacity < 0 THEN
        capacity := 0;
    END_IF

    IF bEnqEdge THEN
        IF (capacity <= 0) OR (elementCount >= capacity) THEN
            status := 16#8002;
        ELSE
            IF elementCount <= 0 THEN
                head := 0;
                tail := 0;
            END_IF
            udiOffset := DINT_TO_UDINT(tail) * elemSize;
            pDst := buffer.pData + udiOffset;
            pSrc := item.pData;
            FOR udiCount := 1 TO elemSize DO
                pDst^ := pSrc^;
                pDst := pDst + 1;
                pSrc := pSrc + 1;
            END_FOR
            tail := tail + 1;
            IF tail >= capacity THEN
                tail := 0;
            END_IF
            elementCount := elementCount + 1;
        END_IF
    ELSIF bDeqEdge THEN
        IF (capacity <= 0) OR (elementCount <= 0) THEN
            status := 16#8001;
        ELSE
            udiOffset := DINT_TO_UDINT(head) * elemSize;
            pSrc := buffer.pData + udiOffset;
            pDst := item.pData;
            FOR udiCount := 1 TO elemSize DO
                pDst^ := pSrc^;
                pDst := pDst + 1;
                pSrc := pSrc + 1;
            END_FOR
            head := head + 1;
            IF head >= capacity THEN
                head := 0;
            END_IF
            elementCount := elementCount - 1;
            IF elementCount <= 0 THEN
                elementCount := 0;
            END_IF
        END_IF
    END_IF
END_IF
END_FUNCTION_BLOCK
