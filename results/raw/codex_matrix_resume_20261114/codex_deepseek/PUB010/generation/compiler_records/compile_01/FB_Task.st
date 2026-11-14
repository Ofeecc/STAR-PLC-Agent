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
    sensorFault : BOOL;
    demand : BOOL;
    heatLimitReached : BOOL;
    wasHeating : BOOL;
    currentTime : TIME;
    heatStartTime : TIME;
    protectionStartTime : TIME;
END_VAR

CurrentTemperature := TemperatureSensorInput;
SetTempDisplay := SetTemperature;
sensorFault := (TemperatureSensorInput < 0.0) OR (TemperatureSensorInput > 100.0);

IF NOT sensorFault THEN
    IF TemperatureSensorInput < SetTemperature THEN
        demand := TRUE;
    ELSIF TemperatureSensorInput > SetTemperature THEN
        demand := FALSE;
    END_IF;
END_IF;

currentTime := TIME();
wasHeating := HeaterOutput;

IF OverheatProtection AND ((currentTime - protectionStartTime) >= T#3S) THEN
    OverheatProtection := FALSE;
END_IF;

heatLimitReached := FALSE;
IF wasHeating AND NOT sensorFault THEN
    IF (currentTime - heatStartTime) >= T#5S THEN
        heatLimitReached := TRUE;
    END_IF;
END_IF;

IF heatLimitReached AND NOT OverheatProtection THEN
    OverheatProtection := TRUE;
    protectionStartTime := currentTime;
END_IF;

IF sensorFault OR OverheatProtection THEN
    HeaterOutput := FALSE;
ELSIF demand THEN
    HeaterOutput := TRUE;
ELSE
    HeaterOutput := FALSE;
END_IF;
HeaterStatus := HeaterOutput;

IF HeaterOutput THEN
    IF NOT wasHeating THEN
        heatStartTime := currentTime;
    END_IF;
ELSE
    heatStartTime := currentTime;
END_IF;
END_FUNCTION_BLOCK
