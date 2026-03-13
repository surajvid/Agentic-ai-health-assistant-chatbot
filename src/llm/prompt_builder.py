from src.llm.prompt_templates import (
    SYSTEM_PROMPT,
    OUTPUT_FORMAT_PROMPT,
    ROUTE_PROMPT_MAP,
)


class PromptBuilder:
    """
    Builds safe, grounded, route-aware prompts for the conversational AI layer.
    """

    @staticmethod
    def get_route_instruction(route: str | None) -> str:
        if not route:
            return ROUTE_PROMPT_MAP["general_summary"]

        return ROUTE_PROMPT_MAP.get(route, ROUTE_PROMPT_MAP["general_summary"])

    @staticmethod
    def build_health_summary_prompt(
        user_query: str,
        analysis_summary: str,
        route: str | None = None
    ) -> str:
        route_instruction = PromptBuilder.get_route_instruction(route)

        prompt = f"""
{SYSTEM_PROMPT}

Route-specific guidance:
{route_instruction}

User question:
{user_query}

Structured analysis summary:
{analysis_summary}

{OUTPUT_FORMAT_PROMPT}
"""
        return prompt.strip()