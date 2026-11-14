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
    HeatContinuityTimer : TON;
    CooldownTimer : TON;
    heatDemand : BOOL := FALSE;
    sensorFault : BOOL := FALSE;
    protectionLatched : BOOL := FALSE;
    heatLimitReached : BOOL := FALSE;
    cooldownDone : BOOL := FALSE;
    tripNow : BOOL := FALSE;
    heatEnable : BOOL := FALSE;
    protectionNext : BOOL := FALSE;
    heatCommand : BOOL := FALSE;
END_VAR

sensorFault := (TemperatureSensorInput < 0.0) OR (TemperatureSensorInput > 100.0);

IF NOT sensorFault THEN
    IF TemperatureSensorInput < SetTemperature THEN
        heatDemand := TRUE;
    ELSIF TemperatureSensorInput > SetTemperature THEN
        heatDemand := FALSE;
    END_IF;
END_IF;

CooldownTimer(IN := protectionLatched, PT := T#3S);
cooldownDone := CooldownTimer.Q;

IF protectionLatched AND cooldownDone THEN
    protectionLatched := FALSE;
END_IF;

heatEnable := (NOT sensorFault) AND heatDemand AND (NOT protectionLatched);

HeatContinuityTimer(IN := heatEnable, PT := T#5S);
heatLimitReached := HeatContinuityTimer.Q;
tripNow := heatLimitReached AND (NOT protectionLatched);

IF tripNow THEN
    protectionLatched := TRUE;
END_IF;

CooldownTimer(IN := (protectionLatched OR tripNow), PT := T#3S);

protectionNext := (protectionLatched AND (NOT cooldownDone)) OR tripNow;
heatCommand := (NOT sensorFault) AND heatDemand AND (NOT protectionNext) AND (NOT heatLimitReached);

CurrentTemperature := TemperatureSensorInput;
SetTempDisplay := SetTemperature;
OverheatProtection := protectionNext;
HeaterOutput := heatCommand;
HeaterStatus := HeaterOutput;
END_FUNCTION_BLOCK
