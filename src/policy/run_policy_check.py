from src.policy.policy_engine import PolicyEngine


def main():
    sample_queries = [
        "Summarize the key wellness risks visible in this dataset.",
        "What does the data suggest about smoking and wellness risk?",
        "Can you prescribe medication for high-risk patients?",
        "Can you diagnose which patients are sick?",
        "Can you identify this patient for me?",
    ]

    for query in sample_queries:
        decision = PolicyEngine.evaluate_query(query)

        print("\n" + "=" * 80)
        print("QUERY:", query)
        print("ALLOWED:", decision.allowed)
        print("CATEGORY:", decision.category)
        print("REASON:", decision.reason)
        print("DISCLAIMER:", decision.disclaimer)
        print("BLOCKED_RESPONSE:", decision.blocked_response)


if __name__ == "__main__":
    main()