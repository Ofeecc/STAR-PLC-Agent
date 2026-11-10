import json
import threading
import time
import unittest
from urllib.request import urlopen

from plc_agent.backend import CompileResult, FakeBackend
from plc_agent.config import Settings
from plc_agent.webui import handle_api_request, render_index_html, serve_webui


class WebUITests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()

    def test_render_index_html_contains_titles_and_components(self):
        html = render_index_html()
        self.assertIsInstance(html, str)
        self.assertIn("CODESYS STAR v2 | Auto-Test & Waveform Agent Trace Inspector", html)
        self.assertIn("Task & Dataset Explorer", html)
        self.assertIn("Waveform & Timing Comparator", html)
        self.assertIn("Agent Trace Playback", html)
        self.assertIn("Interactive Sandbox & Verifier", html)
        # Check essential UI controls
        self.assertIn("task-select", html)
        self.assertIn("waveform-view", html)
        self.assertIn("trace-playback", html)
        self.assertIn("sandbox-editor", html)

    def test_handle_api_request_tasks_returns_all_32_tasks(self):
        status, data = handle_api_request("GET", "/api/tasks", {}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertIn("tasks", data)
        tasks = data["tasks"]
        self.assertEqual(len(tasks), 32)
        pub_tasks = [t for t in tasks if t["kind"] == "public"]
        self_tasks = [t for t in tasks if t["kind"] == "self_built"]
        self.assertEqual(len(pub_tasks), 20)
        self.assertEqual(len(self_tasks), 12)
        for t in tasks:
            self.assertIn("id", t)
            self.assertIn("title", t)
            self.assertIn("kind", t)
            self.assertIn("difficulty", t)
            self.assertIn("tests_count", t)

    def test_handle_api_request_task_detail_and_random_cases(self):
        status, data = handle_api_request("GET", "/api/task", {"id": "SELF001"}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertIn("task", data)
        self.assertEqual(data["task"]["id"], "SELF001")
        self.assertIn("agent_view", data)
        self.assertNotIn("tests", data["agent_view"])
        self.assertIn("tests", data)
        self.assertGreater(len(data["tests"]), 0)
        self.assertIn("random_cases", data)
        self.assertGreater(len(data["random_cases"]), 0)

    def test_handle_api_request_task_detail_with_list_query(self):
        status, data = handle_api_request("GET", "/api/task", {"id": ["PUB001"]}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertEqual(data["task"]["id"], "PUB001")
        self.assertIn("random_cases", data)

    def test_handle_api_request_task_not_found(self):
        status, data = handle_api_request("GET", "/api/task", {"id": "NON_EXISTENT"}, None, self.settings)
        self.assertEqual(status, 404)
        self.assertIn("error", data)

    def test_handle_api_request_evaluate_with_fake_backend_compile_failure(self):
        backend = FakeBackend(
            compile_fn=lambda t, c, w: CompileResult(
                status="COMPILE_FAIL",
                success=False,
                diagnostics=[{"message": "Syntax error: unknown variable 'FooBar'"}],
            )
        )
        body = {
            "task_id": "SELF001",
            "candidate": "Invalid ST candidate",
            "include_random": False,
        }
        status, data = handle_api_request("POST", "/api/evaluate", {}, body, self.settings, backend=backend)
        self.assertEqual(status, 200)
        self.assertIn("compile", data)
        self.assertFalse(data["compile"]["success"])
        self.assertEqual(data["compile"]["status"], "COMPILE_FAIL")
        self.assertIn("simulation", data)
        self.assertEqual(data["simulation"]["status"], "COMPILE_FAIL")

    def test_handle_api_request_evaluate_with_fake_backend_simulation_failure(self):
        # Step fn returns all False/0 which fails against SELF001 contract
        backend = FakeBackend(
            step_fn=lambda inp, dt: {"High": False, "Alarm": False, "Filtered": 0.0}
        )
        body = {
            "task_id": "SELF001",
            "candidate": {
                "declaration": "FUNCTION_BLOCK FB_SELF001\nEND_VAR",
                "implementation": "",
            },
            "include_random": True,
        }
        status, data = handle_api_request("POST", "/api/evaluate", {}, body, self.settings, backend=backend)
        self.assertEqual(status, 200)
        self.assertIn("compile", data)
        self.assertTrue(data["compile"]["success"])
        self.assertIn("simulation", data)
        self.assertEqual(data["simulation"]["status"], "TEST_FAIL")
        self.assertGreater(len(data["simulation"]["failures"]), 0)
        self.assertIn("waveform", data)
        self.assertGreater(len(data["waveform"]), 0)
        # Check first failing case has divergence recorded
        first_wave = data["waveform"][0]
        self.assertIn("steps", first_wave)
        matches = [s["match"] for s in first_wave["steps"] if s["match"] is not None]
        self.assertIn(False, matches)

    def test_handle_api_request_evaluate_with_default_fake_backend_passes(self):
        # When step_fn is None, FakeBackend executes ScanContract directly, which passes valid tests
        backend = FakeBackend()
        body = {
            "task_id": "SELF001",
            "candidate": {
                "declaration": "FUNCTION_BLOCK FB_SELF001\nEND_VAR",
                "implementation": "",
            },
            "include_random": False,
        }
        status, data = handle_api_request("POST", "/api/evaluate", {}, body, self.settings, backend=backend)
        self.assertEqual(status, 200)
        self.assertTrue(data["compile"]["success"])
        self.assertEqual(data["simulation"]["status"], "PASS")
        self.assertEqual(len(data["simulation"]["failures"]), 0)

    def test_handle_api_request_export_verify(self):
        candidate = {
            "declaration": (
                "FUNCTION_BLOCK FB_SELF001\n"
                "VAR_INPUT\n  RawValue : REAL;\n  Reset : BOOL;\nEND_VAR\n"
                "VAR_OUTPUT\n  Filtered : REAL;\n  High : BOOL;\n  Alarm : BOOL;\nEND_VAR\n"
            ),
            "implementation": "Filtered := RawValue; High := FALSE; Alarm := FALSE;",
            "supporting_objects": [],
        }
        body = {
            "task_id": "SELF001",
            "candidate": candidate,
        }
        status, data = handle_api_request("POST", "/api/export-verify", {}, body, self.settings)
        self.assertEqual(status, 200)
        self.assertIn("manifest", data)
        manifest = data["manifest"]
        self.assertEqual(manifest["task_id"], "SELF001")
        self.assertEqual(manifest["st_path"], "candidate.st")
        self.assertEqual(manifest["ltl_path"], "spec.ltl")
        self.assertIn("properties", manifest)
        self.assertIn("candidate_st", data)
        self.assertIn("spec_ltl", data)

    def test_handle_api_request_experiments(self):
        status, data = handle_api_request("GET", "/api/experiments", {}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertIn("summaries", data)
        self.assertIn("conditions", data)

    def test_handle_api_request_invalid_route(self):
        status, data = handle_api_request("GET", "/api/unknown_route", {}, None, self.settings)
        self.assertEqual(status, 404)
        self.assertIn("error", data)

    def test_serve_webui_http_server(self):
        # Start server on ephemeral port (port 0) in a background thread
        stop_event = threading.Event()
        bound_port = [0]
        server_thread = threading.Thread(
            target=serve_webui,
            kwargs={
                "host": "127.0.0.1",
                "port": 0,
                "settings": self.settings,
                "stop_event": stop_event,
                "bound_port_box": bound_port,
            },
            daemon=True,
        )
        server_thread.start()
        time.sleep(0.1)

        port = bound_port[0]
        self.assertGreater(port, 0)

        # 1. Fetch index HTML
        url = f"http://127.0.0.1:{port}/"
        with urlopen(url, timeout=3) as response:
            self.assertEqual(response.status, 200)
            content_type = response.headers.get("Content-Type", "")
            self.assertIn("text/html", content_type)
            body = response.read().decode("utf-8")
            self.assertIn("CODESYS STAR v2 | Auto-Test & Waveform Agent Trace Inspector", body)

        # 2. Fetch /api/tasks
        api_url = f"http://127.0.0.1:{port}/api/tasks"
        with urlopen(api_url, timeout=3) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertIn("tasks", data)
            self.assertEqual(len(data["tasks"]), 32)

        # Stop the server
        stop_event.set()
        # Ping once to unblock server loop if needed
        try:
            urlopen(url, timeout=0.5)
        except Exception:
            pass
        server_thread.join(timeout=2)

    def test_cli_web_subcommand_parser(self):
        from unittest.mock import patch

        from plc_agent import cli

        test_argv = ["plc-agent", "web", "--host", "0.0.0.0", "--port", "9999"]
        with patch("sys.argv", test_argv), patch("plc_agent.webui.serve_webui") as mock_serve:
            exit_code = cli.main()
            self.assertEqual(exit_code, 0)
            mock_serve.assert_called_once()
            args, kwargs = mock_serve.call_args
            self.assertEqual(args[0], "0.0.0.0")
            self.assertEqual(args[1], 9999)


if __name__ == "__main__":
    unittest.main()
