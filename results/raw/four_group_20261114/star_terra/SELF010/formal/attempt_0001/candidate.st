FUNCTION_BLOCK FB_Task
VAR_INPUT
    Fault : BOOL;
    Ack : BOOL;
    Reset : BOOL;
END_VAR
VAR_OUTPUT
    Alarm : BOOL := FALSE;
    Acknowledged : BOOL := FALSE;
    Horn : BOOL := FALSE;
END_VAR
VAR
    state : USINT := 0;
    previous_fault : BOOL := FALSE;
    fault_rise : BOOL := FALSE;
    sampled_fault : BOOL;
    sampled_ack : BOOL;
    sampled_reset : BOOL;
END_VAR
VAR CONSTANT
    ST_IDLE : USINT := 0;
    ST_UNACK : USINT := 1;
    ST_ACKED : USINT := 2;
END_VAR

sampled_fault := Fault;
sampled_ack := Ack;
sampled_reset := Reset;

fault_rise := sampled_fault AND NOT previous_fault;
previous_fault := sampled_fault;

CASE state OF
    ST_IDLE:
        IF sampled_reset AND NOT sampled_fault THEN
            state := ST_IDLE;
        ELSIF fault_rise THEN
            state := ST_UNACK;
        ELSIF sampled_fault AND sampled_ack THEN
            state := ST_ACKED;
        ELSIF sampled_fault THEN
            state := ST_UNACK;
        END_IF;

    ST_UNACK:
        IF sampled_reset AND NOT sampled_fault THEN
            state := ST_IDLE;
        ELSIF fault_rise THEN
            state := ST_UNACK;
        ELSIF sampled_ack THEN
            state := ST_ACKED;
        END_IF;

    ST_ACKED:
        IF sampled_reset AND NOT sampled_fault THEN
            state := ST_IDLE;
        ELSIF fault_rise THEN
            state := ST_UNACK;
        END_IF;

    ELSE
        state := ST_IDLE;
END_CASE;

Alarm := state <> ST_IDLE;
Acknowledged := state = ST_ACKED;
Horn := Alarm AND NOT Acknowledged;
END_FUNCTION_BLOCK
