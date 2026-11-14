TYPE ST_Pump :
STRUCT
    priority : INT;
    selection : BOOL;
    RunComd : BOOL;
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_Task
VAR_INPUT
    {attribute 'analysis' := '-27'}
    mode : BOOL;
    start : BOOL;
    stop : BOOL;
END_VAR
VAR_IN_OUT
    pumpGroup : ARRAY[1..5] OF ST_Pump;
END_VAR
VAR
    sampledMode : BOOL;
    sampledStart : BOOL;
    sampledStop : BOOL;
    sampledPriority : ARRAY[1..5] OF INT;
    sampledSelection : ARRAY[1..5] OF BOOL;
    nextCommand : ARRAY[1..5] OF BOOL;
    i : INT;
    j : INT;
    higherCount : INT;
END_VAR

sampledMode := mode;
sampledStart := start;
sampledStop := stop;
FOR i := 1 TO 5 DO
    sampledPriority[i] := pumpGroup[i].priority;
    sampledSelection[i] := pumpGroup[i].selection;
    nextCommand[i] := pumpGroup[i].RunComd;
END_FOR;

IF sampledStop THEN
    FOR i := 1 TO 5 DO
        nextCommand[i] := FALSE;
    END_FOR;
ELSIF sampledStart THEN
    IF sampledMode THEN
        FOR i := 1 TO 5 DO
            higherCount := 0;
            FOR j := 1 TO 5 DO
                IF (sampledPriority[j] > sampledPriority[i]) OR
                   ((sampledPriority[j] = sampledPriority[i]) AND (j < i)) THEN
                    higherCount := higherCount + 1;
                END_IF;
            END_FOR;
            nextCommand[i] := (higherCount < 3);
        END_FOR;
    ELSE
        FOR i := 1 TO 5 DO
            nextCommand[i] := sampledSelection[i];
        END_FOR;
    END_IF;
END_IF;

FOR i := 1 TO 5 DO
    pumpGroup[i].RunComd := nextCommand[i];
END_FOR;
END_FUNCTION_BLOCK
