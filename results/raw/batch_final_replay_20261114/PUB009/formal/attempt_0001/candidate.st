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
    previousTrigger : BOOL := FALSE;
    lastValidWindowSize : INT := 0;
    historyBuffer : ARRAY[0..99] OF LREAL;
    historyCount : INT := 0;
    historyHead : INT := 0;
    historySum : LREAL := 0.0;
    internalAverage : LREAL := 0.0;
    internalWindowSizeReached : BOOL := FALSE;
    invalidWindow : BOOL := FALSE;
    triggerRise : BOOL := FALSE;
    windowChanged : BOOL := FALSE;
    validWindow : BOOL := FALSE;
END_VAR

triggerRise := trigger AND NOT previousTrigger;
previousTrigger := trigger;

validWindow := (windowSize >= 1) AND (windowSize <= 100);

IF NOT validWindow THEN
    invalidWindow := TRUE;
ELSE
    invalidWindow := FALSE;
    IF reset THEN
        historyCount := 0;
        historyHead := 0;
        historySum := 0.0;
        internalAverage := 0.0;
        internalWindowSizeReached := FALSE;
        lastValidWindowSize := windowSize;
    ELSE
        windowChanged := (windowSize <> lastValidWindowSize);
        IF windowChanged THEN
            historyCount := 0;
            historyHead := 0;
            historySum := 0.0;
            internalAverage := 0.0;
            internalWindowSizeReached := FALSE;
            lastValidWindowSize := windowSize;
        END_IF;

        IF cyclicExecution OR triggerRise THEN
            IF historyCount < windowSize THEN
                historyBuffer[historyHead] := value;
                historySum := historySum + value;
                historyCount := historyCount + 1;
                historyHead := (historyHead + 1) MOD windowSize;
                internalAverage := historySum / historyCount;
                internalWindowSizeReached := (historyCount >= windowSize);
            ELSE
                historySum := historySum - historyBuffer[historyHead] + value;
                historyBuffer[historyHead] := value;
                historyHead := (historyHead + 1) MOD windowSize;
                internalAverage := historySum / historyCount;
                internalWindowSizeReached := TRUE;
            END_IF;
        END_IF;
    END_IF;
END_IF;

average := internalAverage;
windowSizeReached := internalWindowSizeReached;
error := invalidWindow;
IF invalidWindow THEN
    status := 16#8200;
ELSE
    status := 16#0000;
END_IF;
END_FUNCTION_BLOCK
