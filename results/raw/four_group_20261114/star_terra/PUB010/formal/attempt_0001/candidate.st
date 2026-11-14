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
    heatElapsed_ms : UDINT := 0;
    cooldownElapsed_ms : UDINT := 0;
    delta_ms : UDINT := 0;
    clockInitialized : BOOL := FALSE;
    clockRun : BOOL := FALSE;
    previousClockValid : BOOL := FALSE;
    clock_ms : UDINT := 0;
    previousClock_ms : UDINT := 0;
    runtime_ms : UDINT := 0;
    previousRuntime_ms : UDINT := 0;
    ClockTON : TON;
    HeatTON : TON;
    CooldownTON : TON;
END_VAR

sampledTemperature := TemperatureSensorInput;
sampledSetTemperature := SetTemperature;
runtime_ms := TIME_TO_UDINT(TIME());

(* Use the elapsed time of a continuously running timer as the scan clock.
   The runtime clock bridges its reset when the long timer expires. *)
clockRun := NOT ClockTON.Q;
ClockTON(IN := clockRun, PT := T#24d);
clock_ms := TIME_TO_UDINT(ClockTON.ET);

delta_ms := 0;
IF clockInitialized THEN
    IF clockRun AND NOT ClockTON.Q AND previousClockValid AND
       (clock_ms >= previousClock_ms) THEN
        delta_ms := clock_ms - previousClock_ms;
    ELSIF runtime_ms >= previousRuntime_ms THEN
        delta_ms := runtime_ms - previousRuntime_ms;
    ELSE
        delta_ms := (UDINT#16#FFFFFFFF - previousRuntime_ms) + runtime_ms + UDINT#1;
    END_IF;
END_IF;
clockInitialized := TRUE;
previousClock_ms := clock_ms;
previousRuntime_ms := runtime_ms;
previousClockValid := clockRun AND NOT ClockTON.Q;

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
            state := 1;
        END_IF;

    1:
        (* Account for the preceding energized interval before applying
           a fault or demand change sampled on this scan. *)
        IF delta_ms >= (UDINT#5000 - heatElapsed_ms) THEN
            heatElapsed_ms := 0;
            cooldownElapsed_ms := 0;
            state := 2;
        ELSIF sensorFault OR NOT heatDemand THEN
            heatElapsed_ms := 0;
            state := 0;
        ELSE
            heatElapsed_ms := heatElapsed_ms + delta_ms;
        END_IF;

    2:
        heatElapsed_ms := 0;
        IF delta_ms >= (UDINT#3000 - cooldownElapsed_ms) THEN
            cooldownElapsed_ms := 0;
            IF NOT sensorFault AND heatDemand THEN
                state := 1;
            ELSE
                state := 0;
            END_IF;
        ELSE
            cooldownElapsed_ms := cooldownElapsed_ms + delta_ms;
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
