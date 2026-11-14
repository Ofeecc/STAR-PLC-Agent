"""Minimal MCP stdio compiler & simulation tool for unmodified baselines.
The controller owns task/attempt budget; tool input can supply source and cases.
Stdout is exclusively JSON-RPC. No API key is needed by this process.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path

from .common import digest, read_json, write_json
from .compiler import compile_st, normalize_candidate
from .config import Settings
from .formal_verify import verify_candidate
from .selftest import validate_self_tests
from .st_verifier import sanitize_counterexamples_for_agent
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

VERIFY_SCHEMA = {
    "type": "object",
    "properties": {
        "source": CANDIDATE_SCHEMA,
        "assertions": {
            "type": "array",
            "items": {"type": "object"},
            "description": "Optional temporal/invariant assertions ({id, formula}) over declared port names.",
        },
    },
    "required": ["source"],
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
                        f"Simulate FB_Task against test cases. At most {settings.max_simulations} simulation attempts."
                    ),
                    "inputSchema": SIMULATE_SCHEMA,
                },
                {
                    "name": "verify_st",
                    "description": (
                        "Formally verify FB_Task against the task's LTL/INVAR specification "
                        "using ST->SMV symbolic compilation and NuSMV/nuXmv. "
                        "Returns PASS, COUNTEREXAMPLE (with offending scan trace), UNSUPPORTED_ST, TIMEOUT, or TOOL_ERROR."
                    ),
                    "inputSchema": VERIFY_SCHEMA,
                },
            ]
        }
    if method == "tools/call":
        params = message.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "compile_st":
            records = sorted(trusted.glob("compile_*/compile_result.json"))
            if settings.max_repairs >= 0 and len(records) >= settings.max_repairs + 1:
                return {
                    "content": [{"type": "text", "text": "Compilation budget exhausted"}],
                    "isError": True,
                }
            run_dir = trusted / f"compile_{len(records):02d}"
            source = args.get("source")
            if backend is not None:
                result = backend.compile(task, source, run_dir)
            else:
                result = compile_st(task, source, run_dir, settings)
            res_dict = asdict(result) if is_dataclass(result) else result
            write_json(run_dir / "compile_result.json", res_dict)
            cand_to_write = (
                source if isinstance(source, dict) else {"declaration": "", "implementation": str(source or "")}
            )
            write_json(run_dir / "candidate.json", cand_to_write)
            return {
                "content": [{"type": "text", "text": json.dumps(res_dict)}],
                "isError": False,
            }

        if tool_name == "simulate_st":
            records = sorted(trusted.glob("sim_*/simulation_result.json"))
            if settings.max_simulations > 0 and len(records) >= settings.max_simulations:
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

            # Quota parity (Scheme A): pre-compile uncompiled/edited source inside run_dir
            # without touching trusted/compile_* so compile_st quota is never consumed.
            try:
                cand_digest = digest(normalize_candidate(source))
            except Exception:
                cand_digest = digest(str(source))

            already_compiled = False
            for comp_file in sorted(trusted.glob("compile_*/compile_result.json")):
                try:
                    comp_data = read_json(comp_file)
                    if not comp_data.get("success"):
                        continue
                    cand_file = comp_file.parent / "candidate.json"
                    cand_data = read_json(cand_file) if cand_file.is_file() else None
                    if comp_data.get("source_sha256") == cand_digest or (
                        isinstance(cand_data, dict) and digest(normalize_candidate(cand_data)) == cand_digest
                    ):
                        already_compiled = True
                        break
                except Exception:
                    pass
            if not already_compiled:
                for pre_file in sorted(trusted.glob("sim_*/precompile_ok.json")):
                    try:
                        if read_json(pre_file).get("source_sha256") == cand_digest:
                            already_compiled = True
                            break
                    except Exception:
                        pass

            if not already_compiled:
                pre_dir = run_dir / "precompile"
                if backend is not None:
                    pre_comp = backend.compile(task, source, pre_dir)
                else:
                    pre_comp = compile_st(task, source, pre_dir, settings)
                pre_dict = asdict(pre_comp) if is_dataclass(pre_comp) else pre_comp
                if not pre_dict.get("success"):
                    fail_payload = {
                        "status": pre_dict.get("status", "COMPILE_FAIL"),
                        "success": False,
                        "passed_cases": 0,
                        "evaluated_cases": 0,
                        "failures": [],
                        "diagnostics": pre_dict.get("diagnostics", []),
                        "infrastructure_error": pre_dict.get("infrastructure_error"),
                    }
                    write_json(run_dir / "simulation_result.json", fail_payload)
                    return {
                        "content": [{"type": "text", "text": json.dumps(fail_payload)}],
                        "isError": False,
                    }
                write_json(run_dir / "precompile_ok.json", {"source_sha256": cand_digest})

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

        if tool_name == "verify_st":
            records = sorted(trusted.glob("verify_*/verification_result.json"))
            max_ver = getattr(settings, "max_verifications", 3)
            if max_ver > 0 and len(records) >= max_ver:
                return {
                    "content": [{"type": "text", "text": "Formal verification budget exhausted"}],
                    "isError": True,
                }
            run_dir = trusted / f"verify_{len(records):02d}"
            source = args.get("source")
            spec_vis = getattr(settings, "spec_visible", True)
            view = agent_view(task, spec_visible=spec_vis)
            extra_assertions = args.get("assertions") if isinstance(args.get("assertions"), list) else None
            full_res = verify_candidate(
                task=view,
                candidate=source,
                out_dir=run_dir,
                include_expected_observer=False,
                use_observer_smv=False,
                extra_assertions=extra_assertions,
            )
            # Zero-leakage response returned to the agent: strip observer_vars and internal file paths
            ver_status = full_res.get("status")
            ver_reason = str(full_res.get("reason") or "")
            guidance = None
            if ver_status == "UNSUPPORTED_ST":
                if "Conditional or looped invocation" in ver_reason:
                    guidance = (
                        "Refactor stateful FUNCTION_BLOCK calls so each instance is invoked unconditionally "
                        "once per scan and pass branch logic via input pins (e.g., IN := cond), or rely on compile_st/simulate_st."
                    )
                else:
                    guidance = (
                        "ST construct is outside the bounded symbolic verifier fragment (not a bug verdict). "
                        "Use compile_st and simulate_st to validate this candidate."
                    )
            elif ver_status == "INCONCLUSIVE":
                guidance = (
                    "Model checker returned UNKNOWN on at least one property (inconclusive, neither proven nor falsified). "
                    "Inspect unknown_property_ids and validate with compile_st and simulate_st."
                )
            elif ver_status in ("TIMEOUT", "TOOL_ERROR"):
                guidance = (
                    f"Verification infrastructure stopped with {ver_status} (not a bug verdict). "
                    "Use compile_st and simulate_st to validate behavior."
                )

            agent_payload = {
                "status": ver_status,
                "verified": full_res.get("verified", False),
                "total_properties": full_res.get("total_properties", 0),
                "passed_properties": full_res.get("passed_properties", 0),
                "failed_properties": full_res.get("failed_properties", 0),
                "unknown_properties": full_res.get("unknown_properties", 0),
                "property_pass_ratio": full_res.get("property_pass_ratio"),
                "failed_property_ids": [
                    pr.get("id") for pr in (full_res.get("property_results") or []) if pr.get("holds") is False
                ],
                "unknown_property_ids": [
                    pr.get("id") for pr in (full_res.get("property_results") or []) if pr.get("holds") is None
                ],
                "counterexamples": sanitize_counterexamples_for_agent(full_res.get("counterexamples") or []),
                "reason": full_res.get("reason"),
                "guidance": guidance,
            }
            return {
                "content": [{"type": "text", "text": json.dumps(agent_payload)}],
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
