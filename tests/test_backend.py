import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from plc_agent.backend import Backend, CodesysBackend, FakeBackend, SimCaseFailure, SimResult
from plc_agent.compiler import CompileResult
from plc_agent.config import Settings
from plc_agent.dataset import load_tasks


class BackendTests(unittest.TestCase):
    def test_backend_protocol_conformity(self):
        backend_fake = FakeBackend()
        backend_codesys = CodesysBackend(Settings())
        self.assertIsInstance(backend_fake, Backend)
        self.assertIsInstance(backend_codesys, Backend)
        self.assertTrue(callable(backend_fake.compile))
        self.assertTrue(callable(backend_fake.simulate))
        self.assertTrue(callable(backend_codesys.compile))
        self.assertTrue(callable(backend_codesys.simulate))

    def test_fake_backend_truncates_failure_to_first_diverging_step(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        # Step 0 in SELF001: Start=False, Stop=False, GuardClosed=True -> Run=False.
        # Step 1 in SELF001: Start=True, Stop=False, GuardClosed=True -> Run=True.
        # Returning {"Run": False} will match step 0 and diverge at step 1.
        backend = FakeBackend(step_fn=lambda inputs, dt_ms=None: {"Run": False})
        with tempfile.TemporaryDirectory() as tmp:
            sim = backend.simulate(
                task,
                {"declaration": "FUNCTION_BLOCK FB_Task\nVAR END_VAR", "implementation": "Run := FALSE;"},
                task["tests"],
                Path(tmp),
            )
            self.assertEqual(sim.status, "TEST_FAIL")
            self.assertEqual(sim.passed_cases, 0)
            self.assertGreaterEqual(len(sim.failures), 1)
            failure = sim.failures[0]
            self.assertEqual(failure.case_id, task["tests"][0]["id"])
            self.assertEqual(failure.first_bad_step, 1)
            self.assertEqual(failure.field, "Run")
            self.assertEqual(failure.expected, True)
            self.assertEqual(failure.observed, False)
            self.assertEqual(len(failure.inputs_prefix), failure.first_bad_step + 1)
            self.assertEqual(failure.inputs_prefix[0], task["tests"][0]["steps"][0]["inputs"])
            self.assertEqual(failure.inputs_prefix[1], task["tests"][0]["steps"][1]["inputs"])

    def test_fake_backend_none_step_fn_passes_valid_task(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        backend = FakeBackend(step_fn=None)
        with tempfile.TemporaryDirectory() as tmp:
            sim = backend.simulate(
                task,
                {"declaration": "FUNCTION_BLOCK FB_Task\nVAR END_VAR", "implementation": ""},
                task["tests"],
                Path(tmp),
            )
            self.assertEqual(sim.status, "PASS")
            self.assertEqual(sim.passed_cases, len(task["tests"]))
            self.assertEqual(sim.evaluated_cases, len(task["tests"]))
            self.assertEqual(sim.failures, [])
            self.assertIsNone(sim.infrastructure_error)

    def test_fake_backend_compilation_error_simulation(self):
        def mock_compile(*args, **kwargs):
            return CompileResult(
                status="COMPILE_FAIL",
                success=False,
                backend="FAKE",
                diagnostics=[{"severity": "error", "text": "Syntax error at line 3"}],
            )

        backend = FakeBackend(compile_fn=mock_compile)
        with tempfile.TemporaryDirectory() as tmp:
            res = backend.compile({"id": "SELF001"}, "invalid st", Path(tmp))
            self.assertEqual(res.status, "COMPILE_FAIL")
            self.assertFalse(res.success)
            self.assertEqual(len(res.diagnostics), 1)

        # Default compile without compile_fn returns PASS
        backend_default = FakeBackend()
        with tempfile.TemporaryDirectory() as tmp:
            cand = {"declaration": "FUNCTION_BLOCK FB_Task\nVAR END_VAR", "implementation": ""}
            res_default = backend_default.compile({"id": "SELF001"}, cand, Path(tmp))
            self.assertEqual(res_default.status, "PASS")
            self.assertTrue(res_default.success)

    def test_codesys_backend_instantiation_and_interface(self):
        settings = Settings()
        backend = CodesysBackend(settings)
        self.assertEqual(backend.settings, settings)
        self.assertTrue(hasattr(backend, "compile"))
        self.assertTrue(hasattr(backend, "simulate"))

    def test_codesys_backend_simulate_parses_run_functional_failure(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        settings = Settings()
        backend = CodesysBackend(settings)

        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp)
            # Create a mock trace.json in ws
            case0 = task["tests"][0]
            trace = {
                "task_id": "SELF001",
                "cases": {
                    case0["id"]: [
                        {"inputs": case0["steps"][0]["inputs"], "outputs": {"Run": False}},
                        {"inputs": case0["steps"][1]["inputs"], "outputs": {"Run": False}},  # expected True
                    ]
                },
            }
            (ws / "trace.json").write_text(json.dumps(trace), encoding="utf-8")

            mock_raw = {
                "status": "TEST_FAIL",
                "trace_path": str(ws / "trace.json"),
                "functional": {
                    "status": "TEST_FAIL",
                    "passed_cases": 0,
                    "evaluated_cases": 1,
                    "details": [
                        {
                            "case_id": case0["id"],
                            "status": "TEST_FAIL",
                            "steps_passed": [True, False],
                        }
                    ],
                },
            }

            with patch("plc_agent.backend.run_functional", return_value=mock_raw):
                sim = backend.simulate(
                    task,
                    {"declaration": "FUNCTION_BLOCK FB_Task\nVAR END_VAR", "implementation": ""},
                    [case0],
                    ws,
                )
                self.assertEqual(sim.status, "TEST_FAIL")
                self.assertEqual(sim.passed_cases, 0)
                self.assertEqual(sim.evaluated_cases, 1)
                self.assertEqual(len(sim.failures), 1)
                f = sim.failures[0]
                self.assertEqual(f.case_id, case0["id"])
                self.assertEqual(f.first_bad_step, 1)
                self.assertEqual(f.field, "Run")
                self.assertEqual(f.expected, True)
                self.assertEqual(f.observed, False)
                self.assertEqual(len(f.inputs_prefix), 2)

    def test_failure_never_leaks_subsequent_steps(self):
        # Synthetic case with 5 steps: step 0 and 1 match, step 2 diverges
        synthetic_task = {
            "id": "SYNTH001",
            "interface": [
                {"direction": "INPUT", "name": "InVal", "type": "INT"},
                {"direction": "OUTPUT", "name": "OutVal", "type": "INT"},
            ],
            "tests": [
                {
                    "id": "SYNTH001.01",
                    "steps": [
                        {"inputs": {"InVal": 1}, "expected": {"OutVal": 10}},
                        {"inputs": {"InVal": 2}, "expected": {"OutVal": 20}},
                        {"inputs": {"InVal": 3}, "expected": {"OutVal": 30}},
                        {"inputs": {"InVal": 4}, "expected": {"OutVal": 40}},
                        {"inputs": {"InVal": 5}, "expected": {"OutVal": 50}},
                    ],
                }
            ],
        }

        call_log = []

        def tracking_step_fn(inputs, dt_ms=None):
            val = inputs["InVal"]
            call_log.append(val)
            if val == 3:
                return {"OutVal": 999}  # Divergence at step index 2
            return {"OutVal": val * 10}

        backend = FakeBackend(step_fn=tracking_step_fn)
        with tempfile.TemporaryDirectory() as tmp:
            sim = backend.simulate(
                synthetic_task,
                {"declaration": "FUNCTION_BLOCK FB_Task\nVAR END_VAR", "implementation": ""},
                synthetic_task["tests"],
                Path(tmp),
            )
            self.assertEqual(sim.status, "TEST_FAIL")
            self.assertEqual(len(sim.failures), 1)
            fail = sim.failures[0]
            self.assertEqual(fail.first_bad_step, 2)
            self.assertEqual(fail.field, "OutVal")
            self.assertEqual(fail.expected, 30)
            self.assertEqual(fail.observed, 999)
            # Only inputs for step 0, 1, 2 must be in inputs_prefix (3 total)
            self.assertEqual(len(fail.inputs_prefix), 3)
            self.assertEqual([s["InVal"] for s in fail.inputs_prefix], [1, 2, 3])
            # Step function must NOT have been called for steps after the divergence (steps 4 and 5)
            self.assertEqual(call_log, [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
