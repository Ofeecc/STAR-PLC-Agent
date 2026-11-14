"""Independent scan oracles for SELF tasks; never a PLC runtime or ST interpreter.

These deliberately small Python transition systems check hand-authored test
expectations. They do not evaluate generated ST and must not be included in PLC
functional pass-rate numerators.
"""
from __future__ import annotations


class ReferenceController:
    _INITIAL_STATES = {
        "SELF001": {"run": False},
        "SELF002": {"direction": 0},
        "SELF003": {"required": True, "run": False},
        "SELF004": {"mode": 0},
        "SELF005": {"phase": 0, "age": 0},
        "SELF006": {"fill": False},
        "SELF007": {"lead_a": True, "served": False, "demand": False},
        "SELF008": {"count": 0},
        "SELF009": {"count": 0, "pulse": False},
        "SELF010": {"latched": False, "ack": False, "fault": False},
        "SELF011": {"mode": 0},
        "SELF012": {"mode": 0, "attempts": 0, "free": 0},
    }

    def __init__(self, task_id: str):
        if task_id not in {f"SELF{i:03d}" for i in range(1, 13)}:
            raise ValueError(f"No independent oracle for {task_id}")
        self.task_id = task_id
        self.state = dict(self._INITIAL_STATES[task_id])

    def step(self, inputs: dict, dt_ms=None) -> dict:
        """Execute one discrete scan. All SELF timers count scans, not dt_ms."""
        return getattr(self, "_" + self.task_id)(dict(inputs))

    def _SELF001(self, i):
        run = i["GuardClosed"] and not i["Stop"] and (i["Start"] or self.state.get("run", False))
        self.state["run"] = run
        return {"Run": run}

    def _SELF002(self, i):
        previous = self.state.get("direction", 0)
        desired = 0 if i["Stop"] or i["ForwardButton"] == i["ReverseButton"] else (1 if i["ForwardButton"] else -1)
        direction = 0 if desired and previous == -desired else desired
        self.state["direction"] = direction
        return {"Forward": direction == 1, "Reverse": direction == -1}

    def _SELF003(self, i):
        required, run = self.state.get("required", True), self.state.get("run", False)
        if not i["EStopNC"]:
            required, run = True, False
        elif required:
            run = False
            if i["Reset"] and not i["Start"] and not i["Stop"]:
                required = False
        elif i["Stop"]:
            run = False
        elif i["Start"]:
            run = True
        self.state.update(required=required, run=run)
        return {"Run": run, "ResetRequired": required}

    def _SELF004(self, i):
        mode = self.state.get("mode", 0)
        if i["Jam"]:
            mode = 3
        elif i["Reset"]:
            mode = 0
        elif mode == 3:
            pass
        elif i["Stop"]:
            mode = 0
        elif mode == 1 and i["AtExit"]:
            mode = 2
        elif mode == 0 and i["Start"] and not i["AtExit"]:
            mode = 1
        self.state["mode"] = mode
        return {"Belt": mode == 1, "Complete": mode == 2, "Fault": mode == 3}

    def _SELF005(self, i):
        phase, age = self.state.get("phase", 0), self.state.get("age", 0)
        if not i["Enable"]:
            phase, age = 0, 0
        elif i["Tick"]:
            age += 1
            if age >= (2, 3, 1)[phase]:
                phase, age = (phase + 1) % 3, 0
        self.state.update(phase=phase, age=age)
        return {"Red": phase == 0, "Green": phase == 1, "Amber": phase == 2, "Phase": phase}

    def _SELF006(self, i):
        fault = i["HighWet"] and not i["LowWet"]
        fill = self.state.get("fill", False)
        if fault or i["Inhibit"] or i["HighWet"]:
            fill = False
        elif not i["LowWet"]:
            fill = True
        self.state["fill"] = fill
        return {"Fill": fill, "SensorFault": fault}

    def _SELF007(self, i):
        lead_a, served = self.state.get("lead_a", True), self.state.get("served", False)
        previous_demand = self.state.get("demand", False)
        if not i["Demand"]:
            if previous_demand and served:
                lead_a = not lead_a
            served = False
            a = b = False
        else:
            if not previous_demand:
                served = False
            if lead_a:
                a = not i["FaultA"]
                b = i["FaultA"] and not i["FaultB"]
            else:
                b = not i["FaultB"]
                a = i["FaultB"] and not i["FaultA"]
            served = served or a or b
        self.state.update(lead_a=lead_a, served=served, demand=i["Demand"])
        return {"PumpA": a, "PumpB": b, "LeadA": lead_a}

    def _SELF008(self, i):
        preset = i["Preset"]
        if not i["Request"] or i["Trip"] or not 1 <= preset <= 5:
            count = 0
        else:
            count = min(self.state.get("count", 0) + 1, preset)
        self.state["count"] = count
        return {"Ready": count >= preset if 1 <= preset <= 5 else False, "Count": count}

    def _SELF009(self, i):
        count, previous = self.state.get("count", 0), self.state.get("pulse", False)
        error = not 1 <= i["Target"] <= 20
        if error or i["Reset"]:
            count = 0
        else:
            count = min(count + int(i["PartPulse"] and not previous), i["Target"])
        self.state.update(count=count, pulse=i["PartPulse"])
        return {"Count": count, "Complete": not error and not i["Reset"] and count >= i["Target"], "Error": error}

    def _SELF010(self, i):
        latched = self.state.get("latched", False)
        acknowledged = self.state.get("ack", False)
        rise = i["Fault"] and not self.state.get("fault", False)
        if i["Reset"] and not i["Fault"]:
            latched, acknowledged = False, False
        elif i["Fault"]:
            latched = True
            if rise:
                acknowledged = False
            elif i["Ack"]:
                acknowledged = True
        elif latched and i["Ack"]:
            acknowledged = True
        self.state.update(latched=latched, ack=acknowledged, fault=i["Fault"])
        return {"Alarm": latched, "Acknowledged": acknowledged, "Horn": latched and not acknowledged}

    def _SELF011(self, i):
        mode = self.state.get("mode", 0)
        if i["Stop"] or i["Reset"]:
            mode = 0
        elif mode == 0:
            if i["Start"] and i["RetractDone"]:
                mode = 1
        elif mode in (1, 2, 3, 4):
            feedback = ("ExtendDone", "ClampDone", "ReleaseDone", "RetractDone")[mode - 1]
            if i[feedback]:
                mode += 1
        self.state["mode"] = mode
        return {"Extend": mode == 1, "Clamp": mode == 2, "Release": mode == 3,
                "Retract": mode == 4, "Busy": 1 <= mode <= 4, "Done": mode == 5}

    def _SELF012(self, i):
        mode, attempts, free = self.state.get("mode", 0), self.state.get("attempts", 0), self.state.get("free", 0)
        if i["Reset"] and not i["Fault"] and not i["Start"]:
            mode, attempts, free = 0, 0, 0
        elif mode == 3:
            pass
        elif i["Stop"]:
            mode, free = 0, 0
        elif mode == 1 and i["Fault"]:
            mode, free = (2 if attempts < 2 else 3), 0
        elif mode == 2:
            free = 0 if i["Fault"] else free + 1
            if free >= 2:
                attempts += 1
                mode, free = 1, 0
        elif mode == 0 and i["Start"] and not i["Fault"]:
            mode = 1
        self.state.update(mode=mode, attempts=attempts, free=free)
        return {"Run": mode == 1, "Locked": mode == 3, "Attempts": attempts}


def evaluate_reference(task: dict) -> dict:
    """Check expected sequences only; explicitly label the evidence source."""
    cases = []
    for case in task["tests"]:
        controller = ReferenceController(task["id"])
        mismatches = []
        for scan, step in enumerate(case["steps"]):
            actual = controller.step(step["inputs"], step.get("dt_ms"))
            for name, expected in step["expected"].items():
                if name not in actual or actual[name] != expected:
                    mismatches.append({"scan": scan, "output": name, "expected": expected, "oracle": actual.get(name)})
        cases.append({"id": case["id"], "passed": not mismatches, "mismatches": mismatches})
    return {"task_id": task["id"], "evidence": "PYTHON_REFERENCE_ONLY", "cases": cases,
            "passed": all(c["passed"] for c in cases)}
