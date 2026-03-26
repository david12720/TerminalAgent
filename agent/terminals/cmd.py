import subprocess
from agent.core.interfaces import ITerminal
from agent.core.models import CommandResult


DANGEROUS_PATTERNS: list[str] = [
    "format c:",
    "rd /s /q c:\\",
    "del /f /s /q c:\\",
    "diskpart",
]


class CmdTerminal(ITerminal):
    """Executes commands via Windows CMD subprocess."""

    def platform_name(self) -> str:
        return "cmd"

    def platform_info(self) -> str:
        return "Windows CMD (Command Prompt)"

    def execute(self, command: str) -> CommandResult:
        self._safety_check(command)
        result = subprocess.run(
            ["cmd", "/c", command],
            capture_output=True,
            text=True,
        )
        return CommandResult(
            command=command,
            stdout=result.stdout.strip(),
            stderr=result.stderr.strip(),
            return_code=result.returncode,
        )

    def _safety_check(self, command: str) -> None:
        lower = command.lower()
        for pattern in DANGEROUS_PATTERNS:
            if pattern in lower:
                raise ValueError(
                    f"Blocked potentially dangerous command pattern: '{pattern}'"
                )
