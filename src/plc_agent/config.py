from __future__ import annotations

import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from .common import ROOT, read_json


def detect_codesys() -> tuple[str, str]:
    """Scan standard Windows installation paths for CODESYS.exe and matching profiles."""
    if os.name != "nt":
        return "", ""
    candidates = [
        Path(r"C:\Program Files\CODESYS\CODESYS\Common\CODESYS.exe"),
        Path(r"C:\Program Files (x86)\CODESYS\CODESYS\Common\CODESYS.exe"),
        Path(r"D:\CODESYS_V3\CODESYS\Common\CODESYS.exe"),
        Path(r"D:\Codesys\CODESYS\Common\CODESYS.exe"),
        Path(r"C:\Codesys\CODESYS\Common\CODESYS.exe"),
    ]
    for prog_dir in (Path(r"C:\Program Files"), Path(r"C:\Program Files (x86)"), Path(r"D:\Program Files")):
        if prog_dir.is_dir():
            try:
                for d in prog_dir.glob("CODESYS*"):
                    exe = d / "CODESYS" / "Common" / "CODESYS.exe"
                    if exe.is_file() and exe not in candidates:
                        candidates.append(exe)
            except OSError:
                pass

    found_exe = ""
    for c in candidates:
        if c.is_file():
            found_exe = str(c)
            break

    found_profile = ""
    if found_exe:
        common_dir = Path(found_exe).parent
        for prof_dir in (common_dir.parent / "Profiles", common_dir.parent.parent / "Profiles"):
            if prof_dir.is_dir():
                try:
                    profiles = sorted([*prof_dir.glob("*.profile"), *prof_dir.glob("*.profile.xml")], key=lambda p: p.stat().st_mtime, reverse=True)
                    if profiles:
                        found_profile = profiles[0].name.removesuffix(".xml").removesuffix(".profile")
                        break
                except OSError:
                    pass
    return found_exe, found_profile


@dataclass
class Settings:
    base_url: str = ""
    api_key: str = field(default="", repr=False)
    codesys_exe: str = ""
    codesys_profile: str = ""
    codesys_template: str = ""
    additional_folder: str = ""
    ascii_work_root: str = ""
    compiler_timeout: int = 180
    llm_timeout: int = 420
    task_timeout: int = 2400
    max_repairs: int = 3
    max_simulations: int = 3
    max_llm_calls: int = 9
    max_output_tokens: int = 24576
    reasoning_effort: str = "medium"
    context_window_tokens: int = 131072
    selftest_max_cases: int = 0
    selftest_max_steps_per_case: int = 0
    tester_max_output_tokens: int = 0
    planner_max_output_tokens: int = 0
    coder_max_output_tokens: int = 0
    repair_max_output_tokens: int = 0
    max_total_tokens: int = 300000

    def output_limit(self, role: str) -> int:
        if role not in ('planner', 'coder', 'repair', 'tester'):
            raise ValueError('Unknown agent role: ' + role)
        return getattr(self, role + '_max_output_tokens') or self.max_output_tokens

    def get_ascii_work_root(self) -> Path:
        if self.ascii_work_root:
            return Path(self.ascii_work_root)
        tmp = tempfile.gettempdir()
        if not str(tmp).isascii():
            return Path("C:/plc_work" if os.name == "nt" else "/tmp/plc_work")
        return Path(tmp) / "plc_work"

    @classmethod
    def load(cls, config_path=None, load_api=True):
        data = {}
        target_path = None
        if config_path:
            p = Path(config_path)
            if p.is_file():
                target_path = p
        if not target_path:
            local_cfg = ROOT / "configs/runtime.local.json"
            default_cfg = ROOT / "configs/runtime.json"
            if local_cfg.is_file():
                target_path = local_cfg
            elif default_cfg.is_file():
                target_path = default_cfg
        if target_path and target_path.is_file():
            data = read_json(target_path)

        values = {
            k: v
            for k, v in data.items()
            if k in cls.__dataclass_fields__ and k != "api_key"
        }

        # Load environment variables from .env if present
        env_file = ROOT / ".env"
        if env_file.is_file():
            for line in env_file.read_text(encoding="utf-8-sig").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    ek, ev = line.split("=", 1)
                    ek = ek.strip()
                    ev = ev.strip().strip("'\"")
                    if ek and ek not in os.environ:
                        os.environ[ek] = ev

        # Read only a private key and base URL. Never execute TOML/MCP snippets.
        key_path = os.environ.get("PLC_API_CONFIG", "")
        if not key_path:
            for candidate in (ROOT / "APIKEY相关.txt", ROOT.parent / "APIKEY相关.txt"):
                if candidate.is_file():
                    key_path = str(candidate)
                    break
        if key_path and load_api:
            content = Path(key_path).read_text(encoding="utf-8-sig")
            first = content.splitlines()[0].strip()
            match = re.search(r"sk-[A-Za-z0-9_.-]+", first)
            if match:
                values["api_key"] = match.group()
            elif first and "=" not in first and " " not in first:
                values["api_key"] = first
            url = re.search(r'base_url\s*=\s*["\x27](https://[^"\x27]+)', content)
            if url:
                values.setdefault("base_url", url.group(1).rstrip("/"))
        mapping = {
            "PLC_API_BASE_URL": "base_url",
            "PLC_LLM_API_KEY": "api_key",
            "PLC_CODESYS_EXE": "codesys_exe",
            "PLC_CODESYS_PROFILE": "codesys_profile",
            "PLC_CODESYS_TEMPLATE": "codesys_template",
            "PLC_CODESYS_ADDITIONAL_FOLDER": "additional_folder",
            "PLC_ASCII_WORK_ROOT": "ascii_work_root",
        }
        for env, field_name in mapping.items():
            if not load_api and field_name in ("api_key", "base_url"):
                continue
            if os.environ.get(env):
                values[field_name] = os.environ[env]

        # Resolve template path: relative -> absolute, or fallback to repo bundled template
        template = values.get("codesys_template", "")
        bundled_template = ROOT / "codesys/templates/benchmark.project"
        if template:
            tp = Path(template)
            if not tp.is_absolute():
                values["codesys_template"] = str((ROOT / tp).resolve())
            elif not tp.is_file() and bundled_template.is_file():
                values["codesys_template"] = str(bundled_template.resolve())
        elif bundled_template.is_file():
            values["codesys_template"] = str(bundled_template.resolve())

        # Auto-detect CODESYS on Windows if not configured or not found
        if os.name == "nt":
            exe_val = values.get("codesys_exe", "")
            if not exe_val or not Path(exe_val).is_file():
                detected_exe, detected_prof = detect_codesys()
                if detected_exe:
                    values["codesys_exe"] = detected_exe
                if detected_prof and not values.get("codesys_profile"):
                    values["codesys_profile"] = detected_prof

        return cls(**values)

    def compiler_ready(self):
        missing = []
        for key in ("codesys_exe", "codesys_template"):
            if not getattr(self, key) or not Path(getattr(self, key)).is_file():
                missing.append(key)
        if not self.codesys_profile:
            missing.append("codesys_profile")
        return missing
