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
VAR CONSTANT
    PHASE_IDLE : INT := 0;
    PHASE_MOVING : INT := 1;
    PHASE_WAIT_PROCESS : INT := 2;
END_VAR
VAR
    phase : INT := 0;
    currentStation : USINT := 1;
    sequenceIndex : USINT := 0;
    target : USINT := 1;
    prevStation1Start : BOOL := FALSE;
    prevStation2Complete : BOOL := FALSE;
    prevStation3Complete : BOOL := FALSE;
    prevStation4Complete : BOOL := FALSE;
    startRise : BOOL;
    comp2Rise : BOOL;
    comp3Rise : BOOL;
    comp4Rise : BOOL;
    targetSensor : BOOL;
    freshMatchingCompletion : BOOL;
END_VAR

startRise := station1Start AND NOT prevStation1Start;
comp2Rise := station2Complete AND NOT prevStation2Complete;
comp3Rise := station3Complete AND NOT prevStation3Complete;
comp4Rise := station4Complete AND NOT prevStation4Complete;

targetSensor := FALSE;
CASE target OF
    1: targetSensor := sensor1;
    2: targetSensor := sensor2;
    3: targetSensor := sensor3;
    4: targetSensor := sensor4;
    5: targetSensor := sensor5;
ELSE
    targetSensor := FALSE;
END_CASE;

CASE phase OF
    PHASE_IDLE:
        IF startRise AND sensor1 AND (processLength >= 1) AND (processLength <= 8) THEN
            IF (processSequence[processLength] = 5) AND (processSequence[1] <> 1) THEN
                currentStation := 1;
                sequenceIndex := 1;
                target := processSequence[1];
                phase := PHASE_MOVING;
            END_IF;
        END_IF;

    PHASE_MOVING:
        IF targetSensor THEN
            currentStation := target;
            IF target = 5 THEN
                sequenceIndex := processLength;
                phase := PHASE_IDLE;
            ELSE
                phase := PHASE_WAIT_PROCESS;
            END_IF;
        END_IF;

    PHASE_WAIT_PROCESS:
        freshMatchingCompletion := FALSE;
        CASE currentStation OF
            2: freshMatchingCompletion := comp2Rise;
            3: freshMatchingCompletion := comp3Rise;
            4: freshMatchingCompletion := comp4Rise;
        ELSE
            freshMatchingCompletion := FALSE;
        END_CASE;
        IF freshMatchingCompletion THEN
            IF sequenceIndex < processLength THEN
                sequenceIndex := sequenceIndex + 1;
                target := processSequence[sequenceIndex];
                IF target = currentStation THEN
                    phase := PHASE_WAIT_PROCESS;
                ELSE
                    phase := PHASE_MOVING;
                END_IF;
            ELSE
                phase := PHASE_IDLE;
            END_IF;
        END_IF;

ELSE
    phase := PHASE_IDLE;
END_CASE;

targetSensor := FALSE;
CASE target OF
    1: targetSensor := sensor1;
    2: targetSensor := sensor2;
    3: targetSensor := sensor3;
    4: targetSensor := sensor4;
    5: targetSensor := sensor5;
ELSE
    targetSensor := FALSE;
END_CASE;

conveyorLeft := FALSE;
conveyorRight := FALSE;
IF (phase = PHASE_MOVING) AND NOT targetSensor THEN
    IF target > currentStation THEN
        conveyorRight := TRUE;
    ELSIF target < currentStation THEN
        conveyorLeft := TRUE;
    END_IF;
END_IF;

prevStation1Start := station1Start;
prevStation2Complete := station2Complete;
prevStation3Complete := station3Complete;
prevStation4Complete := station4Complete;
END_FUNCTION_BLOCK
