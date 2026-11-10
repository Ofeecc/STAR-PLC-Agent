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
    aHistory : ARRAY[0..99] OF LREAL;
    nCount : INT;
    nNext : INT;
    lrSum : LREAL;
    bPreviousTrigger : BOOL;
    nLastValidWindow : INT;
    bValid : BOOL;
    bEdge : BOOL;
    bWindowChanged : BOOL;
END_VAR

bValid := (windowSize >= 1) AND (windowSize <= 100);
bEdge := trigger AND NOT bPreviousTrigger;
bWindowChanged := bValid AND (windowSize <> nLastValidWindow);

IF NOT bValid THEN
    error := TRUE;
    status := 16#8200;
    bPreviousTrigger := trigger;
    RETURN;
END_IF

error := FALSE;
status := 16#0000;

IF bWindowChanged THEN
    nCount := 0;
    lrSum := 0.0;
    nNext := 0;
    average := 0.0;
    windowSizeReached := FALSE;
    nLastValidWindow := windowSize;
END_IF

IF reset THEN
    nCount := 0;
    lrSum := 0.0;
    nNext := 0;
    average := 0.0;
    windowSizeReached := FALSE;
ELSIF cyclicExecution OR bEdge THEN
    IF nCount < windowSize THEN
        aHistory[nNext] := value;
        lrSum := lrSum + value;
        nCount := nCount + 1;
    ELSE
        lrSum := lrSum - aHistory[nNext] + value;
        aHistory[nNext] := value;
    END_IF;
    nNext := (nNext + 1) MOD windowSize;
    average := lrSum / INT_TO_LREAL(nCount);
    windowSizeReached := nCount >= windowSize;
END_IF

bPreviousTrigger := trigger;
END_FUNCTION_BLOCK
