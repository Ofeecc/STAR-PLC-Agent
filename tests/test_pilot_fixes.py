import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from plc_agent.backend import FakeBackend
from plc_agent.compiler import verify_interface_signature
from plc_agent.config import Settings
from plc_agent.dataset import load_tasks
from plc_agent.formal_verify import verify_candidate
from plc_agent.functional import same_declared_inputs
from plc_agent.harness import run_harness
from plc_agent.llm import ProviderError
from plc_agent.simulation import build_program
from plc_agent.st_verifier import compile_st_to_smv, parse_st_function_block


class PilotFixTests(unittest.TestCase):
    def test_named_integer_constants_in_case_and_array_bounds(self):
        candidate = {'declaration': 'FUNCTION_BLOCK FB_Task\nVAR CONSTANT MAX_N: INT := 3; PHASE_IDLE: INT := 0; END_VAR\nVAR phase: INT; buffer: ARRAY[0..MAX_N] OF INT; END_VAR',
                     'implementation': 'CASE phase OF PHASE_IDLE: phase := MAX_N; END_CASE;'}
        program = parse_st_function_block(candidate)
        self.assertEqual(program.statements[0].arms[0][0][0], (0, None))
        self.assertEqual(program.decls[-1].st_type.arr_high, 3)
    def test_qualified_enum_literals_in_initialization_and_case(self):
        candidate = {'declaration': 'FUNCTION_BLOCK FB_Task\nVAR_OUTPUT q: BOOL; END_VAR\nVAR phase: E_Phase := E_Phase.IDLE; END_VAR',
                     'implementation': 'CASE phase OF E_Phase.IDLE: phase := E_Phase.RUN; E_Phase.RUN: q := TRUE; END_CASE;',
                     'supporting_objects': [{'name': 'E_Phase', 'kind': 'DUT', 'declaration': 'TYPE E_Phase : (IDLE := 3, RUN := 7); END_TYPE'}]}
        program = parse_st_function_block(candidate)
        self.assertEqual(program.decls[-1].init_expr.value, 3)
        self.assertEqual(program.statements[0].arms[0][0][0], (3, None))
        self.assertEqual(program.statements[0].arms[1][0][0], (7, None))
    def test_word_output_is_bridged_at_numeric_observer_boundary(self):
        task = next(t for t in load_tasks() if t['id'] == 'PUB003')
        candidate = {'declaration': 'FUNCTION_BLOCK FB_Task\nVAR_INPUT Value, hiLevel, loLevel, hystWindow: REAL; END_VAR\nVAR_OUTPUT hiAlarm, loAlarm, error: BOOL; status: WORD; END_VAR',
                     'implementation': 'hiAlarm := FALSE; loAlarm := FALSE; error := TRUE; status := WORD#32769;'}
        compiled = compile_st_to_smv(candidate, task)
        self.assertIn('status := toint(', compiled['smv_text'])
        task = next(t for t in load_tasks() if t['id'] == 'PUB002')
        candidate = {'declaration': 'FUNCTION_BLOCK FB_Task\nVAR_INPUT value: DWORD; END_VAR\nVAR_OUTPUT hasChanged, hasRisingEdges, hasFallingEdges: BOOL; risingBits, fallingBits: DWORD; noOfRisingBits, noOfFallingBits: USINT; END_VAR\nVAR prev: DWORD; END_VAR',
                     'implementation': 'risingBits := value AND NOT prev; fallingBits := prev AND NOT value; hasChanged := value <> prev; prev := value;'}
        compiled = compile_st_to_smv(candidate, task)
        self.assertNotIn('risingBits := toint(', compiled['smv_text'])
    def test_real_input_monitor_roundtrip_preserves_binary32_identity(self):
        task = {'interface': [{'name': 'x', 'type': 'REAL'}]}
        self.assertTrue(same_declared_inputs(task, {'x': 0.9}, {'x': 0.8999999761581421}))
        self.assertFalse(same_declared_inputs(task, {'x': 0.9000000357627869}, {'x': 0.8999999761581421}))
        self.assertFalse(same_declared_inputs(task, {'x': True}, {'x': 1}))
    def test_pragmas_do_not_hide_ports_or_change_source(self):
        candidate = {'declaration': "FUNCTION_BLOCK FB_Task\nVAR_OUTPUT\n{attribute 'analysis' := '-27'}\nerror: BOOL;\nstatus: WORD;\nEND_VAR", 'implementation': ''}
        original = candidate['declaration']
        ports = [{'name': 'error', 'type': 'BOOL', 'direction': 'OUTPUT'},
                 {'name': 'status', 'type': 'WORD', 'direction': 'OUTPUT'}]
        self.assertEqual(verify_interface_signature(candidate, ports), [])
        self.assertEqual(candidate['declaration'], original)
        self.assertTrue(verify_interface_signature(candidate, [dict(ports[0], type='INT')]))

    def test_missing_checker_returns_tool_error(self):
        task = next(t for t in load_tasks() if t['id'] == 'PUB001')
        with tempfile.TemporaryDirectory() as tmp, patch('plc_agent.st_verifier.verify_candidate_st', side_effect=ValueError('checker missing')):
            result = verify_candidate(task, {'declaration': 'FUNCTION_BLOCK FB_Task\nVAR END_VAR', 'implementation': ''}, tmp)
            self.assertEqual(result['status'], 'TOOL_ERROR')
            self.assertFalse(result['verified'])
            self.assertTrue((Path(tmp)/'verification_result.json').exists())

    def test_timing_waits_even_for_first_step(self):
        task = next(t for t in load_tasks() if t['id'] == 'PUB004')
        program = build_program(task)
        self.assertIn('BenchClockReady', program['implementation'])
        self.assertNotIn('BenchStep = 0 OR', program['implementation'])
        self.assertNotIn('TraceDt[0] := 0;', program['implementation'])

    def test_failed_provider_usage_is_preserved(self):
        class FailedClient:
            request_count = 1
            total_tokens = 20
            def respond(self, model, messages, log_dir, **kw):
                Path(log_dir).mkdir(parents=True)
                (Path(log_dir)/'response.json').write_text(json.dumps({'usage': {'total_tokens': 20}}))
                raise ProviderError('transport failure')
        task = next(t for t in load_tasks() if t['id'] == 'PUB001')
        with tempfile.TemporaryDirectory() as tmp:
            result = run_harness(task, 'fake', Path(tmp)/'run', FailedClient(), Settings(), backend=FakeBackend())
            self.assertEqual(result['llm_calls'], 1)
            self.assertEqual(result['usage'][0]['total_tokens'], 20)

    def test_truncated_optional_plan_proceeds_without_retry(self):
        class TruncatedPlanClient:
            calls = 0
            def respond(self, model, messages, log_dir, **kw):
                self.calls += 1
                if self.calls == 1:
                    raise ProviderError('Responses incomplete: {"reason": "length"}')
                return {'text': json.dumps({'declaration': 'FUNCTION_BLOCK FB_Task\nVAR END_VAR',
                                           'implementation': '', 'supporting_objects': []})}
        task = {'id': 'UNIT_TRUNCATED_PLAN', 'interface': [], 'tests': [], 'requirements': 'unit'}
        client = TruncatedPlanClient()
        with tempfile.TemporaryDirectory() as tmp:
            result = run_harness(task, 'fake', Path(tmp)/'run', client,
                                 Settings(max_verifications=0), backend=FakeBackend(), ablation='no_selftest')
            self.assertEqual(client.calls, 2)
            self.assertTrue(result['final_compiled'])
            self.assertIn('length', result['planner_warning'])
