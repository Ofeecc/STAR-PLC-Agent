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
    analogIndex : DINT;
    channelIndex : DINT;
    rawValue : REAL;
END_VAR

IF count > 0 THEN
    FOR i := 0 TO count - 1 DO
        analogIndex := LOWER_BOUND(analogValues, 1) + i;
        channelIndex := LOWER_BOUND(channels, 1) + i;

        IF channels[channelIndex].enable THEN
            CASE channels[channelIndex].measuringMode OF
                0, 1, 2:
                    IF channels[channelIndex].hiLIM <= channels[channelIndex].loLIM THEN
                        channels[channelIndex].retVal := WORD#16#8002;
                    ELSE
                        rawValue := INT_TO_REAL(analogValues[analogIndex]);
                        channels[channelIndex].retVal := WORD#0;

                        CASE channels[channelIndex].measuringMode OF
                            0:
                                IF channels[channelIndex].bipolar THEN
                                    channels[channelIndex].outputValue :=
                                        channels[channelIndex].loLIM
                                        + ((rawValue + 27648.0) / 55296.0)
                                        * (channels[channelIndex].hiLIM - channels[channelIndex].loLIM);
                                ELSE
                                    channels[channelIndex].outputValue :=
                                        channels[channelIndex].loLIM
                                        + (rawValue / 27648.0)
                                        * (channels[channelIndex].hiLIM - channels[channelIndex].loLIM);
                                END_IF;
                            1:
                                channels[channelIndex].outputValue := rawValue / 10.0;
                            2:
                                channels[channelIndex].outputValue := rawValue / 100.0;
                        END_CASE;
                    END_IF;
            ELSE
                channels[channelIndex].retVal := WORD#16#8001;
            END_CASE;
        END_IF;
    END_FOR;
END_IF;
END_FUNCTION_BLOCK
