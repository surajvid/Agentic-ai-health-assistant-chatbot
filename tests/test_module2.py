from data.data_loader import DataLoader
from data.preprocessing import DataPreprocessor
from data.schema_validator import SchemaValidator
from data.feature_engineering import FeatureEngineer


def main():
    loader = DataLoader(data_dir="data")

    df1 = loader.load_file("Health Dataset 1.xlsm")
    df2 = loader.load_file("Health Dataset 2.xlsm")

    print("Raw Dataset 1 Shape:", df1.shape)
    print("Raw Dataset 2 Shape:", df2.shape)

    df1 = DataPreprocessor.preprocess(df1)
    df2 = DataPreprocessor.preprocess(df2)

    print("Cleaned Dataset 1 Shape:", df1.shape)
    print("Cleaned Dataset 2 Shape:", df2.shape)

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

    print("Schema validation passed.")

    activity_summary_df = FeatureEngineer.aggregate_physical_activity(df2)
    print("Activity Summary Shape:", activity_summary_df.shape)

    merged_df = df1.merge(activity_summary_df, on="patient_number", how="left")
    print("Merged Dataset Shape:", merged_df.shape)

    final_df = FeatureEngineer.engineer_features(merged_df)
    print("Final Dataset Shape:", final_df.shape)

    print("\nFinal Columns:")
    print(final_df.columns.tolist())

    print("\nSample Rows:")
    print(final_df.head())


if __name__ == "__main__":
    main()