import subprocess
from agent.core.interfaces import ITerminal
from agent.core.models import CommandResult


DANGEROUS_PATTERNS: list[str] = [
    "rm -rf /",
    "mkfs.",
    "dd if=",
    ":(){:|:&};:",
    "> /dev/sda",
    "chmod -r 777 /",
]


class BashTerminal(ITerminal):
    """Executes commands via Bash subprocess (Linux/macOS)."""

    def platform_name(self) -> str:
        return "bash"

    def platform_info(self) -> str:
        return "Linux/macOS Bash"

    def execute(self, command: str) -> CommandResult:
        self._safety_check(command)
        result = subprocess.run(
            ["bash", "-c", command],
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
