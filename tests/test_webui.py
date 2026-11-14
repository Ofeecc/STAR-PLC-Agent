import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from urllib.request import urlopen

from plc_agent.backend import CompileResult, FakeBackend
from plc_agent.config import Settings
from plc_agent.webui import handle_api_request, render_index_html, serve_webui


class WebUITests(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.evidence_root = Path(self.temp.name) / "webui_evidence"

    def test_every_task_has_current_chinese_review_interface_tests_and_properties(self):
        from plc_agent.common import digest
        from plc_agent.task_view import agent_view

        status, listing = handle_api_request("GET", "/api/tasks", {}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertEqual(len(listing["task_review"]), 32)
        self.assertEqual(len(listing["pilot_review"]), 6)
        count = 0
        for summary in listing["tasks"]:
            status, detail = handle_api_request("GET", "/api/task", {"id": summary["id"]}, None, self.settings)
            task, review = detail["task"], detail["review"]
            self.assertTrue(review["source_matches"])
            self.assertEqual(review["source_task_sha256"], digest(task))
            self.assertEqual(review["review_status"], "HUMAN_REVIEWED")
            self.assertEqual(detail["agent_view"], agent_view(task))
            self.assertNotIn("translation_zh", detail["agent_view"])
            for field in ("title_zh", "translation_zh", "assumptions_zh", "coverage_zh", "review_points_zh"):
                self.assertRegex(review[field], r"[\u4e00-\u9fff]")
            self.assertEqual(set(review["interface_zh"]), {p["name"] for p in task["interface"]})
            self.assertEqual(set(review["tests_zh"]), {c["id"] for c in task["tests"]})
            for case in task["tests"]:
                self.assertEqual(review["tests_zh"][case["id"]]["source_sha256"], digest(case))
            self.assertEqual(set(review["properties_zh"]), {p["id"] for p in task["ltl"]})
            for prop in task["ltl"]:
                self.assertEqual(review["properties_zh"][prop["id"]]["formula"], prop["formula"])
                self.assertRegex(review["properties_zh"][prop["id"]]["description"], r"[\u4e00-\u9fff]")
                count += 1
        self.assertEqual(count, 294)

    def test_six_pilot_tasks_have_review_material_and_match_current_dataset(self):
        status, listing = handle_api_request("GET", "/api/tasks", {}, None, self.settings)
        self.assertEqual(status, 200)
        ids = ["PUB001", "PUB003", "PUB009", "PUB010", "PUB015", "PUB016"]
        self.assertEqual([r["id"] for r in listing["pilot_review"]], ids)
        cases = steps = 0
        difficulties = []
        for tid in ids:
            status, detail = handle_api_request("GET", "/api/task", {"id": tid}, None, self.settings)
            self.assertEqual(status, 200)
            self.assertEqual(detail["task"]["kind"], "public")
            self.assertEqual(detail["review"]["id"], tid)
            for field in ("title_zh", "translation_zh", "assumptions_zh", "coverage_zh", "review_points_zh"):
                self.assertTrue(detail["review"][field])
            cases += len(detail["tests"])
            steps += sum(len(c["steps"]) for c in detail["tests"])
            difficulties.append(detail["task"]["difficulty"])
            summary = next(t for t in listing["tasks"] if t["id"] == tid)
            self.assertEqual(summary["steps_count"], sum(len(c["steps"]) for c in detail["tests"]))
        selected = [t for t in listing["tasks"] if t["id"] in ids]
        self.assertGreaterEqual((cases, steps), (26, 314))
        self.assertEqual(
            (cases, steps), (sum(t["tests_count"] for t in selected), sum(t["steps_count"] for t in selected))
        )
        self.assertEqual(difficulties, ["easy", "easy", "medium", "medium", "hard", "hard"])

    def test_pilot_chinese_explanations_cover_every_current_formula(self):
        count = 0
        for tid in ["PUB001", "PUB003", "PUB009", "PUB010", "PUB015", "PUB016"]:
            status, detail = handle_api_request("GET", "/api/task", {"id": tid}, None, self.settings)
            self.assertEqual(status, 200)
            chinese = detail["review"]["properties_zh"]
            self.assertEqual(set(chinese), {p["id"] for p in detail["task"]["ltl"]})
            for prop in detail["task"]["ltl"]:
                row = chinese[prop["id"]]
                self.assertEqual(row["formula"], prop["formula"])
                self.assertTrue(row["description"])
                self.assertTrue(row["review"])
                count += 1
        self.assertEqual(count, 64)

    def test_model_checker_api_keeps_reference_scope_and_rejects_other_tasks(self):
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_status = Path(tmpdir) / "smv_status.json"
            for body in (
                None,
                {},
                {"task_id": "NON_EXISTENT"},
                {"task_id": "../../arbitrary"},
                {"task_id": "PUB001", "variant": "../bad"},
            ):
                status, _ = handle_api_request(
                    "POST", "/api/check-reference-model", {}, body, self.settings, smv_status_path=tmp_status
                )
                self.assertEqual(status, 400)
            with (
                patch("plc_agent.model_checker.find_nusmv", side_effect=ValueError("not installed")),
                patch("plc_agent.model_checker.find_nuxmv", side_effect=ValueError("not installed")),
                patch("plc_agent.model_checker.check_model", side_effect=ValueError("not installed")),
            ):
                for tid in ("PUB001", "PUB016"):
                    status, data = handle_api_request(
                        "POST",
                        "/api/check-reference-model",
                        {},
                        {"task_id": tid},
                        self.settings,
                        smv_status_path=tmp_status,
                    )
                    self.assertEqual(status, 503)
                    self.assertEqual(data["status"], "TOOL_ERROR")
                    self.assertEqual(data["verification_status"], "CHECKER_MISSING")
                    self.assertTrue(data["checker_missing"])
                    self.assertEqual(data["smv_status"]["scope"], "EXPLICIT_SMV_MODEL_ONLY")
                    self.assertFalse(data["smv_status"]["candidate_st_verified"])

    def test_persisted_smv_status_reports_verified_both_for_all_32_tasks(self):
        status, listing = handle_api_request("GET", "/api/tasks", {}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertIn("checker_availability", listing)
        self.assertEqual(len(listing["tasks"]), 32)
        for t in listing["tasks"]:
            smv = t["smv_status"]
            self.assertEqual(smv["scope"], "EXPLICIT_SMV_MODEL_ONLY")
            self.assertFalse(smv["candidate_st_verified"])
            self.assertTrue(smv["authored"])
            self.assertFalse(smv["stale"], t["id"])
            self.assertEqual(smv["verification_status"], "VERIFIED_BOTH", t["id"])
            self.assertRegex(smv["authoring_text_zh"], r"[\u4e00-\u9fff]")
            self.assertRegex(smv["badge_text_zh"], r"[\u4e00-\u9fff]")

    def test_missing_checker_handling_preserves_baseline_and_records_unverified_missing(self):
        import shutil
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        from plc_agent.smv_status import DEFAULT_SMV_STATUS_PATH, load_smv_status_store

        with tempfile.TemporaryDirectory() as tmpdir:
            # Subcase A: persisted baseline present + checker uninstalled
            copied_status = Path(tmpdir) / "copied_status.json"
            shutil.copy2(DEFAULT_SMV_STATUS_PATH, copied_status)
            with (
                patch("plc_agent.model_checker.find_nusmv", side_effect=ValueError("NuSMV missing")),
                patch("plc_agent.model_checker.find_nuxmv", side_effect=ValueError("nuXmv missing")),
                patch("plc_agent.model_checker.check_model", side_effect=ValueError("checker missing")),
            ):
                status, detail = handle_api_request(
                    "GET", "/api/task", {"id": "PUB015"}, None, self.settings, smv_status_path=copied_status
                )
                self.assertEqual(status, 200)
                smv = detail["smv_status"]
                self.assertTrue(smv["checker_missing"])
                self.assertFalse(smv["live_rerunnable"])
                self.assertEqual(smv["verification_status"], "VERIFIED_BOTH")
                self.assertIn("nuXmv", smv["badge_text_zh"])

                post_status, post_data = handle_api_request(
                    "POST",
                    "/api/check-reference-model",
                    {},
                    {"task_id": "PUB015", "variant": "reference"},
                    self.settings,
                    smv_status_path=copied_status,
                )
                self.assertEqual(post_status, 503)
                self.assertEqual(post_data["verification_status"], "CHECKER_MISSING")
                store_after = load_smv_status_store(copied_status)
                self.assertEqual(
                    store_after["records"]["PUB015"]["models"]["reference"]["status"],
                    "MODEL_PROPERTIES_TRUE",
                )
                self.assertEqual(
                    store_after["records"]["PUB015"]["last_run_attempt"]["status"],
                    "CHECKER_MISSING",
                )

            # Subcase B: fresh store + checker missing
            empty_status = Path(tmpdir) / "empty_status.json"
            with (
                patch("plc_agent.model_checker.find_nusmv", side_effect=ValueError("NuSMV missing")),
                patch("plc_agent.model_checker.find_nuxmv", side_effect=ValueError("nuXmv missing")),
                patch("plc_agent.model_checker.check_model", side_effect=ValueError("checker missing")),
            ):
                status, detail = handle_api_request(
                    "GET", "/api/task", {"id": "PUB015"}, None, self.settings, smv_status_path=empty_status
                )
                self.assertEqual(status, 200)
                self.assertEqual(detail["smv_status"]["verification_status"], "CHECKER_MISSING")
                self.assertFalse(detail["smv_status"]["persisted_record_present"])

                post_status, post_data = handle_api_request(
                    "POST",
                    "/api/check-reference-model",
                    {},
                    {"task_id": "PUB015", "variant": "reference"},
                    self.settings,
                    smv_status_path=empty_status,
                )
                self.assertEqual(post_status, 503)
                self.assertEqual(post_data["verification_status"], "CHECKER_MISSING")
                persisted = load_smv_status_store(empty_status)
                self.assertEqual(
                    persisted["records"]["PUB015"]["models"]["reference"]["status"],
                    "CHECKER_MISSING",
                )

    def test_stale_smv_status_detected_when_model_hash_differs(self):
        import tempfile
        from pathlib import Path

        from plc_agent.smv_status import DEFAULT_SMV_STATUS_PATH, load_smv_status_store, save_smv_status_store

        with tempfile.TemporaryDirectory() as tmpdir:
            stale_status = Path(tmpdir) / "stale_status.json"
            store = load_smv_status_store(DEFAULT_SMV_STATUS_PATH)
            store["records"]["PUB001"]["models"]["reference"]["model_sha256"] = "0" * 64
            save_smv_status_store(store, status_path=stale_status)
            status, detail = handle_api_request(
                "GET", "/api/task", {"id": "PUB001"}, None, self.settings, smv_status_path=stale_status
            )
            self.assertEqual(status, 200)
            self.assertEqual(detail["smv_status"]["verification_status"], "STALE")
            self.assertTrue(detail["smv_status"]["stale"])
            self.assertTrue(detail["smv_status"]["models"]["reference"]["stale"])

    def test_symbol_glossary_covers_all_tokens_and_highlights_persistence(self):
        import re

        status, listing = handle_api_request("GET", "/api/tasks", {}, None, self.settings)
        self.assertEqual(status, 200)
        inout_checked = 0
        for summary in listing["tasks"]:
            tid = summary["id"]
            st, detail = handle_api_request("GET", "/api/task", {"id": tid}, None, self.settings)
            self.assertEqual(st, 200)
            glossary = detail["symbol_glossary"]
            task = detail["task"]
            for pin in task.get("interface", []):
                self.assertIn(pin["name"], glossary, f"{tid}:{pin['name']}")
                entry = glossary[pin["name"]]
                self.assertTrue(entry.get("category_en"))
                self.assertTrue(entry.get("type_en"))
                self.assertTrue(entry.get("definition_en"))
                if pin.get("direction") == "IN_OUT":
                    inout_checked += 1
                    self.assertEqual(entry["category"], "persistent_inout")
                    self.assertTrue(entry["is_persistent"])
                    self.assertTrue(entry["persistence_warning_zh"])
                    self.assertTrue(entry.get("persistence_warning_en"))
            for prop in task.get("ltl", []):
                for tok in re.findall(r"[A-Za-z_][A-Za-z_0-9.]*", prop["formula"]):
                    if tok in {"G", "F", "X", "U", "R", "V", "W", "TRUE", "FALSE", "AND", "OR", "NOT"} or tok.isdigit():
                        continue
                    self.assertIn(tok, glossary, f"Missing glossary token {tid} {prop['id']}: {tok}")
            if tid == "PUB001":
                self.assertEqual(glossary["phase"]["category"], "ghost_state")
                self.assertTrue(glossary["phase"]["is_persistent"])
                self.assertEqual(glossary["bottleSensor"]["category"], "input")
                self.assertEqual(glossary["Pump_Motor"]["category"], "output")
        self.assertGreater(inout_checked, 0)

    def test_render_index_html_contains_titles_and_components(self):
        html = render_index_html()
        self.assertIsInstance(html, str)
        self.assertIn('<html lang="en">', html)
        self.assertIn("STAR-PLC | Agent Workflow, Benchmark &amp; Waveform Inspector", html)
        self.assertIn("Dataset &amp; Specs", html)
        self.assertIn("Workflow &amp; Benchmark", html)
        self.assertIn("Sandbox &amp; Waveform Lab", html)
        # Ensure clean white-on-black theme without blue/purple styling tokens
        for forbidden_color in ("#38bdf8", "#3b82f6", "#6366f1", "#a855f7", "#8b5cf6", "#c4b5fd", "#93c5fd"):
            self.assertNotIn(forbidden_color, html)
        # Fixed header tracks keep EN/ZH toggle zero-shift
        self.assertIn("grid-template-columns: 1fr auto 1fr", html)
        self.assertIn("grid-template-columns: repeat(3, 190px)", html)
        # Concise UI without defensive boilerplate
        self.assertNotIn("brand-subtitle", html)
        self.assertNotIn("Candidate SMV: UNVERIFIED", html)
        self.assertNotIn("not a candidate ST proof", html)
        # Check essential UI controls
        for req_id in (
            "task-select",
            "waveform-view",
            "trace-playback",
            "sandbox-editor",
            "st-highlight-code",
            "spec-popover",
            "overview-smv-box",
            "pilot-card-smv",
            "run-select",
            "version-history-panel",
            "trace-waveform-display",
            "highlightST",
            "openTestWaveform",
            "renderGlossaryPanel",
            "symbol_glossary",
        ):
            self.assertIn(req_id, html)
        self.assertLess(html.index('id="spec-popover"'), html.rindex("<script>"))

    def test_app_js_parses_and_renders_all_32_tasks_in_js_runtime(self):
        import re
        import shutil
        import subprocess
        import tempfile
        from pathlib import Path

        html = render_index_html()
        match = re.search(r"<script>\s*(.*)\s*</script>", html, re.S)
        self.assertIsNotNone(match)
        js_code = match.group(1)
        gjs_exe = shutil.which("gjs")
        if not gjs_exe:
            self.skipTest("gjs JS runtime not installed")

        _, tasks_data = handle_api_request("GET", "/api/tasks", {}, None, self.settings)
        _, task_detail = handle_api_request("GET", "/api/task", {"id": "PUB015"}, None, self.settings)
        _, runs_data = handle_api_request("GET", "/api/runs", {}, None, self.settings)
        _, exp_data = handle_api_request("GET", "/api/experiments", {}, None, self.settings)
        pub1_run = next(r for r in runs_data["runs"] if r["task_id"] == "PUB001" and r["status"] == "PASS")
        _, trace_data = handle_api_request("GET", "/api/run-trace", {"run": pub1_run["run_id"]}, None, self.settings)
        ids = sorted(set(re.findall(r'id="([^"]+)"', html)))
        harness = f"""
globalThis.TASKS_DATA = {json.dumps(tasks_data)};
globalThis.TASK_DETAIL = {json.dumps(task_detail)};
globalThis.RUNS_DATA = {json.dumps(runs_data)};
globalThis.TRACE_DATA = {json.dumps(trace_data)};
globalThis.EXP_DATA = {json.dumps(exp_data)};
const ALL_IDS = {json.dumps(ids)};
const JS_CODE = {json.dumps(js_code)};
new Function(JS_CODE);
globalThis.URLSearchParams = class {{
  constructor() {{ this.m = {{}}; }}
  get(k) {{ return this.m[k] || null; }}
  set(k, v) {{ this.m[k] = String(v); }}
}};
globalThis.URL = class {{
  constructor(u) {{ this.href = u; this.searchParams = new URLSearchParams(); }}
  toString() {{ return this.href; }}
}};
globalThis.elements = {{}};
globalThis.makeEl = function(id) {{
  return {{
    id, value: '', checked: false, hidden: false, textContent: '', innerHTML: '',
    style: {{}}, dataset: {{}}, options: [],
    classList: {{ toggle() {{}}, add() {{}}, remove() {{}} }},
    setAttribute() {{}}, getAttribute() {{ return ''; }},
    addEventListener() {{}}, querySelectorAll() {{ return []; }}, querySelector() {{ return null; }},
    closest() {{ return null; }}, getBoundingClientRect() {{ return {{left:0,top:0,bottom:10,width:100,height:40}}; }}
  }};
}};
ALL_IDS.forEach(id => globalThis.elements[id] = globalThis.makeEl(id));
globalThis.elements['kind-filter'].value = 'all';
globalThis.elements['difficulty-filter'].value = 'all';
globalThis.elements['language-select'].value = 'en';
globalThis.location = {{ search: '', href: 'http://127.0.0.1:8765/' }};
globalThis.history = {{ replaceState() {{}} }};
globalThis.localStorage = {{ getItem() {{ return null; }}, setItem() {{}} }};
globalThis.addEventListener = (ev, fn) => {{ if (ev === 'DOMContentLoaded') globalThis._domReady = fn; }};
globalThis.innerWidth = 1280;
globalThis.innerHeight = 800;
globalThis.NodeFilter = {{ SHOW_TEXT: 4 }};
globalThis.setTimeout = () => 1;
globalThis.clearTimeout = () => {{}};
globalThis.document = {{
  body: {{}},
  documentElement: {{ lang: 'en' }},
  title: '',
  createTreeWalker() {{ return {{ nextNode() {{ return null; }} }}; }},
  getElementById(id) {{ if (!globalThis.elements[id]) globalThis.elements[id] = globalThis.makeEl(id); return globalThis.elements[id]; }},
  querySelectorAll() {{ return []; }},
  addEventListener() {{}}
}};
globalThis.fetch = async (url) => ({{
  ok: true, status: 200, statusText: 'OK',
  async json() {{
    if (url === '/api/tasks') return globalThis.TASKS_DATA;
    if (url.startsWith('/api/task?')) return globalThis.TASK_DETAIL;
    if (url === '/api/runs') return globalThis.RUNS_DATA;
    if (url === '/api/experiments') return globalThis.EXP_DATA;
    if (url.startsWith('/api/run-trace?')) return globalThis.TRACE_DATA;
    if (url === '/api/check-reference-model') return {{
      status: 'MODEL_PROPERTIES_TRUE', tool: 'NuSMV', verification_status: 'VERIFIED_BOTH',
      smv_status: globalThis.TASK_DETAIL.smv_status
    }};
    return {{}};
  }}
}});
const check = [
  'if (globalThis._domReady) globalThis._domReady();',
  'if (gLang !== "en") throw new Error("Default gLang must be en, got " + gLang);',
  'gTasks = globalThis.TASKS_DATA.tasks;',
  'gReviews = globalThis.TASKS_DATA.task_review;',
  'gPilotReview = globalThis.TASKS_DATA.pilot_review;',
  'gCheckerAvail = globalThis.TASKS_DATA.checker_availability;',
  'renderSystemStatus();',
  'if (!globalThis.elements["system-status"].innerHTML.includes("NuSMV") || globalThis.elements["system-status"].innerHTML.includes("Offline")) throw new Error("Expected live NuSMV badge, got " + globalThis.elements["system-status"].innerHTML);',
  'renderTaskList(false);',
  'gCurrentTask = globalThis.TASK_DETAIL;',
  'renderTaskDetails(globalThis.TASK_DETAIL);',
  'renderReviewDetails(globalThis.TASK_DETAIL);',
  'populateSandboxTemplate(globalThis.TASK_DETAIL);',
  'if (!globalThis.elements["st-highlight-code"].innerHTML.includes("st-kw-block") || !globalThis.elements["st-highlight-code"].innerHTML.includes("st-kw-type")) throw new Error("Missing ST syntax highlighting");',
  'if (!globalThis.elements["tests-container"].innerHTML.includes("wave-table") || !globalThis.elements["tests-container"].innerHTML.includes("openTestWaveform")) throw new Error("Missing inline test signal table or jump button");',
  'openTestWaveform("PUB001.T1");',
  'if (globalThis.elements["waveform-case-select"].value !== "PUB001.T1" || !globalThis.elements["waveform-display"].innerHTML.includes("wave-table")) throw new Error("openTestWaveform did not select PUB001.T1");',
  'if (!globalThis.elements["pilot-grid"].innerHTML.includes("Human reviewed")) throw new Error("Missing English Human reviewed badge");',
  'if (globalThis.elements["tests-container"].innerHTML.includes("固定测试")) throw new Error("Chinese text leaked in EN mode");',
  'showSpecPopover(globalThis.makeEl("anchor"), "Spre", true);',
  'const popEn = globalThis.elements["spec-popover"].innerHTML;',
  'const popOpen = !globalThis.elements["spec-popover"].hidden && popEn.includes("Spre") && !popEn.includes("中文");',
  'changeLanguage("zh");',
  'if (!globalThis.elements["tests-container"].innerHTML.includes("固定测试")) throw new Error("Missing ZH tests label");',
  'if (!globalThis.elements["pilot-grid"].innerHTML.includes("已完成人工审阅")) throw new Error("Missing ZH human reviewed badge");',
  'changeLanguage("en");',
  'gRuns = globalThis.RUNS_DATA.runs;',
  'gExperiments = globalThis.EXP_DATA;',
  'gCurrentRunTrace = globalThis.TRACE_DATA;',
  'renderRunSelect();',
  'renderRunTrace(globalThis.TRACE_DATA);',
  'renderBenchmarkPanel();',
  'if (!globalThis.elements["trace-playback"].innerHTML.includes("1. Planner")) throw new Error("Missing Planner stage");',
  'if (!globalThis.elements["trace-waveform-display"].innerHTML.includes("Pump_Motor")) throw new Error("Missing trace waveform signal");',
  'hideSpecPopover(true);',
  'const cards = (globalThis.elements["pilot-grid"].innerHTML.match(/data-task-id="/g)||[]).length;',
  'const activeCards = (globalThis.elements["pilot-grid"].innerHTML.match(/class="pilot-card active"/g)||[]).length;',
  'const opts = (globalThis.elements["task-select"].innerHTML.match(/<option /g)||[]).length;',
  'if (cards !== 32 || activeCards !== 1 || opts !== 32) throw new Error("Expected 32/1/32 cards/active/options, got " + cards + "/" + activeCards + "/" + opts);',
  'if (!popOpen) throw new Error("Popover did not open cleanly in EN");',
  'if (!globalThis.elements["task-overview"].innerHTML.includes("overview-smv-box")) throw new Error("Missing SMV box");',
  'if (!globalThis.elements["task-overview"].innerHTML.includes("PASS") || globalThis.elements["task-overview"].innerHTML.includes(">UNVERIFIED<")) throw new Error("SMV panel showed UNVERIFIED instead of PASS: " + globalThis.elements["task-overview"].innerHTML);',
  'const noCompHtml = renderSmvBoxInner("PUB002", {{ verification_status: "VERIFIED_BOTH", badge_tone: "green", badge_text_en: "Verified", models: {{ reference: globalThis.TASK_DETAIL.smv_status.models.reference, mutant: globalThis.TASK_DETAIL.smv_status.models.mutant }} }});',
  'if (noCompHtml.includes("complete.smv")) throw new Error("Unexpected complete.smv row for task without complete.smv");',
  'runSmvCheck("reference");',
  'if (!globalThis.elements["overview-smv-box"].innerHTML.includes("smv-action-feedback") || !globalThis.elements["overview-smv-box"].innerHTML.includes("Running...")) throw new Error("Missing instant SMV busy feedback: " + globalThis.elements["overview-smv-box"].innerHTML);',
  'if (!globalThis.elements["ltl-container"].innerHTML.includes("spec-tok--")) throw new Error("Missing highlighted tokens");',
  'print("JS_DOM_OK", cards, opts);'
].join('\\n');
(0, eval)(JS_CODE + '\\n' + check);
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = Path(tmpdir) / "check_webui.js"
            script_path.write_text(harness, encoding="utf-8")
            proc = subprocess.run([gjs_exe, str(script_path)], capture_output=True, text=True, check=False)
            self.assertEqual(proc.returncode, 0, f"gjs failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
            self.assertIn("JS_DOM_OK 32 32", proc.stdout)

    def test_handle_api_request_tasks_returns_all_32_tasks(self):
        status, data = handle_api_request("GET", "/api/tasks", {}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertIn("tasks", data)
        tasks = data["tasks"]
        self.assertEqual(len(tasks), 32)
        pub_tasks = [t for t in tasks if t["kind"] == "public"]
        self_tasks = [t for t in tasks if t["kind"] == "self_built"]
        self.assertEqual(len(pub_tasks), 20)
        self.assertEqual(len(self_tasks), 12)
        for t in tasks:
            self.assertIn("id", t)
            self.assertIn("title", t)
            self.assertIn("kind", t)
            self.assertIn("difficulty", t)
            self.assertIn("tests_count", t)

    def test_handle_api_request_task_detail_and_random_cases(self):
        status, data = handle_api_request("GET", "/api/task", {"id": "SELF001"}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertIn("task", data)
        self.assertEqual(data["task"]["id"], "SELF001")
        self.assertIn("agent_view", data)
        self.assertNotIn("tests", data["agent_view"])
        self.assertIn("tests", data)
        self.assertGreater(len(data["tests"]), 0)
        self.assertIn("random_cases", data)
        self.assertGreater(len(data["random_cases"]), 0)

    def test_handle_api_request_task_detail_with_list_query(self):
        status, data = handle_api_request("GET", "/api/task", {"id": ["PUB001"]}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertEqual(data["task"]["id"], "PUB001")
        self.assertIn("random_cases", data)

    def test_handle_api_request_task_not_found(self):
        status, data = handle_api_request("GET", "/api/task", {"id": "NON_EXISTENT"}, None, self.settings)
        self.assertEqual(status, 404)
        self.assertIn("error", data)

    def test_handle_api_request_evaluate_with_fake_backend_compile_failure(self):
        backend = FakeBackend(
            compile_fn=lambda t, c, w: CompileResult(
                status="COMPILE_FAIL",
                success=False,
                diagnostics=[{"message": "Syntax error: unknown variable 'FooBar'"}],
            )
        )
        body = {
            "task_id": "SELF001",
            "candidate": "Invalid ST candidate",
            "include_random": False,
        }
        status, data = handle_api_request(
            "POST", "/api/evaluate", {}, body, self.settings, backend=backend, evidence_root=self.evidence_root
        )
        self.assertEqual(status, 200)
        self.assertIn("compile", data)
        self.assertFalse(data["compile"]["success"])
        self.assertEqual(data["compile"]["status"], "COMPILE_FAIL")
        self.assertIn("simulation", data)
        self.assertEqual(data["simulation"]["status"], "COMPILE_FAIL")

    def test_handle_api_request_evaluate_with_fake_backend_simulation_failure(self):
        # Step fn returns all False/0 which fails against SELF001 contract
        backend = FakeBackend(step_fn=lambda inp, dt: {"High": False, "Alarm": False, "Filtered": 0.0})
        body = {
            "task_id": "SELF001",
            "candidate": {
                "declaration": "FUNCTION_BLOCK FB_SELF001\nEND_VAR",
                "implementation": "",
            },
            "include_random": True,
        }
        status, data = handle_api_request(
            "POST", "/api/evaluate", {}, body, self.settings, backend=backend, evidence_root=self.evidence_root
        )
        self.assertEqual(status, 200)
        self.assertIn("compile", data)
        self.assertTrue(data["compile"]["success"])
        self.assertIn("simulation", data)
        self.assertEqual(data["simulation"]["status"], "TEST_FAIL")
        self.assertGreater(len(data["simulation"]["failures"]), 0)
        self.assertIn("waveform", data)
        self.assertGreater(len(data["waveform"]), 0)
        # Check first failing case has divergence recorded
        first_wave = data["waveform"][0]
        self.assertIn("steps", first_wave)
        matches = [s["match"] for s in first_wave["steps"] if s["match"] is not None]
        self.assertIn(False, matches)

    def test_evaluate_preserves_compiler_infrastructure_status(self):
        body = {"task_id": "SELF001", "candidate": "Test candidate"}
        for compile_status in ("TOOL_ERROR", "TIMEOUT", "UNVERIFIED"):
            with self.subTest(compile_status=compile_status):
                backend = FakeBackend(
                    compile_fn=lambda task, candidate, workspace: CompileResult(
                        status=compile_status,
                        infrastructure_error="Compiler did not produce usable evidence",
                    )
                )
                status, data = handle_api_request(
                    "POST", "/api/evaluate", {}, body, self.settings, backend=backend, evidence_root=self.evidence_root
                )
                self.assertEqual(status, 200)
                self.assertEqual(data["compile"]["status"], compile_status)
                self.assertEqual(data["simulation"]["status"], compile_status)
                self.assertEqual(data["simulation"]["evaluated_cases"], 0)
                self.assertEqual(data["simulation"]["infrastructure_error"], "Compiler did not produce usable evidence")
                self.assertEqual(data["waveform"], [])

    def test_handle_api_request_evaluate_with_default_fake_backend_passes(self):
        # When step_fn is None, FakeBackend executes ScanContract directly, which passes valid tests
        backend = FakeBackend()
        body = {
            "task_id": "SELF001",
            "candidate": {
                "declaration": "FUNCTION_BLOCK FB_SELF001\nEND_VAR",
                "implementation": "",
            },
            "include_random": False,
        }
        status, data = handle_api_request(
            "POST", "/api/evaluate", {}, body, self.settings, backend=backend, evidence_root=self.evidence_root
        )
        self.assertEqual(status, 200)
        self.assertTrue(data["compile"]["success"])
        self.assertEqual(data["simulation"]["status"], "PASS")
        self.assertEqual(len(data["simulation"]["failures"]), 0)

    def test_handle_api_request_export_verify(self):
        candidate = {
            "declaration": (
                "FUNCTION_BLOCK FB_SELF001\n"
                "VAR_INPUT\n  RawValue : REAL;\n  Reset : BOOL;\nEND_VAR\n"
                "VAR_OUTPUT\n  Filtered : REAL;\n  High : BOOL;\n  Alarm : BOOL;\nEND_VAR\n"
            ),
            "implementation": "Filtered := RawValue; High := FALSE; Alarm := FALSE;",
            "supporting_objects": [],
        }
        body = {
            "task_id": "SELF001",
            "candidate": candidate,
        }
        status, data = handle_api_request("POST", "/api/export-verify", {}, body, self.settings)
        self.assertEqual(status, 200)
        self.assertIn("manifest", data)
        manifest = data["manifest"]
        self.assertEqual(manifest["task_id"], "SELF001")
        self.assertEqual(manifest["st_path"], "candidate.st")
        self.assertEqual(manifest["ltl_path"], "spec.ltl")
        self.assertIn("properties", manifest)
        self.assertIn("candidate_st", data)
        self.assertIn("spec_ltl", data)

    def test_handle_api_request_experiments(self):
        status, data = handle_api_request("GET", "/api/experiments", {}, None, self.settings)
        self.assertEqual(status, 200)
        self.assertIn("summaries", data)
        self.assertIn("conditions", data)

    def test_handle_api_request_invalid_route(self):
        status, data = handle_api_request("GET", "/api/unknown_route", {}, None, self.settings)
        self.assertEqual(status, 404)
        self.assertIn("error", data)

    def test_handle_api_request_runs_and_run_trace_pilot_evidence(self):
        status, runs_data = handle_api_request("GET", "/api/runs", {}, None, self.settings)
        self.assertEqual(status, 200)
        runs = runs_data.get("runs", [])
        self.assertGreaterEqual(len(runs), 2)
        pub1_pass = next(
            (r for r in runs if r["task_id"] == "PUB001" and r["status"] == "PASS" and r["source"] == "pilot"),
            None,
        )
        self.assertIsNotNone(pub1_pass)

        st, trace = handle_api_request("GET", "/api/run-trace", {"run": pub1_pass["run_id"]}, None, self.settings)
        self.assertEqual(st, 200)
        self.assertEqual(trace["task_id"], "PUB001")
        self.assertEqual(trace["framework_kind"], "star")
        self.assertEqual([s["id"] for s in trace["stages"]], ["planner", "dialect", "coder", "tester", "ratchet"])
        self.assertEqual(trace["stages"][0]["status"], "DONE")
        self.assertEqual(trace["stages"][4]["status"], "PASS")
        self.assertGreaterEqual(len(trace["versions"]), 1)
        self.assertGreaterEqual(len(trace["timeline"]), 6)
        self.assertGreater(trace["token_summary"]["total_tokens"], 0)
        self.assertEqual(trace["formal_verification"]["status"], "UNVERIFIED")
        self.assertEqual(trace["waveform_source"]["kind"], "fixed_evaluation")
        self.assertEqual(len(trace["waveforms"]), 2)
        self.assertTrue(all(step["match"] for wf in trace["waveforms"] for step in wf["steps"]))

    def test_handle_api_request_runs_supports_live_experiments_and_ratchet_rollback(self):
        root = Path(self.temp.name) / "ws"
        star_run = root / "experiments" / "E3" / "campaign_demo" / "PUB001" / "run_01"
        star_run.mkdir(parents=True)
        (star_run / "runtime_config.json").write_text(
            json.dumps(
                {"condition": "E3", "framework": "self_harness", "model": "demo-model", "utc": "2026-11-14T10:00:00Z"}
            ),
            encoding="utf-8",
        )
        (star_run / "task_view.json").write_text(json.dumps({"id": "PUB001", "title": "Bottling"}), encoding="utf-8")
        (star_run / "plan.json").write_text(
            json.dumps({"state_machine": {"states": [{"name": "IDLE", "phase": 0}]}}), encoding="utf-8"
        )
        (star_run / "dialect_cards.json").write_text(
            json.dumps([{"id": "ton_timer", "title": "TON"}]), encoding="utf-8"
        )
        (star_run / "version_00.json").write_text(
            json.dumps(
                {
                    "declaration": "FUNCTION_BLOCK FB_Task\nVAR_OUTPUT\n x : BOOL;\nEND_VAR",
                    "implementation": "x := TRUE;",
                }
            ),
            encoding="utf-8",
        )
        (star_run / "version_sim_01.json").write_text(
            json.dumps(
                {
                    "declaration": "FUNCTION_BLOCK FB_Task\nVAR_OUTPUT\n x : BOOL;\nEND_VAR",
                    "implementation": "x := FALSE;",
                }
            ),
            encoding="utf-8",
        )
        (star_run / "compile_sim_01").mkdir()
        (star_run / "compile_sim_01" / "compile_result.json").write_text(
            json.dumps({"status": "COMPILE_FAIL", "success": False}), encoding="utf-8"
        )
        (star_run / "final_candidate.json").write_text(
            json.dumps(
                {
                    "declaration": "FUNCTION_BLOCK FB_Task\nVAR_OUTPUT\n x : BOOL;\nEND_VAR",
                    "implementation": "x := TRUE;",
                }
            ),
            encoding="utf-8",
        )
        (star_run / "selftest.json").write_text(json.dumps([{"id": "case_1", "steps": []}]), encoding="utf-8")
        (star_run / "model_calls.jsonl").write_text(
            json.dumps(
                {
                    "utc": "2026-11-14T10:00:01Z",
                    "event": "request_started",
                    "call_dir": "llm_planner",
                    "model": "demo-model",
                }
            )
            + "\n"
            + json.dumps(
                {
                    "utc": "2026-11-14T10:00:05Z",
                    "event": "request_completed",
                    "call_dir": "llm_planner",
                    "elapsed_seconds": 4.0,
                }
            )
            + "\n"
            + json.dumps(
                {
                    "utc": "2026-11-14T10:00:06Z",
                    "event": "request_started",
                    "call_dir": "llm_tester",
                    "model": "demo-model",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        (star_run / "execution.jsonl").write_text(
            json.dumps({"utc": "2026-11-14T10:00:08Z", "event": "compile_finished", "status": "PASS", "success": True})
            + "\n"
            + '{"utc": "partial_unclosed_line',
            encoding="utf-8",
        )

        base_run = root / "experiments" / "E1" / "campaign_demo" / "SELF001" / "run_02"
        (base_run / "turn_00").mkdir(parents=True)
        (base_run / "trusted" / "compile_00").mkdir(parents=True)
        (base_run / "runtime_config.json").write_text(
            json.dumps(
                {
                    "condition": "E1",
                    "framework": "custom_tool_loop",
                    "model": "demo-model",
                    "utc": "2026-11-14T09:00:00Z",
                }
            ),
            encoding="utf-8",
        )
        (base_run / "task.json").write_text(json.dumps({"id": "SELF001"}), encoding="utf-8")
        (base_run / "turn_00" / "tool_01.json").write_text(
            json.dumps({"call_id": "c1", "name": "compile_st", "arguments": {}, "result": {"status": "PASS"}}),
            encoding="utf-8",
        )
        (base_run / "result.json").write_text(
            json.dumps(
                {
                    "task_id": "SELF001",
                    "condition": "E1",
                    "framework": "custom_tool_loop",
                    "status": "UNVERIFIED",
                    "final_compiled": True,
                }
            ),
            encoding="utf-8",
        )

        st, listed = handle_api_request("GET", "/api/runs", {}, None, self.settings, workspace_root=root)
        self.assertEqual(st, 200)
        self.assertEqual(len(listed["runs"]), 2)
        self.assertEqual(listed["runs"][0]["state"], "running")
        self.assertEqual(listed["runs"][0]["task_id"], "PUB001")

        st, star_trace = handle_api_request(
            "GET", "/api/run-trace", {"run": listed["runs"][0]["run_id"]}, None, self.settings, workspace_root=root
        )
        self.assertEqual(st, 200)
        self.assertEqual(star_trace["state"], "running")
        self.assertIsNone(star_trace["token_summary"]["total_tokens"])
        tester_stage = next(s for s in star_trace["stages"] if s["id"] == "tester")
        ratchet_stage = next(s for s in star_trace["stages"] if s["id"] == "ratchet")
        self.assertEqual(tester_stage["status"], "RUNNING")
        self.assertEqual(ratchet_stage["metrics"]["rollback_count"], 1)
        sim_v = next(v for v in star_trace["versions"] if v["id"] == "version_sim_01")
        self.assertTrue(sim_v["rolled_back"])
        self.assertTrue(
            any(
                "-x := TRUE;" in line and "+x := FALSE;" in "\n".join(sim_v["diff_from_prev"])
                for line in sim_v["diff_from_prev"]
            )
        )

        st, base_trace = handle_api_request(
            "GET", "/api/run-trace", {"run": listed["runs"][1]["run_id"]}, None, self.settings, workspace_root=root
        )
        self.assertEqual(st, 200)
        self.assertEqual(base_trace["framework_kind"], "baseline")
        self.assertEqual([s["id"] for s in base_trace["stages"]], ["context", "tool_loop", "compile_sim", "final"])

    def test_handle_api_request_run_trace_rejects_traversal_and_missing(self):
        for bad in ("../configs", "/etc/passwd", "experiments/../../configs", "src/plc_agent"):
            st, _ = handle_api_request("GET", "/api/run-trace", {"run": bad}, None, self.settings)
            self.assertIn(st, (400, 403, 404))
        st_missing, _ = handle_api_request("GET", "/api/run-trace", {}, None, self.settings)
        self.assertEqual(st_missing, 400)

    def test_handle_api_request_reference_st(self):
        st, data = handle_api_request("GET", "/api/reference-st", {"id": "SELF001"}, None, self.settings)
        self.assertEqual(st, 200)
        self.assertTrue(data["available"])
        self.assertIn("FUNCTION_BLOCK FB_Task", data["declaration"])
        self.assertIn("provenance", data)
        st_404, miss = handle_api_request("GET", "/api/reference-st", {"id": "PUB001"}, None, self.settings)
        self.assertEqual(st_404, 404)
        self.assertFalse(miss["available"])
        st_bad, _ = handle_api_request("GET", "/api/reference-st", {"id": "../secret"}, None, self.settings)
        self.assertEqual(st_bad, 400)

    def test_serve_webui_http_server(self):
        # Start server on ephemeral port (port 0) in a background thread
        stop_event = threading.Event()
        bound_port = [0]
        server_thread = threading.Thread(
            target=serve_webui,
            kwargs={
                "host": "127.0.0.1",
                "port": 0,
                "settings": self.settings,
                "stop_event": stop_event,
                "bound_port_box": bound_port,
            },
            daemon=True,
        )
        server_thread.start()
        time.sleep(0.1)

        port = bound_port[0]
        self.assertGreater(port, 0)

        # 1. Fetch index HTML
        url = f"http://127.0.0.1:{port}/"
        with urlopen(url, timeout=3) as response:
            self.assertEqual(response.status, 200)
            content_type = response.headers.get("Content-Type", "")
            self.assertIn("text/html", content_type)
            body = response.read().decode("utf-8")
            self.assertIn("STAR-PLC | Agent Workflow, Benchmark &amp; Waveform Inspector", body)

        # 2. Fetch /api/tasks
        api_url = f"http://127.0.0.1:{port}/api/tasks"
        with urlopen(api_url, timeout=3) as response:
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            self.assertIn("tasks", data)
            self.assertEqual(len(data["tasks"]), 32)
            self.assertIn("smv_status", data["tasks"][0])

        # 3. Fetch /api/task?id=PUB015
        task_url = f"http://127.0.0.1:{port}/api/task?id=PUB015"
        with urlopen(task_url, timeout=3) as response:
            self.assertEqual(response.status, 200)
            detail = json.loads(response.read().decode("utf-8"))
            self.assertEqual(detail["task"]["id"], "PUB015")
            self.assertIn("symbol_glossary", detail)
            self.assertEqual(detail["smv_status"]["verification_status"], "VERIFIED_BOTH")

        # Stop the server
        stop_event.set()
        # Ping once to unblock server loop if needed
        try:
            urlopen(url, timeout=0.5)
        except Exception:
            pass
        server_thread.join(timeout=2)

    def test_cli_web_subcommand_parser(self):
        from unittest.mock import patch

        from plc_agent import cli

        test_argv = ["plc-agent", "web", "--host", "0.0.0.0", "--port", "9999"]
        with patch("sys.argv", test_argv), patch("plc_agent.webui.serve_webui") as mock_serve:
            exit_code = cli.main()
            self.assertEqual(exit_code, 0)
            mock_serve.assert_called_once()
            args, kwargs = mock_serve.call_args
            self.assertEqual(args[0], "0.0.0.0")
            self.assertEqual(args[1], 9999)


if __name__ == "__main__":
    unittest.main()
