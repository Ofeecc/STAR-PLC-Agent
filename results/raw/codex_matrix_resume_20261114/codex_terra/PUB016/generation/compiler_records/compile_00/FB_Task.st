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
    conveyorLeft : BOOL := FALSE;
    conveyorRight : BOOL := FALSE;
END_VAR
VAR
    phase : USINT := 0;
    currentStation : USINT := 1;
    sequenceIndex : USINT := 0;
    targetStation : USINT := 1;
    previousStart : BOOL := FALSE;
    previousComplete2 : BOOL := FALSE;
    previousComplete3 : BOOL := FALSE;
    previousComplete4 : BOOL := FALSE;
    startEdge : BOOL;
    complete2Edge : BOOL;
    complete3Edge : BOOL;
    complete4Edge : BOOL;
    matchingCompletion : BOOL;
    targetSensor : BOOL;
    arrivedThisScan : BOOL;
    advancedThisScan : BOOL;
END_VAR

startEdge := station1Start AND NOT previousStart;
complete2Edge := station2Complete AND NOT previousComplete2;
complete3Edge := station3Complete AND NOT previousComplete3;
complete4Edge := station4Complete AND NOT previousComplete4;
previousStart := station1Start;
previousComplete2 := station2Complete;
previousComplete3 := station3Complete;
previousComplete4 := station4Complete;
conveyorLeft := FALSE;
conveyorRight := FALSE;
arrivedThisScan := FALSE;
advancedThisScan := FALSE;

IF phase = 0 THEN
    IF startEdge AND sensor1 AND (processLength >= 1) AND (processLength <= 8) THEN
        currentStation := 1;
        sequenceIndex := 1;
        targetStation := processSequence[1];
        phase := 1;
        advancedThisScan := TRUE;
    END_IF;
ELSIF phase = 3 THEN
    phase := 1;
END_IF;

IF phase = 1 THEN
    targetSensor := FALSE;
    CASE targetStation OF
        1: targetSensor := sensor1;
        2: targetSensor := sensor2;
        3: targetSensor := sensor3;
        4: targetSensor := sensor4;
        5: targetSensor := sensor5;
    END_CASE;
    IF targetSensor THEN
        currentStation := targetStation;
        arrivedThisScan := TRUE;
        IF targetStation = 5 THEN
            phase := 0;
        ELSE
            phase := 2;
        END_IF;
    END_IF;
END_IF;

IF (phase = 2) AND NOT advancedThisScan THEN
    matchingCompletion := FALSE;
    CASE currentStation OF
        2: matchingCompletion := complete2Edge;
        3: matchingCompletion := complete3Edge;
        4: matchingCompletion := complete4Edge;
    END_CASE;
    IF matchingCompletion AND (sequenceIndex < processLength) AND (sequenceIndex < 8) THEN
        sequenceIndex := sequenceIndex + 1;
        targetStation := processSequence[sequenceIndex];
        advancedThisScan := TRUE;
        IF targetStation <> currentStation THEN
            IF arrivedThisScan THEN
                phase := 3;
            ELSE
                phase := 1;
            END_IF;
        END_IF;
    END_IF;
END_IF;

IF phase = 1 THEN
    targetSensor := FALSE;
    CASE targetStation OF
        1: targetSensor := sensor1;
        2: targetSensor := sensor2;
        3: targetSensor := sensor3;
        4: targetSensor := sensor4;
        5: targetSensor := sensor5;
    END_CASE;
    IF targetSensor THEN
        currentStation := targetStation;
        IF targetStation = 5 THEN
            phase := 0;
        ELSE
            phase := 2;
        END_IF;
    ELSIF targetStation > currentStation THEN
        conveyorRight := TRUE;
    ELSIF targetStation < currentStation THEN
        conveyorLeft := TRUE;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
