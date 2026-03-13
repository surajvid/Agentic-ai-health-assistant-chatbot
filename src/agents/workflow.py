from agents.state import AgentState
from agents.query_router import QueryRouter
from agents.safety_guard import SafetyGuard
from data.data_analyzer import DataAnalyzer
from llm.response_generator import ResponseGenerator


class AgentWorkflow:
    """
    Main orchestration layer for the conversational AI workflow.
    """

    def __init__(self):
        self.response_generator = ResponseGenerator()

    def run(self, user_query: str, patient_df) -> AgentState:
        state = AgentState(user_query=user_query)

        # Step 1: route query
        state.route = QueryRouter.route_query(user_query)

        # Step 2: safety check
        safety_message = SafetyGuard.check_query(user_query)
        if safety_message:
            state.safety_message = safety_message
            state.final_response = safety_message
            return state

        # Step 3: data analysis based on route
        state.analysis_summary = DataAnalyzer.build_route_summary(
            df=patient_df,
            route=state.route
        )

        # Step 4: response generation
        state.final_response = self.response_generator.generate_health_response(
            user_query=state.user_query,
            analysis_summary=state.analysis_summary
        )

        return state