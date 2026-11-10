FUNCTION_BLOCK FB_Task
VAR_INPUT
    ipText : STRING(254);
END_VAR
VAR_OUTPUT
    ipValue : UDINT;
END_VAR
VAR
    iPos : INT;
    iLen : INT;
    iSegments : INT;
    iDigits : INT;
    udiOctet : UDINT;
    bValid : BOOL;
END_VAR

ipValue := UDINT#0;
iLen := LEN(ipText);
iSegments := 0;
iDigits := 0;
udiOctet := UDINT#0;
bValid := TRUE;

FOR iPos := 1 TO iLen DO
    IF bValid THEN
        IF ipText[iPos] = BYTE#46 THEN
            IF (iDigits = 0) OR (iSegments >= 3) THEN
                bValid := FALSE;
            ELSE
                ipValue := ipValue * UDINT#256 + udiOctet;
                iSegments := iSegments + 1;
                iDigits := 0;
                udiOctet := UDINT#0;
            END_IF;
        ELSIF (ipText[iPos] >= BYTE#48) AND (ipText[iPos] <= BYTE#57) THEN
            udiOctet := udiOctet * UDINT#10 + TO_UDINT(ipText[iPos] - BYTE#48);
            iDigits := iDigits + 1;
            IF udiOctet > UDINT#255 THEN
                bValid := FALSE;
            END_IF;
        ELSE
            bValid := FALSE;
        END_IF;
    END_IF;
END_FOR;

IF bValid THEN
    IF (iDigits = 0) OR (iSegments <> 3) OR (udiOctet > UDINT#255) THEN
        bValid := FALSE;
    ELSE
        ipValue := ipValue * UDINT#256 + udiOctet;
    END_IF;
END_IF;

IF NOT bValid THEN
    ipValue := UDINT#0;
END_IF;
END_FUNCTION_BLOCK
