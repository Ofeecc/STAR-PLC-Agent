FUNCTION_BLOCK FB_Task
VAR_INPUT
    ipText : STRING(254);
END_VAR
VAR_OUTPUT
    ipValue : UDINT;
END_VAR
VAR
    i : INT;
    seg : INT;
    digits : INT;
    val : UDINT;
    c : BYTE;
    ok : BOOL;
END_VAR

ipValue := 0;
seg := 0;
val := 0;
digits := 0;
ok := TRUE;
i := 1;

WHILE (i <= 254) AND ok DO
    c := ipText[i];

    IF c = 0 THEN
        EXIT;
    END_IF

    IF c = 46 THEN
        IF (digits = 0) OR (seg >= 3) THEN
            ok := FALSE;
        ELSIF val > 255 THEN
            ok := FALSE;
        ELSE
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
        END_IF

    ELSIF (c >= 48) AND (c <= 57) THEN
        val := (val * 10) + TO_UDINT(c - 48);
        digits := digits + 1;
        IF val > 255 THEN
            ok := FALSE;
        END_IF

    ELSE
        ok := FALSE;
    END_IF

    i := i + 1;
END_WHILE

IF ok AND (seg = 3) AND (digits > 0) THEN
    ipValue := ipValue + val;
ELSE
    ipValue := 0;
END_IF
END_FUNCTION_BLOCK
