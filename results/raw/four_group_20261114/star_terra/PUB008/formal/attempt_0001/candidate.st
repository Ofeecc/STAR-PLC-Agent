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
    sampledCount : DINT;
    analogLower : DINT;
    analogUpper : DINT;
    channelLower : DINT;
    channelUpper : DINT;
    analogLength : LINT;
    channelLength : LINT;
    j : DINT;
    analogIndex : DINT;
    channelIndex : DINT;
    rawValue : LREAL;
    lowLimit : LREAL;
    highLimit : LREAL;
    convertedValue : LREAL;
END_VAR

sampledCount := count;
analogLower := LOWER_BOUND(analogValues, 1);
analogUpper := UPPER_BOUND(analogValues, 1);
channelLower := LOWER_BOUND(channels, 1);
channelUpper := UPPER_BOUND(channels, 1);

analogLength := DINT_TO_LINT(analogUpper) - DINT_TO_LINT(analogLower) + LINT#1;
channelLength := DINT_TO_LINT(channelUpper) - DINT_TO_LINT(channelLower) + LINT#1;

IF (sampledCount > 0) AND (DINT_TO_LINT(sampledCount) <= analogLength) AND (DINT_TO_LINT(sampledCount) <= channelLength) THEN
    FOR j := 0 TO sampledCount - 1 DO
        channelIndex := channelLower + j;
        IF channels[channelIndex].enable THEN
            IF (channels[channelIndex].measuringMode < 0) OR (channels[channelIndex].measuringMode > 2) THEN
                channels[channelIndex].retVal := WORD#16#8001;
            ELSIF channels[channelIndex].hiLIM <= channels[channelIndex].loLIM THEN
                channels[channelIndex].retVal := WORD#16#8002;
            ELSE
                analogIndex := analogLower + j;
                rawValue := INT_TO_LREAL(analogValues[analogIndex]);
                CASE channels[channelIndex].measuringMode OF
                    0:
                        lowLimit := REAL_TO_LREAL(channels[channelIndex].loLIM);
                        highLimit := REAL_TO_LREAL(channels[channelIndex].hiLIM);
                        IF channels[channelIndex].bipolar THEN
                            convertedValue := lowLimit + ((rawValue + LREAL#27648.0) / LREAL#55296.0) * (highLimit - lowLimit);
                        ELSE
                            convertedValue := lowLimit + (rawValue / LREAL#27648.0) * (highLimit - lowLimit);
                        END_IF;
                    1:
                        convertedValue := rawValue / LREAL#10.0;
                    2:
                        convertedValue := rawValue / LREAL#100.0;
                END_CASE;
                channels[channelIndex].outputValue := LREAL_TO_REAL(convertedValue);
                channels[channelIndex].retVal := WORD#16#0000;
            END_IF;
        END_IF;
    END_FOR;
END_IF;
END_FUNCTION_BLOCK
