from copy import deepcopy
import json
from pathlib import Path
import re
import tempfile
import unittest

from plc_agent.common import ROOT, read_json
from plc_agent.dataset import load_tasks
from plc_agent.normalized_spec import NormalizedScanMonitor, exact_shape_equal, instantiate_finite_conjunction, reference_step, canonical_source_bytes
from plc_agent.scan_contract import ScanContract
from plc_agent.task_view import agent_view


class NormalizedSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = {t['id']:t for t in load_tasks()}

    def test_all_32_preserve_source_tests_and_initial_conditions(self):
        for tid,t in self.tasks.items():
            before=read_json(ROOT/'dataset_versions/before_normalization_20261111'/(tid+'.json'))
            for field in ('requirements','interface','tests','initial_conditions','assumptions'):
                self.assertEqual(t[field],before[field],(tid,field))
            self.assertEqual(len(t['ltl']),len(before['ltl']))
            self.assertEqual(t['normalized_specification']['candidate_formal_verification'],'UNVERIFIED')

    def test_complete_predicates_are_pinned_and_not_future_work_instructions(self):
        for tid,t in self.tasks.items():
            definition=t['atomic_propositions']['CompleteBehaviorV2']
            self.assertNotRegex(definition,r'明确|给出|补G|须声明|需另外|或给出')
            self.assertIn('Sref[k+1]',definition)
            self.assertIn('实际O[k]',definition)
            self.assertEqual(t['specification_contract']['normative_completion'],definition)
            NormalizedScanMonitor(t)  # checks every pinned implementation hash
            self.assertIn('Spre',t['normalized_specification']['auxiliary_state_bindings'])
        self.assertIn('Spre.phase',self.tasks['PUB001']['atomic_propositions']['phase'])
        self.assertIn('O[k][n]',self.tasks['PUB001']['atomic_propositions']['oneHotOutputs'])
        self.assertIn('qForward',self.tasks['SELF002']['normalized_specification']['history_bindings'])
        self.assertEqual(self.tasks['SELF004']['atomic_propositions']['qFault'],'Spre.reference.state.mode=3')

    def test_no_raw_numeric_next_or_unbounded_forall_in_active_formulas(self):
        for t in self.tasks.values():
            for p in t['ltl']:
                self.assertNotRegex(p['formula'],r'X\([^()]*\)\s*(?:=|<(?!->)|>|\+)')
                self.assertNotIn('forall',p['formula'])
                self.assertEqual(p['encoding_status'],'NOT_LOWERED_TO_MODEL_CHECKER')
        f=next(p['formula'] for p in self.tasks['PUB002']['ltl'] if p['id']=='P6')
        self.assertEqual(len(re.findall(r'X\(PrevBit\d+\)',f)),32)

    def test_array_quantifiers_have_binding_domain_and_correct_empty_identity(self):
        d=self.tasks['PUB008']['normalized_specification']['finite_conjunctions']
        self.assertEqual(len(d),7)
        for entry in d.values():
            self.assertEqual(entry['lower_inclusive'],0)
            self.assertEqual(entry['upper_exclusive'],'len(I[k].channels)')
            self.assertTrue(entry['empty_value'])
            self.assertIn('j<I[k].count',entry['guard'])
        t=self.tasks['PUB008']
        self.assertEqual(instantiate_finite_conjunction(t,'AllChannels_P2',0),'TRUE')
        f=instantiate_finite_conjunction(t,'AllChannels_P2',3)
        self.assertNotRegex(f,r'\bj\b')
        self.assertIn('enabled(2)',f)
        self.assertNotIn('enabled(3)',f)
        with self.assertRaises(ValueError):instantiate_finite_conjunction(t,'AllChannels_P2',True)

    def test_timed_liveness_requires_divergent_physical_time(self):
        for tid,pid in [('PUB004','P7'),('PUB005','P5'),('PUB006','P5'),('PUB010','P8'),('PUB013','PUB013.P6')]:
            t=self.tasks[tid]
            p=next(p for p in t['ltl'] if p['id']==pid)
            self.assertIn('G(F(TimeTick))',p['formula'])
            self.assertIn('floor(t[k]/1ms)',t['atomic_propositions']['TimeTick'])

    def test_wrong_observations_fail_and_do_not_drive_reference(self):
        t=self.tasks['PUB001']; m=NormalizedScanMonitor(t)
        i=deepcopy(t['tests'][0]['steps'][1]['inputs'])  # bottle arrives
        correct=dict(Pump_Motor=True,Filling_Valve=False,Capping_Machine=False,
                     Packing_Machine=False,Completion_Light=False)
        wrong={k:False for k in correct}
        self.assertFalse(m.step(i,wrong)['holds'])
        i['bottleSensor']=False
        # A bad observed pump did not reset independent phase; cleaning remains active.
        self.assertTrue(m.step(i,correct)['holds'])
        self.assertEqual(m.reference.phase,1)

    def test_initial_instance_is_distinct_from_first_scan_output(self):
        t=self.tasks['PUB001']; m=NormalizedScanMonitor(t)
        zero={f['name']:False for f in t['interface'] if f['direction']=='OUTPUT'}
        self.assertTrue(all(m.check_initial(zero).values()))
        bad={**zero,'Pump_Motor':True}
        self.assertFalse(m.check_initial(bad)['Pump_Motor'])
        i=deepcopy(t['tests'][0]['steps'][1]['inputs'])
        self.assertTrue(m.step(i,bad)['holds'])

    def test_integer_and_boolean_predicates_do_not_use_float_tolerance(self):
        self.assertFalse(exact_shape_equal(1.000001,1,abs_tol=1e-5))
        self.assertFalse(exact_shape_equal(1,True,abs_tol=1e-5))
        self.assertTrue(exact_shape_equal(1.000001,1.0,abs_tol=1e-5))

    def test_definition_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source.py'
            source.write_bytes(b'\xef\xbb\xbfx = 1\r\ny = 2\r\n')
            self.assertEqual(canonical_source_bytes(source), b'x = 1\ny = 2\n')
        t=deepcopy(self.tasks['PUB001'])
        t['normalized_specification']['transition']['module_sha256']['scan_contract.py']='0'*64
        with self.assertRaisesRegex(ValueError,'changed without spec revision'):
            NormalizedScanMonitor(t)

    def test_storage_database_output_is_checked_even_if_old_trace_omitted_it(self):
        t=self.tasks['PUB017']; m=NormalizedScanMonitor(t)
        i=deepcopy(t['tests'][0]['steps'][0]['inputs'])
        # Caller initial storage is part of the reference, not candidate observations.
        expected=deepcopy(t['test_bindings']['recipe']['initial'])
        got=dict(recipeAdded=False,recipeDeleted=False,recipeModified=False,
            recipeQueryResult=deepcopy(t['initial_conditions']['recipeQueryResult']),
            error=False,status=0,recipe=expected)
        self.assertTrue(m.step(i,got)['holds'])
        got['recipe'][0]['recipeID']=999
        self.assertFalse(m.step(i,got)['field_results']['recipe'])
        self.assertEqual(m.reference.data_contract.recipes[0]['recipeID'],0)

    def test_normalized_sources_stay_out_of_agent_view(self):
        for t in self.tasks.values():
            view=agent_view(t)
            self.assertNotIn('normalized_specification',view)
            self.assertNotIn('specification_contract',view)
            self.assertNotIn('tests',view)
            self.assertNotIn('def _SELF',json.dumps(view))
            self.assertNotIn('ltl',agent_view(t,spec_visible=False))

    def test_each_task_rejects_a_mutated_observation(self):
        def mutate(value):
            if type(value) is bool:return not value
            if type(value) in (int,float):return value+1
            if isinstance(value,str):return 'INVALID'
            result=deepcopy(value)
            if isinstance(result,list):result[0]=mutate(result[0])
            else:
                first=next(iter(result));result[first]=mutate(result[first])
            return result
        for tid,t in self.tasks.items():
            step=t['tests'][0]['steps'][0]
            expected=reference_step(t,ScanContract(tid),step['inputs'],step.get('dt_ms'))
            actual=deepcopy(expected);first=next(iter(actual));actual[first]=mutate(actual[first])
            m=NormalizedScanMonitor(t)
            self.assertFalse(m.step(step['inputs'],actual,step.get('dt_ms'))['holds'],tid)

    def test_recipe_delete_allows_unconstrained_bytes_then_requires_preservation(self):
        t=self.tasks['PUB017']; m=NormalizedScanMonitor(t); oracle=ScanContract('PUB017')
        i=deepcopy(t['tests'][0]['steps'][0]['inputs'])
        for name in ('addRecipe','deleteRecipe','modifyRecipe','queryRecipe'):i[name]=False
        i['recipeIn']={'recipeID':7,'ingredientType':1,'ingredientRatio':0.5,'productionTemperature':20.0}
        for add in (True,False):
            i['addRecipe']=add
            expected=reference_step(t,oracle,i)
            self.assertTrue(m.step(i,expected)['holds'])
        i['deleteRecipe']=True
        actual=reference_step(t,oracle,i)
        actual['recipe'][0]['ingredientType']=999
        self.assertTrue(m.step(i,actual)['holds'])
        self.assertEqual(m.reference.data_contract.recipes[0]['ingredientType'],1)
        i['deleteRecipe']=False
        idle=reference_step(t,oracle,i);idle['recipe'][0]['ingredientType']=999
        self.assertTrue(m.step(i,idle)['holds'])
        idle['recipe'][0]['ingredientType']=998
        self.assertFalse(m.step(i,idle)['holds'])


if __name__=='__main__':unittest.main()
