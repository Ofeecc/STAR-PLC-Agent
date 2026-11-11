from __future__ import annotations

import json
import re
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .backend import Backend, CodesysBackend
from .common import digest, now, write_json
from .compiler import (
    CompileResult,
    compile_st,
    normalize_candidate,
)
from .config import Settings
from .dialect_cards import select_dialect_cards
from .llm import ProviderError, parse_candidate
from .selftest import validate_self_tests
from .task_view import agent_view

CODE_CONTRACT = """Return ONLY a JSON object with declaration, implementation, supporting_objects.
declaration is CODESYS FUNCTION_BLOCK FB_Task followed by all VAR sections; omit END_FUNCTION_BLOCK.
implementation is the ST body alone. supporting_objects is a list of helper DUT/POU objects, each with
name, kind (DUT/FUNCTION/FUNCTION_BLOCK), declaration, implementation; functions need return_type.
Keep exact task interface names/types and implement all behavior. Define referenced DUTs. No Markdown.
Do not change requirements or use reference answers. Standard library is available in the project.
The target is CODESYS 3.5 ST. Compilation is offline; do not contact physical equipment.
"""


def requirement_analysis(task: dict) -> dict:
    return {
        "pou_type": "FUNCTION_BLOCK",
        "pou_name": "FB_Task",
        "interface": task.get("interface", []),
        "initial_conditions": task.get("initial_conditions", {}),
        "scan_semantics": task.get("scan_semantics", ""),
        "safety_priority": task.get("safety_priority", ""),
        "assumptions": task.get("assumptions", ""),
        "formal_properties": task.get("ltl", []),
        "atomic_propositions": task.get("atomic_propositions", {}),
        "supporting_types": task.get("supporting_types", task.get("data_types", [])),
        "specification_version": task.get("specification_version", "1"),
        "specification_contract": task.get("specification_contract", {}),
    }


def task_prompt(task: dict) -> str:
    return json.dumps(task, ensure_ascii=False, indent=2)


def empty_result(
    task: dict, condition: str, model: str, framework: str, reason: str | None = None
) -> dict:
    return {
        "schema_version": 1,
        "task_id": task["id"],
        "task_sha256": digest(task),
        "condition": condition,
        "framework": framework,
        "model": model,
        "status": "NOT_RUN",
        "reason": reason,
        "started_utc": now(),
        "finished_utc": None,
        "first_pass_compiled": None,
        "final_compiled": None,
        "repair_attempts": 0,
        "compilation_attempts": [],
        "compiler_call_count": 0,
        "tool_call_count": 0,
        "simulation_call_count": 0,
        "llm_calls": 0,
        "usage": [],
        "selftest_rejected": [],
        "final_candidate": None,
        "api_cost": None,
        "elapsed_seconds": 0.0,
        "functional": {
            "status": "NOT_RUN",
            "evidence": None,
            "planned_cases": len(task.get("tests", [])),
            "evaluated_cases": 0,
            "passed_cases": 0,
            "evaluated_steps": 0,
            "passed_steps": 0,
        },
    }


def safe_extract_json(text: str) -> Any:
    text = text.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception:
            pass

    match = re.search(r"(\[[\s\S]*\]|\{[\s\S]*\})", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except Exception:
            pass

    return {}


def compact_diagnostics(
    candidate: dict | None,
    diagnostics: list[dict],
    window: int = 3,
    max_chars: int = 4000,
) -> str:
    if not diagnostics:
        return ""

    cand = candidate if isinstance(candidate, dict) else {}
    decl = cand.get("declaration", "")
    impl = cand.get("implementation", "")
    decl_lines = decl.splitlines() if isinstance(decl, str) else []
    impl_lines = impl.splitlines() if isinstance(impl, str) else []

    seen = set()
    formatted_entries: list[str] = []

    for diag in diagnostics:
        if not isinstance(diag, dict):
            continue
        severity = str(diag.get("severity", "Error") or "Error").strip()
        text = str(diag.get("text", "") or "").strip()
        pos_raw = diag.get("position")
        pos_str = str(pos_raw or "").strip()

        # Deduplication key
        dedup_key = (severity.lower(), text, pos_str)
        if dedup_key in seen:
            continue
        seen.add(dedup_key)

        # Parse line and column
        line_num: int | None = None
        col_num: int | None = None

        if "line" in diag and isinstance(diag["line"], int):
            line_num = diag["line"]
        if "column" in diag and isinstance(diag["column"], int):
            col_num = diag["column"]

        if line_num is None and pos_str:
            line_match = re.search(r"\bLine\s*[:#]?\s*(-?\d+)", pos_str, re.IGNORECASE)
            if line_match:
                try:
                    line_num = int(line_match.group(1))
                except ValueError:
                    line_num = None

        if col_num is None and pos_str:
            col_match = re.search(
                r"\bCol(?:umn)?\s*[:#]?\s*(-?\d+)", pos_str, re.IGNORECASE
            )
            if col_match:
                try:
                    col_num = int(col_match.group(1))
                except ValueError:
                    col_num = None

        # Build header
        pos_info = ""
        if pos_str:
            pos_info = f" ({pos_str})"
        elif line_num is not None:
            if col_num is not None:
                pos_info = f" (Line {line_num}, Column {col_num})"
            else:
                pos_info = f" (Line {line_num})"

        entry_header = f"[{severity}]{pos_info}: {text}"

        # Context snippet extraction
        snippet_lines: list[str] = []
        if line_num is not None and line_num > 0:
            target_lines = None
            scope_name = ""

            is_decl = (
                "declaration" in text.lower()
                or "declaration" in str(diag.get("category", "")).lower()
                or bool(
                    re.search(
                        r"\b(var_input|var_output|var_in_out|var_temp|var_stat)\b",
                        text,
                        re.IGNORECASE,
                    )
                )
            )

            if is_decl and 1 <= line_num <= len(decl_lines):
                target_lines = decl_lines
                scope_name = "declaration"
            elif 1 <= line_num <= len(impl_lines):
                target_lines = impl_lines
                scope_name = "implementation"
            elif 1 <= line_num <= len(decl_lines):
                target_lines = decl_lines
                scope_name = "declaration"

            if target_lines is not None:
                start_line = max(1, line_num - window)
                end_line = min(len(target_lines), line_num + window)
                snippet_lines.append(f"  --- [{scope_name}] ---")
                for lno in range(start_line, end_line + 1):
                    prefix = ">" if lno == line_num else " "
                    snippet_lines.append(f"{prefix} {lno:4d} | {target_lines[lno - 1]}")
                    if lno == line_num and col_num is not None and col_num > 0:
                        indent = " " * (col_num - 1)
                        snippet_lines.append(f"         | {indent}^")

        if snippet_lines:
            entry_text = entry_header + "\n" + "\n".join(snippet_lines)
        else:
            entry_text = entry_header

        formatted_entries.append(entry_text)

    combined = "\n\n".join(formatted_entries)
    if len(combined) > max_chars:
        combined = combined[:max_chars].rstrip()
    return combined


class _HarnessCodesysBackend(CodesysBackend):
    def compile(
        self, task: dict, candidate: dict | str, workspace: Path
    ) -> CompileResult:
        ws = Path(workspace)
        return compile_st(task, candidate, ws, self.settings)


def run_harness(
    task: dict,
    model: str,
    workspace: Path | str,
    client: Any,
    settings: Settings,
    condition: str = "E3",
    backend: Backend | None = None,
    spec_visible: bool = True,
    ablation: str | None = None,
) -> dict:
    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=False)

    backend = backend or _HarnessCodesysBackend(settings)

    # Leak-free sanitized agent view
    view = agent_view(task, spec_visible=spec_visible)
    write_json(workspace / "task_view.json", view)
    write_json(workspace / "task.json", task)

    # Runtime config
    snapshot = asdict(settings)
    snapshot.pop("api_key", None)
    write_json(workspace / "runtime_config.json", snapshot)

    started = time.monotonic()
    result = {
        "schema_version": 1,
        "task_id": task["id"],
        "task_sha256": digest(task),
        "condition": condition,
        "framework": "star_v2",
        "model": model,
        "status": "NOT_RUN",
        "reason": None,
        "started_utc": now(),
        "finished_utc": None,
        "first_pass_compiled": None,
        "final_compiled": None,
        "repair_attempts": 0,
        "compilation_attempts": [],
        "compiler_call_count": 0,
        "tool_call_count": 0,
        "simulation_call_count": 0,
        "llm_calls": 0,
        "usage": [],
        "selftest_rejected": [],
        "final_candidate": None,
        "api_cost": None,
        "elapsed_seconds": 0.0,
        "functional": {
            "status": "NOT_RUN",
            "evidence": None,
            "planned_cases": len(task.get("tests", [])),
            "evaluated_cases": 0,
            "passed_cases": 0,
            "evaluated_steps": 0,
            "passed_steps": 0,
        },
    }

    def remaining_time() -> int:
        return max(1, int(settings.task_timeout - (time.monotonic() - started)))

    def is_timed_out() -> bool:
        return time.monotonic() - started >= settings.task_timeout

    try:
        # Step 1: Planner
        plan: dict = {}
        if ablation != "no_planner":
            if is_timed_out():
                result["status"], result["reason"] = (
                    "TIMEOUT",
                    "Task deadline exhausted before planner",
                )
                return result
            if result["llm_calls"] < settings.max_llm_calls:
                planner_prompt = (
                    "You are a PLC control software architect. Analyze the requirements and produce an architecture plan in JSON format with keys:\n"
                    "- state_machine: list of states and transitions\n"
                    "- timer_plan: timers required, PT durations, reset conditions\n"
                    "- priorities: safety and operational priorities\n"
                    "- initial_values: initial values for variables\n\n"
                    f"SPECIFICATIONS:\n{json.dumps(view, indent=2)}"
                )
                planner_messages = [
                    {
                        "role": "developer",
                        "content": "You are a senior PLC control systems architect. Return ONLY valid JSON.",
                    },
                    {"role": "user", "content": planner_prompt},
                ]
                reply = client.respond(
                    model,
                    planner_messages,
                    workspace / "llm_planner",
                    timeout=remaining_time(),
                )
                result["llm_calls"] += 1
                if reply.get("usage"):
                    result["usage"].append(reply["usage"])
                try:
                    plan = safe_extract_json(reply.get("text", ""))
                    if not isinstance(plan, dict):
                        plan = {"raw_plan": str(plan)}
                except Exception:
                    plan = {"raw_plan": reply.get("text", "")}

        write_json(workspace / "plan.json", plan)

        # Step 2: Dialect Selection
        if ablation != "no_dialect":
            cards = select_dialect_cards(view, max_cards=4)
        else:
            cards = []
        write_json(workspace / "dialect_cards.json", cards)

        # Step 3: Coder & Compile-Repair Loop
        coder_developer = (
            CODE_CONTRACT
            + "\nTarget: CODESYS 3.5 IEC 61131-3 Structured Text offline compilation."
        )
        coder_user = (
            f"TASK SPECIFICATIONS:\n{json.dumps(view, indent=2)}\n\n"
            f"ARCHITECTURAL PLAN:\n{json.dumps(plan, indent=2)}\n\n"
            f"CODESYS DIALECT CARDS:\n{json.dumps(cards, indent=2)}"
        )

        if is_timed_out():
            result["status"], result["reason"] = (
                "TIMEOUT",
                "Task deadline exhausted before coding",
            )
            return result

        if result["llm_calls"] >= settings.max_llm_calls:
            result["status"], result["reason"] = (
                "BUDGET_EXHAUSTED",
                "LLM call limit reached",
            )
            return result

        messages = [
            {"role": "developer", "content": coder_developer},
            {"role": "user", "content": coder_user},
        ]
        reply = client.respond(
            model,
            messages,
            workspace / "llm_code_00",
            timeout=remaining_time(),
        )
        result["llm_calls"] += 1
        if reply.get("usage"):
            result["usage"].append(reply["usage"])

        candidate = parse_candidate(reply.get("text", ""))
        write_json(workspace / "version_00.json", candidate)

        if is_timed_out():
            result["status"], result["reason"] = (
                "TIMEOUT",
                "Task deadline exhausted after generation",
            )
            return result

        compiled = backend.compile(task, candidate, workspace / "compile_00")
        result["tool_call_count"] += 1
        result["compiler_call_count"] += 1
        result["compilation_attempts"].append(asdict(compiled))
        result["first_pass_compiled"] = compiled.success

        try:
            prev_cand_hash = digest(normalize_candidate(candidate))
        except Exception:
            prev_cand_hash = digest(str(candidate))
        previous_hashes = [prev_cand_hash]
        stagnation_detected = False

        if compiled.status in ("TOOL_ERROR", "TIMEOUT"):
            result["status"], result["reason"] = compiled.status, compiled.infrastructure_error
            return result

        attempt = 0
        while not compiled.success and attempt < settings.max_repairs:
            if is_timed_out():
                result["status"], result["reason"] = (
                    "TIMEOUT",
                    "Task deadline exhausted during compile repair",
                )
                break
            if result["llm_calls"] >= settings.max_llm_calls:
                break
            if result["compiler_call_count"] >= settings.max_repairs + 1:
                break

            attempt += 1
            result["repair_attempts"] = attempt
            diag_str = compact_diagnostics(candidate, compiled.diagnostics)

            stagnation_msg = ""
            if stagnation_detected:
                stagnation_msg = (
                    "\n\nWARNING: CODE STAGNATION DETECTED. Your previous repair produced identical code "
                    "(hash matches previous attempt). You MUST modify the implementation to address the errors.\n"
                )

            repair_prompt = (
                f"Compilation failed with the following diagnostics:\n{diag_str}\n"
                f"{stagnation_msg}\n"
                f"Current code:\n{json.dumps(candidate, indent=2)}\n\n"
                "Please fix the compilation errors while preserving the required interface and logic."
            )

            repair_messages = [
                {"role": "developer", "content": coder_developer},
                {"role": "user", "content": coder_user},
                {"role": "user", "content": repair_prompt},
            ]

            reply = client.respond(
                model,
                repair_messages,
                workspace / f"llm_repair_{attempt:02d}",
                timeout=remaining_time(),
            )
            result["llm_calls"] += 1
            if reply.get("usage"):
                result["usage"].append(reply["usage"])

            try:
                new_candidate = parse_candidate(reply.get("text", ""))
            except Exception:
                break

            candidate = new_candidate
            write_json(workspace / f"version_{attempt:02d}.json", candidate)

            try:
                new_hash = digest(normalize_candidate(candidate))
            except Exception:
                new_hash = digest(str(candidate))
            stagnation_detected = new_hash in previous_hashes
            previous_hashes.append(new_hash)

            compiled = backend.compile(
                task, candidate, workspace / f"compile_{attempt:02d}"
            )
            result["tool_call_count"] += 1
            result["compiler_call_count"] += 1
            result["compilation_attempts"].append(asdict(compiled))

            if compiled.status in ("TOOL_ERROR", "TIMEOUT"):
                result["status"], result["reason"] = (
                    compiled.status,
                    compiled.infrastructure_error,
                )
                break

        result["final_compiled"] = compiled.success
        result["final_candidate"] = candidate
        best_candidate = candidate
        best_score = (compiled.success, 0)

        if not compiled.success:
            if result["status"] not in ("TOOL_ERROR", "TIMEOUT"):
                result["status"] = "COMPILE_FAIL"
                result["reason"] = "Failed to compile within repair budget"
            return result

        result["status"] = "UNVERIFIED"
        result["reason"] = (
            "CODESYS compiled; PLC functional execution remains to be evaluated"
        )

        # Step 4: Independent Tester (Self-Tests)
        valid_cases: list[dict] = []
        if result["final_compiled"] and ablation != "no_selftest":
            if not is_timed_out() and result["llm_calls"] < settings.max_llm_calls:
                tester_prompt = (
                    "You are an independent PLC test engineer. Generate comprehensive unit test cases for the specified PLC function block.\n"
                    "Return a JSON array of test case objects. Each test case must have:\n"
                    "- id: string identifier (e.g. 'case_1')\n"
                    "- steps: array of steps, where each step has:\n"
                    "    - inputs: dictionary of input variable names and values\n"
                    "    - expected: dictionary of expected output variable names and values\n"
                    "    - dt_ms: (optional) cycle elapsed time in milliseconds\n\n"
                    f"TASK SPECIFICATIONS:\n{json.dumps(view, indent=2)}"
                )
                tester_messages = [
                    {
                        "role": "developer",
                        "content": "You are an independent PLC verification engineer. Return ONLY a JSON list of test cases.",
                    },
                    {"role": "user", "content": tester_prompt},
                ]
                if settings.selftest_max_cases and settings.selftest_max_steps_per_case:
                    tester_messages[-1]['content'] += (
                        f'\nOutput budget: at most {settings.selftest_max_cases} cases, '
                        f'at most {settings.selftest_max_steps_per_case} steps per case. '
                        'Use compact JSON. Cover a complete normal path and one important boundary. '
                        'Keep reasoning concise enough to finish the entire JSON within the output budget.'
                    )
                reply = client.respond(
                    model,
                    tester_messages,
                    workspace / "llm_tester",
                    max_tokens=settings.tester_max_output_tokens or None,
                    timeout=remaining_time(),
                )
                result["llm_calls"] += 1
                if reply.get("usage"):
                    result["usage"].append(reply["usage"])

                try:
                    raw_cases = safe_extract_json(reply.get("text", ""))
                except Exception:
                    raw_cases = []
                if isinstance(raw_cases, list):
                    valid_cases = validate_self_tests(view, raw_cases)
                else:
                    valid_cases = []

        write_json(workspace / "selftest.json", valid_cases)

        # Step 5: Simulation & Behavioral Repair Loop
        if valid_cases:
            active_cases = list(valid_cases)
            best_was_simulated = False
            max_rejections = len(valid_cases) // 2
            rejected_case_ids: set[str] = set()

            sim_attempt = 0
            while sim_attempt < settings.max_simulations:
                if is_timed_out():
                    result["status"], result["reason"] = (
                        "TIMEOUT",
                        "Task deadline exhausted during simulation",
                    )
                    break
                if result["simulation_call_count"] >= settings.max_simulations:
                    break

                sim = backend.simulate(
                    task, candidate, active_cases, workspace / f"sim_{sim_attempt:02d}"
                )
                result["tool_call_count"] += 1
                result["simulation_call_count"] += 1
                sim_attempt += 1

                if sim.status in ("TOOL_ERROR", "TIMEOUT", "UNVERIFIED"):
                    result["status"], result["reason"] = sim.status, sim.infrastructure_error
                    break
                if sim.evaluated_cases != len(active_cases):
                    result["status"], result["reason"] = "UNVERIFIED", "Incomplete simulation coverage"
                    break

                passed_cases = sim.passed_cases
                result["status"], result["reason"] = "TEST_FAIL", "Active self-tests have behavioral failures"
                if (True, passed_cases) >= best_score:
                    best_score = (True, passed_cases)
                    best_candidate = candidate
                    best_was_simulated = True

                if passed_cases == len(active_cases) and len(active_cases) > 0:
                    result["status"] = "PASS"
                    result["reason"] = "All active self-tests passed"
                    break

                if (
                    sim_attempt >= settings.max_simulations
                    or result["llm_calls"] >= settings.max_llm_calls
                    or is_timed_out()
                ):
                    break

                # Format failures for model
                failures_summary = []
                for f in sim.failures:
                    failures_summary.append(
                        {
                            "case_id": f.case_id,
                            "first_bad_step": f.first_bad_step,
                            "field": f.field,
                            "expected": f.expected,
                            "observed": f.observed,
                            "inputs_prefix": f.inputs_prefix,
                        }
                    )

                remaining_rejections = max_rejections - len(rejected_case_ids)
                sim_repair_prompt = (
                    f"Simulation failed on {len(sim.failures)} test case(s):\n"
                    f"{json.dumps(failures_summary, indent=2)}\n\n"
                    f"You may:\n"
                    f"1. Fix the candidate implementation to satisfy the test expectations.\n"
                    f"2. If you believe a self-test case was incorrectly specified, you may reject it by providing:\n"
                    f'   "reject_cases": [{{"id": "<case_id>", "reason": "<reason>"}}]\n'
                    f"   (You can reject at most {remaining_rejections} more case(s); total rejection cap is {max_rejections}).\n\n"
                    f"Current candidate code:\n{json.dumps(candidate, indent=2)}"
                )

                sim_repair_messages = [
                    {"role": "developer", "content": coder_developer},
                    {"role": "user", "content": coder_user},
                    {"role": "user", "content": sim_repair_prompt},
                ]

                reply = client.respond(
                    model,
                    sim_repair_messages,
                    workspace / f"llm_sim_repair_{sim_attempt:02d}",
                    timeout=remaining_time(),
                )
                result["llm_calls"] += 1
                if reply.get("usage"):
                    result["usage"].append(reply["usage"])

                reply_text = reply.get("text", "")

                # Check for reject_cases
                try:
                    parsed_reply = safe_extract_json(reply_text)
                    if (
                        isinstance(parsed_reply, dict)
                        and "reject_cases" in parsed_reply
                    ):
                        for rej in parsed_reply["reject_cases"]:
                            if isinstance(rej, dict) and "id" in rej:
                                rej_id = rej["id"]
                                if rej_id not in rejected_case_ids and rej_id in {
                                    c["id"] for c in valid_cases
                                }:
                                    if len(rejected_case_ids) < max_rejections:
                                        rejected_case_ids.add(rej_id)
                                        result["selftest_rejected"].append(rej)
                except Exception:
                    pass

                next_cases = [c for c in valid_cases if c["id"] not in rejected_case_ids]
                if next_cases != active_cases:
                    # Scores from different test sets are not comparable.
                    best_score = (True, -1)
                    best_was_simulated = False
                active_cases = next_cases

                # Parse new candidate
                try:
                    new_candidate = parse_candidate(reply_text)
                except Exception:
                    candidate = best_candidate
                    continue

                if result["compiler_call_count"] >= settings.max_repairs + 1:
                    candidate = best_candidate
                    break

                compile_ws = workspace / f"compile_sim_{sim_attempt:02d}"
                comp_res = backend.compile(task, new_candidate, compile_ws)
                result["tool_call_count"] += 1
                result["compiler_call_count"] += 1
                result["compilation_attempts"].append(asdict(comp_res))

                if comp_res.status in ("TOOL_ERROR", "TIMEOUT"):
                    result["status"], result["reason"] = comp_res.status, comp_res.infrastructure_error
                    break
                if not comp_res.success:
                    # Ratchet rejects uncompiled code (False, 0) < best_score (True, ...)
                    candidate = best_candidate
                    continue

                candidate = new_candidate
                write_json(workspace / f"version_sim_{sim_attempt:02d}.json", candidate)

            # Update best_candidate as final_candidate
            result["final_candidate"] = best_candidate
            result["selftest_evaluation"] = {"candidate_sha256": digest(normalize_candidate(best_candidate)),
                "cases_sha256": digest(active_cases), "status": result["status"],
                "evaluated_cases": len(active_cases) if best_was_simulated else 0,
                "passed_cases": max(0, best_score[1]) if best_was_simulated else 0}
        else:
            result["final_candidate"] = best_candidate

    except ProviderError as exc:
        result["status"], result["reason"] = "TOOL_ERROR", str(exc)
    except OSError as exc:
        result["status"], result["reason"] = (
            "TOOL_ERROR",
            "Local infrastructure: " + str(exc),
        )
    except (ValueError, TypeError, KeyError) as exc:
        result["status"], result["reason"] = (
            "UNVERIFIED",
            "Invalid model output: " + str(exc),
        )
    finally:
        result["elapsed_seconds"] = time.monotonic() - started
        result["finished_utc"] = now()
        if result.get("final_candidate") is not None:
            try:
                write_json(
                    workspace / "final_candidate.json", result["final_candidate"]
                )
            except Exception:
                pass
        try:
            write_json(workspace / "result.json", result)
        except Exception:
            pass

    return result
