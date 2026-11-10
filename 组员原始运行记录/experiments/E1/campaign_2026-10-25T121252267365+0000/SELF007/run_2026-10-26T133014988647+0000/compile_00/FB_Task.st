FUNCTION_BLOCK FB_Task
VAR_INPUT
    Demand : BOOL;
    FaultA : BOOL;
    FaultB : BOOL;
END_VAR
VAR_OUTPUT
    PumpA : BOOL;
    PumpB : BOOL;
    LeadA : BOOL := TRUE;
END_VAR
VAR
    prevDemand : BOOL := FALSE;
    episodeServed : BOOL := FALSE;
    runA : BOOL;
    runB : BOOL;
    completedServed : BOOL;
END_VAR

runA := Demand AND NOT FaultA AND (LeadA OR FaultB);
runB := Demand AND NOT FaultB AND ((NOT LeadA) OR FaultA);

PumpA := runA;
PumpB := runB;

completedServed := prevDemand AND NOT Demand AND episodeServed;

IF completedServed THEN
    LeadA := NOT LeadA;
END_IF

IF Demand THEN
    IF runA OR runB THEN
        episodeServed := TRUE;
    END_IF
ELSE
    episodeServed := FALSE;
END_IF

prevDemand := Demand;
END_FUNCTION_BLOCK
