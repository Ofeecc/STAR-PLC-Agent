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
    wasProtected : BOOL;
    heatTimer : TON;
    cooldownTimer : TON;
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

wasHeating := HeaterOutput;
wasProtected := OverheatProtection;

heatTimer(IN := wasHeating AND NOT sensorFault, PT := T#5S);
heatLimitReached := heatTimer.Q AND NOT sensorFault;

IF wasProtected THEN
    cooldownTimer(IN := TRUE, PT := T#3S);
    IF cooldownTimer.Q THEN
        OverheatProtection := FALSE;
    END_IF;
ELSE
    cooldownTimer(IN := FALSE, PT := T#3S);
END_IF;

IF NOT OverheatProtection AND heatLimitReached THEN
    OverheatProtection := TRUE;
END_IF;

IF sensorFault OR OverheatProtection THEN
    HeaterOutput := FALSE;
ELSIF demand THEN
    HeaterOutput := TRUE;
ELSE
    HeaterOutput := FALSE;
END_IF;
HeaterStatus := HeaterOutput;

IF HeaterOutput AND NOT wasHeating THEN
    heatTimer(IN := TRUE, PT := T#5S);
ELSIF (NOT HeaterOutput) AND wasHeating THEN
    heatTimer(IN := FALSE, PT := T#5S);
END_IF;

IF OverheatProtection AND NOT wasProtected THEN
    cooldownTimer(IN := TRUE, PT := T#3S);
ELSIF (NOT OverheatProtection) AND wasProtected THEN
    cooldownTimer(IN := FALSE, PT := T#3S);
END_IF;
END_FUNCTION_BLOCK
