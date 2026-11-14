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
    lead_pref : BOOL := TRUE;
    previous_demand : BOOL := FALSE;
    episode_served : BOOL := FALSE;
    sampled_demand : BOOL := FALSE;
    sampled_fault_a : BOOL := FALSE;
    sampled_fault_b : BOOL := FALSE;
    falling_demand : BOOL := FALSE;
    candidate_a : BOOL := FALSE;
    candidate_b : BOOL := FALSE;
END_VAR

sampled_demand := Demand;
sampled_fault_a := FaultA;
sampled_fault_b := FaultB;

falling_demand := previous_demand AND NOT sampled_demand;
IF falling_demand AND episode_served THEN
    lead_pref := NOT lead_pref;
END_IF;

candidate_a := sampled_demand AND NOT sampled_fault_a AND (lead_pref OR sampled_fault_b);
candidate_b := sampled_demand AND NOT sampled_fault_b AND (NOT lead_pref OR sampled_fault_a);

IF sampled_demand THEN
    episode_served := episode_served OR candidate_a OR candidate_b;
ELSE
    episode_served := FALSE;
END_IF;
previous_demand := sampled_demand;

PumpA := candidate_a;
PumpB := candidate_b;
LeadA := lead_pref;
END_FUNCTION_BLOCK
