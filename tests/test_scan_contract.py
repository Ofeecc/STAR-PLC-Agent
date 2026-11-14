import unittest

from plc_agent.dataset import load_tasks
from plc_agent.functional import equal
from plc_agent.normalized_spec import reference_step
from plc_agent.scan_contract import SUPPORTED, ScanContract, check_contract_trace


class ScanContractTests(unittest.TestCase):
    def test_existing_expected_constants_agree(self):
        for task in load_tasks():
            if task["id"] not in SUPPORTED:
                continue
            for case in task["tests"]:
                monitor = ScanContract(task["id"])
                for j, s in enumerate(case["steps"]):
                    with self.subTest(task=task["id"], case=case["id"], scan=j):
                        self.assertTrue(
                            equal(reference_step(task, monitor, s["inputs"], s.get("dt_ms")), s["expected"])
                        )

    def test_filling_wait_and_reset_outputs(self):
        names = [
            "bottleSensor",
            "cleaningConfirmButton",
            "fillingConfirmButton",
            "cappingConfirmButton",
            "packingConfirmButton",
            "finishedButton",
        ]
        m = ScanContract("PUB001")
        for index, event in enumerate(names):
            active = {n: n == event for n in names}
            o = m.step(active)
            self.assertEqual(sum(o.values()), 0 if index == 5 else 1)
            waiting = m.step(dict.fromkeys(names, False))
            self.assertEqual(waiting, o)

    def test_temperature_fault_does_not_clear_cooldown(self):
        m = ScanContract("PUB010")
        i = dict(TemperatureSensorInput=20, SetTemperature=30)
        self.assertTrue(m.step(i, 0)["HeaterOutput"])
        self.assertTrue(m.step(i, 5000)["OverheatProtection"])
        self.assertTrue(m.step(dict(i, TemperatureSensorInput=-1), 1000)["OverheatProtection"])
        self.assertFalse(m.step(i, 1999)["HeaterOutput"])
        self.assertTrue(m.step(i, 1)["HeaterOutput"])

    def test_missing_output_and_constant_stopped_pump_rejected(self):
        rows = [
            dict(
                inputs=dict(Demand=True, FaultA=True, FaultB=False), outputs=dict(PumpA=False, PumpB=False, LeadA=True)
            )
        ]
        self.assertEqual(check_contract_trace("SELF007", rows)["status"], "VIOLATED")
        rows[0]["outputs"].pop("LeadA")
        self.assertTrue(any(v["missing"] for v in check_contract_trace("SELF007", rows)["violations"]))

    def test_no_observations_and_unsupported_are_not_pass(self):
        self.assertEqual(check_contract_trace("PUB999", [])["status"], "UNSUPPORTED")
        self.assertEqual(check_contract_trace("PUB001", [])["status"], "INCOMPLETE")

    def test_timer_does_not_silently_assume_zero(self):
        with self.assertRaises(ValueError):
            ScanContract("PUB010").step(dict(TemperatureSensorInput=20, SetTemperature=30))


if __name__ == "__main__":
    unittest.main()
