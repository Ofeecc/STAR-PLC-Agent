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
    i : INT;
    k : INT;
    bestIdx : INT;
    bestPriority : INT;
    found : BOOL;
    used : ARRAY[1..5] OF BOOL;
END_VAR

IF stop THEN
    FOR i := 1 TO 5 DO
        pumpGroup[i].RunComd := FALSE;
    END_FOR
ELSIF start THEN
    IF NOT mode THEN
        FOR i := 1 TO 5 DO
            pumpGroup[i].RunComd := pumpGroup[i].selection;
        END_FOR
    ELSE
        FOR i := 1 TO 5 DO
            pumpGroup[i].RunComd := FALSE;
            used[i] := FALSE;
        END_FOR
        FOR k := 1 TO 3 DO
            bestIdx := 0;
            bestPriority := 0;
            found := FALSE;
            FOR i := 1 TO 5 DO
                IF NOT used[i] THEN
                    IF (NOT found) OR (pumpGroup[i].priority > bestPriority) THEN
                        bestIdx := i;
                        bestPriority := pumpGroup[i].priority;
                        found := TRUE;
                    END_IF
                END_IF
            END_FOR
            IF bestIdx <> 0 THEN
                pumpGroup[bestIdx].RunComd := TRUE;
                used[bestIdx] := TRUE;
            END_IF
        END_FOR
    END_IF
END_IF
END_FUNCTION_BLOCK
