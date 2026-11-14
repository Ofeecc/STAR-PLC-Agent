FUNCTION F_TaskElapsedMs : UDINT
VAR_INPUT
    nowValue : UDINT;
    startValue : UDINT;
END_VAR

IF nowValue >= startValue THEN
    F_TaskElapsedMs := nowValue - startValue;
ELSE
    F_TaskElapsedMs := (UDINT#16#FFFFFFFF - startValue) + nowValue + UDINT#1;
END_IF;
END_FUNCTION

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
    state : INT := 0; (* 0: idle, 1: heating, 2: protected *)
    heatDemand : BOOL := FALSE;
    sensorFault : BOOL := FALSE;
    sampledTemperature : REAL;
    sampledSetTemperature : REAL;
    now_ms : UDINT := 0;
    heatStart_ms : UDINT := 0;
    protectionStart_ms : UDINT := 0;
    heatElapsed_ms : UDINT := 0;
    cooldownElapsed_ms : UDINT := 0;
    elapsed_ms : UDINT := 0;
    HeatTON : TON;
    CooldownTON : TON;
END_VAR

sampledTemperature := TemperatureSensorInput;
sampledSetTemperature := SetTemperature;
(* TIME() is the CODESYS millisecond system clock. Elapsed-time arithmetic
   handles one clock wrap; the task must execute at least once per wrap. *)
now_ms := TIME_TO_UDINT(TIME());

sensorFault := (sampledTemperature < 0.0) OR (sampledTemperature > 100.0);
IF NOT sensorFault THEN
    IF sampledTemperature < sampledSetTemperature THEN
        heatDemand := TRUE;
    ELSIF sampledTemperature > sampledSetTemperature THEN
        heatDemand := FALSE;
    END_IF;
END_IF;

CASE state OF
    0:
        heatElapsed_ms := 0;
        cooldownElapsed_ms := 0;
        IF NOT sensorFault AND heatDemand THEN
            heatStart_ms := now_ms;
            state := 1;
        END_IF;

    1:
        elapsed_ms := F_TaskElapsedMs(nowValue := now_ms, startValue := heatStart_ms);
        IF elapsed_ms >= 5000 THEN
            heatElapsed_ms := 0;
            cooldownElapsed_ms := 0;
            protectionStart_ms := now_ms;
            state := 2;
        ELSIF sensorFault OR NOT heatDemand THEN
            heatElapsed_ms := 0;
            state := 0;
        ELSE
            heatElapsed_ms := elapsed_ms;
        END_IF;

    2:
        heatElapsed_ms := 0;
        elapsed_ms := F_TaskElapsedMs(nowValue := now_ms, startValue := protectionStart_ms);
        IF elapsed_ms >= 3000 THEN
            cooldownElapsed_ms := 0;
            IF NOT sensorFault AND heatDemand THEN
                heatStart_ms := now_ms;
                state := 1;
            ELSE
                state := 0;
            END_IF;
        ELSE
            cooldownElapsed_ms := elapsed_ms;
        END_IF;

    ELSE
        state := 0;
        heatElapsed_ms := 0;
        cooldownElapsed_ms := 0;
END_CASE;

HeatTON(IN := (state = 1), PT := T#5s);
CooldownTON(IN := (state = 2), PT := T#3s);

CurrentTemperature := sampledTemperature;
SetTempDisplay := sampledSetTemperature;
OverheatProtection := (state = 2);
HeaterOutput := (state = 1);
HeaterStatus := HeaterOutput;
END_FUNCTION_BLOCK
