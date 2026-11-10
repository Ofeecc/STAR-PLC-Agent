import copy
import tempfile
import unittest
from pathlib import Path

from plc_agent.compiler import stage_ascii_workspace, sync_ascii_artifacts
from plc_agent.dataset import load_tasks
from plc_agent.task_view import ALLOWED_KEYS, FORBIDDEN_KEYS, SPEC_KEYS, agent_view


class TaskViewTests(unittest.TestCase):
    def test_agent_view_whitelist_and_immutability(self):
        tasks = load_tasks()
        for task in tasks:
            original = copy.deepcopy(task)
            with_spec = agent_view(task, spec_visible=True)
            without_spec = agent_view(task, spec_visible=False)
            self.assertEqual(task, original)
            self.assertTrue(set(with_spec.keys()).issubset(ALLOWED_KEYS | SPEC_KEYS))
            self.assertTrue(set(without_spec.keys()).issubset(ALLOWED_KEYS))
            for forbidden in FORBIDDEN_KEYS:
                self.assertNotIn(forbidden, with_spec)
                self.assertNotIn(forbidden, without_spec)
            for key in SPEC_KEYS:
                self.assertNotIn(key, without_spec)

    def test_stage_ascii_workspace_copies_script_and_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            non_ascii = Path(tmp) / "中文目录" / "run_01"
            non_ascii.mkdir(parents=True)
            script = non_ascii / "build.py"
            template = non_ascii / "benchmark.project"
            script.write_text("# script\n", encoding="utf-8")
            template.write_bytes(b"TEMPLATE")
            ascii_root = Path(tmp) / "plc_work"
            staged_ws, staged_script, staged_tpl = stage_ascii_workspace(
                non_ascii, script, template, ascii_root
            )
            self.assertTrue(staged_ws.is_dir())
            self.assertEqual(staged_script.read_text(encoding="utf-8"), "# script\n")
            self.assertEqual(staged_tpl.read_bytes(), b"TEMPLATE")
            self.assertTrue(str(staged_ws.name).isascii())

    def test_stage_ascii_workspace_passthrough_when_ascii(self):
        with tempfile.TemporaryDirectory() as tmp:
            ascii_ws = Path(tmp) / "ascii_dir" / "run_01"
            ascii_ws.mkdir(parents=True)
            script = ascii_ws / "build.py"
            template = ascii_ws / "benchmark.project"
            script.write_text("# script\n", encoding="utf-8")
            template.write_bytes(b"TEMPLATE")
            ascii_root = Path(tmp) / "plc_work"
            staged_ws, staged_script, staged_tpl = stage_ascii_workspace(
                ascii_ws, script, template, ascii_root
            )
            self.assertEqual(staged_ws, ascii_ws)
            self.assertEqual(staged_script, script)
            self.assertEqual(staged_tpl, template)

    def test_sync_ascii_artifacts_copies_expected_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            staged = Path(tmp) / "staged"
            target = Path(tmp) / "target"
            staged.mkdir()
            (staged / "codesys_evidence.json").write_text("{}", encoding="utf-8")
            (staged / "simulation_evidence.json").write_text("{}", encoding="utf-8")
            (staged / "stdout.log").write_text("out", encoding="utf-8")
            (staged / "stderr.log").write_text("err", encoding="utf-8")
            (staged / "request.json").write_text("{}", encoding="utf-8")
            (staged / "unrelated.txt").write_text("ignored", encoding="utf-8")

            sync_ascii_artifacts(staged, target)
            self.assertTrue((target / "codesys_evidence.json").is_file())
            self.assertTrue((target / "simulation_evidence.json").is_file())
            self.assertTrue((target / "stdout.log").is_file())
            self.assertTrue((target / "stderr.log").is_file())
            self.assertTrue((target / "request.json").is_file())
            self.assertFalse((target / "unrelated.txt").exists())
