FUNCTION_BLOCK FB_Task
VAR_INPUT
    ipText : STRING(254);
END_VAR
VAR_OUTPUT
    ipValue : UDINT := 0;
END_VAR
VAR
    i : INT;
    textLength : INT;
    dotCount : INT;
    ch : BYTE;
    octetValue : UDINT;
    packedValue : UDINT;
    isValid : BOOL;
    hasDigit : BOOL;
END_VAR

ipValue := 0;
textLength := LEN(ipText);
dotCount := 0;
octetValue := 0;
packedValue := 0;
isValid := TRUE;
hasDigit := FALSE;

FOR i := 1 TO textLength DO
    ch := ipText[i];
    IF ch = BYTE#46 THEN
        IF NOT hasDigit OR (dotCount >= 3) THEN
            isValid := FALSE;
        ELSE
            packedValue := (packedValue * 256) + octetValue;
            dotCount := dotCount + 1;
            octetValue := 0;
            hasDigit := FALSE;
        END_IF;
    ELSIF (ch >= BYTE#48) AND (ch <= BYTE#57) THEN
        hasDigit := TRUE;
        IF (octetValue > 25) OR ((octetValue = 25) AND (ch > BYTE#53)) THEN
            isValid := FALSE;
        ELSE
            octetValue := (octetValue * 10) + BYTE_TO_UDINT(ch) - 48;
        END_IF;
    ELSE
        isValid := FALSE;
    END_IF;
END_FOR;

IF isValid AND hasDigit AND (dotCount = 3) THEN
    ipValue := (packedValue * 256) + octetValue;
END_IF;
END_FUNCTION_BLOCK
