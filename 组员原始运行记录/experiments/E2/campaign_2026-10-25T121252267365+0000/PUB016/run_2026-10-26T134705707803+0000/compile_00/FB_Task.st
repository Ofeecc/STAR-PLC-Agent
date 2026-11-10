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
    phase : USINT := 0;
    currentStation : USINT := 1;
    sequenceIndex : USINT := 1;
    targetStation : USINT := 1;
    previousStart : BOOL := FALSE;
    previousStation2Complete : BOOL := FALSE;
    previousStation3Complete : BOOL := FALSE;
    previousStation4Complete : BOOL := FALSE;
    startEdge : BOOL;
    completionEdge : BOOL;
    targetSensor : BOOL;
END_VAR

conveyorLeft := FALSE;
conveyorRight := FALSE;

startEdge := station1Start AND NOT previousStart;
completionEdge := FALSE;

CASE phase OF
    0: // IDLE
        IF startEdge AND sensor1 THEN
            sequenceIndex := 1;
            targetStation := processSequence[1];
            phase := 1;
        END_IF;

    2: // WAIT_PROCESS
        CASE currentStation OF
            2: completionEdge := station2Complete AND NOT previousStation2Complete;
            3: completionEdge := station3Complete AND NOT previousStation3Complete;
            4: completionEdge := station4Complete AND NOT previousStation4Complete;
        END_CASE;

        IF completionEdge THEN
            IF sequenceIndex < processLength THEN
                sequenceIndex := sequenceIndex + 1;
                targetStation := processSequence[sequenceIndex];
                IF targetStation <> currentStation THEN
                    phase := 1;
                END_IF;
            END_IF;
        END_IF;
END_CASE;

IF phase = 1 THEN // MOVING
    CASE targetStation OF
        1: targetSensor := sensor1;
        2: targetSensor := sensor2;
        3: targetSensor := sensor3;
        4: targetSensor := sensor4;
        5: targetSensor := sensor5;
        ELSE targetSensor := FALSE;
    END_CASE;

    IF targetSensor THEN
        currentStation := targetStation;
        IF targetStation = 5 THEN
            phase := 0;
            currentStation := 1;
            sequenceIndex := 1;
        ELSE
            phase := 2;
        END_IF;
    ELSIF targetStation > currentStation THEN
        conveyorRight := TRUE;
    ELSIF targetStation < currentStation THEN
        conveyorLeft := TRUE;
    END_IF;
END_IF;

previousStart := station1Start;
previousStation2Complete := station2Complete;
previousStation3Complete := station3Complete;
previousStation4Complete := station4Complete;
END_FUNCTION_BLOCK
