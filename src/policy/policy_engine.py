from dataclasses import dataclass
from typing import Optional

from src.policy.policy_rules import (
    DISALLOWED_MEDICAL_TERMS,
    HIGH_RISK_ADVICE_TERMS,
    PRIVACY_SENSITIVE_TERMS,
    ALLOWED_ANALYTICS_CATEGORIES,
    DEFAULT_DISCLAIMER,
    BLOCKED_RESPONSE,
)


@dataclass
class PolicyDecision:
    allowed: bool
    category: str
    reason: Optional[str] = None
    disclaimer: Optional[str] = DEFAULT_DISCLAIMER
    blocked_response: Optional[str] = None


class PolicyEngine:
    """
    Central policy layer for validating whether a user query is safe
    and within the allowed analytical scope.
    """

    @staticmethod
    def evaluate_query(user_query: str, route: Optional[str] = None) -> PolicyDecision:
        query = user_query.lower().strip()

        if any(term in query for term in PRIVACY_SENSITIVE_TERMS):
            return PolicyDecision(
                allowed=False,
                category="privacy_violation",
                reason="Query attempts to identify or expose patient identity.",
                disclaimer=DEFAULT_DISCLAIMER,
                blocked_response=BLOCKED_RESPONSE,
            )

        if any(term in query for term in DISALLOWED_MEDICAL_TERMS):
            return PolicyDecision(
                allowed=False,
                category="medical_restriction",
                reason="Query requests diagnosis, medication, or treatment advice.",
                disclaimer=DEFAULT_DISCLAIMER,
                blocked_response=BLOCKED_RESPONSE,
            )

        if any(term in query for term in HIGH_RISK_ADVICE_TERMS):
            return PolicyDecision(
                allowed=False,
                category="clinical_advice_restriction",
                reason="Query requests medical or clinical advice beyond allowed scope.",
                disclaimer=DEFAULT_DISCLAIMER,
                blocked_response=BLOCKED_RESPONSE,
            )

        if route and route not in ALLOWED_ANALYTICS_CATEGORIES:
            return PolicyDecision(
                allowed=False,
                category="unsupported_route",
                reason=f"Route '{route}' is not in the allowed analytics categories.",
                disclaimer=DEFAULT_DISCLAIMER,
                blocked_response=BLOCKED_RESPONSE,
            )

        return PolicyDecision(
            allowed=True,
            category="allowed",
            reason="Query is within the permitted wellness analytics scope.",
            disclaimer=DEFAULT_DISCLAIMER,
            blocked_response=None,
        )