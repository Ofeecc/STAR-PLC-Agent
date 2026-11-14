import tempfile
import unittest

from plc_agent.codex_transport import CodexTransport
from plc_agent.config import Settings
from plc_agent.simulation import partition_wall_time_cases
from plc_agent.simulation import build_program
from plc_agent.dataset import load_tasks
from plc_agent.functional import same_declared_inputs
from plc_agent.functional import evaluate_trace
from plc_agent.common import digest
from pathlib import Path


class CodexTransportTests(unittest.TestCase):
    def test_dynamic_open_array_length_uses_separate_caller_storage(self):
        task = next(t for t in load_tasks() if t["id"] == "PUB008")
        program = build_program(task)
        self.assertIn("Binding_4_analogValues : ARRAY[-3..-1] OF INT;", program["declaration"])
        self.assertIn("Binding_4_analogValues_step1 : ARRAY[-3..0] OF INT;", program["declaration"])
        self.assertNotIn("Binding_4_analogValues[0]", program["implementation"])
        self.assertIn("Binding_4_analogValues_step1[0]", program["implementation"])
        self.assertEqual(program["trace_mapping"][0]["inputs"]["analogValues"]["kind"], "array")

    def test_nested_real_input_monitoring_uses_binary32_identity(self):
        task = {"interface": [{"name": "a", "type": "ARRAY[*] OF ST_A"}],
                "data_types": {"ST_A": {"kind": "STRUCT", "fields": [{"name": "x", "type": "REAL"}]}}}
        self.assertTrue(same_declared_inputs(task, {"a": [{"x": 0.9}]}, {"a": [{"x": 0.8999999761581421}]}))
        self.assertFalse(same_declared_inputs(task, {"a": [{"x": 0.9000000357627869}]}, {"a": [{"x": 0.8999999761581421}]}))
    def test_timing_gap_is_not_scored_as_correct_or_incorrect_code(self):
        task = {"id": "UNIT_REVIEW", "interface": [{"name": "q", "direction": "OUTPUT", "type": "BOOL"}],
                "tests": [{"id": name, "steps": [{"inputs": {}, "expected": {"q": True}, "dt_ms": 5}]}
                          for name in ("valid", "jitter")]}
        trace = {"task_id": task["id"], "task_sha256": digest(task), "source_sha256": "unit",
                 "backend": "CODESYS_SIMULATION", "operator": "unit fixture not a real benchmark",
                 "observed_utc": "unit", "evidence_files": ["unit.txt"],
                 "cases": {"valid": [{"inputs": {}, "outputs": {"q": True}, "dt_ms": 5}],
                           "jitter": [{"inputs": {}, "outputs": {"q": False}, "dt_ms": 6}]}}
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "unit.txt").write_text("unit fixture")
            with self.assertRaises(ValueError):
                evaluate_trace(task, "unit", trace, tmp)
            result = evaluate_trace(task, "unit", trace, tmp, allow_timing_gaps=True)
            self.assertEqual(result["status"], "PARTIAL")
            self.assertEqual(result["evaluated_cases"], 1)
            self.assertEqual(result["passed_cases"], 1)
            self.assertEqual(result["planned_cases"], 2)
            self.assertEqual(result["details"][1]["status"], "TIMING_NOT_REPRODUCED")
    def test_time_pin_compares_exact_duration_without_relaxing_string_pins(self):
        task = {"interface": [{"name": "d", "type": "TIME"}]}
        self.assertTrue(same_declared_inputs(task, {"d": "TIME#2s"}, {"d": "T#2000ms"}))
        self.assertFalse(same_declared_inputs(task, {"d": "TIME#2001ms"}, {"d": "T#2s"}))
        self.assertFalse(same_declared_inputs(task, {"d": True}, {"d": "T#1ms"}))
        task["interface"][0]["type"] = "STRING"
        self.assertFalse(same_declared_inputs(task, {"d": "TIME#2s"}, {"d": "T#2000ms"}))
    def test_long_fixed_cases_are_not_silently_fast_forwarded(self):
        cases = [{"id": "short", "steps": [{"dt_ms": 1000}]},
                 {"id": "maintenance", "steps": [{"dt_ms": 1800000000}]}]
        runnable, unsupported = partition_wall_time_cases(cases, 1800)
        self.assertEqual([c["id"] for c in runnable], ["short"])
        self.assertEqual(unsupported[0]["case_id"], "maintenance")
        self.assertEqual(cases[1]["steps"][0]["dt_ms"], 1800000000)
    def test_preserves_agent_input_and_enforces_only_declared_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            proxy = CodexTransport(Settings(max_llm_calls=2, max_output_tokens=8192, reasoning_effort="high"), "test", tmp)
            try:
                payload = {"model": "test", "input": [{"role": "user", "content": "original"}], "max_output_tokens": 20000}
                before = list(payload["input"])
                context = proxy.prepare(payload)
                self.assertEqual(payload["input"], before)
                self.assertEqual(payload["max_output_tokens"], 8192)
                self.assertEqual(payload["reasoning"]["effort"], "high")
                self.assertFalse(context["history_truncated"])
                proxy.request_count = 2
                with self.assertRaises(ValueError):
                    proxy.prepare(payload)
            finally:
                proxy.server.server_close()

    def test_records_usage_and_reserves_unknown_usage(self):
        with tempfile.TemporaryDirectory() as tmp:
            proxy = CodexTransport(Settings(), "test", tmp)
            try:
                proxy.record_response(tmp, b'data: {"type":"response.completed","response":{"usage":{"total_tokens":12,"cost":"0.01"}}}\n\n', {})
                self.assertEqual(proxy.total_tokens, 12)
                self.assertEqual(proxy.usage[0]["cost"], "0.01")
                proxy.record_response(tmp, b'', {"input_token_upper_bound": 20, "output_tokens_reserved": 30})
                self.assertEqual(proxy.total_tokens, 62)
            finally:
                proxy.server.server_close()


if __name__ == "__main__":
    unittest.main()
