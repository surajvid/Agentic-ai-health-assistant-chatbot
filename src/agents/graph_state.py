from typing import TypedDict, Optional, Dict, Any


class HealthAgentState(TypedDict):
    """
    Shared state object passed between LangGraph nodes.
    """
    user_query: str
    route: Optional[str]
    analysis_summary: Optional[str]
    safety_message: Optional[str]
    final_response: Optional[str]
    metadata: Dict[str, Any]