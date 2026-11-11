from __future__ import annotations

import copy
import math
from typing import Any


def validate_self_tests(
    task_view: dict[str, Any],
    raw_cases: list[dict[str, Any]],
    max_cases: int = 5,
    max_steps_per_case: int = 20,
    max_total_dt_ms: int = 60000,
) -> list[dict[str, Any]]:
    """Validate and sanitize agent-generated self-test cases against the task view interface and budget."""
    if max_cases <= 0 or max_steps_per_case <= 0 or max_total_dt_ms < 0:
        return []
    if not isinstance(raw_cases, list):
        return []

    declared_inputs_exact: set[str] = set()
    declared_inputs_ci: dict[str, str] = {}
    declared_outputs_exact: set[str] = set()
    declared_outputs_ci: dict[str, str] = {}

    for var in task_view.get("interface", []):
        name = var.get("name")
        if not name or not isinstance(name, str):
            continue
        direction = var.get("direction")
        if direction is None:
            is_in = True
            is_out = True
        else:
            is_in = direction in ("INPUT", "IN_OUT")
            is_out = direction in ("OUTPUT", "IN_OUT")

        if is_in:
            declared_inputs_exact.add(name)
            declared_inputs_ci[name.casefold()] = name
        if is_out:
            declared_outputs_exact.add(name)
            declared_outputs_ci[name.casefold()] = name

    valid_cases: list[dict[str, Any]] = []
    cumulative_dt: int = 0

    for case in raw_cases:
        if not isinstance(case, dict):
            continue
        steps = case.get("steps")
        if not isinstance(steps, list) or len(steps) == 0:
            continue

        case_valid = True
        for step in steps:
            if not isinstance(step, dict):
                case_valid = False
                break

            inputs = step.get("inputs", {})
            if not isinstance(inputs, dict):
                case_valid = False
                break
            for k in inputs.keys():
                if not isinstance(k, str):
                    case_valid = False
                    break
                if k not in declared_inputs_exact and k.casefold() not in declared_inputs_ci:
                    case_valid = False
                    break
            if not case_valid:
                break

            expected = step.get("expected", {})
            if not isinstance(expected, dict):
                case_valid = False
                break
            for k in expected.keys():
                if not isinstance(k, str):
                    case_valid = False
                    break
                if k not in declared_outputs_exact and k.casefold() not in declared_outputs_ci:
                    case_valid = False
                    break
            if not case_valid:
                break

            if "dt_ms" in step:
                dt = step["dt_ms"]
                if isinstance(dt, bool) or not isinstance(dt, (int, float)):
                    case_valid = False
                    break
                if not math.isfinite(dt) or dt < 0:
                    case_valid = False
                    break

        if not case_valid:
            continue

        accepted_steps: list[dict[str, Any]] = []
        for step in steps[:max_steps_per_case]:
            raw_dt = step.get("dt_ms", 0)
            step_dt_int = int(raw_dt) if isinstance(raw_dt, (int, float)) else 0

            if cumulative_dt + step_dt_int <= max_total_dt_ms:
                norm_inputs = {
                    declared_inputs_ci.get(k.casefold(), k): copy.deepcopy(v)
                    for k, v in step.get("inputs", {}).items()
                }
                norm_expected = {
                    declared_outputs_ci.get(k.casefold(), k): copy.deepcopy(v)
                    for k, v in step.get("expected", {}).items()
                }
                new_step: dict[str, Any] = {
                    "inputs": norm_inputs,
                    "expected": norm_expected,
                }
                if "dt_ms" in step:
                    new_step["dt_ms"] = step_dt_int
                accepted_steps.append(new_step)
                cumulative_dt += step_dt_int
            else:
                break

        if not accepted_steps:
            continue

        sanitized_case: dict[str, Any] = {
            "id": case.get("id", f"case_{len(valid_cases) + 1}"),
            "steps": accepted_steps,
        }
        if "purpose" in case:
            sanitized_case["purpose"] = case["purpose"]

        valid_cases.append(sanitized_case)
        if len(valid_cases) >= max_cases:
            break

    return valid_cases
