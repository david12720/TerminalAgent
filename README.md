# BuildAgent

A lightweight CLI tool that translates natural language into shell commands and runs them — fully offline using a local LLM.

```
$ python main.py "build this project"
[>] build this project
[$] dotnet build MyApp.csproj

Build succeeded.
    0 Warning(s)
    0 Error(s)
```

---

## Requirements

- Python 3.11+
- [Ollama](https://ollama.com) running locally (`ollama serve`)
- A pulled model: `ollama pull qwen2.5-coder:7b`

```bash
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py "<natural language request>"
```

Examples:
```bash
python main.py "build this project"
python main.py "run the tests"
python main.py "clean build artifacts"
python main.py "list all cs files"
```

The agent automatically:
1. Scans the current directory for project files
2. Detects the project type (Node.js, .NET, CMake, Rust, Go, Maven, etc.)
3. Asks the local LLM to generate the right command
4. Executes it and shows the output

---

## Supported Project Types

| Indicator File | Detected As |
|---|---|
| `package.json` | Node.js |
| `pom.xml` | Maven (Java) |
| `build.gradle` | Gradle (Java/Kotlin) |
| `CMakeLists.txt` | CMake (C/C++) |
| `Makefile` | Make |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `*.csproj` / `*.sln` | .NET (C#) |
| `pyproject.toml` / `setup.py` | Python |
| `Dockerfile` | Docker |

---

## Supported Terminals

| Terminal | Status |
|---|---|
| PowerShell (Windows) | ✅ Done |
| Bash (Linux/macOS) | 🔜 Planned |
| CMD (Windows) | 🔜 Planned |

---

## Configuration

Edit `main.py` to change defaults:

```python
Agent(
    terminal=PowerShellTerminal(),
    llm=OllamaProvider(model="qwen2.5-coder:7b", host="http://localhost:11434"),
    scanner=DirectoryScanner(),
)
```

---

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for full design details, data flow, and extension guide.

**Quick summary:**

```
IContextScanner  →  scans directory, detects project type
ILLMProvider     →  translates NL + context to a shell command
ITerminal        →  executes the command, returns stdout/stderr
```

All three are interfaces — swap any implementation without changing the core.

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Command ran and succeeded |
| `1` | Command ran but failed, or LLM returned an error |
| `2` | Ollama not reachable |
