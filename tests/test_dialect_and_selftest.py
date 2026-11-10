import math
import unittest
from plc_agent.dataset import load_tasks
from plc_agent.task_view import agent_view
from plc_agent.dialect_cards import DIALECT_CARDS, select_dialect_cards
from plc_agent.selftest import validate_self_tests


class DialectAndSelfTestTests(unittest.TestCase):
    def test_registry_contains_required_eight_cards(self):
        expected_ids = {
            "variant_ref",
            "var_length_array",
            "ltime_ops",
            "ton_timer",
            "edge_detection",
            "inout_struct_array",
            "string_parsing",
            "case_state_machine",
        }
        self.assertLessEqual(len(DIALECT_CARDS), 8)
        self.assertEqual(set(DIALECT_CARDS.keys()), expected_ids)
        for cid, card in DIALECT_CARDS.items():
            self.assertEqual(card["id"], cid)
            self.assertIsInstance(card["title"], str)
            self.assertTrue(len(card["title"]) > 0)
            self.assertIsInstance(card["body"], str)
            lines = card["body"].splitlines()
            self.assertLessEqual(len(lines), 15, f"Card {cid} has {len(lines)} lines > 15")

    def test_select_dialect_cards_deterministic_and_capped(self):
        tasks = {t["id"]: agent_view(t) for t in load_tasks()}
        self.assertEqual(len(tasks), 32)

        # PUB018 uses VARIANT in/out
        pub018_cards = select_dialect_cards(tasks["PUB018"])
        self.assertIn("variant_ref", [c["id"] for c in pub018_cards])

        # PUB008 uses ARRAY[*] OF INT / ARRAY[*] OF ST_AnalogChannel
        pub008_cards = select_dialect_cards(tasks["PUB008"])
        self.assertIn("var_length_array", [c["id"] for c in pub008_cards])

        # Determinism across all tasks and capped constraints
        for tid, view in tasks.items():
            cards1 = select_dialect_cards(view)
            cards2 = select_dialect_cards(view)
            self.assertEqual(
                [c["id"] for c in cards1],
                [c["id"] for c in cards2],
                f"Non-deterministic card selection for {tid}",
            )
            self.assertLessEqual(len(cards1), 4, f"Task {tid} selected > 4 cards")
            for c in cards1:
                lines = c["body"].splitlines()
                self.assertLessEqual(len(lines), 15, f"Task {tid} card {c['id']} body > 15 lines")

    def test_select_dialect_cards_custom_max(self):
        task = next(t for t in load_tasks() if t["id"] == "PUB018")
        view = agent_view(task)
        cards_max1 = select_dialect_cards(view, max_cards=1)
        self.assertLessEqual(len(cards_max1), 1)
        cards_max2 = select_dialect_cards(view, max_cards=2)
        self.assertLessEqual(len(cards_max2), 2)

    def test_validate_self_tests_caps_duration_and_fields(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        view = agent_view(task)
        raw = [
            {
                "id": "S1",
                "purpose": "valid",
                "steps": [
                    {"inputs": {"Start": True, "Stop": False, "GuardClosed": True}, "expected": {"Run": True}, "dt_ms": 40000},
                    {"inputs": {"Start": False, "Stop": True, "GuardClosed": True}, "expected": {"Run": False}, "dt_ms": 40000},
                ],
            },
            {
                "id": "S_bad_field",
                "steps": [
                    {"inputs": {"Unknown": True}, "expected": {"Run": False}}
                ],
            },
            {
                "id": "S_neg_dt",
                "steps": [
                    {"inputs": {"Start": False, "Stop": False, "GuardClosed": False}, "expected": {"Run": False}, "dt_ms": -5}
                ],
            },
        ]
        cleaned = validate_self_tests(view, raw, max_total_dt_ms=60000)
        self.assertEqual(len(cleaned), 1)
        total_dt = sum(s.get("dt_ms", 0) for c in cleaned for s in c["steps"])
        self.assertLessEqual(total_dt, 60000)
        self.assertEqual(len(cleaned[0]["steps"]), 1)
        self.assertEqual(cleaned[0]["steps"][0]["dt_ms"], 40000)

    def test_validate_self_tests_rejects_direction_mismatches(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        view = agent_view(task)

        # Output variable placed into inputs
        raw_output_as_input = [{
            "id": "S_out_in",
            "steps": [{"inputs": {"Run": True}, "expected": {"Run": True}}]
        }]
        self.assertEqual(validate_self_tests(view, raw_output_as_input), [])

        # Input variable placed into expected
        raw_input_as_expected = [{
            "id": "S_in_exp",
            "steps": [{"inputs": {"Start": True}, "expected": {"Start": True}}]
        }]
        self.assertEqual(validate_self_tests(view, raw_input_as_expected), [])

    def test_validate_self_tests_rejects_non_finite_and_invalid_dt(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        view = agent_view(task)

        for bad_dt in [float("nan"), float("inf"), -float("inf"), "100", True, None]:
            raw = [{
                "id": "bad",
                "steps": [{"inputs": {"Start": True}, "expected": {"Run": True}, "dt_ms": bad_dt}]
            }]
            self.assertEqual(validate_self_tests(view, raw), [], f"Failed to reject bad dt: {bad_dt}")

    def test_validate_self_tests_caps_cases_and_steps_per_case(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        view = agent_view(task)

        # 6 valid cases
        raw_cases = [
            {
                "id": f"C{i}",
                "steps": [
                    {"inputs": {"Start": True, "Stop": False, "GuardClosed": True}, "expected": {"Run": True}, "dt_ms": 100}
                    for _ in range(25)  # 25 steps per case
                ]
            }
            for i in range(6)
        ]

        cleaned = validate_self_tests(
            view,
            raw_cases,
            max_cases=3,
            max_steps_per_case=5,
            max_total_dt_ms=60000,
        )
        self.assertEqual(len(cleaned), 3)
        for c in cleaned:
            self.assertEqual(len(c["steps"]), 5)

    def test_validate_self_tests_cumulative_budget_across_multiple_cases(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        view = agent_view(task)

        # Case 1: 2 steps of 20000 = 40000 ms
        # Case 2: 2 steps of 15000 = 30000 ms
        # Budget = 50000 ms
        # Case 1 should get both steps (40000 ms)
        # Case 2 should get only 1st step (10000 ms leftover, but step is 15000 > 10000, so 0 steps in Case 2)
        # Thus Case 2 is dropped because it has 0 steps within budget.
        raw = [
            {
                "id": "C1",
                "steps": [
                    {"inputs": {"Start": True}, "expected": {"Run": True}, "dt_ms": 20000},
                    {"inputs": {"Start": True}, "expected": {"Run": True}, "dt_ms": 20000},
                ],
            },
            {
                "id": "C2",
                "steps": [
                    {"inputs": {"Start": False}, "expected": {"Run": False}, "dt_ms": 15000},
                    {"inputs": {"Start": False}, "expected": {"Run": False}, "dt_ms": 15000},
                ],
            },
        ]
        cleaned = validate_self_tests(view, raw, max_total_dt_ms=50000)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0]["id"], "C1")
        self.assertEqual(len(cleaned[0]["steps"]), 2)

    def test_validate_self_tests_case_insensitive_name_normalization(self):
        task = next(t for t in load_tasks() if t["id"] == "SELF001")
        view = agent_view(task)
        raw = [{
            "id": "C_ci",
            "steps": [
                {"inputs": {"start": True, "stop": False, "guardclosed": True}, "expected": {"run": True}, "dt_ms": 0}
            ]
        }]
        cleaned = validate_self_tests(view, raw)
        self.assertEqual(len(cleaned), 1)
        step = cleaned[0]["steps"][0]
        # Verify keys are normalized to declared casing
        self.assertIn("Start", step["inputs"])
        self.assertIn("Stop", step["inputs"])
        self.assertIn("GuardClosed", step["inputs"])
        self.assertIn("Run", step["expected"])
