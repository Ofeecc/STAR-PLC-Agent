{attribute 'analysis' := '-27'}
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
    error : BOOL := FALSE;
    status : WORD := 16#0000;
END_VAR
VAR
    samples : ARRAY[1..100] OF LREAL;
    sampleCount : INT := 0;
    nextIndex : INT := 1;
    configuredWindow : INT := 0;
    total : LREAL := 0.0;
    previousTrigger : BOOL := FALSE;
END_VAR

IF (windowSize < 1) OR (windowSize > 100) THEN
    error := TRUE;
    status := 16#8200;
ELSE
    error := FALSE;
    status := 16#0000;

    IF reset OR (windowSize <> configuredWindow) THEN
        sampleCount := 0;
        nextIndex := 1;
        total := 0.0;
        average := 0.0;
        windowSizeReached := FALSE;
    END_IF;
    configuredWindow := windowSize;

    IF NOT reset AND (cyclicExecution OR (trigger AND NOT previousTrigger)) THEN
        IF sampleCount = windowSize THEN
            total := total - samples[nextIndex];
        ELSE
            sampleCount := sampleCount + 1;
        END_IF;
        samples[nextIndex] := value;
        total := total + value;
        nextIndex := nextIndex + 1;
        IF nextIndex > windowSize THEN
            nextIndex := 1;
        END_IF;
        average := total / INT_TO_LREAL(sampleCount);
        windowSizeReached := sampleCount = windowSize;
    END_IF;
END_IF;
previousTrigger := trigger;
END_FUNCTION_BLOCK
