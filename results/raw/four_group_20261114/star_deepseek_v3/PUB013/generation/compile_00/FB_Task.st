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
    tonOccupancyDelay : TON;
    permit : BOOL := FALSE;
    state : INT := 0;
END_VAR

// Stage 1: sample inputs and compute permit
permit := OCCUPANCY_DETECTED AND (HVAC_MODE_SELECTOR <> 3);

// Stage 2: unconditional top-level TON call
// The timer is called every scan and resets immediately when permit is FALSE.
tonOccupancyDelay(IN := permit, PT := T#30S);

// Stage 3: state tracking for the fan-delay state machine
IF NOT permit THEN
    state := 0; // S0_RESET_OFF
ELSIF tonOccupancyDelay.Q THEN
    state := 2; // S2_FAN_ON
ELSE
    state := 1; // S1_DELAY_RUNNING
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

// Fan enable: immediate OFF on permit loss; same-scan ON at timer maturity
SUPPLY_FAN_RUN := (state <> 0) AND permit AND tonOccupancyDelay.Q;
END_FUNCTION_BLOCK
