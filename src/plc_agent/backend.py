"""Backend abstraction for CODESYS compilation and simulation.

Supports real CODESYS execution via CodesysBackend and fast deterministic
testing via FakeBackend with failure truncation to the first diverging scan step.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Protocol, runtime_checkable

from .common import digest, read_json
from .compiler import CompileResult, compile_st, normalize_candidate, verify_interface_signature
from .config import Settings
from .functional import equal, outputs_equal
from .normalized_spec import reference_step
from .scan_contract import ScanContract
from .simulation import run_functional


@dataclass
class SimCaseFailure:
    case_id: str
    first_bad_step: int
    field: str
    expected: object
    observed: object
    inputs_prefix: list[dict]
    step_window: list[dict] = field(default_factory=list)


@dataclass
class SimResult:
    status: str
    passed_cases: int
    evaluated_cases: int
    failures: list[SimCaseFailure]
    infrastructure_error: str | None = None
    raw: dict | None = None


@runtime_checkable
class Backend(Protocol):
    def compile(self, task: dict, candidate: dict | str, workspace: Path) -> CompileResult:
        """Compile candidate ST code for task in workspace."""
        ...

    def simulate(self, task: dict, candidate: dict | str, cases: list[dict], workspace: Path) -> SimResult:
        """Simulate candidate against test cases in workspace."""
        ...


def find_first_mismatch(
    task: dict,
    actual: Any,
    expected: dict,
    inputs: dict | None = None,
) -> tuple[str, Any, Any] | None:
    """Find the first output field that diverges from expected, returning (field, expected, observed)."""
    if not isinstance(actual, dict):
        first_key = next(iter(expected.keys())) if expected else ""
        return (first_key, expected.get(first_key), actual)

    times = {
        f["name"]
        for f in task.get("interface", [])
        if f.get("direction") in ("OUTPUT", "IN_OUT") and f.get("type", "").upper() in ("TIME", "LTIME")
    }

    for name, exp_val in expected.items():
        if name not in actual:
            return (name, exp_val, None)
        act_val = actual[name]
        if (
            task.get("id") == "PUB008"
            and task.get("specification_version", "").startswith(("normalized", "2."))
            and inputs is not None
        ):
            from .array_contracts import analog_field_matches

            if not analog_field_matches(name, act_val, exp_val, inputs):
                return (name, exp_val, act_val)
        elif name in times:
            from .timed_contracts import duration_ns

            try:
                if duration_ns(act_val) != duration_ns(exp_val):
                    return (name, exp_val, act_val)
            except (ValueError, TypeError):
                return (name, exp_val, act_val)
        elif not equal(act_val, exp_val):
            return (name, exp_val, act_val)

    return None


def _call_step_fn(step_fn: Callable, inputs: dict, dt_ms: int | float | None = None) -> Any:
    """Invoke step_fn with inputs and optional dt_ms."""
    try:
        return step_fn(inputs, dt_ms=dt_ms)
    except TypeError:
        try:
            return step_fn(inputs, dt_ms)
        except TypeError:
            return step_fn(inputs)


def _call_compile_fn(compile_fn: Callable, task: dict, candidate: dict | str, workspace: Path) -> CompileResult:
    """Invoke compile_fn with flexible parameter shapes."""
    try:
        res = compile_fn(task, candidate, workspace)
    except TypeError:
        try:
            res = compile_fn(candidate, workspace)
        except TypeError:
            try:
                res = compile_fn(candidate)
            except TypeError:
                res = compile_fn()

    if isinstance(res, CompileResult):
        return res
    if isinstance(res, dict):
        return CompileResult(**res)
    return CompileResult(status="PASS", success=True, backend="FAKE")


class CodesysBackend:
    """Real CODESYS IDE compiler and simulation backend."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings.load()

    def compile(self, task: dict, candidate: dict | str, workspace: Path) -> CompileResult:
        ws = Path(workspace)
        return compile_st(task, candidate, ws, self.settings)

    def simulate(self, task: dict, candidate: dict | str, cases: list[dict], workspace: Path) -> SimResult:
        ws = Path(workspace)
        cand_norm = normalize_candidate(candidate)
        source_hash = digest(cand_norm)

        raw = run_functional(task, candidate, source_hash, ws, self.settings, cases=cases)
        status = raw.get("status", "UNVERIFIED")
        infra_error = raw.get("reason") or raw.get("infrastructure_error")

        if status in ("TOOL_ERROR", "TIMEOUT", "UNVERIFIED"):
            return SimResult(
                status=status,
                passed_cases=0,
                evaluated_cases=0,
                failures=[],
                infrastructure_error=infra_error,
                raw=raw,
            )

        functional = raw.get("functional") or {}
        passed_cases = functional.get("passed_cases", 0)
        evaluated_cases = functional.get("evaluated_cases", len(cases))

        if status == "PASS":
            return SimResult(
                status="PASS",
                passed_cases=passed_cases,
                evaluated_cases=evaluated_cases,
                failures=[],
                infrastructure_error=None,
                raw=raw,
            )

        # Parse failures from trace and functional details
        failures: list[SimCaseFailure] = []
        trace_path = raw.get("trace_path") or (ws / "trace.json")
        trace_cases = {}
        if Path(trace_path).is_file():
            try:
                trace_data = read_json(Path(trace_path))
                trace_cases = trace_data.get("cases", {})
            except Exception:
                trace_cases = {}

        details_by_id = {d["case_id"]: d for d in functional.get("details", []) if "case_id" in d}

        for case in cases:
            case_id = case.get("id", "")
            detail = details_by_id.get(case_id)
            if detail and detail.get("status") == "PASS":
                continue

            steps = case.get("steps", [])
            obs_steps = trace_cases.get(case_id, [])
            first_bad_step = 0

            steps_passed = detail.get("steps_passed") if detail else None
            if steps_passed and False in steps_passed:
                first_bad_step = steps_passed.index(False)
            else:
                for idx, step in enumerate(steps):
                    obs = obs_steps[idx].get("outputs", {}) if idx < len(obs_steps) else {}
                    if not outputs_equal(task, obs, step.get("expected", {}), step.get("inputs")):
                        first_bad_step = idx
                        break

            step = steps[first_bad_step] if first_bad_step < len(steps) else {}
            expected = step.get("expected", {})
            obs = obs_steps[first_bad_step].get("outputs", {}) if first_bad_step < len(obs_steps) else {}

            mismatch = find_first_mismatch(task, obs, expected, step.get("inputs"))
            if mismatch:
                field_name, exp_val, obs_val = mismatch
            else:
                field_name = "scan_contract"
                exp_val = "NO_VIOLATION"
                obs_val = "VIOLATION"
                if detail and detail.get("scan_contract", {}).get("violations"):
                    v = detail["scan_contract"]["violations"][0]
                    field_name = v.get("rule", "scan_contract")
                    exp_val = v.get("expected", "NO_VIOLATION")
                    obs_val = v.get("observed", "VIOLATION")
                elif not obs:
                    field_name = next(iter(expected.keys())) if expected else ""
                    exp_val = expected.get(field_name)
                    obs_val = None

            inputs_prefix = [copy.deepcopy(s["inputs"]) for s in steps[: first_bad_step + 1]]
            win_start = max(0, first_bad_step - 2)
            win_end = min(len(steps), first_bad_step + 2)
            step_window = [
                {
                    "step": w_idx,
                    "dt_ms": steps[w_idx].get("dt_ms"),
                    "inputs": copy.deepcopy(steps[w_idx].get("inputs", {})),
                    "expected": copy.deepcopy(steps[w_idx].get("expected", {})),
                    "observed": (
                        copy.deepcopy(obs_steps[w_idx].get("outputs", {}))
                        if w_idx < len(obs_steps) and isinstance(obs_steps[w_idx], dict)
                        else None
                    ),
                }
                for w_idx in range(win_start, win_end)
            ]
            failures.append(
                SimCaseFailure(
                    case_id=case_id,
                    first_bad_step=first_bad_step,
                    field=field_name,
                    expected=exp_val,
                    observed=obs_val,
                    inputs_prefix=inputs_prefix,
                    step_window=step_window,
                )
            )

        return SimResult(
            status="TEST_FAIL",
            passed_cases=passed_cases,
            evaluated_cases=evaluated_cases,
            failures=failures,
            infrastructure_error=infra_error,
            raw=raw,
        )


class FakeBackend:
    """Mock backend for deterministic offline test execution and fast validation."""

    def __init__(
        self,
        compile_fn: Callable | None = None,
        step_fn: Callable | None = None,
    ) -> None:
        self.compile_fn = compile_fn
        self.step_fn = step_fn

    def compile(self, task: dict, candidate: dict | str, workspace: Path) -> CompileResult:
        ws = Path(workspace)
        source_hash = ""
        if candidate:
            try:
                cand_norm = normalize_candidate(candidate)
                source_hash = digest(cand_norm)
                iface_diags = verify_interface_signature(cand_norm, task.get("interface"))
                if iface_diags:
                    return CompileResult(
                        status="COMPILE_FAIL",
                        success=False,
                        backend="FAKE",
                        diagnostics=iface_diags,
                        source_sha256=source_hash,
                    )
            except Exception:
                source_hash = ""

        if self.compile_fn is not None:
            return _call_compile_fn(self.compile_fn, task, candidate, ws)

        return CompileResult(
            status="PASS",
            success=True,
            backend="FAKE",
            source_sha256=source_hash,
        )

    def simulate(self, task: dict, candidate: dict | str, cases: list[dict], workspace: Path) -> SimResult:
        ws = Path(workspace)
        ws.mkdir(parents=True, exist_ok=True)

        if not cases:
            return SimResult(
                status="UNVERIFIED",
                passed_cases=0,
                evaluated_cases=0,
                failures=[],
                infrastructure_error="No test cases provided",
            )

        passed_cases = 0
        evaluated_cases = 0
        failures: list[SimCaseFailure] = []

        for case in cases:
            evaluated_cases += 1
            case_id = case.get("id", f"case_{evaluated_cases}")
            steps = case.get("steps", [])

            # Reset or initialize contract per test case
            contract = None
            if self.step_fn is None:
                try:
                    contract = ScanContract(task["id"])
                except Exception as exc:
                    return SimResult(
                        status="TOOL_ERROR",
                        passed_cases=passed_cases,
                        evaluated_cases=evaluated_cases,
                        failures=failures,
                        infrastructure_error=f"Failed to instantiate ScanContract: {exc}",
                    )
            elif hasattr(self.step_fn, "reset") and callable(self.step_fn.reset):
                self.step_fn.reset()

            case_failed = False
            observed_history: list[Any] = []
            for step_idx, step in enumerate(steps):
                inputs = step.get("inputs", {})
                dt_ms = step.get("dt_ms")
                expected = step.get("expected", {})

                if contract is not None:
                    observed = reference_step(task, contract, inputs, dt_ms)
                else:
                    observed = _call_step_fn(self.step_fn, inputs, dt_ms)
                observed_history.append(observed)

                if not outputs_equal(task, observed, expected, inputs):
                    case_failed = True
                    mismatch = find_first_mismatch(task, observed, expected, inputs)
                    if mismatch:
                        field_name, exp_val, obs_val = mismatch
                    else:
                        field_name = next(iter(expected.keys())) if expected else ""
                        exp_val = expected.get(field_name)
                        obs_val = observed.get(field_name) if isinstance(observed, dict) else observed

                    inputs_prefix = [copy.deepcopy(s["inputs"]) for s in steps[: step_idx + 1]]
                    win_start = max(0, step_idx - 2)
                    step_window = [
                        {
                            "step": w_idx,
                            "dt_ms": steps[w_idx].get("dt_ms"),
                            "inputs": copy.deepcopy(steps[w_idx].get("inputs", {})),
                            "expected": copy.deepcopy(steps[w_idx].get("expected", {})),
                            "observed": copy.deepcopy(observed_history[w_idx]),
                        }
                        for w_idx in range(win_start, step_idx + 1)
                    ]
                    failures.append(
                        SimCaseFailure(
                            case_id=case_id,
                            first_bad_step=step_idx,
                            field=field_name,
                            expected=exp_val,
                            observed=obs_val,
                            inputs_prefix=inputs_prefix,
                            step_window=step_window,
                        )
                    )
                    # Truncate at the first diverging step: do not execute subsequent steps
                    break

            if not case_failed:
                passed_cases += 1

        status = "PASS" if passed_cases == evaluated_cases else "TEST_FAIL"
        return SimResult(
            status=status,
            passed_cases=passed_cases,
            evaluated_cases=evaluated_cases,
            failures=failures,
            infrastructure_error=None,
            raw={"status": status, "passed_cases": passed_cases, "evaluated_cases": evaluated_cases},
        )
