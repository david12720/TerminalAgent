from agent.core.interfaces import ITerminal
from .powershell import PowerShellTerminal
from .bash import BashTerminal
from .cmd import CmdTerminal


TERMINALS: dict[str, type[ITerminal]] = {
    "powershell": PowerShellTerminal,
    "bash": BashTerminal,
    "cmd": CmdTerminal,
}


def get_terminal(name: str) -> ITerminal:
    """Lookup terminal by name. Raises KeyError if not found."""
    cls = TERMINALS.get(name.lower())
    if cls is None:
        available = ", ".join(sorted(TERMINALS.keys()))
        raise KeyError(f"Unknown terminal '{name}'. Available: {available}")
    return cls()
