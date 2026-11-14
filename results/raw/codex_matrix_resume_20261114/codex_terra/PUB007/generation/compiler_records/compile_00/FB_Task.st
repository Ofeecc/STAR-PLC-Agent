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
    pumpIndex : INT;
    otherIndex : INT;
    higherCount : INT;
END_VAR

IF stop THEN
    FOR pumpIndex := 1 TO 5 DO
        pumpGroup[pumpIndex].RunComd := FALSE;
    END_FOR;
ELSIF start THEN
    IF NOT mode THEN
        FOR pumpIndex := 1 TO 5 DO
            pumpGroup[pumpIndex].RunComd := pumpGroup[pumpIndex].selection;
        END_FOR;
    ELSE
        FOR pumpIndex := 1 TO 5 DO
            higherCount := 0;
            FOR otherIndex := 1 TO 5 DO
                IF (pumpGroup[otherIndex].priority > pumpGroup[pumpIndex].priority) OR
                   ((pumpGroup[otherIndex].priority = pumpGroup[pumpIndex].priority) AND (otherIndex < pumpIndex)) THEN
                    higherCount := higherCount + 1;
                END_IF;
            END_FOR;
            pumpGroup[pumpIndex].RunComd := higherCount < 3;
        END_FOR;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
