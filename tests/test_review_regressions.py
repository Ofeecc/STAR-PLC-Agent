"""Independent offline review regressions; all traces are temporary test doubles.

Synthetic artifacts in this module are not CODESYS execution evidence and are
never written under the benchmark results directory.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from plc_agent.common import digest
from plc_agent.functional import evaluate_trace
from plc_agent.harness import empty_result
from plc_agent.metrics import aggregate, audit_records


class TraceReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "capture.log").write_text("UNIT TEST DOUBLE ONLY\n", encoding="utf-8")
        self.task = {
            "id": "UNIT_REVIEW",
            "tests": [
                {"id": "timed", "steps": [{"inputs": {"Enable": True}, "expected": {"Run": True}, "dt_ms": 100}]}
            ],
        }
        self.trace = {
            "task_id": self.task["id"],
            "task_sha256": digest(self.task),
            "source_sha256": "unit-source",
            "backend": "CODESYS_SIMULATION",
            "operator": "UNIT_TEST_DOUBLE",
            "observed_utc": "2026-10-25T00:00:00Z",
            "evidence_files": ["capture.log"],
            "cases": {"timed": [{"inputs": {"Enable": True}, "outputs": {"Run": True}, "dt_ms": 100}]},
        }

    def evaluate(self):
        return evaluate_trace(self.task, "unit-source", self.trace, evidence_root=self.root)

    def test_missing_supporting_file_is_rejected(self):
        self.trace["evidence_files"] = ["missing.log"]
        with self.assertRaisesRegex(ValueError, "missing or empty"):
            self.evaluate()

    def test_evidence_hash_is_retained_and_checked(self):
        actual = self.evaluate()
        self.assertEqual(actual["status"], "PASS")
        checksum = actual["evidence_files"][0]["sha256"]
        self.assertEqual(len(checksum), 64)
        self.trace["evidence_files"] = [{"path": "capture.log", "sha256": "wrong"}]
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            self.evaluate()

    def test_evidence_cannot_escape_trace_directory(self):
        self.trace["evidence_files"] = ["../outside.log"]
        with self.assertRaisesRegex(ValueError, "escapes"):
            self.evaluate()

    def test_missing_observed_interval_is_rejected(self):
        del self.trace["cases"]["timed"][0]["dt_ms"]
        with self.assertRaisesRegex(ValueError, "observed dt_ms"):
            self.evaluate()

    def test_wrong_observed_interval_is_rejected(self):
        self.trace["cases"]["timed"][0]["dt_ms"] = 99
        with self.assertRaisesRegex(ValueError, "fixed test timing"):
            self.evaluate()

    def test_preregistered_timing_tolerance_is_respected(self):
        self.task["tests"][0]["dt_tolerance_ms"] = 5
        self.trace["task_sha256"] = digest(self.task)
        self.trace["cases"]["timed"][0]["dt_ms"] = 105
        self.assertEqual(self.evaluate()["status"], "PASS")
        self.trace["cases"]["timed"][0]["dt_ms"] = 106
        with self.assertRaisesRegex(ValueError, "fixed test timing"):
            self.evaluate()

    def test_numeric_one_cannot_replace_boolean_input(self):
        self.trace["cases"]["timed"][0]["inputs"]["Enable"] = 1
        with self.assertRaisesRegex(ValueError, "inputs"):
            self.evaluate()


class MetricReviewTests(unittest.TestCase):
    def record(self):
        return empty_result({"id": "UNIT_REVIEW", "tests": [{"id": "one"}]}, "E1", "UNIT", "codex_cli")

    def test_codex_total_tokens_are_derived_from_reported_components(self):
        row = self.record()
        row["usage"] = [{"input_tokens": 10, "output_tokens": 5}]
        summary = aggregate([row], 1)[0]
        self.assertEqual(summary["reported_tokens"]["total_tokens"], 15)

    def test_missing_usage_is_unknown_not_zero(self):
        row = self.record()
        row["usage"] = [{"input_tokens": 10}]
        row["llm_calls"] = None
        summary = aggregate([row], 1)[0]
        self.assertIsNone(summary["reported_tokens"]["output_tokens"])
        self.assertIsNone(summary["reported_tokens"]["total_tokens"])
        self.assertIsNone(summary["reported_llm_call_count"])

    def test_final_success_requires_final_attempt_success(self):
        row = self.record()
        row.update(first_pass_compiled=True, final_compiled=True)
        row["compilation_attempts"] = [
            {"status": "PASS", "success": True},
            {"status": "COMPILE_FAIL", "success": False},
        ]
        self.assertTrue(any("final candidate" in error for error in audit_records([row])))

    def test_audit_checks_selected_candidate_against_successful_compile(self):
        selected = {"declaration": "FUNCTION_BLOCK FB_Task", "implementation": "", "supporting_objects": []}
        later = {**selected, "implementation": "Run := FALSE;"}
        row = self.record()
        row.update(first_pass_compiled=True, final_compiled=True, final_candidate=selected)
        row["compilation_attempts"] = [
            {"status": "PASS", "success": True, "source_sha256": digest(selected)},
            {"status": "COMPILE_FAIL", "success": False, "source_sha256": digest(later)},
        ]
        self.assertEqual(audit_records([row]), [])

        row["compilation_attempts"][1].update(status="PASS", success=True)
        row["final_candidate"] = {**selected, "implementation": "Run := TRUE;"}
        self.assertTrue(any("final candidate" in error for error in audit_records([row])))

    def test_partial_functional_result_cannot_claim_task_pass(self):
        row = self.record()
        row["functional"].update(
            status="PASS", planned_cases=2, evaluated_cases=1, passed_cases=1, evidence="CODESYS_SIMULATION"
        )
        summary = aggregate([row], 1)[0]
        self.assertEqual(summary["passed_tasks"], 0)
        self.assertTrue(any("every planned case" in error for error in audit_records([row])))


if __name__ == "__main__":
    unittest.main()
