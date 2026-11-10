FUNCTION_BLOCK FB_Task
VAR_INPUT
    processLength : USINT;
    sensor1 : BOOL;
    sensor2 : BOOL;
    sensor3 : BOOL;
    sensor4 : BOOL;
    sensor5 : BOOL;
    station1Start : BOOL;
    station2Complete : BOOL;
    station3Complete : BOOL;
    station4Complete : BOOL;
    processSequence : ARRAY[1..8] OF USINT;
END_VAR
VAR_OUTPUT
    conveyorLeft : BOOL;
    conveyorRight : BOOL;
END_VAR
VAR
    phase : INT;
    currentStation : USINT;
    sequenceIndex : USINT;
    targetStation : USINT;
    prevStation1Start : BOOL;
    prevStation2Complete : BOOL;
    prevStation3Complete : BOOL;
    prevStation4Complete : BOOL;
    startEdge : BOOL;
    completionEdge : BOOL;
    arrived : BOOL;
END_VAR

conveyorLeft := FALSE;
conveyorRight := FALSE;

startEdge := station1Start AND NOT prevStation1Start;

CASE phase OF
    0:
        IF startEdge AND sensor1 THEN
            sequenceIndex := 1;
            currentStation := 1;
            targetStation := processSequence[1];
            IF targetStation > currentStation THEN
                phase := 1;
                conveyorRight := TRUE;
            ELSIF targetStation < currentStation THEN
                phase := 1;
                conveyorLeft := TRUE;
            ELSE
                phase := 2;
            END_IF;
        END_IF;

    1:
        arrived := FALSE;
        CASE targetStation OF
            1: arrived := sensor1;
            2: arrived := sensor2;
            3: arrived := sensor3;
            4: arrived := sensor4;
            5: arrived := sensor5;
        ELSE
            arrived := FALSE;
        END_CASE;

        IF arrived THEN
            currentStation := targetStation;
            IF targetStation = 5 THEN
                phase := 0;
            ELSE
                phase := 2;
            END_IF;
        ELSE
            IF targetStation > currentStation THEN
                conveyorRight := TRUE;
                conveyorLeft := FALSE;
            ELSIF targetStation < currentStation THEN
                conveyorLeft := TRUE;
                conveyorRight := FALSE;
            ELSE
                conveyorLeft := FALSE;
                conveyorRight := FALSE;
            END_IF;
        END_IF;

    2:
        completionEdge := FALSE;
        CASE currentStation OF
            2:
                completionEdge := station2Complete AND NOT prevStation2Complete;
            3:
                completionEdge := station3Complete AND NOT prevStation3Complete;
            4:
                completionEdge := station4Complete AND NOT prevStation4Complete;
        ELSE
            completionEdge := FALSE;
        END_CASE;

        IF completionEdge THEN
            IF sequenceIndex < processLength THEN
                sequenceIndex := sequenceIndex + 1;
                targetStation := processSequence[sequenceIndex];
                IF targetStation = currentStation THEN
                    phase := 2;
                ELSIF targetStation > currentStation THEN
                    phase := 1;
                    conveyorRight := TRUE;
                ELSIF targetStation < currentStation THEN
                    phase := 1;
                    conveyorLeft := TRUE;
                ELSE
                    phase := 2;
                END_IF;
            ELSE
                phase := 0;
            END_IF;
        END_IF;

    ELSE
        phase := 0;
END_CASE;

prevStation1Start := station1Start;
prevStation2Complete := station2Complete;
prevStation3Complete := station3Complete;
prevStation4Complete := station4Complete;
END_FUNCTION_BLOCK
