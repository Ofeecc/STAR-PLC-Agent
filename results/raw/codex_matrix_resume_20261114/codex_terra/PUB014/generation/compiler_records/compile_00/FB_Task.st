FUNCTION_BLOCK FB_Task
VAR_INPUT
    ipText : STRING(254);
END_VAR
VAR_OUTPUT
    ipValue : UDINT := 0;
END_VAR
VAR
    textLength : INT;
    position : INT;
    character : BYTE;
    octet : UDINT;
    accumulated : UDINT;
    separatorCount : INT;
    hasDigit : BOOL;
    valid : BOOL;
END_VAR

ipValue := 0;
textLength := LEN(ipText);
octet := 0;
accumulated := 0;
separatorCount := 0;
hasDigit := FALSE;
valid := TRUE;

FOR position := 0 TO textLength - 1 DO
    character := ipText[position];
    IF (character >= 48) AND (character <= 57) THEN
        hasDigit := TRUE;
        IF (octet > 25) OR ((octet = 25) AND (character > 53)) THEN
            valid := FALSE;
            EXIT;
        END_IF;
        octet := octet * 10 + BYTE_TO_UDINT(character - 48);
    ELSIF character = 46 THEN
        IF (NOT hasDigit) OR (separatorCount >= 3) THEN
            valid := FALSE;
            EXIT;
        END_IF;
        accumulated := SHL(accumulated, 8) OR octet;
        octet := 0;
        hasDigit := FALSE;
        separatorCount := separatorCount + 1;
    ELSE
        valid := FALSE;
        EXIT;
    END_IF;
END_FOR;

IF valid AND hasDigit AND (separatorCount = 3) THEN
    ipValue := SHL(accumulated, 8) OR octet;
END_IF;
END_FUNCTION_BLOCK
