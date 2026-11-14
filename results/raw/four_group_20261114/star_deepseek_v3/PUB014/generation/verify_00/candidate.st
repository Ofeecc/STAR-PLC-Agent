FUNCTION_BLOCK FB_Task
VAR_INPUT
    ipText : STRING(254);
END_VAR
VAR_OUTPUT
    ipValue : UDINT;
END_VAR
VAR
    visibleLen : INT;
    i : INT;
    c : BYTE;
    parseOk : BOOL;
    valid : BOOL;
    segCount : INT;
    segValue : UDINT;
    digitSeen : BOOL;
    octets : ARRAY[0..3] OF UDINT;
    pendingValue : UDINT;
END_VAR

// Stage 1: sample visible text and reset per-invocation parse state
visibleLen := LEN(ipText);
parseOk := TRUE;
valid := FALSE;
segCount := 0;
segValue := UDINT#0;
digitSeen := FALSE;
octets[0] := UDINT#0;
octets[1] := UDINT#0;
octets[2] := UDINT#0;
octets[3] := UDINT#0;
pendingValue := UDINT#0;

// Capacity / visible length check
IF (visibleLen <= 0) OR (visibleLen > 254) THEN
    parseOk := FALSE;
END_IF;

// Stage 2: strict dotted-decimal IPv4 parse
IF parseOk THEN
    FOR i := 1 TO visibleLen DO
        c := ipText[i];
        IF (c >= BYTE#48) AND (c <= BYTE#57) THEN
            digitSeen := TRUE;
            segValue := segValue * UDINT#10 + (TO_UDINT(c) - UDINT#48);
            IF segValue > UDINT#255 THEN
                parseOk := FALSE;
                EXIT;
            END_IF;
        ELSIF c = BYTE#46 THEN
            IF (NOT digitSeen) OR (segCount >= 3) THEN
                parseOk := FALSE;
                EXIT;
            END_IF;
            octets[segCount] := segValue;
            segCount := segCount + 1;
            segValue := UDINT#0;
            digitSeen := FALSE;
        ELSE
            parseOk := FALSE;
            EXIT;
        END_IF;
    END_FOR;
END_IF;

// Finalize exactly four nonempty segments
IF parseOk AND digitSeen AND (segCount = 3) THEN
    octets[3] := segValue;
    valid := TRUE;
    pendingValue := octets[0] * UDINT#16777216
                  + octets[1] * UDINT#65536
                  + octets[2] * UDINT#256
                  + octets[3];
ELSE
    valid := FALSE;
    pendingValue := UDINT#0;
END_IF;

// Stage 4: unified output, invalid input forces zero in the same invocation
IF valid THEN
    ipValue := pendingValue;
ELSE
    ipValue := UDINT#0;
END_IF;
END_FUNCTION_BLOCK
