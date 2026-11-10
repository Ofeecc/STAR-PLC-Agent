"""Minimal MCP stdio compiler & simulation tool for unmodified baselines.
The controller owns task/attempt budget; tool input can supply source and cases.
Stdout is exclusively JSON-RPC. No API key is needed by this process.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
import json
from pathlib import Path
import sys

from .common import read_json, write_json
from .compiler import compile_st
from .config import Settings
from .selftest import validate_self_tests
from .task_view import agent_view

CANDIDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "declaration": {"type": "string"},
        "implementation": {"type": "string"},
        "supporting_objects": {"type": "array", "items": {"type": "object"}},
    },
    "required": ["declaration", "implementation"],
    "additionalProperties": False,
}

SIMULATE_SCHEMA = {
    "type": "object",
    "properties": {
        "source": CANDIDATE_SCHEMA,
        "cases": {
            "type": "array",
            "items": {"type": "object"},
            "description": "List of test cases with steps (inputs, expected, optional dt_ms)",
        },
    },
    "required": ["source", "cases"],
    "additionalProperties": False,
}


def dispatch(message: dict, task: dict, trusted: Path, settings: Settings, backend=None) -> dict:
    trusted = Path(trusted)
    method = message.get("method")
    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "plc-codesys-tools", "version": "0.2.0"},
        }
    if method == "ping":
        return {}
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "compile_st",
                    "description": (
                        f"Compile FB_Task with the actual CODESYS compiler. "
                        f"At most {settings.max_repairs + 1} attempts including first pass."
                    ),
                    "inputSchema": {
                        "type": "object",
                        "properties": {"source": CANDIDATE_SCHEMA},
                        "required": ["source"],
                        "additionalProperties": False,
                    },
                },
                {
                    "name": "simulate_st",
                    "description": (
                        f"Simulate FB_Task against test cases. "
                        f"At most {settings.max_simulations} simulation attempts."
                    ),
                    "inputSchema": SIMULATE_SCHEMA,
                },
            ]
        }
    if method == "tools/call":
        params = message.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "compile_st":
            records = sorted(trusted.glob("compile_*/compile_result.json"))
            if len(records) >= settings.max_repairs + 1:
                return {
                    "content": [{"type": "text", "text": "Compilation budget exhausted"}],
                    "isError": True,
                }
            run_dir = trusted / f"compile_{len(records):02d}"
            run_dir.mkdir(parents=True, exist_ok=True)
            source = args.get("source")
            if backend is not None:
                result = backend.compile(task, source, run_dir)
            else:
                result = compile_st(task, source, run_dir, settings)
            res_dict = asdict(result) if is_dataclass(result) else result
            write_json(run_dir / "compile_result.json", res_dict)
            cand_to_write = source if isinstance(source, dict) else {"declaration": "", "implementation": str(source or "")}
            write_json(run_dir / "candidate.json", cand_to_write)
            return {
                "content": [{"type": "text", "text": json.dumps(res_dict)}],
                "isError": False,
            }

        if tool_name == "simulate_st":
            records = sorted(trusted.glob("sim_*/simulation_result.json"))
            if len(records) >= settings.max_simulations:
                return {
                    "content": [{"type": "text", "text": "Simulation budget exhausted"}],
                    "isError": True,
                }
            raw_cases = args.get("cases")
            valid_cases = validate_self_tests(agent_view(task), raw_cases) if raw_cases else []
            if not valid_cases:
                return {
                    "content": [{"type": "text", "text": "Invalid or empty test cases"}],
                    "isError": True,
                }
            run_dir = trusted / f"sim_{len(records):02d}"
            run_dir.mkdir(parents=True, exist_ok=True)
            source = args.get("source")
            if backend is not None:
                res = backend.simulate(task, source, valid_cases, run_dir)
            else:
                from .backend import CodesysBackend
                res = CodesysBackend(settings).simulate(task, source, valid_cases, run_dir)
            res_dict = asdict(res) if is_dataclass(res) else res
            write_json(run_dir / "simulation_result.json", res_dict)
            return {
                "content": [{"type": "text", "text": json.dumps(res_dict)}],
                "isError": False,
            }

        raise ValueError(f"Unknown tool: {tool_name}")

    raise ValueError(f"Unsupported method: {method}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--trusted", required=True)
    parser.add_argument("--config")
    args = parser.parse_args()
    task = read_json(args.task)
    settings = Settings.load(args.config, load_api=False)
    trusted = Path(args.trusted)
    trusted.mkdir(parents=True, exist_ok=True)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        message = {}
        try:
            message = json.loads(line)
            if "id" not in message:
                continue
            result = dispatch(message, task, trusted, settings)
            response = {"jsonrpc": "2.0", "id": message["id"], "result": result}
        except Exception as exc:
            response = {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {"code": -32603, "message": f"{type(exc).__name__}: {exc}"},
            }
        print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
