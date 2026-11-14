FUNCTION_BLOCK FB_Task
VAR_INPUT
    THICKNESS_FAULT : BOOL;
    THICKNESS_SIGNAL_VALID : BOOL;
    CUTTING_RUN : BOOL;
    FaultTimestamp : DINT;
    CycleTime : TIME;
END_VAR
VAR_OUTPUT
    THICKNESS_ALARM : BOOL;
    Slab_Fault_Counter : UINT;
    Slab_Runtime_Accumulator : LTIME;
    Slab_Fault_History : ARRAY[0..4] OF DINT;
END_VAR
VAR
    _PrevValidFault : BOOL;
    _HoldActive : BOOL;
    _HoldElapsed : TIME;
    _FaultRise : BOOL;
END_VAR

_FaultRise := THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT AND NOT _PrevValidFault;

IF NOT THICKNESS_SIGNAL_VALID THEN
    _HoldActive := FALSE;
    _HoldElapsed := T#0MS;
    THICKNESS_ALARM := FALSE;
ELSE
    IF _FaultRise THEN
        _HoldActive := TRUE;
        _HoldElapsed := T#0MS;
    ELSIF _HoldActive THEN
        _HoldElapsed := _HoldElapsed + CycleTime;
        IF _HoldElapsed >= T#500MS THEN
            _HoldActive := FALSE;
        END_IF;
    END_IF;

    THICKNESS_ALARM := THICKNESS_FAULT OR _HoldActive;
END_IF;

IF _FaultRise THEN
    Slab_Fault_History[4] := Slab_Fault_History[3];
    Slab_Fault_History[3] := Slab_Fault_History[2];
    Slab_Fault_History[2] := Slab_Fault_History[1];
    Slab_Fault_History[1] := Slab_Fault_History[0];
    Slab_Fault_History[0] := FaultTimestamp;
    Slab_Fault_Counter := Slab_Fault_Counter + 1;
END_IF;

IF THICKNESS_SIGNAL_VALID AND NOT THICKNESS_FAULT AND CUTTING_RUN THEN
    Slab_Runtime_Accumulator := Slab_Runtime_Accumulator + TO_LTIME(CycleTime);
END_IF;

_PrevValidFault := THICKNESS_SIGNAL_VALID AND THICKNESS_FAULT;
END_FUNCTION_BLOCK
