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
from .dialect_cards import select_dialect_cards, select_static_analysis_hint
from .formal_verify import verify_candidate
from .llm import ProviderError, parse_candidate
from .selftest import check_initial_condition_warnings, validate_self_tests
from .st_verifier import sanitize_counterexamples_for_agent
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


def empty_result(task: dict, condition: str, model: str, framework: str, reason: str | None = None) -> dict:
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
        "verification_call_count": 0,
        "cegar_repairs": 0,
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
            col_match = re.search(r"\bCol(?:umn)?\s*[:#]?\s*(-?\d+)", pos_str, re.IGNORECASE)
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

        low_text = text.lower()
        if "sa0027" in low_text:
            entry_text += (
                "\n  [Hint SA0027]: Rename the conflicting internal variable, or if the task interface mandates that exact name, "
                "add `{attribute 'analysis' := '-27'}` on the line immediately before the variable declaration."
            )
        if "sa0033" in low_text:
            entry_text += (
                "\n  [Hint SA0033]: Remove the unused variable declaration or ensure it is read/used meaningfully."
            )

        formatted_entries.append(entry_text)

    combined = "\n\n".join(formatted_entries)
    if len(combined) > max_chars:
        combined = combined[:max_chars].rstrip()
    return combined


def _format_attempt_ledger(entries: list[str], max_entries: int = 8) -> str:
    """Format a compact cross-round history ledger to prevent A<->B repair oscillations."""
    if not entries:
        return ""
    recent = entries[-max_entries:]
    return "REPAIR ATTEMPT LEDGER (do NOT repeat failed approaches):\n" + "\n".join(f"- {e}" for e in recent)


class _HarnessCodesysBackend(CodesysBackend):
    def compile(self, task: dict, candidate: dict | str, workspace: Path) -> CompileResult:
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
        "framework": "star",
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
        "verification_call_count": 0,
        "cegar_repairs": 0,
        "ratchet_rollbacks": 0,
        "verification_status_counts": {},
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

    best_candidate: Any = None
    best_score: tuple[bool, int, int, int] = (False, 0, 0, 0)
    attempt_ledger: list[str] = []

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
            if not settings.max_llm_calls or result["llm_calls"] < settings.max_llm_calls:
                planner_prompt = (
                    "You are a PLC control software architect. Produce a concise architecture plan (at most 2000 words). Do not enumerate exhaustive traces. Return complete JSON with keys:\n"
                    "- state_machine: list of states and transitions\n"
                    "- timer_plan: timers required, PT durations, reset conditions\n"
                    "- priorities: safety and operational priorities\n"
                    "- initial_values: initial values for variables\n"
                    "- scan_execution_order: explicit 4-stage scan order (1. edge sampling, "
                    "2. safety/reset priority & state transitions, "
                    "3. unconditional top-level timer FB calls outside CASE/IF, 4. unified output assignments)\n"
                    '- formal_assertions: optional list of {"id": "A1", "formula": "G(...)"} '
                    "SMV temporal/invariant assertions over declared VAR_INPUT/VAR_OUTPUT port names "
                    "(use SMV operators &, |, !, ->, <->, =, !=; never &&/||, never chained a<=x<=b, "
                    "never X/G/F inside min()/max(), never ST radix literals like 16#8001 — use 0uh16_8001)\n\n"
                    f"SPECIFICATIONS:\n{json.dumps(view, indent=2)}"
                )
                planner_messages = [
                    {
                        "role": "developer",
                        "content": "You are a senior PLC control systems architect. Return ONLY valid JSON.",
                    },
                    {"role": "user", "content": planner_prompt},
                ]
                try:
                    reply = client.respond(
                        model,
                        planner_messages,
                        workspace / "llm_planner",
                        max_tokens=settings.output_limit("planner"),
                        timeout=remaining_time(),
                    )
                except ProviderError as exc:
                    # An optional plan must not consume the entire synthesis run.
                    # Do not feed truncated JSON to the coder or retry invisibly.
                    if "incomplete" not in str(exc) or "length" not in str(exc):
                        raise
                    result["planner_warning"] = str(exc)
                    reply = {"text": "{}"}
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
            static_hint = select_static_analysis_hint(view)
        else:
            cards = []
            static_hint = None
        write_json(workspace / "dialect_cards.json", cards)

        # Step 3: Coder & Compile-Repair Loop
        coder_developer = CODE_CONTRACT + "\nTarget: CODESYS 3.5 IEC 61131-3 Structured Text offline compilation."
        static_hint_block = (
            f"\n\nSTATIC ANALYSIS LIGHT GUIDANCE:\n{json.dumps(static_hint, indent=2)}" if static_hint else ""
        )
        coder_user = (
            f"TASK SPECIFICATIONS:\n{json.dumps(view, indent=2)}\n\n"
            f"ARCHITECTURAL PLAN:\n{json.dumps(plan, indent=2)}\n\n"
            f"CODESYS DIALECT CARDS:\n{json.dumps(cards, indent=2)}"
            f"{static_hint_block}"
        )

        if is_timed_out():
            result["status"], result["reason"] = (
                "TIMEOUT",
                "Task deadline exhausted before coding",
            )
            return result

        if settings.max_llm_calls and result["llm_calls"] >= settings.max_llm_calls:
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
            max_tokens=settings.output_limit("coder"),
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
        if compiled.status not in ("PASS", "COMPILE_FAIL"):
            result["status"], result["reason"] = compiled.status, compiled.infrastructure_error
            return result
        result["first_pass_compiled"] = compiled.success

        try:
            prev_cand_hash = digest(normalize_candidate(candidate))
        except Exception:
            prev_cand_hash = digest(str(candidate))
        previous_hashes = [prev_cand_hash]
        stagnation_detected = False

        attempt = 0
        while not compiled.success and (settings.max_repairs < 0 or attempt < settings.max_repairs):
            if is_timed_out():
                result["status"], result["reason"] = (
                    "TIMEOUT",
                    "Task deadline exhausted during compile repair",
                )
                break
            if settings.max_llm_calls and result["llm_calls"] >= settings.max_llm_calls:
                break
            if settings.max_repairs >= 0 and result["compiler_call_count"] >= settings.max_repairs + 1:
                break

            attempt += 1
            result["repair_attempts"] = attempt
            diag_str = compact_diagnostics(candidate, compiled.diagnostics)
            attempt_ledger.append(
                f"Compile #{attempt - 1} failed ({prev_cand_hash[:8]}): "
                + (diag_str.splitlines() or ["no diagnostic details"])[0][:140]
            )

            stagnation_msg = ""
            if stagnation_detected:
                stagnation_msg = (
                    "\n\nWARNING: CODE STAGNATION DETECTED. Your previous repair produced identical code "
                    "(hash matches previous attempt). You MUST modify the implementation to address the errors.\n"
                )

            ledger_text = _format_attempt_ledger(attempt_ledger)
            repair_prompt = (
                f"Compilation failed with the following diagnostics:\n{diag_str}\n"
                f"{stagnation_msg}"
                + (f"\n{ledger_text}\n" if ledger_text else "")
                + "\nPlease fix the compilation errors while preserving the required interface and logic."
            )

            repair_messages = [
                {"role": "developer", "content": coder_developer},
                {"role": "user", "content": coder_user},
                {"role": "assistant", "content": json.dumps(candidate, ensure_ascii=False, indent=2)},
                {"role": "user", "content": repair_prompt},
            ]

            reply = client.respond(
                model,
                repair_messages,
                workspace / f"llm_repair_{attempt:02d}",
                max_tokens=settings.output_limit("repair"),
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

            compiled = backend.compile(task, candidate, workspace / f"compile_{attempt:02d}")
            result["tool_call_count"] += 1
            result["compiler_call_count"] += 1
            result["compilation_attempts"].append(asdict(compiled))

            if compiled.status not in ("PASS", "COMPILE_FAIL"):
                result["status"], result["reason"] = (
                    compiled.status,
                    compiled.infrastructure_error,
                )
                return result

        result["final_compiled"] = compiled.success
        result["final_candidate"] = candidate
        best_candidate = candidate
        best_score = (compiled.success, 0, 0, 0)

        if not compiled.success:
            if result["status"] not in ("TOOL_ERROR", "TIMEOUT"):
                result["status"] = "COMPILE_FAIL"
                result["reason"] = "Failed to compile within repair budget"
            return result

        result["status"] = "UNVERIFIED"
        result["reason"] = "CODESYS compiled; PLC functional execution remains to be evaluated"

        # Step 3.5: Self-Developed ST->SMV Formal Verification & CEGAR Repair Loop (observer-free Scheme A)
        max_ver_cfg = getattr(settings, "max_verifications", 3)
        max_ver_runs = 5 if max_ver_cfg < 0 else max_ver_cfg
        if result["final_compiled"] and ablation not in ("no_verify", "no_cegar") and max_ver_runs > 0:
            cegar_hashes = {prev_cand_hash}
            formal_assertions = plan.get("formal_assertions") if isinstance(plan, dict) else None
            if not isinstance(formal_assertions, list):
                formal_assertions = None
            for ver_idx in range(max_ver_runs):
                if is_timed_out():
                    break
                ver_res = verify_candidate(
                    task=view,
                    candidate=candidate,
                    out_dir=workspace / f"verify_{ver_idx:02d}",
                    include_expected_observer=False,
                    use_observer_smv=False,
                    extra_assertions=formal_assertions,
                )
                result["tool_call_count"] += 1
                result["verification_call_count"] += 1
                result["verification"] = ver_res

                ver_status = str(ver_res.get("status") or "UNKNOWN")
                status_counts = result["verification_status_counts"]
                status_counts[ver_status] = status_counts.get(ver_status, 0) + 1
                passed_props = int(ver_res.get("passed_properties") or 0)
                if ver_status in ("PASS", "COUNTEREXAMPLE") and (ver_res.get("unknown_properties") or 0) == 0:
                    cand_ver_score = (True, passed_props, best_score[2], best_score[3])
                    if cand_ver_score >= best_score:
                        best_score = cand_ver_score
                        best_candidate = candidate
                    elif ver_idx > 0:
                        result["ratchet_rollbacks"] += 1

                if ver_status == "PASS":
                    attempt_ledger.append(
                        f"Formal verify #{ver_idx:02d}: PASS ({passed_props}/{ver_res.get('total_properties')})"
                    )
                    break
                if ver_status != "COUNTEREXAMPLE":
                    # UNSUPPORTED_ST / INCONCLUSIVE / TOOL_ERROR / TIMEOUT — log and proceed cleanly
                    attempt_ledger.append(
                        f"Formal verify #{ver_idx:02d}: {ver_status} ({ver_res.get('reason') or 'skipped CEGAR'})"[:160]
                    )
                    break

                if ver_idx + 1 >= max_ver_runs:
                    break
                if settings.max_llm_calls and result["llm_calls"] >= settings.max_llm_calls:
                    break
                if is_timed_out():
                    break

                failed_props = [
                    {"id": p.get("id"), "explanation": p.get("explanation", ""), "expression": p.get("expression")}
                    for p in (ver_res.get("property_results") or [])
                    if p.get("holds") is False
                ]
                san_ces = sanitize_counterexamples_for_agent(ver_res.get("counterexamples") or [])
                attempt_ledger.append(
                    f"Formal verify #{ver_idx:02d} FAILED ({passed_props}/{ver_res.get('total_properties')} passed; failed={[p['id'] for p in failed_props]})"
                )
                ledger_text = _format_attempt_ledger(attempt_ledger)
                cegar_prompt = (
                    "Formal LTL/INVAR verification (ST->SMV + NuSMV/nuXmv) found counterexample(s) where your code "
                    "violates the specification:\n"
                    f"VIOLATED PROPERTIES:\n{json.dumps(failed_props[:4], ensure_ascii=False, indent=2)}\n\n"
                    f"COUNTEREXAMPLE TRACE(S) (inputs, your outputs, and candidate internal state):\n{json.dumps(san_ces, indent=2)}\n\n"
                    + (f"{ledger_text}\n\n" if ledger_text else "")
                    + "Fix the logic so every property holds across all scan sequences and edge cases. "
                    + "Return ONLY JSON with declaration, implementation, supporting_objects."
                )
                cegar_messages = [
                    {"role": "developer", "content": coder_developer},
                    {"role": "user", "content": coder_user},
                    {"role": "assistant", "content": json.dumps(candidate, ensure_ascii=False, indent=2)},
                    {"role": "user", "content": cegar_prompt},
                ]
                reply = client.respond(
                    model,
                    cegar_messages,
                    workspace / f"llm_cegar_{ver_idx:02d}",
                    max_tokens=settings.output_limit("repair"),
                    timeout=remaining_time(),
                )
                result["llm_calls"] += 1
                if reply.get("usage"):
                    result["usage"].append(reply["usage"])

                try:
                    new_candidate = parse_candidate(reply.get("text", ""))
                except Exception:
                    break

                try:
                    new_hash = digest(normalize_candidate(new_candidate))
                except Exception:
                    new_hash = digest(str(new_candidate))
                if new_hash in cegar_hashes:
                    attempt_ledger.append(f"CEGAR #{ver_idx + 1:02d} stagnated (identical code hash {new_hash[:8]})")
                    break
                cegar_hashes.add(new_hash)

                if settings.max_repairs >= 0 and result["compiler_call_count"] >= settings.max_repairs + 1:
                    attempt_ledger.append("Compile safety limit reached before CEGAR repair")
                    break
                comp_cegar = backend.compile(task, new_candidate, workspace / f"compile_cegar_{ver_idx:02d}")
                result["tool_call_count"] += 1
                result["compiler_call_count"] += 1
                result["compilation_attempts"].append(asdict(comp_cegar))
                if comp_cegar.status not in ("PASS", "COMPILE_FAIL"):
                    result["status"], result["reason"] = comp_cegar.status, comp_cegar.infrastructure_error
                    candidate = best_candidate
                    break
                if not comp_cegar.success:
                    attempt_ledger.append(f"CEGAR #{ver_idx + 1:02d} failed compile")
                    result["ratchet_rollbacks"] += 1
                    candidate = best_candidate
                    continue

                result["cegar_repairs"] += 1
                candidate = new_candidate
                write_json(workspace / f"version_cegar_{ver_idx:02d}.json", candidate)

            if (result.get("verification") or {}).get("status") == "PASS":
                best_candidate = candidate
            else:
                if candidate is not best_candidate:
                    result["ratchet_rollbacks"] += 1
                candidate = best_candidate
            result["final_candidate"] = best_candidate

        # Step 4: Independent Tester (Self-Tests)
        valid_cases: list[dict] = []
        if result["final_compiled"] and ablation != "no_selftest":
            if not is_timed_out() and (not settings.max_llm_calls or result["llm_calls"] < settings.max_llm_calls):
                tester_prompt = (
                    "You are an independent PLC test engineer. Generate comprehensive unit test cases for the specified PLC function block.\n"
                    "CODESYS Simulation Timing & Edge Rules:\n"
                    "- dt_ms advances elapsed PLC scan time for that step; TON/TOF timers accumulate dt_ms across consecutive steps while IN keeps its active state (e.g., IN=TRUE for TON).\n"
                    "- Rising-edge detection (R_TRIG or x AND NOT prev_x) requires a step with x=FALSE before the step with x=TRUE.\n\n"
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
                    tester_messages[-1]["content"] += (
                        f"\nOutput budget: at most {settings.selftest_max_cases} cases, "
                        f"at most {settings.selftest_max_steps_per_case} steps per case. "
                        "Use compact JSON. Cover a complete normal path and one important boundary. "
                        "Keep reasoning concise enough to finish the entire JSON within the output budget."
                    )
                reply = client.respond(
                    model,
                    tester_messages,
                    workspace / "llm_tester",
                    max_tokens=settings.output_limit("tester"),
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
        init_cond_warnings = check_initial_condition_warnings(valid_cases, view)
        if init_cond_warnings:
            write_json(workspace / "selftest_warnings.json", init_cond_warnings)
            attempt_ledger.append(f"Self-test step-0 initial_conditions warning: {init_cond_warnings[0][:120]}")

        # Step 5: Simulation & Behavioral Repair Loop
        if valid_cases:
            active_cases = list(valid_cases)
            best_was_simulated = False
            max_rejections = len(valid_cases) // 2
            rejected_case_ids: set[str] = set()
            sim_tested_hashes: set[str] = set()
            cases_rejected_in_prev_step = False

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

                try:
                    cur_cand_hash = digest(normalize_candidate(candidate))
                except Exception:
                    cur_cand_hash = digest(str(candidate))
                was_previously_simulated = bool(cur_cand_hash and cur_cand_hash in sim_tested_hashes)
                sim_tested_hashes.add(cur_cand_hash)

                sim = backend.simulate(task, candidate, active_cases, workspace / f"sim_{sim_attempt:02d}")
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

                lazy_rejection_blocked = cases_rejected_in_prev_step and was_previously_simulated
                sim_score = (True, best_score[1], passed_cases, -len(rejected_case_ids))

                if lazy_rejection_blocked:
                    result["ratchet_rollbacks"] += 1
                    result["reason"] = "Blocked lazy test-case rejection without candidate code modification"
                else:
                    if passed_cases == len(active_cases) and len(active_cases) > 0:
                        best_score = sim_score
                        best_candidate = candidate
                        best_was_simulated = True
                        result["status"] = "PASS"
                        result["reason"] = "All active self-tests passed"
                        break
                    if sim_score >= best_score:
                        best_score = sim_score
                        best_candidate = candidate
                        best_was_simulated = True
                    elif sim_attempt > 1:
                        result["ratchet_rollbacks"] += 1

                cases_rejected_in_prev_step = False

                if (
                    sim_attempt >= settings.max_simulations
                    or (settings.max_llm_calls and result["llm_calls"] >= settings.max_llm_calls)
                    or is_timed_out()
                ):
                    break

                # Format failures for model (including local waveform window around first_bad_step)
                failures_summary = []
                for f in sim.failures:
                    f_item: dict[str, Any] = {
                        "case_id": f.case_id,
                        "first_bad_step": f.first_bad_step,
                        "field": f.field,
                        "expected": f.expected,
                        "observed": f.observed,
                        "inputs_prefix": f.inputs_prefix,
                    }
                    if getattr(f, "step_window", None):
                        f_item["step_window"] = f.step_window
                    failures_summary.append(f_item)

                attempt_ledger.append(
                    f"Sim #{sim_attempt:02d}: passed {passed_cases}/{len(active_cases)} "
                    + f"(first fail: {failures_summary[0]['case_id'] if failures_summary else 'none'})"
                )
                ledger_text = _format_attempt_ledger(attempt_ledger)
                remaining_rejections = max_rejections - len(rejected_case_ids)
                sim_repair_prompt = (
                    f"Simulation failed on {len(sim.failures)} test case(s):\n"
                    f"{json.dumps(failures_summary, indent=2)}\n\n"
                    + (f"{ledger_text}\n\n" if ledger_text else "")
                    + "You may:\n"
                    + "1. Fix the candidate implementation to satisfy the test expectations.\n"
                    + "2. Only if a self-test case directly contradicts the task specification, reject it by providing:\n"
                    + '   "reject_cases": [{"id": "<case_id>", "reason": "<specific specification clause>"}]\n'
                    + f"   (You can reject at most {remaining_rejections} more case(s); total rejection cap is {max_rejections}; rejecting cases without modifying code will NOT pass).\n\n"
                    + 'Return ONLY a JSON object with keys: "declaration", "implementation", "supporting_objects", and optionally "reject_cases". '
                    + 'Even if you reject test cases, you MUST still return the full "declaration", "implementation", and "supporting_objects".'
                )

                sim_repair_messages = [
                    {"role": "developer", "content": coder_developer},
                    {"role": "user", "content": coder_user},
                    {"role": "assistant", "content": json.dumps(candidate, ensure_ascii=False, indent=2)},
                    {"role": "user", "content": sim_repair_prompt},
                ]

                reply = client.respond(
                    model,
                    sim_repair_messages,
                    workspace / f"llm_sim_repair_{sim_attempt:02d}",
                    max_tokens=settings.output_limit("repair"),
                    timeout=remaining_time(),
                )
                result["llm_calls"] += 1
                if reply.get("usage"):
                    result["usage"].append(reply["usage"])

                reply_text = reply.get("text", "")

                # Check for reject_cases
                try:
                    parsed_reply = safe_extract_json(reply_text)
                    if isinstance(parsed_reply, dict) and "reject_cases" in parsed_reply:
                        for rej in parsed_reply["reject_cases"]:
                            if isinstance(rej, dict) and "id" in rej:
                                rej_id = rej["id"]
                                if rej_id not in rejected_case_ids and rej_id in {c["id"] for c in valid_cases}:
                                    if len(rejected_case_ids) < max_rejections:
                                        rejected_case_ids.add(rej_id)
                                        result["selftest_rejected"].append(rej)
                except Exception:
                    pass

                next_cases = [c for c in valid_cases if c["id"] not in rejected_case_ids]
                cases_rejected_in_prev_step = next_cases != active_cases
                if cases_rejected_in_prev_step:
                    best_was_simulated = False
                active_cases = next_cases

                # Parse new candidate
                try:
                    new_candidate = parse_candidate(reply_text)
                except Exception:
                    candidate = best_candidate
                    result["ratchet_rollbacks"] += 1
                    continue

                if is_timed_out():
                    candidate = best_candidate
                    break

                if settings.max_repairs >= 0 and result["compiler_call_count"] >= settings.max_repairs + 1:
                    candidate = best_candidate
                    break
                compile_ws = workspace / f"compile_sim_{sim_attempt:02d}"
                comp_res = backend.compile(task, new_candidate, compile_ws)
                result["tool_call_count"] += 1
                result["compiler_call_count"] += 1
                result["compilation_attempts"].append(asdict(comp_res))

                if comp_res.status not in ("PASS", "COMPILE_FAIL"):
                    result["status"], result["reason"] = comp_res.status, comp_res.infrastructure_error
                    break
                if not comp_res.success:
                    # Ratchet rejects uncompiled code (False, ...) < best_score (True, ...)
                    candidate = best_candidate
                    result["ratchet_rollbacks"] += 1
                    continue

                candidate = new_candidate
                write_json(workspace / f"version_sim_{sim_attempt:02d}.json", candidate)

            # Update best_candidate as final_candidate
            result["final_candidate"] = best_candidate
            result["selftest_evaluation"] = {
                "candidate_sha256": digest(normalize_candidate(best_candidate)),
                "cases_sha256": digest(active_cases),
                "status": result["status"],
                "evaluated_cases": len(active_cases) if best_was_simulated else 0,
                "passed_cases": max(0, best_score[2]) if best_was_simulated else 0,
            }
        else:
            result["final_candidate"] = best_candidate

    except ProviderError as exc:
        if result.get("final_compiled") and best_candidate is not None:
            result["final_candidate"] = best_candidate
            if result.get("status") not in ("PASS", "TEST_FAIL"):
                result["status"] = "UNVERIFIED"
            result["reason"] = f"Provider limit/error after valid compilation preserved best_candidate: {exc}"
        else:
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
        # Successful and failed provider responses are both billable. The client
        # journal/terminal responses are the source of truth, not return count.
        if hasattr(client, "request_count"):
            result["llm_calls"] = client.request_count
            result["accounted_tokens"] = client.total_tokens
            result["usage"] = []
            for response_path in sorted(workspace.glob("llm_*/response.json")):
                terminal = json.loads(response_path.read_text(encoding="utf-8-sig"))
                if terminal.get("usage"):
                    result["usage"].append(terminal["usage"])
        result["elapsed_seconds"] = time.monotonic() - started
        result["finished_utc"] = now()
        if result.get("final_candidate") is not None:
            try:
                write_json(workspace / "final_candidate.json", result["final_candidate"])
            except Exception:
                pass
        try:
            write_json(workspace / "result.json", result)
        except Exception:
            pass

    return result
