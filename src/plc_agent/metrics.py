from __future__ import annotations

import math
import random
from collections import Counter
from statistics import mean

from .compiler import final_compile_attempt

BASELINE_MAP = {
    "E3": "E1",
    "E4": "E2",
    "A1": "E1",
    "A2": "E1",
    "A3": "E1",
    "S1": "E1",
    "S2": "E1",
}
STANDARD_CONDITIONS = ("E1", "E2", "E3", "E4", "A1", "A2", "A3", "S1", "S2")


def rate(numerator, denominator):
    return numerator / denominator if denominator else None


def mcnemar_exact(b: int, c: int) -> float:
    """Exact two-sided McNemar binomial test for paired comparison between methods.

    Formula:
        If b + c == 0: return 1.0
        Else: k = min(b, c); n = b + c; p = 2 * sum(comb(n, i) * (0.5 ** n) for i in range(k + 1))
        Cap at 1.0.
    """
    if not isinstance(b, int) or not isinstance(c, int):
        raise TypeError("b and c must be integers")
    if b < 0 or c < 0:
        raise ValueError("b and c must be non-negative integers")
    if b + c == 0:
        return 1.0
    k = min(b, c)
    n = b + c
    p = 2.0 * sum(math.comb(n, i) * (0.5**n) for i in range(k + 1))
    return min(1.0, float(p))


def bootstrap_ci(
    values: list[float],
    n_boot: int = 2000,
    seed: int = 42,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """Computes (1 - alpha) * 100% percentile bootstrap confidence interval of the mean of values."""
    if not values:
        raise ValueError("values cannot be empty")
    rng = random.Random(seed)
    n = len(values)
    boot_means = [sum(rng.choices(values, k=n)) / n for _ in range(n_boot)]
    boot_means.sort()
    low_idx = int((alpha / 2.0) * n_boot)
    high_idx = min(n_boot - 1, int((1.0 - alpha / 2.0) * n_boot))
    return (float(boot_means[low_idx]), float(boot_means[high_idx]))


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


def aggregate(records, planned_tasks, conditions=None):
    seen = [(r["condition"], r["task_id"]) for r in records]
    if len(seen) != len(set(seen)):
        raise ValueError("Duplicate condition-task results; select one preregistered repetition")

    if conditions is None:
        seen_conds = {r["condition"] for r in records}
        # Keep E1..E4 by default for backwards compatibility, plus any other condition present
        conditions = [c for c in STANDARD_CONDITIONS if c in ("E1", "E2", "E3", "E4") or c in seen_conds]
        for c in seen_conds:
            if c not in conditions:
                conditions.append(c)

    all_cond_rows: dict[str, list] = {}
    for r in records:
        all_cond_rows.setdefault(r["condition"], []).append(r)

    out = []
    for condition in conditions:
        rows = all_cond_rows.get(condition, [])
        if len(rows) > planned_tasks:
            raise ValueError("More records than planned task denominator")
        first = sum(r["first_pass_compiled"] is True for r in rows)
        final = sum(r["final_compiled"] is True for r in rows)
        attempted = sum(r["first_pass_compiled"] is not None for r in rows)
        passed_cases = sum(r["functional"]["passed_cases"] for r in rows)
        evaluated_cases = sum(r["functional"]["evaluated_cases"] for r in rows)
        evaluated_tasks = sum(
            r["functional"]["evaluated_cases"] == r["functional"]["planned_cases"]
            and r["functional"]["planned_cases"] > 0
            for r in rows
        )
        task_passes = sum(
            r["functional"]["status"] == "PASS"
            and r["functional"]["planned_cases"] > 0
            and r["functional"]["passed_cases"]
            == r["functional"]["evaluated_cases"]
            == r["functional"]["planned_cases"]
            for r in rows
        )
        usage = [u for r in rows for u in r["usage"] if isinstance(u, dict)]
        totals, usage_coverage = _usage_totals(usage)
        repaired = sum(r["first_pass_compiled"] is False and r["final_compiled"] is True for r in rows)
        initial_fail = sum(r["first_pass_compiled"] is False for r in rows)

        # Verification metrics
        verification_passes = sum(
            r.get("verification", {}).get("verified") is True
            and r.get("verification", {}).get("status") in ("PASS", "VERIFIED")
            for r in rows
        )
        verification_inconclusive = sum(
            isinstance(r.get("verification"), dict) and r["verification"].get("status") == "INCONCLUSIVE" for r in rows
        )
        verification_unsupported = sum(
            isinstance(r.get("verification"), dict) and r["verification"].get("status") == "UNSUPPORTED_ST"
            for r in rows
        )
        verification_eval_rows = [
            r
            for r in rows
            if isinstance(r.get("verification"), dict)
            and r["verification"].get("status") in ("PASS", "VERIFIED", "COUNTEREXAMPLE", "VIOLATION", "FAIL")
        ]
        verification_prop_ratios = []
        for r in verification_eval_rows:
            v = r["verification"]
            ratio = v.get("property_pass_ratio")
            if ratio is None and (v.get("unknown_properties") or 0) == 0:
                total_p = v.get("total_properties") or 0
                passed_p = v.get("passed_properties") or 0
                if total_p > 0:
                    ratio = passed_p / total_p
            if ratio is not None:
                verification_prop_ratios.append(float(ratio))

        # Bootstrap confidence intervals
        comp_vals = [1.0 if r["final_compiled"] is True else 0.0 for r in rows]
        pass_vals = [
            1.0
            if (
                r["functional"]["status"] == "PASS"
                and r["functional"]["planned_cases"] > 0
                and r["functional"]["passed_cases"]
                == r["functional"]["evaluated_cases"]
                == r["functional"]["planned_cases"]
            )
            else 0.0
            for r in rows
        ]
        compilation_ci = bootstrap_ci(comp_vals) if comp_vals else None
        test_pass_ci = bootstrap_ci(pass_vals) if pass_vals else None

        # Paired McNemar tests vs baseline condition
        base_cond = BASELINE_MAP.get(condition)
        mcnemar_p = None
        mcnemar_comp_p = None
        if base_cond and base_cond in all_cond_rows:
            base_rows = all_cond_rows[base_cond]
            c_map = {
                r["task_id"]: (
                    r["functional"]["status"] == "PASS"
                    and r["functional"]["planned_cases"] > 0
                    and r["functional"]["passed_cases"]
                    == r["functional"]["evaluated_cases"]
                    == r["functional"]["planned_cases"]
                )
                for r in rows
            }
            b_map = {
                r["task_id"]: (
                    r["functional"]["status"] == "PASS"
                    and r["functional"]["planned_cases"] > 0
                    and r["functional"]["passed_cases"]
                    == r["functional"]["evaluated_cases"]
                    == r["functional"]["planned_cases"]
                )
                for r in base_rows
            }
            shared = set(c_map.keys()) & set(b_map.keys())
            if shared:
                b_disc = sum(c_map[t] and not b_map[t] for t in shared)
                c_disc = sum(not c_map[t] and b_map[t] for t in shared)
                mcnemar_p = mcnemar_exact(b_disc, c_disc)

            c_comp_map = {r["task_id"]: bool(r.get("final_compiled")) for r in rows}
            b_comp_map = {r["task_id"]: bool(r.get("final_compiled")) for r in base_rows}
            shared_comp = set(c_comp_map.keys()) & set(b_comp_map.keys())
            if shared_comp:
                b_comp_disc = sum(c_comp_map[t] and not b_comp_map[t] for t in shared_comp)
                c_comp_disc = sum(not c_comp_map[t] and b_comp_map[t] for t in shared_comp)
                mcnemar_comp_p = mcnemar_exact(b_comp_disc, c_comp_disc)

        cost_total = (
            sum(r["api_cost"] for r in rows) if rows and all(r.get("api_cost") is not None for r in rows) else None
        )
        ver_status_counter: Counter[str] = Counter()
        for r in rows:
            vcounts = r.get("verification_status_counts")
            if isinstance(vcounts, dict) and vcounts:
                for k, v in vcounts.items():
                    if isinstance(v, int):
                        ver_status_counter[str(k)] += v
            elif isinstance(r.get("verification"), dict) and r["verification"].get("status"):
                ver_status_counter[str(r["verification"]["status"])] += 1
        total_ratchet_rollbacks = sum(int(r.get("ratchet_rollbacks") or 0) for r in rows)
        selftest_rejection_count = sum(
            len(r.get("selftest_rejected") or []) for r in rows if isinstance(r.get("selftest_rejected"), list)
        )

        out.append(
            {
                "condition": condition,
                "planned_tasks": planned_tasks,
                "recorded_tasks": len(rows),
                "status_counts": dict(Counter(r["status"] for r in rows)),
                "actual_first_compilations": attempted,
                "first_pass_compiled_tasks": first,
                "final_compiled_tasks": final,
                # A planned campaign has no measured rate until at least one real compiler evaluation.
                "first_pass_compilation_rate": rate(first, planned_tasks) if attempted else None,
                "final_compilation_rate": rate(final, planned_tasks) if attempted else None,
                "compilation_rate_ci": compilation_ci,
                "first_pass_rate_among_evaluated": rate(first, attempted),
                "compiler_coverage": rate(attempted, planned_tasks),
                "campaign_complete": len(rows) == planned_tasks and attempted == planned_tasks,
                "repair_successes": repaired,
                "repair_effectiveness": rate(repaired, initial_fail),
                "passed_cases": passed_cases,
                "evaluated_cases": evaluated_cases,
                "test_case_pass_rate": rate(passed_cases, evaluated_cases),
                "passed_tasks": task_passes,
                "fully_evaluated_tasks": evaluated_tasks,
                "test_task_pass_rate": rate(task_passes, evaluated_tasks),
                "test_task_pass_rate_ci": test_pass_ci,
                "functional_task_coverage": rate(evaluated_tasks, planned_tasks),
                "verification_passed_tasks": verification_passes,
                "verification_evaluated_tasks": len(verification_eval_rows),
                "verification_inconclusive_tasks": verification_inconclusive,
                "verification_unsupported_tasks": verification_unsupported,
                "verification_pass_rate": rate(verification_passes, planned_tasks) if attempted else None,
                "verification_pass_rate_among_evaluated": rate(verification_passes, len(verification_eval_rows)),
                "mean_property_pass_ratio": mean(verification_prop_ratios) if verification_prop_ratios else None,
                "verification_status_counts": dict(ver_status_counter),
                "total_ratchet_rollbacks": total_ratchet_rollbacks,
                "selftest_rejection_count": selftest_rejection_count,
                "mcnemar_p_value_vs_baseline": mcnemar_p,
                "mcnemar_compilation_p_value_vs_baseline": mcnemar_comp_p,
                "compiler_call_count": sum(len(r["compilation_attempts"]) for r in rows),
                "reported_tool_call_count": _reported_sum(rows, "tool_call_count"),
                "reported_llm_call_count": _reported_sum(rows, "llm_calls"),
                "mean_elapsed_seconds": mean(r["elapsed_seconds"] for r in rows if r["status"] != "NOT_RUN")
                if any(r["status"] != "NOT_RUN" for r in rows)
                else None,
                "token_usage_reported_calls": len(usage),
                "reported_tokens": totals if usage else None,
                "mean_tokens_per_task": rate(totals["total_tokens"], len(rows))
                if totals.get("total_tokens") is not None
                else None,
                "token_usage_field_reported_records": usage_coverage,
                "token_usage_reporting_unit": "provider usage records; a Codex turn record can aggregate several internal model calls",
                "api_cost": cost_total,
                "mean_cost_per_task": rate(cost_total, len(rows)) if cost_total is not None else None,
            }
        )
    return out


def audit_records(records):
    errors = []
    for row in records:
        attempts = row["compilation_attempts"]
        valid = [a for a in attempts if a["status"] in ("PASS", "COMPILE_FAIL")]
        if row["first_pass_compiled"] is not None and (
            not attempts
            or attempts[0]["status"] not in ("PASS", "COMPILE_FAIL")
            or attempts[0]["success"] != row["first_pass_compiled"]
        ):
            errors.append(f"{row['condition']}/{row['task_id']}: first-pass mismatch")
        if row["final_compiled"] is True:
            if not any(a["success"] for a in valid):
                errors.append(f"{row['condition']}/{row['task_id']}: no successful compiler evidence")
            else:
                try:
                    final_compile_attempt(row)
                except ValueError as exc:
                    errors.append(f"{row['condition']}/{row['task_id']}: {exc}")
        f = row["functional"]
        if not 0 <= f["passed_cases"] <= f["evaluated_cases"] <= f["planned_cases"]:
            errors.append(f"{row['condition']}/{row['task_id']}: invalid test counts")
        if not 0 <= f["passed_steps"] <= f["evaluated_steps"]:
            errors.append(f"{row['condition']}/{row['task_id']}: invalid test-step counts")
        if f["evaluated_cases"] and f["evidence"] not in ("CODESYS_SIMULATION", "CODESYS_RUNTIME"):
            errors.append(f"{row['condition']}/{row['task_id']}: non-CODESYS functional evidence")
        if f["status"] == "PASS" and not (
            f["planned_cases"] > 0 and f["passed_cases"] == f["evaluated_cases"] == f["planned_cases"]
        ):
            errors.append(f"{row['condition']}/{row['task_id']}: functional PASS requires every planned case to pass")
    return errors
