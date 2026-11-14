from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from plc_agent.backend import FakeBackend, SimCaseFailure, SimResult
from plc_agent.common import ROOT, digest, read_json
from plc_agent.compiler import compile_st, normalize_candidate, verify_interface_signature
from plc_agent.config import Settings
from plc_agent.dataset import load_tasks
from plc_agent.dialect_cards import (
    DIALECT_CARDS,
    STATIC_ANALYSIS_LIGHT_CARD,
    select_static_analysis_hint,
)
from plc_agent.formal_verify import verify_candidate
from plc_agent.harness import compact_diagnostics, run_harness
from plc_agent.llm import ProviderError, ResponsesClient
from plc_agent.mcp_server import dispatch
from plc_agent.metrics import aggregate
from plc_agent.model_checker import LTL_RESULTS_MARKER, SBMC_START_MARKER, parse_results
from plc_agent.simulation import run_functional
from plc_agent.st_verifier import (
    UnsupportedSTConstructError,
    _is_valid_standalone_smv_expr,
    _translate_st_ltl_to_smv,
    compile_st_to_smv,
    find_nusmv,
    find_nuxmv,
    sanitize_counterexamples_for_agent,
    verify_candidate_st,
)
from plc_agent.task_view import agent_view
from plc_agent.webui import handle_api_request


class STVerifierTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        self.work_dir = Path(self.tmp_dir.name)
        self.tasks = {t["id"]: t for t in load_tasks()}

    def _require_checkers(self):
        if not (find_nusmv() or find_nuxmv()):
            self.skipTest("Neither NuSMV nor nuXmv is available locally")

    def test_pub002_input_alias_and_unmapped_input_rejection(self):
        candidate = {
            "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT value : DWORD; END_VAR\n"
                "VAR_OUTPUT hasChanged : BOOL; hasRisingEdges : BOOL; risingBits : DWORD; "
                "noOfRisingBits : USINT; hasFallingEdges : BOOL; fallingBits : DWORD; "
                "noOfFallingBits : USINT; END_VAR\nVAR prev : DWORD := DWORD#0; END_VAR",
            "implementation": "risingBits := value AND NOT prev; fallingBits := prev AND NOT value; "
                "hasChanged := value <> prev; hasRisingEdges := risingBits <> DWORD#0; "
                "hasFallingEdges := fallingBits <> DWORD#0; noOfRisingBits := 0; "
                "noOfFallingBits := 0; prev := value;",
        }
        smv = compile_st_to_smv(candidate, self.tasks["PUB002"])["smv_text"]
        self.assertNotIn("cand_in_value", smv)
        self.assertIn("cand_post_prev := val;", smv)
        other = read_json(ROOT / "codesys/examples/SELF001.json")
        other["declaration"] += "\nVAR_INPUT extra : BOOL; END_VAR\n"
        with self.assertRaisesRegex(UnsupportedSTConstructError, "no observer binding"):
            compile_st_to_smv(other, self.tasks["SELF001"])

    def test_verify_candidate_st_passes_reference_and_pilot_examples(self):
        self._require_checkers()
        for tid in ("SELF001", "SELF005", "PUB006", "PUB007"):
            cand = read_json(ROOT / f"codesys/examples/{tid}.json")
            res = verify_candidate_st(
                self.tasks[tid],
                cand,
                self.work_dir / f"pass_{tid}",
                timeout=30,
            )
            self.assertEqual(res["status"], "PASS", f"{tid} verify failed: {res}")
            self.assertTrue(res["verified"])
            self.assertTrue(res["candidate_st_verified"])
            self.assertGreater(res["total_properties"], 0)
            self.assertEqual(res["passed_properties"], res["total_properties"])
            self.assertEqual(res["failed_properties"], 0)
            self.assertEqual(res["property_pass_ratio"], 1.0)

        pilot_cand = ROOT / "results/raw/pilot_pair_2026-11-10T143217961073+0000/PUB001_star/final_candidate.json"
        if pilot_cand.is_file():
            res = verify_candidate_st(
                self.tasks["PUB001"],
                read_json(pilot_cand),
                self.work_dir / "pass_PUB001_pilot",
                timeout=30,
            )
            self.assertEqual(res["status"], "PASS", f"PUB001 pilot failed: {res}")
            self.assertEqual(res["property_pass_ratio"], 1.0)

    def test_counterexample_waveform_sanitization_and_initial_instance(self):
        self._require_checkers()

        # 1. SELF001 safety violation (Stop / GuardClosed ignored)
        bug_self001 = read_json(ROOT / "codesys/examples/SELF001.json")
        bug_self001["implementation"] = "IF Start THEN\n    Run := TRUE;\nEND_IF;\n"
        res_self = verify_candidate_st(
            self.tasks["SELF001"],
            bug_self001,
            self.work_dir / "cex_self001",
            timeout=30,
            include_expected_observer=True,
        )
        self.assertEqual(res_self["status"], "COUNTEREXAMPLE")
        self.assertFalse(res_self["verified"])
        self.assertGreaterEqual(res_self["failed_properties"], 1)
        self.assertIsNotNone(res_self["property_pass_ratio"])
        self.assertLess(res_self["property_pass_ratio"], 1.0)
        self.assertTrue(res_self["counterexamples"])

        wf = res_self["waveform"]
        self.assertIsNotNone(wf)
        self.assertIn("signals", wf)
        self.assertIn("steps", wf)
        self.assertGreater(len(wf["steps"]), 0)

        sanitized = sanitize_counterexamples_for_agent(res_self["counterexamples"])
        self.assertEqual(len(sanitized), len(res_self["counterexamples"]))
        for ce in sanitized:
            self.assertEqual(set(ce.keys()), {"property", "loop_start_step", "trace"})
            for step in ce["trace"]:
                self.assertEqual(set(step.keys()), {"step", "inputs", "observed"})
                self.assertNotIn("observer_vars", step)
                self.assertNotIn("internal_state", step)

        res_no_leak = verify_candidate_st(
            self.tasks["SELF001"],
            bug_self001,
            self.work_dir / "cex_self001_noleak",
            timeout=30,
            include_expected_observer=False,
        )
        for ce in res_no_leak["counterexamples"]:
            for step in ce["trace"]:
                self.assertNotIn("observer_vars", step)

        # 2. PUB006 wrong TON preset (T#5S -> T#2S)
        bug_pub006 = read_json(ROOT / "codesys/examples/PUB006.json")
        bug_pub006["implementation"] = bug_pub006["implementation"].replace("T#5S", "T#2S")
        res_pub6 = verify_candidate_st(
            self.tasks["PUB006"],
            bug_pub006,
            self.work_dir / "cex_pub006",
            timeout=30,
        )
        self.assertEqual(res_pub6["status"], "COUNTEREXAMPLE")
        self.assertFalse(res_pub6["verified"])
        self.assertGreaterEqual(res_pub6["failed_properties"], 1)

        # 3. SELF005 INITIAL_INSTANCE failure (Red := FALSE instead of TRUE)
        bug_init = read_json(ROOT / "codesys/examples/SELF005.json")
        bug_init["declaration"] = bug_init["declaration"].replace("Red : BOOL := TRUE;", "Red : BOOL := FALSE;")
        res_init = verify_candidate_st(
            self.tasks["SELF005"],
            bug_init,
            self.work_dir / "cex_self005_init",
            timeout=30,
        )
        self.assertEqual(res_init["status"], "COUNTEREXAMPLE")
        self.assertFalse(res_init["verified"])
        self.assertTrue(res_init["initial_instance_failures"])

    def test_verify_candidate_st_unsupported_construct_pub018(self):
        cand = read_json(ROOT / "codesys/examples/PUB018.json")
        res = verify_candidate_st(
            self.tasks["PUB018"],
            cand,
            self.work_dir / "unsupported_pub018",
            timeout=30,
        )
        self.assertEqual(res["status"], "UNSUPPORTED_ST")
        self.assertFalse(res["verified"])
        self.assertIsNone(res["property_pass_ratio"])

    def test_formal_verify_candidate_writes_manifest(self):
        self._require_checkers()
        out_dir = self.work_dir / "fv_self001"
        cand = read_json(ROOT / "codesys/examples/SELF001.json")
        res = verify_candidate(self.tasks["SELF001"], cand, out_dir, timeout=30)
        self.assertEqual(res["status"], "PASS")
        self.assertTrue(res["verified"])
        manifest = read_json(out_dir / "verification_manifest.json")
        self.assertTrue(manifest["encoding_complete"])
        self.assertTrue(manifest["candidate_st_verified"])
        self.assertEqual(manifest["verification_status"], "PASS")
        self.assertEqual(manifest["bundle_status"], "PASS")

    def test_mcp_server_verify_st_and_budget_enforcement(self):
        self._require_checkers()
        mcp_ws = self.work_dir / "mcp_ws"
        settings = Settings(max_verifications=1)
        listed = dispatch({"method": "tools/list"}, self.tasks["SELF001"], mcp_ws, settings)
        tool_names = [t["name"] for t in listed["tools"]]
        self.assertIn("verify_st", tool_names)

        bug_self001 = read_json(ROOT / "codesys/examples/SELF001.json")
        bug_self001["implementation"] = "IF Start THEN\n    Run := TRUE;\nEND_IF;\n"
        call1 = dispatch(
            {"method": "tools/call", "params": {"name": "verify_st", "arguments": {"source": bug_self001}}},
            self.tasks["SELF001"],
            mcp_ws,
            settings,
        )
        self.assertFalse(call1["isError"])
        payload = json.loads(call1["content"][0]["text"])
        self.assertEqual(payload["status"], "COUNTEREXAMPLE")
        self.assertTrue(payload["counterexamples"])
        for ce in payload["counterexamples"]:
            for step in ce["trace"]:
                self.assertEqual(set(step.keys()), {"step", "inputs", "observed"})

        call2 = dispatch(
            {"method": "tools/call", "params": {"name": "verify_st", "arguments": {"source": bug_self001}}},
            self.tasks["SELF001"],
            mcp_ws,
            settings,
        )
        self.assertTrue(call2["isError"])
        self.assertIn("Formal verification budget exhausted", call2["content"][0]["text"])

    def test_harness_cegar_static_analysis_unlimited_calls_and_provider_error_preservation(self):
        self._require_checkers()

        # 1. SA0027 / SA0033 hints + select_static_analysis_hint without expanding 8-card DIALECT_CARDS
        self.assertEqual(len(DIALECT_CARDS), 8)
        hint_diag = compact_diagnostics(
            {"declaration": "", "implementation": ""},
            [
                {"severity": "Warning", "text": "SA0027: Identifier 'error' collides with keyword"},
                {"severity": "Warning", "text": "SA0033: Unused variable 'tmp'"},
            ],
        )
        self.assertIn("[Hint SA0027]:", hint_diag)
        self.assertIn("[Hint SA0033]:", hint_diag)
        hint_card = select_static_analysis_hint(agent_view(self.tasks["PUB003"]))
        self.assertIsNotNone(hint_card)
        self.assertEqual(hint_card["id"], STATIC_ANALYSIS_LIGHT_CARD["id"])
        self.assertIsNone(select_static_analysis_hint(agent_view(self.tasks["SELF001"])))

        # 2. Unlimited max_llm_calls=0 & max_total_tokens=0 in ResponsesClient
        unlimited_client = ResponsesClient(
            Settings(api_key="k", base_url="https://relay.invalid/v1", max_llm_calls=0, max_total_tokens=0)
        )
        mock_resp = MagicMock(status_code=200, headers={"Content-Type": "application/json"})
        mock_resp.json.return_value = {
            "status": "completed",
            "model": "unit",
            "output": [{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "OK"}]}],
            "usage": {"total_tokens": 500000},
        }
        unlimited_client.session.post = MagicMock()
        unlimited_client.session.post.return_value.__enter__.return_value = mock_resp
        for i in range(5):
            out = unlimited_client.respond("unit", [{"role": "user", "content": "hi"}], self.work_dir / f"ul_{i}")
            self.assertEqual(out["text"], "OK")
        self.assertEqual(unlimited_client.request_count, 5)

        # 3. Step 3.5 CEGAR fixes buggy SELF001 candidate -> PASS with zero leakage in CEGAR prompt
        ref_self001 = read_json(ROOT / "codesys/examples/SELF001.json")
        bug_self001 = dict(ref_self001)
        bug_self001["implementation"] = "IF Start THEN\n    Run := TRUE;\nEND_IF;\n"

        class CegarMockClient:
            def __init__(self):
                self.prompts: dict[str, list[dict]] = {}

            def respond(self, model, messages, log_dir, **kwargs):
                stage = Path(log_dir).name
                self.prompts[stage] = messages
                if stage == "llm_planner":
                    return {"text": '{"summary": "safety latch"}'}
                if stage == "llm_code_00":
                    return {"text": json.dumps(bug_self001)}
                if stage.startswith("llm_cegar"):
                    return {"text": json.dumps(ref_self001)}
                if stage == "llm_tester":
                    return {"text": "[]"}
                raise AssertionError(f"Unexpected LLM stage: {stage}")

        cegar_client = CegarMockClient()
        res_cegar = run_harness(
            self.tasks["SELF001"],
            "unit-model",
            self.work_dir / "cegar_run",
            cegar_client,
            Settings(max_verifications=2, max_llm_calls=0, max_total_tokens=0),
            condition="E3",
            backend=FakeBackend(),
        )
        self.assertTrue(res_cegar["final_compiled"])
        self.assertEqual(res_cegar["verification"]["status"], "PASS")
        self.assertEqual(res_cegar["cegar_repairs"], 1)
        self.assertEqual(res_cegar["verification_call_count"], 2)
        self.assertIn("Stop", res_cegar["final_candidate"]["implementation"])

        cegar_prompt_text = json.dumps(cegar_client.prompts["llm_cegar_00"])
        self.assertNotIn("observer_vars", cegar_prompt_text)
        self.assertNotIn("internal_state", cegar_prompt_text)
        self.assertNotIn('"expected"', cegar_prompt_text)
        self.assertIn("COUNTEREXAMPLE", cegar_prompt_text)

        # 4. Post-compile ProviderError preserves compiled best_candidate
        class FailingTesterClient:
            def respond(self, model, messages, log_dir, **kwargs):
                stage = Path(log_dir).name
                if stage == "llm_planner":
                    return {"text": '{"summary": "safety latch"}'}
                if stage == "llm_code_00":
                    return {"text": json.dumps(ref_self001)}
                if stage == "llm_tester":
                    raise ProviderError("Simulated provider outage during tester")
                raise AssertionError(f"Unexpected LLM stage: {stage}")

        res_err = run_harness(
            self.tasks["SELF001"],
            "unit-model",
            self.work_dir / "provider_err_run",
            FailingTesterClient(),
            Settings(max_verifications=1),
            condition="E3",
            backend=FakeBackend(),
        )
        self.assertTrue(res_err["final_compiled"])
        self.assertIsNotNone(res_err["final_candidate"])
        self.assertEqual(res_err["final_candidate"]["declaration"], ref_self001["declaration"])
        self.assertEqual(res_err["status"], "UNVERIFIED")
        self.assertIn("preserved best_candidate", res_err["reason"])

    def test_metrics_aggregate_verification_fields(self):
        records = [
            {
                "condition": "E3",
                "task_id": "SELF001",
                "framework": "self_harness",
                "model": "unit",
                "status": "PASS",
                "first_pass_compiled": True,
                "final_compiled": True,
                "repair_attempts": 0,
                "compilation_attempts": [{"status": "PASS", "success": True}],
                "functional": {"status": "PASS", "planned_cases": 1, "evaluated_cases": 1, "passed_cases": 1},
                "verification": {"status": "PASS", "verified": True, "property_pass_ratio": 1.0},
                "usage": [],
                "elapsed_seconds": 1.0,
            },
            {
                "condition": "E3",
                "task_id": "SELF002",
                "framework": "self_harness",
                "model": "unit",
                "status": "TEST_FAIL",
                "first_pass_compiled": True,
                "final_compiled": True,
                "repair_attempts": 0,
                "compilation_attempts": [{"status": "PASS", "success": True}],
                "functional": {"status": "TEST_FAIL", "planned_cases": 1, "evaluated_cases": 1, "passed_cases": 0},
                "verification": {"status": "COUNTEREXAMPLE", "verified": False, "property_pass_ratio": 0.5},
                "usage": [],
                "elapsed_seconds": 1.0,
            },
            {
                "condition": "E3",
                "task_id": "PUB018",
                "framework": "self_harness",
                "model": "unit",
                "status": "UNVERIFIED",
                "first_pass_compiled": True,
                "final_compiled": True,
                "repair_attempts": 0,
                "compilation_attempts": [{"status": "PASS", "success": True}],
                "functional": {"status": "UNVERIFIED", "planned_cases": 1, "evaluated_cases": 0, "passed_cases": 0},
                "verification": {"status": "UNSUPPORTED_ST", "verified": False, "property_pass_ratio": None},
                "usage": [],
                "elapsed_seconds": 1.0,
            },
        ]
        summary = aggregate(records, 3, conditions=["E3"])
        self.assertEqual(len(summary), 1)
        row = summary[0]
        self.assertEqual(row["verification_evaluated_tasks"], 2)
        self.assertAlmostEqual(row["verification_pass_rate_among_evaluated"], 0.5)
        self.assertAlmostEqual(row["mean_property_pass_ratio"], 0.75)

    def test_webui_verify_candidate_endpoint(self):
        self._require_checkers()
        ref_self001 = read_json(ROOT / "codesys/examples/SELF001.json")
        st_pass, data_pass = handle_api_request(
            "POST",
            "/api/verify-candidate",
            {},
            {"task_id": "SELF001", "candidate": ref_self001, "out_dir": str(self.work_dir / "web_pass")},
            Settings(),
        )
        self.assertEqual(st_pass, 200)
        self.assertEqual(data_pass["status"], "PASS")
        self.assertTrue(data_pass["verified"])
        self.assertIn("smv_text", data_pass)
        self.assertTrue(len(data_pass["smv_text"]) > 0)

        bug_self001 = dict(ref_self001)
        bug_self001["implementation"] = "IF Start THEN\n    Run := TRUE;\nEND_IF;\n"
        st_cex, data_cex = handle_api_request(
            "POST",
            "/api/verify-candidate",
            {},
            {"task_id": "SELF001", "candidate": bug_self001, "out_dir": str(self.work_dir / "web_cex")},
            Settings(),
        )
        self.assertEqual(st_cex, 200)
        self.assertEqual(data_cex["status"], "COUNTEREXAMPLE")
        self.assertFalse(data_cex["verified"])
        self.assertIsNotNone(data_cex["waveform"])
        self.assertGreater(len(data_cex["waveform"]["steps"]), 0)

    def test_uncertainty_outcomes_inconclusive_sbmc_preservation_and_metrics(self):
        # 1. parse_results: standalone `is unknown` -> INCONCLUSIVE (never conflated with PASS/FAIL)
        res_unk = parse_results(
            stdout=f"{LTL_RESULTS_MARKER}\n-- LTL specification G (Start -> Run)  is unknown\n",
            stderr="",
            returncode=0,
            expected_count=1,
        )
        self.assertEqual(res_unk["status"], "INCONCLUSIVE")
        self.assertEqual(res_unk["unknown_properties"], 1)
        self.assertEqual(res_unk["property_results"][0]["holds"], None)
        self.assertEqual(res_unk["property_results"][0]["status"], "UNKNOWN")

        # 2. parse_results: SBMC falsification preserved when later IC3 prints `is unknown`
        res_sbmc_cex = parse_results(
            stdout=(
                f"{SBMC_START_MARKER}\n"
                "-- LTL specification G (Start -> Run)  is false\n"
                f"{LTL_RESULTS_MARKER}\n"
                "-- LTL specification G (Start -> Run)  is unknown\n"
            ),
            stderr="",
            returncode=0,
            expected_count=1,
        )
        self.assertEqual(res_sbmc_cex["status"], "COUNTEREXAMPLE")
        self.assertEqual(res_sbmc_cex["unknown_properties"], 0)
        self.assertIs(res_sbmc_cex["property_results"][0]["holds"], False)
        self.assertEqual(res_sbmc_cex["property_results"][0]["status"], "FAIL")

        # 3. parse_results: type/range errors surface as TOOL_ERROR
        res_range_err = parse_results(
            stdout="",
            stderr="file model.smv: line 12: cannot assign value 300 to type -128..255\n",
            returncode=1,
            expected_count=1,
        )
        self.assertEqual(res_range_err["status"], "TOOL_ERROR")

        # 4. verify_candidate_st + mcp_server.dispatch propagate INCONCLUSIVE honestly
        ref_self001 = read_json(ROOT / "codesys/examples/SELF001.json")
        fake_inconclusive = {
            "status": "INCONCLUSIVE",
            "expected_properties": 1,
            "checked_properties": 1,
            "unknown_properties": 1,
            "property_results": [{"expression": "P1", "holds": None, "status": "UNKNOWN"}],
            "tool": "nuXmv",
            "engine": "smt",
            "model_sha256": None,
            "tool_exe_sha256": None,
            "stdout_path": None,
            "stderr_path": None,
        }
        with patch("plc_agent.st_verifier.check_model", return_value=fake_inconclusive):
            ver_inc = verify_candidate_st(
                self.tasks["SELF001"],
                ref_self001,
                self.work_dir / "inconclusive_run",
                timeout=10,
            )
        self.assertEqual(ver_inc["status"], "INCONCLUSIVE")
        self.assertFalse(ver_inc["verified"])
        self.assertEqual(ver_inc["unknown_properties"], 1)
        self.assertEqual(ver_inc["failed_properties"], 0)
        self.assertIsNone(ver_inc["property_pass_ratio"])
        self.assertIn("UNKNOWN", ver_inc["reason"])

        with patch("plc_agent.st_verifier.check_model", return_value=fake_inconclusive):
            mcp_inc = dispatch(
                {"method": "tools/call", "params": {"name": "verify_st", "arguments": {"source": ref_self001}}},
                self.tasks["SELF001"],
                self.work_dir / "mcp_inc",
                Settings(max_verifications=2),
            )
        self.assertFalse(mcp_inc["isError"])
        inc_payload = json.loads(mcp_inc["content"][0]["text"])
        self.assertEqual(inc_payload["status"], "INCONCLUSIVE")
        self.assertEqual(inc_payload["unknown_properties"], 1)
        self.assertEqual(inc_payload["failed_property_ids"], [])
        self.assertTrue(inc_payload["unknown_property_ids"])
        self.assertTrue(inc_payload.get("guidance"))

        # 5. metrics.aggregate distinguishes INCONCLUSIVE and UNSUPPORTED_ST from evaluated tasks
        records = [
            {
                "condition": "E3",
                "task_id": "SELF001",
                "framework": "self_harness",
                "model": "unit",
                "status": "PASS",
                "first_pass_compiled": True,
                "final_compiled": True,
                "repair_attempts": 0,
                "compilation_attempts": [{"status": "PASS", "success": True}],
                "functional": {"status": "PASS", "planned_cases": 1, "evaluated_cases": 1, "passed_cases": 1},
                "verification": {
                    "status": "PASS",
                    "verified": True,
                    "property_pass_ratio": 1.0,
                    "unknown_properties": 0,
                },
                "usage": [],
                "elapsed_seconds": 1.0,
            },
            {
                "condition": "E3",
                "task_id": "SELF002",
                "framework": "self_harness",
                "model": "unit",
                "status": "UNVERIFIED",
                "first_pass_compiled": True,
                "final_compiled": True,
                "repair_attempts": 0,
                "compilation_attempts": [{"status": "PASS", "success": True}],
                "functional": {"status": "UNVERIFIED", "planned_cases": 1, "evaluated_cases": 0, "passed_cases": 0},
                "verification": {
                    "status": "INCONCLUSIVE",
                    "verified": False,
                    "property_pass_ratio": None,
                    "unknown_properties": 2,
                },
                "usage": [],
                "elapsed_seconds": 1.0,
            },
            {
                "condition": "E3",
                "task_id": "PUB018",
                "framework": "self_harness",
                "model": "unit",
                "status": "UNVERIFIED",
                "first_pass_compiled": True,
                "final_compiled": True,
                "repair_attempts": 0,
                "compilation_attempts": [{"status": "PASS", "success": True}],
                "functional": {"status": "UNVERIFIED", "planned_cases": 1, "evaluated_cases": 0, "passed_cases": 0},
                "verification": {
                    "status": "UNSUPPORTED_ST",
                    "verified": False,
                    "property_pass_ratio": None,
                    "unknown_properties": 0,
                },
                "usage": [],
                "elapsed_seconds": 1.0,
            },
        ]
        summary = aggregate(records, 3, conditions=["E3"])
        row = summary[0]
        self.assertEqual(row["verification_evaluated_tasks"], 1)
        self.assertEqual(row["verification_inconclusive_tasks"], 1)
        self.assertEqual(row["verification_unsupported_tasks"], 1)
        self.assertAlmostEqual(row["verification_pass_rate_among_evaluated"], 1.0)
        self.assertAlmostEqual(row["mean_property_pass_ratio"], 1.0)

    def test_boundary_rejections_frozen_fbs_and_smt_routing(self):
        # 1. Conditional TON inside IF -> UnsupportedSTConstructError + UNSUPPORTED_ST + MCP guidance
        cond_fb_cand = read_json(ROOT / "codesys/examples/PUB006.json")
        cond_fb_cand["implementation"] = (
            "IF DO_LOW AND AERATION_E_STOP_NC THEN\n"
            "    timer(IN := TRUE, PT := T#5S);\n"
            "END_IF;\n"
            "BLOWER_RUN := timer.Q;\n"
        )
        with self.assertRaises(UnsupportedSTConstructError):
            compile_st_to_smv(cond_fb_cand, self.tasks["PUB006"])
        ver_cond = verify_candidate_st(self.tasks["PUB006"], cond_fb_cand, self.work_dir / "cond_fb", timeout=10)
        self.assertEqual(ver_cond["status"], "UNSUPPORTED_ST")
        self.assertFalse(ver_cond["verified"])
        self.assertIn("conditional", ver_cond["reason"].lower())

        mcp_unsup = dispatch(
            {"method": "tools/call", "params": {"name": "verify_st", "arguments": {"source": cond_fb_cand}}},
            self.tasks["PUB006"],
            self.work_dir / "mcp_unsup",
            Settings(max_verifications=2),
        )
        self.assertFalse(mcp_unsup["isError"])
        unsup_payload = json.loads(mcp_unsup["content"][0]["text"])
        self.assertEqual(unsup_payload["status"], "UNSUPPORTED_ST")
        self.assertTrue(unsup_payload.get("guidance"))

        # 2. Static array out-of-bounds access -> UnsupportedSTConstructError + UNSUPPORTED_ST
        ref_self001 = read_json(ROOT / "codesys/examples/SELF001.json")
        oob_cand = {
            "declaration": ref_self001["declaration"] + "VAR\n    arr : ARRAY[1..3] OF INT;\nEND_VAR\n",
            "implementation": ref_self001["implementation"] + "arr[99] := 1;\n",
        }
        with self.assertRaises(UnsupportedSTConstructError):
            compile_st_to_smv(oob_cand, self.tasks["SELF001"])
        ver_oob = verify_candidate_st(self.tasks["SELF001"], oob_cand, self.work_dir / "oob_arr", timeout=10)
        self.assertEqual(ver_oob["status"], "UNSUPPORTED_ST")

        # 3. Division and MOD by constant zero -> UnsupportedSTConstructError + UNSUPPORTED_ST
        for op in ("/", "MOD"):
            div0_cand = {
                "declaration": ref_self001["declaration"] + "VAR\n    x : INT := 5;\n    y : INT := 0;\nEND_VAR\n",
                "implementation": ref_self001["implementation"] + f"y := x {op} 0;\n",
            }
            with self.assertRaises(UnsupportedSTConstructError):
                compile_st_to_smv(div0_cand, self.tasks["SELF001"])
            ver_div0 = verify_candidate_st(self.tasks["SELF001"], div0_cand, self.work_dir / f"div0_{op}", timeout=10)
            self.assertEqual(ver_div0["status"], "UNSUPPORTED_ST")

        # 4. Uncalled stateful FB keeps frozen state (`next(sv) := sv`) and still passes BDD verification
        uncalled_fb_cand = {
            "declaration": ref_self001["declaration"] + "VAR\n    r_unused : R_TRIG;\nEND_VAR\n",
            "implementation": ref_self001["implementation"],
        }
        compiled_fb = compile_st_to_smv(uncalled_fb_cand, self.tasks["SELF001"])
        self.assertIn("next(cand_fb_r_unused_m) := cand_fb_r_unused_m;", compiled_fb["smv_text"])
        if find_nusmv() or find_nuxmv():
            ver_fb = verify_candidate_st(
                self.tasks["SELF001"], uncalled_fb_cand, self.work_dir / "frozen_fb", timeout=20
            )
            self.assertEqual(ver_fb["status"], "PASS")

        # 5. Unbounded integer arithmetic / literals > 255 auto-route SELF001 candidate to nuXmv SMT (: integer)
        arith_int_cand = {
            "declaration": ref_self001["declaration"] + "VAR\n    cnt : INT := 0;\nEND_VAR\n",
            "implementation": ref_self001["implementation"] + "cnt := cnt + 1;\n",
        }
        compiled_arith = compile_st_to_smv(arith_int_cand, self.tasks["SELF001"])
        self.assertTrue(compiled_arith["uses_smt"])
        self.assertIn("cand_state_cnt : integer;", compiled_arith["smv_text"])

        big_lit_cand = {
            "declaration": ref_self001["declaration"] + "VAR\n    big : INT := 300;\nEND_VAR\n",
            "implementation": ref_self001["implementation"],
        }
        compiled_big = compile_st_to_smv(big_lit_cand, self.tasks["SELF001"])
        self.assertTrue(compiled_big["uses_smt"])
        self.assertIn("cand_state_big : integer;", compiled_big["smv_text"])

    def test_scheme_a_standalone_verification_and_zero_complete_behavior_leak(self):
        # 1. agent_view strips CompleteBehavior and .COMPLETE from spec_visible view
        self001_full = self.tasks["SELF001"]
        self.assertIn("CompleteBehavior", self001_full.get("atomic_propositions", {}))
        self.assertTrue(any(str(p.get("id", "")).endswith(".COMPLETE") for p in self001_full.get("ltl", [])))

        view = agent_view(self001_full, spec_visible=True)
        self.assertNotIn("CompleteBehavior", view.get("atomic_propositions", {}))
        self.assertFalse(any(str(p.get("id", "")).endswith(".COMPLETE") for p in view.get("ltl", [])))
        self.assertGreaterEqual(len(view.get("ltl", [])), 5)

        # 2. Standalone compilation never reads models/*.smv (observer_smv is None)
        ref_self001 = read_json(ROOT / "codesys/examples/SELF001.json")
        with patch(
            "plc_agent.st_verifier.discover_observer_smv", side_effect=AssertionError("must not read observer smv")
        ):
            standalone_compiled = compile_st_to_smv(ref_self001, view, use_observer_smv=False)
        self.assertIsNone(standalone_compiled["observer_smv"])
        self.assertEqual(standalone_compiled["expected_spec_count"], 5)

        # 3. Full standalone verification works against real NuSMV/nuXmv
        self._require_checkers()
        with patch(
            "plc_agent.st_verifier.discover_observer_smv", side_effect=AssertionError("must not read observer smv")
        ):
            ver_pass = verify_candidate(
                task=view,
                candidate=ref_self001,
                out_dir=self.work_dir / "standalone_pass",
                include_expected_observer=False,
                use_observer_smv=False,
                extra_assertions=[{"id": "A_extra", "formula": "G (Stop -> !Run)"}],
            )
        self.assertEqual(ver_pass["status"], "PASS")
        self.assertTrue(ver_pass["standalone_mode"])
        self.assertIsNone(ver_pass["observer_smv"])
        self.assertEqual(ver_pass["passed_properties"], 6)

        bug_self001 = dict(ref_self001)
        bug_self001["implementation"] = "IF Start THEN\n    Run := TRUE;\nEND_IF;\n"
        ver_fail = verify_candidate(
            task=view,
            candidate=bug_self001,
            out_dir=self.work_dir / "standalone_fail",
            include_expected_observer=False,
            use_observer_smv=False,
        )
        self.assertEqual(ver_fail["status"], "COUNTEREXAMPLE")
        self.assertFalse(ver_fail["verified"])
        self.assertIsNone(ver_fail["observer_smv"])
        san = sanitize_counterexamples_for_agent(ver_fail["counterexamples"])
        self.assertTrue(san)

    def test_whitebox_internal_state_preserved_in_sanitized_counterexamples(self):
        self._require_checkers()
        view = agent_view(self.tasks["SELF001"], spec_visible=True)
        cand_with_internal_var = {
            "declaration": (
                "FUNCTION_BLOCK FB_Task\n"
                "VAR_INPUT\n    Start : BOOL;\n    Stop : BOOL;\n    GuardClosed : BOOL;\nEND_VAR\n"
                "VAR_OUTPUT\n    Run : BOOL := FALSE;\nEND_VAR\n"
                "VAR\n    state : INT := 0;\nEND_VAR\n"
            ),
            "implementation": ("IF Start THEN\n    state := 1;\nEND_IF;\nRun := (state = 1);\n"),
            "supporting_objects": [],
        }
        ver = verify_candidate_st(
            view,
            cand_with_internal_var,
            self.work_dir / "whitebox_state",
            timeout=20,
            include_expected_observer=False,
            use_observer_smv=False,
        )
        self.assertEqual(ver["status"], "COUNTEREXAMPLE")
        san = sanitize_counterexamples_for_agent(ver["counterexamples"])
        self.assertTrue(san)
        has_internal = any(
            isinstance(step.get("internal_state"), dict) and "cand_state_state" in step["internal_state"]
            for ce in san
            for step in ce.get("trace", [])
        )
        self.assertTrue(has_internal)
        for ce in san:
            for step in ce["trace"]:
                self.assertNotIn("observer_vars", step)

    def test_interface_signature_hard_lock_and_fake_backend_enforcement(self):
        task = self.tasks["SELF001"]
        # Wrong output type (DINT instead of BOOL)
        bad_type = {
            "declaration": (
                "FUNCTION_BLOCK FB_Task\n"
                "VAR_INPUT\n    Start, Stop, GuardClosed : BOOL;\nEND_VAR\n"
                "VAR_OUTPUT\n    Run : DINT := 0;\nEND_VAR\n"
            ),
            "implementation": "Run := 0;",
            "supporting_objects": [],
        }
        diags = verify_interface_signature(bad_type, task["interface"])
        self.assertTrue(diags)
        self.assertIn("INTERFACE_VIOLATION", diags[0]["text"])

        backend = FakeBackend()
        comp_res = backend.compile(task, bad_type, self.work_dir / "iface_bad_type")
        self.assertEqual(comp_res.status, "COMPILE_FAIL")
        self.assertFalse(comp_res.success)

        # Wrong direction + extra unexpected variable
        bad_dir = {
            "declaration": (
                "FUNCTION_BLOCK FB_Task\n"
                "VAR_INPUT\n    Start, Stop, GuardClosed, Run : BOOL;\n    ExtraPort : INT;\nEND_VAR\n"
            ),
            "implementation": "",
            "supporting_objects": [],
        }
        diags_dir = verify_interface_signature(bad_dir, task["interface"])
        texts = "\n".join(d["text"] for d in diags_dir)
        self.assertIn("expected in VAR_OUTPUT", texts)
        self.assertIn("ExtraPort", texts)

        # Synthetic minimal placeholder remains compatible
        stub = {"declaration": "FUNCTION_BLOCK FB_Task", "implementation": "", "supporting_objects": []}
        self.assertEqual(verify_interface_signature(stub, task["interface"]), [])

    def test_step5_4d_ratchet_blocks_lazy_reject_cases_without_code_edit(self):
        task = self.tasks["SELF001"]
        cand_same = read_json(ROOT / "codesys/examples/SELF001.json")
        plan_json = json.dumps({"state_machine": ["IDLE", "RUN"], "scan_execution_order": ["1", "2", "3", "4"]})
        cases_json = json.dumps(
            [
                {
                    "id": "c1",
                    "steps": [
                        {"inputs": {"Start": True, "Stop": False, "GuardClosed": True}, "expected": {"Run": True}}
                    ],
                },
                {
                    "id": "c2",
                    "steps": [
                        {"inputs": {"Start": True, "Stop": False, "GuardClosed": True}, "expected": {"Run": True}}
                    ],
                },
                {
                    "id": "c3",
                    "steps": [
                        {"inputs": {"Start": True, "Stop": False, "GuardClosed": True}, "expected": {"Run": True}}
                    ],
                },
                {
                    "id": "c4",
                    "steps": [
                        {"inputs": {"Start": True, "Stop": False, "GuardClosed": True}, "expected": {"Run": True}}
                    ],
                },
            ]
        )
        # Lazy LLM returns identical candidate ST code + tries to cheat PASS by rejecting failing c2, c3
        lazy_repair = dict(cand_same)
        lazy_repair["reject_cases"] = [
            {"id": "c2", "reason": "lazy"},
            {"id": "c3", "reason": "lazy"},
        ]

        class _SeqClient:
            def __init__(self, responses):
                self._responses = list(responses)
                self.prompts = {}

            def respond(self, model, messages, log_dir, max_tokens=None, timeout=None):
                Path(log_dir).mkdir(parents=True, exist_ok=True)
                self.prompts[Path(log_dir).name] = messages
                text = self._responses.pop(0)
                return {"text": text, "usage": {"input_tokens": 10, "output_tokens": 10}}

        client = _SeqClient(
            [
                plan_json,
                json.dumps(cand_same),
                cases_json,
                json.dumps(lazy_repair),
            ]
        )

        def _mock_simulate(t, candidate, cases, ws):
            passed = 0
            failures = []
            for c in cases:
                if c["id"] in ("c1", "c4"):
                    passed += 1
                else:
                    failures.append(
                        SimCaseFailure(
                            case_id=c["id"],
                            first_bad_step=0,
                            field="Run",
                            expected=True,
                            observed=False,
                            inputs_prefix=[c["steps"][0]["inputs"]],
                            step_window=[
                                {
                                    "step": 0,
                                    "dt_ms": 0,
                                    "inputs": c["steps"][0]["inputs"],
                                    "expected": {"Run": True},
                                    "observed": {"Run": False},
                                }
                            ],
                        )
                    )
            return SimResult(
                status="PASS" if passed == len(cases) else "TEST_FAIL",
                passed_cases=passed,
                evaluated_cases=len(cases),
                failures=failures,
            )

        backend = FakeBackend()
        backend.simulate = _mock_simulate
        settings = Settings(max_simulations=2, max_verifications=0, max_repairs=1)
        res = run_harness(task, "mock", self.work_dir / "anti_hack", client, settings, backend=backend)

        # Must block lazy PASS promotion even though c1 & c4 passed after rejecting c2 & c3
        self.assertEqual(res["status"], "TEST_FAIL")
        self.assertGreaterEqual(res["ratchet_rollbacks"], 1)
        # Check multi-turn assistant message formatting & explicit JSON schema hint in sim_repair
        sim_msgs = client.prompts["llm_sim_repair_01"]
        self.assertEqual([m["role"] for m in sim_msgs], ["developer", "user", "assistant", "user"])
        self.assertIn("step_window", sim_msgs[-1]["content"])
        self.assertIn("reject_cases", sim_msgs[-1]["content"])

        # Metrics aggregation carries forward rollback & rejection counts
        agg = aggregate([res], 1, conditions=[res["condition"]])
        self.assertGreaterEqual(agg[0]["total_ratchet_rollbacks"], 1)
        self.assertEqual(agg[0]["selftest_rejection_count"], 2)

    def test_mcp_simulate_st_precompile_quota_parity(self):
        task = self.tasks["SELF001"]
        trusted = self.work_dir / "mcp_precompile"
        trusted.mkdir(parents=True, exist_ok=True)
        settings = Settings(max_repairs=1, max_simulations=2)
        bad_iface_src = {
            "declaration": "FUNCTION_BLOCK FB_Task\nVAR_INPUT Start, Stop, GuardClosed : BOOL; END_VAR\nVAR_OUTPUT Run : DINT; END_VAR\n",
            "implementation": "Run := 0;",
            "supporting_objects": [],
        }
        cases = [
            {
                "id": "c1",
                "steps": [{"inputs": {"Start": True, "Stop": False, "GuardClosed": True}, "expected": {"Run": True}}],
            }
        ]
        resp = dispatch(
            {
                "method": "tools/call",
                "params": {"name": "simulate_st", "arguments": {"source": bad_iface_src, "cases": cases}},
            },
            task,
            trusted,
            settings,
            backend=FakeBackend(),
        )
        self.assertFalse(resp["isError"])
        payload = json.loads(resp["content"][0]["text"])
        self.assertEqual(payload["status"], "COMPILE_FAIL")
        self.assertFalse(payload["success"])
        self.assertTrue(any("INTERFACE_VIOLATION" in str(d.get("text", "")) for d in payload["diagnostics"]))
        # Must NOT consume any compile_st quota slots
        self.assertEqual(list(trusted.glob("compile_*")), [])

    def test_compiler_lock_timeout_budget_prevents_simulation_starvation(self):
        cfg = Settings()
        self.assertGreater(cfg.compiler_lock_timeout, cfg.compiler_timeout)
        self.assertGreaterEqual(cfg.compiler_lock_timeout, 900)

        fake_template = self.work_dir / "tpl.project"
        fake_template.write_text("tpl", encoding="utf-8")
        fake_exe = self.work_dir / "codesys.exe"
        fake_exe.write_text("exe", encoding="utf-8")
        cfg = Settings(
            codesys_exe=str(fake_exe),
            codesys_profile="P",
            codesys_template=str(fake_template),
            ascii_work_root=str(self.work_dir / "ascii"),
            compiler_timeout=180,
            compiler_lock_timeout=960,
        )

        lock_timeouts: list[float] = []

        class _FakeLock:
            def __init__(self, timeout: float = 0.0):
                lock_timeouts.append(float(timeout))

            def __enter__(self):
                return 0.0

            def __exit__(self, *args):
                return False

        class _FakeProc:
            def wait(self, timeout=None):
                return 0

        cand = read_json(ROOT / "codesys/examples/SELF001.json")
        with (
            patch("plc_agent.compiler.compiler_lock", side_effect=lambda t=180: _FakeLock(t)),
            patch("plc_agent.compiler.subprocess.Popen", return_value=_FakeProc()),
            patch("plc_agent.compiler.codesys_command", side_effect=lambda cmd: cmd),
            patch("plc_agent.compiler.sync_ascii_artifacts"),
        ):
            compile_st(self.tasks["SELF001"], cand, self.work_dir / "comp_ws", settings=cfg)

        self.assertEqual(lock_timeouts[-1], 960.0)

        # Simulation lock budget also exceeds long timed process timeout
        sim_lock_timeouts: list[float] = []

        class _FakeSimLock:
            def __init__(self, timeout: float = 0.0):
                sim_lock_timeouts.append(float(timeout))

            def __enter__(self):
                return 0.0

            def __exit__(self, *args):
                return False

        timed_case = [
            {
                "id": "t1",
                "steps": [
                    {
                        "dt_ms": 600000,
                        "inputs": {"Start": True, "Stop": False, "GuardClosed": True},
                        "expected": {"Run": True},
                    }
                ],
            }
        ]
        norm_cand = normalize_candidate(cand)
        with (
            patch("plc_agent.simulation.compiler_lock", side_effect=lambda timeout=900: _FakeSimLock(timeout)),
            patch("plc_agent.simulation.subprocess.Popen", return_value=_FakeProc()),
            patch("plc_agent.simulation.codesys_command", side_effect=lambda cmd: cmd),
            patch("plc_agent.simulation.sync_ascii_artifacts"),
        ):
            run_functional(
                self.tasks["SELF001"],
                norm_cand,
                digest(norm_cand),
                self.work_dir / "sim_ws",
                cfg,
                cases=timed_case,
            )

        self.assertGreaterEqual(sim_lock_timeouts[-1], 990 + 60)

    def test_standalone_smv_lowering_chained_words_and_temporal_call_guard(self):
        # C operators + chained inequalities
        self.assertEqual(_translate_st_ltl_to_smv("a && b || !c"), "a & b | !c")
        self.assertEqual(
            _translate_st_ltl_to_smv("-4<=TEMP_SETPOINT_ADJUST<=4"),
            "((-4 <= TEMP_SETPOINT_ADJUST) & (TEMP_SETPOINT_ADJUST <= 4))",
        )
        # ST hex literal & bare integer comparison against word[16]/word[32]
        self.assertEqual(
            _translate_st_ltl_to_smv("status=16#8001", {"status": "word[16]"}),
            "status = 0uh16_8001",
        )
        self.assertEqual(
            _translate_st_ltl_to_smv("G((risingBits & fallingBits)=0)", {"risingBits": "word[32]", "fallingBits": "word[32]"}),
            "G((risingBits & fallingBits) = 0ud32_0)",
        )
        # Temporal operator nested inside scalar function must be rejected
        bad_expr = "G(X(Count) = min(Count + 1, X(Target)))"
        self.assertFalse(
            _is_valid_standalone_smv_expr(
                bad_expr,
                _translate_st_ltl_to_smv(bad_expr),
                {"Count", "Target"},
            )
        )

        # Standalone compilation of PUB002, PUB003, PUB013 avoids '#' & expands chained/word literals
        cand_pub002 = {
            "declaration": (
                "FUNCTION_BLOCK FB_Task\nVAR_INPUT value : DWORD; END_VAR\n"
                "VAR_OUTPUT hasChanged : BOOL; hasRisingEdges : BOOL; risingBits : DWORD; "
                "noOfRisingBits : USINT; hasFallingEdges : BOOL; fallingBits : DWORD; "
                "noOfFallingBits : USINT; END_VAR\nVAR prev : DWORD := DWORD#0; END_VAR"
            ),
            "implementation": (
                "risingBits := value AND NOT prev; fallingBits := prev AND NOT value; "
                "hasChanged := value <> prev; hasRisingEdges := risingBits <> DWORD#0; "
                "hasFallingEdges := fallingBits <> DWORD#0; noOfRisingBits := 0; "
                "noOfFallingBits := 0; prev := value;"
            ),
            "supporting_objects": [],
        }
        cand_pub003 = {
            "declaration": (
                "FUNCTION_BLOCK FB_Task\n"
                "VAR_INPUT Value, hiLevel, loLevel, hystWindow : REAL; END_VAR\n"
                "VAR_OUTPUT hiAlarm, loAlarm, error : BOOL; status : WORD; END_VAR\n"
            ),
            "implementation": "hiAlarm := FALSE; loAlarm := FALSE; error := FALSE; status := WORD#0;",
            "supporting_objects": [],
        }
        cand_pub013 = {
            "declaration": (
                "FUNCTION_BLOCK FB_Task\n"
                "VAR_INPUT OCCUPANCY_DETECTED, ENERGY_SAVING_MODE : BOOL; HVAC_MODE_SELECTOR : INT; END_VAR\n"
                "VAR_OUTPUT SUPPLY_FAN_RUN : BOOL; TEMP_SETPOINT_ADJUST : INT; END_VAR\n"
            ),
            "implementation": "SUPPLY_FAN_RUN := OCCUPANCY_DETECTED; TEMP_SETPOINT_ADJUST := 0;",
            "supporting_objects": [],
        }
        for tid, cand_obj, expected_token in (
            ("PUB002", cand_pub002, "0ud32_0"),
            ("PUB003", cand_pub003, "0uh16_8001"),
            ("PUB013", cand_pub013, "((-4 <= TEMP_SETPOINT_ADJUST) & (TEMP_SETPOINT_ADJUST <= 4))"),
        ):
            compiled = compile_st_to_smv(cand_obj, self.tasks[tid], use_observer_smv=False)
            self.assertNotIn("#", compiled["smv_text"])
            self.assertIn(expected_token, compiled["smv_text"])

    def test_standalone_verify_drops_crashing_planner_assertions_and_skips_nested_temporal_min(self):
        self._require_checkers()
        cand_self009 = {
            "declaration": (
                "FUNCTION_BLOCK FB_Task\n"
                "VAR_INPUT\n"
                "    PartPulse, Reset : BOOL;\n"
                "    Target : INT;\n"
                "END_VAR\n"
                "VAR_OUTPUT\n"
                "    Count : INT := 0;\n"
                "    Complete, Error : BOOL := FALSE;\n"
                "END_VAR\n"
                "VAR\n"
                "    prevPulse : BOOL := FALSE;\n"
                "END_VAR\n"
            ),
            "implementation": (
                "Error := (Target < 1) OR (Target > 20);\n"
                "IF Error OR Reset THEN\n"
                "    Count := 0;\n"
                "ELSE\n"
                "    IF PartPulse AND NOT prevPulse AND Count < Target THEN\n"
                "        Count := Count + 1;\n"
                "    END_IF;\n"
                "END_IF;\n"
                "Complete := (NOT Error) AND (NOT Reset) AND (Count >= Target);\n"
                "prevPulse := PartPulse;\n"
            ),
            "supporting_objects": [],
        }
        bad_assertions = [
            {"id": "A_bad_min", "formula": "G((!Reset & PartPulse) -> X(Count) = min(Count + 1, X(Target)))"},
            {"id": "A_ok", "formula": "G(Error -> Count = 0)"},
        ]
        res = verify_candidate_st(
            task=self.tasks["SELF009"],
            candidate=cand_self009,
            out_dir=self.work_dir / "self009_bad_assert",
            use_observer_smv=False,
            extra_assertions=bad_assertions,
        )
        self.assertEqual(res["status"], "PASS", res)
        self.assertTrue(any("A_bad_min" in w for w in res.get("warnings", [])))

        # Runtime TOOL_ERROR caused solely by extra_assertions falls back cleanly to public/sanity verification
        cand_self001 = read_json(ROOT / "codesys/examples/SELF001.json")
        calls = {"n": 0}

        def _fake_check_model(**kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                return {"status": "TOOL_ERROR", "property_results": [], "expected_properties": 1, "tool": "NuSMV"}
            return {
                "status": "MODEL_PROPERTIES_TRUE",
                "property_results": [{"id": "P_sanity", "holds": True}],
                "expected_properties": 1,
                "tool": "NuSMV",
            }

        with patch("plc_agent.st_verifier.check_model", side_effect=_fake_check_model):
            fb_res = verify_candidate_st(
                task=self.tasks["SELF001"],
                candidate=cand_self001,
                out_dir=self.work_dir / "self001_extra_fallback",
                use_observer_smv=False,
                extra_assertions=[{"id": "A_oops", "formula": "G(Start -> Run)"}],
            )
        self.assertEqual(calls["n"], 2)
        self.assertEqual(fb_res["status"], "PASS")
        self.assertTrue(any("Dropped planner formal_assertions" in w for w in fb_res.get("warnings", [])))

    def test_coupled_observer_mode_maps_task_ltl_ids_and_retains_honest_gaps(self):
        from plc_agent.st_verifier import _parse_observer_smv, discover_observer_smv, extract_observer_spec_id_map

        # PUB001_complete.smv uses shifted P1_init..P11 + SPEC_outputs_iff; formula+tag mapping aligns all 12 specs
        pub1_smv = discover_observer_smv("PUB001")
        self.assertIsNotNone(pub1_smv)
        obs_pub1 = _parse_observer_smv(pub1_smv.read_text(encoding="utf-8"))
        pub1_map = extract_observer_spec_id_map(obs_pub1.spec_stmts, self.tasks["PUB001"])
        self.assertEqual(pub1_map[0], "PUB001.P_init")
        self.assertEqual(pub1_map[1], "PUB001.P1")
        self.assertIn("PUB001.COMPLETE", pub1_map)

        # PUB004_reference.smv lacks COMPLETE; PUB004.COMPLETE must stay unmapped cleanly
        obs_pub4 = _parse_observer_smv(discover_observer_smv("PUB004").read_text(encoding="utf-8"))
        pub4_map = extract_observer_spec_id_map(obs_pub4.spec_stmts, self.tasks["PUB004"])
        self.assertIn("PUB004.P1", pub4_map)
        self.assertNotIn("PUB004.COMPLETE", pub4_map)

        # End-to-end coupled observer compilation & verification on SELF001 reference ST achieves COMPLETE coverage
        self._require_checkers()
        ref_self001 = read_json(ROOT / "codesys/examples/SELF001.json")
        compiled = compile_st_to_smv(ref_self001, self.tasks["SELF001"], use_observer_smv=True)
        self.assertIn("spec_id_map", compiled)
        self.assertIn("SELF001.COMPLETE", compiled["spec_id_map"])
        ver = verify_candidate_st(
            task=self.tasks["SELF001"],
            candidate=ref_self001,
            out_dir=self.work_dir / "self001_coupled_mapped",
            use_observer_smv=True,
        )
        self.assertEqual(ver["status"], "PASS", ver)
        self.assertEqual(ver["specification_coverage"]["status"], "COMPLETE")
        self.assertEqual(ver["specification_coverage"]["unproven_or_unmapped_ids"], [])
        self.assertTrue(ver["full_specification_verified"])


if __name__ == "__main__":
    unittest.main()
