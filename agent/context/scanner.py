import os
from agent.core.interfaces import IContextScanner
from agent.core.models import ProjectContext
from .project_detector import ProjectDetector


IGNORED_DIRS: frozenset[str] = frozenset({
    ".git", "node_modules", "__pycache__",
    "bin", "obj", ".vs", ".vscode",
    "dist", "build", "out",
    ".venv", "venv", ".env",
    ".idea", ".gradle",
})


class DirectoryScanner(IContextScanner):
    """
    Walks a directory tree (skipping noise dirs) and returns a ProjectContext
    with relative file paths and detected project metadata.
    """

    def __init__(self, detector: ProjectDetector | None = None) -> None:
        self._detector = detector or ProjectDetector()

    def scan(self, path: str) -> ProjectContext:
        files = self._collect_files(path)
        project_type, build_file = self._detector.detect(files)
        return ProjectContext(
            root_path=os.path.abspath(path),
            files=files,
            project_type=project_type,
            build_file=build_file,
        )

    def _collect_files(self, path: str) -> list[str]:
        result: list[str] = []
        for root, dirs, filenames in os.walk(path):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for filename in filenames:
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, path)
                result.append(rel_path.replace("\\", "/"))
        return sorted(result)
