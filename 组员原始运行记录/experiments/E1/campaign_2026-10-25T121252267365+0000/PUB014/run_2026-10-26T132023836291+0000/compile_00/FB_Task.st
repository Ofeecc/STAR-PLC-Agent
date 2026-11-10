FUNCTION_BLOCK FB_Task
VAR_INPUT
    ipText : STRING(254);
END_VAR
VAR_OUTPUT
    ipValue : UDINT;
END_VAR
VAR
    i : INT;
    len : INT;
    seg : INT;
    digits : INT;
    val : UDINT;
    c : BYTE;
    ok : BOOL;
END_VAR

ipValue := 0;
len := LEN(ipText);
IF len <= 0 THEN
    RETURN;
END_IF

ok := TRUE;
seg := 0;
val := 0;
digits := 0;

FOR i := 1 TO len DO
    c := ipText[i];

    IF c = 46 THEN
        IF (digits = 0) OR (seg >= 3) THEN
            ok := FALSE;
            EXIT;
        END_IF
        IF val > 255 THEN
            ok := FALSE;
            EXIT;
        END_IF

        IF seg = 0 THEN
            ipValue := val * 16777216;
        ELSIF seg = 1 THEN
            ipValue := ipValue + (val * 65536);
        ELSIF seg = 2 THEN
            ipValue := ipValue + (val * 256);
        END_IF

        seg := seg + 1;
        val := 0;
        digits := 0;

    ELSIF (c >= 48) AND (c <= 57) THEN
        val := (val * 10) + TO_UDINT(c - 48);
        digits := digits + 1;
        IF val > 255 THEN
            ok := FALSE;
            EXIT;
        END_IF

    ELSE
        ok := FALSE;
        EXIT;
    END_IF
END_FOR

IF NOT ok THEN
    ipValue := 0;
    RETURN;
END_IF

IF (digits = 0) OR (seg <> 3) THEN
    ipValue := 0;
    RETURN;
END_IF

ipValue := ipValue + val;
END_FUNCTION_BLOCK
