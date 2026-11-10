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
    return view
