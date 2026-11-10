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
  sampleCount : INT := 0;
  sumSamples : LREAL := 0.0;
  previousTrigger : BOOL := FALSE;
  lastValidWindowSize : INT := 0;
  i : INT;
  validWindow : BOOL;
  triggerRise : BOOL;
END_VAR

validWindow := (windowSize >= 1) AND (windowSize <= 100);
triggerRise := trigger AND NOT previousTrigger;

IF NOT validWindow THEN
  error := TRUE;
  status := 16#8200;
ELSE
  error := FALSE;
  status := 16#0000;

  IF lastValidWindowSize <> windowSize THEN
    sampleCount := 0;
    sumSamples := 0.0;
    average := 0.0;
    windowSizeReached := FALSE;
    lastValidWindowSize := windowSize;
  END_IF;

  IF reset THEN
    sampleCount := 0;
    sumSamples := 0.0;
    average := 0.0;
    windowSizeReached := FALSE;
  ELSIF cyclicExecution OR triggerRise THEN
    IF sampleCount < windowSize THEN
      sampleCount := sampleCount + 1;
      samples[sampleCount] := value;
      sumSamples := sumSamples + value;
    ELSE
      sumSamples := sumSamples - samples[1] + value;
      IF windowSize > 1 THEN
        FOR i := 1 TO windowSize - 1 DO
          samples[i] := samples[i + 1];
        END_FOR;
      END_IF;
      samples[windowSize] := value;
    END_IF;

    average := sumSamples / sampleCount;
    windowSizeReached := (sampleCount = windowSize);
  END_IF;
END_IF;

previousTrigger := trigger;
END_FUNCTION_BLOCK
