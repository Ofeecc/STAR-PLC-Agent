import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from plc_agent.batch import load_source, main, run_task, select_tasks, stage_result
from plc_agent.common import digest, read_json, write_json
from plc_agent.compiler import compiler_lock


class BatchTests(unittest.TestCase):
    def test_task_selection_rejects_unknown_and_duplicate_ids(self):
        tasks = [{"id": "PUB001"}, {"id": "SELF001"}]
        self.assertEqual(select_tasks(tasks, "public"), tasks[:1])
        self.assertEqual(select_tasks(tasks, "self"), tasks[1:])
        for value in ("PUB999", "PUB001,PUB001", ""):
            with self.assertRaises(ValueError):
                select_tasks(tasks, value)

    def test_model_generation_requires_explicit_opt_in(self):
        with patch("plc_agent.batch.Settings.load") as config:
            with self.assertRaises(SystemExit) as raised:
                main(["--generate-missing"])
            self.assertEqual(raised.exception.code, 2)
            config.assert_not_called()

    def test_changed_task_cannot_reuse_old_generation(self):
        task = {"id": "PUB001", "tests": []}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "result.json"
            write_json(path, {"task_id": task["id"], "task_sha256": digest(task), "model": "test"})
            self.assertIsNone(load_source(path, task, "test")[1])
            with self.assertRaises(ValueError):
                load_source(path, dict(task, requirements="changed"), "test")

    def test_stage_cache_skips_actions_and_rejects_changed_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            calls = []

            def action(attempt):
                calls.append(attempt)
                return {"status": "PASS"}, "unit_fake_not_plc"

            stage_result(work, "formal", "hash1", {"retry_infra": False}, action)
            cached = stage_result(work, "formal", "hash1", {"retry_infra": False}, action)
            self.assertTrue(cached["cached"])
            self.assertEqual(len(calls), 1)
            with self.assertRaises(ValueError):
                stage_result(work, "formal", "hash2", {"retry_infra": False}, action)

    def test_infrastructure_retry_preserves_previous_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            calls = []

            def action(attempt):
                attempt.mkdir()
                calls.append(attempt)
                return {"status": "TOOL_ERROR" if len(calls) == 1 else "PASS"}, "unit_fake_not_plc"

            stage_result(work, "formal", "hash", {"retry_infra": False}, action)
            stage_result(work, "formal", "hash", {"retry_infra": False}, action)
            self.assertEqual(len(calls), 1)
            final = stage_result(work, "formal", "hash", {"retry_infra": True}, action)
            self.assertEqual(final["result"]["status"], "PASS")
            self.assertEqual([p.name for p in calls], ["attempt_0001", "attempt_0002"])
            self.assertTrue(calls[0].is_dir())

    def test_missing_candidate_never_constructs_model_client(self):
        with tempfile.TemporaryDirectory() as tmp, patch("plc_agent.llm.ResponsesClient") as client:
            options = {"out_dir": tmp, "source_dir": tmp, "settings": {}, "model": "test", "generate_missing": False}
            result = run_task({"task": {"id": "PUB001", "difficulty": "easy", "tests": []}, "options": options})
            self.assertEqual(result["status"], "MISSING_CANDIDATE")
            self.assertEqual(result["new_llm_calls"], 0)
            client.assert_not_called()

    def test_missing_selected_candidate_is_never_reported_as_pass(self):
        task = {"id": "PUB001", "difficulty": "easy", "tests": []}
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            record = base / "source/PUB001/generation/result.json"
            options = {"out_dir": str(base / "out"), "source_dir": str(base / "source"),
                       "settings": {}, "model": "test", "generate_missing": False}
            for old_status, expected in (("PASS", "UNVERIFIED"), ("COMPILE_FAIL", "FAIL")):
                write_json(record, {"task_id": task["id"], "task_sha256": digest(task), "model": "test", "status": old_status})
                result = run_task({"task": task, "options": options})
                self.assertEqual(result["status"], expected)

    def test_partial_formal_proof_cannot_become_full_pass(self):
        task = {"id": "PUB001", "difficulty": "easy", "tests": []}
        candidate = {"declaration": "FUNCTION_BLOCK FB_Task\nVAR END_VAR", "implementation": "", "supporting_objects": []}
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            write_json(base / "source/PUB001/generation/result.json", {
                "task_id": task["id"], "task_sha256": digest(task), "model": "test", "final_candidate": candidate})
            options = {"out_dir": str(base / "out"), "source_dir": str(base / "source"), "settings": {},
                       "model": "test", "generate_missing": False, "fingerprint": "unit", "retry_infra": False,
                       "recompile": True, "reuse_traces": False, "formal_timeout": 1,
                       "stages": ["compile", "functional", "formal"]}
            from plc_agent.compiler import CompileResult
            with patch("plc_agent.compiler.compile_st", return_value=CompileResult("PASS", success=True)), \
                 patch("plc_agent.simulation.run_functional", return_value={"status": "PASS"}), \
                 patch("plc_agent.formal_verify.verify_candidate", return_value={"status": "PASS", "full_specification_verified": False}):
                result = run_task({"task": task, "options": options})
            self.assertTrue(result["compiled"])
            self.assertTrue(result["stage_checks_passed"])
            self.assertEqual(result["status"], "PARTIAL")
            self.assertEqual(read_json(base / "out/PUB001/fullflow_result.json")["status"], "PARTIAL")

    def test_shared_lock_blocks_other_process_and_releases(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock_path = Path(tmp) / "shared.lock"
            code = ("import sys; from plc_agent.compiler import compiler_lock; "
                    "\nwith compiler_lock(timeout=0.2, path=sys.argv[1]): print('locked')")
            with compiler_lock(path=lock_path):
                blocked = subprocess.run([sys.executable, "-X", "utf8", "-c", code, str(lock_path)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15)
                self.assertNotEqual(blocked.returncode, 0)
                self.assertIn("TimeoutError", blocked.stderr)
            released = subprocess.run([sys.executable, "-X", "utf8", "-c", code, str(lock_path)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15)
            self.assertEqual(released.returncode, 0, released.stderr)
            self.assertIn("locked", released.stdout)


if __name__ == "__main__":
    unittest.main()
