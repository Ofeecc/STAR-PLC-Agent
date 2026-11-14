import unittest

from plc_agent.dataset import load_tasks
from plc_agent.functional import equal
from plc_agent.normalized_spec import reference_step
from plc_agent.random_testing import generate_random_cases
from plc_agent.scan_contract import SUPPORTED, ScanContract, check_contract_trace


class RandomTestingTests(unittest.TestCase):
    def test_all_32_tasks_supported_and_pass_fixed_tests(self):
        tasks = load_tasks()
        self.assertEqual(len(tasks), 32)
        all_ids = {t["id"] for t in tasks}
        self.assertEqual(len(all_ids), 32)

        expected_ids = {f"PUB{i:03d}" for i in range(1, 21)} | {f"SELF{i:03d}" for i in range(1, 13)}
        self.assertEqual(all_ids, expected_ids)
        self.assertTrue(expected_ids.issubset(SUPPORTED), f"Missing from SUPPORTED: {expected_ids - SUPPORTED}")

        for task in tasks:
            tid = task["id"]
            for case in task["tests"]:
                monitor = ScanContract(tid)
                rows = []
                for j, s in enumerate(case["steps"]):
                    with self.subTest(task=tid, case=case["id"], scan=j):
                        full_outputs = reference_step(task, monitor, s["inputs"], s.get("dt_ms"))
                        self.assertTrue(
                            equal(full_outputs, s["expected"]),
                            f"Output mismatch on {tid}/{case['id']} scan {j}: {full_outputs} vs {s['expected']}",
                        )
                        row = dict(inputs=s["inputs"], outputs=full_outputs)
                        if "dt_ms" in s:
                            row["dt_ms"] = s["dt_ms"]
                        rows.append(row)

                res = check_contract_trace(tid, rows)
                self.assertEqual(
                    res["status"],
                    "NO_VIOLATION_IN_OBSERVED_TRACE",
                    f"Contract violation on {tid}/{case['id']}: {res.get('violations')}",
                )
                self.assertEqual(res["violations"], [])

    def test_random_cases_deterministic_and_self_consistent(self):
        tasks = load_tasks()
        self.assertEqual(len(tasks), 32)

        for task in tasks:
            tid = task["id"]
            with self.subTest(task=tid):
                cases_a = generate_random_cases(task, seed=20261110)
                cases_b = generate_random_cases(task, seed=20261110)
                self.assertEqual(cases_a, cases_b, f"{tid} must be seed-deterministic")

                cases_c = generate_random_cases(task, seed=20261111)
                self.assertNotEqual(cases_a, cases_c, f"{tid} cases should vary with seed")

                self.assertGreater(len(cases_a), 0)
                for case in cases_a:
                    self.assertGreater(len(case["steps"]), 0)
                    res = check_contract_trace(tid, [dict(s, outputs=s["expected"]) for s in case["steps"]])
                    self.assertEqual(
                        res["status"],
                        "NO_VIOLATION_IN_OBSERVED_TRACE",
                        f"Generated random case violated contract on {tid}: {res.get('violations')}",
                    )
                    self.assertEqual(res["violations"], [])


if __name__ == "__main__":
    unittest.main()
