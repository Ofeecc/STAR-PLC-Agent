from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from plc_agent.cli import main
from plc_agent.common import digest, read_json, write_json
from plc_agent.config import Settings, detect_codesys
from plc_agent.harness import empty_result


class CliAndConfigTests(unittest.TestCase):
    def test_settings_load_resolves_bundled_template(self):
        settings = Settings.load(load_api=False)
        self.assertTrue(Path(settings.codesys_template).is_file())
        self.assertTrue(settings.codesys_template.endswith("benchmark.project"))

    def test_settings_load_prefers_local_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp) / "custom.json"
            write_json(tmp_path, {"codesys_profile": "TEST_PROFILE_V99"})
            settings = Settings.load(tmp_path, load_api=False)
            self.assertEqual(settings.codesys_profile, "TEST_PROFILE_V99")

    def test_detect_codesys_callable(self):
        # On Linux/macOS returns empty strings; on Windows scans disk
        exe, prof = detect_codesys()
        self.assertIsInstance(exe, str)
        self.assertIsInstance(prof, str)

    def test_cli_configure_subcommand(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_local = Path(tmp) / "runtime.local.json"
            with patch("sys.argv", ["plc-agent", "--config", str(tmp_local), "configure", "--profile", "PROFILE_X"]):
                code = main()
                self.assertEqual(code, 0)
                data = read_json(tmp_local)
                self.assertEqual(data.get("codesys_profile"), "PROFILE_X")

    def test_cli_test_reference_fake_backend(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch("sys.argv", ["plc-agent", "test-reference", "--task", "SELF001", "--backend", "fake", "--out-dir", tmp]):
                code = main()
                self.assertEqual(code, 0)

    def test_cli_test_reference_invalid_task_raises(self):
        with patch("sys.argv", ["plc-agent", "test-reference", "--task", "NONEXISTENT", "--backend", "fake"]):
            code = main()
            self.assertEqual(code, 2)

    def test_cli_fixed_tests_use_selected_candidate_compile_evidence(self):
        task = {"id": "UNIT", "tests": []}
        selected = {"declaration": "FUNCTION_BLOCK FB_Task", "implementation": "", "supporting_objects": []}
        selected_hash = digest(selected)
        later_hash = digest({**selected, "implementation": "Run := FALSE;"})
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result_path = root / "run" / "result.json"
            manifest_path = root / "results" / "summary" / "campaign.json"
            write_json(manifest_path, {"conditions": [{"id": "E3"}], "records": {"E3/UNIT": "run/result.json"}})
            write_json(result_path.with_name("final_candidate.json"), selected)

            for later_status in ("COMPILE_FAIL", "PASS"):
                with self.subTest(later_status=later_status):
                    row = empty_result(task, "E3", "unit", "star")
                    row.update(final_compiled=True, final_candidate=selected)
                    row["compilation_attempts"] = [
                        {"status": "PASS", "success": True, "source_sha256": selected_hash},
                        {"status": later_status, "success": later_status == "PASS", "source_sha256": later_hash},
                    ]
                    write_json(result_path, row)
                    with (
                        patch("sys.argv", ["plc-agent", "test", "--condition", "E3", "--task-id", "UNIT"]),
                        patch("plc_agent.cli.ROOT", root),
                        patch("plc_agent.cli.load_tasks", return_value=[task]),
                        patch("plc_agent.cli.summarize"),
                        patch("plc_agent.simulation.run_functional", return_value={"status": "UNVERIFIED"}) as run_functional,
                    ):
                        self.assertEqual(main(), 0)
                    self.assertEqual(run_functional.call_args.args[1:3], (selected, selected_hash))

    def test_cli_import_trace_uses_selected_candidate_compile_evidence(self):
        task = {"id": "UNIT", "tests": []}
        candidate = {"declaration": "FUNCTION_BLOCK FB_Task", "implementation": "", "supporting_objects": []}
        source_hash = digest(candidate)
        row = empty_result(task, "E3", "unit", "star")
        row.update(final_compiled=True, final_candidate=candidate)
        row["compilation_attempts"] = [
            {"status": "PASS", "success": True, "source_sha256": source_hash},
            {"status": "PASS", "success": True, "source_sha256": "later-candidate"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_json(root / "results" / "summary" / "campaign.json", {"records": {"E3/UNIT": "run/result.json"}})
            write_json(root / "run" / "result.json", row)
            trace_path = root / "trace.json"
            write_json(trace_path, {"source_sha256": source_hash})

            def check_hash(_task, compiled_hash, trace, evidence_root):
                self.assertEqual(compiled_hash, trace["source_sha256"])
                return {"status": "UNVERIFIED", "evidence_files": []}

            with (
                patch("sys.argv", ["plc-agent", "import-trace", "--condition", "E3", "--task", "UNIT", "--trace", str(trace_path)]),
                patch("plc_agent.cli.ROOT", root),
                patch("plc_agent.cli.load_tasks", return_value=[task]),
                patch("plc_agent.functional.evaluate_trace", side_effect=check_hash),
            ):
                self.assertEqual(main(), 0)
