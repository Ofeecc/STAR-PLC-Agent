FUNCTION_BLOCK FB_Task
VAR_INPUT
    count : DINT;
END_VAR
VAR_IN_OUT
    analogValues : ARRAY[*] OF INT;
    channels : ARRAY[*] OF ST_AnalogChannel;
END_VAR
VAR
    j : DINT;
    aIdx : DINT;
    cIdx : DINT;
    raw : INT;
    mode : INT;
    lo : REAL;
    hi : REAL;
    scaledValue : REAL;
END_VAR

j := 0;
WHILE j < count DO
    cIdx := LOWER_BOUND(channels, 1) + j;
    IF channels[cIdx].enable THEN
        mode := channels[cIdx].measuringMode;
        IF (mode <> 0) AND (mode <> 1) AND (mode <> 2) THEN
            channels[cIdx].retVal := 16#8001;
        ELSIF channels[cIdx].hiLIM <= channels[cIdx].loLIM THEN
            channels[cIdx].retVal := 16#8002;
        ELSE
            aIdx := LOWER_BOUND(analogValues, 1) + j;
            raw := analogValues[aIdx];
            IF mode = 0 THEN
                lo := channels[cIdx].loLIM;
                hi := channels[cIdx].hiLIM;
                IF channels[cIdx].bipolar THEN
                    scaledValue := lo + ((INT_TO_REAL(raw) + 27648.0) / 55296.0) * (hi - lo);
                ELSE
                    scaledValue := lo + (INT_TO_REAL(raw) / 27648.0) * (hi - lo);
                END_IF;
            ELSIF mode = 1 THEN
                scaledValue := INT_TO_REAL(raw) / 10.0;
            ELSE
                scaledValue := INT_TO_REAL(raw) / 100.0;
            END_IF;
            channels[cIdx].retVal := 16#0000;
            channels[cIdx].outputValue := scaledValue;
        END_IF;
    END_IF;
    j := j + 1;
END_WHILE;
END_FUNCTION_BLOCK
