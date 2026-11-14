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
    history : ARRAY[0..99] OF LREAL;
    historyCount : INT := 0;
    writeIndex : INT := 0;
    lastValidWindowSize : INT := 0;
    previousTrigger : BOOL := FALSE;
    i : INT;
    sampleSum : LREAL;
    triggerRise : BOOL;
    windowChanged : BOOL;
    validWindow : BOOL;
END_VAR

triggerRise := trigger AND NOT previousTrigger;
validWindow := (windowSize >= 1) AND (windowSize <= 100);

IF NOT validWindow THEN
    error := TRUE;
    status := 16#8200;
ELSIF reset THEN
    error := FALSE;
    status := 16#0000;
    historyCount := 0;
    writeIndex := 0;
    lastValidWindowSize := windowSize;
    average := 0.0;
    windowSizeReached := FALSE;
ELSE
    error := FALSE;
    status := 16#0000;
    windowChanged := (lastValidWindowSize <> windowSize);

    IF windowChanged THEN
        historyCount := 0;
        writeIndex := 0;
        lastValidWindowSize := windowSize;
    END_IF;

    IF cyclicExecution OR triggerRise THEN
        history[writeIndex] := value;
        IF historyCount < windowSize THEN
            historyCount := historyCount + 1;
        END_IF;

        writeIndex := writeIndex + 1;
        IF writeIndex >= windowSize THEN
            writeIndex := 0;
        END_IF;

        sampleSum := 0.0;
        FOR i := 0 TO 99 DO
            IF i < historyCount THEN
                sampleSum := sampleSum + history[i];
            END_IF;
        END_FOR;
        average := sampleSum / INT_TO_LREAL(historyCount);
        windowSizeReached := (historyCount >= windowSize);
    ELSIF windowChanged THEN
        average := 0.0;
        windowSizeReached := FALSE;
    END_IF;
END_IF;

previousTrigger := trigger;
END_FUNCTION_BLOCK
