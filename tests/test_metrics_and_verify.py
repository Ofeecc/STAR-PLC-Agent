from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from plc_agent.common import ROOT, read_json
from plc_agent.dataset import load_tasks
from plc_agent.formal_verify import export_verification_bundle, import_verification_evidence
from plc_agent.metrics import aggregate, bootstrap_ci, mcnemar_exact


class MetricsAndVerificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.work_dir = Path(self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_mcnemar_exact_formula_and_bounds(self):
        # b=0, c=6 -> exactly 0.03125
        p = mcnemar_exact(0, 6)
        self.assertAlmostEqual(p, 0.03125, places=5)

        # Symmetry: b=6, c=0 -> 0.03125
        self.assertAlmostEqual(mcnemar_exact(6, 0), 0.03125, places=5)

        # b=0, c=0 -> 1.0
        self.assertEqual(mcnemar_exact(0, 0), 1.0)

        # b=5, c=5 -> 1.0 (capped at 1.0)
        self.assertEqual(mcnemar_exact(5, 5), 1.0)

        # b=1, c=10 -> p-value is significant (< 0.05)
        p_skew = mcnemar_exact(1, 10)
        self.assertTrue(0.0 < p_skew < 0.05)

        # Negative inputs must raise ValueError
        with self.assertRaises(ValueError):
            mcnemar_exact(-1, 5)
        with self.assertRaises(ValueError):
            mcnemar_exact(5, -2)

    def test_bootstrap_ci_coverage_and_reproducibility(self):
        # 28 ones, 4 zeros -> mean is 0.875
        values = [1.0] * 28 + [0.0] * 4
        low, high = bootstrap_ci(values, n_boot=2000, seed=42)
        self.assertLessEqual(low, 0.875)
        self.assertGreaterEqual(high, 0.875)
        self.assertGreater(low, 0.65)
        self.assertLess(high, 1.0)

        # Determinism with same seed
        low2, high2 = bootstrap_ci(values, n_boot=2000, seed=42)
        self.assertEqual(low, low2)
        self.assertEqual(high, high2)

        # Uniform all-ones values give (1.0, 1.0)
        low_ones, high_ones = bootstrap_ci([1.0] * 10, n_boot=500, seed=42)
        self.assertEqual(low_ones, 1.0)
        self.assertEqual(high_ones, 1.0)

        # Empty values raise ValueError
        with self.assertRaises(ValueError):
            bootstrap_ci([])

    def test_experiments_json_defines_all_conditions(self):
        config_path = ROOT / "configs/experiments.json"
        self.assertTrue(config_path.is_file())
        data = read_json(config_path)
        conditions = data.get("conditions", [])
        condition_ids = {c["id"] for c in conditions}

        expected_ids = {"E1", "E2", "E3", "E4", "A1", "A2", "A3", "S1", "S2"}
        self.assertTrue(
            expected_ids.issubset(condition_ids),
            f"Missing required conditions: {expected_ids - condition_ids}",
        )

        # Check metadata on all conditions
        for cond in conditions:
            cid = cond["id"]
            if cid in expected_ids:
                self.assertIn("framework", cond, f"Missing framework in {cid}")
                self.assertIn("model", cond, f"Missing model in {cid}")
                self.assertIn("spec_visible", cond, f"Missing spec_visible in {cid}")
                self.assertIn("ablation", cond, f"Missing ablation in {cid}")
                self.assertIn("budgets", cond, f"Missing budgets in {cid}")

        # Specific ablation metadata checks
        by_id = {c["id"]: c for c in conditions}
        self.assertIn(by_id["A1"]["ablation"], ("no_planner",))
        self.assertIn(by_id["A2"]["ablation"], ("no_dialect", "no_dialect_cards"))
        self.assertIn(by_id["A3"]["ablation"], ("no_selftest", "no_self_test"))
        self.assertFalse(by_id["S1"]["spec_visible"])
        self.assertFalse(by_id["S2"]["spec_visible"])
        self.assertTrue(by_id["E3"]["spec_visible"])

    def test_export_verification_bundle_files_and_manifest(self):
        tasks = load_tasks()
        task = next(t for t in tasks if t["id"] == "PUB001")
        candidate = {
            "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT\n bottleSensor : BOOL;\n cleaningConfirmButton : BOOL;\n fillingConfirmButton : BOOL;\n cappingConfirmButton : BOOL;\n packingConfirmButton : BOOL;\n finishedButton : BOOL;\nEND_VAR\nVAR_OUTPUT\n Pump_Motor : BOOL;\n Filling_Valve : BOOL;\n Capping_Machine : BOOL;\n Packing_Machine : BOOL;\n Completion_Light : BOOL;\nEND_VAR",
            "implementation": "Pump_Motor := bottleSensor;\nFilling_Valve := cleaningConfirmButton;\nCapping_Machine := fillingConfirmButton;\nPacking_Machine := cappingConfirmButton;\nCompletion_Light := packingConfirmButton;",
            "supporting_objects": [
                {
                    "name": "DUT_Helper",
                    "kind": "DUT",
                    "declaration": "TYPE DUT_Helper : STRUCT\n  flag : BOOL;\nEND_STRUCT\nEND_TYPE",
                    "implementation": "",
                }
            ],
        }

        bundle_dir = self.work_dir / "bundle_pub001"
        manifest = export_verification_bundle(task, candidate, bundle_dir)

        # Check bundle directory contents
        st_file = bundle_dir / "candidate.st"
        ltl_file = bundle_dir / "spec.ltl"
        manifest_file = bundle_dir / "verification_manifest.json"

        self.assertTrue(st_file.is_file())
        self.assertTrue(ltl_file.is_file())
        self.assertTrue(manifest_file.is_file())

        # Verify candidate.st includes FB_Task and supporting DUT
        st_content = st_file.read_text(encoding="utf-8")
        self.assertIn("FB_Task", st_content)
        self.assertIn("DUT_Helper", st_content)
        self.assertIn("END_FUNCTION_BLOCK", st_content)

        # Verify spec.ltl contains property IDs and formulas
        ltl_content = ltl_file.read_text(encoding="utf-8")
        self.assertIn("P1", ltl_content)
        self.assertIn("P2", ltl_content)
        self.assertIn("init", ltl_content)

        # Verify manifest structure
        self.assertEqual(manifest["task_id"], "PUB001")
        self.assertEqual(manifest["tools_supported"], [])
        self.assertFalse(manifest["encoding_complete"])
        self.assertEqual(manifest["st_path"], "candidate.st")
        self.assertEqual(manifest["ltl_path"], "spec.ltl")
        self.assertIsInstance(manifest["properties"], list)
        self.assertGreater(len(manifest["properties"]), 0)
        self.assertIn("phase", manifest["atomic_propositions"])

        # String candidate input also works
        raw_st = "FUNCTION_BLOCK FB_Task\nVAR_INPUT Start:BOOL; END_VAR\nVAR_OUTPUT Run:BOOL; END_VAR\nRun := Start;\nEND_FUNCTION_BLOCK"
        bundle_str = self.work_dir / "bundle_str"
        manifest_str = export_verification_bundle(task, raw_st, bundle_str)
        self.assertEqual(manifest_str["task_id"], "PUB001")
        self.assertTrue((bundle_str / "candidate.st").is_file())

    def test_import_verification_evidence(self):
        bundle_dir = self.work_dir / "bundle_verify"
        bundle_dir.mkdir(parents=True)

        # Test SAT evidence
        sat_evidence = bundle_dir / "nuxmv_sat.log"
        sat_evidence.write_text(
            "-- specification P1 is true\n-- specification P2 is true\nresult: SAT\n",
            encoding="utf-8",
        )
        res_sat = import_verification_evidence(bundle_dir, sat_evidence)
        self.assertEqual(res_sat["status"], "PROPERTIES_TRUE")
        self.assertFalse(res_sat["verified"])
        self.assertTrue((bundle_dir / "verification_result.json").is_file())

        # Test Counterexample evidence
        cex_evidence = bundle_dir / "nuxmv_cex.log"
        cex_evidence.write_text(
            "-- specification P1 is true\n-- specification P2 is false\n-- as demonstrated by the following execution trace\nTrace Type: Counterexample\n",
            encoding="utf-8",
        )
        res_cex = import_verification_evidence(bundle_dir, cex_evidence)
        self.assertEqual(res_cex["status"], "COUNTEREXAMPLE")
        self.assertFalse(res_cex["verified"])

        # Test JSON evidence
        json_evidence = bundle_dir / "evidence.json"
        json_evidence.write_text(
            json.dumps({"status": "UNSAT", "details": {"bounded_steps": 50}}),
            encoding="utf-8",
        )
        res_json = import_verification_evidence(bundle_dir, json_evidence)
        self.assertEqual(res_json["status"], "UNSAT")
        self.assertFalse(res_json["verified"])

    def test_aggregate_with_statistical_metrics(self):
        # Build mock records for E1 (baseline) and E3 (STAR v2)
        tasks = load_tasks()
        planned_tasks = len(tasks)

        e1_records = []
        e3_records = []
        for i, t in enumerate(tasks):
            # E1 passes first 16, fails rest
            e1_pass = i < 16
            e1_records.append({
                "condition": "E1",
                "task_id": t["id"],
                "framework": "baseline",
                "model": "deepseek-v4.1-flash",
                "status": "PASS" if e1_pass else "TEST_FAIL",
                "first_pass_compiled": e1_pass,
                "final_compiled": e1_pass,
                "repair_attempts": 0,
                "compilation_attempts": [{"status": "PASS" if e1_pass else "COMPILE_FAIL", "success": e1_pass}],
                "functional": {
                    "status": "PASS" if e1_pass else "TEST_FAIL",
                    "planned_cases": 2,
                    "evaluated_cases": 2,
                    "passed_cases": 2 if e1_pass else 1,
                    "passed_steps": 4 if e1_pass else 2,
                    "evaluated_steps": 4,
                    "evidence": "CODESYS_SIMULATION",
                },
                "usage": [],
                "elapsed_seconds": 10.0,
                "api_cost": 0.05,
            })

            # E3 passes first 28, fails rest (outperforms E1)
            e3_pass = i < 28
            e3_records.append({
                "condition": "E3",
                "task_id": t["id"],
                "framework": "self_harness",
                "model": "deepseek-v4.1-flash",
                "status": "PASS" if e3_pass else "TEST_FAIL",
                "first_pass_compiled": e3_pass,
                "final_compiled": e3_pass,
                "repair_attempts": 0,
                "compilation_attempts": [{"status": "PASS" if e3_pass else "COMPILE_FAIL", "success": e3_pass}],
                "functional": {
                    "status": "PASS" if e3_pass else "TEST_FAIL",
                    "planned_cases": 2,
                    "evaluated_cases": 2,
                    "passed_cases": 2 if e3_pass else 1,
                    "passed_steps": 4 if e3_pass else 2,
                    "evaluated_steps": 4,
                    "evidence": "CODESYS_SIMULATION",
                },
                "usage": [],
                "elapsed_seconds": 15.0,
                "api_cost": 0.08,
            })

        all_records = e1_records + e3_records
        agg = aggregate(all_records, planned_tasks)
        by_cond = {c["condition"]: c for c in agg}

        # Check E1 metrics
        e1_agg = by_cond["E1"]
        self.assertEqual(e1_agg["first_pass_compiled_tasks"], 16)
        self.assertEqual(e1_agg["final_compiled_tasks"], 16)
        self.assertIn("compilation_rate_ci", e1_agg)
        self.assertIn("test_task_pass_rate_ci", e1_agg)

        # Check E3 metrics and McNemar against E1
        e3_agg = by_cond["E3"]
        self.assertEqual(e3_agg["first_pass_compiled_tasks"], 28)
        self.assertEqual(e3_agg["final_compiled_tasks"], 28)
        self.assertIn("mcnemar_p_value_vs_baseline", e3_agg)
        # E3 has 12 discordant tasks where E3=1, E1=0, and 0 where E3=0, E1=1.
        # McNemar p for b=12, c=0 is 2*(0.5^12) = 0.000488 < 0.05
        self.assertLess(e3_agg["mcnemar_p_value_vs_baseline"], 0.01)

    def test_cli_subcommands_export_import_and_random_test(self):
        import subprocess
        import sys

        # Test CLI help contains new subcommands
        res = subprocess.run(
            [sys.executable, "-m", "plc_agent.cli", "--help"],
            capture_output=True,
            text=True, encoding="utf-8",
            cwd=str(ROOT),
            env={"PYTHONPATH": str(ROOT / "src"), "PYTHONUTF8": "1"},
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("export-verify", res.stdout)
        self.assertIn("import-verify", res.stdout)
        self.assertIn("random-test", res.stdout)

        # Test CLI random-test
        rand_out = self.work_dir / "random_cases.json"
        res_rand = subprocess.run(
            [
                sys.executable,
                "-m",
                "plc_agent.cli",
                "random-test",
                "--task",
                "PUB001",
                "--seed",
                "12345",
                "--num-cases",
                "2",
                "--steps-per-case",
                "3",
                "--out",
                str(rand_out),
            ],
            capture_output=True,
            text=True, encoding="utf-8",
            cwd=str(ROOT),
            env={"PYTHONPATH": str(ROOT / "src"), "PYTHONUTF8": "1"},
        )
        self.assertEqual(res_rand.returncode, 0, res_rand.stderr)
        self.assertTrue(rand_out.is_file())
        cases = json.loads(rand_out.read_text(encoding="utf-8"))
        self.assertEqual(len(cases), 2)
        self.assertEqual(len(cases[0]["steps"]), 3)

        # Test CLI export-verify
        cand_file = self.work_dir / "candidate.json"
        cand_file.write_text(
            json.dumps({
                "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT A:BOOL; END_VAR\nVAR_OUTPUT B:BOOL; END_VAR",
                "implementation": "B := A;",
                "supporting_objects": [],
            }),
            encoding="utf-8",
        )
        bundle_dir = self.work_dir / "cli_bundle"
        res_exp = subprocess.run(
            [
                sys.executable,
                "-m",
                "plc_agent.cli",
                "export-verify",
                "--task",
                "PUB001",
                "--candidate",
                str(cand_file),
                "--out-dir",
                str(bundle_dir),
            ],
            capture_output=True,
            text=True, encoding="utf-8",
            cwd=str(ROOT),
            env={"PYTHONPATH": str(ROOT / "src"), "PYTHONUTF8": "1"},
        )
        self.assertEqual(res_exp.returncode, 0, res_exp.stderr)
        self.assertTrue((bundle_dir / "verification_manifest.json").is_file())
        self.assertTrue((bundle_dir / "candidate.st").is_file())
        self.assertTrue((bundle_dir / "spec.ltl").is_file())

        # Test CLI import-verify
        ev_file = bundle_dir / "evidence.txt"
        ev_file.write_text("result: SAT\n-- specification is true\n", encoding="utf-8")
        res_imp = subprocess.run(
            [
                sys.executable,
                "-m",
                "plc_agent.cli",
                "import-verify",
                "--bundle-dir",
                str(bundle_dir),
                "--evidence",
                str(ev_file),
            ],
            capture_output=True,
            text=True, encoding="utf-8",
            cwd=str(ROOT),
            env={"PYTHONPATH": str(ROOT / "src"), "PYTHONUTF8": "1"},
        )
        self.assertEqual(res_imp.returncode, 0, res_imp.stderr)
        self.assertTrue((bundle_dir / "verification_result.json").is_file())
        ver_res = json.loads((bundle_dir / "verification_result.json").read_text(encoding="utf-8"))
        self.assertEqual(ver_res["status"], "PROPERTIES_TRUE")
        self.assertFalse(ver_res["verified"])


if __name__ == "__main__":
    unittest.main()
