FUNCTION_BLOCK FB_Task
VAR_INPUT
    OCCUPANCY_DETECTED : BOOL;
    ENERGY_SAVING_MODE : BOOL;
    HVAC_MODE_SELECTOR : INT;
END_VAR
VAR_OUTPUT
    SUPPLY_FAN_RUN : BOOL := FALSE;
    TEMP_SETPOINT_ADJUST : INT := 0;
END_VAR
VAR
    freeRunTimer : TON;
    startTime : TIME;
    elapsed : TIME;
    timing : BOOL := FALSE;
    state : INT := 0;
    permit : BOOL := FALSE;
END_VAR

// Stage 1: sample inputs and compute permit
permit := OCCUPANCY_DETECTED AND (HVAC_MODE_SELECTOR <> 3);

// Stage 2: free-running timer for elapsed time measurement
// Use a TON as a monotonic time source. IN is always TRUE and PT is large.
freeRunTimer(IN := TRUE, PT := T#24H);

// Stage 3: timing logic and state machine
IF NOT permit THEN
    timing := FALSE;
    elapsed := T#0S;
    state := 0; // S0_RESET_OFF
ELSIF NOT timing THEN
    timing := TRUE;
    startTime := freeRunTimer.ET;
    elapsed := T#0S;
    state := 1; // S1_DELAY_RUNNING
ELSE
    elapsed := freeRunTimer.ET - startTime;
    IF elapsed >= T#30S THEN
        state := 2; // S2_FAN_ON
    ELSE
        state := 1; // S1_DELAY_RUNNING
    END_IF;
END_IF;

// Stage 4: unified output assignments
CASE HVAC_MODE_SELECTOR OF
    3:
        TEMP_SETPOINT_ADJUST := 4;
    0:
        IF OCCUPANCY_DETECTED THEN
            TEMP_SETPOINT_ADJUST := 0;
        ELSIF ENERGY_SAVING_MODE THEN
            TEMP_SETPOINT_ADJUST := 3;
        ELSE
            TEMP_SETPOINT_ADJUST := 2;
        END_IF;
    1:
        IF OCCUPANCY_DETECTED THEN
            TEMP_SETPOINT_ADJUST := 0;
        ELSE
            TEMP_SETPOINT_ADJUST := 1;
        END_IF;
    2:
        IF OCCUPANCY_DETECTED THEN
            TEMP_SETPOINT_ADJUST := 0;
        ELSE
            TEMP_SETPOINT_ADJUST := 4;
        END_IF;
    ELSE
        TEMP_SETPOINT_ADJUST := 0;
END_CASE;

// Enforce the required adjustment bounds
IF TEMP_SETPOINT_ADJUST < -4 THEN
    TEMP_SETPOINT_ADJUST := -4;
ELSIF TEMP_SETPOINT_ADJUST > 4 THEN
    TEMP_SETPOINT_ADJUST := 4;
END_IF;

// Fan enable: true only after 30 s of continuous permit
SUPPLY_FAN_RUN := (state = 2);
END_FUNCTION_BLOCK
