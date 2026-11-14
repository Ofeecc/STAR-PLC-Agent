"""Reproduce PUB002 DWORD smoke test against the new self-developed converter."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from plc_agent.model_checker import check_model
from plc_agent.st_verifier import compile_st_to_smv, verify_candidate_st


def main() -> None:
    source_path = Path(sys.argv[1])
    executable = sys.argv[2]
    task = json.loads((ROOT / "dataset/public/PUB002.json").read_text(encoding="utf-8-sig"))
    source = source_path.read_text(encoding="utf-8")
    declaration, implementation = source.split("risingBits :=", 1)
    implementation = "risingBits :=" + implementation.split("END_FUNCTION_BLOCK", 1)[0]
    candidate = {"declaration": declaration, "implementation": implementation, "supporting_objects": []}
    out = ROOT / "results/raw/converter_smoke_20261114/PUB002_wrong_count_probe"
    out.mkdir(parents=True, exist_ok=True)
    (out / "candidate.json").write_text(json.dumps(candidate, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        compiled = compile_st_to_smv(candidate, task)
        (out / "candidate_coupled_compile_only.smv").write_text(compiled["smv_text"], encoding="utf-8")
        print(json.dumps({"compile": "PASS", "expected_spec_count": compiled["expected_spec_count"],
                          "uses_smt": compiled["uses_smt"]}, ensure_ascii=False), flush=True)
    except Exception as exc:
        print(json.dumps({"compile": type(exc).__name__, "reason": str(exc)}, ensure_ascii=False), flush=True)
        raise
    result = verify_candidate_st(task, candidate, out / "verify", timeout=30,
                                 executable=executable, tool="nuxmv")
    print(json.dumps({k: result.get(k) for k in ("status", "verified", "reason", "total_properties", "passed_properties", "failed_properties", "unknown_properties")}, ensure_ascii=False), flush=True)
    # Diagnostic control: bind the exact same candidate input to the observer's
    # existing val symbol, leaving candidate SSA and all properties untouched.
    coupled = re.sub(r"(?m)^  cand_in_value : unsigned word\[32\];\n", "", compiled["smv_text"])
    coupled = re.sub(r"\bcand_in_value\b", "val", coupled)
    corrected_model = out / "diagnostic_input_bound.smv"
    corrected_model.write_text(coupled, encoding="utf-8")
    control = check_model(corrected_model, out / "input_binding_control", executable=executable,
                          timeout=30, tool="nuxmv")
    print(json.dumps({"input_binding_control_status": control.get("status"),
                      "property_results": [(p.get("expression"), p.get("holds")) for p in control.get("property_results", [])]}, ensure_ascii=False), flush=True)

if __name__ == "__main__":
    main()
