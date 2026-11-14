TYPE E_Mode :
(
    EM_IDLE := 0,
    EM_RUNNING := 1,
    EM_WAIT := 2,
    EM_LOCKED := 3
);
END_TYPE

FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    Fault : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Run : BOOL := FALSE;
    Locked : BOOL := FALSE;
    Attempts : USINT := 0;
END_VAR
VAR
    mode : E_Mode := E_Mode.EM_IDLE;
    free_scans : USINT := 0;
    attempt_count : USINT := 0;
    validReset : BOOL;
    bStart : BOOL;
    bStop : BOOL;
    bFault : BOOL;
    bReset : BOOL;
END_VAR

// Stage 1: sample inputs once and derive valid reset
bStart := Start;
bStop := Stop;
bFault := Fault;
bReset := Reset;
validReset := bReset AND NOT bFault AND NOT bStart;

// Stage 2: priority transition using retained pre-state q[k]
IF validReset THEN
    mode := E_Mode.EM_IDLE;
    attempt_count := 0;
    free_scans := 0;
ELSIF mode = E_Mode.EM_LOCKED THEN
    // Latched lockout: remain LOCKED absent valid reset
    mode := E_Mode.EM_LOCKED;
    free_scans := 0;
    // attempt_count preserved
ELSIF bStop THEN
    // Abort to IDLE without clearing retry count
    mode := E_Mode.EM_IDLE;
    free_scans := 0;
    // attempt_count preserved
ELSE
    CASE mode OF
        E_Mode.EM_IDLE:
            IF bStart AND NOT bFault THEN
                mode := E_Mode.EM_RUNNING;
                free_scans := 0;
                // attempt_count preserved
            ELSE
                mode := E_Mode.EM_IDLE;
                free_scans := 0;
                // attempt_count preserved
            END_IF;

        E_Mode.EM_RUNNING:
            IF bFault THEN
                IF attempt_count >= 2 THEN
                    mode := E_Mode.EM_LOCKED;
                    free_scans := 0;
                    // attempt_count preserved
                ELSE
                    mode := E_Mode.EM_WAIT;
                    free_scans := 0;
                    // attempt_count preserved
                END_IF;
            ELSE
                mode := E_Mode.EM_RUNNING;
                free_scans := 0;
                // attempt_count preserved
            END_IF;

        E_Mode.EM_WAIT:
            IF bFault THEN
                mode := E_Mode.EM_WAIT;
                free_scans := 0;
                // attempt_count preserved
            ELSIF free_scans >= 1 THEN
                // Second consecutive fault-free dwell scan: issue one retry
                IF attempt_count < 2 THEN
                    attempt_count := attempt_count + 1;
                END_IF;
                free_scans := 0;
                mode := E_Mode.EM_RUNNING;
            ELSE
                // First fault-free dwell scan
                free_scans := free_scans + 1;
                mode := E_Mode.EM_WAIT;
                // attempt_count preserved
            END_IF;

        E_Mode.EM_LOCKED:
            // Defensive latch branch; normally handled before CASE
            mode := E_Mode.EM_LOCKED;
            free_scans := 0;
            // attempt_count preserved

        ELSE
            mode := E_Mode.EM_IDLE;
            free_scans := 0;
            // attempt_count preserved
    END_CASE;
END_IF;

// Stage 3: no timer FB calls for SELF012; recovery dwell is scan-count based

// Stage 4: unified output assignments from post-transition state
Run := (mode = E_Mode.EM_RUNNING);
Locked := (mode = E_Mode.EM_LOCKED);
Attempts := attempt_count;
END_FUNCTION_BLOCK
