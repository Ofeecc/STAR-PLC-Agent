"""Build transparently hand-designed SELF tasks, fixed traces and ST examples.

This authoring script contains the original task records. Expected values below
are constants selected from the written requirements, not oracle outputs.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEMANTICS = (
    "At scan k, sample every input once, read retained pre-state q[k], execute one "
    "transition, and observe outputs O[k] at the end of that same scan. Updated "
    "state becomes q[k+1]. Reset the instance before each test. Step 0 executes "
    "normally; initial conditions describe pre-state, not an extra delayed scan. "
    "All timing in this task is explicitly counted in invocations, not wall time."
)


def port(direction, name, typ, description):
    return dict(direction=direction, name=name, type=typ, description=description)


def create(number, title, difficulty, scenario, requirement, ins, outs, initial,
           priorities, assumptions, atoms, properties, tests, variables, body):
    task_id = f"SELF{number:03d}"
    interface = [port("INPUT", *v) for v in ins] + [port("OUTPUT", *v) for v in outs]
    atomic = {v["name"]: v["description"] + " Boolean names are propositions; numeric names appear only inside defined predicates."
              for v in interface}
    atomic.update({"first": "True only on the first invocation after resetting the FB instance."})
    atomic.update(atoms)
    task = dict(schema_version=1, id=task_id, kind="self_built", title=title,
                difficulty=difficulty,
                provenance=dict(source_type="independent_synthesis", source_file="scripts/build_self_dataset.py",
                                source_index=number,
                                adaptation="Independently specified for this project; no public task was copied. "
                                           "The coding assistant chose the state variables, priority order and fixed scan traces, "
                                           "then reviewed the traces against a separate Python transition implementation.",
                                rationale=scenario,
                                review="Assistant consistency review of initialization, simultaneous commands, retained state "
                                       "and recovery boundaries; independent Python oracle checked against manual expected traces. "
                                       "Not an industrial safety certification or external expert review."),
                requirements=requirement, scenario=scenario, interface=interface,
                initial_conditions=initial, scan_semantics=SEMANTICS,
                safety_priority=priorities, assumptions=assumptions,
                atomic_propositions=atomic,
                ltl=[dict(id=f"P{k+1}", formula=p[0], explanation=p[1]) for k, p in enumerate(properties)],
                tests=tests)
    path = ROOT / "dataset/self_built" / (task_id + ".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(task, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    def output_declaration(name, typ):
        # Preserve observable power-up state as well as the internal latch.
        # In particular, ResetRequired and LeadA must already be TRUE before
        # the first invocation; assigning them in the body is too late.
        if name in initial and isinstance(initial[name], (bool, int, float)):
            value = initial[name]
            literal = ("TRUE" if value else "FALSE") if isinstance(value, bool) else str(value)
            return f"    {name} : {typ} := {literal};\n"
        return f"    {name} : {typ};\n"
    declaration = "FUNCTION_BLOCK FB_Task\nVAR_INPUT\n" + "".join(f"    {n} : {t};\n" for n,t,_ in ins)
    declaration += "END_VAR\nVAR_OUTPUT\n" + "".join(output_declaration(n, t) for n,t,_ in outs) + "END_VAR\n"
    if variables:
        declaration += "VAR\n" + variables.strip() + "\nEND_VAR\n"
    code = dict(declaration=declaration, implementation=body.strip()+"\n", supporting_objects=[],
                provenance="Hand-designed reference example authored with the task; not a model benchmark output. "
                           "CODESYS compilation and PLC execution are unverified until actual backend records exist.")
    (ROOT / "codesys/examples").mkdir(parents=True, exist_ok=True)
    (ROOT / "codesys/examples" / (task_id + ".json")).write_text(json.dumps(code, indent=2)+"\n", encoding="utf-8")


def trace(case_id, purpose, defaults, rows):
    return dict(id=case_id, purpose=purpose,
                steps=[dict(inputs={**defaults, **overrides}, expected=expected) for overrides, expected in rows])


BOOL = "BOOL"
create(1, "Guarded motor with retained run command", "easy",
       "A packaging motor uses a door guard as a scan-level permissive and a retained operator run request.",
       "Implement a guarded motor latch. Inputs are Start, Stop and GuardClosed. Run initially is FALSE. "
       "On every scan, Stop or an open guard forces Run FALSE. Otherwise Start sets Run TRUE; without Start "
       "retain Run. If Start remains held while the guard closes, starting on that closing scan is permitted. "
       "This is logic for a teaching controller, not a replacement for a safety-rated guard circuit.",
       [("Start",BOOL,"Operator start request"),("Stop",BOOL,"Stop request"),("GuardClosed",BOOL,"Door permissive")],
       [("Run",BOOL,"Motor run command")], {"Run":False},
       ["Open guard and Stop override Start", "Loss of permissive clears the retained latch"],
       ["Inputs are level-sensitive; no start edge is required."],
       {"qRun":"Run retained from the preceding invocation, initially FALSE."},
       [("G(first -> !qRun)","The instance starts with no retained run request."),
        ("G((Stop | !GuardClosed) -> !Run)","Stop and guard override every startup request in the same scan."),
        ("G((Start & !Stop & GuardClosed) -> Run)","A permitted start takes effect at end of the sampled scan."),
        ("G((!Start & !Stop & GuardClosed) -> (Run <-> qRun))","Retain the preceding run value without a new command."),
        ("G(Run -> X(Stop | !GuardClosed | Run))","Across invocations, run persists unless a higher-priority input intervenes.")],
       [trace("latch","Initialize, start, hold and stop",dict(Start=False,Stop=False,GuardClosed=True),[
           ({},{"Run":False}),({"Start":True},{"Run":True}),({},{"Run":True}),({"Stop":True},{"Run":False}),({},{"Run":False})]),
        trace("priority","Simultaneous requests and guard recovery",dict(Start=True,Stop=False,GuardClosed=True),[
           ({"Stop":True},{"Run":False}),({"GuardClosed":False},{"Run":False}),({},{"Run":True}),({"Start":False,"GuardClosed":False},{"Run":False}),({"Start":False},{"Run":False})])],
       "", """IF Stop OR NOT GuardClosed THEN
    Run := FALSE;
ELSIF Start THEN
    Run := TRUE;
END_IF;""")

create(2,"Reversing jog drive with a neutral scan", "medium",
       "A reversible positioning drive must break its previous direction command for one full output scan before reversing.",
       "ForwardButton and ReverseButton are jog commands. Stop, both buttons, or neither button gives both outputs FALSE. "
       "Exactly one button requests that direction. If the previous scan output commanded the opposite direction, "
       "give a neutral scan with both outputs FALSE; a request held into the following scan can then run. "
       "At initialization the previous direction is neutral. Never energize Forward and Reverse together.",
       [("ForwardButton",BOOL,"Forward jog request"),("ReverseButton",BOOL,"Reverse jog request"),("Stop",BOOL,"Stop request")],
       [("Forward",BOOL,"Forward contactor command"),("Reverse",BOOL,"Reverse contactor command")],
       {"previous_direction":0,"Forward":False,"Reverse":False},
       ["Stop and ambiguous button combinations command neutral", "Opposite-direction request inserts neutral"],[],
       {"qForward":"Previous scan Forward output; initially FALSE.","qReverse":"Previous scan Reverse output; initially FALSE.",
        "fwdOnly":"ForwardButton & !ReverseButton & !Stop.","revOnly":"ReverseButton & !ForwardButton & !Stop."},
       [("G(!(Forward & Reverse))","Direction outputs are mutually exclusive."),
        ("G((Stop | (ForwardButton <-> ReverseButton)) -> (!Forward & !Reverse))","Invalid or stopped requests produce neutral."),
        ("G((fwdOnly & qReverse) -> (!Forward & !Reverse))","Reversal from reverse has one neutral output scan."),
        ("G((revOnly & qForward) -> (!Forward & !Reverse))","Reversal from forward has one neutral output scan."),
        ("G((fwdOnly & !qReverse) -> Forward)","A permitted forward jog operates immediately."),
        ("G((revOnly & !qForward) -> Reverse)","A permitted reverse jog operates immediately.")],
       [trace("reverse","Direct reversal and held reverse request",dict(ForwardButton=False,ReverseButton=False,Stop=False),[
           ({"ForwardButton":True},{"Forward":True,"Reverse":False}),({"ReverseButton":True},{"Forward":False,"Reverse":False}),
           ({"ReverseButton":True},{"Forward":False,"Reverse":True}),({"ForwardButton":True},{"Forward":False,"Reverse":False}),
           ({"ForwardButton":True},{"Forward":True,"Reverse":False}),({},{"Forward":False,"Reverse":False})]),
        trace("ambiguous","Both buttons and Stop override direction",dict(ForwardButton=True,ReverseButton=True,Stop=False),[
           ({},{"Forward":False,"Reverse":False}),({"ReverseButton":False},{"Forward":True,"Reverse":False}),
           ({"Stop":True,"ReverseButton":False},{"Forward":False,"Reverse":False}),({"ForwardButton":False},{"Forward":False,"Reverse":True})])],
       "    PreviousDirection : SINT := 0;\n    DesiredDirection : SINT := 0;",
       """DesiredDirection := 0;
IF NOT Stop AND (ForwardButton XOR ReverseButton) THEN
    IF ForwardButton THEN DesiredDirection := 1; ELSE DesiredDirection := -1; END_IF;
END_IF;
IF (DesiredDirection <> 0) AND (PreviousDirection = -DesiredDirection) THEN
    DesiredDirection := 0;
END_IF;
Forward := DesiredDirection = 1;
Reverse := DesiredDirection = -1;
PreviousDirection := DesiredDirection;""")

create(3,"Emergency stop reset with restart inhibition", "medium",
       "A workshop spindle requires a deliberate reset with Start released before a restart after emergency-stop release.",
       "Run initially is FALSE and ResetRequired initially is TRUE. EStopNC=FALSE immediately forces Run FALSE and "
       "sets ResetRequired TRUE. While ResetRequired is TRUE, keep Run FALSE. Clear ResetRequired only when EStopNC "
       "is TRUE, Reset is TRUE, Start is FALSE and Stop is FALSE. That clearing scan cannot start the motor. "
       "Once reset, Stop stops the motor, Start starts it, otherwise retain Run. Start held during reset must not "
       "clear the restart inhibition. This educational logic does not implement a certified emergency-stop chain.",
       [("Start",BOOL,"Start request"),("Stop",BOOL,"Normal stop request"),("EStopNC",BOOL,"TRUE means emergency stop released"),("Reset",BOOL,"Reset request")],
       [("Run",BOOL,"Spindle run command"),("ResetRequired",BOOL,"Restart inhibition latch")],
       {"Run":False,"ResetRequired":True},
       ["Emergency stop overrides all requests", "Restart inhibition overrides Start", "Normal stop overrides Start"],[],
       {"qRequired":"Pre-scan ResetRequired, initially TRUE.","qRun":"Pre-scan Run, initially FALSE.",
        "validReset":"EStopNC & Reset & !Start & !Stop."},
       [("G(first -> (qRequired & !qRun))","A fresh instance requires reset."),
        ("G(!EStopNC -> (!Run & ResetRequired))","Emergency stop forces safe outputs immediately."),
        ("G(qRequired -> !Run)","Reset acceptance and motor start cannot share one scan."),
        ("G((qRequired & EStopNC) -> (ResetRequired <-> !validReset))","Reset requires released Start and Stop."),
        ("G((!qRequired & EStopNC & !Stop & Start) -> Run)","A subsequent permitted start energizes the motor."),
        ("G((!qRequired & EStopNC & Stop) -> !Run)","Stop has priority after reset.")],
       [trace("reset_restart","Power-up inhibition, reset, run and emergency stop",dict(Start=False,Stop=False,EStopNC=True,Reset=False),[
           ({"Start":True},{"Run":False,"ResetRequired":True}),({"Reset":True},{"Run":False,"ResetRequired":False}),
           ({"Start":True},{"Run":True,"ResetRequired":False}),({},{"Run":True,"ResetRequired":False}),
           ({"EStopNC":False,"Reset":True},{"Run":False,"ResetRequired":True}),({"Start":True},{"Run":False,"ResetRequired":True})]),
        trace("invalid_reset","Held Start and Stop block reset",dict(Start=True,Stop=False,EStopNC=True,Reset=True),[
           ({},{"Run":False,"ResetRequired":True}),({"Start":False,"Stop":True},{"Run":False,"ResetRequired":True}),
           ({"Start":False},{"Run":False,"ResetRequired":False}),({"Stop":True},{"Run":False,"ResetRequired":False})])],
       "    Required : BOOL := TRUE;",
       """IF NOT EStopNC THEN
    Run := FALSE; Required := TRUE;
ELSIF Required THEN
    Run := FALSE;
    IF Reset AND NOT Start AND NOT Stop THEN Required := FALSE; END_IF;
ELSIF Stop THEN
    Run := FALSE;
ELSIF Start THEN
    Run := TRUE;
END_IF;
ResetRequired := Required;""")

create(4,"Pallet indexing with a latched jam fault", "medium",
       "A small conveyor indexes one pallet to an exit sensor and preserves a jam indication until a deliberate reset.",
       "Use states IDLE, MOVING, COMPLETE and FAULT, initially IDLE. Jam forces FAULT from any state; Belt and "
       "Complete are FALSE there. With Jam FALSE, Reset returns any state to IDLE. Without Reset, FAULT is "
       "latched. Stop aborts a non-fault cycle to IDLE. In IDLE accept Start only if AtExit is FALSE and enter "
       "MOVING. In MOVING, AtExit enters COMPLETE. COMPLETE is held until Reset or Stop; Start alone does "
       "not clear it. Belt is TRUE only in MOVING, Complete only in COMPLETE and Fault only in FAULT. "
       "Execute at most one state transition per scan.",
       [("Start",BOOL,"Start one pallet"),("Stop",BOOL,"Abort cycle"),("AtExit",BOOL,"Pallet at exit"),("Jam",BOOL,"Jam detected"),("Reset",BOOL,"Clear completion or cleared jam")],
       [("Belt",BOOL,"Conveyor command"),("Complete",BOOL,"Pallet cycle completed"),("Fault",BOOL,"Latched jam fault")],
       {"state":"IDLE","Belt":False,"Complete":False,"Fault":False},
       ["Jam", "Reset when Jam is FALSE", "Latched fault", "Stop", "Normal transition"],[],
       {"qIdle":"Pre-state IDLE.","qMoving":"Pre-state MOVING.","qComplete":"Pre-state COMPLETE.","qFault":"Pre-state FAULT."},
       [("G(Jam -> (Fault & !Belt & !Complete))","Jam wins over Reset and Start."),
        ("G((qFault & !Reset) -> Fault)","Fault requires an explicit clear operation."),
        ("G((!Jam & Reset) -> (!Belt & !Complete & !Fault))","A cleared-jam reset returns IDLE."),
        ("G((qIdle & !Jam & !Reset & !Stop & Start & !AtExit) -> Belt)","A valid idle start moves the pallet."),
        ("G((qMoving & AtExit & !Jam & !Reset & !Stop) -> (Complete & !Belt))","Exit arrival stops indexing in the same scan."),
        ("G(!(Belt & (Complete | Fault)))","Movement excludes completion and fault outputs."),
        ("G(Fault -> (G Fault | (Fault U (!Jam & Reset))))","A latched jam remains until a cleared-jam reset, or forever if no such reset occurs; this does not assume eventual reset.")],
       [trace("index","One pallet and retained completion",dict(Start=False,Stop=False,AtExit=False,Jam=False,Reset=False),[
           ({"Start":True},{"Belt":True,"Complete":False,"Fault":False}),({},{"Belt":True,"Complete":False,"Fault":False}),
           ({"AtExit":True},{"Belt":False,"Complete":True,"Fault":False}),({"Start":True},{"Belt":False,"Complete":True,"Fault":False}),
           ({"Reset":True},{"Belt":False,"Complete":False,"Fault":False})]),
        trace("jam","Jam priority, retained fault and safe reset",dict(Start=True,Stop=False,AtExit=False,Jam=False,Reset=False),[
           ({},{"Belt":True,"Complete":False,"Fault":False}),({"Jam":True,"Reset":True},{"Belt":False,"Complete":False,"Fault":True}),
           ({},{"Belt":False,"Complete":False,"Fault":True}),({"Reset":True},{"Belt":False,"Complete":False,"Fault":False}),
           ({"AtExit":True},{"Belt":False,"Complete":False,"Fault":False}),({"Stop":True},{"Belt":False,"Complete":False,"Fault":False})])],
       "    State : USINT := 0;",
       """IF Jam THEN State := 3;
ELSIF Reset THEN State := 0;
ELSIF State = 3 THEN
    State := 3;
ELSIF Stop THEN State := 0;
ELSE
    CASE State OF
        0: IF Start AND NOT AtExit THEN State := 1; END_IF;
        1: IF AtExit THEN State := 2; END_IF;
    END_CASE;
END_IF;
Belt := State = 1;
Complete := State = 2;
Fault := State = 3;""")

create(5,"Three phase signal with externally clocked durations", "medium",
       "A training traffic signal uses a deterministic logical tick, allowing reproducible testing without wall-clock timing jitter.",
       "Phase 0 is RED for 2 Tick=TRUE invocations, phase 1 GREEN for 3, and phase 2 AMBER for 1. "
       "At initialization set phase RED and elapsed ticks zero. With Enable FALSE force RED and clear elapsed ticks "
       "every scan. With Enable TRUE and Tick FALSE retain phase and elapsed ticks. A TRUE Tick adds one; upon "
       "reaching that phase's duration transition RED->GREEN->AMBER->RED and clear elapsed ticks. Output Phase "
       "is 0,1,2 and exactly one color describes the post-transition phase. Tick is an enable level per invocation, "
       "not a rising-edge detector.",
       [("Enable",BOOL,"Enable normal signal cycle"),("Tick",BOOL,"One logical tick on each TRUE invocation")],
       [("Red",BOOL,"Red lamp"),("Green",BOOL,"Green lamp"),("Amber",BOOL,"Amber lamp"),("Phase","USINT","Post-scan phase number")],
       {"phase":0,"elapsed_ticks":0},["Disable resets the cycle to RED"],
       ["A logical tick is not claimed to be a physical second.","No opposite road or pedestrian signal is controlled."],
       {"qRedLast":"Pre-state is RED with one elapsed tick.","qGreenLast":"Pre-state is GREEN with two elapsed ticks.",
        "qAmber":"Pre-state is AMBER.","qPhase":"Pre-state phase number.","oneColor":"Exactly one of Red, Green and Amber is TRUE."},
       [("G(oneColor)","The lamp encoding is one-hot."),
        ("G(!Enable -> (Red & !Green & !Amber))","Disabled operation is a steady red."),
        ("G((Enable & !Tick) -> (Phase = qPhase))","No tick preserves phase."),
        ("G((Enable & Tick & qRedLast) -> Green)","The second red tick enters green."),
        ("G((Enable & Tick & qGreenLast) -> Amber)","The third green tick enters amber."),
        ("G((Enable & Tick & qAmber) -> Red)","One amber tick returns red."),
        ("(G Enable & G(F Tick)) -> (G(F Red) & G(F Green) & G(F Amber))","Persistent enable plus infinitely many ticks makes every phase recur; finite traces cannot prove this liveness property.")],
       [trace("cycle","Full phase duration boundaries and pause",dict(Enable=True,Tick=True),[
           ({},{"Phase":0,"Red":True,"Green":False,"Amber":False}),({"Tick":False},{"Phase":0}),({},{"Phase":1}),
           ({},{"Phase":1}),({},{"Phase":1}),({},{"Phase":2}),({},{"Phase":0})]),
        trace("disable","Disable clears elapsed tick progress",dict(Enable=True,Tick=True),[
           ({},{"Phase":0}),({},{"Phase":1}),({"Enable":False},{"Phase":0,"Red":True}),
           ({},{"Phase":0}),({},{"Phase":1})])],
       "    CurrentPhase : USINT := 0;\n    Elapsed : USINT := 0;\n    Limit : USINT := 2;",
       """IF NOT Enable THEN
    CurrentPhase := 0; Elapsed := 0;
ELSIF Tick THEN
    CASE CurrentPhase OF 0: Limit := 2; 1: Limit := 3; 2: Limit := 1; END_CASE;
    Elapsed := Elapsed + 1;
    IF Elapsed >= Limit THEN
        Elapsed := 0;
        IF CurrentPhase = 2 THEN CurrentPhase := 0; ELSE CurrentPhase := CurrentPhase + 1; END_IF;
    END_IF;
END_IF;
Phase := CurrentPhase;
Red := CurrentPhase = 0;
Green := CurrentPhase = 1;
Amber := CurrentPhase = 2;""")

create(6,"Tank filling with hysteresis and sensor inconsistency", "easy",
       "A refill tank avoids contactor chatter between low and high level switches and detects physically inconsistent switch combinations.",
       "LowWet and HighWet indicate water covering the respective lower and upper switches. HighWet TRUE with "
       "LowWet FALSE is inconsistent: SensorFault TRUE and Fill FALSE. SensorFault is combinational and clears "
       "when inputs become consistent. Inhibit or HighWet also forces Fill FALSE. Otherwise LowWet FALSE starts "
       "Fill; LowWet TRUE and HighWet FALSE retains Fill. Fill initializes FALSE. Clearing Inhibit at a middle "
       "level retains the resulting stopped state until water falls below the low switch.",
       [("LowWet",BOOL,"Water reaches lower switch"),("HighWet",BOOL,"Water reaches upper switch"),("Inhibit",BOOL,"External fill inhibit")],
       [("Fill",BOOL,"Inlet valve command"),("SensorFault",BOOL,"Inconsistent level switches")],
       {"Fill":False},["Inconsistent sensors or Inhibit stop filling", "High switch stops", "Low switch starts", "Middle level retains"],[],
       {"qFill":"Pre-scan retained Fill, initially FALSE.","middle":"LowWet & !HighWet."},
       [("G(SensorFault <-> (HighWet & !LowWet))","Fault exactly identifies inconsistent switches."),
        ("G((SensorFault | Inhibit | HighWet) -> !Fill)","Inhibit, fault and full tank force shutoff."),
        ("G((!LowWet & !HighWet & !Inhibit) -> Fill)","A low tank starts filling."),
        ("G((middle & !Inhibit) -> (Fill <-> qFill))","The middle band retains the prior command."),
        ("G(first -> !qFill)","No retained filling command exists on reset.")],
       [trace("hysteresis","Fill cycle across both switching thresholds",dict(LowWet=False,HighWet=False,Inhibit=False),[
           ({},{"Fill":True,"SensorFault":False}),({"LowWet":True},{"Fill":True,"SensorFault":False}),
           ({"LowWet":True,"HighWet":True},{"Fill":False,"SensorFault":False}),({"LowWet":True},{"Fill":False,"SensorFault":False}),
           ({},{"Fill":True,"SensorFault":False})]),
        trace("fault_inhibit","Invalid switch pair and inhibit recovery",dict(LowWet=True,HighWet=False,Inhibit=False),[
           ({},{"Fill":False,"SensorFault":False}),({"LowWet":False,"HighWet":True},{"Fill":False,"SensorFault":True}),
           ({"LowWet":False},{"Fill":True,"SensorFault":False}),({"Inhibit":True},{"Fill":False,"SensorFault":False}),
           ({},{"Fill":False,"SensorFault":False})])],"",
       """SensorFault := HighWet AND NOT LowWet;
IF SensorFault OR Inhibit OR HighWet THEN Fill := FALSE;
ELSIF NOT LowWet THEN Fill := TRUE;
END_IF;""")

create(7,"Duty standby alternation with healthy pump fallback", "medium",
       "Two sump pumps share wear by alternating the preferred pump only after a demand episode that actually delivered pumping.",
       "LeadA initializes TRUE. During Demand choose preferred healthy pump, falling back to the other if the "
       "preferred pump is faulted. Both faulty means neither runs. Fault changes cause immediate fallback within "
       "the episode. Never run both. When Demand falls FALSE, toggle LeadA exactly once if any pump ran during "
       "that just-ended continuous demand episode. An all-faulted episode with no running scan does not toggle "
       "the lead. Without Demand both pumps are FALSE. LeadA is the retained preference for the current or next "
       "episode, not a report of which fallback pump is presently running.",
       [("Demand",BOOL,"Sump pumping demand"),("FaultA",BOOL,"Pump A unavailable"),("FaultB",BOOL,"Pump B unavailable")],
       [("PumpA",BOOL,"Pump A run command"),("PumpB",BOOL,"Pump B run command"),("LeadA",BOOL,"TRUE selects A as preferred pump")],
       {"LeadA":True,"previous_demand":False,"episode_served":False},
       ["Faulted pumps never run", "No demand forces both off", "Prefer selected lead, then healthy fallback"],[],
       {"qLeadA":"Pre-scan lead preference, initially TRUE.","completedServed":"Pre-scan Demand was TRUE, current Demand is FALSE and a pump ran in that episode."},
       [("G(!(PumpA & PumpB))","At most one pump runs."),
        ("G((!Demand | FaultA) -> !PumpA)","A cannot run without demand or with its fault."),
        ("G((!Demand | FaultB) -> !PumpB)","B cannot run without demand or with its fault."),
        ("G((Demand & LeadA & !FaultA) -> PumpA)","A is selected when it is the healthy lead."),
        ("G((Demand & !LeadA & !FaultB) -> PumpB)","B is selected when it is the healthy lead."),
        ("G(completedServed -> (LeadA <-> !qLeadA))","Toggle once on a served demand's falling edge."),
        ("G(!completedServed -> (LeadA <-> qLeadA))","Unserved episodes and held demand preserve preference.")],
       [trace("alternate","Served episodes alternate preference",dict(Demand=False,FaultA=False,FaultB=False),[
           ({},{"PumpA":False,"PumpB":False,"LeadA":True}),({"Demand":True},{"PumpA":True,"PumpB":False,"LeadA":True}),
           ({"Demand":True},{"PumpA":True,"PumpB":False,"LeadA":True}),({},{"PumpA":False,"PumpB":False,"LeadA":False}),
           ({},{"LeadA":False}),({"Demand":True},{"PumpA":False,"PumpB":True,"LeadA":False}),({},{"LeadA":True})]),
        trace("fallback","Fault fallback, unserved episode and recovery",dict(Demand=False,FaultA=True,FaultB=True),[
           ({"Demand":True},{"PumpA":False,"PumpB":False,"LeadA":True}),({},{"LeadA":True}),
           ({"Demand":True,"FaultB":False},{"PumpA":False,"PumpB":True,"LeadA":True}),
           ({"Demand":True,"FaultA":False,"FaultB":False},{"PumpA":True,"PumpB":False,"LeadA":True}),({},{"LeadA":False})])],
       "    PreferredA : BOOL := TRUE;\n    PreviousDemand : BOOL := FALSE;\n    Served : BOOL := FALSE;",
       """PumpA := FALSE; PumpB := FALSE;
IF NOT Demand THEN
    IF PreviousDemand AND Served THEN PreferredA := NOT PreferredA; END_IF;
    Served := FALSE;
ELSE
    IF NOT PreviousDemand THEN Served := FALSE; END_IF;
    IF PreferredA THEN
        PumpA := NOT FaultA;
        PumpB := FaultA AND NOT FaultB;
    ELSE
        PumpB := NOT FaultB;
        PumpA := FaultB AND NOT FaultA;
    END_IF;
    Served := Served OR PumpA OR PumpB;
END_IF;
PreviousDemand := Demand;
LeadA := PreferredA;""")

create(8,"Consecutive scan qualification with an immediate trip", "easy",
       "A cyclic quality check accepts a request only after a configurable number of consecutive healthy invocations.",
       "Preset is valid from 1 through 5. Initialize Count=0. If Trip TRUE, Request FALSE, or Preset invalid, "
       "clear Count and Ready. Otherwise Count becomes min(previous Count+1, Preset); Ready is TRUE exactly "
       "when Count reaches Preset. Count saturates. Changes of Preset take effect immediately using the same "
       "rule, so reducing Preset can qualify on that scan. This counts invocations, not elapsed milliseconds.",
       [("Request",BOOL,"Raw qualification request"),("Trip",BOOL,"Immediate inhibit"),("Preset","USINT","Required consecutive scans, valid 1 through 5")],
       [("Ready",BOOL,"Qualified request"),("Count","USINT","Saturated consecutive scan count")],
       {"Count":0,"Ready":False},["Trip, missing request and invalid Preset clear progress"],[],
       {"invalid":"Preset < 1 or Preset > 5.","qualified":"Count >= Preset and Preset is valid.",
        "qCount":"Pre-scan Count, initially zero.","nextCount":"min(qCount+1, Preset) as an integer expression."},
       [("G((Trip | !Request | invalid) -> (!Ready & (Count = 0)))","Every interruption clears qualification immediately."),
        ("G((Request & !Trip & !invalid) -> (Count = nextCount))","Healthy scans increment and saturate precisely."),
        ("G(Ready <-> qualified)","The indication agrees with the post-scan count."),
        ("G(!invalid -> ((Count >= 0) & (Count <= Preset)))","The counter stays within bounds."),
        ("(G(Request & !Trip & !invalid)) -> F Ready","A perpetually valid request qualifies within at most five scans, even if valid Preset varies.")],
       [trace("delay","Three scans qualify, hold saturates, trip clears",dict(Request=True,Trip=False,Preset=3),[
           ({},{"Count":1,"Ready":False}),({},{"Count":2,"Ready":False}),({},{"Count":3,"Ready":True}),
           ({},{"Count":3,"Ready":True}),({"Trip":True},{"Count":0,"Ready":False}),({},{"Count":1,"Ready":False})]),
        trace("bounds","Invalid presets and immediate reduced threshold",dict(Request=True,Trip=False,Preset=5),[
           ({"Preset":0},{"Count":0,"Ready":False}),({"Preset":6},{"Count":0,"Ready":False}),({},{"Count":1,"Ready":False}),
           ({"Preset":1},{"Count":1,"Ready":True}),({"Request":False},{"Count":0,"Ready":False})])],
       "    ValidPreset : BOOL;",
       """ValidPreset := (Preset >= 1) AND (Preset <= 5);
IF Trip OR NOT Request OR NOT ValidPreset THEN
    Count := 0; Ready := FALSE;
ELSE
    IF Count < Preset THEN Count := Count + 1; ELSE Count := Preset; END_IF;
    Ready := Count >= Preset;
END_IF;""")

create(9,"Rising edge batch counter with reset sampling", "easy",
       "A packaging batch counts individual sensor edges and prevents a held sensor during reset from being counted again.",
       "Target is valid 1..20. Initialize Count=0 and previous PartPulse FALSE. Error is TRUE exactly when "
       "Target is invalid. An invalid Target or Reset clears Count and Complete. Otherwise count only a "
       "FALSE-to-TRUE PartPulse transition, then clamp Count to Target. Complete is TRUE when Count reaches "
       "Target and remains TRUE until reset or an invalid target; a higher Target can clear it. Every scan, "
       "including reset and invalid-target scans, samples PartPulse into its edge memory. A held TRUE pulse "
       "after reset therefore cannot cause a phantom count.",
       [("PartPulse",BOOL,"Part detection level"),("Reset",BOOL,"Reset batch"),("Target","USINT","Batch target, valid 1 through 20")],
       [("Count","USINT","Saturated part count"),("Complete",BOOL,"Target reached"),("Error",BOOL,"Invalid target")],
       {"Count":0,"previous_pulse":False},["Invalid Target and Reset override counting", "Update edge memory on every scan"],[],
       {"invalid":"Target < 1 or Target > 20.","rise":"PartPulse & !qPulse.","qPulse":"Previous scan PartPulse, initially FALSE.",
        "qCount":"Pre-scan Count, initially zero.","countAfterEdge":"min(qCount + (1 if rise else 0), Target)."},
       [("G(Error <-> invalid)","Target validation is exact."),
        ("G((Reset | invalid) -> ((Count = 0) & !Complete))","Reset or invalid target clears the batch."),
        ("G((!Reset & !invalid) -> (Count = countAfterEdge))","Only rising edges add an item, with saturation."),
        ("G((!Reset & !invalid) -> (Complete <-> (Count >= Target)))","Complete reports the post-scan count."),
        ("G(PartPulse -> X qPulse)","Edge memory samples the pulse even during reset.")],
       [trace("edges","Held pulses count once and target saturates",dict(PartPulse=False,Reset=False,Target=2),[
           ({},{"Count":0,"Complete":False,"Error":False}),({"PartPulse":True},{"Count":1,"Complete":False}),
           ({"PartPulse":True},{"Count":1,"Complete":False}),({},{"Count":1}),({"PartPulse":True},{"Count":2,"Complete":True}),
           ({},{"Count":2,"Complete":True}),({"PartPulse":True},{"Count":2,"Complete":True})]),
        trace("reset_edge","Reset while pulse is high suppresses phantom count",dict(PartPulse=True,Reset=False,Target=1),[
           ({"Reset":True},{"Count":0,"Complete":False,"Error":False}),({},{"Count":0,"Complete":False}),
           ({"PartPulse":False},{"Count":0}),({},{"Count":1,"Complete":True}),({"Target":0},{"Count":0,"Complete":False,"Error":True}),
           ({"Target":21},{"Count":0,"Complete":False,"Error":True})])],
       "    PreviousPulse : BOOL := FALSE;\n    Rising : BOOL;",
       """Rising := PartPulse AND NOT PreviousPulse;
Error := (Target < 1) OR (Target > 20);
IF Error OR Reset THEN
    Count := 0; Complete := FALSE;
ELSE
    IF Rising AND (Count < Target) THEN Count := Count + 1; END_IF;
    IF Count > Target THEN Count := Target; END_IF;
    Complete := Count >= Target;
END_IF;
PreviousPulse := PartPulse;""")

create(10,"Latched alarm with acknowledgment and reannunciation", "medium",
       "A panel alarm retains the event after a fault clears, silences the horn after acknowledgment, and sounds again for a new fault edge.",
       "Initialize Alarm and Acknowledged FALSE and previous Fault FALSE. A Fault sets Alarm. A rising Fault "
       "also clears Acknowledged, taking priority over Ack on that scan. While Fault remains TRUE, Ack can "
       "set Acknowledged. When Fault is FALSE the alarm remains latched; Ack can acknowledge that retained "
       "alarm. Reset clears both values only when Fault is FALSE, taking priority over Ack then. A new Fault "
       "rising edge reannunciates even if an old alarm was already latched. Horn equals Alarm AND NOT "
       "Acknowledged. Always update the previous Fault sample.",
       [("Fault",BOOL,"Current fault condition"),("Ack",BOOL,"Acknowledge horn"),("Reset",BOOL,"Clear a removed fault")],
       [("Alarm",BOOL,"Latched visible alarm"),("Acknowledged",BOOL,"Alarm acknowledged"),("Horn",BOOL,"Unacknowledged alarm horn")],
       {"Alarm":False,"Acknowledged":False,"previous_fault":False},
       ["New fault edge reannunciates before Ack", "Reset only clears when Fault is absent", "Reset then precedes Ack"],[],
       {"rise":"Fault & !qFault.","qFault":"Previous Fault sample, initially FALSE.","qAlarm":"Pre-scan Alarm.",
        "qAck":"Pre-scan Acknowledged."},
       [("G(Horn <-> (Alarm & !Acknowledged))","Horn follows the latched acknowledgment state."),
        ("G(Fault -> Alarm)","A present fault cannot be reset away."),
        ("G(rise -> (Alarm & !Acknowledged & Horn))","Every new event annunciates despite simultaneous Ack."),
        ("G((Reset & !Fault) -> (!Alarm & !Acknowledged & !Horn))","Reset clears a removed fault."),
        ("G((!Fault & !Reset & qAlarm) -> Alarm)","Fault disappearance does not clear the visible alarm."),
        ("G((!rise & !Reset & Ack & qAlarm) -> Acknowledged)","Acknowledgment silences a retained event.")],
       [trace("annunciate","Acknowledge, fault clear and new event",dict(Fault=False,Ack=False,Reset=False),[
           ({},{"Alarm":False,"Acknowledged":False,"Horn":False}),({"Fault":True,"Ack":True},{"Alarm":True,"Acknowledged":False,"Horn":True}),
           ({"Fault":True,"Ack":True},{"Alarm":True,"Acknowledged":True,"Horn":False}),({},{"Alarm":True,"Acknowledged":True,"Horn":False}),
           ({"Fault":True},{"Alarm":True,"Acknowledged":False,"Horn":True}),({"Reset":True},{"Alarm":False,"Acknowledged":False,"Horn":False})]),
        trace("reset_priority","Present fault blocks reset; removed fault reset wins",dict(Fault=True,Ack=False,Reset=True),[
           ({},{"Alarm":True,"Acknowledged":False,"Horn":True}),({"Ack":True},{"Alarm":True,"Acknowledged":True,"Horn":False}),
           ({"Fault":False,"Ack":True},{"Alarm":False,"Acknowledged":False,"Horn":False})])],
       "    PreviousFault : BOOL := FALSE;\n    Rising : BOOL;",
       """Rising := Fault AND NOT PreviousFault;
IF Reset AND NOT Fault THEN
    Alarm := FALSE; Acknowledged := FALSE;
ELSIF Fault THEN
    Alarm := TRUE;
    IF Rising THEN Acknowledged := FALSE; ELSIF Ack THEN Acknowledged := TRUE; END_IF;
ELSIF Alarm AND Ack THEN
    Acknowledged := TRUE;
END_IF;
Horn := Alarm AND NOT Acknowledged;
PreviousFault := Fault;""")

create(11,"Single cycle actuator handshakes with one transition per scan", "hard",
       "An assembly fixture coordinates an extending slide and a clamp using explicit completion handshakes, allowing deterministic commissioning tests.",
       "Use IDLE, EXTEND, CLAMP, RELEASE, RETRACT and DONE states, initially IDLE. Stop or Reset immediately "
       "returns IDLE. Start is accepted in IDLE only if RetractDone indicates the home position. Then enter "
       "EXTEND; ExtendDone enters CLAMP, ClampDone enters RELEASE, ReleaseDone enters RETRACT, and "
       "RetractDone enters DONE. Execute at most one transition per scan, so even all feedbacks TRUE cannot "
       "skip a state. DONE holds until Reset or Stop. Each of Extend, Clamp, Release and Retract is TRUE "
       "exactly in its corresponding post-transition state. Busy is TRUE in those four action states; Done "
       "is TRUE only in DONE. Start during Busy or DONE is ignored.",
       [("Start",BOOL,"Begin one fixture cycle"),("Stop",BOOL,"Abort fixture cycle"),("Reset",BOOL,"Clear cycle state"),
        ("ExtendDone",BOOL,"Extension completion handshake"),("ClampDone",BOOL,"Clamp completion handshake"),
        ("ReleaseDone",BOOL,"Release completion handshake"),("RetractDone",BOOL,"Retracted home handshake")],
       [("Extend",BOOL,"Slide extend command"),("Clamp",BOOL,"Clamp command"),("Release",BOOL,"Release command"),
        ("Retract",BOOL,"Slide retract command"),("Busy",BOOL,"An action state is active"),("Done",BOOL,"Cycle completed")],
       {"state":"IDLE","all_commands":False},["Stop or Reset overrides all transitions", "At most one state transition per invocation"],
       ["Completion inputs are handshake states; no mechanical safety certification is implied.","No timeout is included; an absent handshake intentionally stalls the current action."],
       {"qIdle":"Pre-state IDLE.","qExtend":"Pre-state EXTEND.","qClamp":"Pre-state CLAMP.","qRelease":"Pre-state RELEASE.",
        "qRetract":"Pre-state RETRACT.","qDone":"Pre-state DONE.","normal":"!Stop & !Reset.",
        "oneAction":"At most one of Extend, Clamp, Release, Retract is TRUE."},
       [("G(oneAction)","Action commands never overlap."),
        ("G((Stop | Reset) -> (!Busy & !Done & !Extend & !Clamp & !Release & !Retract))","Abort clears every command immediately."),
        ("G((normal & qIdle & Start & RetractDone) -> Extend)","Home-qualified Start enters only the first action."),
        ("G((normal & qExtend & ExtendDone) -> Clamp)","Extension completion enters clamp."),
        ("G((normal & qClamp & ClampDone) -> Release)","Clamp completion enters release."),
        ("G((normal & qRelease & ReleaseDone) -> Retract)","Release completion enters retract."),
        ("G((normal & qRetract & RetractDone) -> Done)","Home arrival completes the cycle."),
        ("G((normal & qDone) -> Done)","A completed cycle cannot restart without an explicit clear."),
        ("G((normal & qExtend & !ExtendDone) -> Extend)","The fixture waits for an extension handshake rather than assuming completion.")],
       [trace("handshake","Normal cycle and completion retention",dict(Start=False,Stop=False,Reset=False,ExtendDone=False,ClampDone=False,ReleaseDone=False,RetractDone=False),[
           ({"Start":True},{"Busy":False,"Done":False}),({"Start":True,"RetractDone":True},{"Extend":True,"Busy":True,"Done":False}),
           ({},{"Extend":True}),({"ExtendDone":True},{"Extend":False,"Clamp":True}),
           ({"ClampDone":True},{"Clamp":False,"Release":True}),({"ReleaseDone":True},{"Release":False,"Retract":True}),
           ({"RetractDone":True},{"Retract":False,"Busy":False,"Done":True}),({"Start":True},{"Busy":False,"Done":True}),
           ({"Reset":True},{"Busy":False,"Done":False})]),
        trace("single_transition","All handshakes cannot skip states; Stop aborts",dict(Start=True,Stop=False,Reset=False,ExtendDone=True,ClampDone=True,ReleaseDone=True,RetractDone=True),[
           ({},{"Extend":True,"Clamp":False,"Release":False,"Retract":False}),({},{"Extend":False,"Clamp":True}),
           ({},{"Clamp":False,"Release":True}),({"Stop":True},{"Extend":False,"Clamp":False,"Release":False,"Retract":False,"Busy":False,"Done":False}),
           ({"Reset":True},{"Busy":False,"Done":False})])],
       "    State : USINT := 0;",
       """IF Stop OR Reset THEN
    State := 0;
ELSE
    CASE State OF
        0: IF Start AND RetractDone THEN State := 1; END_IF;
        1: IF ExtendDone THEN State := 2; END_IF;
        2: IF ClampDone THEN State := 3; END_IF;
        3: IF ReleaseDone THEN State := 4; END_IF;
        4: IF RetractDone THEN State := 5; END_IF;
    END_CASE;
END_IF;
Extend := State = 1; Clamp := State = 2;
Release := State = 3; Retract := State = 4;
Busy := (State >= 1) AND (State <= 4);
Done := State = 5;""")

create(12,"Bounded automatic fault retries with a recovery dwell", "hard",
       "A laboratory feeder allows two automatic retries after a transient process fault and locks out a repeatedly failing actuator.",
       "States are IDLE, RUNNING, WAIT and LOCKED, initially IDLE with Attempts=0. Start in IDLE starts only "
       "when Fault FALSE. A Fault while RUNNING immediately switches off Run. If Attempts<2 enter WAIT, else "
       "enter LOCKED. WAIT requires two consecutive Fault=FALSE scans before automatically restarting; a "
       "TRUE Fault clears the recovery dwell. Each automatic restart increments Attempts once. LOCKED persists "
       "despite Start or Stop. A Reset is accepted only when Fault FALSE and Start FALSE; it returns any state "
       "to IDLE and clears Attempts. Otherwise Stop aborts a non-locked state to IDLE and clears its dwell, "
       "retaining Attempts. Reset acceptance takes priority over Stop. Run is TRUE only in RUNNING and Locked "
       "only in LOCKED. Attempts counts automatic restarts, not the initial operator start. No scan may "
       "perform more than one transition.",
       [("Start",BOOL,"Operator start request"),("Stop",BOOL,"Abort without clearing retry count"),("Fault",BOOL,"Process fault"),("Reset",BOOL,"Clear retry history with Start released")],
       [("Run",BOOL,"Feeder command"),("Locked",BOOL,"Retry exhaustion lockout"),("Attempts","USINT","Automatic restarts issued, zero through two")],
       {"state":"IDLE","Attempts":0,"recovery_free_scans":0},
       ["Valid reset", "Latched lockout", "Stop", "Running fault", "Recovery dwell", "Idle start"],
       ["The fault is an educational process input, not a personnel safety function.","Operator stop/start does not restore the automatic retry budget; only accepted Reset does."],
       {"qLocked":"Pre-state LOCKED.","qRunning":"Pre-state RUNNING.","qWait":"Pre-state WAIT.",
        "qAttempts":"Pre-scan Attempts, initially zero.","validReset":"Reset & !Fault & !Start.",
        "retryDue":"qWait & !Fault and one preceding consecutive fault-free WAIT scan.","normal":"!validReset & !Stop."},
       [("G(Fault -> !Run)","A present fault cannot command the feeder."),
        ("G((Attempts >= 0) & (Attempts <= 2))","Automatic restart count stays within the budget."),
        ("G(validReset -> (!Run & !Locked & (Attempts = 0)))","Accepted reset clears history and leaves the feeder stopped."),
        ("G((qLocked & !validReset) -> (Locked & !Run))","Lockout requires a safe explicit reset."),
        ("G((qRunning & Fault & normal & (qAttempts = 2)) -> Locked)","Failure after the second retry exhausts the budget."),
        ("G((retryDue & normal) -> (Run & (Attempts = qAttempts + 1)))","Only the second consecutive healthy WAIT scan restarts."),
        ("G((qWait & Fault & normal) -> !Run)","A fault during recovery clears progress and prevents restart.")],
       [trace("exhaustion","Two automatic retries then third fault locks",dict(Start=False,Stop=False,Fault=False,Reset=False),[
           ({"Start":True},{"Run":True,"Locked":False,"Attempts":0}),({"Fault":True},{"Run":False,"Locked":False,"Attempts":0}),
           ({},{"Run":False,"Attempts":0}),({},{"Run":True,"Attempts":1}),
           ({"Fault":True},{"Run":False,"Attempts":1}),({},{"Run":False,"Attempts":1}),({},{"Run":True,"Attempts":2}),
           ({"Fault":True},{"Run":False,"Locked":True,"Attempts":2}),({"Stop":True},{"Run":False,"Locked":True,"Attempts":2}),
           ({"Reset":True,"Start":True},{"Run":False,"Locked":True,"Attempts":2}),({"Reset":True},{"Run":False,"Locked":False,"Attempts":0})]),
        trace("dwell_interrupt","Fault interrupts healthy dwell; Stop aborts wait",dict(Start=False,Stop=False,Fault=False,Reset=False),[
           ({"Start":True},{"Run":True,"Attempts":0}),({"Fault":True},{"Run":False,"Attempts":0}),({},{"Run":False}),
           ({"Fault":True},{"Run":False}),({},{"Run":False}),({},{"Run":True,"Attempts":1}),
           ({"Fault":True},{"Run":False,"Attempts":1}),({"Stop":True},{"Run":False,"Attempts":1}),({},{"Run":False,"Attempts":1})])],
       "    State : USINT := 0;\n    FreeScans : USINT := 0;",
       """IF Reset AND NOT Fault AND NOT Start THEN
    State := 0; Attempts := 0; FreeScans := 0;
ELSIF State = 3 THEN
    State := 3;
ELSIF Stop THEN
    State := 0; FreeScans := 0;
ELSE
    CASE State OF
        0: IF Start AND NOT Fault THEN State := 1; END_IF;
        1: IF Fault THEN
            FreeScans := 0;
            IF Attempts < 2 THEN State := 2; ELSE State := 3; END_IF;
           END_IF;
        2: IF Fault THEN FreeScans := 0; ELSE FreeScans := FreeScans + 1; END_IF;
           IF FreeScans >= 2 THEN
               Attempts := Attempts + 1; State := 1; FreeScans := 0;
           END_IF;
    END_CASE;
END_IF;
Run := State = 1; Locked := State = 3;""")

if __name__ == "__main__":
    print("Created 12 independent task records and 12 hand-designed ST examples.")
