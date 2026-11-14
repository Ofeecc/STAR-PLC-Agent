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
    clockInitialized : BOOL := FALSE;
    clockOriginUs : ULINT := 0;
    rawClockUs : ULINT := 0;
    nowUs : ULINT := 0;
    heatStartUs : ULINT := 0;
    protectionStartUs : ULINT := 0;
    elapsedUs : ULINT := 0;
    heatElapsed_ms : UDINT := 0;
    cooldownElapsed_ms : UDINT := 0;
    HeatTON : TON;
    CooldownTON : TON;
END_VAR

(* SysTimeGetUs requires the CODESYS SysTimeCore library. *)
sampledTemperature := TemperatureSensorInput;
sampledSetTemperature := SetTemperature;
rawClockUs := SysTimeGetUs();
IF NOT clockInitialized THEN
    clockOriginUs := rawClockUs;
    clockInitialized := TRUE;
END_IF;
nowUs := F_TaskElapsedUs(nowValue := rawClockUs, startValue := clockOriginUs);

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
            heatStartUs := nowUs;
            state := 1;
        END_IF;

    1:
        elapsedUs := F_TaskElapsedUs(nowValue := nowUs, startValue := heatStartUs);
        IF elapsedUs >= ULINT#5000000 THEN
            heatElapsed_ms := 0;
            cooldownElapsed_ms := 0;
            protectionStartUs := nowUs;
            state := 2;
        ELSIF sensorFault OR NOT heatDemand THEN
            heatElapsed_ms := 0;
            state := 0;
        ELSE
            heatElapsed_ms := ULINT_TO_UDINT(elapsedUs / ULINT#1000);
        END_IF;

    2:
        heatElapsed_ms := 0;
        elapsedUs := F_TaskElapsedUs(nowValue := nowUs, startValue := protectionStartUs);
        IF elapsedUs >= ULINT#3000000 THEN
            cooldownElapsed_ms := 0;
            IF NOT sensorFault AND heatDemand THEN
                heatStartUs := nowUs;
                state := 1;
            ELSE
                state := 0;
            END_IF;
        ELSE
            cooldownElapsed_ms := ULINT_TO_UDINT(elapsedUs / ULINT#1000);
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
