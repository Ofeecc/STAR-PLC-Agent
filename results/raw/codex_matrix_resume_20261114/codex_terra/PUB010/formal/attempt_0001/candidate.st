FUNCTION_BLOCK FB_Task
VAR_INPUT
    TemperatureSensorInput : REAL;
    SetTemperature : REAL;
END_VAR
VAR_OUTPUT
    CurrentTemperature : REAL := 0.0;
    SetTempDisplay : REAL := 0.0;
    HeaterStatus : BOOL := FALSE;
    OverheatProtection : BOOL := FALSE;
    HeaterOutput : BOOL := FALSE;
END_VAR
VAR
    heatDemand : BOOL := FALSE;
    sensorFault : BOOL := FALSE;
    heatTimer : TON;
    cooldownTimer : TON;
END_VAR

CurrentTemperature := TemperatureSensorInput;
SetTempDisplay := SetTemperature;
sensorFault := (TemperatureSensorInput < 0.0) OR (TemperatureSensorInput > 100.0);
IF NOT sensorFault THEN
    IF TemperatureSensorInput < SetTemperature THEN
        heatDemand := TRUE;
    ELSIF TemperatureSensorInput > SetTemperature THEN
        heatDemand := FALSE;
    END_IF;
END_IF;

IF OverheatProtection THEN
    cooldownTimer(IN := TRUE, PT := T#3s);
    IF cooldownTimer.Q THEN
        OverheatProtection := FALSE;
    END_IF;
ELSE
    cooldownTimer(IN := FALSE, PT := T#3s);
END_IF;

heatTimer(IN := (NOT sensorFault) AND heatDemand AND (NOT OverheatProtection), PT := T#5s);
IF heatTimer.Q THEN
    OverheatProtection := TRUE;
    cooldownTimer(IN := TRUE, PT := T#3s);
END_IF;

HeaterOutput := (NOT sensorFault) AND heatDemand AND (NOT OverheatProtection);
HeaterStatus := HeaterOutput;
END_FUNCTION_BLOCK
