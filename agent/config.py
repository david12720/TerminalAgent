import tomllib
import os
from dataclasses import dataclass, field
from typing import Optional

CONFIG_FILENAME = "buildagent.toml"


@dataclass
class Config:
    terminal: str = "powershell"
    model: str = "qwen2.5-coder:7b"
    ollama_host: str = "http://localhost:11434"

    @classmethod
    def load(cls, working_dir: str = ".") -> "Config":
        """
        Load config from buildagent.toml in working_dir.
        Falls back to defaults if file doesn't exist.
        """
        config_path = os.path.join(working_dir, CONFIG_FILENAME)
        if not os.path.isfile(config_path):
            return cls()

        with open(config_path, "rb") as f:
            data = tomllib.load(f)

        return cls(
            terminal=data.get("terminal", cls.terminal),
            model=data.get("model", cls.model),
            ollama_host=data.get("ollama_host", cls.ollama_host),
        )
