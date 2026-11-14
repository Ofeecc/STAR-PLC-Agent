FUNCTION_BLOCK FB_Task
VAR_INPUT
    enqueue : BOOL;
    dequeue : BOOL;
    reset : BOOL;
END_VAR
VAR_OUTPUT
    elementCount : DINT := 0;
    status : WORD := 16#0000;
END_VAR
VAR_IN_OUT
    item : VARIANT;
    buffer : VARIANT;
END_VAR
VAR
    previousEnqueue : BOOL := FALSE;
    previousDequeue : BOOL := FALSE;
    enqueueEdge : BOOL;
    dequeueEdge : BOOL;
    head : DINT := 0;
    tail : DINT := 0;
    capacity : DINT;
    itemInfo : __SYSTEM.VAR_INFO;
    bufferInfo : __SYSTEM.VAR_INFO;
    itemSize : __UXINT;
    bufferSize : __UXINT;
    itemAddress : __UXINT;
    bufferAddress : __UXINT;
    addressOffset : __UXINT;
    byteOffset : __UXINT;
    lane : __UXINT;
    itemPtr : POINTER TO BYTE;
    bufferPtr : POINTER TO BYTE;
    aliasesElement : BOOL;
    aliasIndex : DINT;
    shift : DINT;
    gcdA : DINT;
    gcdB : DINT;
    gcdRemainder : DINT;
    cycle : DINT;
    currentPosition : DINT;
    nextPosition : DINT;
    savedByte : BYTE;
    displacedByte : BYTE;
END_VAR

// Integration must verify that VARIANT is supported and that ADR and
// __VARINFO expose the bound object, not a VARIANT descriptor. Array
// elements must occupy consecutive itemSize-byte slots. Validate the
// specified array and item types and capacity before using this block.
// Without that target-specific support, integration must fail.
enqueueEdge := enqueue AND NOT previousEnqueue;
dequeueEdge := dequeue AND NOT previousDequeue;
previousEnqueue := enqueue;
previousDequeue := dequeue;
status := 16#0000;

itemInfo := __VARINFO(item);
bufferInfo := __VARINFO(buffer);
itemSize := itemInfo.ByteSize;
bufferSize := bufferInfo.ByteSize;
itemPtr := ADR(item);
bufferPtr := ADR(buffer);
itemAddress := ADR(item);
bufferAddress := ADR(buffer);

// The binding preconditions guarantee a nonzero item size and a positive
// quotient representable by DINT.
capacity := TO_DINT(bufferSize / itemSize);

IF reset THEN
    head := 0;
    tail := 0;
    elementCount := 0;
ELSIF enqueueEdge THEN
    IF elementCount = capacity THEN
        status := 16#8002;
    ELSE
        lane := 0;
        WHILE lane < itemSize DO
            byteOffset := DINT_TO_UDINT(tail) * itemSize + lane;
            bufferPtr[byteOffset] := itemPtr[lane];
            lane := lane + 1;
        END_WHILE;
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
        // An item bound to an array element must not overwrite a remaining
        // queue element. Rotate the entire buffer so that the old head lands
        // on that item; the remaining queue then follows it in FIFO order.
        aliasesElement := FALSE;
        IF itemAddress >= bufferAddress THEN
            addressOffset := itemAddress - bufferAddress;
            IF addressOffset < bufferSize THEN
                IF (addressOffset MOD itemSize) = 0 THEN
                    aliasesElement := TRUE;
                    aliasIndex := TO_DINT(addressOffset / itemSize);
                END_IF;
            END_IF;
        END_IF;

        IF aliasesElement THEN
            shift := aliasIndex - head;
            IF shift < 0 THEN
                shift := shift + capacity;
            END_IF;
            IF shift <> 0 THEN
                // Rotate each byte lane independently, using one-byte
                // temporaries and the cycles of the element permutation.
                gcdA := capacity;
                gcdB := shift;
                WHILE gcdB <> 0 DO
                    gcdRemainder := gcdA MOD gcdB;
                    gcdA := gcdB;
                    gcdB := gcdRemainder;
                END_WHILE;
                lane := 0;
                WHILE lane < itemSize DO
                    cycle := 0;
                    WHILE cycle < gcdA DO
                        currentPosition := cycle;
                        byteOffset := DINT_TO_UDINT(currentPosition) * itemSize + lane;
                        savedByte := bufferPtr[byteOffset];
                        REPEAT
                            IF currentPosition >= capacity - shift THEN
                                nextPosition := currentPosition - (capacity - shift);
                            ELSE
                                nextPosition := currentPosition + shift;
                            END_IF;
                            byteOffset := DINT_TO_UDINT(nextPosition) * itemSize + lane;
                            displacedByte := bufferPtr[byteOffset];
                            bufferPtr[byteOffset] := savedByte;
                            savedByte := displacedByte;
                            currentPosition := nextPosition;
                        UNTIL currentPosition = cycle
                        END_REPEAT;
                        cycle := cycle + 1;
                    END_WHILE;
                    lane := lane + 1;
                END_WHILE;
                IF tail >= capacity - shift THEN
                    tail := tail - (capacity - shift);
                ELSE
                    tail := tail + shift;
                END_IF;
            END_IF;
            head := aliasIndex;
        ELSE
            lane := 0;
            WHILE lane < itemSize DO
                byteOffset := DINT_TO_UDINT(head) * itemSize + lane;
                itemPtr[lane] := bufferPtr[byteOffset];
                lane := lane + 1;
            END_WHILE;
        END_IF;

        IF head = capacity - 1 THEN
            head := 0;
        ELSE
            head := head + 1;
        END_IF;
        elementCount := elementCount - 1;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
