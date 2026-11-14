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
    // 0=IDLE, 1=MOVING, 2=WAIT_PROCESS, 3=DEFER, 4=FAULT
    phase : USINT := 0;
    currentStation : USINT := 1;
    sequenceIndex : USINT := 0;
    target : USINT := 1;
    snapshotLength : USINT := 0;
    snapshotSequence : ARRAY[1..8] OF USINT;
    previous_station1Start : BOOL := FALSE;
    previous_station2Complete : BOOL := FALSE;
    previous_station3Complete : BOOL := FALSE;
    previous_station4Complete : BOOL := FALSE;
    startEdge : BOOL;
    completionEdges : ARRAY[1..5] OF BOOL;
    arrivalSensors : ARRAY[1..5] OF BOOL;
    recipeValid : BOOL;
    internalValid : BOOL;
    selectTarget : BOOL;
    i : USINT;
END_VAR

// Sample edges globally, including while their corresponding events are ignored.
startEdge := station1Start AND NOT previous_station1Start;
completionEdges[1] := FALSE;
completionEdges[2] := station2Complete AND NOT previous_station2Complete;
completionEdges[3] := station3Complete AND NOT previous_station3Complete;
completionEdges[4] := station4Complete AND NOT previous_station4Complete;
completionEdges[5] := FALSE;
previous_station1Start := station1Start;
previous_station2Complete := station2Complete;
previous_station3Complete := station3Complete;
previous_station4Complete := station4Complete;

arrivalSensors[1] := sensor1;
arrivalSensors[2] := sensor2;
arrivalSensors[3] := sensor3;
arrivalSensors[4] := sensor4;
arrivalSensors[5] := sensor5;
selectTarget := FALSE;

// Check retained state before using a retained value as an array index.
IF (phase = 1) OR (phase = 2) OR (phase = 3) THEN
    internalValid := TRUE;
    IF (snapshotLength < 1) OR (snapshotLength > 8) THEN
        internalValid := FALSE;
    END_IF;
    IF (sequenceIndex < 1) OR (sequenceIndex > snapshotLength) OR (sequenceIndex > 8) THEN
        internalValid := FALSE;
    END_IF;
    IF (target < 2) OR (target > 5) THEN
        internalValid := FALSE;
    END_IF;
    IF internalValid THEN
        IF target <> snapshotSequence[sequenceIndex] THEN
            internalValid := FALSE;
        END_IF;
    END_IF;
    IF phase = 1 THEN
        IF (currentStation < 1) OR (currentStation > 4) OR (target = currentStation) THEN
            internalValid := FALSE;
        END_IF;
    ELSE
        IF (currentStation < 2) OR (currentStation > 4) OR (target <> currentStation) THEN
            internalValid := FALSE;
        END_IF;
    END_IF;
    IF NOT internalValid THEN
        phase := 4;
    END_IF;
END_IF;

CASE phase OF
    0: // IDLE
        IF startEdge AND sensor1 THEN
            recipeValid := TRUE;
            IF (processLength < 1) OR (processLength > 8) THEN
                recipeValid := FALSE;
            ELSE
                IF processSequence[processLength] <> 5 THEN
                    recipeValid := FALSE;
                END_IF;
                FOR i := 1 TO 8 DO
                    IF i < processLength THEN
                        IF (processSequence[i] < 2) OR (processSequence[i] > 4) THEN
                            recipeValid := FALSE;
                        END_IF;
                    END_IF;
                END_FOR;
            END_IF;
            IF recipeValid THEN
                snapshotLength := processLength;
                FOR i := 1 TO 8 DO
                    IF i <= processLength THEN
                        snapshotSequence[i] := processSequence[i];
                    ELSE
                        snapshotSequence[i] := 0;
                    END_IF;
                END_FOR;
                currentStation := 1;
                sequenceIndex := 1;
                selectTarget := TRUE;
            ELSE
                phase := 4;
            END_IF;
        END_IF;

    1: // MOVING: arrival has priority over further motion.
        IF arrivalSensors[target] THEN
            currentStation := target;
            IF target = 5 THEN
                phase := 0;
            ELSE
                phase := 2;
                IF completionEdges[currentStation] THEN
                    phase := 3;
                END_IF;
            END_IF;
        END_IF;

    2: // WAIT_PROCESS
        IF completionEdges[currentStation] THEN
            IF sequenceIndex < snapshotLength THEN
                sequenceIndex := sequenceIndex + 1;
                selectTarget := TRUE;
            ELSE
                phase := 4;
            END_IF;
        END_IF;

    3: // DEFER: advance an arrival-scan completion on this invocation.
        IF sequenceIndex < snapshotLength THEN
            sequenceIndex := sequenceIndex + 1;
            selectTarget := TRUE;
        ELSE
            phase := 4;
        END_IF;

    4: // FAULT: reinitialization is required.
        ;

    ELSE
        phase := 4;
END_CASE;

// Selection is performed at most once per invocation.
IF selectTarget THEN
    IF (sequenceIndex < 1) OR (sequenceIndex > snapshotLength) OR (sequenceIndex > 8) THEN
        phase := 4;
    ELSE
        target := snapshotSequence[sequenceIndex];
        IF (target < 2) OR (target > 5) THEN
            phase := 4;
        ELSIF target = currentStation THEN
            // A repeated station is a new operation; do not reuse an edge.
            IF target = 5 THEN
                phase := 4;
            ELSE
                phase := 2;
            END_IF;
        ELSE
            phase := 1;
            IF arrivalSensors[target] THEN
                currentStation := target;
                IF target = 5 THEN
                    phase := 0;
                ELSE
                    phase := 2;
                    IF completionEdges[currentStation] THEN
                        phase := 3;
                    END_IF;
                END_IF;
            END_IF;
        END_IF;
    END_IF;
END_IF;

// Unified output assignment provides the direction interlock.
conveyorLeft := FALSE;
conveyorRight := FALSE;
IF phase = 1 THEN
    IF (target >= 2) AND (target <= 5) THEN
        IF NOT arrivalSensors[target] THEN
            IF target > currentStation THEN
                conveyorRight := TRUE;
            ELSIF target < currentStation THEN
                conveyorLeft := TRUE;
            END_IF;
        END_IF;
    END_IF;
END_IF;
END_FUNCTION_BLOCK
