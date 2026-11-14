from __future__ import annotations

import copy

ALLOWED_KEYS = {
    "id",
    "title",
    "difficulty",
    "requirements",
    "scenario",
    "interface",
    "data_types",
    "supporting_types",
    "initial_conditions",
    "scan_semantics",
    "safety_priority",
    "assumptions",
}

SPEC_KEYS = {
    "ltl",
    "atomic_propositions",
}

FORBIDDEN_KEYS = {
    "tests",
    "test_bindings",
    "specification_contract",
    "provenance",
}


def agent_view(task: dict, spec_visible: bool = True) -> dict:
    """Return a sanitized, leak-free task view for agent consumption."""
    visible_keys = ALLOWED_KEYS | (SPEC_KEYS if spec_visible else set())
    view = {}
    for key, val in task.items():
        if key in visible_keys:
            view[key] = copy.deepcopy(val)
    if isinstance(view.get("atomic_propositions"), dict):
        view["atomic_propositions"] = {k: v for k, v in view["atomic_propositions"].items() if k != "CompleteBehavior"}
    if isinstance(view.get("ltl"), list):
        view["ltl"] = [
            item
            for item in view["ltl"]
            if not (
                isinstance(item, dict)
                and (
                    str(item.get("id", "")).endswith(".COMPLETE") or "CompleteBehavior" in str(item.get("formula", ""))
                )
            )
        ]
    return view
