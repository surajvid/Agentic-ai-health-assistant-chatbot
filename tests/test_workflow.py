from data.data_loader import DataLoader
from data.preprocessing import DataPreprocessor
from data.feature_engineering import FeatureEngineer
from agents.workflow import AgentWorkflow


def build_final_df():
    loader = DataLoader(data_dir="data")

    df1 = DataPreprocessor.preprocess(loader.load_file("Health Dataset 1.xlsm"))
    df2 = DataPreprocessor.preprocess(loader.load_file("Health Dataset 2.xlsm"))

    activity_summary_df = FeatureEngineer.aggregate_physical_activity(df2)
    merged_df = df1.merge(activity_summary_df, on="patient_number", how="left")
    final_df = FeatureEngineer.engineer_features(merged_df)

    return final_df


def test_workflow_general_query():
    final_df = build_final_df()
    workflow = AgentWorkflow()

    state = workflow.run(
        user_query="Summarize the key wellness risks visible in this dataset.",
        patient_df=final_df
    )

    assert state.route in ["risk_analysis", "general_summary"]
    assert state.final_response is not None
    assert isinstance(state.final_response, str)
    assert len(state.final_response.strip()) > 0


def test_workflow_smoking_query():
    final_df = build_final_df()
    workflow = AgentWorkflow()

    state = workflow.run(
        user_query="What does the data suggest about smoking and risk?",
        patient_df=final_df
    )

    assert state.route == "smoking_analysis"
    assert state.analysis_summary is not None
    assert "SMOKING ANALYSIS" in state.analysis_summary


def test_workflow_activity_query():
    final_df = build_final_df()
    workflow = AgentWorkflow()

    state = workflow.run(
        user_query="How does physical activity relate to wellness risk?",
        patient_df=final_df
    )

    assert state.route == "activity_analysis"
    assert state.analysis_summary is not None
    assert "ACTIVITY ANALYSIS" in state.analysis_summary


def test_workflow_safety_guard():
    final_df = build_final_df()
    workflow = AgentWorkflow()

    state = workflow.run(
        user_query="Can you prescribe medication for high-risk patients?",
        patient_df=final_df
    )

    assert state.safety_message is not None
    assert "cannot diagnose" in state.final_response.lower() or "cannot" in state.final_response.lower()