from data.data_loader import DataLoader
from data.preprocessing import DataPreprocessor
from data.schema_validator import SchemaValidator
from data.feature_engineering import FeatureEngineer


def test_data_loading():
    loader = DataLoader(data_dir="data")

    df1 = loader.load_file("Health Dataset 1.xlsm")
    df2 = loader.load_file("Health Dataset 2.xlsm")

    assert df1 is not None
    assert df2 is not None
    assert df1.shape[0] > 0
    assert df2.shape[0] > 0


def test_preprocessing():
    loader = DataLoader(data_dir="data")

    df1 = loader.load_file("Health Dataset 1.xlsm")
    df2 = loader.load_file("Health Dataset 2.xlsm")

    df1 = DataPreprocessor.preprocess(df1)
    df2 = DataPreprocessor.preprocess(df2)

    assert "patient_number" in df1.columns
    assert "patient_number" in df2.columns
    assert "age" in df1.columns
    assert "physical_activity" in df2.columns


def test_schema_validation():
    loader = DataLoader(data_dir="data")

    df1 = DataPreprocessor.preprocess(loader.load_file("Health Dataset 1.xlsm"))
    df2 = DataPreprocessor.preprocess(loader.load_file("Health Dataset 2.xlsm"))

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


def test_feature_engineering():
    loader = DataLoader(data_dir="data")

    df1 = DataPreprocessor.preprocess(loader.load_file("Health Dataset 1.xlsm"))
    df2 = DataPreprocessor.preprocess(loader.load_file("Health Dataset 2.xlsm"))

    activity_summary_df = FeatureEngineer.aggregate_physical_activity(df2)
    merged_df = df1.merge(activity_summary_df, on="patient_number", how="left")
    final_df = FeatureEngineer.engineer_features(merged_df)

    assert "avg_physical_activity" in final_df.columns
    assert "bmi_category" in final_df.columns
    assert "age_group" in final_df.columns
    assert "risk_flag" in final_df.columns