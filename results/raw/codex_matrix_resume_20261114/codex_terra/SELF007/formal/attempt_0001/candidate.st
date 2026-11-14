FUNCTION_BLOCK FB_Task
VAR_INPUT
    Demand : BOOL;
    FaultA : BOOL;
    FaultB : BOOL;
END_VAR
VAR_OUTPUT
    PumpA : BOOL := FALSE;
    PumpB : BOOL := FALSE;
    LeadA : BOOL := TRUE;
END_VAR
VAR
    previous_demand : BOOL := FALSE;
    episode_served : BOOL := FALSE;
END_VAR

IF NOT Demand THEN
    PumpA := FALSE;
    PumpB := FALSE;
    IF previous_demand AND episode_served THEN
        LeadA := NOT LeadA;
    END_IF;
    episode_served := FALSE;
ELSE
    PumpA := NOT FaultA AND (LeadA OR FaultB);
    PumpB := NOT FaultB AND (NOT LeadA OR FaultA);
    IF PumpA OR PumpB THEN
        episode_served := TRUE;
    END_IF;
END_IF;
previous_demand := Demand;
END_FUNCTION_BLOCK
