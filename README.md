# BuildAgent

A lightweight CLI tool that translates natural language into shell commands and runs them — fully offline using a local LLM.

```
$ python main.py "build this project"
[>] build this project
[~] terminal=powershell  model=qwen2.5-coder:7b
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

### CLI Flags

| Flag | Short | Description |
|---|---|---|
| `--terminal` | `-t` | Shell to use: `powershell`, `bash`, `cmd` |
| `--model` | `-m` | Ollama model name |
| `--dry-run` | `-n` | Print command without executing |
| `--host` | | Ollama server URL |

```bash
# Use Bash instead of PowerShell
python main.py -t bash "build this project"

# Use a different model
python main.py -m mistral:7b "run the tests"

# See the command without running it
python main.py --dry-run "deploy to staging"
```

---

## Configuration

Create a `buildagent.toml` in your project directory (see `buildagent.example.toml`):

```toml
terminal = "powershell"
model = "qwen2.5-coder:7b"
ollama_host = "http://localhost:11434"
```

Priority: CLI flags > `buildagent.toml` > built-in defaults.

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
| PowerShell (Windows) | Done |
| Bash (Linux/macOS) | Done |
| CMD (Windows) | Done |

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
