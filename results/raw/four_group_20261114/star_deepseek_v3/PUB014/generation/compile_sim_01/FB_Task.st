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
    d : INT;
    ch : STRING(1);
    parseOk : BOOL;
    valid : BOOL;
    segCount : INT;
    segValue : UDINT;
    digitSeen : BOOL;
    octets : ARRAY[0..3] OF UDINT;
    pendingValue : UDINT;
END_VAR

// Stage 1: determine visible length of the sampled text
visibleLen := LEN(ipText);
IF visibleLen > 254 THEN
    visibleLen := 254;
END_IF;

// Reset all per-invocation parse state (no retained parse state)
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

IF visibleLen <= 0 THEN
    parseOk := FALSE;
END_IF;

// Stage 2: strict dotted-decimal IPv4 parse, character by character
IF parseOk THEN
    FOR i := 1 TO visibleLen DO
        // extract the i-th character using unambiguous LEFT/RIGHT semantics
        ch := RIGHT(LEFT(ipText, i), 1);

        // end of visible text (embedded NUL or exhausted string)
        IF (ch = '') OR (LEN(ch) = 0) THEN
            EXIT;
        END_IF;

        // 1-based position inside '0123456789'; 0 means not a decimal digit
d := FIND('0123456789', ch);

        IF d > 0 THEN
            // decimal digit: accumulate, reject values above 255
            digitSeen := TRUE;
            segValue := segValue * UDINT#10 + TO_UDINT(d - 1);
            IF segValue > UDINT#255 THEN
                parseOk := FALSE;
                EXIT;
            END_IF;
        ELSIF ch = '.' THEN
            // segment separator: requires a nonempty segment and at most 4 segments
            IF (NOT digitSeen) OR (segCount >= 3) THEN
                parseOk := FALSE;
                EXIT;
            END_IF;
            octets[segCount] := segValue;
            segCount := segCount + 1;
            segValue := UDINT#0;
            digitSeen := FALSE;
        ELSE
            // sign, whitespace, hex prefix, embedded nondigit -> invalid
            parseOk := FALSE;
            EXIT;
        END_IF;
    END_FOR;
END_IF;

// Finalize: exactly four nonempty segments, each 0..255
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

// Stage 4: single unified output assignment; invalid input forces zero this scan
IF valid THEN
    ipValue := pendingValue;
ELSE
    ipValue := UDINT#0;
END_IF;
END_FUNCTION_BLOCK
