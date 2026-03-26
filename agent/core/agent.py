from .interfaces import ITerminal, ILLMProvider, IContextScanner
from .models import CommandResult, ProjectContext


class Agent:
    """
    Orchestrates the NL → command → execution pipeline.

    Depends only on abstractions (ITerminal, ILLMProvider, IContextScanner)
    so each piece is independently swappable without touching this class.
    """

    def __init__(
        self,
        terminal: ITerminal,
        llm: ILLMProvider,
        scanner: IContextScanner,
    ) -> None:
        self._terminal = terminal
        self._llm = llm
        self._scanner = scanner

    def run(self, user_input: str, working_dir: str = ".") -> CommandResult:
        context = self._scanner.scan(working_dir)
        context_str = self._build_context_string(context)
        command = self._llm.translate(user_input, context_str)

        if command.upper().startswith("ERROR:"):
            raise ValueError(command)

        return self._terminal.execute(command)

    def _build_context_string(self, context: ProjectContext) -> str:
        lines = [
            f"Platform: {self._terminal.platform_info()}",
            f"Working directory: {context.root_path}",
        ]
        if context.project_type:
            lines.append(f"Detected project type: {context.project_type}")
        if context.build_file:
            lines.append(f"Primary build file: {context.build_file}")

        lines.append("Files in project:")
        lines.extend(f"  {f}" for f in context.files[:60])
        if len(context.files) > 60:
            lines.append(f"  ... and {len(context.files) - 60} more")

        return "\n".join(lines)
