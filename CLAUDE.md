# Claude Context — BuildAgent

Read ARCHITECTURE.md before making any changes to this project.

## Key Rules
- Follow SOLID principles — all new features go through interfaces in `agent/core/interfaces.py`
- Never put logic directly in `Agent` that belongs in a terminal, provider, or scanner
- PowerShell is the current terminal — Bash and CMD are next
- Offline-first: only external dependency is a local Ollama instance
- Python 3.11+ required (uses `X | Y` union syntax)

## Quick Start for Development
1. Read `ARCHITECTURE.md` for full design, file map, and data flow
2. Read `README.md` for usage examples
3. Check the TODO section in `ARCHITECTURE.md` for next steps
