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
    wasProtected : BOOL;
    heatTimer : TON;
    cooldownTimer : TON;
END_VAR

CurrentTemperature := TemperatureSensorInput;
SetTempDisplay := SetTemperature;

sensorFault := (TemperatureSensorInput < 0.0) OR (TemperatureSensorInput > 100.0);

IF TemperatureSensorInput < SetTemperature THEN
    heatDemand := TRUE;
ELSIF TemperatureSensorInput > SetTemperature THEN
    heatDemand := FALSE;
END_IF;

wasProtected := OverheatProtection;

IF wasProtected THEN
    cooldownTimer(IN := TRUE, PT := T#3S);
    IF cooldownTimer.Q THEN
        OverheatProtection := FALSE;
    END_IF;
ELSE
    cooldownTimer(IN := FALSE, PT := T#3S);
END_IF;

heatTimer(IN := heatDemand AND NOT sensorFault AND NOT OverheatProtection,
          PT := T#5S);

IF heatTimer.Q THEN
    OverheatProtection := TRUE;
END_IF;

IF OverheatProtection AND NOT wasProtected THEN
    cooldownTimer(IN := TRUE, PT := T#3S);
END_IF;

HeaterOutput := heatDemand AND NOT sensorFault AND NOT OverheatProtection;
HeaterStatus := HeaterOutput;
END_FUNCTION_BLOCK
