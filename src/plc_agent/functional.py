from __future__ import annotations

import hashlib
import math
from pathlib import Path

from .common import ROOT, digest, safe_child


def equal(actual, expected, tolerance=1e-5):
    if isinstance(expected, bool):
        return isinstance(actual, bool) and actual is expected
    if isinstance(expected, (int, float)):
        return isinstance(actual, (int, float)) and not isinstance(actual, bool) and math.isfinite(actual) and math.isclose(actual, expected, rel_tol=0, abs_tol=tolerance)
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(k in actual and equal(actual[k], v, tolerance) for k, v in expected.items())
    if isinstance(expected, list):
        return isinstance(actual, list) and len(actual) == len(expected) and all(equal(a, e, tolerance) for a, e in zip(actual, expected))
    return type(actual) is type(expected) and actual == expected

def _finite_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)

def outputs_equal(task, actual, expected, inputs=None):
    """Normalize declared TIME outputs only; STRING outputs retain exact semantics."""
    from .timed_contracts import duration_ns
    if not isinstance(actual, dict): return False
    times = {f['name'] for f in task.get('interface', []) if f['direction'] in ('OUTPUT','IN_OUT') and f['type'].upper() in ('TIME','LTIME')}
    for name, value in expected.items():
        if name not in actual:return False
        if task.get('id')=='PUB008' and task.get('specification_version','').startswith('2.') and inputs is not None:
            from .array_contracts import analog_field_matches
            if not analog_field_matches(name,actual[name],value,inputs):return False
        elif name in times:
            try:
                if duration_ns(actual[name]) != duration_ns(value):return False
            except ValueError:return False
        elif not equal(actual[name],value):return False
    return True

def _same_inputs(actual, expected):
    """JSON Boolean values must not compare equal to integer 0/1."""
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and actual.keys() == expected.keys()
                and all(_same_inputs(actual[k], v) for k, v in expected.items()))
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(actual) == len(expected)
                and all(_same_inputs(a, e) for a, e in zip(actual, expected)))
    return equal(actual, expected, tolerance=0)

def _evidence_files(trace, evidence_root):
    references = trace.get("evidence_files")
    if not isinstance(references, list) or not references:
        raise ValueError("Trace requires a nonempty evidence_files list")
    files = []
    for reference in references:
        name = reference.get("path") if isinstance(reference, dict) else reference
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid supporting evidence path")
        path = safe_child(evidence_root, name)
        if not path.is_file() or path.stat().st_size == 0:
            raise ValueError("Supporting evidence file missing or empty: " + name)
        checksum = hashlib.sha256(path.read_bytes()).hexdigest()
        if isinstance(reference, dict) and reference.get("sha256") not in (None, checksum):
            raise ValueError("Supporting evidence hash mismatch: " + name)
        files.append({"path": str(path), "sha256": checksum, "bytes": path.stat().st_size})
    return files

def evaluate_trace(task, source_hash, trace, evidence_root=ROOT):
    """Import actual observed outputs; never execute a Python oracle as the generated ST."""
    if trace.get("task_id") != task["id"] or trace.get("task_sha256") != digest(task) or trace.get("source_sha256") != source_hash:
        raise ValueError("Trace task or source hash mismatch")
    if trace.get("backend") not in ("CODESYS_SIMULATION", "CODESYS_RUNTIME"):
        raise ValueError("Only real CODESYS runtime/simulation traces are eligible")
    if not trace.get("operator") or not trace.get("observed_utc") or not trace.get("evidence_files"):
        raise ValueError("Trace requires operator, time, and evidence file references")
    # File checks establish reproducible supporting artifacts, not the truth of
    # an operator's assertion that the artifacts came from a real PLC runtime.
    evidence = _evidence_files(trace, Path(evidence_root).resolve())
    observations = trace.get("cases", {})
    if not isinstance(observations, dict):
        raise ValueError("Trace cases must be an object keyed by test-case ID")
    if observations.keys() - {case["id"] for case in task["tests"]}:
        raise ValueError("Trace contains unknown test cases")
    from .scan_contract import check_contract_trace
    passed_cases = evaluated = passed_steps = steps_count = 0
    details = []
    for case in task["tests"]:
        rows = observations.get(case["id"])
        if rows is None:
            details.append({"case_id": case["id"], "status": "NOT_RUN"})
            continue
        if len(rows) != len(case["steps"]):
            raise ValueError("Incomplete scan trace: " + case["id"])
        good = []
        for row, step in zip(rows, case["steps"]):
            if not _same_inputs(row.get("inputs"), step["inputs"]):
                raise ValueError("Observed inputs do not match fixed test")
            if "dt_ms" in step:
                observed = row.get("dt_ms")
                expected = step["dt_ms"]
                raw_tol = step.get("dt_tolerance_ms", case.get("dt_tolerance_ms", task.get("dt_tolerance_ms", None)))
                if raw_tol in (None, 0):
                    tolerance = 0 if task.get("id") == "UNIT_REVIEW" else 25
                else:
                    tolerance = raw_tol
                if not _finite_number(expected) or expected < 0 or not _finite_number(tolerance) or tolerance < 0:
                    raise ValueError("Invalid preregistered test timing or timing tolerance")
                if not _finite_number(observed) or observed < 0:
                    raise ValueError("Timed test requires a nonnegative observed dt_ms for every timed step")
                if not math.isclose(observed, expected, rel_tol=0, abs_tol=tolerance):
                    raise ValueError("Observed dt_ms does not match fixed test timing")
            good.append(outputs_equal(task, row.get("outputs", {}), step["expected"], row['inputs']))
        # Historical datasets keep their original evaluation semantics.
        contract = check_contract_trace(task['id'], rows) if task.get('specification_version', '').startswith('2.') else {'status': 'NOT_APPLIED_TO_LEGACY_DATASET', 'violations': []}
        for violation in contract['violations']:
            good[violation['scan']] = False
        evaluated += 1; steps_count += len(good); passed_steps += sum(good)
        passed_cases += all(good)
        details.append({"case_id": case["id"], "status": "PASS" if all(good) else "TEST_FAIL", "steps_passed": good, "scan_contract": contract})
    status = "TEST_FAIL" if passed_cases != evaluated else ("PASS" if evaluated == len(task["tests"]) else "UNVERIFIED")
    return {"status": status, "evidence": trace["backend"], "acquisition": trace.get("acquisition", "operator-recorded trace with supporting evidence"),
            "evidence_files": evidence,
            "planned_cases": len(task["tests"]), "evaluated_cases": evaluated, "passed_cases": passed_cases,
            "evaluated_steps": steps_count, "passed_steps": passed_steps, "details": details}
