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
    previous_demand : BOOL := FALSE;
    episode_served : BOOL := FALSE;
END_VAR

PumpA := FALSE;
PumpB := FALSE;

IF Demand THEN
    IF LeadA THEN
        IF NOT FaultA THEN
            PumpA := TRUE;
        ELSIF NOT FaultB THEN
            PumpB := TRUE;
        END_IF;
    ELSE
        IF NOT FaultB THEN
            PumpB := TRUE;
        ELSIF NOT FaultA THEN
            PumpA := TRUE;
        END_IF;
    END_IF;

    IF PumpA OR PumpB THEN
        episode_served := TRUE;
    END_IF;
END_IF;

IF previous_demand AND NOT Demand THEN
    IF episode_served THEN
        LeadA := NOT LeadA;
    END_IF;
    episode_served := FALSE;
END_IF;

previous_demand := Demand;
END_FUNCTION_BLOCK
