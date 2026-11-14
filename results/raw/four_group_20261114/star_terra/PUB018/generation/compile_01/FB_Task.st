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

(* Cannot implement or compile the required interface in this project: the compiler reports VARIANT as an unknown type, and __SYSTEM.VAR_INFO has no ByteSize member. Defining a concrete DUT named VARIANT would not permit the required direct DINT, BOOL, and array bindings. A supported generic-reference and metadata facility, or an interface change, is required. *)
END_FUNCTION_BLOCK
