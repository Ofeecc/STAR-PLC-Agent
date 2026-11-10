FUNCTION_BLOCK FB_Task
VAR_INPUT
    Start : BOOL;
    Stop : BOOL;
    Reset : BOOL;
    ExtendDone : BOOL;
    ClampDone : BOOL;
    ReleaseDone : BOOL;
    RetractDone : BOOL;
END_VAR
VAR_OUTPUT
    Extend : BOOL;
    Clamp : BOOL;
    Release : BOOL;
    Retract : BOOL;
    Busy : BOOL;
    Done : BOOL;
END_VAR
VAR
    State : E_FixtureState := FixtureState_IDLE;
END_VAR

IF Stop OR Reset THEN
    State := FixtureState_IDLE;
ELSE
    CASE State OF
        FixtureState_IDLE:
            IF Start AND RetractDone THEN
                State := FixtureState_EXTEND;
            END_IF;

        FixtureState_EXTEND:
            IF ExtendDone THEN
                State := FixtureState_CLAMP;
            END_IF;

        FixtureState_CLAMP:
            IF ClampDone THEN
                State := FixtureState_RELEASE;
            END_IF;

        FixtureState_RELEASE:
            IF ReleaseDone THEN
                State := FixtureState_RETRACT;
            END_IF;

        FixtureState_RETRACT:
            IF RetractDone THEN
                State := FixtureState_DONE;
            END_IF;

        FixtureState_DONE:
            State := FixtureState_DONE;
    ELSE
        State := FixtureState_IDLE;
    END_CASE;
END_IF;

Extend := State = FixtureState_EXTEND;
Clamp := State = FixtureState_CLAMP;
Release := State = FixtureState_RELEASE;
Retract := State = FixtureState_RETRACT;
Busy := Extend OR Clamp OR Release OR Retract;
Done := State = FixtureState_DONE;
END_FUNCTION_BLOCK
