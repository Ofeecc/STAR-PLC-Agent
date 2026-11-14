TYPE ST_Pump :
STRUCT
    priority : INT;
    selection : BOOL;
    RunComd : BOOL;
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_Task
VAR_INPUT
    mode : BOOL;
    start : BOOL;
    stop : BOOL;
END_VAR
VAR_IN_OUT
    pumpGroup : ARRAY[1..5] OF ST_Pump;
END_VAR
VAR
    runCmd : ARRAY[1..5] OF BOOL;
    modeSampled : BOOL;
    startSampled : BOOL;
    stopSampled : BOOL;
    prioritySampled : ARRAY[1..5] OF INT;
    selectionSampled : ARRAY[1..5] OF BOOL;
    sortIndex : ARRAY[1..5] OF INT;
    i : INT;
    j : INT;
    tmpIndex : INT;
END_VAR

// 1. Sample all inputs once at scan start
modeSampled := mode;
startSampled := start;
stopSampled := stop;
FOR i := 1 TO 5 DO
    prioritySampled[i] := pumpGroup[i].priority;
    selectionSampled[i] := pumpGroup[i].selection;
    sortIndex[i] := i;
END_FOR;

// Prepare automatic priority order: descending priority, ties by lower array index
FOR i := 1 TO 4 DO
    FOR j := 1 TO (5 - i) DO
        IF (prioritySampled[sortIndex[j]] < prioritySampled[sortIndex[j + 1]]) OR
           ((prioritySampled[sortIndex[j]] = prioritySampled[sortIndex[j + 1]]) AND (sortIndex[j] > sortIndex[j + 1])) THEN
            tmpIndex := sortIndex[j];
            sortIndex[j] := sortIndex[j + 1];
            sortIndex[j + 1] := tmpIndex;
        END_IF;
    END_FOR;
END_FOR;

// 2. Safety/priority and state transition. Stop wins over simultaneous start.
IF stopSampled THEN
    FOR i := 1 TO 5 DO
        runCmd[i] := FALSE;
    END_FOR;
ELSIF startSampled THEN
    IF NOT modeSampled THEN
        // Manual mode: latch the selected pumps
        FOR i := 1 TO 5 DO
            runCmd[i] := selectionSampled[i];
        END_FOR;
    ELSE
        // Automatic mode: latch exactly the highest-priority three pumps
        FOR i := 1 TO 5 DO
            runCmd[i] := FALSE;
        END_FOR;
        FOR i := 1 TO 3 DO
            runCmd[sortIndex[i]] := TRUE;
        END_FOR;
    END_IF;
END_IF;
// Else: neither stop nor start is TRUE; hold runCmd unchanged.

// 3. No timer operations are required by this specification.

// 4. Unified output assignment: write only RunComd, never priority or selection
FOR i := 1 TO 5 DO
    pumpGroup[i].RunComd := runCmd[i];
END_FOR;
END_FUNCTION_BLOCK
