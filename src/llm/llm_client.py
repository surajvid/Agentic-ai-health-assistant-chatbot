import ollama
from src.config.settings import settings


class LLMClient:
    """
    Handles interaction with the configured LLM provider.
    Currently supports Ollama.
    """

    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL

    def generate(self, prompt: str) -> str:
        if self.provider != "ollama":
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"]