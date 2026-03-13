from pydantic import BaseModel
from typing import Optional


class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    route: Optional[str]
    safety_message: Optional[str]
    analysis_summary: Optional[str]
    final_response: Optional[str]


class HealthResponse(BaseModel):
    status: str
    llm_provider: str
    llm_model: str