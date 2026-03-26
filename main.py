import sys
import os

from agent.core.agent import Agent
from agent.context.scanner import DirectoryScanner
from agent.llm.ollama_provider import OllamaProvider
from agent.terminals.powershell import PowerShellTerminal


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<natural language request>\"")
        print("Example: python main.py \"build this project\"")
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])
    working_dir = os.getcwd()

    agent = Agent(
        terminal=PowerShellTerminal(),
        llm=OllamaProvider(model="qwen2.5-coder:7b"),
        scanner=DirectoryScanner(),
    )

    print(f"[>] {user_input}")

    try:
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


if __name__ == "__main__":
    main()
