from data.data_loader import DataLoader
from data.preprocessing import DataPreprocessor
from data.feature_engineering import FeatureEngineer
from data.data_analyzer import DataAnalyzer


def build_final_df():
    loader = DataLoader(data_dir="data")

    df1 = DataPreprocessor.preprocess(loader.load_file("Health Dataset 1.xlsm"))
    df2 = DataPreprocessor.preprocess(loader.load_file("Health Dataset 2.xlsm"))

    activity_summary_df = FeatureEngineer.aggregate_physical_activity(df2)
    merged_df = df1.merge(activity_summary_df, on="patient_number", how="left")
    final_df = FeatureEngineer.engineer_features(merged_df)

    return final_df


def test_basic_summary():
    final_df = build_final_df()

    summary = DataAnalyzer.get_basic_summary(final_df)

    assert isinstance(summary, dict)
    assert summary["total_records"] > 0
    assert summary["total_columns"] > 0


def test_risk_summary():
    final_df = build_final_df()

    summary = DataAnalyzer.get_risk_summary(final_df)

    assert isinstance(summary, dict)
    assert "risk_flag_distribution" in summary or "avg_risk_score" in summary


def test_activity_summary():
    final_df = build_final_df()

    summary = DataAnalyzer.get_activity_summary(final_df)

    assert isinstance(summary, dict)
    assert "avg_physical_activity_mean" in summary or "activity_level_distribution" in summary


def test_build_general_summary():
    final_df = build_final_df()

    summary_text = DataAnalyzer.build_general_summary(final_df)

    assert isinstance(summary_text, str)
    assert "DATASET OVERVIEW" in summary_text
    assert "RISK SUMMARY" in summary_text