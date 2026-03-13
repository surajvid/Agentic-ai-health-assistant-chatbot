from src.agents.query_router import QueryRouter
from src.agents.safety_guard import SafetyGuard
from src.data.data_analyzer import DataAnalyzer
from src.llm.response_generator import ResponseGenerator


response_generator = ResponseGenerator()


def route_query_node(state):
    user_query = state["user_query"]
    route = QueryRouter.route_query(user_query)

    return {
        **state,
        "route": route
    }


def safety_check_node(state):
    user_query = state["user_query"]
    route = state.get("route")
    safety_message = SafetyGuard.check_query(user_query, route=route)

    return {
        **state,
        "safety_message": safety_message
    }


def build_analysis_node(state):
    patient_df = state["metadata"]["patient_df"]
    route = state["route"]

    analysis_summary = DataAnalyzer.build_route_summary(
        df=patient_df,
        route=route
    )

    return {
        **state,
        "analysis_summary": analysis_summary
    }


def generate_response_node(state):
    final_response = response_generator.generate_health_response(
        user_query=state["user_query"],
        analysis_summary=state["analysis_summary"],
        route=state.get("route")
    )

    return {
        **state,
        "final_response": final_response
    }


def blocked_response_node(state):
    return {
        **state,
        "final_response": state["safety_message"]
    }