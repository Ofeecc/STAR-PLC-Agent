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

    def test_find_nusmv_supports_posix_local_and_path(self):
        import os
        import stat
        import tempfile
        from pathlib import Path
        from unittest.mock import patch

        import plc_agent.model_checker as mc

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            exe = root / '.local/model_checkers/NuSMV-2.7.1-linux64/usr/bin/NuSMV'
            exe.parent.mkdir(parents=True)
            exe.write_text('#!/bin/sh\nexit 0\n', encoding='utf-8')
            exe.chmod(exe.stat().st_mode | stat.S_IXUSR)
            with patch.object(mc, 'ROOT', root), patch.dict(os.environ, {}, clear=False):
                os.environ.pop('NUSMV_EXE', None)
                self.assertEqual(mc.find_nusmv(), exe.resolve())

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sys_exe = root / 'bin/NuSMV'
            sys_exe.parent.mkdir(parents=True)
            sys_exe.write_text('#!/bin/sh\nexit 0\n', encoding='utf-8')
            sys_exe.chmod(sys_exe.stat().st_mode | stat.S_IXUSR)
            with patch.object(mc, 'ROOT', root), patch('shutil.which', return_value=str(sys_exe)), patch.dict(os.environ, {}, clear=False):
                os.environ.pop('NUSMV_EXE', None)
                self.assertEqual(mc.find_nusmv(), sys_exe.resolve())

    def test_check_model_runs_real_nusmv_when_installed(self):
        import tempfile
        from pathlib import Path

        import plc_agent.model_checker as mc

        try:
            exe = mc.find_nusmv()
        except ValueError:
            self.skipTest('Local NuSMV executable not installed')
        with tempfile.TemporaryDirectory() as tmp:
            out_ref = Path(tmp) / 'ref'
            res_ref = check_model(mc.ROOT / 'models/PUB001_reference.smv', out_ref, str(exe))
            self.assertEqual(res_ref['status'], 'MODEL_PROPERTIES_TRUE')
            self.assertEqual(res_ref['checked_properties'], 9)
            self.assertEqual(res_ref['expected_properties'], 9)
            out_neg = Path(tmp) / 'neg'
            res_neg = check_model(mc.ROOT / 'models/negative_control.smv', out_neg, str(exe))
            self.assertEqual(res_neg['status'], 'COUNTEREXAMPLE')
            self.assertEqual(res_neg['checked_properties'], 2)
            self.assertEqual([r['holds'] for r in res_neg['property_results']], [False, True])

    def test_pub001_reference_uses_current_transition_properties(self):
        model = (ROOT / 'models/PUB001_reference.smv').read_text()
        task = json.loads((ROOT / 'dataset/public/PUB001.json').read_text(encoding='utf-8'))
        for prop in task['ltl']:
            if prop['id'] in {f'PUB001.P{i}' for i in range(2, 10)}:
                self.assertIn(prop['formula'], model)


if __name__ == '__main__':
    unittest.main()
