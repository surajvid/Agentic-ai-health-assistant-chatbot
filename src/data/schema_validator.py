import pandas as pd


class SchemaValidator:
    """
    Validates dataset schema before preprocessing and feature engineering.
    """

    @staticmethod
    def validate_required_columns(
        df: pd.DataFrame,
        required_columns: list[str],
        dataset_name: str = "dataset"
    ) -> None:
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            raise ValueError(
                f"Missing required columns in {dataset_name}: {missing_columns}. "
                f"Available columns: {df.columns.tolist()}"
            )

    @staticmethod
    def validate_non_empty(df: pd.DataFrame, dataset_name: str = "dataset") -> None:
        if df.empty:
            raise ValueError(f"{dataset_name} is empty.")

    @staticmethod
    def validate_schema(
        df: pd.DataFrame,
        required_columns: list[str],
        dataset_name: str = "dataset"
    ) -> None:
        SchemaValidator.validate_non_empty(df, dataset_name)

        if required_columns:
            SchemaValidator.validate_required_columns(df, required_columns, dataset_name)