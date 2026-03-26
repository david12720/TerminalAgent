from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CommandResult:
    command: str
    stdout: str
    stderr: str
    return_code: int

    @property
    def success(self) -> bool:
        return self.return_code == 0


@dataclass
class ProjectContext:
    root_path: str
    files: list[str] = field(default_factory=list)
    project_type: Optional[str] = None
    build_file: Optional[str] = None
