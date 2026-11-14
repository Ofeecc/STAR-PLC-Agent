FUNCTION_BLOCK FB_Task
VAR_INPUT
    Value : REAL;
    hiLevel : REAL;
    loLevel : REAL;
    hystWindow : REAL;
END_VAR
VAR_OUTPUT
    hiAlarm : BOOL := FALSE;
    loAlarm : BOOL := FALSE;
    {attribute 'analysis' := '-27'}
    error : BOOL := FALSE;
    {attribute 'analysis' := '-27'}
    status : WORD := 16#0000;
END_VAR
VAR
    sampledValue : REAL;
    sampledHi : REAL;
    sampledLo : REAL;
    sampledHyst : REAL;
    limitSpan : REAL;
    highRelease : REAL;
    lowRelease : REAL;
    qHi : BOOL := FALSE;
    qLo : BOOL := FALSE;
    diagError : BOOL := FALSE;
    diagStatus : WORD := 16#0000;
END_VAR

sampledValue := Value;
sampledHi := hiLevel;
sampledLo := loLevel;
sampledHyst := hystWindow;

diagError := FALSE;
diagStatus := 16#0000;

IF sampledLo >= sampledHi THEN
    diagError := TRUE;
    diagStatus := 16#8001;
ELSE
    limitSpan := sampledHi - sampledLo;
    IF sampledHyst >= limitSpan THEN
        diagError := TRUE;
        diagStatus := 16#8002;
    ELSE
        highRelease := sampledHi - sampledHyst;
        lowRelease := sampledLo + sampledHyst;

        IF sampledValue > sampledHi THEN
            qHi := TRUE;
        ELSIF sampledValue < highRelease THEN
            qHi := FALSE;
        END_IF;

        IF sampledValue < sampledLo THEN
            qLo := TRUE;
        ELSIF sampledValue > lowRelease THEN
            qLo := FALSE;
        END_IF;
    END_IF;
END_IF;

hiAlarm := qHi;
loAlarm := qLo;
error := diagError;
status := diagStatus;
END_FUNCTION_BLOCK
