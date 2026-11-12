"""Symbol and alias glossary builder for the Web UI specification inspector.

Classifies every identifier appearing in LTL formulas and task contracts into:
- input: sampled INPUT pin I[k]
- output: observed OUTPUT pin O[k]
- persistent_inout: caller-owned IN_OUT persistent storage
- obs_history: previous observed output history O[k-1]
- ghost_state: input-driven reference pre/post state, edge memory I[k-1], or timer state
- alias: pure combinational / temporal / contract macro alias
"""
from __future__ import annotations

import json
import re
from typing import Any

CATEGORY_LABELS_ZH = {
    "input": "输入变量 (INPUT)",
    "output": "输出变量 (OUTPUT)",
    "persistent_inout": "持久化存储 (IN_OUT)",
    "obs_history": "上拍实测历史 (O[k-1])",
    "ghost_state": "跨拍参考/幽灵状态",
    "alias": "规约别名 / 原子命题",
}

_GHOST_STATE_NAMES = {
    "Spre",
    "Spost",
    "phase",
    "phase0_idle",
    "previous-input",
    "done_phase",
    "move_phase",
    "wait_phase",
    "phase_move",
    "phase_wait",
    "qIdle",
    "qMoving",
    "qComplete",
    "qFault",
    "qPhase",
    "qRedLast",
    "qGreenLast",
    "qAmber",
    "qExtend",
    "qClamp",
    "qRelease",
    "qRetract",
    "qDone",
    "qRunning",
    "qWait",
    "qLocked",
    "refAttempts",
    "retryDue",
    "busy",
    "modeChanged",
    "no_mode",
    "mode_initial",
    "start_memory",
    "history",
    "historyAfter",
    "length",
    "storage",
    "currentStation",
    "targetStation",
    "demand",
    "cooldownDone",
    "heatLimitReached",
    "delayDone",
    "gapQualified",
    "mature",
    "startup",
    "hold",
    "timing",
    "runPrev",
    "windowChanged",
    "same",
    "same_stats",
    "same_time",
    "same_temp",
    "same_input",
    "same_output",
    "sameAlarms",
    "unchangedMean",
    "completedServed",
}

_OBS_HISTORY_NAMES = {
    "pre-output",
}

_COMMON_ZH: dict[str, tuple[str, str, str | None]] = {
    "CompleteBehaviorV2": (
        "完整单拍行为关系 (V2)",
        "固定 Python 参考转移 T 与初始状态共同定义的完整扫描判定谓词：输入 I[k] 推进参考状态 Sref[k]->Sref[k+1] 与预期输出 E[k]，要求实际输出 O[k] 的所有受约束字段均严格匹配；绝对不允许用实际输出 O 反向推进参考状态。",
        "参考状态 Sref 跨拍演进且仅由采样输入驱动，防止与候选 ST 内部变量混淆。",
    ),
    "init": (
        "初始实例观测条件",
        "指首次扫描 (k=0) 调用之前的独立初始实例快照：检查参考前态与所有已声明 OUTPUT 变量在未调用前的默认初值。",
        "仅约束首次扫描前（pre-invocation）的初始存储与输出零态，不要求运行期间恒保持。",
    ),
    "first": (
        "首拍扫描标志 (k=0)",
        "表示当前为第 0 拍正式调用（k=0），区别于调用前的初始观测 init。",
        None,
    ),
    "TimeTick": (
        "物理时间推进条件",
        "相邻两拍之间物理累计时间跨过至少 1ms 整数格：floor(t[k]/1ms) > floor(t[k-1]/1ms)，首拍 t[0]=0, TimeTick[0]=FALSE。G(F(TimeTick)) 表示物理时钟持续前进、不出现无限零步长停滞。",
        "依赖跨拍累计时间基准 clk/t[k]；k=0 首拍忽略 dt_ms[0]，时钟固定自 0 起步。",
    ),
    "Spre": (
        "输入驱动参考前态 Sref[k]",
        "本拍执行前的参考状态 Sref[k]，由上一拍参考转移推进得到；属于规范侧“幽灵状态（ghost state）”，不直接断言候选 ST 内部变量名。",
        "高危跨拍状态：仅受 I[k-1] 等历史输入序列影响，绝不读取候选实际输出 O[k-1]。",
    ),
    "Spost": (
        "输入驱动参考后态 Sref[k+1]",
        "本拍读取 I[k] 完成单拍参考转移后的参考状态 Sref[k+1]；下一拍 LTL X(...) 时刻的 Spre 即为此刻 Spost。",
        "高危跨拍状态：与实测后拍绑定区分，不可混用为候选内部变量。",
    ),
    "pre-output": (
        "上拍实测输出前态 O[k-1]",
        "指上一次扫描结束时观测到的实际 OUTPUT 值 O[k-1]（首拍取显式声明初值）；对 IN_OUT 参数则指调用方传入的当前值 I[k]。",
        "实测历史绑定：记录真实被测对象上拍输出，不可被参考模型覆盖。",
    ),
    "previous-input": (
        "上拍采样输入 I[k-1]",
        "上一次扫描采样到的输入值（首拍默认 FALSE / 0），每拍结束后无条件更新（含复位/无效输入/故障拍），用于边沿触发判断。",
        "边沿记忆状态：必须在每拍（含复位与异常拍）固定更新，不能在故障拍跳过锁存。",
    ),
    "TIME": ("IEC 32位时间类型", "IEC 61131-3 标准 32 位时间字面量类型，如 TIME#5s。", None),
    "LTIME": ("IEC 64位纳秒时间类型", "IEC 61131-3 / CODESYS 64 位高精度时间类型，如 LTIME#500h。", None),
    "TIME_TO_LTIME": ("时间类型转换函数", "IEC 转换函数：将 TIME 转换为 LTIME 精度进行累计或比较。", None),
    "h": ("小时单位", "时间字面量单位后缀（小时，1h = 3,600,000 ms）。", None),
    "ms": ("毫秒单位", "时间字面量单位后缀（毫秒）。", None),
}


def _describe_history_binding(name: str, hb: dict[str, Any]) -> tuple[str, str, str]:
    kind = hb.get("kind", "")
    source = hb.get("source", "")
    initial = hb.get("initial")
    update = hb.get("update", "")
    if kind == "previous_observed_output":
        return (
            "obs_history",
            f"上拍实测输出 ({source})",
            f"记录上一拍真实观测输出 {source}；初值={json.dumps(initial, ensure_ascii=False)}。每拍比对后更新：{update}",
            f"实测历史状态：初值={json.dumps(initial, ensure_ascii=False)}，仅在每拍比对后存入实际观测值，严禁改写入参考幽灵状态。",
        )
    return (
        "ghost_state",
        f"上拍输入边沿记忆 ({source})",
        f"记录上一拍采样输入 {source}；初值={json.dumps(initial, ensure_ascii=False)}。更新规则：{update}",
        f"输入记忆状态：初值={json.dumps(initial, ensure_ascii=False)}，每拍无论是否报错/复位/无效均须更新，否则会漏检或误报边沿。",
    )


def _format_source_def(raw: Any) -> str:
    if isinstance(raw, str):
        return raw
    return json.dumps(raw, ensure_ascii=False)


def _classify_alias(name: str, task: dict[str, Any], hbs: dict[str, Any]) -> str:
    if name in hbs:
        return "obs_history" if hbs[name].get("kind") == "previous_observed_output" else "ghost_state"
    if name in _OBS_HISTORY_NAMES:
        return "obs_history"
    if name in _GHOST_STATE_NAMES or name.startswith("PrevBit"):
        return "ghost_state"
    ap_val = str((task.get("atomic_propositions") or {}).get(name, ""))
    if any(marker in ap_val for marker in ("Spre.", "Spost.", "Sref.", "pre-phase", "post-phase", "pre-database", "pre-queue", "pre-count", "pre-runtime", "pre-firingTemp", "pre-busy", "pre-sequence", "retained", "latched_batch_mode")):
        return "ghost_state"
    if "previous_observed_output" in ap_val or "O[k-1]" in ap_val:
        return "obs_history"
    return "alias"


def build_symbol_glossary(task: dict[str, Any], review: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    """Build deterministic, complete symbol/alias glossary for /api/task."""
    glossary: dict[str, dict[str, Any]] = {}
    iface_zh = (review or {}).get("interface_zh") or {}
    aliases_zh = (review or {}).get("aliases_zh") or {}
    ns = task.get("normalized_specification") or {}
    hbs = ns.get("history_bindings") or {}
    abs_map = ns.get("auxiliary_state_bindings") or {}
    fc_map = ns.get("finite_conjunctions") or {}
    ap_map = task.get("atomic_propositions") or {}

    # 1. Interface variables (INPUT, OUTPUT, IN_OUT)
    for pin in task.get("interface", []):
        name = pin["name"]
        direction = pin.get("direction", "INPUT")
        iec_type = pin.get("type", "")
        src_desc = pin.get("description") or pin.get("comment") or ""
        zh_desc = iface_zh.get(name) or src_desc or name

        if direction == "IN_OUT":
            cat = "persistent_inout"
            is_persistent = True
            warn_zh = f"IN_OUT 引用传递变量（{iec_type}）：跨扫描周期在调用方持久保存；空闲、禁用或报错拍必须保持原有内容不被清零，严禁传入常量。"
        elif direction == "OUTPUT":
            cat = "output"
            is_persistent = False
            warn_zh = None
        else:
            cat = "input"
            is_persistent = False
            warn_zh = None

        glossary[name] = {
            "name": name,
            "category": cat,
            "category_zh": CATEGORY_LABELS_ZH[cat],
            "type": iec_type,
            "label_zh": f"{name}（{cat == 'persistent_inout' and '持久 IN_OUT' or direction}）",
            "is_persistent": is_persistent,
            "definition_zh": zh_desc,
            "definition_source": src_desc,
            "persistence_warning_zh": warn_zh,
        }

    # 2. Combined non-interface candidates from ap, hb, ab, fc
    candidate_names: list[str] = []
    for source_dict in (hbs, fc_map, abs_map, ap_map):
        for k in source_dict:
            if k not in glossary and k not in candidate_names:
                candidate_names.append(k)

    # Ensure formula literals like PUB004 TIME/LTIME/h/ms or PUB007 base array tokens are included
    formula_text = " ".join(p.get("formula", "") for p in task.get("ltl", []))
    for tok in re.findall(r"[A-Za-z_][A-Za-z_0-9.]*", formula_text):
        if tok not in {"G", "F", "X", "U", "R", "V", "W", "TRUE", "FALSE", "AND", "OR", "NOT"} and not tok.isdigit():
            if tok not in glossary and tok not in candidate_names:
                candidate_names.append(tok)

    # Index stripped base names like runPrev from runPrev[i]
    indexed_sources: dict[str, tuple[str, Any]] = {}
    for k, v in ap_map.items():
        m = re.match(r"^([A-Za-z_][A-Za-z_0-9]*)\[[A-Za-z0-9_]+\]$", k)
        if m and m.group(1) not in ap_map:
            indexed_sources[m.group(1)] = (k, v)

    for raw_name in candidate_names:
        if raw_name in glossary:
            continue
        custom = aliases_zh.get(raw_name) or {}
        src_val = ap_map.get(raw_name) or fc_map.get(raw_name) or abs_map.get(raw_name) or (indexed_sources.get(raw_name, (None, ""))[1])
        src_text = _format_source_def(src_val) if src_val not in (None, "") else ""

        if raw_name in hbs:
            cat, auto_label, auto_zh, auto_warn = _describe_history_binding(raw_name, hbs[raw_name])
            typ_str = f"历史绑定 · {hbs[raw_name].get('source', '')}"
        elif raw_name in _COMMON_ZH:
            auto_label, auto_zh, auto_warn = _COMMON_ZH[raw_name]
            cat = _classify_alias(raw_name, task, hbs)
            typ_str = "规范元符号" if cat != "ghost_state" else "跨拍参考状态 / 计时"
        elif m := re.match(r"^(Prev|Value)Bit(\d+)$", raw_name):
            is_prev = m.group(1) == "Prev"
            bit = int(m.group(2))
            cat = "ghost_state" if is_prev else "alias"
            auto_label = f"{'上拍输入' if is_prev else '本拍输入'} Bit {bit}"
            auto_zh = (
                f"上一拍 I[k-1].value 的第 {bit} 位（0..31）；首拍 pre=0，每拍更新为 I[k].value。"
                if is_prev
                else f"本拍无符号 32 位输入 I[k].value 的第 {bit} 位（BOOL）。"
            )
            auto_warn = "跨拍输入位记忆：首拍全 0，每拍无条件刷新。" if is_prev else None
            typ_str = f"BOOL 展开位 (bit {bit})"
        elif m := re.match(r"^TopThree([1-5])$", raw_name):
            idx = m.group(1)
            cat = "alias"
            auto_label = f"自动前三优先位 · 泵{idx}"
            auto_zh = f"判断第 {idx} 号泵（下标 {int(idx)-1}）按优先级降序（同优先级小下标优先）是否位于前 3 名。"
            auto_warn = None
            typ_str = "布尔优先判定别名"
        elif m := re.match(r"^AllChannels_(P\d+)$", raw_name):
            pid = m.group(1)
            cat = "alias"
            auto_label = f"全通道有限合取 · {pid}"
            auto_zh = f"对 j = 0 .. len(I[k].channels)-1 展开的有限合取谓词，要求每个通道均满足 {pid}（0 通道时真空为 TRUE）。"
            auto_warn = None
            typ_str = "有限全称合取宏"
        else:
            cat = _classify_alias(raw_name, task, hbs)
            auto_label = custom.get("label_zh") or raw_name
            auto_zh = custom.get("description_zh") or src_text or raw_name
            auto_warn = custom.get("persistence_note_zh")
            if cat == "ghost_state" and not auto_warn:
                auto_warn = "跨拍状态/阶段绑定：请区分扫描前态 Spre 与扫描后更新，严禁受候选内部私有状态名污染。"
            elif cat == "obs_history" and not auto_warn:
                auto_warn = "上拍实测输出绑定 O[k-1]：初值在首拍前确定，每拍仅由真实输出更新。"
            typ_str = (
                "有限合取宏"
                if raw_name in fc_map
                else ("跨拍参考/内存状态" if cat == "ghost_state" else ("历史输出绑定" if cat == "obs_history" else "规约别名 / 命题"))
            )

        glossary[raw_name] = {
            "name": raw_name,
            "category": cat,
            "category_zh": CATEGORY_LABELS_ZH[cat],
            "type": custom.get("type_zh") or typ_str,
            "label_zh": custom.get("label_zh") or auto_label,
            "is_persistent": cat in {"persistent_inout", "ghost_state", "obs_history"},
            "definition_zh": custom.get("description_zh") or auto_zh,
            "definition_source": src_text or (f"{raw_name}: {indexed_sources[raw_name][0]}" if raw_name in indexed_sources else raw_name),
            "persistence_warning_zh": custom.get("persistence_note_zh") or auto_warn,
        }

    return glossary
