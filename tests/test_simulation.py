"""Offline tests of the real simulation adapter, with no runtime claims."""
import copy
import unittest
from plc_agent.dataset import load_tasks
from plc_agent.simulation import build_program, eligibility, st_literal

class SimulationAdapterTests(unittest.TestCase):
    def test_all_twelve_self_tasks_have_untimed_scalar_adapter(self):
        for task in load_tasks():
            if task["kind"] == "self_built":
                with self.subTest(task=task["id"]):
                    self.assertEqual(eligibility(task), [])
                    program = build_program(task)
                    self.assertEqual(program["step_count"], sum(len(c["steps"]) for c in task["tests"]))
                    self.assertEqual(program["implementation"].count("BenchCalls := BenchCalls + 1;"), program["step_count"])

    def test_expected_answers_cannot_influence_the_executed_test_program(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        before = build_program(task)
        mutated = copy.deepcopy(task)
        for case in mutated["tests"]:
            for step in case["steps"]:
                step["expected"] = {"impossible_marker": "NOT_EXECUTED_ANSWER"}
        self.assertEqual(build_program(mutated), before)
        self.assertNotIn("NOT_EXECUTED_ANSWER", before["implementation"])

    def test_fresh_instance_for_every_case(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        program = build_program(task)
        for index, case in enumerate(task["tests"]):
            self.assertIn(f"BenchUut{index} : FB_Task;", program["declaration"])
            self.assertEqual(program["implementation"].count(f"BenchUut{index}();"), len(case["steps"]))

    def test_physical_timing_and_generic_bindings_are_explicitly_unsupported(self):
        tasks = {t["id"]: t for t in load_tasks()}
        self.assertTrue(eligibility(tasks["PUB004"]))
        self.assertTrue(eligibility(tasks["PUB018"]))
        with self.assertRaises(ValueError):
            build_program(tasks["PUB018"])

    def test_scalar_literals_preserve_type_and_reject_bool_as_number(self):
        self.assertEqual(st_literal(True, "BOOL"), "TRUE")
        self.assertEqual(st_literal(4294967295, "DWORD"), "DWORD#4294967295")
        self.assertEqual(st_literal("a'b$c", "STRING(254)"), "'a$'b$$c'")
        with self.assertRaises(ValueError):
            st_literal(True, "INT")

if __name__ == "__main__":
    unittest.main()
