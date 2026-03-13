from src.llm.llm_client import LLMClient
from src.llm.prompt_builder import PromptBuilder


class ResponseGenerator:
    """
    Orchestrates prompt creation and LLM response generation.
    """

    def __init__(self):
        self.llm_client = LLMClient()

    def generate_health_response(
        self,
        user_query: str,
        analysis_summary: str,
        route: str | None = None
    ) -> str:
        prompt = PromptBuilder.build_health_summary_prompt(
            user_query=user_query,
            analysis_summary=analysis_summary,
            route=route
        )

        response = self.llm_client.generate(prompt)
        return response