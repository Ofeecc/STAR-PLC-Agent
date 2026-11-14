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
    phase : INT := 0;
    currentStation : USINT := 1;
    targetStation : USINT := 1;
    sequenceIndex : USINT := 0;
    targetPresent : BOOL := FALSE;
    freshComplete : BOOL := FALSE;
    startPrev : BOOL := FALSE;
    complete2Prev : BOOL := FALSE;
    complete3Prev : BOOL := FALSE;
    complete4Prev : BOOL := FALSE;
END_VAR

conveyorLeft := FALSE;
conveyorRight := FALSE;
targetPresent := FALSE;
CASE targetStation OF
    2: targetPresent := sensor2;
    3: targetPresent := sensor3;
    4: targetPresent := sensor4;
    5: targetPresent := sensor5;
END_CASE;

CASE phase OF
    0:
        IF station1Start AND NOT startPrev AND sensor1 THEN
            sequenceIndex := 1;
            targetStation := processSequence[1];
            currentStation := 1;
            targetPresent := FALSE;
            CASE targetStation OF
                2: targetPresent := sensor2;
                3: targetPresent := sensor3;
                4: targetPresent := sensor4;
                5: targetPresent := sensor5;
            END_CASE;
            IF targetStation = 1 THEN
                phase := 0;
            ELSIF targetPresent THEN
                currentStation := targetStation;
                IF targetStation = 5 THEN
                    sequenceIndex := processLength;
                    phase := 0;
                ELSE
                    phase := 2;
                END_IF
            ELSE
                phase := 1;
            END_IF
        END_IF

    1:
        IF targetPresent THEN
            currentStation := targetStation;
            IF targetStation = 5 THEN
                sequenceIndex := processLength;
                phase := 0;
            ELSE
                phase := 2;
            END_IF
        END_IF

    2:
        freshComplete := ((currentStation = 2) AND station2Complete AND NOT complete2Prev)
                      OR ((currentStation = 3) AND station3Complete AND NOT complete3Prev)
                      OR ((currentStation = 4) AND station4Complete AND NOT complete4Prev);
        IF freshComplete AND (sequenceIndex < processLength) THEN
            sequenceIndex := sequenceIndex + 1;
            targetStation := processSequence[sequenceIndex];
            targetPresent := FALSE;
            CASE targetStation OF
                2: targetPresent := sensor2;
                3: targetPresent := sensor3;
                4: targetPresent := sensor4;
                5: targetPresent := sensor5;
            END_CASE;
            IF targetStation = currentStation THEN
                phase := 2;
            ELSIF targetPresent THEN
                currentStation := targetStation;
                IF targetStation = 5 THEN
                    sequenceIndex := processLength;
                    phase := 0;
                ELSE
                    phase := 2;
                END_IF
            ELSE
                phase := 1;
            END_IF
        END_IF
END_CASE;

IF phase = 1 THEN
    IF targetStation > currentStation THEN
        conveyorRight := TRUE;
        conveyorLeft := FALSE;
    ELSIF targetStation < currentStation THEN
        conveyorLeft := TRUE;
        conveyorRight := FALSE;
    END_IF;
END_IF;

startPrev := station1Start;
complete2Prev := station2Complete;
complete3Prev := station3Complete;
complete4Prev := station4Complete;
END_FUNCTION_BLOCK
