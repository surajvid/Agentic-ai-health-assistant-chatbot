from langgraph.graph import StateGraph, END

from src.agents.graph_state import HealthAgentState
from src.agents.graph_nodes import (
    route_query_node,
    safety_check_node,
    build_analysis_node,
    generate_response_node,
    blocked_response_node,
)
from src.monitoring.logger import setup_logger
from src.monitoring.metrics import Timer, QueryMetrics


class LangGraphWorkflow:
    """
    LangGraph-based agent workflow for the health assistant project.
    """

    def __init__(self):
        self.app = self._build_graph()
        self.logger = setup_logger("langgraph_workflow")

    def _build_graph(self):
        workflow = StateGraph(HealthAgentState)

        workflow.add_node("route_query", route_query_node)
        workflow.add_node("safety_check", safety_check_node)
        workflow.add_node("build_analysis", build_analysis_node)
        workflow.add_node("generate_response", generate_response_node)
        workflow.add_node("blocked_response", blocked_response_node)

        workflow.set_entry_point("route_query")
        workflow.add_edge("route_query", "safety_check")

        workflow.add_conditional_edges(
            "safety_check",
            self._safety_router,
            {
                "blocked": "blocked_response",
                "safe": "build_analysis",
            }
        )

        workflow.add_edge("build_analysis", "generate_response")
        workflow.add_edge("generate_response", END)
        workflow.add_edge("blocked_response", END)

        return workflow.compile()

    @staticmethod
    def _safety_router(state):
        if state.get("safety_message"):
            return "blocked"
        return "safe"

    def run(self, user_query: str, patient_df):
        timer = Timer()
        timer.start()

        self.logger.info(f"Received query: {user_query}")

        initial_state = {
            "user_query": user_query,
            "route": None,
            "analysis_summary": None,
            "safety_message": None,
            "final_response": None,
            "metadata": {
                "patient_df": patient_df
            }
        }

        try:
            result = self.app.invoke(initial_state)

            timer.stop()

            metrics = QueryMetrics(
                user_query=user_query,
                route=result.get("route"),
                safety_triggered=result.get("safety_message") is not None,
                success=True,
                duration_seconds=timer.duration(),
                error_message=None
            )

            self.logger.info(
                f"Workflow success | metrics={metrics.to_dict()}"
            )

            return result

        except Exception as e:
            timer.stop()

            metrics = QueryMetrics(
                user_query=user_query,
                route=None,
                safety_triggered=False,
                success=False,
                duration_seconds=timer.duration(),
                error_message=str(e)
            )

            self.logger.error(
                f"Workflow failed | metrics={metrics.to_dict()}"
            )

            raise