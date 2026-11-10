from __future__ import annotations
import os
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from .common import ROOT, read_json

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
    llm_timeout: int = 180
    task_timeout: int = 1500
    max_repairs: int = 3
    max_simulations: int = 3
    max_llm_calls: int = 9
    max_output_tokens: int = 8192
    reasoning_effort: str = "medium"

    def get_ascii_work_root(self) -> Path:
        if self.ascii_work_root:
            return Path(self.ascii_work_root)
        tmp = tempfile.gettempdir()
        if not str(tmp).isascii():
            return Path("C:/plc_work" if os.name == "nt" else "/tmp/plc_work")
        return Path(tmp) / "plc_work"

    @classmethod
    def load(cls, config_path=None, load_api=True):
        data = read_json(config_path) if config_path else {}
        values = {k: v for k, v in data.items() if k in cls.__dataclass_fields__ and k != "api_key"}
        # Read only a private key and base URL. Never execute TOML/MCP snippets.
        key_path = os.environ.get("PLC_API_CONFIG", "")
        if not key_path:
            candidate = ROOT.parent / "APIKEY相关.txt"
            if candidate.is_file():
                key_path = str(candidate)
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
        mapping = {"PLC_API_BASE_URL": "base_url", "PLC_LLM_API_KEY": "api_key",
                   "PLC_CODESYS_EXE": "codesys_exe", "PLC_CODESYS_PROFILE": "codesys_profile",
                   "PLC_CODESYS_TEMPLATE": "codesys_template",
                   "PLC_CODESYS_ADDITIONAL_FOLDER": "additional_folder",
                   "PLC_ASCII_WORK_ROOT": "ascii_work_root"}
        for env, field_name in mapping.items():
            if not load_api and field_name in ("api_key", "base_url"):
                continue
            if os.environ.get(env):
                values[field_name] = os.environ[env]
        return cls(**values)

    def compiler_ready(self):
        missing = []
        for key in ("codesys_exe", "codesys_template"):
            if not getattr(self, key) or not Path(getattr(self, key)).is_file():
                missing.append(key)
        if not self.codesys_profile:
            missing.append("codesys_profile")
        return missing
