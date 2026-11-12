import json
import tempfile
import unittest
from pathlib import Path

from plc_agent.config import ROOT
from plc_agent.model_checker import check_model, find_nusmv

REFERENCE_TASKS = [
    ("public", "PUB001", "PUB001_complete.smv"),
    ("public", "PUB011", "PUB011_reference.smv"),
    *[("self_built", f"SELF{i:03d}", f"SELF{i:03d}_reference.smv") for i in range(1, 13)],
]

POSITIVE_MODELS = ["PUB001_reference.smv"] + [item[2] for item in REFERENCE_TASKS]

MUTANT_EXPECTATIONS = {
    "negative_control.smv": (1, 1, ("value < 2",)),
    "PUB001_mutant.smv": (10, 1, ("!cleaningConfirmButton", "Pump_Motor")),
    "PUB011_mutant.smv": (6, 1, ("WAIT_A", "MOVE_AB")),
    "SELF001_mutant.smv": (3, 1, ("Run <-> qRun",)),
    "SELF002_mutant.smv": (1, 2, ("qReverse", "qForward")),
    "SELF003_mutant.smv": (7, 1, ("!Start", "Run <-> qRun")),
    "SELF004_mutant.smv": (7, 1, ("Stop", "qIdle")),
    "SELF005_mutant.smv": (7, 1, ("qAge < 2", "qPhase = 1")),
    "SELF006_mutant.smv": (1, 1, ("middle & !Inhibit",)),
    "SELF007_mutant.smv": (7, 2, ("FaultA", "PumpB", "FaultB", "PumpA")),
    "SELF008_mutant.smv": (1, 1, ("Count <= Preset",)),
    "SELF009_mutant.smv": (2, 1, ("qPulse <-> PartPulse",)),
    "SELF010_mutant.smv": (6, 1, ("!validReset", "qAck")),
    "SELF011_mutant.smv": (9, 1, ("qClamp", "!ClampDone")),
    "SELF012_mutant.smv": (7, 1, ("mode = IDLE", "qRunning")),
}


def _task_io_names(task: dict) -> list[str]:
    iface = task["interface"]
    if isinstance(iface, list):
        return [entry["name"] for entry in iface]
    return [entry["name"] for entry in iface.get("inputs", []) + iface.get("outputs", [])]


class SmvModelsTests(unittest.TestCase):
    def test_smv_models_cover_task_interfaces_and_clean_comments(self):
        for subdir, task_id, filename in REFERENCE_TASKS:
            with self.subTest(task=task_id, model=filename):
                task = json.loads((ROOT / "dataset" / subdir / f"{task_id}.json").read_text(encoding="utf-8"))
                smv_text = (ROOT / "models" / filename).read_text(encoding="utf-8")
                for var_name in _task_io_names(task):
                    self.assertIn(var_name, smv_text)

        pub001 = json.loads((ROOT / "dataset/public/PUB001.json").read_text(encoding="utf-8"))
        pub001_complete = (ROOT / "models/PUB001_complete.smv").read_text(encoding="utf-8")
        for prop in pub001["ltl"]:
            if prop["id"] in {"P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11"}:
                self.assertIn(prop["formula"], pub001_complete)

        for smv_path in sorted((ROOT / "models").glob("*.smv")):
            with self.subTest(comment_check=smv_path.name):
                for line in smv_path.read_text(encoding="utf-8").splitlines():
                    stripped = line.strip()
                    if stripped.startswith("--"):
                        self.assertNotIn("LTLSPEC", stripped)
                        self.assertNotIn("INVARSPEC", stripped)

    def test_positive_and_mutant_models_verify_under_nusmv(self):
        try:
            exe = find_nusmv()
        except ValueError:
            self.skipTest("Local NuSMV executable not installed")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            for filename in POSITIVE_MODELS:
                with self.subTest(positive=filename):
                    res = check_model(ROOT / "models" / filename, tmp_root / filename[:-4], str(exe), timeout=30)
                    self.assertEqual(res["status"], "MODEL_PROPERTIES_TRUE")
                    self.assertGreater(res["expected_properties"], 0)
                    self.assertEqual(res["checked_properties"], res["expected_properties"])
                    self.assertEqual(res["scope"], "EXPLICIT_SMV_MODEL_ONLY")
                    self.assertFalse(res["candidate_st_verified"])
                    self.assertTrue(all(item["holds"] for item in res["property_results"]))

            for filename, (exp_pass, exp_fail, markers) in MUTANT_EXPECTATIONS.items():
                with self.subTest(mutant=filename):
                    res = check_model(ROOT / "models" / filename, tmp_root / filename[:-4], str(exe), timeout=30)
                    self.assertEqual(res["status"], "COUNTEREXAMPLE")
                    self.assertEqual(res["checked_properties"], res["expected_properties"])
                    passed = [item for item in res["property_results"] if item["holds"]]
                    failed = [item for item in res["property_results"] if not item["holds"]]
                    self.assertEqual(len(passed), exp_pass)
                    self.assertEqual(len(failed), exp_fail)
                    joined_fail = " ".join(item["expression"] for item in failed)
                    self.assertTrue(any(marker in joined_fail for marker in markers), joined_fail)


if __name__ == "__main__":
    unittest.main()
