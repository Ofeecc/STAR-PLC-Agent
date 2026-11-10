"""Manually fixed expected traces versus independent Python state machines."""
import json
from pathlib import Path
import unittest
from plc_agent.reference import ReferenceController, evaluate_reference


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
        task = {"id": "SELF001", "tests": [{"id": "mutation", "steps": [
            {"inputs": {"Start": True, "Stop": True, "GuardClosed": True}, "expected": {"Run": True}}
        ]}]}
        self.assertFalse(evaluate_reference(task)["passed"])


if __name__ == "__main__":
    unittest.main()
