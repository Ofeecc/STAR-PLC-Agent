"""Manually fixed expected traces versus independent Python state machines."""

import json
import tempfile
import unittest
from pathlib import Path

from plc_agent.backend import FakeBackend
from plc_agent.compiler import normalize_candidate
from plc_agent.dataset import load_tasks
from plc_agent.reference import ReferenceController, evaluate_reference
from plc_agent.simulation import build_program

ROOT = Path(__file__).resolve().parents[1]


class ReferenceTests(unittest.TestCase):
    def test_every_self_task_has_an_oracle_and_matches_manual_expectations(self):
        files = sorted((ROOT / "dataset/self_built").glob("SELF*.json"))
        self.assertGreaterEqual(len(files), 12)
        for path in files:
            with self.subTest(task=path.stem):
                result = evaluate_reference(json.loads(path.read_text(encoding="utf-8")))
                self.assertTrue(result["passed"], result)
                self.assertEqual(result["evidence"], "PYTHON_REFERENCE_ONLY")

    def test_all_sixteen_codesys_examples_normalize_and_pass_scan_contract_simulation(self):
        example_files = sorted((ROOT / "codesys/examples").glob("*.json"))
        self.assertEqual(len(example_files), 16)
        expected_ids = {f"SELF{i:03d}" for i in range(1, 13)} | {"PUB006", "PUB007", "PUB017", "PUB018"}
        self.assertEqual({f.stem for f in example_files}, expected_ids)

        tasks = {t["id"]: t for t in load_tasks()}
        backend = FakeBackend()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            for path in example_files:
                task_id = path.stem
                with self.subTest(example=task_id):
                    self.assertIn(task_id, tasks)
                    task = tasks[task_id]
                    raw_example = json.loads(path.read_text(encoding="utf-8"))

                    normalized = normalize_candidate(raw_example)
                    self.assertIn("declaration", normalized)
                    self.assertIn("implementation", normalized)
                    self.assertIsInstance(normalized["supporting_objects"], list)

                    program = build_program(task)
                    self.assertGreater(program["step_count"], 0)
                    self.assertIn("PROGRAM PLC_PRG", program["declaration"])

                    sim_res = backend.simulate(task, normalized, task["tests"], tmp_path)
                    self.assertEqual(sim_res.status, "PASS", f"{task_id} failed: {sim_res}")
                    self.assertEqual(sim_res.passed_cases, len(task["tests"]))
                    self.assertEqual(len(sim_res.failures), 0)

    def test_rejects_unknown_tasks(self):
        with self.assertRaises(ValueError):
            ReferenceController("PUB001")

    def test_reset_creates_isolated_retained_state(self):
        running = ReferenceController("SELF001")
        running.step({"Start": True, "Stop": False, "GuardClosed": True})
        fresh = ReferenceController("SELF001")
        observed = fresh.step({"Start": False, "Stop": False, "GuardClosed": True})
        self.assertFalse(observed["Run"])
        self.assertTrue(running.state["run"])

    def test_fault_recovery_requires_two_healthy_wait_scans(self):
        feeder = ReferenceController("SELF012")
        defaults = {"Start": False, "Stop": False, "Fault": False, "Reset": False}
        self.assertTrue(feeder.step({**defaults, "Start": True})["Run"])
        self.assertFalse(feeder.step({**defaults, "Fault": True})["Run"])
        self.assertFalse(feeder.step(defaults)["Run"])
        # A renewed fault invalidates the first healthy wait observation.
        self.assertFalse(feeder.step({**defaults, "Fault": True})["Run"])
        self.assertFalse(feeder.step(defaults)["Run"])
        restart = feeder.step(defaults)
        self.assertTrue(restart["Run"])
        self.assertEqual(restart["Attempts"], 1)

    def test_expected_trace_mutation_is_detected(self):
        task = {
            "id": "SELF001",
            "tests": [
                {
                    "id": "mutation",
                    "steps": [
                        {"inputs": {"Start": True, "Stop": True, "GuardClosed": True}, "expected": {"Run": True}}
                    ],
                }
            ],
        }
        self.assertFalse(evaluate_reference(task)["passed"])


if __name__ == "__main__":
    unittest.main()
