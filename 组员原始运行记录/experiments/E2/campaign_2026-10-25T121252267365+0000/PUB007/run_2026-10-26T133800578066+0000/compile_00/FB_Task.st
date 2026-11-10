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
    j : INT;
    rank : INT;
END_VAR

IF stop THEN
    FOR i := 1 TO 5 DO
        pumpGroup[i].RunComd := FALSE;
    END_FOR;
ELSIF start THEN
    IF mode THEN
        FOR i := 1 TO 5 DO
            rank := 0;
            FOR j := 1 TO 5 DO
                IF (pumpGroup[j].priority > pumpGroup[i].priority) OR
                   ((pumpGroup[j].priority = pumpGroup[i].priority) AND (j < i)) THEN
                    rank := rank + 1;
                END_IF;
            END_FOR;
            pumpGroup[i].RunComd := rank < 3;
        END_FOR;
    ELSE
        FOR i := 1 TO 5 DO
            pumpGroup[i].RunComd := pumpGroup[i].selection;
        END_FOR;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
