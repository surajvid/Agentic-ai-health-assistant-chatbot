from src.llm.prompt_builder import PromptBuilder


def main():
    sample_query = "What does the data suggest about smoking and wellness risk?"
    sample_route = "smoking_analysis"
    sample_analysis_summary = """
SMOKING ANALYSIS
- {'smoking_distribution': {'0': 1200, '1': 800}, 'smoking_vs_risk': {'high': {0: 300, 1: 500}, 'moderate': {0: 400, 1: 200}, 'low': {0: 500, 1: 100}}}

RISK CONTEXT
- {'risk_flag_distribution': {'high': 800, 'moderate': 600, 'low': 600}, 'avg_risk_score': 2.1, 'max_risk_score': 5.0, 'min_risk_score': 0.0}
"""

    prompt = PromptBuilder.build_health_summary_prompt(
        user_query=sample_query,
        analysis_summary=sample_analysis_summary,
        route=sample_route
    )

    print(prompt)


if __name__ == "__main__":
    main()