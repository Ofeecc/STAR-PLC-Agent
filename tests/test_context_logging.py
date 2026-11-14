import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from plc_agent.backend import FakeBackend
from plc_agent.baseline import run_baseline
from plc_agent.common import read_json, write_json
from plc_agent.compiler import CompileResult
from plc_agent.config import Settings
from plc_agent.llm import ProviderError, ResponsesClient
from plc_agent.mcp_server import dispatch
from plc_agent.replay import ResumingClient


class ContextLoggingTests(unittest.TestCase):
    def client(self):
        client = ResponsesClient(
            Settings(
                api_key="unit-private-key",
                base_url="https://relay.invalid/v1",
                max_output_tokens=32,
                max_llm_calls=1,
                reasoning_effort="high",
            )
        )
        response = MagicMock(status_code=200, headers={"Content-Type": "application/json"})
        response.json.return_value = {
            "status": "completed",
            "model": "model-alias",
            "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "OK"}]}],
            "usage": {"input_tokens": 5, "output_tokens": 1},
        }
        client.session.post = MagicMock()
        client.session.post.return_value.__enter__.return_value = response
        return client

    def test_complete_context_retained_redacted_and_request_budget_enforced(self):
        client = self.client()
        messages = [{"role": "user", "content": "visible context unit-private-key"}]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(client.respond("test-model", messages, root / "call_1")["text"], "OK")
            request = read_json(root / "call_1/request.json")
            self.assertEqual(request["reasoning"], {"effort": "high"})
            self.assertEqual(request["input"][0]["content"], "visible context [REDACTED]")
            self.assertFalse(read_json(root / "call_1/context.json")["history_truncated"])
            self.assertNotIn("unit-private-key", (root / "model_calls.jsonl").read_text())
            with self.assertRaisesRegex(ProviderError, "request budget"):
                client.respond("test-model", messages, root / "call_2")
            self.assertEqual(client.session.post.call_count, 1)

    def test_context_limit_stops_before_network_and_preserves_input(self):
        client = self.client()
        client.settings.context_window_tokens = 300
        messages = [{"role": "user", "content": "long" * 200}]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(ProviderError, "context budget"):
                client.respond("test-model", messages, root / "call")
            client.session.post.assert_not_called()
            self.assertEqual(read_json(root / "call/request.json")["input"], messages)
            self.assertEqual(client.request_count, 0)

    def test_incomplete_response_preserves_usage_and_failure_reason(self):
        client = self.client()
        response = client.session.post.return_value.__enter__.return_value
        response.json.return_value = {
            "status": "incomplete",
            "incomplete_details": {"reason": "max_output_tokens"},
            "usage": {"output_tokens": 32},
            "output": [],
        }
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(ProviderError, "max_output_tokens"):
                client.respond("test-model", [{"role": "user", "content": "test"}], root / "call")
            self.assertEqual(read_json(root / "call/response.json")["usage"]["output_tokens"], 32)
            events = [json.loads(x) for x in (root / "model_calls.jsonl").read_text().splitlines()]
            failed = next(e for e in events if e["event"] == "request_failed")
            self.assertEqual(failed["usage"], {"output_tokens": 32})
            self.assertEqual(events[-1]["event"], "token_budget_accounted")
            self.assertGreater(client.total_tokens, 0)

    def test_total_token_guard_counts_failed_usage_and_blocks_before_http(self):
        client = self.client()
        client.settings.max_llm_calls = 9
        client.settings.max_total_tokens = 1000
        response = client.session.post.return_value.__enter__.return_value
        response.json.return_value = {
            "status": "incomplete",
            "incomplete_details": {"reason": "max_output_tokens"},
            "usage": {"total_tokens": 900},
            "output": [],
        }
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(ProviderError, "max_output_tokens"):
                client.respond("unit", [{"role": "user", "content": "test"}], root / "first")
            self.assertEqual(client.total_tokens, 900)
            with self.assertRaisesRegex(ProviderError, "total token safety limit"):
                client.respond("unit", [{"role": "user", "content": "test"}], root / "second")
            self.assertEqual(client.session.post.call_count, 1)
            self.assertEqual(client.request_count, 1)

    def test_mcp_compiler_receives_uncreated_work_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)

            def compile_probe(task, source, workspace, settings):
                self.assertFalse(workspace.exists())
                return CompileResult("PASS", success=True)

            with patch("plc_agent.mcp_server.compile_st", side_effect=compile_probe):
                response = dispatch(
                    {
                        "method": "tools/call",
                        "params": {
                            "name": "compile_st",
                            "arguments": {"source": {"declaration": "FUNCTION_BLOCK FB_Task", "implementation": ""}},
                        },
                    },
                    {"id": "UNIT"},
                    root,
                    Settings(),
                )
            self.assertFalse(response["isError"])
            self.assertTrue((root / "compile_00/compile_result.json").is_file())

    def test_resume_reuses_exact_completed_context_and_rejects_changed_input(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            settings = Settings(reasoning_effort="high")
            messages = [{"role": "user", "content": "same task"}]
            source = root / "original/llm_planner"
            write_json(
                source / "request.json",
                {
                    "model": "unit",
                    "input": messages,
                    "reasoning": {"effort": "high"},
                    "max_output_tokens": settings.max_output_tokens,
                },
            )
            write_json(
                source / "response.json",
                {
                    "status": "completed",
                    "output": [{"type": "message", "content": [{"type": "output_text", "text": "saved plan"}]}],
                    "usage": {"total_tokens": 10},
                },
            )
            client = ResumingClient(settings, root / "original", remaining_requests=6)
            with patch.object(client.session, "post") as post:
                reply = client.respond("unit", messages, root / "resumed/llm_planner")
                self.assertEqual(reply["text"], "saved plan")
                self.assertIsNone(reply["usage"])
                self.assertEqual(client.request_count, 0)
                with self.assertRaisesRegex(ProviderError, "Cached request differs"):
                    client.respond("unit", [{"role": "user", "content": "changed task"}], root / "other/llm_planner")
                post.assert_not_called()

    def test_baseline_multiple_tool_calls_replay_in_responses_format(self):
        candidate = {"declaration": "FUNCTION_BLOCK FB_Task", "implementation": "", "supporting_objects": []}

        class Client:
            def __init__(self):
                self.inputs = []

            def respond(self, model, input_items, **kwargs):
                self.inputs.append(copy.deepcopy(input_items))
                if len(self.inputs) == 1:
                    return {
                        "output": [
                            {
                                "type": "function_call",
                                "call_id": name,
                                "name": "compile_st",
                                "arguments": json.dumps({"source": candidate}),
                            }
                            for name in ("first", "second")
                        ],
                        "text": "",
                    }
                return {"output": [], "text": "done"}

        client = Client()
        task = {"id": "UNIT", "requirements": "unit task", "interface": [], "tests": []}
        with tempfile.TemporaryDirectory() as temp:
            run_baseline(
                task,
                "unit-model",
                Path(temp) / "run",
                Settings(),
                driver="deepseek_harness",
                client=client,
                backend=FakeBackend(),
            )
        replay = client.inputs[1]
        self.assertEqual([x["call_id"] for x in replay if x.get("type") == "function_call"], ["first", "second"])
        self.assertEqual([x["call_id"] for x in replay if x.get("type") == "function_call_output"], ["first", "second"])
        self.assertFalse(any(x.get("role") == "tool" for x in replay))

    def test_role_specific_output_limits(self):
        from plc_agent.harness import run_harness

        class Client:
            def __init__(self):
                self.limits = {}

            def respond(self, model, input_items, log_dir, **kwargs):
                stage = Path(log_dir).name
                self.limits[stage] = kwargs.get("max_tokens")
                text = (
                    "{}"
                    if stage == "llm_planner"
                    else "[]"
                    if stage == "llm_tester"
                    else json.dumps(
                        {"declaration": "FUNCTION_BLOCK FB_Task", "implementation": "", "supporting_objects": []}
                    )
                )
                return {"text": text}

        client = Client()
        with tempfile.TemporaryDirectory() as temp:
            run_harness(
                {"id": "UNIT", "interface": [], "tests": []},
                "unit-model",
                Path(temp) / "run",
                client,
                Settings(
                    planner_max_output_tokens=16384,
                    coder_max_output_tokens=24576,
                    tester_max_output_tokens=24576,
                    repair_max_output_tokens=32768,
                ),
                backend=FakeBackend(),
            )
        self.assertEqual(client.limits["llm_planner"], 16384)
        self.assertEqual(client.limits["llm_code_00"], 24576)
        self.assertEqual(client.limits["llm_tester"], 24576)
        self.assertEqual(Settings(repair_max_output_tokens=32768).output_limit("repair"), 32768)

    def test_compile_repair_receives_its_role_budget(self):
        from plc_agent.harness import run_harness

        class Client:
            def __init__(self):
                self.limits = {}

            def respond(self, model, input_items, log_dir, **kwargs):
                stage = Path(log_dir).name
                self.limits[stage] = kwargs.get("max_tokens")
                text = (
                    "{}"
                    if stage == "llm_planner"
                    else "[]"
                    if stage == "llm_tester"
                    else json.dumps(
                        {"declaration": "FUNCTION_BLOCK FB_Task", "implementation": "", "supporting_objects": []}
                    )
                )
                return {"text": text}

        outcomes = [
            CompileResult("COMPILE_FAIL", diagnostics=[{"severity": "Error", "text": "unit compile error"}]),
            CompileResult("PASS", success=True),
        ]
        client = Client()
        with tempfile.TemporaryDirectory() as temp:
            run_harness(
                {"id": "UNIT", "interface": [], "tests": []},
                "unit-model",
                Path(temp) / "run",
                client,
                Settings(repair_max_output_tokens=32768),
                backend=FakeBackend(compile_fn=lambda *args: outcomes.pop(0)),
            )
        self.assertEqual(client.limits["llm_repair_01"], 32768)


if __name__ == "__main__":
    unittest.main()
