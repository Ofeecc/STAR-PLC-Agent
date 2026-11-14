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
    sampledMode : BOOL;
    sampledStart : BOOL;
    sampledStop : BOOL;
    autoRequest : BOOL;
    runNext : ARRAY[1..5] OF BOOL;
    topThree : ARRAY[1..5] OF BOOL;
    i : INT;
    j : INT;
    rank : INT;
END_VAR

// Stage 1: sample inputs once for the scan
sampledMode := mode;
sampledStart := start;
sampledStop := stop;

// Stage 2: select operating request; stop has priority over start
autoRequest := FALSE;
IF (NOT sampledStop) AND sampledStart AND sampledMode THEN
    autoRequest := TRUE;
END_IF;

// Stage 3: no timer FBs are required in this design

// Stage 4: unified output assignment
IF autoRequest THEN
    FOR i := 1 TO 5 DO
        topThree[i] := FALSE;
    END_FOR;

    FOR i := 1 TO 5 DO
        rank := 0;
        FOR j := 1 TO 5 DO
            IF (pumpGroup[j].priority > pumpGroup[i].priority)
               OR ((pumpGroup[j].priority = pumpGroup[i].priority) AND (j < i)) THEN
                rank := rank + 1;
            END_IF;
        END_FOR;

        IF rank < 3 THEN
            topThree[i] := TRUE;
        END_IF;
    END_FOR;
END_IF;

FOR i := 1 TO 5 DO
    IF sampledStop THEN
        runNext[i] := FALSE;
    ELSIF sampledStart THEN
        IF sampledMode THEN
            runNext[i] := topThree[i];
        ELSE
            runNext[i] := pumpGroup[i].selection;
        END_IF;
    ELSE
        runNext[i] := pumpGroup[i].RunComd;
    END_IF;
END_FOR;

FOR i := 1 TO 5 DO
    pumpGroup[i].RunComd := runNext[i];
END_FOR;
END_FUNCTION_BLOCK
