FUNCTION_BLOCK FB_Task
VAR_INPUT
    cyclicExecution : BOOL;
    trigger : BOOL;
    value : LREAL;
    windowSize : INT;
    reset : BOOL;
END_VAR
VAR_OUTPUT
    average : LREAL;
    windowSizeReached : BOOL;
    error : BOOL;
    status : WORD;
END_VAR
VAR
    samples : ARRAY[1..100] OF LREAL;
    sampleCount : INT;
    writeIndex : INT := 1;
    sampleSum : LREAL;
    previousTrigger : BOOL;
    lastWindowSize : INT;
    acceptSample : BOOL;
END_VAR

acceptSample := FALSE;

IF (windowSize < 1) OR (windowSize > 100) THEN
    error := TRUE;
    status := WORD#16#8200;
ELSE
    error := FALSE;
    status := WORD#16#0000;

    IF windowSize <> lastWindowSize THEN
        sampleCount := 0;
        writeIndex := 1;
        sampleSum := 0.0;
        average := 0.0;
        windowSizeReached := FALSE;
        lastWindowSize := windowSize;
    END_IF;

    IF reset THEN
        sampleCount := 0;
        writeIndex := 1;
        sampleSum := 0.0;
        average := 0.0;
        windowSizeReached := FALSE;
    ELSE
        acceptSample := cyclicExecution OR (trigger AND NOT previousTrigger);
        IF acceptSample THEN
            IF sampleCount < windowSize THEN
                sampleCount := sampleCount + 1;
            ELSE
                sampleSum := sampleSum - samples[writeIndex];
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
    END_IF;
END_IF;

previousTrigger := trigger;
END_FUNCTION_BLOCK
