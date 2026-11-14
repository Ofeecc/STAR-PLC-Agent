{attribute 'qualified_only'}
{attribute 'strict'}
TYPE E_TaskMode :
(
    IDLE := 0,
    RUNNING := 1,
    WAIT := 2,
    LOCKED := 3
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
    mode : E_TaskMode := E_TaskMode.IDLE;
    attempt_count : USINT := 0;
    free_scans : USINT := 0;
    sampledStart : BOOL;
    sampledStop : BOOL;
    sampledFault : BOOL;
    sampledReset : BOOL;
END_VAR

sampledStart := Start;
sampledStop := Stop;
sampledFault := Fault;
sampledReset := Reset;

IF sampledReset AND NOT sampledFault AND NOT sampledStart THEN
    mode := E_TaskMode.IDLE;
    attempt_count := 0;
    free_scans := 0;
ELSIF mode <> E_TaskMode.LOCKED THEN
    IF sampledStop THEN
        mode := E_TaskMode.IDLE;
        free_scans := 0;
    ELSE
        CASE mode OF
            E_TaskMode.IDLE:
                IF sampledStart AND NOT sampledFault THEN
                    mode := E_TaskMode.RUNNING;
                END_IF;

            E_TaskMode.RUNNING:
                IF sampledFault THEN
                    IF attempt_count >= 2 THEN
                        mode := E_TaskMode.LOCKED;
                    ELSE
                        mode := E_TaskMode.WAIT;
                        free_scans := 0;
                    END_IF;
                END_IF;

            E_TaskMode.WAIT:
                IF sampledFault THEN
                    free_scans := 0;
                ELSE
                    free_scans := free_scans + 1;
                    IF free_scans >= 2 THEN
                        attempt_count := attempt_count + 1;
                        free_scans := 0;
                        mode := E_TaskMode.RUNNING;
                    END_IF;
                END_IF;
        END_CASE;
    END_IF;
END_IF;

Run := (mode = E_TaskMode.RUNNING);
Locked := (mode = E_TaskMode.LOCKED);
Attempts := attempt_count;
END_FUNCTION_BLOCK
