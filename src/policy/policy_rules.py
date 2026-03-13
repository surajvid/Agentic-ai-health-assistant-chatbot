DISALLOWED_MEDICAL_TERMS = [
    "diagnose",
    "diagnosis",
    "prescribe",
    "prescription",
    "medicine",
    "medication",
    "drug",
    "drugs",
    "treatment plan",
    "cure",
    "heal me",
    "which patient is sick",
    "what disease",
    "which disease",
]

HIGH_RISK_ADVICE_TERMS = [
    "should i take",
    "what should i take",
    "what medicine should",
    "which medicine",
    "medical advice",
    "clinical advice",
    "doctor recommendation",
]

PRIVACY_SENSITIVE_TERMS = [
    "patient name",
    "full identity",
    "personal identity",
    "who is this patient",
    "identify this patient",
]

ALLOWED_ANALYTICS_CATEGORIES = [
    "general_summary",
    "risk_analysis",
    "smoking_analysis",
    "activity_analysis",
    "stress_analysis",
]

DEFAULT_DISCLAIMER = (
    "This system provides dataset-grounded wellness insights only. "
    "It does not diagnose diseases, prescribe medications, or replace licensed medical professionals."
)

BLOCKED_RESPONSE = (
    "I can only provide general wellness-oriented insights based on the dataset. "
    "I cannot diagnose conditions, prescribe medication, identify individuals, or provide clinical treatment advice. "
    "Please consult a licensed medical professional for medical decisions."
)