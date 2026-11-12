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

    def test_every_task_has_current_chinese_review_interface_tests_and_properties(self):
        from plc_agent.common import digest
        from plc_agent.task_view import agent_view
        status, listing=handle_api_request('GET','/api/tasks',{},None,self.settings)
        self.assertEqual(status,200)
        self.assertEqual(len(listing['task_review']),32)
        self.assertEqual(len(listing['pilot_review']),6)
        count=0
        for summary in listing['tasks']:
            status,detail=handle_api_request('GET','/api/task',{'id':summary['id']},None,self.settings)
            task,review=detail['task'],detail['review']
            self.assertTrue(review['source_matches'])
            self.assertEqual(review['source_task_sha256'],digest(task))
            self.assertEqual(review['review_status'],'PENDING_HUMAN_REVIEW')
            self.assertEqual(detail['agent_view'],agent_view(task))
            self.assertNotIn('translation_zh',detail['agent_view'])
            for field in ('title_zh','translation_zh','assumptions_zh','coverage_zh','review_points_zh'):
                self.assertRegex(review[field],r'[\u4e00-\u9fff]')
            self.assertEqual(set(review['interface_zh']),{p['name'] for p in task['interface']})
            self.assertEqual(set(review['tests_zh']),{c['id'] for c in task['tests']})
            for case in task['tests']:
                self.assertEqual(review['tests_zh'][case['id']]['source_sha256'],digest(case))
            self.assertEqual(set(review['properties_zh']),{p['id'] for p in task['ltl']})
            for prop in task['ltl']:
                self.assertEqual(review['properties_zh'][prop['id']]['formula'],prop['formula'])
                self.assertRegex(review['properties_zh'][prop['id']]['description'],r'[\u4e00-\u9fff]')
                count+=1
        self.assertEqual(count,294)

    def test_six_pilot_tasks_have_review_material_and_match_current_dataset(self):
        status, listing = handle_api_request('GET','/api/tasks',{},None,self.settings)
        self.assertEqual(status,200)
        ids = ['PUB001','PUB003','PUB009','PUB010','PUB015','PUB016']
        self.assertEqual([r['id'] for r in listing['pilot_review']],ids)
        cases = steps = 0
        difficulties = []
        for tid in ids:
            status, detail = handle_api_request('GET','/api/task',{'id':tid},None,self.settings)
            self.assertEqual(status,200)
            self.assertEqual(detail['task']['kind'],'public')
            self.assertEqual(detail['review']['id'],tid)
            for field in ('title_zh','translation_zh','assumptions_zh','coverage_zh','review_points_zh'):
                self.assertTrue(detail['review'][field])
            cases += len(detail['tests'])
            steps += sum(len(c['steps']) for c in detail['tests'])
            difficulties.append(detail['task']['difficulty'])
            summary = next(t for t in listing['tasks'] if t['id'] == tid)
            self.assertEqual(summary['steps_count'],sum(len(c['steps']) for c in detail['tests']))
        self.assertEqual((cases,steps),(26,314))
        self.assertEqual(difficulties,['easy','easy','medium','medium','hard','hard'])

    def test_pilot_chinese_explanations_cover_every_current_formula(self):
        count = 0
        for tid in ['PUB001','PUB003','PUB009','PUB010','PUB015','PUB016']:
            status, detail = handle_api_request('GET','/api/task',{'id':tid},None,self.settings)
            self.assertEqual(status,200)
            chinese = detail['review']['properties_zh']
            self.assertEqual(set(chinese),{p['id'] for p in detail['task']['ltl']})
            for prop in detail['task']['ltl']:
                row = chinese[prop['id']]
                self.assertEqual(row['formula'],prop['formula'])
                self.assertTrue(row['description'])
                self.assertTrue(row['review'])
                count += 1
        self.assertEqual(count,64)

    def test_model_checker_api_keeps_reference_scope_and_rejects_other_tasks(self):
        import shutil
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_status = Path(tmpdir) / 'smv_status.json'
            for body in (
                None,
                {},
                {'task_id': 'NON_EXISTENT'},
                {'task_id': '../../arbitrary'},
                {'task_id': 'PUB001', 'variant': '../bad'},
            ):
                status, _ = handle_api_request(
                    'POST', '/api/check-reference-model', {}, body, self.settings, smv_status_path=tmp_status
                )
                self.assertEqual(status, 400)
            with patch('plc_agent.model_checker.find_nusmv', side_effect=ValueError('not installed')), patch(
                'plc_agent.model_checker.find_nuxmv', side_effect=ValueError('not installed')
            ), patch('plc_agent.model_checker.check_model', side_effect=ValueError('not installed')):
                for tid in ('PUB001', 'PUB016'):
                    status, data = handle_api_request(
                        'POST',
                        '/api/check-reference-model',
                        {},
                        {'task_id': tid},
                        self.settings,
                        smv_status_path=tmp_status,
                    )
                    self.assertEqual(status, 503)
                    self.assertEqual(data['status'], 'TOOL_ERROR')
                    self.assertEqual(data['verification_status'], 'CHECKER_MISSING')
                    self.assertTrue(data['checker_missing'])
                    self.assertEqual(data['smv_status']['scope'], 'EXPLICIT_SMV_MODEL_ONLY')
                    self.assertFalse(data['smv_status']['candidate_st_verified'])

    def test_persisted_smv_status_reports_verified_both_for_all_32_tasks(self):
        status, listing = handle_api_request('GET', '/api/tasks', {}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertIn('checker_availability', listing)
        self.assertEqual(len(listing['tasks']), 32)
        for t in listing['tasks']:
            smv = t['smv_status']
            self.assertEqual(smv['scope'], 'EXPLICIT_SMV_MODEL_ONLY')
            self.assertFalse(smv['candidate_st_verified'])
            self.assertTrue(smv['authored'])
            self.assertFalse(smv['stale'], t['id'])
            self.assertEqual(smv['verification_status'], 'VERIFIED_BOTH', t['id'])
            self.assertRegex(smv['authoring_text_zh'], r'[\u4e00-\u9fff]')
            self.assertRegex(smv['badge_text_zh'], r'[\u4e00-\u9fff]')

    def test_missing_checker_handling_preserves_baseline_and_records_unverified_missing(self):
        import re
        import shutil
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        from plc_agent.smv_status import DEFAULT_SMV_STATUS_PATH, load_smv_status_store

        with tempfile.TemporaryDirectory() as tmpdir:
            # Subcase A: persisted baseline present + checker uninstalled
            copied_status = Path(tmpdir) / 'copied_status.json'
            shutil.copy2(DEFAULT_SMV_STATUS_PATH, copied_status)
            with patch('plc_agent.model_checker.find_nusmv', side_effect=ValueError('NuSMV missing')), patch(
                'plc_agent.model_checker.find_nuxmv', side_effect=ValueError('nuXmv missing')
            ), patch('plc_agent.model_checker.check_model', side_effect=ValueError('checker missing')):
                status, detail = handle_api_request(
                    'GET', '/api/task', {'id': 'PUB015'}, None, self.settings, smv_status_path=copied_status
                )
                self.assertEqual(status, 200)
                smv = detail['smv_status']
                self.assertTrue(smv['checker_missing'])
                self.assertFalse(smv['live_rerunnable'])
                self.assertEqual(smv['verification_status'], 'VERIFIED_BOTH')
                self.assertIn('nuXmv', smv['badge_text_zh'])

                post_status, post_data = handle_api_request(
                    'POST',
                    '/api/check-reference-model',
                    {},
                    {'task_id': 'PUB015', 'variant': 'reference'},
                    self.settings,
                    smv_status_path=copied_status,
                )
                self.assertEqual(post_status, 503)
                self.assertEqual(post_data['verification_status'], 'CHECKER_MISSING')
                store_after = load_smv_status_store(copied_status)
                self.assertEqual(
                    store_after['records']['PUB015']['models']['reference']['status'],
                    'MODEL_PROPERTIES_TRUE',
                )
                self.assertEqual(
                    store_after['records']['PUB015']['last_run_attempt']['status'],
                    'CHECKER_MISSING',
                )

            # Subcase B: fresh store + checker missing
            empty_status = Path(tmpdir) / 'empty_status.json'
            with patch('plc_agent.model_checker.find_nusmv', side_effect=ValueError('NuSMV missing')), patch(
                'plc_agent.model_checker.find_nuxmv', side_effect=ValueError('nuXmv missing')
            ), patch('plc_agent.model_checker.check_model', side_effect=ValueError('checker missing')):
                status, detail = handle_api_request(
                    'GET', '/api/task', {'id': 'PUB015'}, None, self.settings, smv_status_path=empty_status
                )
                self.assertEqual(status, 200)
                self.assertEqual(detail['smv_status']['verification_status'], 'CHECKER_MISSING')
                self.assertFalse(detail['smv_status']['persisted_record_present'])

                post_status, post_data = handle_api_request(
                    'POST',
                    '/api/check-reference-model',
                    {},
                    {'task_id': 'PUB015', 'variant': 'reference'},
                    self.settings,
                    smv_status_path=empty_status,
                )
                self.assertEqual(post_status, 503)
                self.assertEqual(post_data['verification_status'], 'CHECKER_MISSING')
                persisted = load_smv_status_store(empty_status)
                self.assertEqual(
                    persisted['records']['PUB015']['models']['reference']['status'],
                    'CHECKER_MISSING',
                )

    def test_stale_smv_status_detected_when_model_hash_differs(self):
        import tempfile
        from pathlib import Path

        from plc_agent.smv_status import DEFAULT_SMV_STATUS_PATH, load_smv_status_store, save_smv_status_store

        with tempfile.TemporaryDirectory() as tmpdir:
            stale_status = Path(tmpdir) / 'stale_status.json'
            store = load_smv_status_store(DEFAULT_SMV_STATUS_PATH)
            store['records']['PUB001']['models']['reference']['model_sha256'] = '0' * 64
            save_smv_status_store(store, status_path=stale_status)
            status, detail = handle_api_request(
                'GET', '/api/task', {'id': 'PUB001'}, None, self.settings, smv_status_path=stale_status
            )
            self.assertEqual(status, 200)
            self.assertEqual(detail['smv_status']['verification_status'], 'STALE')
            self.assertTrue(detail['smv_status']['stale'])
            self.assertTrue(detail['smv_status']['models']['reference']['stale'])

    def test_symbol_glossary_covers_all_tokens_and_highlights_persistence(self):
        import re

        status, listing = handle_api_request('GET', '/api/tasks', {}, None, self.settings)
        self.assertEqual(status, 200)
        inout_checked = 0
        for summary in listing['tasks']:
            tid = summary['id']
            st, detail = handle_api_request('GET', '/api/task', {'id': tid}, None, self.settings)
            self.assertEqual(st, 200)
            glossary = detail['symbol_glossary']
            task = detail['task']
            for pin in task.get('interface', []):
                self.assertIn(pin['name'], glossary, f'{tid}:{pin["name"]}')
                if pin.get('direction') == 'IN_OUT':
                    inout_checked += 1
                    self.assertEqual(glossary[pin['name']]['category'], 'persistent_inout')
                    self.assertTrue(glossary[pin['name']]['is_persistent'])
                    self.assertTrue(glossary[pin['name']]['persistence_warning_zh'])
            for prop in task.get('ltl', []):
                for tok in re.findall(r'[A-Za-z_][A-Za-z_0-9.]*', prop['formula']):
                    if tok in {'G', 'F', 'X', 'U', 'R', 'V', 'W', 'TRUE', 'FALSE', 'AND', 'OR', 'NOT'} or tok.isdigit():
                        continue
                    self.assertIn(tok, glossary, f'Missing glossary token {tid} {prop["id"]}: {tok}')
            if tid == 'PUB001':
                self.assertEqual(glossary['phase']['category'], 'ghost_state')
                self.assertTrue(glossary['phase']['is_persistent'])
                self.assertEqual(glossary['bottleSensor']['category'], 'input')
                self.assertEqual(glossary['Pump_Motor']['category'], 'output')
        self.assertGreater(inout_checked, 0)

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
        self.assertIn("spec-popover", html)
        self.assertIn("overview-smv-box", html)
        self.assertIn("pilot-card-smv", html)
        self.assertIn("renderGlossaryPanel", html)
        self.assertIn("symbol_glossary", html)

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
            self.assertIn("smv_status", data["tasks"][0])

        # 3. Fetch /api/task?id=PUB015
        task_url = f"http://127.0.0.1:{port}/api/task?id=PUB015"
        with urlopen(task_url, timeout=3) as response:
            self.assertEqual(response.status, 200)
            detail = json.loads(response.read().decode("utf-8"))
            self.assertEqual(detail["task"]["id"], "PUB015")
            self.assertIn("symbol_glossary", detail)
            self.assertEqual(detail["smv_status"]["verification_status"], "VERIFIED_BOTH")

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
