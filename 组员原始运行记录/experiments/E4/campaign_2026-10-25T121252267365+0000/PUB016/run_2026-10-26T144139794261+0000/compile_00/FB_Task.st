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
    targetStation : USINT;
    previousStation1Start : BOOL;
    previousStation2Complete : BOOL;
    previousStation3Complete : BOOL;
    previousStation4Complete : BOOL;
    startRising : BOOL;
    station2CompleteRising : BOOL;
    station3CompleteRising : BOOL;
    station4CompleteRising : BOOL;
    completionRising : BOOL;
    arrivalSensor : BOOL;
END_VAR

conveyorLeft := FALSE;
conveyorRight := FALSE;
completionRising := FALSE;
arrivalSensor := FALSE;

startRising := station1Start AND NOT previousStation1Start;
station2CompleteRising := station2Complete AND NOT previousStation2Complete;
station3CompleteRising := station3Complete AND NOT previousStation3Complete;
station4CompleteRising := station4Complete AND NOT previousStation4Complete;

CASE phase OF
    0:
        IF startRising AND sensor1 THEN
            currentStation := 1;
            sequenceIndex := 1;
            targetStation := processSequence[1];
            phase := 1;
        END_IF

    2:
        CASE currentStation OF
            2:
                completionRising := station2CompleteRising;
            3:
                completionRising := station3CompleteRising;
            4:
                completionRising := station4CompleteRising;
        END_CASE

        IF completionRising AND (sequenceIndex < processLength) THEN
            sequenceIndex := sequenceIndex + 1;
            targetStation := processSequence[sequenceIndex];

            IF targetStation = currentStation THEN
                phase := 2;
            ELSE
                phase := 1;
            END_IF
        END_IF
END_CASE

IF phase = 1 THEN
    CASE targetStation OF
        1:
            arrivalSensor := sensor1;
        2:
            arrivalSensor := sensor2;
        3:
            arrivalSensor := sensor3;
        4:
            arrivalSensor := sensor4;
        5:
            arrivalSensor := sensor5;
    END_CASE

    IF arrivalSensor THEN
        currentStation := targetStation;

        IF targetStation = 5 THEN
            phase := 0;
        ELSE
            phase := 2;
        END_IF
    ELSIF targetStation > currentStation THEN
        conveyorRight := TRUE;
    ELSIF targetStation < currentStation THEN
        conveyorLeft := TRUE;
    END_IF
END_IF

previousStation1Start := station1Start;
previousStation2Complete := station2Complete;
previousStation3Complete := station3Complete;
previousStation4Complete := station4Complete;
END_FUNCTION_BLOCK
