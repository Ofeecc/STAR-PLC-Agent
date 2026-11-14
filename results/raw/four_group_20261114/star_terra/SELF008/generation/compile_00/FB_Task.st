FUNCTION_BLOCK FB_Task
VAR_INPUT
    Request : BOOL;
    Trip : BOOL;
    Preset : USINT;
END_VAR
VAR_OUTPUT
    Ready : BOOL := FALSE;
    Count : USINT := 0;
END_VAR
VAR
    SampledRequest : BOOL;
    SampledTrip : BOOL;
    SampledPreset : USINT;
    NextCount : USINT := 0;
    NextReady : BOOL := FALSE;
END_VAR

SampledRequest := Request;
SampledTrip := Trip;
SampledPreset := Preset;

IF SampledTrip OR NOT SampledRequest OR (SampledPreset < USINT#1) OR (SampledPreset > USINT#5) THEN
    NextCount := 0;
    NextReady := FALSE;
ELSE
    IF Count >= SampledPreset THEN
        NextCount := SampledPreset;
    ELSE
        NextCount := Count + USINT#1;
    END_IF;
    NextReady := (NextCount >= SampledPreset);
END_IF;

Count := NextCount;
Ready := NextReady;
END_FUNCTION_BLOCK
