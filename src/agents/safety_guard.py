from src.policy.policy_engine import PolicyEngine


class SafetyGuard:
    """
    Applies policy checks for health-related conversational responses.
    """

    @staticmethod
    def check_query(user_query: str, route: str | None = None) -> str | None:
        decision = PolicyEngine.evaluate_query(user_query=user_query, route=route)

        if not decision.allowed:
            return decision.blocked_response

        return None