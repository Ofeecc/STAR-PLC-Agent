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
    lbA : DINT;
    ubA : DINT;
    lenA : DINT;
    lbC : DINT;
    ubC : DINT;
    lenC : DINT;
    nProcess : DINT;
    i : DINT;
    idxA : DINT;
    idxC : DINT;
    mode : INT;
    raw : INT;
    lo : REAL;
    hi : REAL;
END_VAR

lbA := LOWER_BOUND(analogValues, 1);
ubA := UPPER_BOUND(analogValues, 1);
lenA := ubA - lbA + 1;
lbC := LOWER_BOUND(channels, 1);
ubC := UPPER_BOUND(channels, 1);
lenC := ubC - lbC + 1;

IF count < 0 THEN
    nProcess := 0;
ELSIF count > lenA THEN
    nProcess := lenA;
ELSE
    nProcess := count;
END_IF;

IF nProcess > lenC THEN
    nProcess := lenC;
END_IF;

IF nProcess < 0 THEN
    nProcess := 0;
END_IF;

IF nProcess > 0 THEN
    FOR i := 0 TO nProcess - 1 DO
        idxC := lbC + i;
        IF channels[idxC].enable THEN
            mode := channels[idxC].measuringMode;
            lo := channels[idxC].loLIM;
            hi := channels[idxC].hiLIM;
            IF (mode <> 0) AND (mode <> 1) AND (mode <> 2) THEN
                channels[idxC].retVal := 16#8001;
            ELSIF hi <= lo THEN
                channels[idxC].retVal := 16#8002;
            ELSE
                idxA := lbA + i;
                raw := analogValues[idxA];
                IF mode = 0 THEN
                    IF channels[idxC].bipolar THEN
                        channels[idxC].outputValue := lo + ((INT_TO_REAL(raw) + 27648.0) / 55296.0) * (hi - lo);
                    ELSE
                        channels[idxC].outputValue := lo + (INT_TO_REAL(raw) / 27648.0) * (hi - lo);
                    END_IF;
                ELSIF mode = 1 THEN
                    channels[idxC].outputValue := INT_TO_REAL(raw) / 10.0;
                ELSIF mode = 2 THEN
                    channels[idxC].outputValue := INT_TO_REAL(raw) / 100.0;
                END_IF;
                channels[idxC].retVal := 0;
            END_IF;
        END_IF;
    END_FOR;
END_IF;
END_FUNCTION_BLOCK
