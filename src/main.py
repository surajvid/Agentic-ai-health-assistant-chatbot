from src.config.settings import settings
from src.data.data_loader import DataLoader
from src.data.preprocessing import DataPreprocessor
from src.data.feature_engineering import FeatureEngineer
from src.data.schema_validator import SchemaValidator
from src.agents.langgraph_workflow import LangGraphWorkflow
from src.monitoring.logger import setup_logger


logger = setup_logger("main_app")


def main():
    logger.info("Application startup initiated.")
    print("Agentic AI System Starting...")
    print("Provider:", settings.LLM_PROVIDER)
    print("Model:", settings.LLM_MODEL)

    loader = DataLoader(data_dir="data")

    df1 = loader.load_file("Health Dataset 1.xlsm")
    df2 = loader.load_file("Health Dataset 2.xlsm")

    logger.info(f"Raw Dataset 1 Shape: {df1.shape}")
    logger.info(f"Raw Dataset 2 Shape: {df2.shape}")

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

    logger.info(f"Final analytical dataframe shape: {final_df.shape}")

    workflow = LangGraphWorkflow()

    user_query = "What does the data suggest about smoking and wellness risk?"
    result = workflow.run(user_query=user_query, patient_df=final_df)

    print("\nQuery Route:")
    print(result["route"])

    print("\nSafety Message:")
    print(result["safety_message"])

    print("\nAnalysis Summary:")
    print(result["analysis_summary"])

    print("\nFinal Response:")
    print(result["final_response"])

    logger.info("Application run completed successfully.")


if __name__ == "__main__":
    main()