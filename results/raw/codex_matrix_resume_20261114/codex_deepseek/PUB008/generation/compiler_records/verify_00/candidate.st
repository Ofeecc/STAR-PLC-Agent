TYPE ST_AnalogChannel :
STRUCT
    enable : BOOL;
    hiLIM : REAL;
    loLIM : REAL;
    bipolar : BOOL;
    measuringMode : INT;
    retVal : WORD;
    outputValue : REAL;
END_STRUCT
END_TYPE

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
    rawValue : INT;
    rangeValue : REAL;
END_VAR

analogIndex := LOWER_BOUND(analogValues, 1);
channelIndex := LOWER_BOUND(channels, 1);

FOR i := 0 TO count - 1 DO
    IF channels[channelIndex + i].enable THEN
        IF (channels[channelIndex + i].measuringMode <> 0) AND
           (channels[channelIndex + i].measuringMode <> 1) AND
           (channels[channelIndex + i].measuringMode <> 2) THEN
            channels[channelIndex + i].retVal := 16#8001;
        ELSIF channels[channelIndex + i].hiLIM <= channels[channelIndex + i].loLIM THEN
            channels[channelIndex + i].retVal := 16#8002;
        ELSE
            rawValue := analogValues[analogIndex + i];
            rangeValue := channels[channelIndex + i].hiLIM - channels[channelIndex + i].loLIM;

            CASE channels[channelIndex + i].measuringMode OF
                0:
                    IF channels[channelIndex + i].bipolar THEN
                        channels[channelIndex + i].outputValue := channels[channelIndex + i].loLIM +
                            ((INT_TO_REAL(rawValue) + 27648.0) / 55296.0) * rangeValue;
                    ELSE
                        channels[channelIndex + i].outputValue := channels[channelIndex + i].loLIM +
                            (INT_TO_REAL(rawValue) / 27648.0) * rangeValue;
                    END_IF
                1:
                    channels[channelIndex + i].outputValue := INT_TO_REAL(rawValue) / 10.0;
                2:
                    channels[channelIndex + i].outputValue := INT_TO_REAL(rawValue) / 100.0;
            END_CASE

            channels[channelIndex + i].retVal := 0;
        END_IF
    END_IF
END_FOR
END_FUNCTION_BLOCK
