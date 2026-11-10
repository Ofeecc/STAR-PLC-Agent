"""CODESYS STAR v2 Auto-Testing & Waveform Agent Trace Inspector Web Platform.

Provides a standalone zero-dependency HTTP server with a rich single-page application
for exploring tasks, visualizing logic waveforms, inspecting agent traces,
and testing/verifying ST programs.
"""
from __future__ import annotations

import dataclasses
import http.server
import json
from pathlib import Path
import tempfile
import threading
from typing import Any
import urllib.parse

from .backend import Backend, CodesysBackend, FakeBackend, SimCaseFailure, SimResult
from .common import ROOT, digest, now, read_json, write_json
from .compiler import CompileResult, normalize_candidate
from .config import Settings
from .dataset import load_tasks
from .formal_verify import export_verification_bundle
from .functional import outputs_equal
from .random_testing import generate_random_cases
from .task_view import agent_view


def _is_compiler_ready(settings: Settings) -> bool:
    ready = settings.compiler_ready()
    if isinstance(ready, bool):
        return ready
    if isinstance(ready, (list, tuple, set)):
        return len(ready) == 0
    return bool(ready)


def _safe_json_serialize(obj: Any) -> Any:
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, (list, tuple)):
        return [_safe_json_serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _safe_json_serialize(v) for k, v in obj.items()}
    return obj


def _build_step_waveforms(
    task: dict,
    cases: list[dict],
    sim_res: SimResult,
    workspace: Path,
) -> list[dict[str, Any]]:
    """Build detailed step-by-step logic signal waveforms with divergence highlighting."""
    # Check if a real execution trace was dumped in the workspace or raw result
    raw_cases: dict[str, Any] = {}
    if sim_res.raw and isinstance(sim_res.raw, dict):
        raw_cases = sim_res.raw.get("cases") or {}
    if not raw_cases:
        trace_file = workspace / "trace.json"
        if trace_file.is_file():
            try:
                trace_data = read_json(trace_file)
                raw_cases = trace_data.get("cases", {})
            except Exception:
                raw_cases = {}

    waveforms = []
    failure_map = {f.case_id: f for f in sim_res.failures}

    for case_idx, case in enumerate(cases):
        case_id = case.get("id", f"case_{case_idx + 1}")
        case_name = case.get("name", case_id)
        case_fail = failure_map.get(case_id)
        raw_case = raw_cases.get(case_id, {})
        raw_steps = raw_case.get("steps", [])

        steps_data = []
        for step_idx, step in enumerate(case.get("steps", [])):
            inputs = step.get("inputs", {})
            expected = step.get("expected", {})
            dt_ms = step.get("dt_ms")

            if raw_steps and step_idx < len(raw_steps):
                obs = raw_steps[step_idx].get("outputs", raw_steps[step_idx])
                is_match = outputs_equal(task, obs, expected, inputs)
                divergence = None
                if not is_match:
                    diff_fields = [k for k in expected if not outputs_equal(task, {k: obs.get(k)}, {k: expected.get(k)}, inputs)]
                    field_name = diff_fields[0] if diff_fields else next(iter(expected.keys()), "")
                    divergence = {
                        "field": field_name,
                        "expected": expected.get(field_name),
                        "observed": obs.get(field_name) if isinstance(obs, dict) else obs,
                    }
                steps_data.append({
                    "step": step_idx,
                    "inputs": inputs,
                    "expected": expected,
                    "observed": obs,
                    "dt_ms": dt_ms,
                    "match": is_match,
                    "divergence": divergence,
                })
            elif case_fail:
                if step_idx < case_fail.first_bad_step:
                    steps_data.append({
                        "step": step_idx,
                        "inputs": inputs,
                        "expected": expected,
                        "observed": dict(expected),
                        "dt_ms": dt_ms,
                        "match": True,
                        "divergence": None,
                    })
                elif step_idx == case_fail.first_bad_step:
                    obs = dict(expected)
                    obs[case_fail.field] = case_fail.observed
                    steps_data.append({
                        "step": step_idx,
                        "inputs": inputs,
                        "expected": expected,
                        "observed": obs,
                        "dt_ms": dt_ms,
                        "match": False,
                        "divergence": {
                            "field": case_fail.field,
                            "expected": case_fail.expected,
                            "observed": case_fail.observed,
                        },
                    })
                else:
                    steps_data.append({
                        "step": step_idx,
                        "inputs": inputs,
                        "expected": expected,
                        "observed": None,
                        "dt_ms": dt_ms,
                        "match": None,
                        "divergence": None,
                    })
            else:
                steps_data.append({
                    "step": step_idx,
                    "inputs": inputs,
                    "expected": expected,
                    "observed": dict(expected),
                    "dt_ms": dt_ms,
                    "match": True,
                    "divergence": None,
                })

        waveforms.append({
            "case_id": case_id,
            "name": case_name,
            "passed": case_fail is None,
            "steps": steps_data,
        })

    return waveforms


def handle_api_request(
    method: str,
    path: str,
    query: dict,
    body: dict | None,
    settings: Settings,
    backend: Backend | None = None,
) -> tuple[int, dict]:
    """Dispatch API request to internal handlers and return (status_code, json_dict)."""
    method = method.upper()

    def get_query_param(name: str) -> str | None:
        val = query.get(name)
        if isinstance(val, list):
            return str(val[0]) if val else None
        return str(val) if val is not None else None

    # 1. GET /api/tasks
    if method == "GET" and path == "/api/tasks":
        tasks = load_tasks()
        task_list = [
            {
                "id": t["id"],
                "title": t.get("title", ""),
                "kind": t.get("kind", ""),
                "difficulty": t.get("difficulty", ""),
                "tests_count": len(t.get("tests", [])),
            }
            for t in tasks
        ]
        return 200, {"tasks": task_list, "total": len(task_list)}

    # 2. GET /api/task?id=...
    if method == "GET" and path == "/api/task":
        task_id = get_query_param("id")
        if not task_id:
            return 400, {"error": "Missing required query parameter: 'id'"}
        tasks = load_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return 404, {"error": f"Task '{task_id}' not found"}
        rand_cases = generate_random_cases(task)
        return 200, {
            "task": task,
            "agent_view": agent_view(task),
            "tests": task.get("tests", []),
            "random_cases": rand_cases,
        }

    # 3. POST /api/evaluate
    if method == "POST" and path == "/api/evaluate":
        if not body or not isinstance(body, dict):
            return 400, {"error": "Request body must be a JSON object"}
        task_id = body.get("task_id")
        if not task_id:
            return 400, {"error": "Missing required field: 'task_id'"}
        candidate = body.get("candidate")
        if candidate is None:
            return 400, {"error": "Missing required field: 'candidate'"}

        tasks = load_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return 404, {"error": f"Task '{task_id}' not found"}

        if backend is None:
            if _is_compiler_ready(settings):
                backend = CodesysBackend(settings)
            else:
                backend = FakeBackend()

        with tempfile.TemporaryDirectory(prefix=f"webui_eval_{task_id}_") as tmpdir:
            workspace = Path(tmpdir)
            compile_res = backend.compile(task, candidate, workspace)

            cases = list(task.get("tests", []))
            if body.get("include_random", False):
                cases.extend(generate_random_cases(task))

            if not compile_res.success:
                sim_res = SimResult(
                    status="COMPILE_FAIL",
                    passed_cases=0,
                    evaluated_cases=0,
                    failures=[],
                    infrastructure_error=compile_res.infrastructure_error,
                )
                waveform: list[dict] = []
            else:
                sim_res = backend.simulate(task, candidate, cases, workspace)
                waveform = _build_step_waveforms(task, cases, sim_res, workspace)

            return 200, {
                "compile": _safe_json_serialize(compile_res),
                "simulation": _safe_json_serialize(sim_res),
                "waveform": waveform,
            }

    # 4. GET /api/experiments
    if method == "GET" and path == "/api/experiments":
        summaries: dict[str, Any] = {}
        summary_dir = ROOT / "results/summary"
        if summary_dir.is_dir():
            for f in sorted(summary_dir.glob("*.json")):
                try:
                    summaries[f.stem] = read_json(f)
                except Exception:
                    pass

        conditions = []
        cfg_path = ROOT / "configs/experiments.json"
        if cfg_path.is_file():
            try:
                conditions = read_json(cfg_path).get("conditions", [])
            except Exception:
                conditions = []

        metrics = summaries.get("metrics")
        campaign = summaries.get("campaign")
        return 200, {
            "metrics": metrics,
            "campaign": campaign,
            "conditions": conditions,
            "summaries": summaries,
        }

    # 5. POST /api/export-verify
    if method == "POST" and path == "/api/export-verify":
        if not body or not isinstance(body, dict):
            return 400, {"error": "Request body must be a JSON object"}
        task_id = body.get("task_id")
        if not task_id:
            return 400, {"error": "Missing required field: 'task_id'"}
        candidate = body.get("candidate")
        if candidate is None:
            return 400, {"error": "Missing required field: 'candidate'"}

        tasks = load_tasks()
        task = next((t for t in tasks if t["id"] == task_id), None)
        if not task:
            return 404, {"error": f"Task '{task_id}' not found"}

        out_dir_str = body.get("out_dir")
        if out_dir_str:
            out_dir = Path(out_dir_str)
        else:
            out_dir = Path(tempfile.mkdtemp(prefix=f"star_verify_{task_id}_"))

        out_dir.mkdir(parents=True, exist_ok=True)
        manifest = export_verification_bundle(task, candidate, out_dir)

        st_file = out_dir / manifest.get("st_path", "candidate.st")
        ltl_file = out_dir / manifest.get("ltl_path", "spec.ltl")
        st_content = st_file.read_text(encoding="utf-8") if st_file.is_file() else ""
        ltl_content = ltl_file.read_text(encoding="utf-8") if ltl_file.is_file() else ""

        return 200, {
            "status": "PASS",
            "manifest": manifest,
            "bundle_dir": str(out_dir),
            "files": {
                "st_path": str(st_file),
                "ltl_path": str(ltl_file),
                "manifest_path": str(out_dir / "verification_manifest.json"),
            },
            "candidate_st": st_content,
            "spec_ltl": ltl_content,
        }

    return 404, {"error": f"Not found: {method} {path}"}


def render_index_html() -> str:
    """Render a sleek, modern, responsive single-page application UI."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CODESYS STAR v2 | Auto-Test & Waveform Agent Trace Inspector</title>
  <style>
    :root {
      --bg-primary: #0f141c;
      --bg-secondary: #171f2c;
      --bg-card: #1f2b3e;
      --bg-accent: #263854;
      --text-main: #e2e8f0;
      --text-muted: #94a3b8;
      --text-bright: #ffffff;
      --cyan: #38bdf8;
      --green: #22c55e;
      --amber: #f59e0b;
      --red: #ef4444;
      --purple: #a855f7;
      --border-color: #334155;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg-primary);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 1rem;
    }
    .brand-icon {
      width: 38px;
      height: 38px;
      border-radius: 8px;
      background: linear-gradient(135deg, #0284c7, #38bdf8);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      color: #fff;
      font-size: 1.2rem;
    }
    .brand-text h1 {
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text-bright);
    }
    .brand-text p {
      font-size: 0.8rem;
      color: var(--cyan);
      font-family: var(--font-mono);
    }
    .status-badge {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.4rem 0.8rem;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 9999px;
      font-size: 0.8rem;
      font-family: var(--font-mono);
    }
    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--green);
      box-shadow: 0 0 8px var(--green);
    }
    nav.tab-nav {
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      padding: 0 2rem;
      gap: 0.5rem;
      overflow-x: auto;
    }
    .tab-btn {
      background: none;
      border: none;
      color: var(--text-muted);
      padding: 0.9rem 1.2rem;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      border-bottom: 3px solid transparent;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .tab-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.03);
    }
    .tab-btn.active {
      color: var(--cyan);
      border-bottom-color: var(--cyan);
      background: rgba(56, 189, 248, 0.05);
    }
    main {
      flex: 1;
      padding: 1.5rem 2rem;
      max-width: 1600px;
      width: 100%;
      margin: 0 auto;
    }
    .tab-pane {
      display: none;
    }
    .tab-pane.active {
      display: block;
      animation: fadeIn 0.2s ease;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .card {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 1.25rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      padding-bottom: 0.75rem;
      border-bottom: 1px solid var(--border-color);
    }
    .card-title {
      font-size: 1.1rem;
      font-weight: 700;
      color: var(--text-bright);
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }
    .controls-row {
      display: flex;
      align-items: center;
      gap: 1rem;
      flex-wrap: wrap;
      margin-bottom: 1rem;
    }
    select, input[type="text"], input[type="number"], textarea {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.6rem 0.9rem;
      border-radius: 6px;
      font-family: inherit;
      font-size: 0.9rem;
    }
    select:focus, input:focus, textarea:focus {
      outline: none;
      border-color: var(--cyan);
      box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }
    button.btn {
      background: linear-gradient(135deg, #0284c7, #0ea5e9);
      color: white;
      border: none;
      padding: 0.6rem 1.2rem;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.9rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.15s ease;
    }
    button.btn:hover {
      background: linear-gradient(135deg, #0369a1, #0284c7);
      transform: translateY(-1px);
    }
    button.btn-secondary {
      background: var(--bg-accent);
      color: var(--text-main);
      border: 1px solid var(--border-color);
    }
    button.btn-secondary:hover {
      background: var(--bg-card);
    }
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      margin-top: 0.5rem;
    }
    table.data-table th, table.data-table td {
      border: 1px solid var(--border-color);
      padding: 0.6rem 0.8rem;
      text-align: left;
    }
    table.data-table th {
      background: var(--bg-card);
      color: var(--text-bright);
      font-weight: 600;
    }
    table.data-table tr:nth-child(even) {
      background: rgba(255, 255, 255, 0.02);
    }
    .badge {
      display: inline-block;
      padding: 0.2rem 0.55rem;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      font-family: var(--font-mono);
    }
    .badge-pub { background: #0369a1; color: #bae6fd; }
    .badge-self { background: #7e22ce; color: #f3e8ff; }
    .badge-easy { background: #15803d; color: #bbf7d0; }
    .badge-med { background: #b45309; color: #fef3c7; }
    .badge-hard { background: #b91c1c; color: #fee2e2; }
    .badge-pass { background: #166534; color: #86efac; }
    .badge-fail { background: #991b1b; color: #fca5a5; }

    /* Waveform visualizer */
    .waveform-container {
      overflow-x: auto;
      background: #090d13;
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 1rem;
      margin-top: 1rem;
      font-family: var(--font-mono);
      min-height: 240px;
    }
    .waveform-timeline {
      display: grid;
      grid-template-columns: 180px repeat(auto-fit, minmax(65px, 1fr));
      gap: 2px;
      margin-bottom: 0.5rem;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 0.5rem;
    }
    .waveform-signal {
      display: grid;
      grid-template-columns: 180px repeat(auto-fit, minmax(65px, 1fr));
      gap: 2px;
      align-items: center;
      margin-bottom: 4px;
    }
    .sig-label {
      font-size: 0.8rem;
      color: var(--cyan);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding-right: 0.5rem;
    }
    .sig-cell {
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.75rem;
      border-radius: 3px;
      border: 1px solid rgba(255, 255, 255, 0.05);
      font-weight: 600;
    }
    .sig-cell.true { background: rgba(34, 197, 94, 0.2); color: #86efac; border-color: rgba(34, 197, 94, 0.4); }
    .sig-cell.false { background: rgba(239, 68, 68, 0.1); color: #94a3b8; }
    .sig-cell.mismatch { background: #dc2626 !important; color: white !important; font-weight: 800; box-shadow: 0 0 8px #ef4444; }
    .sig-cell.unexecuted { background: #1e293b; color: #64748b; }

    /* Trace Playback Graph */
    .pipeline-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1rem;
      margin-top: 1rem;
    }
    .pipeline-step {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 1rem;
      position: relative;
    }
    .pipeline-step.active {
      border-color: var(--cyan);
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
    }
    .pipeline-step-num {
      font-size: 0.75rem;
      font-family: var(--font-mono);
      color: var(--cyan);
      text-transform: uppercase;
      margin-bottom: 0.3rem;
    }
    .pipeline-step-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-bright);
      margin-bottom: 0.5rem;
    }

    /* Sandbox editor */
    .editor-wrapper {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }
    @media (max-width: 1024px) {
      .editor-wrapper { grid-template-columns: 1fr; }
    }
    textarea.code-area {
      width: 100%;
      height: 440px;
      font-family: var(--font-mono);
      font-size: 0.85rem;
      line-height: 1.4;
      background: #0d121a;
      color: #f1f5f9;
      resize: vertical;
    }
    .console-box {
      background: #090d13;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 1rem;
      font-family: var(--font-mono);
      font-size: 0.8rem;
      max-height: 440px;
      overflow-y: auto;
      color: #cbd5e1;
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-icon">⚡</div>
      <div class="brand-text">
        <h1>CODESYS STAR v2 | Auto-Test & Waveform Agent Trace Inspector</h1>
        <p>AUTONOMOUS IEC 61131-3 VERIFIED ENGINEERING BENCHMARK</p>
      </div>
    </div>
    <div class="status-badge">
      <div class="pulse-dot"></div>
      <span id="system-status">AGENT READY (32 TASKS LOADED)</span>
    </div>
  </header>

  <nav class="tab-nav">
    <button class="tab-btn active" onclick="switchTab('explorer')">📂 Task & Dataset Explorer</button>
    <button class="tab-btn" onclick="switchTab('waveform')">📊 Waveform & Timing Comparator</button>
    <button class="tab-btn" onclick="switchTab('trace')">🧠 Agent Trace Playback</button>
    <button class="tab-btn" onclick="switchTab('sandbox')">🧪 Interactive Sandbox & Verifier</button>
  </nav>

  <main>
    <!-- TAB 1: TASK & DATASET EXPLORER -->
    <div id="tab-explorer" class="tab-pane active">
      <div class="card">
        <div class="card-header">
          <div class="card-title"><span>Task Selector & Metadata</span></div>
          <div class="controls-row" style="margin-bottom:0;">
            <select id="task-select" onchange="onTaskSelected(this.value)">
              <option value="">Loading tasks...</option>
            </select>
            <button class="btn btn-secondary" onclick="reloadTasks()">🔄 Refresh</button>
          </div>
        </div>
        <div id="task-overview">
          <p style="color:var(--text-muted);">Select a task above to inspect details, interface pins, specifications, and test cases.</p>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title"><span>IEC Interface Pins & Signals</span></div>
        </div>
        <div id="interface-pins-container">
          <p style="color:var(--text-muted);">No task selected.</p>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title"><span>Formal LTL Properties & Safety Contracts</span></div>
        </div>
        <div id="ltl-container">
          <p style="color:var(--text-muted);">No task selected.</p>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <div class="card-title"><span>Fixed & Differential Random Test Cases</span></div>
        </div>
        <div id="tests-container">
          <p style="color:var(--text-muted);">No task selected.</p>
        </div>
      </div>
    </div>

    <!-- TAB 2: WAVEFORM & TIMING COMPARATOR -->
    <div id="tab-waveform" class="tab-pane">
      <div class="card" id="waveform-view">
        <div class="card-header">
          <div class="card-title"><span>Signal Waveform Comparator</span></div>
          <div class="controls-row" style="margin-bottom:0;">
            <select id="waveform-case-select" onchange="renderActiveWaveform()">
              <option value="">(Run evaluation to view waveforms)</option>
            </select>
            <button class="btn btn-secondary" onclick="runSandboxEvaluate()">⚡ Evaluate Current Task</button>
          </div>
        </div>
        <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">
          Visualizing step-by-step logic signals: comparing input stimuli, expected outputs, candidate observed outputs, and dt_ms intervals.
          Red blocks indicate first Divergence point where candidate failed.
        </div>
        <div id="waveform-display" class="waveform-container">
          <p style="color:var(--text-muted); padding:2rem; text-align:center;">Select or evaluate a candidate ST to inspect signal waveforms.</p>
        </div>
      </div>
    </div>

    <!-- TAB 3: AGENT TRACE PLAYBACK -->
    <div id="tab-trace" class="tab-pane">
      <div class="card" id="trace-playback">
        <div class="card-header">
          <div class="card-title"><span>Multi-Stage STAR Reasoning Pipeline</span></div>
          <button class="btn btn-secondary" onclick="loadTraceDetails()">🔄 Refresh Trace Status</button>
        </div>
        <p style="font-size:0.85rem; color:var(--text-muted);">
          Inspect the deterministic state graph, dialect cards applied, compiler diagnostic compactions, and ratchet progress.
        </p>

        <div class="pipeline-grid">
          <div class="pipeline-step active">
            <div class="pipeline-step-num">STAGE 01</div>
            <div class="pipeline-step-title">Contract Analyzer</div>
            <p style="font-size:0.8rem; color:var(--text-muted);">Parses interface types, LTL safety constraints, and initial state invariants.</p>
          </div>
          <div class="pipeline-step active">
            <div class="pipeline-step-num">STAGE 02</div>
            <div class="pipeline-step-title">Dialect Cards</div>
            <p style="font-size:0.8rem; color:var(--text-muted);">Injects target CODESYS V3.5 syntax rules, TIME literals, and vendor pragmas.</p>
          </div>
          <div class="pipeline-step active">
            <div class="pipeline-step-num">STAGE 03</div>
            <div class="pipeline-step-title">Compiler Loop</div>
            <p style="font-size:0.8rem; color:var(--text-muted);">Performs headless build, captures diagnostics, and maps line numbers.</p>
          </div>
          <div class="pipeline-step active">
            <div class="pipeline-step-num">STAGE 04</div>
            <div class="pipeline-step-title">Lexicographical Ratchet</div>
            <p style="font-size:0.8rem; color:var(--text-muted);">Monotonically guards against regression on passed test cases.</p>
          </div>
          <div class="pipeline-step active">
            <div class="pipeline-step-num">STAGE 05</div>
            <div class="pipeline-step-title">Formal Verifier</div>
            <p style="font-size:0.8rem; color:var(--text-muted);">Exports nuXmv / UPPAAL / CBMC bundles and verifies trace consistency.</p>
          </div>
        </div>

        <div style="margin-top:1.5rem;">
          <h3 style="font-size:1rem; margin-bottom:0.5rem; color:var(--cyan);">Applied CODESYS Dialect Rules</h3>
          <table class="data-table">
            <thead>
              <tr><th>Rule ID</th><th>Category</th><th>IEC 61131-3 Standard</th><th>CODESYS V3.5 Dialect Requirement</th></tr>
            </thead>
            <tbody>
              <tr><td>CARD-01</td><td>Time Literals</td><td><code>T#10s, TIME#100ms</code></td><td>Strict duration syntax, no space after prefix, microsecond precision</td></tr>
              <tr><td>CARD-02</td><td>In-Out Variables</td><td><code>VAR_IN_OUT</code> passed by reference</td><td>Requires allocated variable storage, no constants in caller POUs</td></tr>
              <tr><td>CARD-03</td><td>Ton/Toff Timers</td><td><code>IN, PT, Q, ET</code></td><td>State persistence across scan cycles; cannot be re-instantiated dynamically</td></tr>
              <tr><td>CARD-04</td><td>Array Indices</td><td>1-based or 0-based bounds</td><td>Explicit <code>ARRAY[0..N] OF TYPE</code> bounds checking</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 4: INTERACTIVE SANDBOX & VERIFIER -->
    <div id="tab-sandbox" class="tab-pane">
      <div class="card" id="sandbox-editor">
        <div class="card-header">
          <div class="card-title"><span>IEC Structured Text Sandbox & Verifier</span></div>
          <div class="controls-row" style="margin-bottom:0;">
            <label style="font-size:0.85rem; color:var(--text-muted);">
              <input type="checkbox" id="eval-include-random" checked> Include Random Differential Tests
            </label>
            <button class="btn" onclick="runSandboxEvaluate()">▶ Compile & Simulate</button>
            <button class="btn btn-secondary" onclick="exportFormalVerify()">🛡️ Export Verification Bundle</button>
          </div>
        </div>

        <div class="editor-wrapper">
          <div>
            <div style="font-size:0.85rem; color:var(--cyan); margin-bottom:0.4rem; font-family:var(--font-mono);">CANDIDATE STRUCTURED TEXT (ST):</div>
            <textarea id="st-source-code" class="code-area" placeholder="Enter Structured Text POUs (FUNCTION_BLOCK FB_Task ... END_FUNCTION_BLOCK)"></textarea>
          </div>
          <div>
            <div style="font-size:0.85rem; color:var(--cyan); margin-bottom:0.4rem; font-family:var(--font-mono);">COMPILER & SIMULATION CONSOLE:</div>
            <div id="sandbox-console" class="console-box">Ready. Select a task or edit Structured Text and press "Compile & Simulate".</div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <script>
    let gTasks = [];
    let gCurrentTask = null;
    let gLastWaveformData = [];

    function switchTab(name) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      const btn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.textContent.toLowerCase().includes(name));
      if (btn) btn.classList.add('active');
      const pane = document.getElementById('tab-' + name);
      if (pane) pane.classList.add('active');
    }

    async function reloadTasks() {
      try {
        const res = await fetch('/api/tasks');
        const data = await res.json();
        gTasks = data.tasks || [];
        const select = document.getElementById('task-select');
        select.innerHTML = '';
        gTasks.forEach(t => {
          const opt = document.createElement('option');
          opt.value = t.id;
          opt.textContent = `[${t.id}] ${t.title} (${t.difficulty.toUpperCase()}, ${t.kind})`;
          select.appendChild(opt);
        });
        if (gTasks.length > 0) {
          select.value = gTasks[0].id;
          onTaskSelected(gTasks[0].id);
        }
      } catch (err) {
        console.error("Failed to load tasks", err);
      }
    }

    async function onTaskSelected(taskId) {
      if (!taskId) return;
      try {
        const res = await fetch('/api/task?id=' + encodeURIComponent(taskId));
        const data = await res.json();
        gCurrentTask = data;
        renderTaskDetails(data);
        populateSandboxTemplate(data);
      } catch (err) {
        console.error("Failed to load task details", err);
      }
    }

    function renderTaskDetails(data) {
      const task = data.task;
      const overview = document.getElementById('task-overview');
      const kindClass = task.kind === 'public' ? 'badge-pub' : 'badge-self';
      const diffClass = task.difficulty === 'easy' ? 'badge-easy' : (task.difficulty === 'medium' ? 'badge-med' : 'badge-hard');

      overview.innerHTML = `
        <div style="display:flex; gap:0.5rem; align-items:center; margin-bottom:0.75rem;">
          <span class="badge ${kindClass}">${task.kind}</span>
          <span class="badge ${diffClass}">${task.difficulty}</span>
          <span style="font-weight:700; font-size:1.1rem; color:var(--text-bright);">${task.id}: ${task.title}</span>
        </div>
        <p style="margin-bottom:0.5rem; color:#cbd5e1;"><strong>Scenario:</strong> ${task.scenario || ''}</p>
        <p style="margin-bottom:0.5rem; color:#94a3b8; font-size:0.9rem;"><strong>Requirements:</strong> ${task.requirements || ''}</p>
        <p style="font-size:0.85rem; color:var(--cyan);"><strong>Safety Priority:</strong> ${task.safety_priority || 'Standard'}</p>
      `;

      // Interface table
      const pinsBox = document.getElementById('interface-pins-container');
      const iface = task.interface || [];
      if (iface.length === 0) {
        pinsBox.innerHTML = '<p style="color:var(--text-muted);">No pins defined.</p>';
      } else {
        let html = '<table class="data-table"><thead><tr><th>Name</th><th>Type</th><th>Direction</th><th>Comment</th></tr></thead><tbody>';
        iface.forEach(p => {
          html += `<tr>
            <td style="font-family:var(--font-mono); font-weight:700; color:var(--cyan);">${p.name}</td>
            <td style="font-family:var(--font-mono);">${p.type}</td>
            <td><span class="badge" style="background:#334155;">${p.direction}</span></td>
            <td style="color:#94a3b8;">${p.comment || ''}</td>
          </tr>`;
        });
        html += '</tbody></table>';
        pinsBox.innerHTML = html;
      }

      // LTL table
      const ltlBox = document.getElementById('ltl-container');
      const ltl = task.ltl || [];
      if (ltl.length === 0) {
        ltlBox.innerHTML = '<p style="color:var(--text-muted);">No LTL properties defined.</p>';
      } else {
        let html = '<table class="data-table"><thead><tr><th>Property ID</th><th>Formal Formula (LTL)</th><th>Description</th></tr></thead><tbody>';
        ltl.forEach(p => {
          html += `<tr>
            <td style="font-family:var(--font-mono); color:var(--amber); font-weight:700;">${p.id}</td>
            <td style="font-family:var(--font-mono); color:#a5b4fc;"><code>${p.formula}</code></td>
            <td style="color:#cbd5e1;">${p.explanation || p.description || ''}</td>
          </tr>`;
        });
        html += '</tbody></table>';
        ltlBox.innerHTML = html;
      }

      // Tests
      const testsBox = document.getElementById('tests-container');
      const fixedTests = data.tests || [];
      const randTests = data.random_cases || [];
      let thtml = `<p style="margin-bottom:0.5rem; font-size:0.9rem;">
        Fixed Dataset Tests: <strong>${fixedTests.length}</strong> | Differential Random Tests: <strong>${randTests.length}</strong>
      </p>`;
      thtml += '<table class="data-table"><thead><tr><th>Test ID</th><th>Kind</th><th>Steps Count</th><th>Description</th></tr></thead><tbody>';
      fixedTests.forEach(t => {
        thtml += `<tr>
          <td style="font-family:var(--font-mono); font-weight:700;">${t.id}</td>
          <td><span class="badge badge-pub">FIXED</span></td>
          <td>${(t.steps || []).length} steps</td>
          <td>${t.name || 'Dataset test'}</td>
        </tr>`;
      });
      randTests.forEach(t => {
        thtml += `<tr>
          <td style="font-family:var(--font-mono); font-weight:700;">${t.id}</td>
          <td><span class="badge badge-self">RANDOM</span></td>
          <td>${(t.steps || []).length} steps</td>
          <td>${t.name || 'Random differential test'}</td>
        </tr>`;
      });
      thtml += '</tbody></table>';
      testsBox.innerHTML = thtml;
    }

    function populateSandboxTemplate(data) {
      const task = data.task;
      const declLines = [
        `FUNCTION_BLOCK FB_${task.id}`,
        "VAR_INPUT"
      ];
      (task.interface || []).filter(p => p.direction === 'INPUT').forEach(p => {
        declLines.push(`    ${p.name} : ${p.type};`);
      });
      declLines.push("END_VAR");
      declLines.push("VAR_OUTPUT");
      (task.interface || []).filter(p => p.direction === 'OUTPUT').forEach(p => {
        declLines.push(`    ${p.name} : ${p.type};`);
      });
      declLines.push("END_VAR");

      const code = declLines.join("\\n") + "\\n\\n(* Implementation Logic *)\\n";
      const area = document.getElementById('st-source-code');
      if (area && !area.value.trim()) {
        area.value = code;
      }
    }

    async function runSandboxEvaluate() {
      if (!gCurrentTask) return;
      const taskId = gCurrentTask.task.id;
      const code = document.getElementById('st-source-code').value;
      const incRand = document.getElementById('eval-include-random').checked;
      const consoleBox = document.getElementById('sandbox-console');

      consoleBox.textContent = `[EVALUATING ${taskId}] Compiling ST & simulating cases...\\n`;
      try {
        const res = await fetch('/api/evaluate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            task_id: taskId,
            candidate: code,
            include_random: incRand
          })
        });
        const data = await res.json();
        const compile = data.compile || {};
        const sim = data.simulation || {};
        gLastWaveformData = data.waveform || [];

        let out = `--- COMPILATION RESULT ---\\n`;
        out += `Status: ${compile.status} (success=${compile.success})\\n`;
        if (compile.diagnostics) {
          out += `Diagnostics:\\n${JSON.stringify(compile.diagnostics, null, 2)}\\n`;
        }
        out += `\\n--- SIMULATION RESULT ---\\n`;
        out += `Status: ${sim.status}\\n`;
        out += `Passed: ${sim.passed_cases} / ${sim.evaluated_cases} cases\\n`;
        if (sim.failures && sim.failures.length > 0) {
          out += `Failures (${sim.failures.length}):\\n`;
          sim.failures.forEach((f, idx) => {
            out += `  [${idx+1}] Case: ${f.case_id}, First Bad Step: ${f.first_bad_step}, Field: ${f.field}\\n`;
            out += `       Expected: ${JSON.stringify(f.expected)}\\n`;
            out += `       Observed: ${JSON.stringify(f.observed)}\\n`;
          });
        }
        consoleBox.textContent = out;

        // Populate waveform selector
        updateWaveformCaseSelector();
        switchTab('waveform');
      } catch (err) {
        consoleBox.textContent += `\\nEvaluation error: ${err.message}`;
      }
    }

    function updateWaveformCaseSelector() {
      const select = document.getElementById('waveform-case-select');
      select.innerHTML = '';
      if (!gLastWaveformData || gLastWaveformData.length === 0) {
        select.innerHTML = '<option value="">(No waveform data)</option>';
        return;
      }
      gLastWaveformData.forEach((w, idx) => {
        const opt = document.createElement('option');
        opt.value = idx;
        opt.textContent = `${w.case_id} (${w.passed ? 'PASS' : 'FAIL'}, ${w.steps.length} steps)`;
        select.appendChild(opt);
      });
      renderActiveWaveform();
    }

    function renderActiveWaveform() {
      const select = document.getElementById('waveform-case-select');
      const idx = parseInt(select.value, 10);
      const display = document.getElementById('waveform-display');
      if (isNaN(idx) || !gLastWaveformData[idx]) {
        display.innerHTML = '<p style="color:var(--text-muted); padding:2rem; text-align:center;">No waveform data for this selection.</p>';
        return;
      }
      const wave = gLastWaveformData[idx];
      const steps = wave.steps || [];
      if (steps.length === 0) {
        display.innerHTML = '<p style="color:var(--text-muted); padding:2rem; text-align:center;">Empty steps.</p>';
        return;
      }

      // Collect all signal keys
      const inKeys = Object.keys(steps[0].inputs || {});
      const outKeys = Object.keys(steps[0].expected || {});

      let html = `<div style="margin-bottom:0.75rem; font-size:0.9rem;">
        <strong>Case:</strong> ${wave.case_id} | <strong>Status:</strong> ${wave.passed ? '<span class="badge badge-pass">PASS</span>' : '<span class="badge badge-fail">DIVERGED</span>'}
      </div>`;

      // Header row
      html += '<div class="waveform-timeline"><div class="sig-label">SIGNAL / STEP</div>';
      steps.forEach((s, sIdx) => {
        const dtLabel = s.dt_ms !== null && s.dt_ms !== undefined ? `+${s.dt_ms}ms` : `#${sIdx}`;
        html += `<div style="text-align:center; font-size:0.7rem; color:var(--text-muted);">${dtLabel}</div>`;
      });
      html += '</div>';

      // Inputs
      inKeys.forEach(k => {
        html += `<div class="waveform-signal"><div class="sig-label" title="${k}">IN: ${k}</div>`;
        steps.forEach(s => {
          const val = s.inputs ? s.inputs[k] : '';
          const isBool = typeof val === 'boolean';
          const cls = isBool ? (val ? 'true' : 'false') : '';
          html += `<div class="sig-cell ${cls}">${val}</div>`;
        });
        html += '</div>';
      });

      // Expected outputs
      outKeys.forEach(k => {
        html += `<div class="waveform-signal"><div class="sig-label" style="color:#a5b4fc;" title="${k}">EXP: ${k}</div>`;
        steps.forEach(s => {
          const val = s.expected ? s.expected[k] : '';
          const isBool = typeof val === 'boolean';
          const cls = isBool ? (val ? 'true' : 'false') : '';
          html += `<div class="sig-cell ${cls}">${val}</div>`;
        });
        html += '</div>';
      });

      // Observed outputs
      outKeys.forEach(k => {
        html += `<div class="waveform-signal"><div class="sig-label" style="color:var(--amber);" title="${k}">OBS: ${k}</div>`;
        steps.forEach(s => {
          const val = s.observed ? s.observed[k] : '(unexec)';
          const isMismatch = s.divergence && s.divergence.field === k;
          let cls = '';
          if (s.observed === null || s.observed === undefined) {
            cls = 'unexecuted';
          } else if (isMismatch) {
            cls = 'mismatch';
          } else if (typeof val === 'boolean') {
            cls = val ? 'true' : 'false';
          }
          html += `<div class="sig-cell ${cls}">${val}</div>`;
        });
        html += '</div>';
      });

      display.innerHTML = html;
    }

    async function exportFormalVerify() {
      if (!gCurrentTask) return;
      const taskId = gCurrentTask.task.id;
      const code = document.getElementById('st-source-code').value;
      const consoleBox = document.getElementById('sandbox-console');

      consoleBox.textContent = `[EXPORT VERIFY ${taskId}] Generating nuXmv / UPPAAL verification bundle...\\n`;
      try {
        const res = await fetch('/api/export-verify', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ task_id: taskId, candidate: code })
        });
        const data = await res.json();
        consoleBox.textContent = `--- VERIFICATION BUNDLE EXPORTED ---\\nStatus: ${data.status}\\nDirectory: ${data.bundle_dir}\\n\\nManifest:\\n${JSON.stringify(data.manifest, null, 2)}\\n\\nCandidate ST:\\n${data.candidate_st}\\n\\nSpec LTL:\\n${data.spec_ltl}`;
      } catch (err) {
        consoleBox.textContent += `\\nExport error: ${err.message}`;
      }
    }

    async function loadTraceDetails() {
      try {
        const res = await fetch('/api/experiments');
        const data = await res.json();
        console.log("Experiments loaded:", data);
      } catch (err) {
        console.error("Failed to load experiments", err);
      }
    }

    // Init
    window.addEventListener('DOMContentLoaded', () => {
      reloadTasks();
    });
  </script>
</body>
</html>
"""


class WebUIRequestHandler(http.server.BaseHTTPRequestHandler):
    """Custom HTTP handler dispatching static HTML UI and REST API."""

    def __init__(self, *args, settings: Settings, backend: Backend | None = None, **kwargs) -> None:
        self.settings = settings
        self.backend = backend
        super().__init__(*args, **kwargs)

    def log_message(self, format: str, *args) -> None:
        # Suppress routine log messages during automated testing
        pass

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html", "/index.htm"):
            html = render_index_html()
            encoded = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return

        if parsed.path.startswith("/api/"):
            query = urllib.parse.parse_qs(parsed.query)
            status, data = handle_api_request("GET", parsed.path, query, None, self.settings, backend=self.backend)
            body_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body_bytes)))
            self.end_headers()
            self.wfile.write(body_bytes)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith("/api/"):
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length) if length > 0 else b"{}"
            try:
                body = json.loads(raw_body.decode("utf-8")) if raw_body else {}
            except Exception:
                body = None

            query = urllib.parse.parse_qs(parsed.query)
            status, data = handle_api_request("POST", parsed.path, query, body, self.settings, backend=self.backend)
            body_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body_bytes)))
            self.end_headers()
            self.wfile.write(body_bytes)
            return

        self.send_response(404)
        self.end_headers()


def serve_webui(
    host: str = "127.0.0.1",
    port: int = 8765,
    settings: Settings | None = None,
    stop_event: threading.Event | None = None,
    bound_port_box: list[int] | None = None,
) -> None:
    """Run interactive Auto-Testing & Waveform Trace Inspector Web server."""
    cfg = settings or Settings.load()

    def handler_factory(*args, **kwargs):
        return WebUIRequestHandler(*args, settings=cfg, **kwargs)

    server = http.server.HTTPServer((host, port), handler_factory)
    actual_port = server.server_port
    if bound_port_box is not None and len(bound_port_box) > 0:
        bound_port_box[0] = actual_port

    if stop_event is not None:
        server.timeout = 0.2
        while not stop_event.is_set():
            server.handle_request()
        server.server_close()
    else:
        print(f"🚀 CODESYS STAR v2 WebUI running at http://{host}:{actual_port}/")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
