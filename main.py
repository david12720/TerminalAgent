import argparse
import sys
import os

from agent.core.agent import Agent
from agent.context.scanner import DirectoryScanner
from agent.llm.ollama_provider import OllamaProvider
from agent.terminals.registry import get_terminal
from agent.config import Config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="buildagent",
        description="Translate natural language to shell commands using a local LLM.",
    )
    parser.add_argument(
        "request",
        nargs="+",
        help="Natural language request (e.g. 'build this project')",
    )
    parser.add_argument(
        "--terminal", "-t",
        choices=["powershell", "bash", "cmd"],
        default=None,
        help="Shell to use (default: from config or powershell)",
    )
    parser.add_argument(
        "--model", "-m",
        default=None,
        help="Ollama model name (default: from config or qwen2.5-coder:7b)",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Print the generated command without executing it",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Ollama server URL (default: http://localhost:11434)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    working_dir = os.getcwd()

    # Config file provides defaults; CLI flags override
    config = Config.load(working_dir)
    terminal_name = args.terminal or config.terminal
    model = args.model or config.model
    host = args.host or config.ollama_host

    user_input = " ".join(args.request)

    terminal = get_terminal(terminal_name)
    agent = Agent(
        terminal=terminal,
        llm=OllamaProvider(model=model, host=host),
        scanner=DirectoryScanner(),
    )

    print(f"[>] {user_input}")
    print(f"[~] terminal={terminal_name}  model={model}")

    try:
        if args.dry_run:
            context = agent._scanner.scan(working_dir)
            context_str = agent._build_context_string(context)
            command = agent._llm.translate(user_input, context_str)
            print(f"[$] {command}")
            print("[i] Dry run — command not executed.")
            sys.exit(0)

        result = agent.run(user_input, working_dir)
        print(f"[$] {result.command}\n")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"[!] {result.stderr}", file=sys.stderr)
        sys.exit(0 if result.success else result.return_code)

    except ValueError as exc:
        print(f"[!] {exc}", file=sys.stderr)
        sys.exit(1)

    except ConnectionError as exc:
        print(f"[!] {exc}", file=sys.stderr)
        sys.exit(2)

    except KeyError as exc:
        print(f"[!] {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
