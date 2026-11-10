"""Tests for baseline suite (deepseek_harness, codex_cli, claude_code) and dual-tool MCP server."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from plc_agent.backend import FakeBackend, SimCaseFailure, SimResult
from plc_agent.baseline import run_baseline
from plc_agent.compiler import CompileResult
from plc_agent.config import Settings
from plc_agent.mcp_server import dispatch


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
    "test_bindings": {"TC01": "secret_test_binding"},
    "specification_contract": {"contract_secret": "FORBIDDEN_SPEC_CONTRACT"},
    "provenance": {"benchmark_author": "secret"},
}

SAMPLE_CANDIDATE = {
    "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT start, stop: BOOL; END_VAR\nVAR_OUTPUT m1, m2: BOOL; END_VAR",
    "implementation": "m1 := start AND NOT stop;\nm2 := FALSE;",
    "supporting_objects": [],
}


class FakeToolClient:
    def __init__(self, actions: list[dict] | None = None):
        self.actions = list(actions or [])
        self.recorded_calls: list[dict] = []

    def respond(self, model, input_items, log_dir, tools=None, tool_choice=None, max_tokens=None, timeout=None):
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        self.recorded_calls.append({
            "model": model,
            "input": copy.deepcopy(input_items),
            "tools": tools,
            "log_dir": log_dir,
        })
        if self.actions:
            return self.actions.pop(0)
        return {
            "text": "Completed task successfully.",
            "output": [{"type": "message", "content": [{"type": "output_text", "text": "Completed task successfully."}]}],
            "usage": {"prompt_tokens": 50, "completion_tokens": 20, "total_tokens": 70},
        }


class BaselineAndMCPTests(unittest.TestCase):
    def test_mcp_server_exposes_compile_and_simulate_tools(self):
        with tempfile.TemporaryDirectory() as tmp:
            trusted = Path(tmp) / "trusted"
            trusted.mkdir()
            settings = Settings(max_repairs=3, max_simulations=3)
            result = dispatch({"method": "tools/list"}, SAMPLE_TASK, trusted, settings)
            tools = result.get("tools", [])
            tool_names = [t["name"] for t in tools]
            self.assertIn("compile_st", tool_names)
            self.assertIn("simulate_st", tool_names)

    def test_mcp_server_compile_and_simulate_execution_with_backend(self):
        with tempfile.TemporaryDirectory() as tmp:
            trusted = Path(tmp) / "trusted"
            trusted.mkdir()
            settings = Settings(max_repairs=3, max_simulations=3)
            backend = FakeBackend(
                step_fn=lambda inp, dt=None: {"m1": inp.get("start", False) and not inp.get("stop", False), "m2": False}
            )

            # Compile call
            compile_msg = {
                "method": "tools/call",
                "params": {"name": "compile_st", "arguments": {"source": SAMPLE_CANDIDATE}},
            }
            c_resp = dispatch(compile_msg, SAMPLE_TASK, trusted, settings, backend=backend)
            self.assertFalse(c_resp["isError"])
            c_data = json.loads(c_resp["content"][0]["text"])
            self.assertTrue(c_data["success"])
            self.assertEqual(c_data["status"], "PASS")
            self.assertTrue((trusted / "compile_00" / "compile_result.json").exists())

            # Simulate call
            sim_cases = [
                {
                    "id": "self_1",
                    "steps": [
                        {"inputs": {"start": True, "stop": False}, "expected": {"m1": True, "m2": False}},
                    ],
                }
            ]
            sim_msg = {
                "method": "tools/call",
                "params": {"name": "simulate_st", "arguments": {"source": SAMPLE_CANDIDATE, "cases": sim_cases}},
            }
            s_resp = dispatch(sim_msg, SAMPLE_TASK, trusted, settings, backend=backend)
            self.assertFalse(s_resp["isError"])
            s_data = json.loads(s_resp["content"][0]["text"])
            self.assertEqual(s_data["status"], "PASS")
            self.assertEqual(s_data["passed_cases"], 1)
            self.assertTrue((trusted / "sim_00" / "simulation_result.json").exists())

    def test_mcp_server_strictly_blocks_exceeded_budgets(self):
        with tempfile.TemporaryDirectory() as tmp:
            trusted = Path(tmp) / "trusted"
            trusted.mkdir()
            settings = Settings(max_repairs=1, max_simulations=1)
            backend = FakeBackend()

            # Compile calls: max_repairs=1 means max 2 calls (compile_00 and compile_01)
            compile_msg = {
                "method": "tools/call",
                "params": {"name": "compile_st", "arguments": {"source": SAMPLE_CANDIDATE}},
            }
            c1 = dispatch(compile_msg, SAMPLE_TASK, trusted, settings, backend=backend)
            self.assertFalse(c1["isError"])
            c2 = dispatch(compile_msg, SAMPLE_TASK, trusted, settings, backend=backend)
            self.assertFalse(c2["isError"])
            c3 = dispatch(compile_msg, SAMPLE_TASK, trusted, settings, backend=backend)
            self.assertTrue(c3["isError"])
            self.assertIn("Compilation budget exhausted", c3["content"][0]["text"])

            # Simulation calls: max_simulations=1 means max 1 call (sim_00)
            sim_cases = [
                {
                    "id": "self_1",
                    "steps": [
                        {"inputs": {"start": True, "stop": False}, "expected": {"m1": True, "m2": False}},
                    ],
                }
            ]
            sim_msg = {
                "method": "tools/call",
                "params": {"name": "simulate_st", "arguments": {"source": SAMPLE_CANDIDATE, "cases": sim_cases}},
            }
            s1 = dispatch(sim_msg, SAMPLE_TASK, trusted, settings, backend=backend)
            self.assertFalse(s1["isError"])
            s2 = dispatch(sim_msg, SAMPLE_TASK, trusted, settings, backend=backend)
            self.assertTrue(s2["isError"])
            self.assertIn("Simulation budget exhausted", s2["content"][0]["text"])

    def test_mcp_server_validates_test_cases_rejects_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            trusted = Path(tmp) / "trusted"
            trusted.mkdir()
            settings = Settings(max_repairs=3, max_simulations=3)
            backend = FakeBackend()

            # Invalid case with non-existent field
            invalid_cases = [
                {
                    "id": "bad_case",
                    "steps": [
                        {"inputs": {"non_existent_input": True}, "expected": {"m1": True}},
                    ],
                }
            ]
            sim_msg = {
                "method": "tools/call",
                "params": {"name": "simulate_st", "arguments": {"source": SAMPLE_CANDIDATE, "cases": invalid_cases}},
            }
            resp = dispatch(sim_msg, SAMPLE_TASK, trusted, settings, backend=backend)
            self.assertTrue(resp["isError"])

    def test_mcp_server_truncates_failures_to_first_bad_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            trusted = Path(tmp) / "trusted"
            trusted.mkdir()
            settings = Settings(max_repairs=3, max_simulations=3)
            # Backend outputs m1=False always
            backend = FakeBackend(
                step_fn=lambda inp, dt=None: {"m1": False, "m2": False}
            )

            # 3-step test case: step 0 expects False (passes), step 1 expects True (fails), step 2 expects True
            cases = [
                {
                    "id": "multi_step_case",
                    "steps": [
                        {"inputs": {"start": False, "stop": False}, "expected": {"m1": False, "m2": False}},
                        {"inputs": {"start": True, "stop": False}, "expected": {"m1": True, "m2": False}},
                        {"inputs": {"start": True, "stop": False}, "expected": {"m1": True, "m2": False}},
                    ],
                }
            ]
            sim_msg = {
                "method": "tools/call",
                "params": {"name": "simulate_st", "arguments": {"source": SAMPLE_CANDIDATE, "cases": cases}},
            }
            s_resp = dispatch(sim_msg, SAMPLE_TASK, trusted, settings, backend=backend)
            self.assertFalse(s_resp["isError"])
            s_data = json.loads(s_resp["content"][0]["text"])
            self.assertEqual(s_data["status"], "TEST_FAIL")
            self.assertEqual(len(s_data["failures"]), 1)
            fail = s_data["failures"][0]
            self.assertEqual(fail["first_bad_step"], 1)
            self.assertEqual(fail["field"], "m1")
            self.assertEqual(fail["expected"], True)
            self.assertEqual(fail["observed"], False)
            # inputs_prefix must only contain step 0 and step 1; step 2 is truncated
            self.assertEqual(len(fail["inputs_prefix"]), 2)

    def test_deepseek_harness_baseline_tool_loop_and_counters(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "ws"
            settings = Settings(max_repairs=2, max_simulations=2)
            backend = FakeBackend(
                step_fn=lambda inp, dt=None: {"m1": inp.get("start", False) and not inp.get("stop", False), "m2": False}
            )

            # Scripted responses:
            # Turn 1: call compile_st
            # Turn 2: call simulate_st
            # Turn 3: final completion text
            actions = [
                {
                    "text": "",
                    "output": [
                        {
                            "type": "function_call",
                            "name": "compile_st",
                            "arguments": json.dumps({"source": SAMPLE_CANDIDATE}),
                            "call_id": "call_c1",
                        }
                    ],
                    "usage": {"prompt_tokens": 100, "completion_tokens": 30, "total_tokens": 130},
                },
                {
                    "text": "",
                    "output": [
                        {
                            "type": "function_call",
                            "name": "simulate_st",
                            "arguments": json.dumps({
                                "source": SAMPLE_CANDIDATE,
                                "cases": [
                                    {
                                        "id": "s1",
                                        "steps": [{"inputs": {"start": True, "stop": False}, "expected": {"m1": True, "m2": False}}],
                                    }
                                ],
                            }),
                            "call_id": "call_s1",
                        }
                    ],
                    "usage": {"prompt_tokens": 150, "completion_tokens": 40, "total_tokens": 190},
                },
                {
                    "text": "Implementation confirmed. Candidate is ready.",
                    "output": [
                        {
                            "type": "message",
                            "content": [{"type": "output_text", "text": "Implementation confirmed. Candidate is ready."}],
                        }
                    ],
                    "usage": {"prompt_tokens": 200, "completion_tokens": 20, "total_tokens": 220},
                },
            ]
            client = FakeToolClient(actions)

            result = run_baseline(
                task=SAMPLE_TASK,
                model="deepseek-coder",
                workspace=workspace,
                settings=settings,
                condition="E1",
                driver="deepseek_harness",
                client=client,
                backend=backend,
            )

            self.assertEqual(result["compiler_call_count"], 1)
            self.assertEqual(result["simulation_call_count"], 1)
            self.assertEqual(result["tool_call_count"], 2)
            self.assertEqual(result["llm_calls"], 3)
            self.assertTrue(result["final_compiled"])
            self.assertEqual(result["status"], "UNVERIFIED")
            self.assertEqual(len(result["usage"]), 3)
            self.assertTrue((workspace / "final_candidate.json").exists())

    def test_deepseek_harness_zero_test_leakage(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "ws"
            settings = Settings()
            client = FakeToolClient([])

            run_baseline(
                task=SAMPLE_TASK,
                model="deepseek-coder",
                workspace=workspace,
                settings=settings,
                condition="E1",
                driver="deepseek_harness",
                client=client,
            )

            # Check recorded calls to LLM
            forbidden = ["TC01", "secret_test_binding", "FORBIDDEN_SPEC_CONTRACT", "benchmark_author"]
            for call in client.recorded_calls:
                call_str = json.dumps(call, default=str)
                for f in forbidden:
                    self.assertNotIn(f, call_str, f"Forbidden key leaked to LLM: {f}")

            # Check all files in workspace
            for p in workspace.rglob("*"):
                if p.is_file() and p.suffix in (".json", ".txt", ".log", ".jsonl"):
                    content = p.read_text(encoding="utf-8", errors="replace")
                    for f in forbidden:
                        self.assertNotIn(f, content, f"Forbidden key leaked in workspace file {p}: {f}")

    def test_missing_cli_executables_set_tool_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws_codex = Path(tmp) / "ws_codex"
            ws_claude = Path(tmp) / "ws_claude"
            settings = Settings()

            res_codex = run_baseline(SAMPLE_TASK, "model", ws_codex, settings, driver="codex_cli")
            self.assertEqual(res_codex["status"], "TOOL_ERROR")
            self.assertIn("Codex CLI executable missing", res_codex["reason"])

            res_claude = run_baseline(SAMPLE_TASK, "model", ws_claude, settings, driver="claude_code")
            self.assertEqual(res_claude["status"], "TOOL_ERROR")
            self.assertIn("Claude CLI executable missing", res_claude["reason"])


if __name__ == "__main__":
    unittest.main()
