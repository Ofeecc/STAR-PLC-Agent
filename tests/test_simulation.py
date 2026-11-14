"""Offline tests of the real simulation adapter, with no runtime claims."""

import copy
import unittest
from pathlib import Path

from plc_agent.dataset import load_tasks
from plc_agent.functional import evaluate_trace
from plc_agent.simulation import build_program, eligibility, st_literal, unflatten_observations


class SimulationAdapterTests(unittest.TestCase):
    def test_all_twelve_self_tasks_have_untimed_scalar_adapter(self):
        for task in load_tasks():
            if task["kind"] == "self_built":
                with self.subTest(task=task["id"]):
                    self.assertEqual(eligibility(task), [])
                    program = build_program(task)
                    self.assertEqual(program["step_count"], sum(len(c["steps"]) for c in task["tests"]))
                    self.assertEqual(
                        program["implementation"].count("BenchCalls := BenchCalls + 1;"), program["step_count"]
                    )

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

    def test_all_32_tasks_eligible_and_build_program(self):
        for task in load_tasks():
            with self.subTest(task=task["id"]):
                self.assertEqual(eligibility(task), [], task["id"])
                prog = build_program(task)
                self.assertGreater(prog["step_count"], 0)
                self.assertIn("PROGRAM PLC_PRG", prog["declaration"])

    def test_build_program_timed_gate_and_dt_trace(self):
        pub004 = next(t for t in load_tasks() if t["id"] == "PUB004")
        prog = build_program(pub004)
        self.assertIn("TIME()", prog["implementation"])
        self.assertIn("TraceDt", prog["declaration"])

    def test_build_program_inout_binding_retains_storage_after_step_zero(self):
        pub017 = next(t for t in load_tasks() if t["id"] == "PUB017")
        prog = build_program(pub017)
        impl = prog["implementation"]
        step0_block = impl.split(" 0:")[1].split(" 1:")[0]
        step1_block = impl.split(" 1:")[1].split(" 2:")[0]
        self.assertIn("Binding_0_recipe[1].recipeID := INT#0;", step0_block)
        self.assertNotIn("Binding_0_recipe[1].recipeID :=", step1_block)

    def test_scalar_literals_preserve_type_and_reject_bool_as_number(self):
        self.assertEqual(st_literal(True, "BOOL"), "TRUE")
        self.assertEqual(st_literal(4294967295, "DWORD"), "DWORD#4294967295")
        self.assertEqual(st_literal("a'b$c", "STRING(254)"), "'a$'b$$c'")
        with self.assertRaises(ValueError):
            st_literal(True, "INT")

    def test_time_literals_and_composite_serialization(self):
        self.assertEqual(st_literal("T#100ms", "TIME"), "T#100ms")
        self.assertEqual(st_literal(200, "TIME"), "TIME#200ms")
        self.assertEqual(st_literal("LTIME#500ms", "LTIME"), "LTIME#500ms")
        self.assertEqual(st_literal(1000, "LTIME"), "LTIME#1000ms")
        self.assertEqual(st_literal([1, 2, 3], "ARRAY[1..3] OF INT"), "[INT#1, INT#2, INT#3]")
        self.assertEqual(
            st_literal({"recipeID": 1, "ingredientType": 2}, "ST_Recipe"),
            "(recipeID := INT#1, ingredientType := INT#2)",
        )

    def test_build_program_custom_cases(self):
        pub004 = next(t for t in load_tasks() if t["id"] == "PUB004")
        custom_cases = [
            {
                "id": "custom1",
                "steps": [
                    {
                        "inputs": {
                            "VISCOSITY_OK": True,
                            "PASTE_E_STOP_NC": True,
                            "DebounceTime": "T#1s",
                            "CycleTime": "T#100ms",
                        },
                        "expected": {},
                        "dt_ms": 0,
                    },
                    {
                        "inputs": {
                            "VISCOSITY_OK": True,
                            "PASTE_E_STOP_NC": True,
                            "DebounceTime": "T#1s",
                            "CycleTime": "T#100ms",
                        },
                        "expected": {},
                        "dt_ms": 100,
                    },
                ],
            }
        ]
        self.assertEqual(eligibility(pub004, cases=custom_cases), [])
        prog = build_program(pub004, cases=custom_cases)
        self.assertEqual(prog["step_count"], 2)
        self.assertIn("BenchUut0", prog["declaration"])
        self.assertNotIn("BenchUut1", prog["declaration"])

    def test_unflatten_observations_reconstruction(self):
        pub017 = next(t for t in load_tasks() if t["id"] == "PUB017")
        single_step_case = [{"id": pub017["tests"][0]["id"], "steps": [pub017["tests"][0]["steps"][0]]}]
        prog = build_program(pub017, cases=single_step_case)
        raw_monitoring = {
            "PLC_PRG.TraceIn_addRecipe[0]": "FALSE",
            "PLC_PRG.TraceIn_deleteRecipe[0]": "FALSE",
            "PLC_PRG.TraceIn_modifyRecipe[0]": "FALSE",
            "PLC_PRG.TraceIn_queryRecipe[0]": "FALSE",
            "PLC_PRG.TraceIn_recipeIn_recipeID[0]": "0",
            "PLC_PRG.TraceIn_recipeIn_ingredientType[0]": "0",
            "PLC_PRG.TraceIn_recipeIn_ingredientRatio[0]": "0.0",
            "PLC_PRG.TraceIn_recipeIn_productionTemperature[0]": "0.0",
            "PLC_PRG.TraceOut_recipeAdded[0]": "FALSE",
            "PLC_PRG.TraceOut_recipeDeleted[0]": "FALSE",
            "PLC_PRG.TraceOut_recipeModified[0]": "FALSE",
            "PLC_PRG.TraceOut_error[0]": "FALSE",
            "PLC_PRG.TraceOut_status[0]": "16#0000",
            "PLC_PRG.TraceOut_recipeQueryResult_recipeID[0]": "42",
            "PLC_PRG.TraceOut_recipeQueryResult_ingredientType[0]": "7",
            "PLC_PRG.TraceOut_recipeQueryResult_ingredientRatio[0]": "0.75",
            "PLC_PRG.TraceOut_recipeQueryResult_productionTemperature[0]": "65.5",
        }
        # Step 0
        obs = unflatten_observations(prog, raw_monitoring)
        self.assertEqual(len(obs), 1)
        step0 = obs[0]
        self.assertEqual(step0["inputs"]["addRecipe"], False)
        self.assertEqual(step0["inputs"]["recipeIn"]["recipeID"], 0)
        self.assertTrue(
            isinstance(step0["inputs"]["recipe"], dict) and step0["inputs"]["recipe"].get("$binding") == "recipe"
        )
        self.assertEqual(step0["outputs"]["recipeAdded"], False)
        self.assertEqual(step0["outputs"]["status"], 0)
        self.assertEqual(step0["outputs"]["recipeQueryResult"]["recipeID"], 42)
        self.assertEqual(step0["outputs"]["recipeQueryResult"]["ingredientType"], 7)
        self.assertAlmostEqual(step0["outputs"]["recipeQueryResult"]["ingredientRatio"], 0.75)
        self.assertAlmostEqual(step0["outputs"]["recipeQueryResult"]["productionTemperature"], 65.5)

    def test_functional_default_timing_tolerance(self):
        from plc_agent.common import digest

        task = {
            "id": "PUB999_TEST",
            "interface": [
                {"direction": "INPUT", "name": "In", "type": "BOOL"},
                {"direction": "OUTPUT", "name": "Out", "type": "BOOL"},
            ],
            "tests": [{"id": "T1", "steps": [{"inputs": {"In": True}, "expected": {"Out": True}, "dt_ms": 100}]}],
        }
        trace = {
            "task_id": "PUB999_TEST",
            "task_sha256": digest(task),
            "source_sha256": "fake_hash",
            "backend": "CODESYS_SIMULATION",
            "operator": "automated CODESYS IDE simulation scan sequencer",
            "observed_utc": "2026-11-10T12:00:00Z",
            "evidence_files": [],
            "cases": {
                "T1": [
                    {
                        "inputs": {"In": True},
                        "outputs": {"Out": True},
                        "dt_ms": 115,
                    }  # 15ms jitter, within default 25ms tolerance
                ]
            },
        }
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            (p / "ev.log").write_text("ok")
            trace["evidence_files"] = ["ev.log"]
            res = evaluate_trace(task, "fake_hash", trace, evidence_root=p)
            self.assertEqual(res["status"], "PASS")

            # But jitter > 25ms should fail:
            trace["cases"]["T1"][0]["dt_ms"] = 130
            with self.assertRaises(ValueError):
                evaluate_trace(task, "fake_hash", trace, evidence_root=p)


if __name__ == "__main__":
    unittest.main()
