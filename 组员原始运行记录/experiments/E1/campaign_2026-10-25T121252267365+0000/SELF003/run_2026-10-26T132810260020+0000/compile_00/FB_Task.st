FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    EStopNC : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Run : BOOL := FALSE;
    ResetRequired : BOOL := TRUE;
END_VAR
VAR
END_VAR

IF NOT EStopNC THEN
    (* Emergency stop overrides everything *)
    Run := FALSE;
    ResetRequired := TRUE;
ELSIF ResetRequired THEN
    (* Restart inhibition active: motor can never run this scan, and a valid
       reset clears the latch without starting the motor. *)
    IF Reset AND NOT Start AND NOT Stop THEN
        ResetRequired := FALSE;
    END_IF
    Run := FALSE;
ELSE
    (* Normal operation after a successful reset *)
    IF Stop THEN
        Run := FALSE;
    ELSIF Start THEN
        Run := TRUE;
    END_IF
END_IF
END_FUNCTION_BLOCK
