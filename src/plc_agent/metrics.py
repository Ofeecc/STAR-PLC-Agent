from __future__ import annotations
from collections import Counter
from statistics import mean

def rate(numerator, denominator):
    return numerator / denominator if denominator else None

def _usage_number(value):
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None

def _usage_totals(usage):
    """Do not turn an unreported usage field into zero tokens."""
    values = {key: [] for key in ("input_tokens", "output_tokens", "total_tokens")}
    for entry in usage:
        incoming = _usage_number(entry.get("input_tokens"))
        outgoing = _usage_number(entry.get("output_tokens"))
        total = _usage_number(entry.get("total_tokens"))
        if total is None and incoming is not None and outgoing is not None:
            total = incoming + outgoing
        for key, value in (("input_tokens", incoming), ("output_tokens", outgoing), ("total_tokens", total)):
            values[key].append(value)
    totals = {key: sum(items) if items and all(x is not None for x in items) else None for key, items in values.items()}
    coverage = {key: sum(x is not None for x in items) for key, items in values.items()}
    return totals, coverage

def _reported_sum(rows, key):
    values = [row.get(key) for row in rows]
    return sum(values) if values and all(_usage_number(v) is not None for v in values) else None

def aggregate(records, planned_tasks):
    seen = [(r["condition"], r["task_id"]) for r in records]
    if len(seen) != len(set(seen)):
        raise ValueError("Duplicate condition-task results; select one preregistered repetition")
    out = []
    for condition in ("E1", "E2", "E3", "E4"):
        rows = [r for r in records if r["condition"] == condition]
        if len(rows) > planned_tasks:
            raise ValueError("More records than planned task denominator")
        first = sum(r["first_pass_compiled"] is True for r in rows)
        final = sum(r["final_compiled"] is True for r in rows)
        attempted = sum(r["first_pass_compiled"] is not None for r in rows)
        passed_cases = sum(r["functional"]["passed_cases"] for r in rows)
        evaluated_cases = sum(r["functional"]["evaluated_cases"] for r in rows)
        evaluated_tasks = sum(r["functional"]["evaluated_cases"] == r["functional"]["planned_cases"] and r["functional"]["planned_cases"] > 0 for r in rows)
        task_passes = sum(r["functional"]["status"] == "PASS" and r["functional"]["planned_cases"] > 0
                          and r["functional"]["passed_cases"] == r["functional"]["evaluated_cases"] == r["functional"]["planned_cases"] for r in rows)
        usage = [u for r in rows for u in r["usage"] if isinstance(u, dict)]
        totals, usage_coverage = _usage_totals(usage)
        repaired = sum(r["first_pass_compiled"] is False and r["final_compiled"] is True for r in rows)
        initial_fail = sum(r["first_pass_compiled"] is False for r in rows)
        out.append({"condition": condition, "planned_tasks": planned_tasks, "recorded_tasks": len(rows),
            "status_counts": dict(Counter(r["status"] for r in rows)), "actual_first_compilations": attempted,
            "first_pass_compiled_tasks": first, "final_compiled_tasks": final,
            # A planned campaign has no measured rate until at least one real compiler evaluation.
            "first_pass_compilation_rate": rate(first, planned_tasks) if attempted else None,
            "final_compilation_rate": rate(final, planned_tasks) if attempted else None,
            "first_pass_rate_among_evaluated": rate(first, attempted),
            "compiler_coverage": rate(attempted, planned_tasks),
            "campaign_complete": len(rows) == planned_tasks and attempted == planned_tasks,
            "repair_successes": repaired, "repair_effectiveness": rate(repaired, initial_fail),
            "passed_cases": passed_cases, "evaluated_cases": evaluated_cases,
            "test_case_pass_rate": rate(passed_cases, evaluated_cases), "passed_tasks": task_passes,
            "fully_evaluated_tasks": evaluated_tasks, "test_task_pass_rate": rate(task_passes, evaluated_tasks),
            "functional_task_coverage": rate(evaluated_tasks, planned_tasks),
            "compiler_call_count": sum(len(r["compilation_attempts"]) for r in rows),
            "reported_tool_call_count": _reported_sum(rows, "tool_call_count"),
            "reported_llm_call_count": _reported_sum(rows, "llm_calls"),
            "mean_elapsed_seconds": mean(r["elapsed_seconds"] for r in rows if r["status"] != "NOT_RUN") if any(r["status"] != "NOT_RUN" for r in rows) else None,
            "token_usage_reported_calls": len(usage), "reported_tokens": totals if usage else None,
            "token_usage_field_reported_records": usage_coverage,
            "token_usage_reporting_unit": "provider usage records; a Codex turn record can aggregate several internal model calls",
            "api_cost": sum(r["api_cost"] for r in rows) if rows and all(r["api_cost"] is not None for r in rows) else None})
    return out

def audit_records(records):
    errors = []
    for row in records:
        attempts = row["compilation_attempts"]
        valid = [a for a in attempts if a["status"] in ("PASS", "COMPILE_FAIL")]
        if row["first_pass_compiled"] is not None and (not attempts or attempts[0]["status"] not in ("PASS", "COMPILE_FAIL")
                                                      or attempts[0]["success"] != row["first_pass_compiled"]):
            errors.append(f"{row['condition']}/{row['task_id']}: first-pass mismatch")
        if row["final_compiled"] is True and not any(a["success"] for a in valid):
            errors.append(f"{row['condition']}/{row['task_id']}: no successful compiler evidence")
        if row["final_compiled"] is True and attempts and (attempts[-1]["status"] != "PASS" or not attempts[-1]["success"]):
            errors.append(f"{row['condition']}/{row['task_id']}: final candidate does not match last compiler outcome")
        f = row["functional"]
        if not 0 <= f["passed_cases"] <= f["evaluated_cases"] <= f["planned_cases"]:
            errors.append(f"{row['condition']}/{row['task_id']}: invalid test counts")
        if not 0 <= f["passed_steps"] <= f["evaluated_steps"]:
            errors.append(f"{row['condition']}/{row['task_id']}: invalid test-step counts")
        if f["evaluated_cases"] and f["evidence"] not in ("CODESYS_SIMULATION", "CODESYS_RUNTIME"):
            errors.append(f"{row['condition']}/{row['task_id']}: non-CODESYS functional evidence")
        if f["status"] == "PASS" and not (f["planned_cases"] > 0 and f["passed_cases"] == f["evaluated_cases"] == f["planned_cases"]):
            errors.append(f"{row['condition']}/{row['task_id']}: functional PASS requires every planned case to pass")
    return errors
