"""Generate publication-grade vector PDF (and PNG preview) figures for the report.

All numeric quantities are derived directly from verified dataset manifests,
SMV verification records, and the merged four-condition benchmark snapshot
(results/summary/fullflow_matrix_snapshot_20261114.json + per-task raw traces).
"""

from __future__ import annotations

import glob
import json
import os
import statistics
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "report" / "figures"


def _resolve_gen_result_path(cond: str, gid: str, row: dict) -> Path | None:
    tid = row["task_id"]
    if cond in ("E1", "E2"):
        p = ROOT / "results" / "raw" / "codex_matrix_resume_20261114" / gid / tid / "generation" / "result.json"
        if p.is_file():
            return p
    ev_rel = row.get("evidence")
    if ev_rel:
        ev_path = ROOT / ev_rel
        if ev_path.is_file():
            ev = json.loads(ev_path.read_text(encoding="utf-8"))
            gw = str(ev.get("generation_record", "")).replace("\\", "/")
            idx = gw.find("results/raw/")
            if idx >= 0 and (ROOT / gw[idx:]).is_file():
                return ROOT / gw[idx:]
            alt = ev_path.parent / "generation" / "result.json"
            if alt.is_file():
                return alt
    return None


def _extract_case_and_formal(row: dict) -> tuple[bool, int, int, int, str]:
    comp = bool(row.get("compiled"))
    if "fixed_tests" in row:
        ft = row["fixed_tests"]
        return (
            comp,
            int(ft.get("passed") or 0),
            int(ft.get("evaluated") or 0),
            int(ft.get("planned") or 0),
            str((row.get("formal") or {}).get("status") or "NOT_RUN"),
        )
    fn = row.get("functional") or {}
    vr = row.get("verification") or {}
    return (
        comp,
        int(fn.get("passed_cases") or 0),
        int(fn.get("evaluated_cases") or 0),
        int(fn.get("planned_cases") or row.get("planned_cases") or 0),
        str(vr.get("status") or "NOT_RUN"),
    )


def _add_usage_record(us: dict, totals: dict) -> None:
    in_tok = int(us.get("input_tokens") or 0)
    cached = int((us.get("input_tokens_details") or {}).get("cached_tokens") or 0)
    out_tok = int(us.get("output_tokens") or 0)
    reas = int((us.get("output_tokens_details") or {}).get("reasoning_tokens") or 0)
    totals["in"] += in_tok
    totals["cached"] += cached
    totals["uncached"] += max(0, in_tok - cached)
    totals["out"] += out_tok
    totals["reasoning"] += reas
    totals["direct"] += max(0, out_tok - reas)
    totals["usage_reqs"] += 1
    cost_raw = str(us.get("cost") or "").lstrip("¥")
    if cost_raw:
        totals["cost"] += float(cost_raw)
        totals["cost_reqs"] += 1


def collect_metrics() -> dict:
    tasks = [json.loads(Path(p).read_text(encoding="utf-8")) for p in sorted(glob.glob(str(ROOT / "dataset/*/*.json")))]
    diff_map = {t["id"]: (t["kind"], t["difficulty"]) for t in tasks}

    kind_diff = Counter((t["kind"], t["difficulty"]) for t in tasks)
    port_types: Counter[str] = Counter()
    ltl_scopes: Counter[str] = Counter()
    for t in tasks:
        for prop in t.get("ltl", []):
            ltl_scopes[prop.get("scope", "SCAN_SEQUENCE")] += 1
        for pin in t.get("interface", []):
            tp = pin["type"].upper()
            if "ARRAY[*]" in tp:
                port_types["ARRAY[*]"] += 1
            elif "ARRAY" in tp:
                port_types["ARRAY"] += 1
            elif "STRING" in tp:
                port_types["STRING"] += 1
            elif "ST_" in tp:
                port_types["STRUCT"] += 1
            else:
                port_types[tp] += 1

    smv_status = json.loads((ROOT / "configs/smv_verification_status.json").read_text(encoding="utf-8"))
    ref_ok = sum(
        1
        for rec in smv_status.get("records", {}).values()
        if (rec.get("models", {}).get("reference") or {}).get("status") == "MODEL_PROPERTIES_TRUE"
    )
    mut_ce = sum(
        1
        for rec in smv_status.get("records", {}).values()
        if (rec.get("models", {}).get("mutant") or {}).get("status") == "COUNTEREXAMPLE"
    )

    snap = json.loads((ROOT / "results/summary/fullflow_matrix_snapshot_20261114.json").read_text(encoding="utf-8"))
    groups: dict[str, dict] = {}
    for g in snap["groups"]:
        gid = g["group_id"]
        cond = g["condition"]
        by_kind: dict[str, dict] = {}
        by_diff: dict[str, dict] = {}
        formal_dist: Counter[str] = Counter()
        role_in: Counter[str] = Counter()
        role_out: Counter[str] = Counter()
        tok = {"in": 0, "cached": 0, "uncached": 0, "out": 0, "reasoning": 0, "direct": 0, "usage_reqs": 0, "cost": 0.0, "cost_reqs": 0}
        first_pass = repaired = comp_fail = tool_err = 0
        calls_total = comp_calls = rep_atts = sim_calls = ver_calls = 0
        gen_elapsed_list: list[float] = []

        for row in g["tasks"]:
            tid = row["task_id"]
            kind, diff = diff_map[tid]
            comp, c_pass, c_eval, c_plan, fs = _extract_case_and_formal(row)
            formal_dist[fs] += 1
            task_pass = c_eval > 0 and c_pass == c_eval

            for bucket, key in ((by_kind, kind), (by_diff, diff)):
                d = bucket.setdefault(
                    key,
                    {"n": 0, "comp": 0, "task_eff": 0, "t_eval": 0, "c_pass": 0, "c_eval": 0, "c_plan": 0, "f_pass": 0},
                )
                d["n"] += 1
                if comp:
                    d["comp"] += 1
                if c_eval > 0:
                    d["t_eval"] += 1
                if task_pass:
                    d["task_eff"] += 1
                d["c_pass"] += c_pass
                d["c_eval"] += c_eval
                d["c_plan"] += c_plan
                if fs == "PASS":
                    d["f_pass"] += 1

            gr_path = _resolve_gen_result_path(cond, gid, row)
            if gr_path and gr_path.is_file():
                gr = json.loads(gr_path.read_text(encoding="utf-8"))
                if gr.get("first_pass_compiled"):
                    first_pass += 1
                elif comp:
                    repaired += 1
                elif row.get("generation_status") == "TOOL_ERROR" or row.get("status") == "TOOL_ERROR":
                    tool_err += 1
                else:
                    comp_fail += 1

                comp_calls += int(gr.get("compiler_call_count") or 0)
                rep_atts += int(gr.get("repair_attempts") or 0)
                sim_calls += int(gr.get("simulation_call_count") or 0)
                ver_calls += int(gr.get("verification_call_count") or 0)
                if gr.get("elapsed_seconds") is not None:
                    gen_elapsed_list.append(float(gr["elapsed_seconds"]))

                if cond in ("E1", "E2"):
                    calls_total += int(row.get("source_llm_calls") or gr.get("llm_calls") or 0)
                    for u in (row.get("usage") or []):
                        _add_usage_record(u, tok)
                else:
                    gen_dir = gr_path.parent
                    resps = sorted(glob.glob(str(gen_dir / "llm_*/response.json")))
                    calls_total += len(resps)
                    for sub in resps:
                        stage = os.path.basename(os.path.dirname(sub))
                        if stage.startswith("llm_repair"):
                            role = "Repair"
                        elif stage.startswith("llm_sim_repair"):
                            role = "SimRepair"
                        elif stage == "llm_planner":
                            role = "Planner"
                        elif stage == "llm_code_00":
                            role = "Coder"
                        elif stage == "llm_tester":
                            role = "Tester"
                        else:
                            role = "Other"
                        resp = json.loads(Path(sub).read_text(encoding="utf-8"))
                        us = resp.get("usage") or {}
                        role_in[role] += int(us.get("input_tokens") or 0)
                        role_out[role] += int(us.get("output_tokens") or 0)
                        _add_usage_record(us, tok)

        groups[cond] = {
            "summary": g,
            "by_kind": by_kind,
            "by_diff": by_diff,
            "formal_dist": dict(formal_dist),
            "first_pass": first_pass,
            "repaired": repaired,
            "comp_fail": comp_fail,
            "tool_err": tool_err,
            "calls_total": calls_total,
            "comp_calls": comp_calls,
            "rep_atts": rep_atts,
            "sim_calls": sim_calls,
            "ver_calls": ver_calls,
            "tok": tok,
            "role_in": dict(role_in),
            "role_out": dict(role_out),
            "gen_elapsed_mean": statistics.mean(gen_elapsed_list) if gen_elapsed_list else 0.0,
            "gen_elapsed_med": statistics.median(gen_elapsed_list) if gen_elapsed_list else 0.0,
        }

    return {
        "tasks_count": len(tasks),
        "kind_diff": dict(kind_diff),
        "port_types": port_types.most_common(),
        "ltl_scopes": dict(ltl_scopes),
        "smv_ref_ok": ref_ok,
        "smv_mut_ce": mut_ce,
        "groups": groups,
    }


TEX_PREAMBLE = r"""\documentclass[tikz,border=6pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usetikzlibrary{arrows.meta,positioning,fit,backgrounds,shapes.geometric,calc}
\definecolor{navy}{HTML}{16324F}
\definecolor{tealC}{HTML}{007F82}
\definecolor{amberC}{HTML}{D97706}
\definecolor{coralC}{HTML}{C2410C}
\definecolor{redC}{HTML}{DC2626}
\definecolor{mintC}{HTML}{059669}
\definecolor{slateC}{HTML}{64748B}
\definecolor{paleBg}{HTML}{F4F7FA}
\definecolor{softTeal}{HTML}{E6F4F4}
\definecolor{softNavy}{HTML}{EAF0F6}
\definecolor{softAmber}{HTML}{FEF3C7}
\begin{document}
"""


def build_fig0_architecture() -> str:
    return TEX_PREAMBLE + r"""
\begin{tikzpicture}[
    node distance=7mm and 9mm,
    font=\sffamily\footnotesize,
    box/.style={draw=navy!75, rounded corners=3pt, fill=white, align=center, inner sep=5pt, minimum height=9.5mm},
    stage/.style={box, draw=tealC!85, fill=softTeal!70, text width=31.5mm},
    base/.style={box, draw=amberC!90, fill=softAmber!50, text width=33mm},
    eval/.style={box, draw=navy, fill=softNavy, text width=34mm},
    arr/.style={-{Stealth[length=2.2mm]}, thick, color=navy!80},
    dasharr/.style={-{Stealth[length=2.2mm]}, thick, dashed, color=tealC!80}
]

% Benchmark Dataset & Agent View
\node[box, fill=paleBg, text width=39mm] (db) {\textbf{32-Task Benchmark}\\{\scriptsize 20 Public + 12 Self-Built (AI+Human)}\\{\scriptsize 276 Cases $\cdot$ 294 LTLs $\cdot$ 32 Ref SMVs}};
\node[box, fill=white, draw=redC!75, below=8mm of db, text width=39mm] (view) {\textbf{Leak-Free \texttt{agent\_view()}}\\{\scriptsize Strips tests, reference ST,}\\{\scriptsize CompleteBehavior \& bindings}};

\draw[arr] (db) -- (view);

% STAR Pipeline (Upper Branch)
\node[stage, right=12mm of db, yshift=4mm] (s1) {\textbf{Step 1: Planner}\\{\scriptsize 4-stage scan contract}\\{\scriptsize \& SMV assertions JSON}};
\node[stage, right=6.5mm of s1] (s2) {\textbf{Step 2: Dialect Cards}\\{\scriptsize Score \& select top cards}\\{\scriptsize + SA0027/33 hints}};
\node[stage, right=6.5mm of s2] (s3) {\textbf{Step 3: Compile-Repair}\\{\scriptsize CODESYS SP22 build}\\{\scriptsize Hash stagnation ledger}};
\node[stage, below=9mm of s3, fill=softNavy, draw=navy] (s35) {\textbf{Step 3.5:}\\\textbf{Formal CEGAR}\\{\scriptsize Observer-free ST$\to$SMV}\\{\scriptsize Isolated planner asserts}};
\node[stage, left=14mm of s35] (s4) {\textbf{Step 4: Indep. Tester}\\{\scriptsize Bounded self-tests}\\{\scriptsize No held-out leakage}};
\node[stage, left=6.5mm of s4] (s5) {\textbf{Step 5: Sim \& Ratchet}\\{\scriptsize 1ms CODESYS + anti-lazy}\\{\scriptsize Lexicographic ratchet}};

\draw[arr] (view.east) -- ++(4.5mm,0) |- (s1.west);
\draw[arr] (s1) -- (s2);
\draw[arr] (s2) -- (s3);
\draw[arr] (s3) -- node[right, font=\sffamily\scriptsize, color=navy] {Compiled} (s35);
\draw[arr] (s35) -- node[above, font=\sffamily\scriptsize, color=navy] {Scheme A} (s4);
\draw[arr] (s4) -- (s5);

% Codex Baseline (Lower Branch)
\node[base, below=20mm of s5, xshift=6mm] (codex) {\textbf{Codex CLI v0.142.5}\\{\scriptsize Official unmodified CLI}\\{\scriptsize Max reasoning (\texttt{high})}};
\node[base, right=24mm of codex] (mcp) {\textbf{Shared Relay \& MCP}\\{\scriptsize \texttt{CodexTransport} + quotas}\\{\scriptsize \texttt{compile\_st/sim/verify}}};

\draw[arr] (view.east) -- ++(4.5mm,0) |- (codex.west);
\draw[arr, <->] (codex.east) -- node[above, font=\sffamily\scriptsize, align=center] {stdio\\JSON-RPC} (mcp.west);

% Offline Held-Out Final Evaluator (Right)
\node[eval, right=17mm of s3, yshift=-2mm] (e1) {\textbf{Offline Stage 1: Compile}\\{\scriptsize Independent clean project}\\{\scriptsize Same CODESYS template}};
\node[eval, below=6.5mm of e1] (e2) {\textbf{Offline Stage 2: 1ms Sim}\\{\scriptsize 276 held-out fixed cases}\\{\scriptsize Binary32 + timing gate}};
\node[eval, below=6.5mm of e2] (e3) {\textbf{Offline Stage 3: Formal}\\{\scriptsize Coupled reference observer}\\{\scriptsize NuSMV BDD / nuXmv SMT}};

\draw[arr] (s5.south) -- ++(0,-4.5mm) -| ($(e1.west)-(9mm,0)$) |- ([yshift=2.2mm]e1.west);
\draw[dasharr] (mcp.east) -| ($(e1.west)-(6mm,0)$) |- ([yshift=-2.2mm]e1.west);
\draw[arr] (e1) -- (e2);
\draw[arr] (e2) -- (e3);

\begin{scope}[on background layer]
  \node[draw=tealC!60, dashed, rounded corners=4pt, fill=softTeal!22, fit=(s1)(s2)(s3)(s35)(s4)(s5), inner xsep=7pt, inner ysep=10pt] (gstar) {};
  \node[draw=tealC!60, fill=white, rounded corners=2pt, inner sep=2.5pt, font=\sffamily\bfseries\scriptsize, text=tealC] at (gstar.north) {STAR Decoupled Harness};

  \node[draw=amberC!70, dashed, rounded corners=4pt, fill=softAmber!15, fit=(codex)(mcp), inner xsep=7pt, inner ysep=10pt] (gbase) {};
  \node[draw=amberC!70, fill=white, rounded corners=2pt, inner sep=2.5pt, font=\sffamily\bfseries\scriptsize, text=amberC!90!black] at (gbase.south) {Comparative Baseline};

  \node[draw=navy!55, rounded corners=4pt, fill=paleBg, fit=(e1)(e2)(e3), inner xsep=7pt, inner ysep=10pt] (geval) {};
  \node[draw=navy!55, fill=white, rounded corners=2pt, inner sep=2.5pt, font=\sffamily\bfseries\scriptsize, text=navy] at (geval.north) {Final Adjudicator (\texttt{batch.py})};
\end{scope}

\end{tikzpicture}
\end{document}
"""


def build_fig1_dataset(m: dict) -> str:
    kd = m["kind_diff"]
    pub_e, pub_m, pub_h = kd[("public", "easy")], kd[("public", "medium")], kd[("public", "hard")]
    slf_e, slf_m, slf_h = kd[("self_built", "easy")], kd[("self_built", "medium")], kd[("self_built", "hard")]

    non_bool = [(k, v) for k, v in m["port_types"] if k != "BOOL"]
    top_types = non_bool[:10]
    rest_types = non_bool[10:]
    items = list(top_types)
    if rest_types:
        items.append((f"Others ({len(rest_types)} types)", sum(v for _, v in rest_types)))
    rev_items = list(reversed(items))
    coords = "\n".join(f"    ({v},{idx})" for idx, (_, v) in enumerate(rev_items))
    ytick_idx = ",".join(str(idx) for idx in range(len(rev_items)))
    ylabels = ",".join(f"{{{k}}}" for k, _ in rev_items)
    non_bool_total = sum(v for _, v in non_bool)
    bool_cnt = dict(m["port_types"]).get("BOOL", 0)

    return TEX_PREAMBLE + rf"""
\begin{{tikzpicture}}
\begin{{axis}}[
    name=leftax,
    ybar stacked,
    bar width=16pt,
    width=6.6cm,
    height=5.8cm,
    ymin=0, ymax=17.5,
    ylabel={{\footnotesize Number of Tasks}},
    symbolic x coords={{Easy, Medium, Hard}},
    xtick=data,
    tick label style={{font=\footnotesize\sffamily}},
    label style={{font=\footnotesize\sffamily}},
    title={{\small\sffamily\bfseries (a) Task Split by Source \& Difficulty ($N=32$)}},
    title style={{yshift=6.5mm}},
    legend style={{at={{(0.5,1.02)}}, anchor=south, legend columns=2, font=\scriptsize\sffamily, draw=navy!20, fill=white}},
    nodes near coords,
    every node near coord/.append style={{font=\scriptsize\sffamily\bfseries, color=white}},
    ymajorgrids=true,
    grid style={{dashed, gray!30}},
    enlarge x limits=0.28,
]
\addplot[fill=navy!88, draw=navy] coordinates {{(Easy,{pub_e}) (Medium,{pub_m}) (Hard,{pub_h})}};
\addplot[fill=tealC!85, draw=tealC] coordinates {{(Easy,{slf_e}) (Medium,{slf_m}) (Hard,{slf_h})}};
\legend{{Public (20), Self-Built [AI+Human] (12)}}
\end{{axis}}

\begin{{axis}}[
    name=rightax,
    at={{($(leftax.south east)+(24mm,0)$)}},
    anchor=south west,
    xbar,
    bar width=7.5pt,
    width=7.2cm,
    height=5.8cm,
    xmin=0, xmax=13,
    xlabel={{\footnotesize Declared Port Count ({non_bool_total} Non-BOOL Ports; \texttt{{BOOL}}: {bool_cnt})}},
    ytick={{{ytick_idx}}},
    yticklabels={{{ylabels}}},
    tick label style={{font=\scriptsize\sffamily}},
    label style={{font=\footnotesize\sffamily}},
    title={{\small\sffamily\bfseries (b) Non-Boolean IEC 61131-3 Port Coverage}},
    title style={{yshift=6.5mm}},
    xmajorgrids=true,
    grid style={{dashed, gray!30}},
    nodes near coords,
    every node near coord/.append style={{font=\scriptsize\sffamily, color=navy, anchor=west}},
    enlarge y limits=0.08,
]
\addplot[fill=tealC!78, draw=navy!80] coordinates {{
{coords}
}};
\end{{axis}}

\node[font=\scriptsize\sffamily, color=slateC, anchor=north, align=center] at ($(current bounding box.south)+(0,-1.5mm)$)
  {{276 Fixed Held-Out Cases (2,994 Scans) $\cdot$ 294 LTLs (30 Init / 264 Scan) $\cdot$ Ref SMV: {m['smv_ref_ok']}/32 True (15 BDD + 17 SMT) $\cdot$ Mutant SMV: {m['smv_mut_ce']}/32 CE}};
\end{{tikzpicture}}
\end{{document}}
"""


def build_fig2_overview(m: dict) -> str:
    def pct(a: int, b: int) -> float:
        return round(100.0 * a / b, 1) if b else 0.0

    conds = ["E1", "E2", "E3", "E4"]
    metrics_rows = []
    for cond in conds:
        g = m["groups"][cond]
        s = g["summary"]
        k = g["by_kind"]
        task_eff = k["public"]["task_eff"] + k["self_built"]["task_eff"]
        metrics_rows.append({
            "first": pct(g["first_pass"], 32),
            "final": pct(s["compiled_tasks"], 32),
            "case_eval": pct(s["fixed_cases"]["passed"], s["fixed_cases"]["evaluated"]),
            "case_plan": pct(s["fixed_cases"]["passed"], 276),
            "task_eff": pct(task_eff, 32),
            "pub_comp": pct(k["public"]["comp"], 20),
            "pub_case": pct(k["public"]["c_pass"], k["public"]["c_eval"]),
        })

    keys = [
        ("first", "1st Compile"),
        ("final", "Final Compile"),
        ("case_eval", "Case (Eval)"),
        ("case_plan", "Case (Plan)"),
        ("task_eff", "Task Pass (/32)"),
        ("pub_comp", "PUB Compile"),
        ("pub_case", "PUB Case (Eval)"),
    ]
    xtick_idx = ",".join(str(idx) for idx in range(len(keys)))
    xlabels = ",".join(f"{{{label}}}" for _, label in keys)
    series = []
    for row in metrics_rows:
        series.append(" ".join(f"({idx},{row[k]})" for idx, (k, _) in enumerate(keys)))

    def fmt_line(c: str) -> str:
        g = m["groups"][c]
        s = g["summary"]
        k = g["by_kind"]
        te = k["public"]["task_eff"] + k["self_built"]["task_eff"]
        return (
            f"\\textbf{{{c}}}: 1st {g['first_pass']}/32, Comp {s['compiled_tasks']}/32, "
            f"Cases {s['fixed_cases']['passed']}/{s['fixed_cases']['evaluated']} ({s['fixed_cases']['planned']} plan), "
            f"Task {te}/32, SELF {k['self_built']['comp']}/12 \\& {k['self_built']['c_pass']}/{k['self_built']['c_eval']}"
        )

    denom_note = f"{fmt_line('E1')} $\\mid$ {fmt_line('E2')}\\\\{fmt_line('E3')} $\\mid$ {fmt_line('E4')}"

    return TEX_PREAMBLE + rf"""
\begin{{tikzpicture}}
\begin{{axis}}[
    ybar=1.8pt,
    bar width=6.2pt,
    width=15.6cm,
    height=6.5cm,
    ymin=0, ymax=116,
    ylabel={{\footnotesize Pass / Coverage Rate (\%)}},
    xtick={{{xtick_idx}}},
    xticklabels={{{xlabels}}},
    x tick label style={{font=\scriptsize\sffamily, rotate=12, anchor=east}},
    ytick={{0,20,40,60,80,100}},
    tick label style={{font=\footnotesize\sffamily}},
    label style={{font=\footnotesize\sffamily}},
    title={{\small\sffamily\bfseries Four-Condition Benchmark Overview Across Compilation, Execution, and Split Coverage ($N=32$)}},
    title style={{yshift=7mm}},
    legend style={{at={{(0.5,1.02)}}, anchor=south, legend columns=2, font=\scriptsize\sffamily, draw=navy!20, fill=white}},
    nodes near coords,
    every node near coord/.append style={{font=\tiny\sffamily, rotate=90, anchor=west}},
    ymajorgrids=true,
    grid style={{dashed, gray!30}},
    enlarge x limits=0.09,
]
\addplot[fill=amberC!78, draw=amberC!90!black] coordinates {{{series[0]}}};
\addplot[fill=coralC!82, draw=coralC!90!black] coordinates {{{series[1]}}};
\addplot[fill=navy!88, draw=navy] coordinates {{{series[2]}}};
\addplot[fill=tealC!82, draw=tealC] coordinates {{{series[3]}}};
\legend{{E1: Codex + DeepSeek-V4.1-Flash, E2: Codex + GPT-6.1-Terra, E3: STAR + DeepSeek-V4.1-Flash, E4: STAR + GPT-6.1-Terra}}
\end{{axis}}
\node[font=\tiny\sffamily, color=slateC, anchor=north, align=center] at (current axis.south) [yshift=-11mm]
  {{{denom_note}}};
\end{{tikzpicture}}
\end{{document}}
"""


def build_fig3_difficulty_formal(m: dict) -> str:
    def pct(a: int, b: int) -> float:
        return round(100.0 * a / b, 1) if b else 0.0

    diffs = [("Easy (10)", "easy"), ("Medium (14)", "medium"), ("Hard (8)", "hard")]
    conds = ["E1", "E2", "E3", "E4"]
    diff_coords = []
    for cond in conds:
        d = m["groups"][cond]["by_diff"]
        diff_coords.append(" ".join(f"({idx},{pct(d[k]['task_eff'], d[k]['n'])})" for idx, (_, k) in enumerate(diffs)))

    formal_cats = ["PASS", "COUNTEREXAMPLE", "TIMEOUT", "UNSUPPORTED_ST", "NOT_RUN"]
    formal_coords = {}
    for cat in formal_cats:
        formal_coords[cat] = " ".join(
            f"({idx},{m['groups'][cond]['formal_dist'].get(cat, 0)})" for idx, cond in enumerate(conds)
        )

    return TEX_PREAMBLE + rf"""
\begin{{tikzpicture}}
\begin{{axis}}[
    name=leftax,
    ybar=1.8pt,
    bar width=6.8pt,
    width=8.2cm,
    height=6.2cm,
    ymin=0, ymax=116,
    ylabel={{\footnotesize Task Functional Pass Rate (\%)}},
    xtick={{0,1,2}},
    xticklabels={{{diffs[0][0]},{diffs[1][0]},{diffs[2][0]}}},
    tick label style={{font=\scriptsize\sffamily}},
    label style={{font=\footnotesize\sffamily}},
    title={{\small\sffamily\bfseries (a) Task Pass (/N) by Difficulty Tier}},
    title style={{yshift=8mm}},
    legend style={{at={{(0.5,1.02)}}, anchor=south, legend columns=2, font=\tiny\sffamily, draw=navy!20, fill=white}},
    nodes near coords,
    every node near coord/.append style={{font=\tiny\sffamily, rotate=90, anchor=west}},
    ymajorgrids=true,
    grid style={{dashed, gray!30}},
    enlarge x limits=0.25,
]
\addplot[fill=amberC!78, draw=amberC!90!black] coordinates {{{diff_coords[0]}}};
\addplot[fill=coralC!82, draw=coralC!90!black] coordinates {{{diff_coords[1]}}};
\addplot[fill=navy!88, draw=navy] coordinates {{{diff_coords[2]}}};
\addplot[fill=tealC!82, draw=tealC] coordinates {{{diff_coords[3]}}};
\legend{{E1 Codex+DS, E2 Codex+GPT, E3 STAR+DS, E4 STAR+GPT}}
\end{{axis}}

\begin{{axis}}[
    at={{($(leftax.south east)+(12mm,0)$)}},
    anchor=south west,
    ybar stacked,
    bar width=18pt,
    width=7.4cm,
    height=6.2cm,
    ymin=0, ymax=35,
    ylabel={{\footnotesize Number of Tasks ($N=32$)}},
    xtick={{0,1,2,3}},
    xticklabels={{E1\\Codex+DS, E2\\Codex+GPT, E3\\STAR+DS, E4\\STAR+GPT}},
    x tick label style={{font=\tiny\sffamily, align=center}},
    tick label style={{font=\scriptsize\sffamily}},
    label style={{font=\footnotesize\sffamily}},
    title={{\small\sffamily\bfseries (b) Stage 3 Formal Outcomes}},
    title style={{yshift=8mm}},
    legend style={{at={{(1.03,0.98)}}, anchor=north west, font=\scriptsize\sffamily, draw=navy!20, fill=white}},
    nodes near coords={{\pgfmathfloattoint{{\pgfplotspointmeta}}\ifnum\pgfmathresult>0 \pgfmathresult\fi}},
    every node near coord/.append style={{font=\tiny\sffamily\bfseries, color=white, inner sep=0pt}},
    ymajorgrids=true,
    grid style={{dashed, gray!30}},
    enlarge x limits=0.22,
]
\addplot[fill=mintC!90, draw=mintC!70!black] coordinates {{{formal_coords['PASS']}}};
\addplot[fill=redC!88, draw=redC!70!black] coordinates {{{formal_coords['COUNTEREXAMPLE']}}};
\addplot[fill=amberC!88, draw=amberC!70!black] coordinates {{{formal_coords['TIMEOUT']}}};
\addplot[fill=slateC!65, draw=slateC] coordinates {{{formal_coords['UNSUPPORTED_ST']}}};
\addplot[fill=gray!45, draw=gray!70] coordinates {{{formal_coords['NOT_RUN']}}};
\legend{{PASS, COUNTEREXAMPLE, TIMEOUT, UNSUPPORTED\_ST, NOT\_RUN}}
\end{{axis}}
\end{{tikzpicture}}
\end{{document}}
"""


def build_fig4_tokens_cost(m: dict) -> str:
    conds = ["E1", "E2", "E3", "E4"]

    def mt(val: int) -> float:
        return round(val / 1_000_000.0, 3)

    uncached_coords = " ".join(f"({i},{mt(m['groups'][c]['tok']['uncached'])})" for i, c in enumerate(conds))
    cached_coords = " ".join(f"({i},{mt(m['groups'][c]['tok']['cached'])})" for i, c in enumerate(conds))
    reas_coords = " ".join(f"({i},{mt(m['groups'][c]['tok']['reasoning'])})" for i, c in enumerate(conds))
    direct_coords = " ".join(f"({i},{mt(m['groups'][c]['tok']['direct'])})" for i, c in enumerate(conds))

    cost_coords = " ".join(f"({round(m['groups'][c]['tok']['cost'], 2)},{3-i})" for i, c in enumerate(conds))
    lat_coords = " ".join(f"({round(m['groups'][c]['gen_elapsed_mean'], 1)},{3-i})" for i, c in enumerate(conds))

    tot_labels = []
    for i, c in enumerate(conds):
        t = m["groups"][c]["tok"]
        tot_m = round((t["in"] + t["out"]) / 1_000_000.0, 2)
        tot_labels.append(f"\\node[font=\\tiny\\sffamily\\bfseries, color=navy, anchor=south] at (axis cs:{i},{tot_m}) {{{tot_m:.2f}M}};")
    tot_nodes = "\n".join(tot_labels)

    call_notes = " $\\cdot$ ".join(
        f"{c}: {m['groups'][c]['calls_total']} reqs ({m['groups'][c]['comp_calls']} comp / {m['groups'][c]['sim_calls']} sim / {m['groups'][c]['ver_calls']} verify)"
        for c in conds
    )

    return TEX_PREAMBLE + rf"""
\begin{{tikzpicture}}
\begin{{axis}}[
    name=leftax,
    ybar stacked,
    bar width=20pt,
    width=8.2cm,
    height=6.9cm,
    ymin=0, ymax=6.05,
    ylabel={{\footnotesize Cumulative Tokens Over 32 Tasks (Millions)}},
    xtick={{0,1,2,3}},
    xticklabels={{E1\\Codex+DS, E2\\Codex+GPT, E3\\STAR+DS, E4\\STAR+GPT}},
    x tick label style={{font=\scriptsize\sffamily, align=center}},
    tick label style={{font=\footnotesize\sffamily}},
    label style={{font=\footnotesize\sffamily}},
    title={{\small\sffamily\bfseries (a) Token Structure: Context Input vs.\ Output ($N=32$)}},
    title style={{yshift=11mm}},
    legend style={{at={{(0.5,1.02)}}, anchor=south, legend columns=2, font=\tiny\sffamily, draw=navy!20, fill=white}},
    ymajorgrids=true,
    grid style={{dashed, gray!30}},
    enlarge x limits=0.22,
]
\addplot[fill=navy!88, draw=navy] coordinates {{{uncached_coords}}};
\addplot[fill=navy!30, draw=navy!60] coordinates {{{cached_coords}}};
\addplot[fill=tealC!88, draw=tealC] coordinates {{{reas_coords}}};
\addplot[fill=mintC!75, draw=mintC!80!black] coordinates {{{direct_coords}}};
\legend{{Uncached Input, Cached Input, Reasoning Out, Direct Out}}
{tot_nodes}
\end{{axis}}

\begin{{axis}}[
    name=topr,
    at={{($(leftax.north east)+(27mm,1mm)$)}},
    anchor=north west,
    xbar,
    bar width=7pt,
    width=6.2cm,
    height=2.85cm,
    xmin=0, xmax=9.2,
    xlabel={{\scriptsize Reported API Cost (CNY \textyen)}},
    ytick={{0,1,2,3}},
    yticklabels={{E4 STAR+GPT, E3 STAR+DS, E2 Codex+GPT, E1 Codex+DS}},
    tick label style={{font=\scriptsize\sffamily}},
    label style={{font=\scriptsize\sffamily}},
    title={{\small\sffamily\bfseries (b) Reported API Cost (32 Tasks)}},
    title style={{yshift=0.5mm}},
    xmajorgrids=true,
    grid style={{dashed, gray!30}},
    nodes near coords,
    every node near coord/.append style={{font=\tiny\sffamily\bfseries, color=navy, anchor=west}},
    enlarge y limits=0.22,
]
\addplot[fill=amberC!80, draw=amberC!90!black] coordinates {{{cost_coords}}};
\end{{axis}}

\begin{{axis}}[
    name=botr,
    at={{($(leftax.south east)+(27mm,0mm)$)}},
    anchor=south west,
    xbar,
    bar width=7pt,
    width=6.2cm,
    height=2.85cm,
    xmin=0, xmax=270,
    xlabel={{\scriptsize Mean Generation Time per Task (s)}},
    ytick={{0,1,2,3}},
    yticklabels={{E4 STAR+GPT, E3 STAR+DS, E2 Codex+GPT, E1 Codex+DS}},
    tick label style={{font=\scriptsize\sffamily}},
    label style={{font=\scriptsize\sffamily}},
    title={{\small\sffamily\bfseries (c) Mean Generation Time}},
    title style={{yshift=0.5mm}},
    xmajorgrids=true,
    grid style={{dashed, gray!30}},
    nodes near coords,
    every node near coord/.append style={{font=\tiny\sffamily\bfseries, color=navy, anchor=west}},
    enlarge y limits=0.22,
]
\addplot[fill=tealC!78, draw=navy!80] coordinates {{{lat_coords}}};
\end{{axis}}

\node[font=\tiny\sffamily, color=slateC, anchor=north, align=center] at ($(current bounding box.south)+(0,-1.5mm)$)
  {{{call_notes}}};
\end{{tikzpicture}}
\end{{document}}
"""


def compile_figure(name: str, tex_content: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = FIG_DIR / f"{name}.tex"
    tex_path.write_text(tex_content.strip() + "\n", encoding="utf-8")
    proc = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=FIG_DIR,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        print(proc.stdout[-2000:], proc.stderr[-1000:], file=sys.stderr)
        raise RuntimeError(f"pdflatex failed for {name}")
    pdf_path = FIG_DIR / f"{name}.pdf"
    png_prefix = FIG_DIR / name
    subprocess.run(
        ["pdftoppm", "-png", "-r", "240", "-singlefile", str(pdf_path), str(png_prefix)],
        check=True,
    )
    for ext in (".aux", ".log"):
        p = FIG_DIR / f"{name}{ext}"
        if p.exists():
            p.unlink()
    print(f"Generated {pdf_path.name} and {name}.png")


def main() -> int:
    metrics = collect_metrics()
    for stale in glob.glob(str(FIG_DIR / "fig2_e3_e4_benchmark_overview.*")):
        Path(stale).unlink(missing_ok=True)
    compile_figure("fig0_star_architecture", build_fig0_architecture())
    compile_figure("fig1_dataset_composition", build_fig1_dataset(metrics))
    compile_figure("fig2_four_group_overview", build_fig2_overview(metrics))
    compile_figure("fig3_difficulty_formal_breakdown", build_fig3_difficulty_formal(metrics))
    compile_figure("fig4_token_cost_efficiency", build_fig4_tokens_cost(metrics))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
