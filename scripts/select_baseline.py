"""Record a transparent pre-benchmark baseline substitution, preserving setup runs."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from plc_agent.common import ROOT, read_json, write_json, now
from plc_agent.dataset import load_tasks
from plc_agent.harness import empty_result

settings_path = ROOT / "configs/experiments.json"
config = read_json(settings_path)
for condition in config["conditions"]:
    if condition["id"] in ("E1", "E2"):
        condition["framework"] = "smolagents"
config["selection_status"] = "RESPONSES_MODELS_VERIFIED_BASELINE_TOOL_INTEGRATION_PENDING"
config["baseline_version"] = "smolagents 1.26.0 ToolCallingAgent"
config["baseline_substitution_reason"] = "Codex CLI tool execution required approvals unavailable under its local noninteractive policy; preserved as setup infrastructure failures. No policy was bypassed."
write_json(settings_path, config)
campaign_path = ROOT / "results/summary/campaign.json"
manifest = read_json(campaign_path)
if manifest["conditions"] != config["conditions"]:
    archive = ROOT / "results/raw/protocol_revision_codex_to_smolagents.json"
    if not archive.exists():
        write_json(archive, {"observed_utc": now(), "reason": config["baseline_substitution_reason"], "previous_campaign": manifest})
    manifest["conditions"] = config["conditions"]
    manifest["protocol_revised_utc"] = now()
    manifest["protocol_revision_evidence"] = str(archive.relative_to(ROOT))
    tasks = {t["id"]: t for t in load_tasks()}
    for condition in config["conditions"]:
        if condition["id"] not in ("E1", "E2"):
            continue
        for task in tasks.values():
            key = condition["id"] + "/" + task["id"]
            previous = read_json(ROOT / manifest["records"][key])
            if previous["framework"] == "smolagents":
                continue
            destination = ROOT / "experiments" / condition["id"] / manifest["id"] / task["id"] / "planned_smolagents_result.json"
            write_json(destination, empty_result(task, condition["id"], condition["model"], "smolagents", "Awaiting smolagents baseline integration; Codex setup outcomes preserved separately"))
            manifest["records"][key] = str(destination.relative_to(ROOT))
    write_json(campaign_path, manifest)
print("Baseline selected: smolagents 1.26.0. Prior Codex setup records preserved.")
