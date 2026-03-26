# BuildAgent — Architecture & Codebase Context

> This file is the primary Claude context document. Read this before touching any code.

---

## What This Project Does

A CLI tool that accepts a **natural language request** from the user, translates it to a shell command using a **local LLM (Ollama)**, and executes it. No internet required.

```
user: "build this project"
        ↓
DirectoryScanner  →  ProjectContext (files, type, build file)
        ↓
OllamaProvider    →  "dotnet build MyApp.csproj"
        ↓
PowerShellTerminal → subprocess → stdout/stderr
```

---

## Design Principles

- **SOLID throughout**: each class has one job, depends on abstractions, open for extension
- **No agent loop** (by design for v1): single-shot NL → command → execute
- **Offline-first**: only dependency is a running Ollama instance on localhost

---

## File Map

```
main.py                                   Entry point. Wires all dependencies and runs the agent.
requirements.txt                          Python dependencies (ollama SDK only).

agent/core/interfaces.py                  The 3 core abstractions: ITerminal, ILLMProvider, IContextScanner
agent/core/models.py                      Dataclasses: CommandResult, ProjectContext
agent/core/agent.py                       Orchestrator: scans → builds prompt → translates → executes

agent/context/scanner.py                  Walks directory tree, ignores noise dirs, returns sorted file list
agent/context/project_detector.py         Maps file list → (project_type, build_file) using INDICATORS table

agent/llm/ollama_provider.py              Calls local Ollama HTTP API. System prompt lives here.
agent/terminals/powershell.py             Runs commands via PowerShell subprocess. Safety blocklist here.
```

---

## Key Abstractions (`agent/core/interfaces.py`)

| Interface | Responsibility | Current Implementation |
|---|---|---|
| `ITerminal` | Execute a command, report platform info | `PowerShellTerminal` |
| `ILLMProvider` | Translate NL + context → command string | `OllamaProvider` |
| `IContextScanner` | Scan directory → `ProjectContext` | `DirectoryScanner` |

---

## Data Flow (detailed)

1. `main.py` instantiates concrete classes and passes them to `Agent`
2. `Agent.run(user_input, working_dir)` is called
3. `DirectoryScanner.scan(working_dir)` → `ProjectContext`
   - Walks dir tree, skips `IGNORED_DIRS` (node_modules, .git, bin, obj, etc.)
   - `ProjectDetector.detect(files)` → first match in `INDICATORS` table
4. `Agent._build_context_string(context)` builds a text block with platform, dir, project type, file list
5. `OllamaProvider.translate(user_input, context_str)` → raw command string
   - If LLM returns `ERROR: ...` → `Agent.run` raises `ValueError`
6. `PowerShellTerminal.execute(command)` → `CommandResult`
   - Safety blocklist checked before subprocess call
7. `main.py` prints stdout/stderr, exits with return code

---

## How to Extend

### Add a new terminal (e.g. Bash, CMD)
1. Create `agent/terminals/bash.py` implementing `ITerminal`
2. Implement `execute()`, `platform_name()`, `platform_info()`
3. Pass `BashTerminal()` to `Agent(...)` in `main.py`
4. No other files need to change

### Add a new LLM provider (e.g. OpenAI-compatible, llama-cpp-python)
1. Create `agent/llm/openai_provider.py` implementing `ILLMProvider`
2. Implement `translate(user_input, context) -> str`
3. Pass it to `Agent(...)` in `main.py`

### Add new project type detection
- Open `agent/context/project_detector.py`
- Add a row to the `INDICATORS` list: `("filename_or_*.ext", "Human Label")`
- Order matters — first match wins

---

## Status: What Is Done vs TODO

### Done (v1 — PowerShell)
- [x] Core abstractions and data models
- [x] Directory scanner with ignore list
- [x] Project type detector (13 project types)
- [x] Ollama LLM provider
- [x] PowerShell terminal with safety blocklist
- [x] Agent orchestrator
- [x] CLI entry point (`main.py`)

### TODO (planned next)
- [ ] `agent/terminals/bash.py` — Linux/macOS Bash terminal
- [ ] `agent/terminals/cmd.py` — Windows CMD terminal
- [ ] CLI flag `--terminal powershell|bash|cmd` to select terminal at runtime
- [ ] CLI flag `--model` to override Ollama model
- [ ] CLI flag `--dry-run` to print command without executing
- [ ] Multi-step agent loop mode (optional, opt-in)
- [ ] Config file (`buildagent.toml`) for defaults

---

## Dependencies

```
Python >= 3.11  (uses X | Y union syntax and list[str] generics)
ollama          (pip install ollama) — Python SDK for Ollama
Ollama server   (https://ollama.com) running locally on :11434
```

Recommended models (balance speed vs quality):
- `qwen2.5-coder:7b` — best for code/shell tasks, default
- `mistral:7b` — good general purpose fallback
- `deepseek-coder:6.7b` — alternative for code tasks
