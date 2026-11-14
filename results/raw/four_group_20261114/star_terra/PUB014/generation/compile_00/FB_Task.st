FUNCTION_BLOCK FB_Task
VAR_INPUT
    ipText : STRING(254);
END_VAR
VAR_OUTPUT
    ipValue : UDINT := UDINT#0;
END_VAR
VAR
    snapshot : STRING(254);
    index : INT;
    byteValue : BYTE;
    digit : UINT;
    octet : UINT;
    periodCount : UINT;
    segmentNonempty : BOOL;
    valid : BOOL;
    candidate : UDINT;
    selectedResult : UDINT;
END_VAR

snapshot := ipText;
candidate := UDINT#0;
octet := UINT#0;
periodCount := UINT#0;
segmentNonempty := FALSE;
valid := TRUE;
selectedResult := UDINT#0;

FOR index := 0 TO 253 DO
    byteValue := snapshot[index];
    IF byteValue = BYTE#0 THEN
        EXIT;
    ELSIF (byteValue >= BYTE#48) AND (byteValue <= BYTE#57) THEN
        digit := BYTE_TO_UINT(byteValue) - UINT#48;
        IF (octet > UINT#25) OR ((octet = UINT#25) AND (digit > UINT#5)) THEN
            valid := FALSE;
            EXIT;
        END_IF;
        octet := octet * UINT#10 + digit;
        segmentNonempty := TRUE;
    ELSIF byteValue = BYTE#46 THEN
        IF (NOT segmentNonempty) OR (periodCount >= UINT#3) THEN
            valid := FALSE;
            EXIT;
        END_IF;
        candidate := candidate * UDINT#256 + UINT_TO_UDINT(octet);
        periodCount := periodCount + UINT#1;
        octet := UINT#0;
        segmentNonempty := FALSE;
    ELSE
        valid := FALSE;
        EXIT;
    END_IF;
END_FOR;

IF valid AND (periodCount = UINT#3) AND segmentNonempty THEN
    selectedResult := candidate * UDINT#256 + UINT_TO_UDINT(octet);
END_IF;

ipValue := selectedResult;
END_FUNCTION_BLOCK
