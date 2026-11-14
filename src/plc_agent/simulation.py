"""Actual CODESYS IDE simulation for fixed and timed scan traces.

Each test gets a separate fresh FB instance. An editable PLC_PRG sequencer
assigns fixed inputs, invokes the generated FB exactly once per task scan,
and copies actual sampled inputs and outputs to typed trace arrays. Expected
outputs never appear in the generated test program.
"""

from __future__ import annotations

import hashlib
import math
import os
import re
import shutil
import subprocess
import time
import uuid
from pathlib import Path

from .common import ROOT, digest, now, read_json, write_json
from .compiler import _kill_tree, codesys_command, normalize_candidate, stage_ascii_workspace, sync_ascii_artifacts

SCALAR_TYPES = {
    "BOOL",
    "BYTE",
    "WORD",
    "DWORD",
    "LWORD",
    "SINT",
    "INT",
    "DINT",
    "LINT",
    "USINT",
    "UINT",
    "UDINT",
    "ULINT",
    "REAL",
    "LREAL",
}
INTEGER_TYPES = SCALAR_TYPES - {"BOOL", "REAL", "LREAL"}
TIME_TYPES = {"TIME", "LTIME"}


def get_struct_defs(task: dict | None = None) -> dict[str, dict[str, str]]:
    defs: dict[str, dict[str, str]] = {
        "ST_Recipe": {
            "recipeID": "INT",
            "ingredientType": "INT",
            "ingredientRatio": "REAL",
            "productionTemperature": "REAL",
        },
        "ST_Pump": {
            "priority": "INT",
            "selection": "BOOL",
            "RunComd": "BOOL",
        },
        "ST_AnalogChannel": {
            "enable": "BOOL",
            "hiLIM": "REAL",
            "loLIM": "REAL",
            "bipolar": "BOOL",
            "measuringMode": "INT",
            "retVal": "WORD",
            "outputValue": "REAL",
        },
    }
    if not task:
        return defs
    for dt_name, dt_info in (task.get("data_types") or {}).items():
        if isinstance(dt_info, dict) and dt_info.get("kind") == "STRUCT":
            fields = {f["name"]: f["type"] for f in dt_info.get("fields", [])}
            defs[dt_name] = fields
    for st in task.get("supporting_types") or []:
        decl = st.get("declaration", "")
        m = re.search(r"STRUCT\s+(.*?)\s+END_STRUCT", decl, re.DOTALL | re.IGNORECASE)
        if m:
            fields = {}
            for line in m.group(1).splitlines():
                line = line.strip().rstrip(";")
                if ":" in line:
                    fname, ftype = line.split(":", 1)
                    fields[fname.strip()] = ftype.strip()
            defs[st["name"]] = fields
    return defs


def is_array_type(type_name: str) -> bool:
    return bool(re.fullmatch(r"ARRAY\s*\[.+\]\s+OF\s+.+", type_name.strip(), re.IGNORECASE))


def parse_array_type(type_name: str) -> tuple[int | None, int | None, str]:
    m = re.fullmatch(
        r"ARRAY\s*\[\s*(\*|-?\d+)\s*(?:\.\.\s*(-?\d+))?\s*\]\s+OF\s+(.+)", type_name.strip(), re.IGNORECASE
    )
    if not m:
        raise ValueError(f"Invalid array type: {type_name}")
    low_s, high_s, elem_t = m.group(1), m.group(2), m.group(3).strip()
    if low_s == "*":
        return None, None, elem_t
    return int(low_s), int(high_s), elem_t


def supported_type(type_name: str, task: dict | None = None) -> bool:
    val = type_name.strip()
    up = val.upper()
    if up in SCALAR_TYPES or up in TIME_TYPES or up == "VARIANT":
        return True
    if bool(re.fullmatch(r"STRING(\([1-9][0-9]*\))?", up)):
        return True
    if is_array_type(val):
        _, _, elem_t = parse_array_type(val)
        return supported_type(elem_t, task)
    sdefs = get_struct_defs(task)
    if val in sdefs or up in sdefs:
        return True
    return False


def eligibility(task: dict, cases: list[dict] | None = None) -> list[str]:
    reasons = []
    if cases is None:
        cases = task.get("tests", [])
    for field in task.get("interface", []):
        if not supported_type(field["type"], task):
            reasons.append("Unsupported automatic monitoring type: " + field["type"])
    return sorted(set(reasons))


def st_literal(value: object, type_name: str, task: dict | None = None) -> str:
    typ = type_name.strip()
    up = typ.upper()
    if up == "BOOL":
        if not isinstance(value, bool):
            raise ValueError("BOOL input requires a JSON Boolean")
        return "TRUE" if value else "FALSE"
    if up in INTEGER_TYPES:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("Integer input requires a JSON integer")
        return up + "#" + str(value)
    if up in ("REAL", "LREAL"):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
            raise ValueError("Real input must be finite")
        text_val = repr(float(value))
        return up + "#" + text_val
    if up.startswith("STRING"):
        if not isinstance(value, str):
            raise ValueError("STRING input requires a string")
        escaped = value.replace("$", "$$").replace("'", "$'").replace("\r", "$R").replace("\n", "$N")
        return "'" + escaped + "'"
    if up in TIME_TYPES:
        if isinstance(value, str):
            v_up = value.strip().upper()
            if v_up.startswith("T#") or v_up.startswith("TIME#") or v_up.startswith("LTIME#"):
                return value.strip()
            return f"{up}#{value.strip()}"
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return f"{up}#{int(value)}ms"
        raise ValueError(f"Invalid {up} input: {value!r}")
    if is_array_type(typ):
        if not isinstance(value, list):
            raise ValueError("Array input requires a list")
        _, _, elem_t = parse_array_type(typ)
        return "[" + ", ".join(st_literal(elem, elem_t, task) for elem in value) + "]"
    sdefs = get_struct_defs(task)
    if typ in sdefs or up in sdefs:
        if not isinstance(value, dict):
            raise ValueError(f"Struct input requires a dict for {typ}")
        fields = sdefs.get(typ) or sdefs.get(up)
        parts = []
        for k, v in value.items():
            if k in fields:
                parts.append(f"{k} := {st_literal(v, fields[k], task)}")
        return "(" + ", ".join(parts) + ")"
    raise ValueError("Unsupported test input type: " + type_name)


def generate_assignments(lhs: str, value: object, type_name: str, task: dict | None = None) -> list[str]:
    typ = type_name.strip()
    up = typ.upper()
    if is_array_type(typ):
        if not isinstance(value, list):
            raise ValueError(f"Expected list for array {lhs}")
        low, high, elem_t = parse_array_type(typ)
        if low is None:
            low = 1
        lines = []
        for idx, item in enumerate(value):
            elem_idx = low + idx
            lines.extend(generate_assignments(f"{lhs}[{elem_idx}]", item, elem_t, task))
        return lines
    sdefs = get_struct_defs(task)
    if typ in sdefs or up in sdefs:
        if not isinstance(value, dict):
            raise ValueError(f"Expected dict for struct {lhs}")
        fields = sdefs.get(typ) or sdefs.get(up)
        lines = []
        for fname, ftype in fields.items():
            if fname in value:
                lines.extend(generate_assignments(f"{lhs}.{fname}", value[fname], ftype, task))
        return lines
    return [f"{lhs} := {st_literal(value, typ, task)};"]


def get_case_inouts(task: dict, case_index: int, case: dict) -> dict[str, dict]:
    res = {}
    for f in task.get("interface", []):
        if f["direction"] != "IN_OUT":
            continue
        vname = f["name"]
        step0_in = case["steps"][0]["inputs"].get(vname)
        if isinstance(step0_in, dict) and "$binding" in step0_in:
            bid = step0_in.get("binding_id")
            retain = step0_in.get("retain_storage", False)
            t_bindings = task.get("test_bindings", {})
            if isinstance(t_bindings, dict) and vname in t_bindings:
                b_info = t_bindings[vname]
                res[vname] = {
                    "type": b_info.get("type", f["type"]),
                    "initial": b_info.get("initial"),
                    "retain_storage": retain,
                }
            elif isinstance(t_bindings, list):
                match = next((b for b in t_bindings if b.get("id") == bid), None)
                if match:
                    res[vname] = {
                        "type": match.get(f"{vname}_type", f["type"]),
                        "initial": match.get(f"{vname}_initial"),
                        "retain_storage": retain,
                    }
        else:
            if f["type"] == "VARIANT":
                buf_in = case["steps"][0]["inputs"].get("buffer")
                bid = buf_in.get("binding_id") if isinstance(buf_in, dict) else None
                match = next((b for b in task.get("test_bindings", []) if b.get("id") == bid), None)
                concrete_type = match.get(f"{vname}_type", "DINT") if match else "DINT"
                res[vname] = {
                    "type": concrete_type,
                    "initial": None,
                    "retain_storage": False,
                }
            elif "ARRAY[*]" in f["type"].upper():
                val = step0_in
                length = len(val) if isinstance(val, list) else 1
                _, _, elem_t = parse_array_type(f["type"])
                low = int(case.get("array_lower_bounds", {}).get(vname, 1))
                high = low + length - 1
                res[vname] = {
                    "type": f"ARRAY[{low}..{high}] OF {elem_t}",
                    "initial": None,
                    "retain_storage": False,
                    "lower_bound": low,
                }
            else:
                res[vname] = {
                    "type": f["type"],
                    "initial": None,
                    "retain_storage": False,
                }
    return res


def parse_value(raw: object, type_name: str) -> object:
    value = str(raw).strip().replace("_", "")
    typ = type_name.upper()
    if typ == "BOOL":
        if value.upper() in ("TRUE", "BOOL#TRUE", "1"):
            return True
        if value.upper() in ("FALSE", "BOOL#FALSE", "0"):
            return False
        raise RuntimeError("Unexpected BOOL representation: " + str(raw))
    if typ in ("TIME", "LTIME"):
        return str(raw).strip()
    if typ.startswith("STRING"):
        val_str = str(raw).strip()
        if len(val_str) >= 2 and val_str[0] == "'" and val_str[-1] == "'":
            val_str = val_str[1:-1]
        return val_str.replace("$N", "\n").replace("$R", "\r").replace("$'", "'").replace("$$", "$")
    if "#" in value:
        prefix, rest = value.split("#", 1)
        if prefix.upper() == typ:
            value = rest
    if typ in ("REAL", "LREAL"):
        return float(value)
    for marker, base in (("16#", 16), ("8#", 8), ("2#", 2)):
        if value.upper().startswith(marker):
            return int(value[len(marker) :], base)
    return int(value)


def unflatten_observations(program: dict, raw_values: dict[str, str]) -> list[dict]:
    def get_raw(expr: str) -> str | None:
        if expr in raw_values:
            return raw_values[expr]
        if expr.startswith("PLC_PRG."):
            short = expr[len("PLC_PRG.") :]
            if short in raw_values:
                return raw_values[short]
        else:
            long_expr = "PLC_PRG." + expr
            if long_expr in raw_values:
                return raw_values[long_expr]
        return None

    def resolve_item(spec: dict) -> object:
        kind = spec.get("kind")
        if kind == "raw":
            return spec["value"]
        if kind == "scalar":
            expr = spec["expr"]
            raw = get_raw(expr)
            if raw is None:
                raise KeyError(f"Missing raw monitoring value for expression: {expr}")
            return parse_value(raw, spec["type"])
        if kind == "array":
            return [resolve_item(elem) for elem in spec["elements"]]
        if kind == "struct":
            return {k: resolve_item(v) for k, v in spec["fields"].items()}
        raise ValueError(f"Unknown mapping kind: {kind}")

    observations = []
    for step_map in program.get("trace_mapping", []):
        row = {
            "index": step_map["step_index"],
            "inputs": {k: resolve_item(v) for k, v in step_map["inputs"].items()},
            "outputs": {k: resolve_item(v) for k, v in step_map["outputs"].items()},
        }
        if step_map.get("dt_expr"):
            dt_raw = get_raw(step_map["dt_expr"])
            if dt_raw is not None:
                row["dt_ms"] = parse_value(dt_raw, "UDINT")
        observations.append(row)
    return observations


def build_program(task: dict, cases: list[dict] | None = None) -> dict:
    if cases is None:
        cases = task["tests"]
    reasons = eligibility(task, cases=cases)
    if reasons:
        raise ValueError("; ".join(reasons))
    fields = task["interface"]
    for field in fields:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", field["name"]):
            raise ValueError("Unexpected IEC field identifier")
    inputs = [v for v in fields if v["direction"] == "INPUT"]
    outputs = [v for v in fields if v["direction"] == "OUTPUT"]
    in_outs = [v for v in fields if v["direction"] == "IN_OUT"]
    count = sum(len(case["steps"]) for case in cases)
    if count <= 0:
        raise ValueError("No fixed test steps")
    is_timed = any("dt_ms" in step for case in cases for step in case["steps"])
    sdefs = get_struct_defs(task)

    case_inouts_map = [get_case_inouts(task, c_idx, c) for c_idx, c in enumerate(cases)]

    declarations = [
        "PROGRAM PLC_PRG",
        "VAR",
        " BenchStep : UDINT := 0;",
        " BenchCalls : UDINT := 0;",
        " BenchDone : BOOL := FALSE;",
    ]
    if is_timed:
        declarations += [
            " BenchLastTime : TIME := T#0ms;",
            " BenchCurrentTime : TIME := T#0ms;",
            f" TraceDt : ARRAY[0..{count - 1}] OF UDINT;",
        ]
    declarations += [f" BenchUut{i} : FB_Task;" for i, _ in enumerate(cases)]

    # Caller-owned storage for each case
    for c_idx, cin in enumerate(case_inouts_map):
        for vname, binfo in cin.items():
            declarations.append(f" Binding_{c_idx}_{vname} : {binfo['type']};")

    # Trace arrays
    # 1. Inputs
    for field in inputs:
        ftyp = field["type"]
        fname = field["name"]
        if is_array_type(ftyp):
            low, high, elem_t = parse_array_type(ftyp)
            if low is None:
                low = 1
            max_len = max(len(c["steps"][0]["inputs"][fname]) for c in cases)
            for idx in range(max_len):
                declarations.append(f" TraceIn_{fname}_{low + idx} : ARRAY[0..{count - 1}] OF {elem_t};")
        elif ftyp in sdefs:
            for sfname, sftype in sdefs[ftyp].items():
                declarations.append(f" TraceIn_{fname}_{sfname} : ARRAY[0..{count - 1}] OF {sftype};")
        else:
            declarations.append(f" TraceIn_{fname} : ARRAY[0..{count - 1}] OF {ftyp};")

    # 2. Outputs (and IN_OUTs in expected)
    expected_fields = set(k for c in cases for s in c["steps"] for k in s.get("expected", {}).keys())
    for field in outputs:
        ftyp = field["type"]
        fname = field["name"]
        if is_array_type(ftyp):
            low, high, elem_t = parse_array_type(ftyp)
            if low is None:
                low = 1
            for elem_idx in range(low, high + 1):
                declarations.append(f" TraceOut_{fname}_{elem_idx} : ARRAY[0..{count - 1}] OF {elem_t};")
        elif ftyp in sdefs:
            for sfname, sftype in sdefs[ftyp].items():
                declarations.append(f" TraceOut_{fname}_{sfname} : ARRAY[0..{count - 1}] OF {sftype};")
        else:
            declarations.append(f" TraceOut_{fname} : ARRAY[0..{count - 1}] OF {ftyp};")

    for field in in_outs:
        fname = field["name"]
        if fname not in expected_fields:
            continue
        if fname == "item":
            declarations.append(f" TraceOut_item_DINT : ARRAY[0..{count - 1}] OF DINT;")
            declarations.append(f" TraceOut_item_BOOL : ARRAY[0..{count - 1}] OF BOOL;")
        elif fname == "pumpGroup":
            for idx in range(1, 6):
                for sfname, sftype in sdefs["ST_Pump"].items():
                    declarations.append(f" TraceOut_pumpGroup_{idx}_{sfname} : ARRAY[0..{count - 1}] OF {sftype};")
        elif fname == "analogValues":
            max_len = max(len(c["steps"][0]["inputs"]["analogValues"]) for c in cases)
            for idx in range(1, max_len + 1):
                declarations.append(f" TraceOut_analogValues_{idx} : ARRAY[0..{count - 1}] OF INT;")
        elif fname == "channels":
            max_len = max(len(c["steps"][0]["inputs"]["channels"]) for c in cases)
            for idx in range(1, max_len + 1):
                for sfname, sftype in sdefs["ST_AnalogChannel"].items():
                    declarations.append(f" TraceOut_channels_{idx}_{sfname} : ARRAY[0..{count - 1}] OF {sftype};")
        elif fname == "recipe":
            r_type = case_inouts_map[0]["recipe"]["type"]
            r_low, r_high, _ = parse_array_type(r_type)
            if r_low is None:
                r_low = 1
            for idx in range(r_low, r_high + 1):
                for sfname, sftype in sdefs["ST_Recipe"].items():
                    declarations.append(f" TraceOut_recipe_{idx}_{sfname} : ARRAY[0..{count - 1}] OF {sftype};")

    declarations.append("END_VAR")

    # Body
    body = ["IF NOT BenchDone THEN"]
    if is_timed:
        body.append(" BenchCurrentTime := TIME();")
    body.append(" CASE BenchStep OF")

    trace_expressions = []
    trace_mappings = []
    step_index = 0
    steps = []

    for case_index, case in enumerate(cases):
        instance = "BenchUut" + str(case_index)
        cin = case_inouts_map[case_index]
        for case_step, step in enumerate(case["steps"]):
            body.append(f" {step_index}:")
            step_map = {
                "step_index": step_index,
                "case_id": case["id"],
                "case_step": case_step,
                "dt_expr": f"PLC_PRG.TraceDt[{step_index}]" if is_timed else None,
                "inputs": {},
                "outputs": {},
            }
            indent = "   "
            if is_timed:
                step_dt = step.get("dt_ms", 0)
                body.append(f"  IF BenchStep = 0 OR (TIME() - BenchLastTime >= UDINT_TO_TIME({step_dt})) THEN")
                if step_index == 0:
                    body.append("   TraceDt[0] := 0;")
                else:
                    body.append(f"   TraceDt[{step_index}] := TIME_TO_UDINT(TIME() - BenchLastTime);")
                body.append("   BenchLastTime := TIME();")
                trace_expressions.append(f"PLC_PRG.TraceDt[{step_index}]")

            # 1. Caller storage initialization
            for vname, binfo in cin.items():
                b_var = f"Binding_{case_index}_{vname}"
                if binfo["retain_storage"]:
                    if case_step == 0 and binfo["initial"] is not None:
                        inits = generate_assignments(b_var, binfo["initial"], binfo["type"], task)
                        for line in inits:
                            body.append(indent + line)
                else:
                    if vname in step["inputs"]:
                        inits = generate_assignments(b_var, step["inputs"][vname], binfo["type"], task)
                        for line in inits:
                            body.append(indent + line)

            # 2. Assign regular inputs
            for field in inputs:
                fname = field["name"]
                if fname in step["inputs"]:
                    f_var = f"{instance}.{fname}"
                    lines = generate_assignments(f_var, step["inputs"][fname], field["type"], task)
                    for line in lines:
                        body.append(indent + line)

            # 3. Trace inputs
            for field in inputs:
                fname = field["name"]
                ftyp = field["type"]
                if is_array_type(ftyp):
                    low, high, elem_t = parse_array_type(ftyp)
                    if low is None:
                        low = 1
                    val = step["inputs"][fname]
                    elements = []
                    for idx in range(len(val)):
                        elem_idx = low + idx
                        tr_var = f"TraceIn_{fname}_{elem_idx}"
                        body.append(f"{indent}{tr_var}[{step_index}] := {instance}.{fname}[{elem_idx}];")
                        expr = f"PLC_PRG.{tr_var}[{step_index}]"
                        elements.append({"kind": "scalar", "expr": expr, "type": elem_t})
                        trace_expressions.append(expr)
                    step_map["inputs"][fname] = {"kind": "array", "elements": elements}
                elif ftyp in sdefs:
                    f_map = {}
                    for sfname, sftype in sdefs[ftyp].items():
                        tr_var = f"TraceIn_{fname}_{sfname}"
                        body.append(f"{indent}{tr_var}[{step_index}] := {instance}.{fname}.{sfname};")
                        expr = f"PLC_PRG.{tr_var}[{step_index}]"
                        f_map[sfname] = {"kind": "scalar", "expr": expr, "type": sftype}
                        trace_expressions.append(expr)
                    step_map["inputs"][fname] = {"kind": "struct", "fields": f_map}
                else:
                    tr_var = f"TraceIn_{fname}"
                    body.append(f"{indent}{tr_var}[{step_index}] := {instance}.{fname};")
                    expr = f"PLC_PRG.{tr_var}[{step_index}]"
                    step_map["inputs"][fname] = {"kind": "scalar", "expr": expr, "type": ftyp}
                    trace_expressions.append(expr)

            # Map IN_OUT inputs
            for field in in_outs:
                vname = field["name"]
                if vname in step["inputs"]:
                    step_map["inputs"][vname] = {"kind": "raw", "value": step["inputs"][vname]}

            # 4. Invoke FB
            if cin:
                args = ", ".join(f"{vname} := Binding_{case_index}_{vname}" for vname in cin)
                body.append(f"{indent}{instance}({args});")
            else:
                body.append(f"{indent}{instance}();")

            # 5. Trace outputs
            for field in outputs:
                fname = field["name"]
                ftyp = field["type"]
                if is_array_type(ftyp):
                    low, high, elem_t = parse_array_type(ftyp)
                    if low is None:
                        low = 1
                    elements = []
                    for elem_idx in range(low, high + 1):
                        tr_var = f"TraceOut_{fname}_{elem_idx}"
                        body.append(f"{indent}{tr_var}[{step_index}] := {instance}.{fname}[{elem_idx}];")
                        expr = f"PLC_PRG.{tr_var}[{step_index}]"
                        elements.append({"kind": "scalar", "expr": expr, "type": elem_t})
                        trace_expressions.append(expr)
                    step_map["outputs"][fname] = {"kind": "array", "elements": elements}
                elif ftyp in sdefs:
                    f_map = {}
                    for sfname, sftype in sdefs[ftyp].items():
                        tr_var = f"TraceOut_{fname}_{sfname}"
                        body.append(f"{indent}{tr_var}[{step_index}] := {instance}.{fname}.{sfname};")
                        expr = f"PLC_PRG.{tr_var}[{step_index}]"
                        f_map[sfname] = {"kind": "scalar", "expr": expr, "type": sftype}
                        trace_expressions.append(expr)
                    step_map["outputs"][fname] = {"kind": "struct", "fields": f_map}
                else:
                    tr_var = f"TraceOut_{fname}"
                    body.append(f"{indent}{tr_var}[{step_index}] := {instance}.{fname};")
                    expr = f"PLC_PRG.{tr_var}[{step_index}]"
                    step_map["outputs"][fname] = {"kind": "scalar", "expr": expr, "type": ftyp}
                    trace_expressions.append(expr)

            # Trace IN_OUT outputs (if in expected_fields)
            for field in in_outs:
                fname = field["name"]
                if fname not in expected_fields:
                    continue
                if fname == "item":
                    itype = cin["item"]["type"]
                    tr_var = f"TraceOut_item_{itype}"
                    body.append(f"{indent}{tr_var}[{step_index}] := Binding_{case_index}_item;")
                    expr = f"PLC_PRG.{tr_var}[{step_index}]"
                    step_map["outputs"]["item"] = {"kind": "scalar", "expr": expr, "type": itype}
                    trace_expressions.append(expr)
                elif fname == "pumpGroup":
                    elements = []
                    for idx in range(1, 6):
                        s_map = {}
                        for sfname, sftype in sdefs["ST_Pump"].items():
                            tr_var = f"TraceOut_pumpGroup_{idx}_{sfname}"
                            body.append(
                                f"{indent}{tr_var}[{step_index}] := Binding_{case_index}_pumpGroup[{idx}].{sfname};"
                            )
                            expr = f"PLC_PRG.{tr_var}[{step_index}]"
                            s_map[sfname] = {"kind": "scalar", "expr": expr, "type": sftype}
                            trace_expressions.append(expr)
                        elements.append({"kind": "struct", "fields": s_map})
                    step_map["outputs"]["pumpGroup"] = {"kind": "array", "elements": elements}
                elif fname == "analogValues":
                    cur_len = len(step["inputs"]["analogValues"])
                    a_low = cin["analogValues"].get("lower_bound", 1)
                    elements = []
                    for idx in range(1, cur_len + 1):
                        tr_var = f"TraceOut_analogValues_{idx}"
                        body.append(
                            f"{indent}{tr_var}[{step_index}] := Binding_{case_index}_analogValues[{a_low + idx - 1}];"
                        )
                        expr = f"PLC_PRG.{tr_var}[{step_index}]"
                        elements.append({"kind": "scalar", "expr": expr, "type": "INT"})
                        trace_expressions.append(expr)
                    step_map["outputs"]["analogValues"] = {"kind": "array", "elements": elements}
                elif fname == "channels":
                    cur_len = len(step["inputs"]["channels"])
                    c_low = cin["channels"].get("lower_bound", 1)
                    elements = []
                    for idx in range(1, cur_len + 1):
                        s_map = {}
                        for sfname, sftype in sdefs["ST_AnalogChannel"].items():
                            tr_var = f"TraceOut_channels_{idx}_{sfname}"
                            body.append(
                                f"{indent}{tr_var}[{step_index}] := Binding_{case_index}_channels[{c_low + idx - 1}].{sfname};"
                            )
                            expr = f"PLC_PRG.{tr_var}[{step_index}]"
                            s_map[sfname] = {"kind": "scalar", "expr": expr, "type": sftype}
                            trace_expressions.append(expr)
                        elements.append({"kind": "struct", "fields": s_map})
                    step_map["outputs"]["channels"] = {"kind": "array", "elements": elements}
                elif fname == "recipe":
                    r_low, r_high, _ = parse_array_type(cin["recipe"]["type"])
                    if r_low is None:
                        r_low = 1
                    elements = []
                    for idx in range(r_low, r_high + 1):
                        s_map = {}
                        for sfname, sftype in sdefs["ST_Recipe"].items():
                            tr_var = f"TraceOut_recipe_{idx}_{sfname}"
                            body.append(
                                f"{indent}{tr_var}[{step_index}] := Binding_{case_index}_recipe[{idx}].{sfname};"
                            )
                            expr = f"PLC_PRG.{tr_var}[{step_index}]"
                            s_map[sfname] = {"kind": "scalar", "expr": expr, "type": sftype}
                            trace_expressions.append(expr)
                        elements.append({"kind": "struct", "fields": s_map})
                    step_map["outputs"]["recipe"] = {"kind": "array", "elements": elements}

            # 6. Increment calls & step
            body.append(f"{indent}BenchCalls := BenchCalls + 1;")
            if is_timed:
                body.append(f"{indent}BenchStep := BenchStep + 1;")
                body.append("  END_IF;")

            trace_mappings.append(step_map)
            steps.append(
                {"index": step_index, "case_id": case["id"], "case_step": case_step, "dt_ms": step.get("dt_ms", 0)}
            )
            step_index += 1

    body.append(" END_CASE;")
    if not is_timed:
        body.append(" BenchStep := BenchStep + 1;")
    body += [f" IF BenchStep >= {count} THEN BenchDone := TRUE; END_IF;", "END_IF;"]

    return {
        "declaration": "\n".join(declarations),
        "implementation": "\n".join(body),
        "step_count": count,
        "steps": steps,
        "inputs": inputs,
        "outputs": outputs,
        "trace_expressions": list(dict.fromkeys(trace_expressions)),
        "trace_mapping": trace_mappings,
    }


def run_functional(
    task: dict, candidate: dict | str, source_hash: str, workspace: Path, settings, cases: list[dict] | None = None
) -> dict:
    """Return real simulation trace/evidence. Unsupported tasks remain UNVERIFIED."""
    if cases is None:
        cases = task["tests"]
    workspace = Path(workspace).resolve()
    workspace.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    result = {
        "status": "UNVERIFIED",
        "actual_simulation": False,
        "execution_verified": False,
        "backend": "CODESYS_SIMULATION",
        "task_id": task["id"],
        "source_sha256": source_hash,
        "physical_connection_allowed": False,
        "trace_path": None,
        "reason": None,
    }
    reasons = eligibility(task, cases=cases)
    if reasons:
        result["reason"] = "; ".join(reasons)
        write_json(workspace / "simulation_result.json", result)
        return result
    candidate = normalize_candidate(candidate)
    if digest(candidate) != source_hash:
        raise ValueError("Functional candidate source hash mismatch")
    missing = settings.compiler_ready()
    if missing:
        result["status"], result["reason"] = "TOOL_ERROR", "Missing compiler configuration: " + ", ".join(missing)
        write_json(workspace / "simulation_result.json", result)
        return result
    program = build_program(task, cases=cases)
    token = uuid.uuid4().hex
    script_path = ROOT / "codesys/scripts/run_tests.py"
    template_path = Path(settings.codesys_template)
    exec_ws, staged_script, staged_template = stage_ascii_workspace(
        workspace, script_path, template_path, settings.get_ascii_work_root()
    )
    project = exec_ws / "simulation.project"
    shutil.copy2(staged_template, project)
    request = {
        "request_id": token,
        "mode": "IDE_SIMULATION_ONLY",
        "no_physical_connection": True,
        "workspace": str(exec_ws),
        "project": str(project),
        "template": str(staged_template),
        "task_id": task["id"],
        "task_sha256": digest(task),
        "source_sha256": source_hash,
        "candidate": candidate,
        "program": program,
        "result_path": str(exec_ws / "simulation_evidence.json"),
    }
    write_json(exec_ws / "request.json", request)
    write_json(exec_ws / "candidate.json", candidate)
    (exec_ws / "test_program.st").write_text(
        program["declaration"] + "\n\n" + program["implementation"] + "\nEND_PROGRAM\n", encoding="utf-8"
    )
    if exec_ws != workspace:
        write_json(workspace / "request.json", request)
        write_json(workspace / "candidate.json", candidate)
        (workspace / "test_program.st").write_text(
            program["declaration"] + "\n\n" + program["implementation"] + "\nEND_PROGRAM\n", encoding="utf-8"
        )
    command = [
        settings.codesys_exe,
        "--profile=" + settings.codesys_profile,
        "--runscript=" + str(staged_script),
        "--noUI",
        "--culture=en",
    ]
    if settings.additional_folder:
        command.append("--additionalfolder=" + settings.additional_folder)
    write_json(
        exec_ws / "invocation.json",
        {
            "argv": command,
            "template_sha256": hashlib.sha256(Path(settings.codesys_template).read_bytes()).hexdigest(),
            "script_sha256": hashlib.sha256(staged_script.read_bytes()).hexdigest(),
            "program_sha256": digest(program),
        },
    )
    env = os.environ.copy()
    env["PLC_CODESYS_TEST_REQUEST"] = str(exec_ws / "request.json")
    for key in ("PLC_LLM_API_KEY", "OPENAI_API_KEY", "PLC_API_CONFIG"):
        env.pop(key, None)
    try:
        lock_path = ROOT / ".local/compiler.lock"
        lock_path.parent.mkdir(exist_ok=True)
        with lock_path.open("a+b") as lock:
            if os.name == "nt":
                import msvcrt

                if lock.tell() == 0:
                    lock.write(b"0")
                    lock.flush()
                lock.seek(0)
                deadline = time.monotonic() + 900
                while True:
                    try:
                        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
                        break
                    except OSError:
                        if time.monotonic() >= deadline:
                            raise TimeoutError("Shared CODESYS lock wait exceeded 900 seconds")
                        time.sleep(0.25)
            with (exec_ws / "stdout.log").open("wb") as out, (exec_ws / "stderr.log").open("wb") as err:
                proc = subprocess.Popen(
                    codesys_command(command),
                    env=env,
                    stdout=out,
                    stderr=err,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                )
                try:
                    result["process_exit_code"] = proc.wait(timeout=max(180, settings.compiler_timeout))
                except subprocess.TimeoutExpired:
                    _kill_tree(proc)
                    result["status"], result["reason"] = "TIMEOUT", "CODESYS simulation process timeout"
            if result["status"] != "TIMEOUT":
                evidence = read_json(exec_ws / "simulation_evidence.json")
                if (
                    evidence.get("request_id") != token
                    or evidence.get("source_sha256") != source_hash
                    or evidence.get("physical_connection_allowed") is not False
                ):
                    raise ValueError("Unrelated simulation evidence")
                result.update(
                    {
                        k: evidence.get(k)
                        for k in ("status", "actual_simulation", "execution_verified", "infrastructure_error")
                    }
                )
                if result["process_exit_code"] != 0:
                    result["status"], result["reason"] = "TOOL_ERROR", "Simulation IDE process exited abnormally"
                elif evidence.get("execution_verified"):
                    if "raw_monitoring" in evidence:
                        rows = unflatten_observations(program, evidence["raw_monitoring"])
                    else:
                        rows = evidence.get("observations", [])
                    if len(rows) != program["step_count"]:
                        raise ValueError("Missing observed scan rows")
                    cases_dict = {case["id"]: [] for case in cases}
                    for meta, row in zip(program["steps"], rows):
                        step_data = {"inputs": row["inputs"], "outputs": row["outputs"]}
                        if "dt_ms" in row:
                            step_data["dt_ms"] = row["dt_ms"]
                        cases_dict[meta["case_id"]].append(step_data)
                    task_eval = task
                    if cases != task.get("tests"):
                        task_eval = dict(task)
                        task_eval["tests"] = cases
                    trace = {
                        "task_id": task["id"],
                        "task_sha256": digest(task_eval),
                        "source_sha256": source_hash,
                        "backend": "CODESYS_SIMULATION",
                        "operator": "automated CODESYS IDE simulation scan sequencer",
                        "acquisition": "automated CODESYS IDE simulation with native scan sequencer",
                        "observed_utc": now(),
                        "evidence_files": ["simulation_evidence.json", "test_program.st", "request.json"],
                        "cases": cases_dict,
                        "scan_control": "One FB invocation per real simulator task scan; separate freshly initialized instance per fixed test",
                    }
                    write_json(workspace / "trace.json", trace)
                    if exec_ws != workspace:
                        sync_ascii_artifacts(exec_ws, workspace)
                    from .functional import evaluate_trace

                    evaluated = evaluate_trace(task_eval, source_hash, trace, evidence_root=workspace)
                    result["status"] = evaluated["status"]
                    result["functional"] = evaluated
                    result["trace_path"] = str(workspace / "trace.json")
    except (OSError, ValueError, KeyError) as exc:
        result["status"], result["reason"] = "TOOL_ERROR", f"{type(exc).__name__}: {exc}"
    finally:
        if exec_ws != workspace:
            sync_ascii_artifacts(exec_ws, workspace)
    result["elapsed_seconds"] = time.monotonic() - started
    result["finished_utc"] = now()
    write_json(workspace / "simulation_result.json", result)
    return result
