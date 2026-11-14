FUNCTION_BLOCK FB_Task
VAR_INPUT
    count : DINT;
END_VAR
VAR_IN_OUT
    analogValues : ARRAY[*] OF INT;
    channels : ARRAY[*] OF ST_AnalogChannel;
END_VAR
VAR
    offset : DINT;
    analogBase : DINT;
    channelBase : DINT;
    rawValue : LREAL;
    lowLimit : LREAL;
    highLimit : LREAL;
END_VAR

analogBase := LOWER_BOUND(analogValues, 1);
channelBase := LOWER_BOUND(channels, 1);
FOR offset := 0 TO count - 1 DO
    IF channels[channelBase + offset].enable THEN
        IF (channels[channelBase + offset].measuringMode < 0) OR (channels[channelBase + offset].measuringMode > 2) THEN
            channels[channelBase + offset].retVal := 16#8001;
        ELSIF channels[channelBase + offset].hiLIM <= channels[channelBase + offset].loLIM THEN
            channels[channelBase + offset].retVal := 16#8002;
        ELSE
            rawValue := INT_TO_LREAL(analogValues[analogBase + offset]);
            CASE channels[channelBase + offset].measuringMode OF
                0:
                    lowLimit := REAL_TO_LREAL(channels[channelBase + offset].loLIM);
                    highLimit := REAL_TO_LREAL(channels[channelBase + offset].hiLIM);
                    IF channels[channelBase + offset].bipolar THEN
                        channels[channelBase + offset].outputValue := LREAL_TO_REAL(lowLimit + ((rawValue + 27648.0) / 55296.0) * (highLimit - lowLimit));
                    ELSE
                        channels[channelBase + offset].outputValue := LREAL_TO_REAL(lowLimit + (rawValue / 27648.0) * (highLimit - lowLimit));
                    END_IF;
                1:
                    channels[channelBase + offset].outputValue := LREAL_TO_REAL(rawValue / 10.0);
                2:
                    channels[channelBase + offset].outputValue := LREAL_TO_REAL(rawValue / 100.0);
            END_CASE;
            channels[channelBase + offset].retVal := 0;
        END_IF;
    END_IF;
END_FOR;
END_FUNCTION_BLOCK
