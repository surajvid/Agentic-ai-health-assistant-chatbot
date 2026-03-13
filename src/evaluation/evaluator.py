from src.agents.langgraph_workflow import LangGraphWorkflow


class Evaluator:
    """
    Evaluates the conversational AI system on routing, safety, and response generation.
    """

    def __init__(self, patient_df):
        self.patient_df = patient_df
        self.workflow = LangGraphWorkflow()

    def evaluate_test_case(self, test_case: dict) -> dict:
        query = test_case["query"]
        expected_route = test_case["expected_route"]
        should_trigger_safety = test_case["should_trigger_safety"]

        result = self.workflow.run(
            user_query=query,
            patient_df=self.patient_df
        )

        actual_route = result.get("route")
        actual_safety_message = result.get("safety_message")
        actual_response = result.get("final_response")
        analysis_summary = result.get("analysis_summary")

        route_match = actual_route == expected_route
        safety_match = (actual_safety_message is not None) == should_trigger_safety
        response_present = isinstance(actual_response, str) and len(actual_response.strip()) > 0

        analysis_present = True
        if not should_trigger_safety:
            analysis_present = isinstance(analysis_summary, str) and len(analysis_summary.strip()) > 0

        return {
            "query": query,
            "category": test_case["category"],
            "expected_route": expected_route,
            "actual_route": actual_route,
            "route_match": route_match,
            "expected_safety": should_trigger_safety,
            "actual_safety_triggered": actual_safety_message is not None,
            "safety_match": safety_match,
            "response_present": response_present,
            "analysis_present": analysis_present,
            "final_response": actual_response,
        }

    def evaluate_all(self, test_cases: list[dict]) -> list[dict]:
        return [self.evaluate_test_case(case) for case in test_cases]

    @staticmethod
    def summarize_results(results: list[dict]) -> dict:
        total_cases = len(results)
        route_correct = sum(1 for r in results if r["route_match"])
        safety_correct = sum(1 for r in results if r["safety_match"])
        response_present_count = sum(1 for r in results if r["response_present"])
        analysis_present_count = sum(1 for r in results if r["analysis_present"])

        return {
            "total_cases": total_cases,
            "route_accuracy": round((route_correct / total_cases) * 100, 2) if total_cases else 0.0,
            "safety_accuracy": round((safety_correct / total_cases) * 100, 2) if total_cases else 0.0,
            "response_presence_rate": round((response_present_count / total_cases) * 100, 2) if total_cases else 0.0,
            "analysis_presence_rate": round((analysis_present_count / total_cases) * 100, 2) if total_cases else 0.0,
        }

    @staticmethod
    def build_report(summary: dict, detailed_results: list[dict]) -> str:
        lines = []
        lines.append("MODULE 11 — EVALUATION REPORT")
        lines.append("")
        lines.append(f"Total Test Cases: {summary['total_cases']}")
        lines.append(f"Route Accuracy: {summary['route_accuracy']}%")
        lines.append(f"Safety Accuracy: {summary['safety_accuracy']}%")
        lines.append(f"Response Presence Rate: {summary['response_presence_rate']}%")
        lines.append(f"Analysis Presence Rate: {summary['analysis_presence_rate']}%")
        lines.append("")
        lines.append("DETAILED RESULTS")

        for idx, result in enumerate(detailed_results, start=1):
            lines.append(f"{idx}. Query: {result['query']}")
            lines.append(f"   Category: {result['category']}")
            lines.append(f"   Expected Route: {result['expected_route']}")
            lines.append(f"   Actual Route: {result['actual_route']}")
            lines.append(f"   Route Match: {result['route_match']}")
            lines.append(f"   Expected Safety Trigger: {result['expected_safety']}")
            lines.append(f"   Actual Safety Trigger: {result['actual_safety_triggered']}")
            lines.append(f"   Safety Match: {result['safety_match']}")
            lines.append(f"   Response Present: {result['response_present']}")
            lines.append(f"   Analysis Present: {result['analysis_present']}")
            lines.append("")

        return "\n".join(lines)