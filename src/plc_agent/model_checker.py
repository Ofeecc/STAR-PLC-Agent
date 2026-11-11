"""Local NuSMV runner for explicitly encoded SMV models (not an ST translator)."""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path

from .common import ROOT, now, write_json


def find_nusmv(executable: str | None = None) -> Path:
    configured = executable or os.environ.get('NUSMV_EXE')
    if configured:
        path = Path(configured).resolve()
        if not path.is_file():
            raise ValueError('NuSMV executable does not exist')
        return path
    paths = sorted((ROOT / '.local/model_checkers').glob('**/NuSMV.exe'))
    if not paths:
        raise ValueError('Install official NuSMV locally or set NUSMV_EXE')
    return paths[-1].resolve()


def parse_results(stdout: str, stderr: str, returncode: int, expected_count: int) -> dict:
    checks = [{'expression': m.group(1), 'holds': m.group(2).lower() == 'true'}
              for m in re.finditer(r'^--\s+(?:specification|invariant)\s+(.+?)\s+is\s+(true|false)\s*$', stdout, re.M | re.I)]
    failed = bool(returncode != 0 or expected_count < 1 or len(checks) != expected_count
                  or re.search(r'(syntax error|aborting|cannot read|undefined|^.*error:)', stdout + '\n' + stderr, re.M | re.I))
    status = 'TOOL_ERROR' if failed else ('COUNTEREXAMPLE' if any(not c['holds'] for c in checks) else 'MODEL_PROPERTIES_TRUE')
    return {'status': status, 'property_results': checks, 'expected_properties': expected_count,
            'checked_properties': len(checks), 'returncode': returncode}


def check_model(model: str | Path, out_dir: str | Path, executable: str | None = None,
                timeout: int = 60) -> dict:
    if not 1 <= timeout <= 600:
        raise ValueError('Timeout must be between 1 and 600 seconds')
    source = Path(model).read_bytes()
    text = source.decode('utf-8-sig')
    # Count declarations after removing SMV line comments; NuSMV parses the model itself.
    stripped = re.sub(r'--[^\n]*', '', text)
    count = len(re.findall(r'\b(?:LTLSPEC|INVARSPEC|CTLSPEC|SPEC)\b', stripped))
    exe = find_nusmv(executable)
    output = Path(out_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / 'model.smv').write_text(text, encoding='utf-8')
    timed_out = False
    try:
        proc = subprocess.run([str(exe), 'model.smv'], cwd=output, capture_output=True, timeout=timeout)
        stdout = proc.stdout.decode('utf-8', errors='replace')
        stderr = proc.stderr.decode('utf-8', errors='replace')
        result = parse_results(stdout, stderr, proc.returncode, count)
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or b'').decode('utf-8', errors='replace')
        stderr = (exc.stderr or b'').decode('utf-8', errors='replace')
        result = {'status': 'TIMEOUT', 'property_results': [], 'expected_properties': count}
        timed_out = True
    (output / 'stdout.txt').write_text(stdout, encoding='utf-8')
    (output / 'stderr.txt').write_text(stderr, encoding='utf-8')
    result.update({'tool': 'NuSMV', 'tool_exe_sha256': hashlib.sha256(exe.read_bytes()).hexdigest(),
                   'model_sha256': hashlib.sha256(source).hexdigest(), 'created_utc': now(),
                   'scope': 'EXPLICIT_SMV_MODEL_ONLY', 'candidate_st_verified': False,
                   'timed_out': timed_out, 'stdout_path': 'stdout.txt', 'stderr_path': 'stderr.txt'})
    write_json(output / 'model_check_result.json', result)
    return result
