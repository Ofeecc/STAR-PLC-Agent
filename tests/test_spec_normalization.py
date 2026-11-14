import json
import re
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from plc_agent.common import ROOT, read_json
from plc_agent.dataset import load_tasks
from plc_agent.normalized_spec import (
    NormalizedScanMonitor,
    canonical_source_bytes,
    exact_shape_equal,
    instantiate_finite_conjunction,
    reference_step,
)
from plc_agent.scan_contract import ScanContract
from plc_agent.task_view import agent_view


class NormalizedSpecTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = {t['id']:t for t in load_tasks()}

    def test_all_32_preserve_source_tests_and_initial_conditions(self):
        for tid,t in self.tasks.items():
            before=read_json(ROOT/'dataset_versions/before_normalization_20261111'/(tid+'.json'))
            self.assertEqual(t['specification_version'],'normalized-20261114',tid)
            self.assertEqual(t['interface'],before['interface'],(tid,'interface'))
            if t['kind']=='public':
                self.assertEqual(t['requirements'],before['requirements'],(tid,'requirements'))
            self.assertGreaterEqual(len(t['ltl']),len(before['ltl']),tid)
            self.assertGreaterEqual(len(t['tests']),len(before['tests']),tid)
            outs=[f['name'] for f in t['interface'] if f['direction']=='OUTPUT']
            if outs:
                self.assertTrue(any(p.get('scope')=='INITIAL_INSTANCE' and p['formula']=='init' for p in t['ltl']),tid)
                for o in outs:
                    self.assertIn(o,t['initial_conditions'],(tid,o))
            for case in t['tests']:
                for sidx,step in enumerate(case['steps']):
                    for o in outs:
                        self.assertIn(o,step['expected'],(tid,case['id'],sidx,o))
            self.assertEqual(t['normalized_specification']['candidate_formal_verification'],'UNVERIFIED')

    def test_complete_predicates_are_pinned_and_not_future_work_instructions(self):
        for tid,t in self.tasks.items():
            definition=t['atomic_propositions']['CompleteBehavior']
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
        f=next(p['formula'] for p in self.tasks['PUB002']['ltl'] if p['id']=='PUB002.P6')
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
        for tid,pid in [('PUB004','PUB004.P7'),('PUB005','PUB005.P5'),('PUB006','PUB006.P5'),('PUB010','PUB010.P8'),('PUB013','PUB013.P6')]:
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


class Round1FixesTests(unittest.TestCase):
    def test_pub010_scan0_clock_zero_and_demand_freezes_on_fault(self):
        c=ScanContract('PUB010')
        out0=c.step({'TemperatureSensorInput':50.0,'SetTemperature':80.0},dt_ms=9999)
        self.assertTrue(out0['HeaterOutput'])
        self.assertEqual(float(c.clock),0.0)
        # Step 1 <5s still heats, demand is True; step 2 fault=120 freezes demand=True!
        c.step({'TemperatureSensorInput':120.0,'SetTemperature':40.0},dt_ms=100)
        self.assertTrue(c.demand)

    def test_pub017_zero_rejected_negative_accepted_concurrent_edges_rejected_and_bad_deleted_slot_rejected(self):
        c=ScanContract('PUB017')
        rec_neg={'recipeID':-7,'ingredientType':1,'ingredientRatio':0.5,'productionTemperature':60.0}
        rec_zero={'recipeID':0,'ingredientType':0,'ingredientRatio':0.0,'productionTemperature':0.0}
        base=dict(addRecipe=False,deleteRecipe=False,modifyRecipe=False,queryRecipe=False,
                  recipeIn=rec_zero,recipe=[deepcopy(rec_zero) for _ in range(10)])
        with self.assertRaisesRegex(ValueError,'zero'):
            c.step({**base,'addRecipe':True})
        c=ScanContract('PUB017')
        with self.assertRaisesRegex(ValueError,'multiple'):
            c.step({**base,'addRecipe':True,'queryRecipe':True,'recipeIn':rec_neg})
        t=next(x for x in load_tasks() if x['id']=='PUB017')
        m=NormalizedScanMonitor(t)
        oracle=ScanContract('PUB017')
        out=reference_step(t,oracle,{**base,'addRecipe':True,'recipeIn':rec_neg})
        self.assertTrue(out['recipeAdded'])
        self.assertEqual(out['recipe'][0]['recipeID'],-7)
        self.assertTrue(m.step({**base,'addRecipe':True,'recipeIn':rec_neg},out)['holds'])
        # Deleted slot struct validation rejects bad keys/NaN
        step_del=reference_step(t,oracle,{**base,'deleteRecipe':True,'recipeIn':rec_neg})
        bad_obs=deepcopy(step_del)
        bad_obs['recipe'][0]={'recipeID':0,'unexpected':1}
        self.assertFalse(m.step({**base,'deleteRecipe':True,'recipeIn':rec_neg},bad_obs)['field_results']['recipe'])

    def test_pub018_concurrent_enq_deq_and_nonpositive_capacity_rejected(self):
        c=ScanContract('PUB018')
        buf={'$binding':'buffer','binding_id':'A','capacity':2,'buffer_initial':[0,0],'item_type':'DINT'}
        with self.assertRaisesRegex(ValueError,'enqueue and dequeue'):
            c.step({'enqueue':True,'dequeue':True,'reset':False,'item':1,'buffer':buf})
        with self.assertRaisesRegex(ValueError,'capacity'):
            ScanContract('PUB018').step({'enqueue':True,'dequeue':False,'reset':False,'item':1,
                                        'buffer':[]})

    def test_pub019_simultaneous_modes_rejected(self):
        c=ScanContract('PUB019')
        i={f['name']:False for f in next(x for x in load_tasks() if x['id']=='PUB019')['interface'] if f['direction']=='INPUT'}
        i['EmergencyStop']=True
        i['ManualMode']=True
        i['SingleStepMode']=True
        with self.assertRaisesRegex(ValueError,'simultaneous'):
            c.step(i)

    def test_functional_respects_zero_dt_tolerance_and_metrics_verification_passes(self):
        from plc_agent.common import digest
        from plc_agent.functional import evaluate_trace
        from plc_agent.harness import empty_result
        from plc_agent.metrics import aggregate
        task=deepcopy(next(x for x in load_tasks() if x['id']=='PUB010'))
        case=task['tests'][0]
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'log.txt').write_text('ok\n',encoding='utf-8')
            trace={'task_id':'PUB010','task_sha256':digest(task),'source_sha256':'s','backend':'CODESYS_SIMULATION',
                   'operator':'UNIT_DOUBLE','observed_utc':'2026-11-12T00:00:00Z','evidence_files':['log.txt'],
                   'cases':{c['id']:[{'inputs':s['inputs'],'outputs':s['expected'],'dt_ms':s['dt_ms']} for s in c['steps']]
                            for c in task['tests']}}
            trace['cases'][case['id']][1]['dt_ms']=5000  # differs by 1ms from 4999 where dt_tolerance_ms==0
            with self.assertRaisesRegex(ValueError,'fixed test timing'):
                evaluate_trace(task,'s',trace,evidence_root=root)
        row=empty_result(task,'E1','UNIT','codex_cli')
        row['verification']={'verified':True,'status':'SAT'}
        self.assertEqual(aggregate([row],1)[0]['verification_passed_tasks'],0)
        row['verification']={'verified':True,'status':'VERIFIED'}
        self.assertEqual(aggregate([row],1)[0]['verification_passed_tasks'],1)


if __name__=='__main__':unittest.main()
