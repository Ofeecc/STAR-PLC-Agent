FUNCTION_BLOCK FB_Task
VAR_INPUT
    cyclicExecution : BOOL;
    trigger : BOOL;
    value : LREAL;
    windowSize : INT;
    reset : BOOL;
END_VAR
VAR_OUTPUT
    average : LREAL := 0.0;
    windowSizeReached : BOOL := FALSE;
    {attribute 'analysis' := '-27'}
    error : BOOL := FALSE;
    {attribute 'analysis' := '-27'}
    status : WORD := 16#0000;
END_VAR
VAR
    sampleBuffer : ARRAY[0..99] OF LREAL;
    sampleCount : INT := 0;
    nextIndex : INT := 0;
    activeWindowSize : INT := 0;
    previousTrigger : BOOL := FALSE;
    triggerRise : BOOL := FALSE;
    mean : LREAL := 0.0;
    sampleSum : LREAL := 0.0;
    i : INT := 0;
END_VAR

triggerRise := trigger AND NOT previousTrigger;
previousTrigger := trigger;

IF (windowSize < 1) OR (windowSize > 100) THEN
    error := TRUE;
    status := 16#8200;
ELSE
    error := FALSE;
    status := 16#0000;

    IF reset OR (windowSize <> activeWindowSize) THEN
        sampleCount := 0;
        nextIndex := 0;
        mean := 0.0;
    END_IF;
    activeWindowSize := windowSize;

    IF NOT reset AND (cyclicExecution OR triggerRise) THEN
        sampleBuffer[nextIndex] := value;
        IF sampleCount < activeWindowSize THEN
            sampleCount := sampleCount + 1;
        END_IF;

        nextIndex := nextIndex + 1;
        IF nextIndex >= activeWindowSize THEN
            nextIndex := 0;
        END_IF;

        sampleSum := 0.0;
        FOR i := 0 TO sampleCount - 1 DO
            sampleSum := sampleSum + sampleBuffer[i];
        END_FOR;
        mean := sampleSum / INT_TO_LREAL(sampleCount);
    END_IF;
END_IF;

average := mean;
windowSizeReached := (activeWindowSize > 0) AND (sampleCount = activeWindowSize);
END_FUNCTION_BLOCK
