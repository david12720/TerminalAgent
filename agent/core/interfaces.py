from abc import ABC, abstractmethod
from .models import CommandResult, ProjectContext


class ITerminal(ABC):
    """Executes shell commands on a specific platform/shell."""

    @abstractmethod
    def execute(self, command: str) -> CommandResult: ...

    @abstractmethod
    def platform_name(self) -> str:
        """Short identifier, e.g. 'powershell', 'bash', 'cmd'."""
        ...

    @abstractmethod
    def platform_info(self) -> str:
        """Human-readable description injected into the LLM prompt."""
        ...


class ILLMProvider(ABC):
    """Translates natural language to a shell command string."""

    @abstractmethod
    def translate(self, user_input: str, context: str) -> str: ...


class IContextScanner(ABC):
    """Scans a directory and returns structured project context."""

    @abstractmethod
    def scan(self, path: str) -> ProjectContext: ...
