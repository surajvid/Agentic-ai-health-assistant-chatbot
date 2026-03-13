import pandas as pd
import numpy as np


class FeatureEngineer:
    """
    Creates useful derived features from cleaned data.
    """

    @staticmethod
    def aggregate_physical_activity(activity_df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate daily physical activity to patient level.
        """
        grouped_df = (
            activity_df.groupby("patient_number", as_index=False)
            .agg(
                avg_physical_activity=("physical_activity", "mean"),
                min_physical_activity=("physical_activity", "min"),
                max_physical_activity=("physical_activity", "max"),
                activity_std_dev=("physical_activity", "std"),
                activity_days=("day_number", "nunique"),
            )
        )

        grouped_df["activity_std_dev"] = grouped_df["activity_std_dev"].fillna(0)

        return grouped_df

    @staticmethod
    def add_bmi_category(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "bmi" not in df.columns:
            return df

        conditions = [
            df["bmi"] < 18.5,
            (df["bmi"] >= 18.5) & (df["bmi"] < 25),
            (df["bmi"] >= 25) & (df["bmi"] < 30),
            df["bmi"] >= 30,
        ]
        categories = ["underweight", "normal", "overweight", "obese"]

        df["bmi_category"] = np.select(conditions, categories, default="unknown")
        return df

    @staticmethod
    def add_age_group(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "age" not in df.columns:
            return df

        conditions = [
            df["age"] < 18,
            (df["age"] >= 18) & (df["age"] < 35),
            (df["age"] >= 35) & (df["age"] < 50),
            df["age"] >= 50,
        ]
        groups = ["minor", "young_adult", "mid_age", "senior"]

        df["age_group"] = np.select(conditions, groups, default="unknown")
        return df

    @staticmethod
    def add_activity_level(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        if "avg_physical_activity" not in df.columns:
            return df

        conditions = [
            df["avg_physical_activity"] < 5000,
            (df["avg_physical_activity"] >= 5000) & (df["avg_physical_activity"] < 10000),
            df["avg_physical_activity"] >= 10000,
        ]
        labels = ["low_activity", "moderate_activity", "high_activity"]

        df["activity_level"] = np.select(conditions, labels, default="unknown")
        return df

    @staticmethod
    def add_risk_flag(df: pd.DataFrame) -> pd.DataFrame:
        """
        Create a simple non-clinical wellness risk flag.
        """
        df = df.copy()

        conditions = []

        if {"blood_pressure_abnormality", "bmi", "smoking", "chronic_kidney_disease", "level_of_stress"}.issubset(df.columns):
            risk_score = (
                (df["blood_pressure_abnormality"] == 1).astype(int)
                + (df["bmi"] >= 30).astype(int)
                + (df["smoking"] == 1).astype(int)
                + (df["chronic_kidney_disease"] == 1).astype(int)
                + (df["level_of_stress"] >= 3).astype(int)
            )

            if "avg_physical_activity" in df.columns:
                risk_score += (df["avg_physical_activity"] < 5000).astype(int)

            df["risk_score"] = risk_score

            df["risk_flag"] = np.where(
                df["risk_score"] >= 3,
                "high",
                np.where(df["risk_score"] == 2, "moderate", "low")
            )

        return df

    @staticmethod
    def engineer_features(patient_df: pd.DataFrame) -> pd.DataFrame:
        df = patient_df.copy()
        df = FeatureEngineer.add_bmi_category(df)
        df = FeatureEngineer.add_age_group(df)
        df = FeatureEngineer.add_activity_level(df)
        df = FeatureEngineer.add_risk_flag(df)
        return df