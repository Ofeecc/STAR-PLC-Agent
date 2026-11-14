FUNCTION_BLOCK FB_Task
VAR_INPUT
    ipText : STRING(254);
END_VAR
VAR_OUTPUT
    ipValue : UDINT := 0;
END_VAR
VAR
    i : INT;
    nLen : INT;
    c : BYTE;
    segNo : INT;
    segVal : UDINT;
    segHasDigit : BOOL;
    parsedValue : UDINT;
    isValid : BOOL;
END_VAR

ipValue := 0;
parsedValue := 0;
segNo := 1;
segVal := 0;
segHasDigit := FALSE;
isValid := TRUE;
nLen := LEN(ipText);

IF (nLen <= 0) OR (nLen > 254) THEN
    isValid := FALSE;
ELSE
    FOR i := 1 TO nLen DO
        c := ipText[i];
        IF (c >= 48) AND (c <= 57) THEN
            segHasDigit := TRUE;
            IF segVal <= 255 THEN
                segVal := segVal * 10 + TO_UDINT(c - 48);
                IF segVal > 255 THEN
                    isValid := FALSE;
                END_IF;
            ELSE
                isValid := FALSE;
            END_IF;
        ELSIF c = 46 THEN
            IF (NOT segHasDigit) OR (segNo >= 4) THEN
                isValid := FALSE;
            ELSE
                parsedValue := parsedValue * 256 + segVal;
                segNo := segNo + 1;
                segVal := 0;
                segHasDigit := FALSE;
            END_IF;
        ELSE
            isValid := FALSE;
        END_IF;
    END_FOR;

    IF (NOT segHasDigit) OR (segNo <> 4) THEN
        isValid := FALSE;
    ELSE
        parsedValue := parsedValue * 256 + segVal;
    END_IF;
END_IF;

IF isValid THEN
    ipValue := parsedValue;
ELSE
    ipValue := 0;
END_IF;
END_FUNCTION_BLOCK
