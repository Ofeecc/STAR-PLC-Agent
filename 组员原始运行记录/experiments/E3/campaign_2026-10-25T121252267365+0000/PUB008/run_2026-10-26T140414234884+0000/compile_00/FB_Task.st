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
    rawIndex : DINT;
    chIndex : DINT;
    rawValue : INT;
    mode : INT;
    lo : REAL;
    hi : REAL;
    isBipolar : BOOL;
END_VAR

IF count > 0 THEN
    FOR i := 0 TO count - 1 DO
        chIndex := LOWER_BOUND(channels, 1) + i;
        IF channels[chIndex].enable THEN
            mode := channels[chIndex].measuringMode;
            IF (mode <> 0) AND (mode <> 1) AND (mode <> 2) THEN
                channels[chIndex].retVal := WORD#16#8001;
            ELSE
                lo := channels[chIndex].loLIM;
                hi := channels[chIndex].hiLIM;
                IF hi <= lo THEN
                    channels[chIndex].retVal := WORD#16#8002;
                ELSE
                    rawIndex := LOWER_BOUND(analogValues, 1) + i;
                    rawValue := analogValues[rawIndex];
                    isBipolar := channels[chIndex].bipolar;
                    CASE mode OF
                        0:
                            IF isBipolar THEN
                                channels[chIndex].outputValue := lo + ((INT_TO_REAL(rawValue) + 27648.0) / 55296.0) * (hi - lo);
                            ELSE
                                channels[chIndex].outputValue := lo + (INT_TO_REAL(rawValue) / 27648.0) * (hi - lo);
                            END_IF
                        1:
                            channels[chIndex].outputValue := INT_TO_REAL(rawValue) / 10.0;
                        2:
                            channels[chIndex].outputValue := INT_TO_REAL(rawValue) / 100.0;
                    END_CASE
                    channels[chIndex].retVal := 0;
                END_IF
            END_IF
        END_IF
    END_FOR
END_IF
END_FUNCTION_BLOCK
