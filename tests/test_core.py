"""Offline boundary tests. Synthetic evidence here is never benchmark evidence."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from plc_agent.common import digest, redact
from plc_agent.compiler import compile_st, normalize_candidate, verify_evidence
from plc_agent.config import Settings
from plc_agent.dataset import load_tasks, validate
from plc_agent.functional import equal, evaluate_trace
from plc_agent.harness import empty_result, run_harness
from plc_agent.mcp_server import dispatch
from plc_agent.metrics import aggregate, audit_records


class CoreTests(unittest.TestCase):
    def test_complete_dataset(self):
        report = validate(load_tasks())
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["by_kind"], {"public": 20, "self_built": 12})

    def test_stale_evidence_is_rejected(self):
        request = {"request_id": "current", "source_sha256": "abc"}
        evidence = {
            "backend": "CODESYS",
            "request_id": "old",
            "source_sha256": "abc",
            "finished": True,
            "rebuild_invoked": True,
            "error_count": 0,
            "compiled_pou_crc": "1",
        }
        with self.assertRaisesRegex(ValueError, "Stale"):
            verify_evidence(evidence, request)
        evidence["request_id"] = "current"
        self.assertEqual(verify_evidence(evidence, request), ("PASS", True))
        evidence["compiled_pou_crc"] = None
        with self.assertRaisesRegex(ValueError, "demonstrably"):
            verify_evidence(evidence, request)
        evidence["error_count"] = 1
        self.assertEqual(verify_evidence(evidence, request), ("COMPILE_FAIL", False))

    def test_missing_codesys_is_tool_error_never_compile_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = compile_st(
                {"id": "UNIT_ONLY"},
                {"declaration": "FUNCTION_BLOCK FB_Task\nVAR END_VAR", "implementation": ""},
                Path(tmp) / "run",
                Settings(),
            )
            self.assertEqual(result.status, "TOOL_ERROR")
            self.assertFalse(result.success)
            self.assertIsNone(result.evidence)

    def test_full_st_split(self):
        text = (
            "FUNCTION_BLOCK FB_Task\nVAR_INPUT A:BOOL; END_VAR\nVAR_OUTPUT B:BOOL; END_VAR\nB := A;\nEND_FUNCTION_BLOCK"
        )
        self.assertEqual(normalize_candidate(text)["implementation"], "B := A;")

    def test_aggregation_denominator_and_missing_are_explicit(self):
        task = load_tasks()[0]
        first = empty_result(task, "E3", "A", "self")
        summary = aggregate([first], 32)[2]
        self.assertIsNone(summary["first_pass_compilation_rate"])
        self.assertEqual(summary["compiler_coverage"], 0)
        first.update(first_pass_compiled=False, final_compiled=True, status="UNVERIFIED")
        first["compilation_attempts"] = [
            {"status": "COMPILE_FAIL", "success": False},
            {"status": "PASS", "success": True},
        ]
        summary = aggregate([first], 32)[2]
        self.assertEqual(summary["final_compilation_rate"], 1 / 32)
        self.assertEqual(summary["repair_effectiveness"], 1)
        self.assertEqual(audit_records([first]), [])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            aggregate([first, first], 32)

    def test_boolean_and_number_are_not_interchangeable(self):
        self.assertFalse(equal(1, True))
        self.assertFalse(equal(False, 0))
        self.assertTrue(equal({"x": 1.000001, "extra": 8}, {"x": 1.0}))
        self.assertFalse(equal(float("nan"), 1.0))

    def test_reference_trace_cannot_be_counted_as_plc(self):
        task = load_tasks()[0]
        trace = {
            "task_id": task["id"],
            "task_sha256": digest(task),
            "source_sha256": "x",
            "backend": "PYTHON_REFERENCE_ONLY",
        }
        with self.assertRaisesRegex(ValueError, "real CODESYS"):
            evaluate_trace(task, "x", trace)

    def test_secret_redaction(self):
        self.assertNotIn("very-private", redact("very-private sk-abc123", ["very-private"]))
        self.assertNotIn("sk-abc123", redact("Bearer sk-abc123"))

    def test_compiler_tool_budget_persists_across_process_restarts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for i in range(3):
                (root / f"compile_{i:02d}").mkdir()
                (root / f"compile_{i:02d}/compile_result.json").write_text("{}")
            message = {"method": "tools/call", "params": {"name": "compile_st", "arguments": {}}}
            result = dispatch(message, {"id": "UNIT_ONLY"}, root, Settings(max_repairs=2))
            self.assertTrue(result["isError"])

    def test_harness_repair_and_stop_control_flow_only(self):
        # Injected doubles test state-machine logic only; outputs remain in temp directories.
        from plc_agent.compiler import CompileResult

        class FakeClient:
            def respond(self, *args, **kwargs):
                return {
                    "text": json.dumps({"declaration": "FUNCTION_BLOCK FB_Task", "implementation": ""}),
                    "usage": None,
                }

        failed = CompileResult("COMPILE_FAIL", diagnostics=[{"severity": "Error", "text": "synthetic unit error"}])
        passed = CompileResult("PASS", success=True)
        with tempfile.TemporaryDirectory() as tmp, patch("plc_agent.harness.compile_st", side_effect=[failed, passed]):
            result = run_harness(load_tasks()[0], "UNIT_TEST_DOUBLE", Path(tmp) / "run", FakeClient(), Settings())
            self.assertEqual(result["repair_attempts"], 1)
            self.assertEqual(result["status"], "UNVERIFIED")
            self.assertTrue(result["final_compiled"])
            self.assertEqual(result["functional"]["evaluated_cases"], 0)

    def test_harness_does_not_score_an_unavailable_compiler_as_a_rejection(self):
        from plc_agent.backend import FakeBackend
        from plc_agent.compiler import CompileResult

        candidate = {"declaration": "FUNCTION_BLOCK FB_Task", "implementation": ""}
        task = load_tasks()[0]
        with tempfile.TemporaryDirectory() as tmp:
            for status in ("TOOL_ERROR", "TIMEOUT", "UNVERIFIED"):
                with self.subTest(status=status):
                    client = Mock()
                    client.respond.return_value = {"text": json.dumps(candidate)}
                    backend = FakeBackend(compile_fn=lambda *args: CompileResult(status, infrastructure_error="unit"))
                    result = run_harness(
                        task, "unit", Path(tmp) / status, client, Settings(), backend=backend, ablation="no_planner"
                    )
                    self.assertEqual(result["status"], status)
                    self.assertIsNone(result["first_pass_compiled"])
                    self.assertIsNone(result["final_compiled"])
                    self.assertEqual(aggregate([result], 1)[2]["actual_first_compilations"], 0)
                    self.assertEqual(audit_records([result]), [])
                    self.assertEqual(client.respond.call_count, 1)

    def test_harness_keeps_first_rejection_if_repair_compile_is_unavailable(self):
        from plc_agent.backend import FakeBackend
        from plc_agent.compiler import CompileResult

        candidate = {"declaration": "FUNCTION_BLOCK FB_Task", "implementation": ""}
        with tempfile.TemporaryDirectory() as tmp:
            client = Mock()
            client.respond.return_value = {"text": json.dumps(candidate)}
            outcomes = iter([CompileResult("COMPILE_FAIL"), CompileResult("TOOL_ERROR", infrastructure_error="unit")])
            backend = FakeBackend(compile_fn=lambda *args: next(outcomes))
            result = run_harness(
                load_tasks()[0], "unit", Path(tmp) / "run", client, Settings(), backend=backend, ablation="no_planner"
            )
            self.assertEqual(result["status"], "TOOL_ERROR")
            self.assertIs(result["first_pass_compiled"], False)
            self.assertIsNone(result["final_compiled"])


if __name__ == "__main__":
    unittest.main()
