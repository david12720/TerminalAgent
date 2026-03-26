from typing import Optional, Tuple


# Ordered by specificity — first match wins.
# Each entry: (filename_or_glob, human_readable_project_type)
INDICATORS: list[tuple[str, str]] = [
    ("package.json",      "Node.js"),
    ("pom.xml",           "Maven (Java)"),
    ("build.gradle",      "Gradle (Java/Kotlin)"),
    ("build.gradle.kts",  "Gradle Kotlin DSL"),
    ("CMakeLists.txt",    "CMake (C/C++)"),
    ("Makefile",          "Make (C/C++)"),
    ("Cargo.toml",        "Rust"),
    ("go.mod",            "Go"),
    ("*.csproj",          ".NET (C#)"),
    ("*.sln",             ".NET Solution"),
    ("pyproject.toml",    "Python (pyproject)"),
    ("setup.py",          "Python (setup.py)"),
    ("requirements.txt",  "Python"),
    ("Dockerfile",        "Docker"),
]


class ProjectDetector:
    """
    Single responsibility: map a list of relative file paths to a
    (project_type, build_file) pair using known indicator files.
    """

    def detect(self, files: list[str]) -> Tuple[Optional[str], Optional[str]]:
        for indicator, project_type in INDICATORS:
            matched = self._match(indicator, files)
            if matched:
                return project_type, matched
        return None, None

    @staticmethod
    def _match(indicator: str, files: list[str]) -> Optional[str]:
        if "*" in indicator:
            ext = indicator.lstrip("*")
            return next((f for f in files if f.endswith(ext)), None)
        return next(
            (f for f in files if f.split("/")[-1].lower() == indicator.lower()),
            None,
        )
