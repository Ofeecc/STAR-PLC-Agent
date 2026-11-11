from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATUSES = {"PASS", "COMPILE_FAIL", "TEST_FAIL", "TIMEOUT", "TOOL_ERROR", "NOT_RUN", "UNVERIFIED"}

def now():
    return datetime.now(timezone.utc).isoformat()

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))

def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temp, path)

def digest(value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def redact(text, secrets=()):
    result = str(text)
    for secret in secrets:
        if secret:
            result = result.replace(secret, "[REDACTED]")
    return re.sub(r"(?i)(?:sk-|bearer\s+)[A-Za-z0-9_.-]+", "[REDACTED]", result)

def safe_child(root, name):
    root = Path(root).resolve()
    path = (root / name).resolve()
    if not path.is_relative_to(root):
        raise ValueError("Path escapes workspace")
    return path

def artifact_path(value):
    """Resolve historical absolute artifact paths after extracting a submission."""
    path = Path(value)
    if path.is_file():
        return path
    normalized = str(value).replace("\\", "/")
    marker = "/" + ROOT.name + "/"
    if marker in normalized:
        return safe_child(ROOT, normalized.split(marker, 1)[1])
    return safe_child(ROOT, normalized) if not path.is_absolute() else path
