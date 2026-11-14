FUNCTION_BLOCK FB_Task
VAR_INPUT
    enqueue : BOOL;
    dequeue : BOOL;
    reset : BOOL;
END_VAR
VAR_OUTPUT
    elementCount : DINT := 0;
    status : WORD := 16#0000;
END_VAR
VAR_IN_OUT
    item : VARIANT;
    buffer : VARIANT;
END_VAR

(* No conforming repair is available with this target's reported types. VARIANT is unknown, and defining it as a DUT would not allow direct VAR_IN_OUT bindings to both scalar values and arrays. This declaration remains non-compiling. A compatible generic-reference facility must be supplied, or an interface change must be approved. *)
END_FUNCTION_BLOCK
