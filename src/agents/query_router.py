class QueryRouter:
    """
    Routes the user query to the most relevant analysis path.
    """

    @staticmethod
    def route_query(user_query: str) -> str:
        query = user_query.lower()

        if any(word in query for word in ["smoking", "smoker", "tobacco"]):
            return "smoking_analysis"

        if any(word in query for word in ["activity", "exercise", "physical activity", "steps"]):
            return "activity_analysis"

        if any(word in query for word in ["stress", "mental", "pressure"]):
            return "stress_analysis"

        if any(word in query for word in ["risk", "high risk", "wellness risk"]):
            return "risk_analysis"

        return "general_summary"