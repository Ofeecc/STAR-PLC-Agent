"""Recalculate descriptive benchmark results from the active campaign's raw rows.

No model calls, compiler execution, result-row edits or imputation occur here.
Run with Project1: python scripts/analyze_results.py [--no-plots].
Figures are withheld while any planned agent run is NOT_RUN, unless explicitly
requested with --allow-incomplete. A snapshot always records completeness.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from plc_agent.metrics import BASELINE_MAP, bootstrap_ci, mcnemar_exact
from plc_agent.simulation import eligibility


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()


def valid_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def valid_token(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def ratio(a, b):
    return a / b if b else None


def percentage(value):
    return "not evaluated" if value is None else f"{100 * value:.2f}%"


def format_ci(ci):
    if ci is None:
        return "--"
    return f"[{100 * ci[0]:.2f}%, {100 * ci[1]:.2f}%]"


def format_p(p):
    if p is None:
        return "--"
    if p < 0.001:
        return "< 0.001"
    return f"{p:.4f}"


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8-sig")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def classify_agent_error(row):
    if row["status"] == "NOT_RUN":
        return "not_run"
    if row["status"] == "TIMEOUT":
        return "timeout"
    if row["status"] != "TOOL_ERROR":
        return None
    text = (row.get("reason", "") + " " + row.get("agent_completion_error", "")).lower()
    if any(token in text for token in ("ssleof", "sslerror", "unexpected_eof_while_reading")):
        return "tls_transport"
    if any(
        token in text
        for token in (
            "stream closed before",
            "without a terminal",
            "terminal event",
            "missing completed responses event",
            "truncated output",
        )
    ):
        return "relay_incomplete_stream"
    if any(token in text for token in ("proxyerror", "connect to proxy", "remotedisconnected")):
        return "proxy_or_disconnected_transport"
    if "timeout" in text or "timed out" in text:
        return "provider_or_tool_timeout"
    if any(token in text for token in ("connectionerror", "connection", "http")):
        return "other_transport_or_http"
    if row.get("compilation_attempts"):
        return "compiler_or_tool_infrastructure"
    return "other_agent_or_provider_error"


def llm_observations(directory):
    """A saved request is an attempt; absent usage remains unknown, not zero.

    Response JSON files contain the provider's reported usage. We deliberately
    avoid parsing request prompts or event content, which is unnecessary here.
    """
    calls = []
    for request in sorted(directory.glob("llm_*/request.json")):
        response_file = request.parent / "response.json"
        response = read(response_file) if response_file.is_file() else {}
        usage = response.get("usage") if isinstance(response.get("usage"), dict) else {}
        incoming, outgoing, total = [usage.get(key) for key in ("input_tokens", "output_tokens", "total_tokens")]
        if not valid_token(total) and valid_token(incoming) and valid_token(outgoing):
            total = incoming + outgoing
        calls.append(
            {
                "request": relative(request),
                "response_saved": response_file.is_file(),
                "response_status": response.get("status"),
                "input_tokens": incoming if valid_token(incoming) else None,
                "output_tokens": outgoing if valid_token(outgoing) else None,
                "total_tokens": total if valid_token(total) else None,
            }
        )
    return calls


def summarize(rows, tasks, planned_tasks):
    attempted = [row for row in rows if row["status"] != "NOT_RUN"]
    first_count = sum(row["first_pass_compiled"] is True for row in rows)
    final_count = sum(row["final_compiled"] is True for row in rows)
    compiler_evaluated = sum(row["first_pass_compiled"] is not None for row in rows)
    failed_initial = sum(row["first_pass_compiled"] is False for row in rows)
    repaired = sum(row["first_pass_compiled"] is False and row["final_compiled"] is True for row in rows)
    cases = sum(len(tasks[row["task_id"]]["tests"]) for row in rows)
    steps = sum(len(case["steps"]) for row in rows for case in tasks[row["task_id"]]["tests"])
    functional = [row["functional"] for row in rows]
    evaluated_cases = sum(f["evaluated_cases"] for f in functional)
    passed_cases = sum(f["passed_cases"] for f in functional)
    evaluated_steps = sum(f["evaluated_steps"] for f in functional)
    passed_steps = sum(f["passed_steps"] for f in functional)
    evaluated_tasks = sum(f["evaluated_cases"] == f["planned_cases"] and f["planned_cases"] > 0 for f in functional)
    passed_tasks = sum(
        f["status"] == "PASS" and f["passed_cases"] == f["evaluated_cases"] == f["planned_cases"] > 0
        for f in functional
    )
    observations = [call for row in rows for call in row["_calls"]]
    resource = {}
    for key in ("input_tokens", "output_tokens", "total_tokens"):
        observed = [call[key] for call in observations if call[key] is not None]
        resource["observed_" + key] = sum(observed) if observed else None
        resource[key + "_reporting_calls"] = len(observed)
        resource["missing_" + key + "_calls"] = len(observations) - len(observed)
        resource["complete_" + key] = sum(observed) if observations and len(observed) == len(observations) else None
    elapsed = [row["elapsed_seconds"] for row in attempted if valid_number(row.get("elapsed_seconds"))]
    comp_vals = [1.0 if row["final_compiled"] is True else 0.0 for row in rows]
    compilation_ci = bootstrap_ci(comp_vals) if comp_vals else None
    task_pass_vals = [
        1.0 if (f["status"] == "PASS" and f["passed_cases"] == f["evaluated_cases"] == f["planned_cases"] > 0) else 0.0
        for f in functional
    ]
    task_pass_ci = bootstrap_ci(task_pass_vals) if task_pass_vals else None
    return {
        "planned_tasks": planned_tasks,
        "recorded_tasks": len(rows),
        "agent_attempted_tasks": len(attempted),
        "agent_campaign_complete": len(rows) == planned_tasks and len(attempted) == planned_tasks,
        "status_counts": dict(Counter(row["status"] for row in rows)),
        "functional_status_counts": dict(Counter(f["status"] for f in functional)),
        "actual_first_compilations": compiler_evaluated,
        "first_pass_compiled_tasks": first_count,
        "final_compiled_tasks": final_count,
        "first_pass_compilation_rate": ratio(first_count, planned_tasks),
        "final_compilation_rate": ratio(final_count, planned_tasks),
        "compilation_ci": compilation_ci,
        "compiler_coverage": ratio(compiler_evaluated, planned_tasks),
        "first_pass_rate_among_compiler_evaluated": ratio(first_count, compiler_evaluated),
        "final_rate_among_compiler_evaluated": ratio(final_count, compiler_evaluated),
        "initial_compile_failures": failed_initial,
        "repair_successes": repaired,
        "repair_effectiveness": ratio(repaired, failed_initial),
        "repair_attempts": sum(row["repair_attempts"] for row in rows),
        "compiler_calls": sum(len(row["compilation_attempts"]) for row in rows),
        "planned_cases": cases,
        "evaluated_cases": evaluated_cases,
        "passed_cases": passed_cases,
        "failed_cases": evaluated_cases - passed_cases,
        "case_pass_rate": ratio(passed_cases, evaluated_cases),
        "case_coverage": ratio(evaluated_cases, cases),
        "planned_steps": steps,
        "evaluated_steps": evaluated_steps,
        "passed_steps": passed_steps,
        "scan_pass_rate": ratio(passed_steps, evaluated_steps),
        "fully_evaluated_tasks": evaluated_tasks,
        "passed_tasks": passed_tasks,
        "task_pass_rate": ratio(passed_tasks, evaluated_tasks),
        "task_pass_ci": task_pass_ci,
        "functional_task_coverage": ratio(evaluated_tasks, planned_tasks),
        "eligible_tasks": sum(not eligibility(tasks[row["task_id"]]) for row in rows),
        "mean_agent_elapsed_seconds": statistics.mean(elapsed) if elapsed else None,
        "median_agent_elapsed_seconds": statistics.median(elapsed) if elapsed else None,
        "min_agent_elapsed_seconds": min(elapsed) if elapsed else None,
        "max_agent_elapsed_seconds": max(elapsed) if elapsed else None,
        "summed_agent_elapsed_seconds": sum(elapsed) if elapsed else None,
        "attempted_llm_requests_from_files": len(observations),
        "saved_llm_responses": sum(call["response_saved"] for call in observations),
        "reported_llm_calls_row_field": sum(row.get("llm_calls", 0) for row in rows),
        "reported_tool_calls_row_field": sum(row.get("tool_call_count", 0) for row in rows),
        "agent_error_categories": dict(
            Counter(category for row in rows if (category := classify_agent_error(row)) is not None)
        ),
        "api_cost": sum(row["api_cost"] for row in attempted)
        if attempted and all(valid_number(row.get("api_cost")) for row in attempted)
        else None,
        **resource,
    }


def render_markdown(data):
    complete = all(c["agent_campaign_complete"] for c in data["conditions"])
    text = [
        "# Recalculated experiment results",
        "",
        f"Snapshot: {data['generated_utc']}. Campaign `{data['campaign']}`.",
        "",
        "Agent-run coverage: "
        + ("all 128 planned runs were attempted." if complete else "INCOMPLETE; this is a provisional snapshot."),
        "",
        "All compilation rates use the fixed denominator of 32 tasks per condition, including transport failures. Functional rates use only actually evaluated CODESYS cases or tasks; their coverage is shown separately. Compilation is a syntax/type/build measurement, not proof of task correctness.",
        "",
        "| Condition | Framework | Relay model ID | Agent attempted | First compile | Final compile | Compiler evaluated |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for c in data["conditions"]:
        text.append(
            f"| {c['condition']} | {c['framework']} | `{c['model']}` | {c['agent_attempted_tasks']}/32 | {c['first_pass_compiled_tasks']}/32 ({percentage(c['first_pass_compilation_rate'])}) | {c['final_compiled_tasks']}/32 ({percentage(c['final_compilation_rate'])}) | {c['actual_first_compilations']}/32 |"
        )
    text += [
        "",
        "| Condition | Passed/evaluated cases | Case pass rate | Cases evaluated/planned | Passed/fully evaluated tasks | Task pass rate | Tasks evaluated/planned |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for c in data["conditions"]:
        text.append(
            f"| {c['condition']} | {c['passed_cases']}/{c['evaluated_cases']} | {percentage(c['case_pass_rate'])} | {c['evaluated_cases']}/{c['planned_cases']} | {c['passed_tasks']}/{c['fully_evaluated_tasks']} | {percentage(c['task_pass_rate'])} | {c['fully_evaluated_tasks']}/32 |"
        )
    text += [
        "",
        "| Condition | Compiler calls | Repair successes/initial failures | Saved request attempts | Usage-reported calls | Observed input/output tokens | Mean/median agent time (s) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for c in data["conditions"]:
        average = (
            f"{c['mean_agent_elapsed_seconds']:.1f}/{c['median_agent_elapsed_seconds']:.1f}"
            if c["mean_agent_elapsed_seconds"] is not None
            else "unknown"
        )
        text.append(
            f"| {c['condition']} | {c['compiler_calls']} | {c['repair_successes']}/{c['initial_compile_failures']} | {c['attempted_llm_requests_from_files']} | {c['total_tokens_reporting_calls']} | {c['observed_input_tokens']}/{c['observed_output_tokens']} | {average} |"
        )
    text += [
        "",
        "## Statistical significance and 95% bootstrap confidence intervals",
        "",
        "| Condition | Final pass (95% CI) | Task pass rate (95% CI) | Baseline | McNemar p (compilation) | McNemar p (task pass) |",
        "|---|---|---|---|---:|---:|",
    ]
    for c in data["conditions"]:
        comp_ci = format_ci(c.get("compilation_ci"))
        task_ci = format_ci(c.get("task_pass_ci"))
        base = c.get("baseline_condition") or "--"
        p_comp = format_p(c.get("mcnemar_compilation_p_value"))
        p_task = format_p(c.get("mcnemar_task_pass_p_value"))
        text.append(
            f"| {c['condition']} | {c['final_compiled_tasks']}/32 ({percentage(c['final_compilation_rate'])}) {comp_ci} | {c['passed_tasks']}/{c['fully_evaluated_tasks']} ({percentage(c['task_pass_rate'])}) {task_ci} | {base} | {p_comp} | {p_task} |"
        )
    text += [
        "",
        "## Interpretation and limits",
        "",
        "- `agent_campaign_complete` means every planned task was attempted. It differs from `metrics.json`'s conservative `campaign_complete`, which requires a real compiler observation for every task; provider failures lower compiler coverage.",
        "- Attempt counts come from each active run's `llm_*/request.json`. The self harness's stored `llm_calls` increments after a successful response, whereas the baseline counts attempts. The request-file derivation makes the count comparable without editing historical rows.",
        "- Token totals are sums of observed provider usage records only. Every missing input/output/total usage field has a separate missing-call count. Unknown calls are not assigned zero. Complete token totals and API costs remain null when unreported; prices and upstream model identity are unverified.",
        "- Mean/median times describe the original end-to-end agent runs, including compiler calls and failures. Later functional-test acquisition time is excluded. There is one repetition per task and condition; no statistical significance or causal superiority is claimed.",
        "- The automatic simulator adapter supports 21/32 tasks, 52/81 cases and 359/576 scan observations. Remaining tasks require elapsed-time, composite or IN_OUT adapters. Eligibility alone is not execution evidence.",
        "- A custom `VARIANT` DUT allowed E1/PUB018 to compile, but its caller interface differs from native generic storage. This remains a task-fidelity limitation, not a verified generic FIFO implementation.",
        "",
    ]
    for c in data["conditions"]:
        text.append(
            f"{c['condition']} agent errors: `{json.dumps(c['agent_error_categories'], sort_keys=True)}`. Functional outcomes: `{json.dumps(c['functional_status_counts'], sort_keys=True)}`."
        )
        text.append("")
    return "\n".join(text)


def render_latex(data):
    """Small booktabs fragments for the main report; every denominator is explicit."""
    row_end = chr(92) * 2

    def pct(value):
        return "--" if value is None else f"{100 * value:.2f}\\%"

    text = [
        "% Generated by scripts/analyze_results.py; do not edit numbers manually.",
        "\\begin{table}[htbp]",
        "\\centering\\small",
        "\\setlength{\\tabcolsep}{5pt}",
        "\\caption{Compilation outcomes. All rates use 32 planned tasks per condition; infrastructure failures stay in the denominator.}",
        "\\label{tab:compilation}",
        "\\begin{tabular}{lrrrrr}",
        "\\toprule",
        "Condition & Attempted & First pass & Final pass & \\shortstack{Compiler\\\\evaluated} & Repairs " + row_end,
        "\\midrule",
    ]
    for c in data["conditions"]:
        text.append(
            f"{c['condition']} & {c['agent_attempted_tasks']}/32 & {c['first_pass_compiled_tasks']}/32 ({pct(c['first_pass_compilation_rate'])}) & {c['final_compiled_tasks']}/32 ({pct(c['final_compilation_rate'])}) & {c['actual_first_compilations']}/32 & {c['repair_successes']}/{c['initial_compile_failures']} "
            + row_end
        )
    text += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
        "",
        "\\begin{table}[htbp]",
        "\\centering\\small",
        "\\setlength{\\tabcolsep}{5pt}",
        "\\caption{Actual CODESYS functional results. Pass rates are conditional on evaluation; planned totals are 81 cases and 32 tasks per condition.}",
        "\\label{tab:functional}",
        "\\begin{tabular}{lrrrrrr}",
        "\\toprule",
        "Condition & \\shortstack{Cases\\\\passed} & Case rate & \\shortstack{Case\\\\coverage} & \\shortstack{Tasks\\\\passed} & Task rate & \\shortstack{Task\\\\coverage} "
        + row_end,
        "\\midrule",
    ]
    for c in data["conditions"]:
        text.append(
            f"{c['condition']} & {c['passed_cases']}/{c['evaluated_cases']} & {pct(c['case_pass_rate'])} & {c['evaluated_cases']}/81 & {c['passed_tasks']}/{c['fully_evaluated_tasks']} & {pct(c['task_pass_rate'])} & {c['fully_evaluated_tasks']}/32 "
            + row_end
        )
    text += [
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
        "",
        "\\begin{table}[htbp]",
        "\\centering\\small",
        "\\setlength{\\tabcolsep}{4pt}",
        "\\caption{Statistical significance and 95\\% percentile bootstrap confidence intervals against baseline.}",
        "\\label{tab:significance}",
        "\\begin{tabular}{lrrrrr}",
        "\\toprule",
        "Condition & Final pass (95\\% CI) & Task pass (95\\% CI) & Base & \\shortstack{McNemar $p$\\\\(compile)} & \\shortstack{McNemar $p$\\\\(task)} "
        + row_end,
        "\\midrule",
    ]
    for c in data["conditions"]:
        comp_ci = format_ci(c.get("compilation_ci")).replace("%", "\\%")
        task_ci = format_ci(c.get("task_pass_ci")).replace("%", "\\%")
        base = c.get("baseline_condition") or "--"
        p_comp = format_p(c.get("mcnemar_compilation_p_value"))
        p_task = format_p(c.get("mcnemar_task_pass_p_value"))
        text.append(
            f"{c['condition']} & {pct(c['final_compilation_rate'])} {comp_ci} & {pct(c['task_pass_rate'])} {task_ci} & {base} & {p_comp} & {p_task} "
            + row_end
        )
    text += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    return "\n".join(text)


def render_resource_latex(data):
    row_end = chr(92) * 2
    text = [
        "% Generated by scripts/analyze_results.py from saved request/response artifacts.",
        "\\begin{table}[htbp]",
        "\\centering\\small",
        "\\setlength{\\tabcolsep}{5pt}",
        "\\caption{Original agent-run resources. Times include failed runs and compiler calls. Token counts sum observed provider reports only; unknown usage is not zero.}",
        "\\label{tab:resources}",
        "\\begin{tabular}{lrrrrrr}",
        "\\toprule",
        "Condition & \\shortstack{Mean/median\\\\seconds} & Requests & \\shortstack{Usage\\\\coverage} & \\shortstack{Observed\\\\input tokens} & \\shortstack{Observed\\\\output tokens} & \\shortstack{Compiler\\\\calls} "
        + row_end,
        "\\midrule",
    ]
    for c in data["conditions"]:
        elapsed = (
            f"{c['mean_agent_elapsed_seconds']:.1f}/{c['median_agent_elapsed_seconds']:.1f}"
            if c["mean_agent_elapsed_seconds"] is not None
            else "--"
        )
        incoming = f"{c['observed_input_tokens']:,}" if c["observed_input_tokens"] is not None else "--"
        outgoing = f"{c['observed_output_tokens']:,}" if c["observed_output_tokens"] is not None else "--"
        text.append(
            f"{c['condition']} & {elapsed} & {c['attempted_llm_requests_from_files']} & {c['total_tokens_reporting_calls']}/{c['attempted_llm_requests_from_files']} & {incoming} & {outgoing} & {c['compiler_calls']} "
            + row_end
        )
    text += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    return "\n".join(text)


def make_plots(data, rows, output):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.ticker import MaxNLocator, PercentFormatter

    output.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titleweight": "bold",
            "savefig.facecolor": "white",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    conditions = data["conditions"]
    x = np.arange(len(conditions))
    width = 0.34
    fig, ax = plt.subplots(figsize=(7.5, 4.1), constrained_layout=True)
    for offset, key, label, color in (
        (-width / 2, "first_pass_compiled_tasks", "First compilation", "#16324F"),
        (width / 2, "final_compiled_tasks", "Final compilation", "#007F82"),
    ):
        counts = [c[key] for c in conditions]
        bars = ax.bar(x + offset, [n / 32 for n in counts], width, color=color, label=label)
        for bar, n in zip(bars, counts):
            ax.annotate(
                f"{n}/32",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
            )
    ax.set_xticks(x, [c["condition"] for c in conditions])
    ax.set_ylim(0, 1.12)
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.set_ylabel("Compiled tasks / all 32 planned tasks")
    ax.set_title("Compilation success, including infrastructure failures")
    ax.legend(loc="upper left", frameon=False, ncol=2)
    ax.grid(axis="y", alpha=0.18)
    ax.set_axisbelow(True)
    for ext in ("png", "pdf"):
        fig.savefig(output / f"compilation_rates.{ext}", dpi=220)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7.5, 4.1), constrained_layout=True)
    passed = [c["passed_cases"] for c in conditions]
    failed = [c["failed_cases"] for c in conditions]
    missing = [c["planned_cases"] - c["evaluated_cases"] for c in conditions]
    ax.bar(x, passed, color="#207451", label="Passed")
    ax.bar(x, failed, bottom=passed, color="#A43732", label="Failed")
    ax.bar(x, missing, bottom=np.array(passed) + np.array(failed), color="#CCD6DE", label="Not evaluated")
    for i, c in enumerate(conditions):
        ax.text(
            i,
            c["planned_cases"] + 1.3,
            f"{c['passed_cases']}/{c['evaluated_cases']} evaluated passed",
            ha="center",
            fontsize=8,
        )
    ax.set_xticks(x, [c["condition"] for c in conditions])
    ax.set_ylim(0, max(c["planned_cases"] for c in conditions) + 12)
    ax.set_ylabel("Fixed test cases (81 planned per condition)")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_title("Functional case outcomes from actual CODESYS simulation")
    ax.legend(frameon=False, ncol=3, loc="upper center")
    ax.grid(axis="y", alpha=0.18)
    ax.set_axisbelow(True)
    for ext in ("png", "pdf"):
        fig.savefig(output / f"functional_coverage.{ext}", dpi=220)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7.5, 4.1), constrained_layout=True)
    samples = [
        [r["elapsed_seconds"] for r in rows if r["condition"] == c["condition"] and r["status"] != "NOT_RUN"]
        for c in conditions
    ]
    boxes = ax.boxplot(
        samples,
        tick_labels=[c["condition"] for c in conditions],
        patch_artist=True,
        showmeans=False,
        showfliers=False,
        medianprops={"color": "#007F82", "linewidth": 1.5},
    )
    for box in boxes["boxes"]:
        box.set(facecolor="#F0F5F8", edgecolor="#16324F")
    for i, values in enumerate(samples):
        jitter = np.linspace(-0.14, 0.14, len(values)) if values else []
        ax.scatter(np.ones(len(values)) * (i + 1) + jitter, values, s=13, alpha=0.48, c="#007F82", zorder=3)
    ax.set_ylabel("Original agent elapsed time (seconds)")
    ax.set_title("Task latency, including failed agent runs")
    ax.grid(axis="y", alpha=0.18)
    ax.set_axisbelow(True)
    for ext in ("png", "pdf"):
        fig.savefig(output / f"agent_latency.{ext}", dpi=220)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-plots", action="store_true")
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args()
    campaign_file = ROOT / "results/summary/campaign.json"
    manifest = read(campaign_file)
    tasks = {
        task["id"]: task
        for directory in ("public", "self_built")
        for file in sorted((ROOT / "dataset" / directory).glob("*.json"))
        if (task := read(file))
    }
    rows, raw_hashes = [], []
    for key, value in sorted(manifest["records"].items()):
        path = ROOT / value
        row = read(path)
        if key != row["condition"] + "/" + row["task_id"]:
            raise ValueError("Campaign pointer mismatch: " + key)
        row["_path"] = relative(path)
        row["_calls"] = llm_observations(path.parent)
        rows.append(row)
        raw_hashes.append({"key": key, "path": relative(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    conditions = []
    group_rows = []
    for condition in manifest["conditions"]:
        selected = [row for row in rows if row["condition"] == condition["id"]]
        summary = summarize(selected, tasks, manifest["planned_tasks"])
        summary.update({"condition": condition["id"], "framework": condition["framework"], "model": condition["model"]})
        conditions.append(summary)
        for dimension in ("difficulty", "kind"):
            for group in sorted({task[dimension] for task in tasks.values()}):
                group_tasks = {k: t for k, t in tasks.items() if t[dimension] == group}
                subset = [row for row in selected if row["task_id"] in group_tasks]
                s = summarize(subset, tasks, len(group_tasks))
                group_rows.append(
                    {
                        "condition": condition["id"],
                        "dimension": dimension,
                        "group": group,
                        **{
                            key: s[key]
                            for key in (
                                "planned_tasks",
                                "agent_attempted_tasks",
                                "first_pass_compiled_tasks",
                                "final_compiled_tasks",
                                "actual_first_compilations",
                                "first_pass_compilation_rate",
                                "final_compilation_rate",
                                "evaluated_cases",
                                "passed_cases",
                                "case_pass_rate",
                                "fully_evaluated_tasks",
                                "passed_tasks",
                                "task_pass_rate",
                            )
                        },
                    }
                )

    by_cond_rows = {}
    for row in rows:
        by_cond_rows.setdefault(row["condition"], {})[row["task_id"]] = row

    for c in conditions:
        cid = c["condition"]
        base_id = BASELINE_MAP.get(cid)
        mcnemar_compile_p = None
        mcnemar_task_p = None
        if base_id and base_id in by_cond_rows and cid in by_cond_rows:
            c_task_dict = by_cond_rows[cid]
            b_task_dict = by_cond_rows[base_id]
            shared_tids = set(c_task_dict.keys()) & set(b_task_dict.keys())
            if shared_tids:
                b_comp = sum(
                    bool(c_task_dict[t]["final_compiled"]) and not bool(b_task_dict[t]["final_compiled"])
                    for t in shared_tids
                )
                c_comp = sum(
                    not bool(c_task_dict[t]["final_compiled"]) and bool(b_task_dict[t]["final_compiled"])
                    for t in shared_tids
                )
                mcnemar_compile_p = mcnemar_exact(b_comp, c_comp)

                def is_task_pass(r):
                    f = r["functional"]
                    return f["status"] == "PASS" and f["passed_cases"] == f["evaluated_cases"] == f["planned_cases"] > 0

                b_pass = sum(is_task_pass(c_task_dict[t]) and not is_task_pass(b_task_dict[t]) for t in shared_tids)
                c_pass = sum(not is_task_pass(c_task_dict[t]) and is_task_pass(b_task_dict[t]) for t in shared_tids)
                mcnemar_task_p = mcnemar_exact(b_pass, c_pass)

        c["baseline_condition"] = base_id
        c["mcnemar_compilation_p_value"] = mcnemar_compile_p
        c["mcnemar_task_pass_p_value"] = mcnemar_task_p
    issues = []
    task_rows, failures, diagnostic_rows, functional_failures = [], [], [], []
    for row in rows:
        task = tasks[row["task_id"]]
        functional = row["functional"]
        if functional["evaluated_cases"] and functional.get("evidence") not in (
            "CODESYS_SIMULATION",
            "CODESYS_RUNTIME",
        ):
            issues.append(row["condition"] + "/" + row["task_id"] + ": functional counts lack CODESYS evidence label")
        task_rows.append(
            {
                "condition": row["condition"],
                "task_id": row["task_id"],
                "kind": task["kind"],
                "difficulty": task["difficulty"],
                "status": row["status"],
                "first_pass_compiled": row["first_pass_compiled"],
                "final_compiled": row["final_compiled"],
                "compiler_calls": len(row["compilation_attempts"]),
                "repair_attempts": row["repair_attempts"],
                "eligible_for_automated_simulation": not eligibility(task),
                "functional_status": functional["status"],
                "passed_cases": functional["passed_cases"],
                "evaluated_cases": functional["evaluated_cases"],
                "planned_cases": functional["planned_cases"],
                "passed_steps": functional["passed_steps"],
                "evaluated_steps": functional["evaluated_steps"],
                "attempted_llm_requests": len(row["_calls"]),
                "reported_llm_calls": row["llm_calls"],
                "observed_total_tokens": sum(
                    call["total_tokens"] for call in row["_calls"] if call["total_tokens"] is not None
                )
                if any(call["total_tokens"] is not None for call in row["_calls"])
                else None,
                "missing_usage_calls": sum(call["total_tokens"] is None for call in row["_calls"]),
                "elapsed_seconds": row["elapsed_seconds"],
                "active_result": row["_path"],
            }
        )
        category = classify_agent_error(row)
        if category and category != "not_run":
            failures.append(
                {
                    "condition": row["condition"],
                    "task_id": row["task_id"],
                    "status": row["status"],
                    "category": category,
                    "reason": row.get("reason"),
                    "active_result": row["_path"],
                }
            )
        for case in functional.get("details", []):
            if case.get("status") == "TEST_FAIL":
                functional_failures.append(
                    {
                        "condition": row["condition"],
                        "task_id": row["task_id"],
                        "case_id": case["case_id"],
                        "failed_scan_indices_zero_based": ",".join(
                            str(i) for i, passed in enumerate(case.get("steps_passed", [])) if not passed
                        ),
                        "functional_evidence": functional.get("evidence"),
                        "active_result": row["_path"],
                    }
                )
        for attempt, compilation in enumerate(row["compilation_attempts"]):
            for diagnostic in compilation.get("diagnostics", []):
                if diagnostic.get("severity") in ("Error", "FatalError"):
                    diagnostic_rows.append(
                        {
                            "condition": row["condition"],
                            "task_id": row["task_id"],
                            "attempt": attempt,
                            "severity": diagnostic["severity"],
                            "text": diagnostic["text"],
                            "position": diagnostic.get("position"),
                            "eventual_compilation_success": row["final_compiled"],
                            "active_result": row["_path"],
                        }
                    )
    data = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "campaign": manifest["id"],
        "dataset_sha256": manifest["dataset_sha256"],
        "replications": 1,
        "denominators": {
            "tasks_per_condition": len(tasks),
            "cases_per_condition": sum(len(t["tests"]) for t in tasks.values()),
            "steps_per_condition": sum(len(c["steps"]) for t in tasks.values() for c in t["tests"]),
            "eligible_automatic_simulation_tasks": sum(not eligibility(t) for t in tasks.values()),
        },
        "conditions": conditions,
        "groups": group_rows,
        "integrity_issues": issues,
        "active_result_hashes": raw_hashes,
        "notes": [
            "Unknown provider usage and prices are not imputed.",
            "Saved requests count attempts even if a provider stream fails.",
            "All planned agent failures remain in compilation-rate denominators.",
            "Functional pass rates are conditional on actual evaluation and require coverage beside them.",
            "This is descriptive analysis of one repetition; no significance claim is supported.",
        ],
    }
    output = ROOT / "results/analysis"
    write(output / "analysis.json", data)
    (output / "summary.md").write_text(render_markdown(data), encoding="utf-8")
    (output / "report_tables.tex").write_text(render_latex(data), encoding="utf-8")
    (output / "resource_table.tex").write_text(render_resource_latex(data), encoding="utf-8")
    write_csv(output / "task_analysis.csv", task_rows)
    write_csv(output / "group_analysis.csv", group_rows)
    write_csv(output / "agent_failures.csv", failures)
    write_csv(output / "compiler_errors.csv", diagnostic_rows)
    write_csv(output / "functional_failures.csv", functional_failures)
    complete = all(c["agent_campaign_complete"] for c in conditions)
    if complete:
        compilation_keys = (
            "condition",
            "planned_tasks",
            "agent_attempted_tasks",
            "actual_first_compilations",
            "first_pass_compiled_tasks",
            "final_compiled_tasks",
            "compiler_calls",
            "initial_compile_failures",
            "repair_successes",
        )
        frozen = {
            "campaign": data["campaign"],
            "dataset_sha256": data["dataset_sha256"],
            "conditions": [{key: c[key] for key in compilation_keys} for c in conditions],
            "active_results_and_compiled_sources": [
                {"path": row["_path"], "source_sha256": [a.get("source_sha256") for a in row["compilation_attempts"]]}
                for row in rows
            ],
        }
        snapshot_path = output / "compilation_snapshot.json"
        if snapshot_path.exists() and read(snapshot_path) != frozen:
            raise ValueError("Compilation fields changed after the complete-campaign analysis snapshot")
        if not snapshot_path.exists():
            write(snapshot_path, frozen)
    if not args.no_plots and (complete or args.allow_incomplete):
        make_plots(data, rows, ROOT / "results/figures")
        figures = [
            path
            for stem in ("compilation_rates", "functional_coverage", "agent_latency")
            for extension in ("png", "pdf")
            if (path := ROOT / "results/figures" / (stem + "." + extension)).is_file()
        ]
        write(
            output / "figure_manifest.json",
            {
                "analysis_generated_utc": data["generated_utc"],
                "agent_campaign_complete": complete,
                "functional_evaluated_cases": {c["condition"]: c["evaluated_cases"] for c in conditions},
                "analysis_sha256": hashlib.sha256((output / "analysis.json").read_bytes()).hexdigest(),
                "figures": [
                    {"path": relative(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                    for path in figures
                ],
            },
        )
    print(
        json.dumps(
            {
                "analysis": str(output / "analysis.json"),
                "agent_campaign_complete": complete,
                "planned_runs": len(rows),
                "attempted_runs": sum(c["agent_attempted_tasks"] for c in conditions),
                "integrity_issues": issues,
                "figures_written": not args.no_plots and (complete or args.allow_incomplete),
            },
            indent=2,
        )
    )
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
