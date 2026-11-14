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
    LeadA_State : BOOL := TRUE;
    previous_demand : BOOL := FALSE;
    served : BOOL := FALSE;
    PumpCmdA : BOOL := FALSE;
    PumpCmdB : BOOL := FALSE;
    scanDemand : BOOL := FALSE;
    scanFaultA : BOOL := FALSE;
    scanFaultB : BOOL := FALSE;
    fallingEdge : BOOL := FALSE;
END_VAR

scanDemand := Demand;
scanFaultA := FaultA;
scanFaultB := FaultB;
fallingEdge := previous_demand AND NOT scanDemand;

IF NOT scanDemand THEN
    PumpCmdA := FALSE;
    PumpCmdB := FALSE;
    IF fallingEdge AND served THEN
        LeadA_State := NOT LeadA_State;
    END_IF;
    served := FALSE;
ELSE
    IF LeadA_State THEN
        IF NOT scanFaultA THEN
            PumpCmdA := TRUE;
            PumpCmdB := FALSE;
        ELSIF NOT scanFaultB THEN
            PumpCmdA := FALSE;
            PumpCmdB := TRUE;
        ELSE
            PumpCmdA := FALSE;
            PumpCmdB := FALSE;
        END_IF;
    ELSE
        IF NOT scanFaultB THEN
            PumpCmdA := FALSE;
            PumpCmdB := TRUE;
        ELSIF NOT scanFaultA THEN
            PumpCmdA := TRUE;
            PumpCmdB := FALSE;
        ELSE
            PumpCmdA := FALSE;
            PumpCmdB := FALSE;
        END_IF;
    END_IF;
    IF PumpCmdA OR PumpCmdB THEN
        served := TRUE;
    END_IF;
END_IF;

previous_demand := scanDemand;

PumpA := PumpCmdA;
PumpB := PumpCmdB;
LeadA := LeadA_State;
END_FUNCTION_BLOCK
