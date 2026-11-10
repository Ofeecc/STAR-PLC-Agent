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
    writeIndex : INT := 1;
    sampleSum : LREAL := 0.0;
    previousTrigger : BOOL := FALSE;
    lastWindowSize : INT := 0;
    triggerRise : BOOL;
    windowChanged : BOOL;
END_VAR

triggerRise := trigger AND NOT previousTrigger;
previousTrigger := trigger;

IF (windowSize < 1) OR (windowSize > 100) THEN
    error := TRUE;
    status := 16#8200;
    RETURN;
END_IF;

error := FALSE;
status := 16#0000;
windowChanged := windowSize <> lastWindowSize;

IF windowChanged THEN
    lastWindowSize := windowSize;
END_IF;

IF reset OR windowChanged THEN
    sampleCount := 0;
    writeIndex := 1;
    sampleSum := 0.0;
    average := 0.0;
    windowSizeReached := FALSE;
END_IF;

IF reset THEN
    RETURN;
END_IF;

IF cyclicExecution OR triggerRise THEN
    IF sampleCount >= windowSize THEN
        sampleSum := sampleSum - samples[writeIndex];
    ELSE
        sampleCount := sampleCount + 1;
    END_IF;

    samples[writeIndex] := value;
    sampleSum := sampleSum + value;

    writeIndex := writeIndex + 1;
    IF writeIndex > windowSize THEN
        writeIndex := 1;
    END_IF;

    average := sampleSum / TO_LREAL(sampleCount);
    windowSizeReached := sampleCount = windowSize;
END_IF;
END_FUNCTION_BLOCK
