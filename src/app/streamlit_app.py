import os
import sys
from io import BytesIO

# Ensure project root is available in PYTHONPATH for Streamlit execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import streamlit as st

from src.config.settings import settings
from src.data.data_loader import DataLoader
from src.data.preprocessing import DataPreprocessor
from src.data.feature_engineering import FeatureEngineer
from src.data.schema_validator import SchemaValidator
from src.agents.langgraph_workflow import LangGraphWorkflow
from src.monitoring.logger import setup_logger


logger = setup_logger("streamlit_app")


@st.cache_data
def build_final_dataframe():
    """
    Load, preprocess, validate, integrate, and engineer features.
    Cached to avoid recomputing on every UI interaction.
    """
    loader = DataLoader(data_dir="data")

    df1 = loader.load_file("Health Dataset 1.xlsm")
    df2 = loader.load_file("Health Dataset 2.xlsm")

    df1 = DataPreprocessor.preprocess(df1)
    df2 = DataPreprocessor.preprocess(df2)

    dataset_1_required_columns = [
        "patient_number",
        "blood_pressure_abnormality",
        "level_of_hemoglobin",
        "genetic_pedigree_coefficient",
        "age",
        "bmi",
        "sex",
        "pregnancy",
        "smoking",
        "salt_content_in_the_diet",
        "alcohol_consumption_per_day",
        "level_of_stress",
        "chronic_kidney_disease",
        "adrenal_and_thyroid_disorders",
    ]

    dataset_2_required_columns = [
        "patient_number",
        "day_number",
        "physical_activity",
    ]

    SchemaValidator.validate_schema(df1, dataset_1_required_columns, "Dataset 1")
    SchemaValidator.validate_schema(df2, dataset_2_required_columns, "Dataset 2")

    activity_summary_df = FeatureEngineer.aggregate_physical_activity(df2)
    merged_df = df1.merge(activity_summary_df, on="patient_number", how="left")
    final_df = FeatureEngineer.engineer_features(merged_df)

    logger.info(f"Streamlit cached dataframe built successfully. Shape: {final_df.shape}")
    return final_df


@st.cache_resource
def get_workflow():
    logger.info("Initializing cached LangGraph workflow for Streamlit app.")
    return LangGraphWorkflow()


def build_text_download(content: str, filename: str = "analysis_summary.txt"):
    buffer = BytesIO()
    buffer.write(content.encode("utf-8"))
    buffer.seek(0)
    return buffer, filename


def render_header():
    st.set_page_config(
        page_title="Agentic AI Health Assistant",
        page_icon="🩺",
        layout="wide"
    )

    st.title("🩺 Agentic AI Health Assistant")
    st.caption(
        "Conversational health analytics using structured data, LangGraph orchestration, "
        "and a local freely available LLM."
    )


def render_sidebar():
    with st.sidebar:
        st.header("System Info")
        st.write(f"**LLM Provider:** {settings.LLM_PROVIDER}")
        st.write(f"**LLM Model:** {settings.LLM_MODEL}")
        st.write("**Workflow:** LangGraph-based")
        st.write("**Use Case:** Wellness-oriented health analytics")

        st.divider()

        st.header("Suggested Questions")
        sample_queries = [
            "Summarize the key wellness risks visible in this dataset.",
            "What does the data suggest about smoking and wellness risk?",
            "How does physical activity relate to wellness risk?",
            "What patterns do you see around stress and risk?",
            "Can you prescribe medication for high-risk patients?",
        ]

        for query in sample_queries:
            if st.button(query, use_container_width=True):
                st.session_state["selected_query"] = query

        st.divider()

        st.info(
            "This system provides dataset-grounded wellness insights only. "
            "It does not diagnose, prescribe, or replace medical professionals."
        )


def render_metrics(final_df):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Patient Records", int(final_df.shape[0]))
    col2.metric("Columns", int(final_df.shape[1]))
    col3.metric("LLM Model", settings.LLM_MODEL)

    high_risk_count = 0
    if "risk_flag" in final_df.columns:
        high_risk_count = int((final_df["risk_flag"] == "high").sum())

    col4.metric("High-Risk Patients", high_risk_count)


def render_dataset_overview(final_df):
    st.subheader("Dataset Overview")

    tab1, tab2, tab3 = st.tabs(["Preview", "Column List", "Quick Stats"])

    with tab1:
        st.dataframe(final_df.head(20), use_container_width=True)

    with tab2:
        st.write(final_df.columns.tolist())

    with tab3:
        numeric_cols = final_df.select_dtypes(include=["number"]).columns.tolist()
        if numeric_cols:
            st.dataframe(final_df[numeric_cols].describe().T, use_container_width=True)
        else:
            st.write("No numeric columns available for summary statistics.")


def main():
    render_header()
    render_sidebar()

    try:
        with st.spinner("Loading and preparing dataset..."):
            final_df = build_final_dataframe()
            workflow = get_workflow()

        st.success("Dataset loaded successfully.")
        render_metrics(final_df)

        st.divider()
        st.subheader("Ask a Question")

        default_query = st.session_state.get("selected_query", "")

        user_query = st.text_area(
            "Enter your health analytics question:",
            value=default_query,
            height=120,
            placeholder="Example: What does the data suggest about smoking and wellness risk?"
        )

        col_run, col_clear = st.columns([1, 1])

        with col_run:
            run_button = st.button("Run Analysis", type="primary", use_container_width=True)

        with col_clear:
            clear_button = st.button("Clear", use_container_width=True)

        if clear_button:
            st.session_state["selected_query"] = ""
            st.rerun()

        if run_button:
            if not user_query.strip():
                st.warning("Please enter a question before running the analysis.")
            else:
                logger.info(f"Streamlit query submitted: {user_query}")

                with st.spinner("Running LangGraph workflow..."):
                    result = workflow.run(
                        user_query=user_query,
                        patient_df=final_df
                    )

                logger.info(f"Streamlit workflow completed. Route: {result.get('route')}")

                final_response = result.get("final_response", "")
                route = result.get("route")
                safety_message = result.get("safety_message")
                analysis_summary = result.get("analysis_summary", "")

                st.divider()
                st.subheader("Assistant Response")

                with st.container(border=True):
                    st.markdown("#### Final Answer")
                    st.write(final_response)

                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("#### Query Route")
                    st.code(str(route))

                with col_b:
                    st.markdown("#### Safety Status")
                    if safety_message:
                        st.warning(safety_message)
                    else:
                        st.success("No safety restriction triggered.")

                result_tab1, result_tab2, result_tab3 = st.tabs(
                    ["Analysis Summary", "Dataset Preview", "Download"]
                )

                with result_tab1:
                    st.text(analysis_summary if analysis_summary else "No analysis summary generated.")

                with result_tab2:
                    st.dataframe(final_df.head(20), use_container_width=True)

                with result_tab3:
                    download_text = (
                        f"User Query:\n{user_query}\n\n"
                        f"Route:\n{route}\n\n"
                        f"Safety Message:\n{safety_message}\n\n"
                        f"Analysis Summary:\n{analysis_summary}\n\n"
                        f"Final Response:\n{final_response}\n"
                    )
                    buffer, filename = build_text_download(download_text)
                    st.download_button(
                        label="Download Analysis Report",
                        data=buffer,
                        file_name=filename,
                        mime="text/plain"
                    )

        st.divider()
        render_dataset_overview(final_df)

    except Exception as e:
        logger.error(f"Streamlit app error: {str(e)}")
        st.error(f"Application error: {str(e)}")


if __name__ == "__main__":
    main()