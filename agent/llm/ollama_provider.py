import ollama
from agent.core.interfaces import ILLMProvider


SYSTEM_PROMPT = """\
You are a shell command expert. Translate the user's natural language request \
into a single shell command appropriate for the given platform and project context.

Rules:
- Output ONLY the raw command. No explanation, no markdown, no code fences.
- Match the shell syntax exactly to the platform specified in the context.
- Use the project context (detected type, build file, file list) to pick the \
  correct tool and arguments.
- If the request is ambiguous, unsafe, or impossible to translate, output:
  ERROR: <short reason>
"""


class OllamaProvider(ILLMProvider):
    """
    LLM provider backed by a local Ollama instance.
    Swap this class for any other ILLMProvider implementation
    (e.g. OpenAI, LlamaCpp) without touching Agent.
    """

    def __init__(
        self,
        model: str = "qwen2.5-coder:7b",
        host: str = "http://localhost:11434",
    ) -> None:
        self._model = model
        self._client = ollama.Client(host=host)

    def translate(self, user_input: str, context: str) -> str:
        try:
            response = self._client.chat(
                model=self._model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Project context:\n{context}\n\nRequest: {user_input}",
                    },
                ],
            )
            return response.message.content.strip()
        except Exception as exc:
            raise ConnectionError(
                f"Ollama unreachable. Is it running? Details: {exc}"
            ) from exc
