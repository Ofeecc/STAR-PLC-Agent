FUNCTION_BLOCK FB_Task
VAR_INPUT
    enqueue : BOOL;
    dequeue : BOOL;
    reset : BOOL;
END_VAR
VAR_OUTPUT
    elementCount : DINT := 0;
    {attribute 'analysis' := '-27'}
    status : WORD := 16#0000;
END_VAR
VAR_IN_OUT
    item : VARIANT;
    buffer : VARIANT;
END_VAR
VAR
    initialized : BOOL := FALSE;
    capacity : DINT := 0;
    head : DINT := 0;
    tail : DINT := 0;
    internalCount : DINT := 0;
    enqueuePrev : BOOL := FALSE;
    dequeuePrev : BOOL := FALSE;
    enqueueRise : BOOL;
    dequeueRise : BOOL;
    bufferInfo : __SYSTEM.VAR_INFO;
    itemInfo : __SYSTEM.VAR_INFO;
    elementSize : UDINT;
    pBuffer : POINTER TO BYTE;
    pItem : POINTER TO BYTE;
    pElem : POINTER TO BYTE;
    idx : DINT;
    offset : UDINT;
END_VAR

bufferInfo := __VARINFO(buffer);
itemInfo := __VARINFO(item);

IF NOT initialized THEN
    elementSize := itemInfo.Size;
    IF elementSize > 0 THEN
        capacity := UDINT_TO_DINT(bufferInfo.Size / elementSize);
    ELSE
        capacity := 0;
    END_IF;
    IF capacity < 0 THEN
        capacity := 0;
    END_IF;
    head := 0;
    tail := 0;
    internalCount := 0;
    status := 16#0000;
    initialized := TRUE;
END_IF;

pBuffer := bufferInfo.pAddress;
pItem := itemInfo.pAddress;

enqueueRise := enqueue AND NOT enqueuePrev;
dequeueRise := dequeue AND NOT dequeuePrev;
enqueuePrev := enqueue;
dequeuePrev := dequeue;

IF reset THEN
    internalCount := 0;
    head := 0;
    tail := 0;
    status := 16#0000;
ELSIF enqueueRise AND dequeueRise THEN
    status := 16#0000;
ELSIF enqueueRise THEN
    IF internalCount >= capacity THEN
        status := 16#8002;
    ELSE
        idx := tail;
        offset := DINT_TO_UDINT(idx) * elementSize;
        pElem := pBuffer + offset;
        FIFO_CopyBytes(dest := pElem, src := pItem, size := elementSize);
        tail := (tail + 1) MOD capacity;
        internalCount := internalCount + 1;
        status := 16#0000;
    END_IF;
ELSIF dequeueRise THEN
    IF internalCount <= 0 THEN
        status := 16#8001;
    ELSE
        idx := head;
        offset := DINT_TO_UDINT(idx) * elementSize;
        pElem := pBuffer + offset;
        FIFO_CopyBytes(dest := pItem, src := pElem, size := elementSize);
        head := (head + 1) MOD capacity;
        internalCount := internalCount - 1;
        status := 16#0000;
    END_IF;
ELSE
    status := 16#0000;
END_IF;

elementCount := internalCount;
END_FUNCTION_BLOCK
