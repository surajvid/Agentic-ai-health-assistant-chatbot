from fastapi import FastAPI, HTTPException
from src.api.schemas import AskRequest, AskResponse, HealthResponse
from src.api.dependencies import build_final_dataframe
from src.agents.langgraph_workflow import LangGraphWorkflow
from src.config.settings import settings

app = FastAPI(
    title="Agentic AI Health Assistant",
    description="Conversational AI system for wellness-oriented health dataset analysis",
    version="1.0.0"
)

workflow = LangGraphWorkflow()


@app.get("/")
def root():
    return {
        "message": "Agentic AI Health Assistant API is running"
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        llm_provider=settings.LLM_PROVIDER,
        llm_model=settings.LLM_MODEL
    )


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    try:
        final_df = build_final_dataframe()

        result = workflow.run(
            user_query=request.query,
            patient_df=final_df
        )

        return AskResponse(
            route=result.get("route"),
            safety_message=result.get("safety_message"),
            analysis_summary=result.get("analysis_summary"),
            final_response=result.get("final_response")
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))