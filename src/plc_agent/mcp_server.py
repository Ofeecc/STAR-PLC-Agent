"""Minimal MCP stdio compiler tool for the unmodified Codex baseline.
The controller owns task/attempt budget; tool input can supply source only.
Stdout is exclusively JSON-RPC. No API key is needed by this process.
"""
from __future__ import annotations
import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from .common import read_json, write_json
from .compiler import compile_st
from .config import Settings

CANDIDATE_SCHEMA = {"type": "object", "properties": {
    "declaration": {"type": "string"}, "implementation": {"type": "string"},
    "supporting_objects": {"type": "array", "items": {"type": "object"}}},
    "required": ["declaration", "implementation"], "additionalProperties": False}

def dispatch(message, task, trusted, settings):
    method = message.get("method")
    if method == "initialize":
        return {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                "serverInfo": {"name": "plc-codesys-compiler", "version": "0.1.0"}}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": [{"name": "compile_st", "description":
            f"Compile FB_Task with the actual CODESYS compiler. At most {settings.max_repairs + 1} attempts including first pass.",
            "inputSchema": {"type": "object", "properties": {"source": CANDIDATE_SCHEMA}, "required": ["source"], "additionalProperties": False}}]}
    if method == "tools/call":
        params = message["params"]
        if params["name"] != "compile_st":
            raise ValueError("Unknown tool")
        records = sorted(trusted.glob("compile_*/compile_result.json"))
        if len(records) >= settings.max_repairs + 1:
            return {"content": [{"type": "text", "text": "Compilation budget exhausted"}], "isError": True}
        result = compile_st(task, params["arguments"]["source"], trusted / f"compile_{len(records):02d}", settings)
        return {"content": [{"type": "text", "text": json.dumps(asdict(result))}], "isError": False}
    raise ValueError("Unsupported method")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--trusted", required=True)
    parser.add_argument("--config")
    args = parser.parse_args()
    task, settings = read_json(args.task), Settings.load(args.config, load_api=False)
    trusted = Path(args.trusted)
    trusted.mkdir(parents=True, exist_ok=True)
    for line in sys.stdin:
        message = {}
        try:
            message = json.loads(line)
            if "id" not in message:
                continue
            result = dispatch(message, task, trusted, settings)
            response = {"jsonrpc": "2.0", "id": message["id"], "result": result}
        except Exception as exc:
            response = {"jsonrpc": "2.0", "id": message.get("id"), "error": {"code": -32603,
                "message": f"{type(exc).__name__}: {exc}"}}
        print(json.dumps(response), flush=True)

if __name__ == "__main__":
    main()
