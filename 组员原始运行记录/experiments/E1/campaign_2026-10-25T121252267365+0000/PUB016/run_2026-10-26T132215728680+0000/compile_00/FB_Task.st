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
    phase : E_Phase := E_Phase.IDLE;
    currentStation : USINT := 1;
    sequenceIndex : USINT := 1;
    targetStation : USINT := 1;
    prevStart : BOOL;
    prevComp2 : BOOL;
    prevComp3 : BOOL;
    prevComp4 : BOOL;
    startEdge : BOOL;
    comp2Edge : BOOL;
    comp3Edge : BOOL;
    comp4Edge : BOOL;
    completion : BOOL;
    sensorAtTarget : BOOL;
END_VAR

(* ---------- fresh rising-edge detection ---------- *)
startEdge := station1Start AND NOT prevStart;
prevStart := station1Start;

comp2Edge := station2Complete AND NOT prevComp2;
prevComp2 := station2Complete;

comp3Edge := station3Complete AND NOT prevComp3;
prevComp3 := station3Complete;

comp4Edge := station4Complete AND NOT prevComp4;
prevComp4 := station4Complete;

(* ---------- sensor of the currently targeted station ---------- *)
sensorAtTarget := FALSE;
CASE targetStation OF
    1: sensorAtTarget := sensor1;
    2: sensorAtTarget := sensor2;
    3: sensorAtTarget := sensor3;
    4: sensorAtTarget := sensor4;
    5: sensorAtTarget := sensor5;
END_CASE

(* ---------- main state machine ---------- *)
CASE phase OF

E_Phase.IDLE:
    conveyorLeft := FALSE;
    conveyorRight := FALSE;
    IF sensor1 AND startEdge THEN
        sequenceIndex := 1;
        currentStation := 1;
        targetStation := processSequence[1];
        IF targetStation = currentStation THEN
            phase := E_Phase.WAIT_PROCESS;
        ELSE
            phase := E_Phase.MOVING;
            IF targetStation > currentStation THEN
                conveyorRight := TRUE;
                conveyorLeft := FALSE;
            ELSE
                conveyorLeft := TRUE;
                conveyorRight := FALSE;
            END_IF
        END_IF
    END_IF

E_Phase.MOVING:
    IF sensorAtTarget THEN
        (* destination reached: stop immediately *)
        currentStation := targetStation;
        conveyorLeft := FALSE;
        conveyorRight := FALSE;
        IF targetStation = 5 THEN
            phase := E_Phase.IDLE;
        ELSE
            phase := E_Phase.WAIT_PROCESS;
        END_IF
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
        END_IF
    END_IF

E_Phase.WAIT_PROCESS:
    conveyorLeft := FALSE;
    conveyorRight := FALSE;
    completion := FALSE;
    CASE currentStation OF
        2: completion := comp2Edge;
        3: completion := comp3Edge;
        4: completion := comp4Edge;
    END_CASE
    IF completion THEN
        IF sequenceIndex >= processLength THEN
            phase := E_Phase.IDLE;
        ELSE
            sequenceIndex := sequenceIndex + 1;
            targetStation := processSequence[sequenceIndex];
            IF targetStation = currentStation THEN
                (* repeated station: separate operation, no movement *)
                phase := E_Phase.WAIT_PROCESS;
            ELSE
                phase := E_Phase.MOVING;
                IF targetStation > currentStation THEN
                    conveyorRight := TRUE;
                    conveyorLeft := FALSE;
                ELSE
                    conveyorLeft := TRUE;
                    conveyorRight := FALSE;
                END_IF
            END_IF
        END_IF
    END_IF

ELSE
    conveyorLeft := FALSE;
    conveyorRight := FALSE;
    phase := E_Phase.IDLE;
END_CASE
END_FUNCTION_BLOCK
