"""Tests for the stateless STAR PLC Agent harness."""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from plc_agent.backend import FakeBackend, SimCaseFailure, SimResult
from plc_agent.compiler import CompileResult
from plc_agent.config import Settings
from plc_agent.harness import compact_diagnostics, run_harness

SAMPLE_TASK = {
    "id": "TASK_TEST",
    "title": "Dual Conveyor Controller",
    "difficulty": "Medium",
    "requirements": "Control two motors with safety interlock",
    "scenario": "Conveyor sorting line",
    "interface": [
        {"name": "start", "type": "BOOL", "direction": "INPUT"},
        {"name": "stop", "type": "BOOL", "direction": "INPUT"},
        {"name": "m1", "type": "BOOL", "direction": "OUTPUT"},
        {"name": "m2", "type": "BOOL", "direction": "OUTPUT"},
    ],
    "data_types": [],
    "supporting_types": [],
    "initial_conditions": {"m1": False, "m2": False},
    "scan_semantics": "Cyclic 10ms",
    "safety_priority": "Stop overrides start",
    "assumptions": "Standard IEC 61131-3",
    "ltl": ["G(stop -> !m1)"],
    "atomic_propositions": {"stop": "stop = TRUE", "m1": "m1 = TRUE"},
    # Hidden forbidden keys
    "tests": [
        {
            "id": "TC01",
            "steps": [
                {"inputs": {"start": True, "stop": False}, "expected": {"m1": True, "m2": False}},
            ],
        }
    ],
    "test_bindings": {"TC01": "binding_secret"},
    "specification_contract": {"contract_secret": "FORBIDDEN_SPEC_CONTRACT"},
    "provenance": {"benchmark_author": "secret"},
}


class MockLLMClient:
    def __init__(self, responses: list[str] | None = None):
        self.responses = list(responses or [])
        self.recorded_calls: list[dict] = []
        self.call_count = 0

    def respond(self, model, input_items, log_dir, tools=None, tool_choice=None, max_tokens=None, timeout=None):
        self.call_count += 1
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        self.recorded_calls.append({
            "model": model,
            "input": copy.deepcopy(input_items),
            "log_dir": log_dir,
        })
        text = self.responses.pop(0) if self.responses else json.dumps({
            "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT start, stop: BOOL; END_VAR\nVAR_OUTPUT m1, m2: BOOL; END_VAR",
            "implementation": "m1 := start AND NOT stop;\nm2 := FALSE;",
            "supporting_objects": [],
        })
        return {
            "text": text,
            "output": [],
            "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
            "elapsed_seconds": 0.1,
            "reported_model": model,
            "cost": None,
        }


class StarHarnessTests(unittest.TestCase):
    def test_compact_diagnostics_handles_lineless_and_out_of_range(self):
        candidate = {
            "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT\n    start : BOOL;\nEND_VAR",
            "implementation": "line1 := 1;\nline2 := 2;\nline3 := 3;\nline4 := 4;\nline5 := 5;",
            "supporting_objects": [],
        }
        diagnostics = [
            {"severity": "Error", "text": "Undefined variable line3", "position": "Line 3, Column 1"},
            # Duplicate diagnostic - should be deduplicated
            {"severity": "Error", "text": "Undefined variable line3", "position": "Line 3, Column 1"},
            # Missing / None position
            {"severity": "Error", "text": "Global syntax failure", "position": None},
            {"severity": "Warning", "text": "Unused variable", "position": ""},
            # Out of range line number
            {"severity": "Error", "text": "Out of range line error", "position": "Line 9999, Column 4"},
            # Negative line
            {"severity": "Error", "text": "Negative line error", "position": "Line -5"},
        ]
        compact = compact_diagnostics(candidate, diagnostics, window=2, max_chars=1000)
        self.assertIsInstance(compact, str)
        # Verify deduplication: "Undefined variable line3" appears exactly once
        self.assertEqual(compact.count("Undefined variable line3"), 1)
        # Verify line context is present for valid line 3
        self.assertIn("line3 := 3;", compact)
        self.assertIn("line2 := 2;", compact)
        # Verify missing positions and out-of-range lines do not crash and are included
        self.assertIn("Global syntax failure", compact)
        self.assertIn("Out of range line error", compact)

        # Verify max_chars capping
        capped = compact_diagnostics(candidate, diagnostics, window=2, max_chars=50)
        self.assertLessEqual(len(capped), 50)

    def test_zero_test_leakage_and_leak_free_prompts(self):
        client = MockLLMClient()
        settings = Settings()
        backend = FakeBackend()
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "run"
            res = run_harness(SAMPLE_TASK, "mock-model", ws, client, settings, backend=backend)
            self.assertIsNotNone(res)

            # Check all prompts sent to LLM across planner, coder, tester, etc.
            self.assertGreater(len(client.recorded_calls), 0)
            for call in client.recorded_calls:
                for item in call["input"]:
                    content = str(item.get("content", ""))
                    self.assertNotIn("FORBIDDEN_SPEC_CONTRACT", content)
                    self.assertNotIn("specification_contract", content)
                    self.assertNotIn("TC01", content)
                    self.assertNotIn("binding_secret", content)
                    self.assertNotIn("benchmark_author", content)

    def test_hash_stagnation_detection(self):
        # Initial code fails compile; repair returns exact same code (hash stagnation)
        stagnant_code = json.dumps({
            "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT start, stop: BOOL; END_VAR\nVAR_OUTPUT m1, m2: BOOL; END_VAR",
            "implementation": "syntax error bad code",
            "supporting_objects": [],
        })
        client = MockLLMClient(responses=[
            json.dumps({"state_machine": ["IDLE"]}),  # planner
            stagnant_code,  # coder version 0
            stagnant_code,  # repair 1 (same hash)
            stagnant_code,  # repair 2
        ])
        compile_fail = CompileResult(
            status="COMPILE_FAIL",
            success=False,
            diagnostics=[{"severity": "Error", "text": "Syntax error", "position": "Line 1"}],
        )
        backend = FakeBackend(compile_fn=lambda *args, **kwargs: compile_fail)
        settings = Settings(max_repairs=2)
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "run"
            run_harness(SAMPLE_TASK, "mock-model", ws, client, settings, backend=backend)

            # At least one prompt after repair 1 must include stagnation warning
            found_stagnation_warning = False
            for call in client.recorded_calls:
                for item in call["input"]:
                    content = str(item.get("content", ""))
                    if "stagnat" in content.lower():
                        found_stagnation_warning = True
                        break
            self.assertTrue(found_stagnation_warning, "Expected code stagnation warning in repair prompt")

    def test_rejection_cap_and_lexicographic_ratchet(self):
        # Planner response
        plan_resp = json.dumps({"state_machine": ["IDLE"]})
        # Initial Coder response: passes compile, passes 1 of 4 cases
        cand_0 = json.dumps({
            "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT start, stop: BOOL; END_VAR\nVAR_OUTPUT m1, m2: BOOL; END_VAR",
            "implementation": "m1 := start;\nm2 := FALSE;",
            "supporting_objects": [],
        })
        # Tester response: 4 test cases
        tester_resp = json.dumps([
            {"id": "case_1", "steps": [{"inputs": {"start": True, "stop": False}, "expected": {"m1": True, "m2": False}}]},
            {"id": "case_2", "steps": [{"inputs": {"start": False, "stop": True}, "expected": {"m1": False, "m2": False}}]},
            {"id": "case_3", "steps": [{"inputs": {"start": True, "stop": True}, "expected": {"m1": False, "m2": False}}]},
            {"id": "case_4", "steps": [{"inputs": {"start": False, "stop": False}, "expected": {"m1": False, "m2": False}}]},
        ])
        # Behavioral repair 1: attempts to reject 3 cases (over 50% cap of 4//2 = 2) + provides cand_1 (uncompilable)
        cand_uncompilable = json.dumps({
            "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT start, stop: BOOL; END_VAR\nVAR_OUTPUT m1, m2: BOOL; END_VAR",
            "implementation": "THIS IS UNCOMPILABLE SYNTAX ERROR",
            "supporting_objects": [],
            "reject_cases": [
                {"id": "case_2", "reason": "flawed"},
                {"id": "case_3", "reason": "flawed"},
                {"id": "case_4", "reason": "flawed"},  # Exceeds cap (max 2 allowed)
            ],
        })
        # Behavioral repair 2: provides cand_2 (compiles but passes 0 cases - regression!)
        cand_regressed = json.dumps({
            "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT start, stop: BOOL; END_VAR\nVAR_OUTPUT m1, m2: BOOL; END_VAR",
            "implementation": "m1 := FALSE;\nm2 := FALSE;",
            "supporting_objects": [],
        })

        client = MockLLMClient(responses=[
            plan_resp,
            cand_0,
            tester_resp,
            cand_uncompilable,
            cand_regressed,
        ])

        compile_pass = CompileResult(status="PASS", success=True)
        compile_fail = CompileResult(status="COMPILE_FAIL", success=False)

        def mock_compile(task, candidate, workspace):
            if "UNCOMPILABLE" in str(candidate):
                return compile_fail
            return compile_pass

        # Simulation behavior:
        # cand_0 passes case_1 only (1 pass out of active)
        # cand_regressed passes 0 cases
        def mock_simulate(task, candidate, cases, workspace):
            passed = 0
            failures = []
            for c in cases:
                if c["id"] == "case_1" and "m1 := start" in str(candidate):
                    passed += 1
                else:
                    failures.append(SimCaseFailure(
                        case_id=c["id"],
                        first_bad_step=0,
                        field="m1",
                        expected=True,
                        observed=False,
                        inputs_prefix=[c["steps"][0]["inputs"]],
                    ))
            status = "PASS" if passed == len(cases) else "TEST_FAIL"
            return SimResult(status=status, passed_cases=passed, evaluated_cases=len(cases), failures=failures)

        backend = FakeBackend(compile_fn=mock_compile)
        backend.simulate = mock_simulate  # override simulate

        settings = Settings(max_simulations=3, max_repairs=3)
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "run"
            result = run_harness(SAMPLE_TASK, "mock-model", ws, client, settings, backend=backend)

            # Rejection cap check: 4 valid cases -> max 2 rejections allowed
            self.assertLessEqual(len(result["selftest_rejected"]), 2)
            # Exactly 2 were accepted
            self.assertEqual(len(result["selftest_rejected"]), 2)

            # Lexicographic ratchet check:
            # cand_uncompilable was rejected because uncompilable (False, 0) < (True, 1)
            # cand_regressed was rejected because (True, 0) < (True, 1)
            # Best candidate remains cand_0
            self.assertIn("m1 := start;", result["final_candidate"]["implementation"])
            self.assertTrue(result["final_compiled"])

    def test_budget_enforcement(self):
        # Test compiler limit (max 4 compiles) and simulation limit (max 3) and LLM calls (max 9)
        client = MockLLMClient()
        settings = Settings(max_repairs=3, max_simulations=3, max_llm_calls=9)
        compile_counts = [0]

        def counting_compile(*args, **kwargs):
            compile_counts[0] += 1
            return CompileResult(status="COMPILE_FAIL", success=False, diagnostics=[{"severity": "Error", "text": "err"}])

        backend = FakeBackend(compile_fn=counting_compile)
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "run"
            result = run_harness(SAMPLE_TASK, "mock-model", ws, client, settings, backend=backend)

            self.assertLessEqual(result["compiler_call_count"], 4)
            self.assertLessEqual(result["simulation_call_count"], 3)
            self.assertLessEqual(result["llm_calls"], 9)
            self.assertEqual(result["final_compiled"], False)

    def test_ablations(self):
        # Test ablation="no_planner"
        client = MockLLMClient()
        settings = Settings()
        backend = FakeBackend()
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "run"
            res = run_harness(SAMPLE_TASK, "mock-model", ws, client, settings, backend=backend, ablation="no_planner")
            plan_file = ws / "plan.json"
            self.assertTrue(plan_file.is_file())
            self.assertEqual(json.loads(plan_file.read_text(encoding="utf-8")), {})

        # Test ablation="no_dialect"
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "run"
            res = run_harness(SAMPLE_TASK, "mock-model", ws, client, settings, backend=backend, ablation="no_dialect")
            cards_file = ws / "dialect_cards.json"
            self.assertTrue(cards_file.is_file())
            self.assertEqual(json.loads(cards_file.read_text(encoding="utf-8")), [])

        # Test ablation="no_selftest"
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "run"
            res = run_harness(SAMPLE_TASK, "mock-model", ws, client, settings, backend=backend, ablation="no_selftest")
            selftest_file = ws / "selftest.json"
            self.assertTrue(selftest_file.is_file())
            self.assertEqual(json.loads(selftest_file.read_text(encoding="utf-8")), [])
            self.assertEqual(res["simulation_call_count"], 0)


if __name__ == "__main__":
    unittest.main()
