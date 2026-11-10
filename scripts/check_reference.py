"""Finite reference-model safety exploration, not generated ST verification.

The independently stated predicates below are checked over every reachable
state and every input valuation in the finite SELF task domains. This validates
the Python reference model and selected properties; it does not implement an
LTL model checker and does not prove that any generated ST obeys the properties.
"""
from __future__ import annotations

import itertools
import json
import platform
import sys
from collections import deque
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from plc_agent.reference import ReferenceController, evaluate_reference


def valuations(task):
    inputs = [v for v in task["interface"] if v["direction"] == "INPUT"]
    domains = []
    for var in inputs:
        if var["type"] == "BOOL":
            domains.append((False, True))
        elif var["name"] == "Preset":
            domains.append(tuple(range(7)))
        elif var["name"] == "Target":
            domains.append(tuple(range(22)))
        else:
            raise ValueError("No finite review domain for " + var["name"])
    return [dict(zip([v["name"] for v in inputs], row)) for row in itertools.product(*domains)]


def safety(task_id, q, i, o):
    """Selected requirement predicates, independent of transition implementation."""
    checks = {}
    if task_id == "SELF001":
        checks["stop_guard_priority"] = not (i["Stop"] or not i["GuardClosed"]) or not o["Run"]
        checks["permitted_start"] = not (i["Start"] and not i["Stop"] and i["GuardClosed"]) or o["Run"]
    elif task_id == "SELF002":
        checks["mutual_exclusion"] = not (o["Forward"] and o["Reverse"])
        checks["neutral_on_reversal"] = not ((q.get("direction", 0) == 1 and i["ReverseButton"] and not i["ForwardButton"]) or
                                                    (q.get("direction", 0) == -1 and i["ForwardButton"] and not i["ReverseButton"])) or not (o["Forward"] or o["Reverse"])
        checks["ambiguous_or_stop_is_neutral"] = not (i["Stop"] or i["ForwardButton"] == i["ReverseButton"]) or not (o["Forward"] or o["Reverse"])
    elif task_id == "SELF003":
        checks["estop_priority"] = i["EStopNC"] or (not o["Run"] and o["ResetRequired"])
        checks["inhibited_scan_cannot_start"] = not q.get("required", True) or not o["Run"]
        checks["reset_cannot_overlap_start"] = not (q.get("required", True) and i["Start"]) or o["ResetRequired"]
        checks["stop_priority"] = not i["Stop"] or not o["Run"]
    elif task_id == "SELF004":
        checks["jam_priority"] = not i["Jam"] or (o["Fault"] and not o["Belt"] and not o["Complete"])
        checks["latched_fault"] = not (q.get("mode", 0) == 3 and not i["Reset"]) or o["Fault"]
        checks["output_exclusion"] = sum(o.values()) <= 1
    elif task_id == "SELF005":
        checks["one_hot"] = sum(o[n] for n in ("Red", "Green", "Amber")) == 1
        checks["phase_encoding"] = o[("Red", "Green", "Amber")[o["Phase"]]]
        checks["disable_red"] = i["Enable"] or (o["Red"] and o["Phase"] == 0)
        checks["pause"] = not (i["Enable"] and not i["Tick"]) or o["Phase"] == q.get("phase", 0)
    elif task_id == "SELF006":
        checks["exact_sensor_fault"] = o["SensorFault"] == (i["HighWet"] and not i["LowWet"])
        checks["inhibit_full_fault_stop"] = not (i["Inhibit"] or i["HighWet"] or o["SensorFault"]) or not o["Fill"]
        checks["middle_retention"] = not (i["LowWet"] and not i["HighWet"] and not i["Inhibit"]) or o["Fill"] == q.get("fill", False)
    elif task_id == "SELF007":
        checks["mutual_exclusion"] = not (o["PumpA"] and o["PumpB"])
        checks["fault_demand_priority"] = not ((i["FaultA"] or not i["Demand"]) and o["PumpA"]) and not ((i["FaultB"] or not i["Demand"]) and o["PumpB"])
        checks["available_pump_serves_demand"] = not (i["Demand"] and not (i["FaultA"] and i["FaultB"])) or (o["PumpA"] or o["PumpB"])
        toggle_due = q.get("demand", False) and not i["Demand"] and q.get("served", False)
        checks["episode_alternation"] = o["LeadA"] == (not q.get("lead_a", True) if toggle_due else q.get("lead_a", True))
    elif task_id == "SELF008":
        valid = 1 <= i["Preset"] <= 5
        healthy = valid and i["Request"] and not i["Trip"]
        checks["interruption_clears"] = healthy or (o["Count"] == 0 and not o["Ready"])
        checks["ready_threshold"] = o["Ready"] == (valid and o["Count"] >= i["Preset"])
        checks["count_bound"] = 0 <= o["Count"] <= (i["Preset"] if valid else 0)
    elif task_id == "SELF009":
        valid = 1 <= i["Target"] <= 20
        checks["exact_validation"] = o["Error"] == (not valid)
        checks["reset_and_invalid_clear"] = not (i["Reset"] or not valid) or (o["Count"] == 0 and not o["Complete"])
        checks["count_bounds"] = 0 <= o["Count"] <= (i["Target"] if valid else 0)
        checks["complete_threshold"] = o["Complete"] == (valid and not i["Reset"] and o["Count"] >= i["Target"])
        checks["held_pulse_cannot_increment"] = not (q.get("pulse", False) and i["PartPulse"]) or o["Count"] <= q.get("count", 0)
    elif task_id == "SELF010":
        checks["horn_encoding"] = o["Horn"] == (o["Alarm"] and not o["Acknowledged"])
        checks["present_fault_latches"] = not i["Fault"] or o["Alarm"]
        checks["new_event_reannunciates"] = not (i["Fault"] and not q.get("fault", False)) or (o["Horn"] and not o["Acknowledged"])
        checks["clear_reset"] = not (i["Reset"] and not i["Fault"]) or not any(o.values())
    elif task_id == "SELF011":
        commands = sum(o[n] for n in ("Extend", "Clamp", "Release", "Retract"))
        checks["one_action"] = commands <= 1
        checks["busy_encoding"] = o["Busy"] == (commands == 1)
        checks["abort"] = not (i["Stop"] or i["Reset"]) or not any(o.values())
        checks["done_holds"] = not (q.get("mode", 0) == 5 and not i["Stop"] and not i["Reset"]) or o["Done"]
    elif task_id == "SELF012":
        valid_reset = i["Reset"] and not i["Fault"] and not i["Start"]
        checks["fault_stops"] = not i["Fault"] or not o["Run"]
        checks["retry_bound"] = 0 <= o["Attempts"] <= 2
        checks["lockout_retention"] = not (q.get("mode", 0) == 3 and not valid_reset) or (o["Locked"] and not o["Run"])
        checks["valid_reset"] = not valid_reset or (not o["Run"] and not o["Locked"] and o["Attempts"] == 0)
        checks["stop_stops"] = not i["Stop"] or not o["Run"]
    return checks


def explore(task):
    controller = ReferenceController(task["id"])
    initial_state = deepcopy(controller.state)
    pending = deque([initial_state])
    seen = {json.dumps(initial_state, sort_keys=True)}
    inputs = valuations(task)
    transitions = 0
    counts = {}
    failures = []
    while pending:
        q = pending.popleft()
        for i in inputs:
            controller.state = deepcopy(q)
            o = controller.step(i)
            for name, ok in safety(task["id"], q, i, o).items():
                counts[name] = counts.get(name, 0) + 1
                if not ok:
                    failures.append(dict(property=name, pre_state=q, inputs=i, outputs=o))
            next_state = deepcopy(controller.state)
            key = json.dumps(next_state, sort_keys=True)
            if key not in seen:
                seen.add(key)
                pending.append(next_state)
            transitions += 1
            if len(seen) > 10000:
                raise RuntimeError("Unexpected unbounded reference state")
    return dict(task_id=task["id"], reachable_state_encodings=len(seen), input_valuations=len(inputs),
                transitions=transitions, checked_properties=counts, passed=not failures, failures=failures,
                numeric_domain_note="BOOL exhaustively enumerated; Preset 0..6 and Target 0..21 cover valid ranges and adjacent invalid boundaries. Larger USINT invalid values are represented by the invalid-class boundaries, not exhaustively enumerated.")


def main():
    tasks = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "dataset/self_built").glob("SELF*.json"))]
    traces = [evaluate_reference(task) for task in tasks]
    exploration = [explore(task) for task in tasks]
    result = dict(evidence="PYTHON_REFERENCE_ONLY", generated_utc=datetime.now(timezone.utc).isoformat(),
                  interpreter=sys.executable, python_version=platform.python_version(), task_count=len(tasks),
                  test_cases=sum(len(t["tests"]) for t in tasks),
                  scan_observations=sum(len(c["steps"]) for t in tasks for c in t["tests"]),
                  reference_traces=traces, finite_safety_exploration=exploration,
                  passed=all(t["passed"] for t in traces) and all(e["passed"] for e in exploration),
                  limitation="No ST interpreter, real CODESYS compiler, PLC runtime or unbounded LTL model checker was invoked by this reference review. Exclude all counts here from PLC functional success metrics.")
    target = ROOT / "results/summary/reference_validation.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("evidence", "task_count", "test_cases", "scan_observations", "passed")}, indent=2))
    print("Explored transitions:", sum(x["transitions"] for x in exploration))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
