from __future__ import annotations

from collections import Counter
import re

from .common import ROOT, digest, read_json


def load_tasks(root=ROOT):
    files = sorted((root / "dataset/public").glob("PUB*.json")) + sorted((root / "dataset/self_built").glob("SELF*.json"))
    return [read_json(f) for f in files]

def validate(tasks):
    errors = []
    ids = [t.get("id") for t in tasks]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate task IDs")
    required = {"id", "title", "kind", "difficulty", "provenance", "requirements", "scenario", "interface",
                "initial_conditions", "scan_semantics", "safety_priority", "assumptions", "ltl", "atomic_propositions", "tests"}
    for task in tasks:
        tid = task.get("id", "UNKNOWN")
        errors.extend(f"{tid}: missing {k}" for k in required - task.keys())
        if not task.get("ltl") or not task.get("tests"):
            errors.append(f"{tid}: needs LTL and functional tests")
        if task.get('specification_version','').startswith(('2.1-normalized', '2.2-normalized')):
            from .normalized_spec import check_definition_binding
            normalized=task.get('normalized_specification',{})
            if normalized.get('status')!='NORMALIZED_PENDING_HUMAN_REVIEW':
                errors.append(f'{tid}: missing normalized definition/review boundary')
            if normalized.get('candidate_formal_verification')!='UNVERIFIED':
                errors.append(f'{tid}: normalization must not certify candidate ST')
            for prop in task.get('ltl',[]):
                formula=prop['formula']
                if 'forall' in formula or re.search(r'X\([^()]*\)\s*(?:=|<(?!->)|>|\+)',formula):
                    errors.append(f'{tid}/{prop["id"]}: non-Boolean next or unexpanded quantifier')
            if not normalized.get('transition',{}).get('module_sha256'):
                errors.append(f'{tid}: unpinned transition definition')
            else:
                try:
                    check_definition_binding(task)
                except ValueError as exc:
                    errors.append(f'{tid}: {exc}')
        names = [v["name"].casefold() for v in task.get("interface", [])]
        if len(names) != len(set(names)):
            errors.append(f"{tid}: duplicate case-insensitive IEC identifiers")
        inputs = {v["name"] for v in task.get("interface", []) if v["direction"] in ("INPUT", "IN_OUT")}
        outputs = {v["name"] for v in task.get("interface", []) if v["direction"] in ("OUTPUT", "IN_OUT")}
        for test in task.get("tests", []):
            if not test.get("steps"):
                errors.append(f"{tid}/{test['id']}: empty test")
            for i, step in enumerate(test.get("steps", [])):
                absent = inputs - step.get("inputs", {}).keys()
                extra_inputs = step.get("inputs", {}).keys() - inputs
                extra = step.get("expected", {}).keys() - outputs
                if absent:
                    errors.append(f"{tid}/{test['id']}/{i}: omitted inputs {sorted(absent)}")
                if extra_inputs:
                    errors.append(f"{tid}/{test['id']}/{i}: unknown inputs {sorted(extra_inputs)}")
                if extra:
                    errors.append(f"{tid}/{test['id']}/{i}: unknown outputs {sorted(extra)}")
                if not step.get("expected"):
                    errors.append(f"{tid}/{test['id']}/{i}: no expected outputs")
    return {"task_count": len(tasks), "by_kind": dict(Counter(t["kind"] for t in tasks)),
            "by_difficulty": dict(Counter(t["difficulty"] for t in tasks)),
            "test_cases": sum(len(t.get("tests", [])) for t in tasks),
            "test_steps": sum(len(c["steps"]) for t in tasks for c in t.get("tests", [])),
            "ltl_properties": sum(len(t.get("ltl", [])) for t in tasks),
            "dataset_sha256": digest(tasks), "errors": errors,
            "normalized_tasks":sum('normalized_specification' in t for t in tasks),
            "normalization_is_formal_proof":False}

def public_coverage(tasks, source):
    expected = [x["en"] for group in ("easy", "medium", "hard") for x in source[group]]
    actual = [t["requirements"] for t in tasks if t["kind"] == "public"]
    return {"official_count": len(expected), "included_count": len(actual),
            "verbatim_all_included": sorted(expected) == sorted(actual), "source_sha256": digest(source)}
