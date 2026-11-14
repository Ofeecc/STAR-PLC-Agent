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
    FAN_START_DELAY : TON;
    occupancy_sample : BOOL;
    energy_saving_sample : BOOL;
    mode_sample : INT;
    permit : BOOL;
    previous_permit : BOOL := FALSE;
    permit_rising : BOOL;
    permit_falling : BOOL;
    state : INT := 0; (* 0: blocked, 1: permitted *)
    adjustment : INT;
END_VAR

occupancy_sample := OCCUPANCY_DETECTED;
energy_saving_sample := ENERGY_SAVING_MODE;
mode_sample := HVAC_MODE_SELECTOR;

permit := occupancy_sample AND (mode_sample <> 3);
permit_rising := permit AND NOT previous_permit;
permit_falling := NOT permit AND previous_permit;
previous_permit := permit;

IF permit THEN
    state := 1;
ELSE
    state := 0;
END_IF;

FAN_START_DELAY(IN := permit, PT := T#30s);
SUPPLY_FAN_RUN := permit AND FAN_START_DELAY.Q;

adjustment := 0;
IF mode_sample = 3 THEN
    adjustment := 4;
ELSIF occupancy_sample THEN
    adjustment := 0;
ELSE
    CASE mode_sample OF
        0:
            IF energy_saving_sample THEN
                adjustment := 3;
            ELSE
                adjustment := 2;
            END_IF;
        1:
            adjustment := 1;
        2:
            adjustment := 4;
    ELSE
        adjustment := 0;
    END_CASE;
END_IF;

IF adjustment > 4 THEN
    adjustment := 4;
ELSIF adjustment < -4 THEN
    adjustment := -4;
END_IF;
TEMP_SETPOINT_ADJUST := adjustment;
END_FUNCTION_BLOCK
