import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from plc_agent import cli
from plc_agent.config import ROOT
from plc_agent.model_checker import (
    LTL_RESULTS_MARKER,
    SBMC_START_MARKER,
    _build_nuxmv_smt_script,
    _has_infinite_vars,
    _needs_smt_engine,
    _pick_checker_path,
    check_model,
    find_nuxmv,
    parse_results,
    resolve_model_checker,
)

# All 18 newly covered public tasks backed by nuXmv (reference property counts).
NUXMV_REFERENCE_MODELS = [
    ("PUB002", "PUB002_reference.smv", 8),
    ("PUB003", "PUB003_reference.smv", 11),
    ("PUB004", "PUB004_reference.smv", 7),
    ("PUB005", "PUB005_reference.smv", 6),
    ("PUB006", "PUB006_reference.smv", 6),
    ("PUB007", "PUB007_reference.smv", 5),
    ("PUB008", "PUB008_reference.smv", 8),
    ("PUB009", "PUB009_reference.smv", 7),
    ("PUB010", "PUB010_reference.smv", 11),
    ("PUB012", "PUB012_reference.smv", 7),
    ("PUB013", "PUB013_reference.smv", 7),
    ("PUB014", "PUB014_reference.smv", 3),
    ("PUB015", "PUB015_reference.smv", 11),
    ("PUB016", "PUB016_reference.smv", 6),
    ("PUB017", "PUB017_reference.smv", 7),
    ("PUB018", "PUB018_reference.smv", 5),
    ("PUB019", "PUB019_reference.smv", 10),
    ("PUB020", "PUB020_reference.smv", 10),
]

# Expected mutant verdicts: (pass_count, fail_count, substring markers in failed expressions).
NUXMV_MUTANT_MODELS = {
    "PUB002_mutant.smv": (6, 2, ("fallingBits",)),
    "PUB003_mutant.smv": (2, 1, ("hiAlarm = hiPrev",)),
    "PUB004_mutant.smv": (0, 3, ("VFD_RUN",)),
    "PUB005_mutant.smv": (0, 2, ("Weld_Soft_Start_Active", "next(clk) >= clk")),
    "PUB006_mutant.smv": (2, 1, ("AERATION_BLOWER_CYCLE_COUNT",)),
    "PUB007_mutant.smv": (1, 1, ("top3_1",)),
    "PUB008_mutant.smv": (1, 1, ("32769",)),
    "PUB009_mutant.smv": (1, 1, ("windowSize",)),
    "PUB010_mutant.smv": (2, 1, ("HeaterOutput",)),
    "PUB012_mutant.smv": (0, 2, ("hist0_now", "THICKNESS_ALARM")),
    "PUB013_mutant.smv": (0, 2, ("TEMP_SETPOINT_ADJUST", "SUPPLY_FAN_RUN")),
    "PUB014_mutant.smv": (1, 1, ("ipValue = 0",)),
    "PUB015_mutant.smv": (0, 2, ("all_off", "reset_cond")),
    "PUB016_mutant.smv": (1, 1, ("arrive -> stop_out",)),
    "PUB017_mutant.smv": (1, 1, ("32770", "32771")),
    "PUB018_mutant.smv": (1, 1, ("post_item = q0",)),
    "PUB019_mutant.smv": (0, 2, ("MoveDown", "all_off")),
    "PUB020_mutant.smv": (0, 2, ("firingTemp",)),
}


class NuXmvIntegrationTests(unittest.TestCase):
    def test_smt_feature_and_infinite_var_detection(self):
        finite_smv = "MODULE main\nVAR b : boolean; s : 0..7;\nINVARSPEC b;\n"
        self.assertFalse(_needs_smt_engine(finite_smv))
        self.assertFalse(_has_infinite_vars(finite_smv))

        word_smv = "MODULE main\nVAR w : unsigned word[32];\nINVARSPEC w = 0ud32_0;\n"
        self.assertTrue(_needs_smt_engine(word_smv))
        self.assertFalse(_has_infinite_vars(word_smv))

        inf_smv = "MODULE main\nVAR x : integer; y : real;\nINVARSPEC x >= 0;\n"
        self.assertTrue(_needs_smt_engine(inf_smv))
        self.assertTrue(_has_infinite_vars(inf_smv))

        arr_smv = "MODULE main\nVAR a : array 0..3 of real;\nINVARSPEC TRUE;\n"
        self.assertTrue(_needs_smt_engine(arr_smv))
        self.assertTrue(_has_infinite_vars(arr_smv))

    def test_pick_checker_path_prefers_wrapper_over_raw_usr_local_bin(self):
        wrapper = Path("/tmp/fake/nuXmv-2.2.0-linux64/nuXmv")
        raw_bin = Path("/tmp/fake/nuXmv-2.2.0-linux64/usr/local/bin/nuXmv")
        picked = _pick_checker_path([raw_bin, wrapper])
        self.assertEqual(picked, wrapper.resolve())

    def test_build_nuxmv_smt_script_orders_commands_and_markers(self):
        inf_script = _build_nuxmv_smt_script("VAR x : integer;", invar_count=2, ltl_count=1, bmc_bound=15)
        self.assertIn("go_msat\n", inf_script)
        self.assertNotIn("build_boolean_model", inf_script)
        self.assertIn("check_invar_ic3\n", inf_script)
        self.assertIn(
            f"echo {SBMC_START_MARKER}\nmsat_check_ltlspec_sbmc_inc -k 15\necho {LTL_RESULTS_MARKER}\ncheck_ltlspec_ic3\n",
            inf_script,
        )

        word_script = _build_nuxmv_smt_script("VAR w : unsigned word[32];", invar_count=1, ltl_count=0, bmc_bound=25)
        self.assertIn("go_msat\nbuild_boolean_model\ncheck_invar_ic3\nquit\n", word_script)

    def test_parse_results_strips_sbmc_phase_and_handles_ltl_and_invariant(self):
        stdout = "\n".join(
            [
                "-- invariant x >= 0  is true",
                SBMC_START_MARKER,
                "-- no counterexample found with bound 1",
                "-- LTL specification G (x >= 0)  is false",
                LTL_RESULTS_MARKER,
                "-- LTL specification G (x >= 0)  is true",
                "-- specification !dead  is false",
            ]
        )
        parsed = parse_results(stdout, "", 0, expected_count=3)
        self.assertEqual(parsed["status"], "COUNTEREXAMPLE")
        self.assertEqual(parsed["checked_properties"], 3)
        self.assertEqual([c["holds"] for c in parsed["property_results"]], [True, True, False])

    def test_resolve_and_check_model_reject_invalid_tool_or_ctl_in_smt(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fake_exe = tmp_path / "NuSMV"
            fake_exe.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            fake_exe.chmod(0o755)
            ctl_smv = tmp_path / "ctl.smv"
            ctl_smv.write_text("MODULE main\nVAR b : boolean;\nCTLSPEC AG b;\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                check_model(ctl_smv, tmp_path / "out1", executable=str(fake_exe), tool="nusmv", engine="smt")

            fake_nuxmv = tmp_path / "nuXmv"
            fake_nuxmv.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            fake_nuxmv.chmod(0o755)
            with self.assertRaises(ValueError):
                check_model(ctl_smv, tmp_path / "out2", executable=str(fake_nuxmv), tool="nuxmv", engine="smt")

            with mock.patch.dict(os.environ, {"NUXMV_EXE": str(fake_nuxmv)}, clear=False):
                self.assertEqual(find_nuxmv(), fake_nuxmv.resolve())
                label, exe = resolve_model_checker(tool="auto", needs_smt=True)
                self.assertEqual((label, exe), ("nuXmv", fake_nuxmv.resolve()))

    def test_cli_check_model_forwards_tool_and_engine(self):
        with tempfile.TemporaryDirectory() as tmp:
            smv_path = Path(tmp) / "m.smv"
            smv_path.write_text("MODULE main\nVAR x : boolean;\nINVARSPEC TRUE;\n", encoding="utf-8")
            fake_res = {"status": "MODEL_PROPERTIES_TRUE", "scope": "EXPLICIT_SMV_MODEL_ONLY"}
            buf = io.StringIO()
            with (
                mock.patch("plc_agent.model_checker.check_model", return_value=fake_res) as mocked,
                mock.patch.object(
                    sys,
                    "argv",
                    [
                        "plc-agent",
                        "check-model",
                        "--model",
                        str(smv_path),
                        "--out-dir",
                        str(Path(tmp) / "out"),
                        "--tool",
                        "nuxmv",
                        "--engine",
                        "smt",
                    ],
                ),
                contextlib.redirect_stdout(buf),
            ):
                rc = cli.main()
            self.assertEqual(rc, 0)
            mocked.assert_called_once()
            self.assertEqual(mocked.call_args.kwargs["tool"], "nuxmv")
            self.assertEqual(mocked.call_args.kwargs["engine"], "smt")
            self.assertEqual(json.loads(buf.getvalue())["status"], "MODEL_PROPERTIES_TRUE")

    def test_new_pub_reference_and_mutant_models_verify_under_nuxmv(self):
        try:
            exe = find_nuxmv()
        except ValueError:
            self.skipTest("Local nuXmv executable not installed")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            for task_id, filename, exp_props in NUXMV_REFERENCE_MODELS:
                with self.subTest(reference=filename):
                    res = check_model(
                        ROOT / "models" / filename,
                        tmp_root / f"ref_{task_id}",
                        executable=str(exe),
                        timeout=45,
                        tool="nuxmv",
                    )
                    self.assertEqual(res["status"], "MODEL_PROPERTIES_TRUE")
                    self.assertEqual(res["tool"], "nuXmv")
                    self.assertEqual(res["expected_properties"], exp_props)
                    self.assertEqual(res["checked_properties"], exp_props)
                    self.assertEqual(res["scope"], "EXPLICIT_SMV_MODEL_ONLY")
                    self.assertFalse(res["candidate_st_verified"])
                    self.assertTrue(all(item["holds"] for item in res["property_results"]))

            for filename, (exp_pass, exp_fail, markers) in NUXMV_MUTANT_MODELS.items():
                with self.subTest(mutant=filename):
                    res = check_model(
                        ROOT / "models" / filename,
                        tmp_root / f"mut_{filename[:-4]}",
                        executable=str(exe),
                        timeout=45,
                        tool="nuxmv",
                    )
                    self.assertEqual(res["status"], "COUNTEREXAMPLE")
                    self.assertEqual(res["tool"], "nuXmv")
                    self.assertEqual(res["checked_properties"], res["expected_properties"])
                    passed = [item for item in res["property_results"] if item["holds"]]
                    failed = [item for item in res["property_results"] if not item["holds"]]
                    self.assertEqual(len(passed), exp_pass)
                    self.assertEqual(len(failed), exp_fail)
                    joined_fail = " ".join(item["expression"] for item in failed)
                    self.assertTrue(any(marker in joined_fail for marker in markers), joined_fail)


if __name__ == "__main__":
    unittest.main()
