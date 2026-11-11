import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from plc_agent.common import ROOT
from plc_agent.model_checker import check_model, parse_results


class ModelCheckerTests(unittest.TestCase):
    def test_invariants_and_ltl_results_and_completeness(self):
        text = '-- specification G x is true\n-- invariant x is true\n'
        self.assertEqual(parse_results(text, '', 0, 2)['status'], 'MODEL_PROPERTIES_TRUE')
        for expected in (0, 1, 3):
            self.assertEqual(parse_results(text, '', 0, expected)['status'], 'TOOL_ERROR')
        self.assertEqual(parse_results(text, 'syntax error', 0, 2)['status'], 'TOOL_ERROR')
        self.assertEqual(parse_results(text, '', 1, 2)['status'], 'TOOL_ERROR')
        self.assertEqual(parse_results(text.replace('G x is true', 'G x is false'), '', 0, 2)['status'], 'COUNTEREXAMPLE')

    def test_timeout_retains_partial_log_without_claiming_correctness(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp)
            exe = folder / 'NuSMV.exe'
            exe.write_bytes(b'test executable')
            model = folder / 'input.smv'
            model.write_text('MODULE main\nINVARSPEC TRUE;\n')
            with patch('plc_agent.model_checker.subprocess.run', side_effect=subprocess.TimeoutExpired('NuSMV', 1, output=b'partial log')):
                result = check_model(model, folder / 'output', str(exe), timeout=1)
            self.assertEqual(result['status'], 'TIMEOUT')
            self.assertFalse(result['candidate_st_verified'])
            self.assertEqual((folder / 'output/stdout.txt').read_text(), 'partial log')
            self.assertEqual(json.loads((folder / 'output/model_check_result.json').read_text())['status'], 'TIMEOUT')

    def test_pub001_reference_uses_current_transition_properties(self):
        model = (ROOT / 'models/PUB001_reference.smv').read_text()
        task = json.loads((ROOT / 'dataset/public/PUB001.json').read_text(encoding='utf-8'))
        for prop in task['ltl']:
            if prop['id'] in {'P3','P4','P5','P6','P7','P8','P9','P10'}:
                self.assertIn(prop['formula'], model)


if __name__ == '__main__':
    unittest.main()
