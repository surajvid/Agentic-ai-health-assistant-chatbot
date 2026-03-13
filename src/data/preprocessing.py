import pandas as pd


class DataPreprocessor:
    """
    Handles cleaning and preprocessing of raw datasets.
    """

    @staticmethod
    def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [
            col.strip().lower().replace(" ", "_")
            for col in df.columns
        ]
        return df

    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        return df.drop_duplicates()

    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        numeric_cols = df.select_dtypes(include=["number"]).columns
        categorical_cols = df.select_dtypes(include=["object"]).columns

        for col in numeric_cols:
            df[col] = df[col].fillna(df[col].median())

        for col in categorical_cols:
            df[col] = df[col].fillna("unknown")

        return df

    @staticmethod
    def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        possible_numeric_cols = [
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
            "day_number",
            "physical_activity",
        ]

        for col in possible_numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    @staticmethod
    def preprocess(df: pd.DataFrame) -> pd.DataFrame:
        df = DataPreprocessor.standardize_column_names(df)
        df = DataPreprocessor.convert_numeric_columns(df)
        df = DataPreprocessor.remove_duplicates(df)
        df = DataPreprocessor.handle_missing_values(df)
        return df