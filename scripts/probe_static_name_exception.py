"""Verify a declaration-only SA0027 exception on a retained candidate, not an Agent score."""

import hashlib
import re
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from plc_agent.common import ROOT, now, read_json, write_json
from plc_agent.compiler import compile_st
from plc_agent.config import Settings


def main():
    cfg = Settings.load(load_api=False)
    template_hash = hashlib.sha256(Path(cfg.codesys_template).read_bytes()).hexdigest()
    candidate = read_json(ROOT / "results/raw/pilot_pair_2026-11-10T143217961073+0000/PUB003_star/version_00.json")
    candidate["declaration"], n = re.subn(
        r"(\n[ \t]*)(error\s*:)", r"\1{attribute 'analysis' := '-27'}\1\2", candidate["declaration"], flags=re.I
    )
    assert n == 1, "Expected exactly one error declaration"
    folder = ROOT / "results/raw" / ("name_exception_" + now().replace(":", "").replace(".", ""))
    first = asdict(compile_st({"id": "PUB003_SCOPED_NAME_EXCEPTION_PROBE"}, candidate, folder / "scoped", cfg))
    second_candidate = deepcopy(candidate)
    second_candidate["declaration"] += "\nVAR\n StaticAnalysisUnusedProbe : DINT;\nEND_VAR"
    task = {
        "id": "SCOPED_EXCEPTION_UNUSED_CONTROL",
        "diagnostic_probe_program": {
            "declaration": "PROGRAM PLC_PRG\nVAR\n ProbeInstance : FB_Task;\nEND_VAR",
            "implementation": "ProbeInstance(Value:=0, hiLevel:=10, loLevel:=0, hystWindow:=1);",
        },
    }
    second = asdict(compile_st(task, second_candidate, folder / "unused_control", cfg))
    result = {
        "template_unchanged": template_hash == hashlib.sha256(Path(cfg.codesys_template).read_bytes()).hexdigest(),
        "template_sha256": template_hash,
        "scope": "MANUAL_DECLARATION_EXCEPTION_PROBE_NOT_AGENT_BENCHMARK",
        "scoped_exception": first,
        "other_rule_negative_control": second,
    }
    result["verified"] = bool(
        first["success"]
        and second["status"] == "COMPILE_FAIL"
        and any(d.get("code") == "SA0033" for d in second["diagnostics"])
        and result["template_unchanged"]
    )
    write_json(folder / "summary.json", result)
    print(
        {"verified": result["verified"], "statuses": [first["status"], second["status"]], "evidence": str(folder)},
        flush=True,
    )


if __name__ == "__main__":
    main()
