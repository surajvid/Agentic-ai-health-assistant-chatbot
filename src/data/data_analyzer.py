import pandas as pd


class DataAnalyzer:
    """
    Analyzes processed patient-level data and produces structured summaries
    for downstream LLM explanation.
    """

    @staticmethod
    def get_basic_summary(df: pd.DataFrame) -> dict:
        return {
            "total_records": int(len(df)),
            "total_columns": int(len(df.columns)),
            "columns": df.columns.tolist(),
        }

    @staticmethod
    def get_risk_summary(df: pd.DataFrame) -> dict:
        result = {}

        if "risk_flag" in df.columns:
            risk_counts = df["risk_flag"].value_counts(dropna=False).to_dict()
            result["risk_flag_distribution"] = {
                str(k): int(v) for k, v in risk_counts.items()
            }

        if "risk_score" in df.columns:
            result["avg_risk_score"] = round(float(df["risk_score"].mean()), 2)
            result["max_risk_score"] = round(float(df["risk_score"].max()), 2)
            result["min_risk_score"] = round(float(df["risk_score"].min()), 2)

        return result

    @staticmethod
    def get_activity_summary(df: pd.DataFrame) -> dict:
        result = {}

        if "avg_physical_activity" in df.columns:
            result["avg_physical_activity_mean"] = round(float(df["avg_physical_activity"].mean()), 2)
            result["avg_physical_activity_min"] = round(float(df["avg_physical_activity"].min()), 2)
            result["avg_physical_activity_max"] = round(float(df["avg_physical_activity"].max()), 2)

        if "activity_level" in df.columns:
            activity_counts = df["activity_level"].value_counts(dropna=False).to_dict()
            result["activity_level_distribution"] = {
                str(k): int(v) for k, v in activity_counts.items()
            }

        return result

    @staticmethod
    def get_smoking_summary(df: pd.DataFrame) -> dict:
        result = {}

        if "smoking" in df.columns:
            smoking_counts = df["smoking"].value_counts(dropna=False).to_dict()
            result["smoking_distribution"] = {
                str(k): int(v) for k, v in smoking_counts.items()
            }

        if {"smoking", "risk_flag"}.issubset(df.columns):
            cross_tab = pd.crosstab(df["smoking"], df["risk_flag"]).to_dict()
            result["smoking_vs_risk"] = cross_tab

        return result

    @staticmethod
    def get_stress_summary(df: pd.DataFrame) -> dict:
        result = {}

        if "level_of_stress" in df.columns:
            result["stress_mean"] = round(float(df["level_of_stress"].mean()), 2)
            result["stress_min"] = round(float(df["level_of_stress"].min()), 2)
            result["stress_max"] = round(float(df["level_of_stress"].max()), 2)

        if {"level_of_stress", "risk_flag"}.issubset(df.columns):
            high_stress_high_risk = int(((df["level_of_stress"] >= 3) & (df["risk_flag"] == "high")).sum())
            result["high_stress_high_risk_count"] = high_stress_high_risk

        return result

    @staticmethod
    def get_health_indicator_summary(df: pd.DataFrame) -> dict:
        result = {}

        numeric_cols = [
            "age",
            "bmi",
            "level_of_hemoglobin",
            "genetic_pedigree_coefficient",
            "level_of_stress",
            "salt_content_in_the_diet",
            "alcohol_consumption_per_day",
        ]

        for col in numeric_cols:
            if col in df.columns:
                result[col] = {
                    "mean": round(float(df[col].mean()), 2),
                    "min": round(float(df[col].min()), 2),
                    "max": round(float(df[col].max()), 2),
                }

        return result

    @staticmethod
    def get_top_risk_patterns(df: pd.DataFrame) -> list[str]:
        patterns = []

        if "risk_flag" in df.columns:
            patterns.append(f"High risk patients: {int((df['risk_flag'] == 'high').sum())}")
            patterns.append(f"Moderate risk patients: {int((df['risk_flag'] == 'moderate').sum())}")
            patterns.append(f"Low risk patients: {int((df['risk_flag'] == 'low').sum())}")

        if {"smoking", "risk_flag"}.issubset(df.columns):
            patterns.append(
                f"Smokers in high risk group: {int(((df['smoking'] == 1) & (df['risk_flag'] == 'high')).sum())}"
            )

        if {"blood_pressure_abnormality", "risk_flag"}.issubset(df.columns):
            patterns.append(
                f"Patients with blood pressure abnormality in high risk group: "
                f"{int(((df['blood_pressure_abnormality'] == 1) & (df['risk_flag'] == 'high')).sum())}"
            )

        if {"bmi", "risk_flag"}.issubset(df.columns):
            patterns.append(
                f"Obese patients in high risk group: {int(((df['bmi'] >= 30) & (df['risk_flag'] == 'high')).sum())}"
            )

        if {"avg_physical_activity", "risk_flag"}.issubset(df.columns):
            patterns.append(
                f"Low activity patients in high risk group: "
                f"{int(((df['avg_physical_activity'] < 5000) & (df['risk_flag'] == 'high')).sum())}"
            )

        return patterns

    @staticmethod
    def build_general_summary(df: pd.DataFrame) -> str:
        basic_summary = DataAnalyzer.get_basic_summary(df)
        risk_summary = DataAnalyzer.get_risk_summary(df)
        activity_summary = DataAnalyzer.get_activity_summary(df)
        indicator_summary = DataAnalyzer.get_health_indicator_summary(df)
        top_patterns = DataAnalyzer.get_top_risk_patterns(df)

        return f"""
DATASET OVERVIEW
- Total patient records: {basic_summary['total_records']}
- Total columns: {basic_summary['total_columns']}

RISK SUMMARY
- {risk_summary}

ACTIVITY SUMMARY
- {activity_summary}

HEALTH INDICATOR SUMMARY
- {indicator_summary}

TOP RISK PATTERNS
- {" | ".join(top_patterns)}
""".strip()

    @staticmethod
    def build_route_summary(df: pd.DataFrame, route: str) -> str:
        if route == "smoking_analysis":
            smoking_summary = DataAnalyzer.get_smoking_summary(df)
            risk_summary = DataAnalyzer.get_risk_summary(df)
            return f"""
SMOKING ANALYSIS
- {smoking_summary}

RISK CONTEXT
- {risk_summary}
""".strip()

        if route == "activity_analysis":
            activity_summary = DataAnalyzer.get_activity_summary(df)
            risk_summary = DataAnalyzer.get_risk_summary(df)
            return f"""
ACTIVITY ANALYSIS
- {activity_summary}

RISK CONTEXT
- {risk_summary}
""".strip()

        if route == "stress_analysis":
            stress_summary = DataAnalyzer.get_stress_summary(df)
            risk_summary = DataAnalyzer.get_risk_summary(df)
            return f"""
STRESS ANALYSIS
- {stress_summary}

RISK CONTEXT
- {risk_summary}
""".strip()

        if route == "risk_analysis":
            return DataAnalyzer.build_general_summary(df)

        return DataAnalyzer.build_general_summary(df)