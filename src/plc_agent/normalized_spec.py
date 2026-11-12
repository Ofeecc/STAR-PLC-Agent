"""Versioned scan-predicate definitions. Does not interpret ST or prove LTL.

Reference transitions consume copies of sampled inputs, never candidate outputs.
The observer and normative reference have separate state and namespaces.
"""
from copy import deepcopy
import hashlib
import math
from pathlib import Path
import re

from .common import ROOT
from .scan_contract import ScanContract
from .timed_contracts import duration_ns

CONTRACT_FILES = ('scan_contract.py', 'array_contracts.py', 'data_contracts.py',
                  'timed_contracts.py', 'process_contracts.py', 'reference.py')


def canonical_source_bytes(path):
    """Hash UTF-8 source with LF endings so Git checkout policy is immaterial."""
    return Path(path).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n').encode('utf-8')


def instantiate_finite_conjunction(task, name, binding_length):
    """Expand ordinal quantification without assuming count == storage length."""
    if type(binding_length) is not int or binding_length < 0:
        raise ValueError('Binding length must be a nonnegative integer')
    spec = task['normalized_specification']['finite_conjunctions'][name]
    if not binding_length:
        return 'TRUE'
    return '('+' & '.join('('+re.sub(r'\bj\b', str(j), spec['body'])+')'
                         for j in range(binding_length))+')'


def reference_step(task, reference, inputs, dt_ms=None):
    sampled = deepcopy(inputs)
    if task['id'] == 'PUB017' and isinstance(sampled.get('recipe'), dict):
        binding = sampled['recipe']
        if '$binding' not in binding:
            raise ValueError('Recipe storage must be an array or declared binding')
        sampled['recipe'] = deepcopy(task['test_bindings']['recipe']['initial'])
    expected = reference.step(sampled, dt_ms)
    if task['id'] == 'PUB017':
        expected['recipe'] = deepcopy(reference.data_contract.recipes)
    return expected


def exact_shape_equal(actual, expected, *, abs_tol=0.0, rel_tol=0.0):
    """Integer and Boolean relations are exact; tolerance is only for floats."""
    if isinstance(expected, bool):
        return type(actual) is bool and actual == expected
    if isinstance(expected, int):
        return type(actual) is int and actual == expected
    if isinstance(expected, float):
        return (type(actual) in (int, float) and math.isfinite(actual)
                and math.isclose(actual, expected, abs_tol=abs_tol, rel_tol=rel_tol))
    if isinstance(expected, dict):
        return (isinstance(actual, dict) and actual.keys() == expected.keys()
                and all(exact_shape_equal(actual[k], v, abs_tol=abs_tol, rel_tol=rel_tol)
                        for k, v in expected.items()))
    if isinstance(expected, list):
        return (isinstance(actual, list) and len(actual) == len(expected)
                and all(exact_shape_equal(a, e, abs_tol=abs_tol, rel_tol=rel_tol)
                        for a, e in zip(actual, expected)))
    return type(actual) is type(expected) and actual == expected


def _valid_deleted_recipe_slot(slot):
    required = {'recipeID', 'ingredientType', 'ingredientRatio', 'productionTemperature'}
    if not isinstance(slot, dict) or set(slot.keys()) != required:
        return False
    if type(slot['recipeID']) is not int or not -32768 <= slot['recipeID'] <= 32767:
        return False
    if type(slot['ingredientType']) is not int or not -32768 <= slot['ingredientType'] <= 32767:
        return False
    for rkey in ('ingredientRatio', 'productionTemperature'):
        val = slot[rkey]
        if isinstance(val, bool) or not isinstance(val, (int, float)) or not math.isfinite(val):
            return False
    return True


def output_matches(task_id, name, actual, expected, inputs):
    if name in ('PUMP_RUNTIME_ACC', 'Slab_Runtime_Accumulator'):
        try:
            return duration_ns(actual) == duration_ns(expected)
        except (TypeError, ValueError):
            return False
    if task_id == 'PUB008' and name == 'channels':
        if not isinstance(actual, list) or len(actual) != len(expected):
            return False
        for j, (got, want) in enumerate(zip(actual, expected)):
            if not isinstance(got, dict) or got.keys() != want.keys():
                return False
            sampled = inputs['channels'][j]
            converted = (j < inputs['count'] and sampled['enable']
                         and sampled['measuringMode'] in (0, 1, 2)
                         and sampled['hiLIM'] > sampled['loLIM'])
            for field, value in want.items():
                if not exact_shape_equal(got[field], value,
                        abs_tol=1e-5 if converted and field == 'outputValue' else 0,
                        rel_tol=2e-6 if converted and field == 'outputValue' else 0):
                    return False
        return True
    if task_id == 'PUB020' and name == 'firingTemp':
        return exact_shape_equal(actual, expected, abs_tol=1e-4)
    return exact_shape_equal(actual, expected, abs_tol=1e-5)


def check_definition_binding(task):
    """Reject implementation drift instead of silently changing the standard."""
    definition = task['normalized_specification']
    for name, expected in definition['transition']['module_sha256'].items():
        path = ROOT / 'src/plc_agent' / name
        if hashlib.sha256(canonical_source_bytes(path)).hexdigest() != expected:
            raise ValueError('Reference definition changed without spec revision: ' + name)


class NormalizedScanMonitor:
    """Evaluates CompleteBehaviorV2 on observations, not all legacy LTL clauses."""
    def __init__(self, task):
        check_definition_binding(task)
        self.task = deepcopy(task)
        self.reference = ScanContract(task['id'])
        self.previous_observed = None
        self.deleted_slots = set()
        self.scan = 0

    def check_initial(self, observed):
        """Call only with a fresh instance BEFORE its first invocation."""
        constraints = self.task['normalized_specification']['initial_observed']
        return {name: name in observed and output_matches(self.task['id'], name,
                    observed[name], value, {}) for name, value in constraints.items()}

    def step(self, inputs, observed, dt_ms=None):
        if not isinstance(observed, dict):
            raise ValueError('Observed candidate outputs must be supplied separately')
        sampled = deepcopy(inputs)
        before_recipe = (deepcopy(self.reference.data_contract.recipes)
                         if self.task['id'] == 'PUB017' else None)
        expected = reference_step(self.task, self.reference, sampled, dt_ms)
        checks = {name: name in observed and output_matches(self.task['id'], name,
                    observed[name], value, sampled) for name, value in expected.items()}
        if before_recipe is not None:
            wanted = deepcopy(expected['recipe'])
            newly_deleted = {j for j,(before,after) in enumerate(zip(before_recipe,wanted))
                             if before['recipeID'] != 0 and after['recipeID'] == 0}
            self.deleted_slots |= newly_deleted
            self.deleted_slots = {j for j in self.deleted_slots if wanted[j]['recipeID'] == 0}
            pre_actual = sampled.get('recipe')
            if not isinstance(pre_actual, list):
                pre_actual = (self.previous_observed or {}).get('recipe')
            if pre_actual is None:
                pre_actual = self.task['test_bindings']['recipe']['initial']
            got = observed.get('recipe')
            if isinstance(got,list) and len(got)==len(wanted):
                for j in self.deleted_slots:
                    # Only the deletion invocation leaves non-ID bytes unconstrained,
                    # provided the slot remains a well-typed ST_Recipe struct.
                    # Later invocations must preserve their sampled actual contents.
                    source = got[j] if j in newly_deleted else pre_actual[j]
                    if _valid_deleted_recipe_slot(source):
                        wanted[j] = {**deepcopy(source),'recipeID':0}
            checks['recipe'] = ('recipe' in observed and output_matches(self.task['id'],
                                'recipe', observed['recipe'], wanted, sampled))
        result = {'scan': self.scan, 'predicate': 'CompleteBehaviorV2',
                  'holds': all(checks.values()), 'field_results': checks,
                  'expected': deepcopy(expected), 'observed': deepcopy(observed),
                  'scope': 'FINITE_OBSERVATION_ONLY_NOT_LTL_PROOF'}
        # Observed history is NEVER written into self.reference.
        self.previous_observed = deepcopy(observed)
        self.scan += 1
        return result
