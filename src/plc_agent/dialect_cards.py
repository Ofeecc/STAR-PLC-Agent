from __future__ import annotations

import copy
from typing import Any

DIALECT_CARDS: dict[str, dict[str, str]] = {
    "variant_ref": {
        "id": "variant_ref",
        "title": "CODESYS VARIANT and __VARINFO Generic Typing",
        "body": """// VARIANT input/output syntax and __VARINFO generic typing
VAR_IN_OUT
    item : VARIANT;
END_VAR
VAR
    info : __SYSTEM.VAR_INFO;
END_VAR
info := __VARINFO(item);
IF info.TypeClass = __SYSTEM.TYPE_CLASS.TYPE_INT THEN
    // Inspect or process dynamically typed variable
END_IF;""",
    },
    "var_length_array": {
        "id": "var_length_array",
        "title": "Variable-Length Arrays (ARRAY[*] OF <type>) with Bounds",
        "body": """// Variable-length array ARRAY[*] OF <type> with LOWER_BOUND/UPPER_BOUND
VAR_IN_OUT
    arr : ARRAY[*] OF INT;
END_VAR
VAR
    lb, ub, i : DINT;
END_VAR
lb := LOWER_BOUND(arr, 1);
ub := UPPER_BOUND(arr, 1);
FOR i := lb TO ub DO
    arr[i] := arr[i] + 1;
END_FOR;""",
    },
    "ltime_ops": {
        "id": "ltime_ops",
        "title": "LTIME and TIME Literals and Operations",
        "body": """// TIME (T#... 32-bit) and LTIME (LTIME#... 64-bit nanosecond) literals & ops
VAR
    tCycle : TIME := T#100ms;
    ltAcc : LTIME := LTIME#0ms;
    ltLimit : LTIME := LTIME#10s;
END_VAR
ltAcc := ltAcc + LTIME#100ms;
IF ltAcc >= ltLimit THEN
    ltAcc := LTIME#0ms;
END_IF;""",
    },
    "ton_timer": {
        "id": "ton_timer",
        "title": "Standard IEC TON Timer Block Invocation",
        "body": """// Standard IEC TON timer block declaration, invocation, and reading Q/ET
VAR
    timer : TON;
END_VAR
timer(IN := runCondition, PT := T#2s);
IF timer.Q THEN
    // Timer expired; timer.ET holds elapsed time
END_IF;
IF NOT runCondition THEN
    timer(IN := FALSE); // Reset timer
END_IF;""",
    },
    "edge_detection": {
        "id": "edge_detection",
        "title": "Edge Detection (R_TRIG, F_TRIG and Manual Pattern)",
        "body": """// R_TRIG / F_TRIG function blocks and manual edge detection pattern
VAR
    rTrig : R_TRIG;
    prevSignal : BOOL;
    rising : BOOL;
END_VAR
rTrig(CLK := rawSignal); // rTrig.Q is TRUE for one scan on rising edge
// Manual edge pattern:
rising := rawSignal AND NOT prevSignal;
prevSignal := rawSignal;""",
    },
    "inout_struct_array": {
        "id": "inout_struct_array",
        "title": "VAR_IN_OUT Structures and Arrays In-Place Access",
        "body": """// VAR_IN_OUT structures and arrays modify caller storage directly
VAR_IN_OUT
    recipe : ST_Recipe;
    records : ARRAY[1..10] OF INT;
END_VAR
recipe.status := 1;
records[1] := records[1] + 1;
// Note: VAR_IN_OUT parameters cannot specify default initializers""",
    },
    "string_parsing": {
        "id": "string_parsing",
        "title": "IEC 61131-3 String Manipulation and Parsing",
        "body": """// IEC string operations: FIND, MID, LEFT, RIGHT, LEN, STRING(n)
VAR
    s : STRING(80);
    pos, length : INT;
    sub : STRING(20);
END_VAR
length := LEN(s);
pos := FIND(s, '.'); // 1-based index; returns 0 if not found
IF pos > 1 THEN
    sub := LEFT(s, pos - 1); // extracts prefix
END_IF;""",
    },
    "case_state_machine": {
        "id": "case_state_machine",
        "title": "Explicit CASE State Machine Transitions",
        "body": """// Enum / INT based CASE state OF ... explicit transitions
VAR
    state : INT := 0; // 0=IDLE, 1=RUN, 2=FAULT
END_VAR
CASE state OF
    0: IF startCmd THEN state := 1; END_IF;
    1: IF faultCmd THEN state := 2; ELSIF stopCmd THEN state := 0; END_IF;
    2: IF resetCmd THEN state := 0; END_IF;
    ELSE state := 0;
END_CASE;""",
    },
}

STATIC_ANALYSIS_LIGHT_CARD: dict[str, str] = {
    "id": "static_analysis_light",
    "title": "CODESYS Static Analysis Light (SA0027 / SA0033)",
    "body": """// Avoid SA0027 identifier collision with IEC keywords/reserved library symbols & SA0033 unused variables:
// 1. If the required task interface declares variables named `error`, `status`, `state`, `mode`, `result`, or `info`,
//    add the CODESYS attribute right before the variable declaration if SA0027 warns:
VAR_OUTPUT
    {attribute 'analysis' := '-27'}
    error : BOOL := FALSE;
END_VAR
// 2. Declare only variables that are actively read and written (avoid SA0033 unused variable warnings).""",
}

_ORDERED_CARD_IDS = list(DIALECT_CARDS.keys())


def _score_card(card_id: str, task_view: dict[str, Any]) -> int:
    types = [str(v.get("type", "")).upper() for v in task_view.get("interface", [])]
    inouts = [v for v in task_view.get("interface", []) if v.get("direction") == "IN_OUT"]
    text = (
        str(task_view.get("title", ""))
        + " "
        + str(task_view.get("requirements", ""))
        + " "
        + str(task_view.get("scenario", ""))
        + " "
        + str(task_view.get("scan_semantics", ""))
    ).lower()

    score = 0
    if card_id == "variant_ref":
        if any("VARIANT" in t for t in types):
            score += 100
        if "variant" in text or "__varinfo" in text:
            score += 20

    elif card_id == "var_length_array":
        if any("ARRAY[*]" in t for t in types):
            score += 100
        if "array[*]" in text or "variable-length" in text or "variable length" in text:
            score += 20

    elif card_id == "ltime_ops":
        if any("LTIME" in t for t in types):
            score += 80
        if "ltime" in text or "nanosecond" in text or "microsecond" in text:
            score += 20
        if any("TIME" in t for t in types):
            score += 20

    elif card_id == "ton_timer":
        if any("TIME" in t or "LTIME" in t for t in types):
            score += 50
        timer_keywords = ["timer", "ton", "debounce", "delay", "timeout", "preset time", "elapsed time"]
        if any(k in text for k in timer_keywords):
            score += 40

    elif card_id == "edge_detection":
        edge_keywords = [
            "rising edge",
            "falling edge",
            "r_trig",
            "f_trig",
            "edge",
            "pulse",
            "single scan",
            "one scan",
            "single cycle",
        ]
        if any(k in text for k in edge_keywords):
            score += 50

    elif card_id == "inout_struct_array":
        if inouts:
            score += 60
            if any(
                "ARRAY" in str(v.get("type", "")).upper() or "ST_" in str(v.get("type", "")).upper() for v in inouts
            ):
                score += 40
        if any("ST_" in t for t in types):
            score += 30
        if "in_out" in text or "var_in_out" in text:
            score += 20

    elif card_id == "string_parsing":
        if any("STRING" in t for t in types):
            score += 100
        str_keywords = ["string", "find(", "mid(", "left(", "right(", "len(", "parse", "parsing"]
        if any(k in text for k in str_keywords):
            score += 30

    elif card_id == "case_state_machine":
        fsm_keywords = ["state machine", "states", "mode", "sequence", "phase", "step 1", "fsm", "stages", "case "]
        if any(k in text for k in fsm_keywords):
            score += 40
        if "enum" in text:
            score += 30

    return score


def select_static_analysis_hint(task_view: dict[str, Any]) -> dict[str, str] | None:
    """Return the SA0027/SA0033 light static analysis hint card when relevant to the task interface."""
    text = (
        str(task_view.get("title", ""))
        + " "
        + str(task_view.get("requirements", ""))
        + " "
        + str(task_view.get("scenario", ""))
    ).lower()
    reserved_names = {"error", "status", "state", "mode", "result", "info"}
    iface_names = {str(v.get("name", "")).lower() for v in task_view.get("interface", []) if isinstance(v, dict)}
    if (iface_names & reserved_names) or any(tok in text for tok in ("sa0027", "sa0033", "analysis")):
        return copy.deepcopy(STATIC_ANALYSIS_LIGHT_CARD)
    return None


def select_dialect_cards(task_view: dict[str, Any], max_cards: int = 4) -> list[dict[str, str]]:
    """Deterministically select up to `max_cards` relevant CODESYS dialect cards for a task view."""
    if max_cards <= 0:
        return []

    scored: list[tuple[int, int, str]] = []
    for idx, card_id in enumerate(_ORDERED_CARD_IDS):
        score = _score_card(card_id, task_view)
        if score > 0:
            scored.append((-score, idx, card_id))

    scored.sort()
    selected_ids = [card_id for _, _, card_id in scored[:max_cards]]
    return [copy.deepcopy(DIALECT_CARDS[cid]) for cid in selected_ids]
