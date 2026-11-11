"""CODESYS STAR v2 Auto-Testing & Waveform Agent Trace Inspector Web Platform.

Provides a standalone zero-dependency HTTP server with a rich single-page application
for exploring tasks, visualizing logic waveforms, inspecting agent traces,
and testing/verifying ST programs.
"""
from __future__ import annotations

import contextlib
import dataclasses
import http.server
import json
import tempfile
import threading
import urllib.parse
import uuid
from pathlib import Path
from typing import Any

from .backend import Backend, CodesysBackend, FakeBackend, SimResult
from .common import ROOT, digest, read_json
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
        raw_steps = raw_case.get("steps", []) if isinstance(raw_case, dict) else raw_case

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
                        "observed": None,
                        "dt_ms": dt_ms,
                        "match": None,
                        "divergence": None,
                    })
                elif step_idx == case_fail.first_bad_step:
                    obs = {case_fail.field: case_fail.observed}
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
                    "observed": None,
                    "dt_ms": dt_ms,
                    "match": None,
                    "divergence": None,
                })

        waveforms.append({
            "case_id": case_id,
            "name": case_name,
            "passed": False if case_fail else (True if raw_steps and sim_res.status == "PASS" else None),
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

    review_path = ROOT / 'configs/pilot_review.json'
    pilot_items = read_json(review_path).get('tasks', []) if review_path.is_file() else []
    all_review_path = ROOT / 'configs/task_review_zh.json'
    review_items = read_json(all_review_path).get('tasks', []) if all_review_path.is_file() else pilot_items
    review_by_id = {r['id']: r for r in review_items}

    if method == 'POST' and path == '/api/check-reference-model':
        # Fixed local model only: never execute a browser-supplied path or command.
        if not isinstance(body, dict) or body.get('task_id') != 'PUB001':
            return 400, {'error': 'Only the explicitly encoded PUB001 reference model is available'}
        from .model_checker import check_model
        output = ROOT / '.local/model_checker_evidence' / uuid.uuid4().hex
        try:
            result = check_model(ROOT / 'models/PUB001_reference.smv', output)
        except (ValueError, OSError) as exc:
            return 503, {'status': 'TOOL_ERROR', 'error': str(exc)}
        result['stdout'] = (output / 'stdout.txt').read_text(encoding='utf-8')
        result['stderr'] = (output / 'stderr.txt').read_text(encoding='utf-8')
        result['evidence_dir'] = str(output)
        return 200, result

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
                "steps_count": sum(len(c.get("steps", [])) for c in t.get("tests", [])),
                "properties_count": len(t.get("ltl", [])),
            }
            for t in tasks
        ]
        return 200, {"tasks": task_list, "total": len(task_list), "pilot_review": pilot_items, "task_review": review_items}

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
        review = review_by_id.get(task_id)
        if review:
            review = dict(review, source_matches=review.get('source_task_sha256') == digest(task))
        return 200, {
            "task": task,
            "agent_view": agent_view(task),
            "tests": task.get("tests", []),
            "random_cases": rand_cases,
            "review": review,
            "task_sha256": digest(task),
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
                return 503, {"error": "CODESYS is not configured; candidate execution was not performed", "status": "UNVERIFIED"}

        with contextlib.nullcontext(ROOT / ".local" / "webui_evidence" / uuid.uuid4().hex) as tmpdir:
            workspace = Path(tmpdir)
            compile_res = backend.compile(task, candidate, workspace / "compile")

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
                sim_res = backend.simulate(task, candidate, cases, workspace / "simulate")
                waveform = _build_step_waveforms(task, cases, sim_res, workspace / "simulate")

            return 200, {
                "evidence_workspace": str(workspace),
                "execution_kind": "FAKE_REFERENCE_ONLY" if isinstance(backend, FakeBackend) else "CODESYS",
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
    """Inline local assets so the reviewer UI has no CDN/network dependencies."""
    assets = Path(__file__).parent / "webui_assets"
    html = (assets / "index.html").read_text(encoding="utf-8")
    script = (assets / "app.js").read_text(encoding="utf-8")
    return html.replace("/*__APP_SCRIPT__*/", script)


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
