FUNCTION_BLOCK FB_Task
VAR_INPUT
    count : DINT;
END_VAR
VAR_IN_OUT
    analogValues : ARRAY[*] OF INT;
    channels : ARRAY[*] OF ST_AnalogChannel;
END_VAR
VAR
    i : DINT;
    aIdx : DINT;
    cIdx : DINT;
    rawValue : REAL;
    mode : INT;
    lo : REAL;
    hi : REAL;
END_VAR

FOR i := 0 TO count - 1 DO
    aIdx := LOWER_BOUND(analogValues, 1) + i;
    cIdx := LOWER_BOUND(channels, 1) + i;

    IF channels[cIdx].enable THEN
        mode := channels[cIdx].measuringMode;

        IF (mode <> 0) AND (mode <> 1) AND (mode <> 2) THEN
            channels[cIdx].retVal := 16#8001;
        ELSIF channels[cIdx].hiLIM <= channels[cIdx].loLIM THEN
            channels[cIdx].retVal := 16#8002;
        ELSE
            channels[cIdx].retVal := 0;
            rawValue := INT_TO_REAL(analogValues[aIdx]);
            lo := channels[cIdx].loLIM;
            hi := channels[cIdx].hiLIM;

            CASE mode OF
                0:
                    IF channels[cIdx].bipolar THEN
                        channels[cIdx].outputValue := lo + ((rawValue + 27648.0) / 55296.0) * (hi - lo);
                    ELSE
                        channels[cIdx].outputValue := lo + (rawValue / 27648.0) * (hi - lo);
                    END_IF;
                1:
                    channels[cIdx].outputValue := rawValue / 10.0;
                2:
                    channels[cIdx].outputValue := rawValue / 100.0;
            END_CASE;
        END_IF;
    END_IF;
END_FOR
END_FUNCTION_BLOCK
