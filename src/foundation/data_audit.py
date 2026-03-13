import pandas as pd


class DataAuditor:
    """
    Performs data audit checks on structured datasets before preprocessing.
    """

    @staticmethod
    def get_shape(df: pd.DataFrame) -> dict:
        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
        }

    @staticmethod
    def get_columns(df: pd.DataFrame) -> list[str]:
        return df.columns.tolist()

    @staticmethod
    def get_dtypes(df: pd.DataFrame) -> dict:
        return {col: str(dtype) for col, dtype in df.dtypes.items()}

    @staticmethod
    def get_missing_summary(df: pd.DataFrame) -> dict:
        missing_counts = df.isnull().sum()
        missing_pct = (df.isnull().mean() * 100).round(2)

        result = {}
        for col in df.columns:
            result[col] = {
                "missing_count": int(missing_counts[col]),
                "missing_pct": float(missing_pct[col]),
            }
        return result

    @staticmethod
    def get_duplicate_summary(df: pd.DataFrame) -> dict:
        duplicate_rows = int(df.duplicated().sum())
        return {
            "duplicate_rows": duplicate_rows,
            "duplicate_pct": round((duplicate_rows / len(df)) * 100, 2) if len(df) > 0 else 0.0,
        }

    @staticmethod
    def get_numeric_summary(df: pd.DataFrame) -> dict:
        numeric_df = df.select_dtypes(include=["number"])

        if numeric_df.empty:
            return {}

        summary = {}
        for col in numeric_df.columns:
            summary[col] = {
                "mean": round(float(numeric_df[col].mean()), 2) if numeric_df[col].notna().any() else None,
                "min": round(float(numeric_df[col].min()), 2) if numeric_df[col].notna().any() else None,
                "max": round(float(numeric_df[col].max()), 2) if numeric_df[col].notna().any() else None,
                "median": round(float(numeric_df[col].median()), 2) if numeric_df[col].notna().any() else None,
            }
        return summary

    @staticmethod
    def get_categorical_summary(df: pd.DataFrame, top_n: int = 5) -> dict:
        categorical_df = df.select_dtypes(include=["object", "category", "bool"])

        if categorical_df.empty:
            return {}

        summary = {}
        for col in categorical_df.columns:
            top_values = categorical_df[col].value_counts(dropna=False).head(top_n).to_dict()
            summary[col] = {str(k): int(v) for k, v in top_values.items()}
        return summary

    @staticmethod
    def check_column_uniqueness(df: pd.DataFrame, column_name: str) -> dict:
        if column_name not in df.columns:
            return {
                "column_exists": False,
                "unique_values": None,
                "total_rows": int(len(df)),
                "is_unique_key": False,
            }

        unique_values = int(df[column_name].nunique(dropna=False))
        total_rows = int(len(df))

        return {
            "column_exists": True,
            "unique_values": unique_values,
            "total_rows": total_rows,
            "is_unique_key": unique_values == total_rows,
        }

    @staticmethod
    def get_grain_summary(df: pd.DataFrame, key_columns: list[str]) -> dict:
        missing_keys = [col for col in key_columns if col not in df.columns]

        if missing_keys:
            return {
                "valid": False,
                "missing_keys": missing_keys,
                "unique_combinations": None,
                "total_rows": int(len(df)),
            }

        unique_combinations = int(df[key_columns].drop_duplicates().shape[0])

        return {
            "valid": True,
            "missing_keys": [],
            "unique_combinations": unique_combinations,
            "total_rows": int(len(df)),
            "is_grain_unique": unique_combinations == len(df),
        }

    @staticmethod
    def audit_dataset(
        df: pd.DataFrame,
        dataset_name: str,
        primary_key: str | None = None,
        grain_keys: list[str] | None = None
    ) -> dict:
        report = {
            "dataset_name": dataset_name,
            "shape": DataAuditor.get_shape(df),
            "columns": DataAuditor.get_columns(df),
            "dtypes": DataAuditor.get_dtypes(df),
            "missing_summary": DataAuditor.get_missing_summary(df),
            "duplicate_summary": DataAuditor.get_duplicate_summary(df),
            "numeric_summary": DataAuditor.get_numeric_summary(df),
            "categorical_summary": DataAuditor.get_categorical_summary(df),
        }

        if primary_key:
            report["primary_key_check"] = DataAuditor.check_column_uniqueness(df, primary_key)

        if grain_keys:
            report["grain_summary"] = DataAuditor.get_grain_summary(df, grain_keys)

        return report

    @staticmethod
    def compare_dataset_keys(df1: pd.DataFrame, df2: pd.DataFrame, key: str) -> dict:
        if key not in df1.columns or key not in df2.columns:
            return {
                "key_exists_in_both": False,
                "common_keys": None,
                "only_in_dataset_1": None,
                "only_in_dataset_2": None,
            }

        keys_1 = set(df1[key].dropna().unique())
        keys_2 = set(df2[key].dropna().unique())

        common_keys = len(keys_1.intersection(keys_2))
        only_in_dataset_1 = len(keys_1 - keys_2)
        only_in_dataset_2 = len(keys_2 - keys_1)

        return {
            "key_exists_in_both": True,
            "common_keys": common_keys,
            "only_in_dataset_1": only_in_dataset_1,
            "only_in_dataset_2": only_in_dataset_2,
        }

    @staticmethod
    def build_audit_text_report(dataset_1_audit: dict, dataset_2_audit: dict, key_comparison: dict) -> str:
        return f"""
MODULE 1 — DATA AUDIT REPORT

DATASET 1: {dataset_1_audit['dataset_name']}
- Shape: {dataset_1_audit['shape']['rows']} rows x {dataset_1_audit['shape']['columns']} columns
- Duplicate rows: {dataset_1_audit['duplicate_summary']['duplicate_rows']}
- Primary key check: {dataset_1_audit.get('primary_key_check', {})}
- Grain summary: {dataset_1_audit.get('grain_summary', {})}

DATASET 2: {dataset_2_audit['dataset_name']}
- Shape: {dataset_2_audit['shape']['rows']} rows x {dataset_2_audit['shape']['columns']} columns
- Duplicate rows: {dataset_2_audit['duplicate_summary']['duplicate_rows']}
- Primary key check: {dataset_2_audit.get('primary_key_check', {})}
- Grain summary: {dataset_2_audit.get('grain_summary', {})}

KEY COMPARISON
- {key_comparison}

INITIAL OBSERVATIONS
- Dataset 1 appears to be at patient level.
- Dataset 2 appears to be at patient-day level.
- A direct raw merge may create row explosion unless Dataset 2 is aggregated first.
- Key coverage should be checked before integration.
""".strip()