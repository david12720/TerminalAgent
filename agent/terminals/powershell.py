import subprocess
from agent.core.interfaces import ITerminal
from agent.core.models import CommandResult


DANGEROUS_PATTERNS: list[str] = [
    "format-volume",
    "remove-item -recurse -force",
    "clear-disk",
    "remove-partition",
    "initialize-disk",
    "remove-item c:\\",
]


class PowerShellTerminal(ITerminal):
    """
    Executes commands via Windows PowerShell subprocess.
    To add Bash or CMD: implement ITerminal in a new file — no changes needed here.
    """

    def platform_name(self) -> str:
        return "powershell"

    def platform_info(self) -> str:
        return "Windows PowerShell"

    def execute(self, command: str) -> CommandResult:
        self._safety_check(command)
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
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
