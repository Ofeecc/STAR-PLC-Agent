import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from plc_agent.backend import FakeBackend, SimResult
from plc_agent.common import write_json
from plc_agent.compiler import CompileResult
from plc_agent.config import Settings
from plc_agent.formal_verify import import_verification_evidence
from plc_agent.harness import run_harness
from test_star_harness import SAMPLE_TASK, MockLLMClient


class LocalFixTests(unittest.TestCase):
    def test_repair_feedback_retains_static_analysis_diagnostic_code(self):
        from plc_agent.compiler import actionable_diagnostics
        result = CompileResult('COMPILE_FAIL', diagnostics=[
            {'severity':'Error','code':'SA0033','text':"Unused Variable 'Probe'"},
            {'severity':'Error','code':'SA0033','text':"Unused Variable 'Probe'"},
            {'severity':'Text','code':'SA0000','text':'Additional code checks ...'},
        ])
        self.assertEqual(actionable_diagnostics(result), "SA0033: Unused Variable 'Probe'")

    def test_cli_requires_explicit_api_authorization_before_loading_settings(self):
        from plc_agent.cli import main
        with patch('sys.argv', ['plc-agent', 'run']), patch('plc_agent.cli.Settings.load') as load:
            with self.assertRaises(SystemExit) as exc:
                main()
            self.assertEqual(exc.exception.code, 2)
            load.assert_not_called()

    def test_cli_uses_local_config_by_default(self):
        from plc_agent.cli import main
        with patch('sys.argv', ['plc-agent', 'doctor']), patch('plc_agent.cli.Settings.load', return_value=Settings()) as load, patch('plc_agent.cli.doctor', return_value={}):
            self.assertEqual(main(), 0)
            load.assert_called_once_with(None, load_api=False)

    def test_web_does_not_replace_missing_codesys_with_fake_success(self):
        from plc_agent.webui import handle_api_request
        status, result = handle_api_request('POST', '/api/evaluate', {},
            {'task_id':'SELF001', 'candidate':'invalid ST'}, Settings())
        self.assertEqual(status, 503)
        self.assertEqual(result['status'], 'UNVERIFIED')

    def test_waveform_does_not_invent_unobserved_outputs(self):
        from plc_agent.webui import _build_step_waveforms
        cases = [{'id':'x', 'steps':[{'inputs':{},'expected':{'Run':True}}]}]
        with tempfile.TemporaryDirectory() as tmp:
            wave = _build_step_waveforms({}, cases, SimResult('TOOL_ERROR',0,0,[]),Path(tmp))
        self.assertIsNone(wave[0]['steps'][0]['observed'])
        self.assertIsNone(wave[0]['steps'][0]['match'])
        self.assertIsNone(wave[0]['passed'])

    def test_formal_evidence_requires_matching_hashes_and_every_property(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_json(root/'verification_manifest.json', {
                'encoding_complete':True, 'properties':[{'id':'P1'},{'id':'P2'}],
                'source_sha256':'source-a','task_sha256':'task-a','tools_supported':['checker-a']})
            proof = {'status':'PASS','source_sha256':'source-a','task_sha256':'task-a',
                'tool':'checker-a', 'property_results':{'P1':True,'P2':True}}
            evidence = root/'evidence.json'
            write_json(evidence, proof)
            self.assertTrue(import_verification_evidence(root,evidence)['verified'])
            for changed in ({'source_sha256':'wrong'}, {'task_sha256':'wrong'},
                    {'property_results':{'P1':True}}, {'property_results':{'P1':True,'P2':False}},
                    {'tool':'other'}, {'details':'Trace Type: Counterexample'}):
                write_json(evidence, dict(proof, **changed))
                self.assertFalse(import_verification_evidence(root,evidence)['verified'])

    def test_unknown_and_solver_tokens_never_prove_properties(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for token in ('UNVERIFIED', 'NOT VERIFIED', 'SAT', 'UNSAT', '-- specification P is false'):
                evidence = root / 'log.txt'
                evidence.write_text(token, encoding='utf-8')
                self.assertFalse(import_verification_evidence(root, evidence)['verified'])

    def test_infrastructure_errors_stop_without_model_repair(self):
        code = {'declaration': 'FUNCTION_BLOCK FB_Task', 'implementation': 'old', 'supporting_objects': []}
        client = MockLLMClient(['{}', json.dumps(code)])
        bad = CompileResult('TOOL_ERROR', success=False, infrastructure_error='missing tool')
        with tempfile.TemporaryDirectory() as tmp:
            result = run_harness(SAMPLE_TASK, 'mock', Path(tmp)/'run', client, Settings(),
                backend=FakeBackend(compile_fn=lambda *a: bad))
            self.assertEqual(result['status'], 'TOOL_ERROR')
            self.assertEqual(client.call_count, 2)
            self.assertEqual(result['repair_attempts'], 0)

    def test_changed_test_set_returns_the_actual_passing_candidate(self):
        old = {'declaration': 'FUNCTION_BLOCK FB_Task', 'implementation': 'old', 'supporting_objects': []}
        new = dict(old, implementation='repaired', reject_cases=[{'id':'0'}, {'id':'1'}])
        cases = [{'id':str(i), 'steps':[{'inputs':{'start':False}, 'expected':{'m1':False}}]} for i in range(4)]
        class Backend(FakeBackend):
            def __init__(self):
                super().__init__()
                self.calls = 0
            def simulate(self, task, candidate, cases, workspace):
                self.calls += 1
                return SimResult('TEST_FAIL' if self.calls == 1 else 'PASS', 2, len(cases), [])
        client = MockLLMClient(['{}', json.dumps(old), json.dumps(cases), json.dumps(new)])
        with tempfile.TemporaryDirectory() as tmp:
            result = run_harness(SAMPLE_TASK, 'mock', Path(tmp)/'run', client,
                Settings(max_simulations=2), backend=Backend())
            self.assertEqual(result['status'], 'PASS')
            self.assertEqual(result['final_candidate']['implementation'], 'repaired')
            self.assertIn('cases_sha256', result['selftest_evaluation'])

    def test_simulation_tool_error_is_not_behavioral_failure(self):
        code = {'declaration':'FUNCTION_BLOCK FB_Task', 'implementation':'old', 'supporting_objects':[]}
        cases = [{'id':'x','steps':[{'inputs':{'start':False},'expected':{'m1':False}}]}]
        class Backend(FakeBackend):
            def simulate(self, *a):
                return SimResult('TOOL_ERROR',0,0,[],infrastructure_error='sim unavailable')
        client = MockLLMClient(['{}',json.dumps(code),json.dumps(cases)])
        with tempfile.TemporaryDirectory() as tmp:
            result=run_harness(SAMPLE_TASK,'mock',Path(tmp)/'run',client,Settings(),backend=Backend())
            self.assertEqual(result['status'],'TOOL_ERROR')
            self.assertEqual(client.call_count,3)

    def test_incomplete_simulation_is_unverified_and_not_fixed_test_coverage(self):
        code = {'declaration':'FUNCTION_BLOCK FB_Task', 'implementation':'old', 'supporting_objects':[]}
        cases = [{'id':'x','steps':[{'inputs':{'start':False},'expected':{'m1':False}}]}]
        class Backend(FakeBackend):
            def simulate(self, *args):
                return SimResult('PASS',0,0,[])
        client = MockLLMClient(['{}',json.dumps(code),json.dumps(cases)])
        with tempfile.TemporaryDirectory() as tmp:
            result = run_harness(SAMPLE_TASK,'mock',Path(tmp)/'run',client,Settings(),backend=Backend())
        self.assertEqual(result['status'],'UNVERIFIED')
        self.assertEqual(result['selftest_evaluation']['evaluated_cases'],0)
        self.assertEqual(result['functional']['status'],'NOT_RUN')
        self.assertEqual(result['functional']['evaluated_cases'],0)
