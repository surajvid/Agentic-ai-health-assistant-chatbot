from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AgentState:
    """
    Stores the current workflow state for the agent.
    """

    user_query: str
    route: Optional[str] = None
    analysis_summary: Optional[str] = None
    safety_message: Optional[str] = None
    final_response: Optional[str] = None
    metadata: dict = field(default_factory=dict)