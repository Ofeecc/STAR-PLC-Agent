from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from plc_agent.cli import main
from plc_agent.common import read_json, write_json
from plc_agent.config import Settings, detect_codesys


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
