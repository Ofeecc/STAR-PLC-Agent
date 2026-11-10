FUNCTION_BLOCK FB_Task
VAR_INPUT
    TemperatureSensorInput : REAL;
    SetTemperature : REAL;
END_VAR
VAR_OUTPUT
    CurrentTemperature : REAL;
    SetTempDisplay : REAL;
    HeaterStatus : BOOL;
    OverheatProtection : BOOL;
    HeaterOutput : BOOL;
END_VAR
VAR
    heatDemand : BOOL;
    sensorFault : BOOL;
    heatElapsed : TIME;
    cooldownElapsed : TIME;
    lastScanTime : TIME;
    currentTime : TIME;
    deltaTime : TIME;
    timeInitialized : BOOL;
END_VAR

CurrentTemperature := TemperatureSensorInput;
SetTempDisplay := SetTemperature;

currentTime := TIME();
IF timeInitialized THEN
    deltaTime := currentTime - lastScanTime;
ELSE
    deltaTime := T#0MS;
    timeInitialized := TRUE;
END_IF;
lastScanTime := currentTime;

sensorFault := (TemperatureSensorInput < 0.0) OR (TemperatureSensorInput > 100.0);

IF TemperatureSensorInput < SetTemperature THEN
    heatDemand := TRUE;
ELSIF TemperatureSensorInput > SetTemperature THEN
    heatDemand := FALSE;
END_IF;

IF OverheatProtection THEN
    cooldownElapsed := cooldownElapsed + deltaTime;
    IF cooldownElapsed >= T#3S THEN
        OverheatProtection := FALSE;
        cooldownElapsed := T#0MS;
    END_IF;
ELSE
    cooldownElapsed := T#0MS;
END_IF;

IF HeaterOutput AND heatDemand AND NOT sensorFault AND NOT OverheatProtection THEN
    heatElapsed := heatElapsed + deltaTime;
ELSE
    heatElapsed := T#0MS;
END_IF;

IF heatElapsed >= T#5S THEN
    OverheatProtection := TRUE;
    cooldownElapsed := T#0MS;
    heatElapsed := T#0MS;
END_IF;

HeaterOutput := heatDemand AND NOT sensorFault AND NOT OverheatProtection;
HeaterStatus := HeaterOutput;
END_FUNCTION_BLOCK
