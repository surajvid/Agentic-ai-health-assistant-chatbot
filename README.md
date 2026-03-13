# Agentic AI Health Assistant

A modular conversational AI system for analyzing structured health datasets using deterministic analytics, a policy-aware LangGraph workflow, and a freely available local LLM.

## 1. Overview

This project was built as a conversational analytics system for structured healthcare-related datasets. It allows a user to ask natural-language questions such as:

- What are the key wellness risks visible in the dataset?
- How does smoking relate to wellness risk?
- How does physical activity relate to patient risk?
- What patterns exist around stress and wellness outcomes?

The system does not rely on raw LLM reasoning over spreadsheets. Instead, it uses a layered architecture:

- structured data loading
- preprocessing and validation
- feature engineering
- analytical tools
- policy checks
- LangGraph-based orchestration
- route-aware prompting
- local LLM explanation
- Streamlit UI
- evaluation and monitoring

This improves grounding, safety, and explainability.

---

## 2. Problem Statement

Healthcare datasets often contain structured indicators such as age, BMI, smoking status, stress, and activity levels. Extracting insights from these datasets usually requires technical data analysis skills.

The goal of this project is to build a conversational AI system that can:
- answer natural-language analytical questions over structured health data
- generate grounded and concise insights
- avoid hallucinated claims
- block unsafe healthcare responses such as diagnosis or treatment recommendations

---

## 3. Datasets

### Dataset 1 — Patient Health Profile
Patient-level dataset containing:
- age
- BMI
- smoking
- stress
- blood pressure abnormality
- alcohol consumption
- kidney disease
- thyroid/adrenal disorders
- and other health indicators

### Dataset 2 — Daily Physical Activity
Patient-day level dataset containing:
- patient number
- day number
- physical activity

### Key integration insight
Dataset 1 is at **patient level**.  
Dataset 2 is at **patient-day level**.

Therefore, Dataset 2 must be aggregated to patient level before merging to avoid row explosion.

---

## 4. Architecture Summary

The system uses a layered architecture:

```text
Input Excel Files (.xlsm)
    ↓
Module 1: Data Audit
    ↓
Module 2: Preprocessing
    ↓
Module 3: Feature Engineering
    ↓
Module 4: Integration Layer
    ↓
Module 5: Query Taxonomy
    ↓
Module 6: Analytics Tools
    ↓
Module 7: Policy Layer
    ↓
Module 8: LangGraph Workflow
    ↓
Module 9: Prompting
    ↓
Local LLM via Ollama
    ↓
Module 10: Streamlit App
    ↓
Module 11: Evaluation
    ↓
Module 12: Logging & Monitoring

### 5.Module Breakdown

Phase 1 — Foundation

-Module 0: Problem framing
- Module 1: Data audit
- Module 2: Preprocessing
- Module 3: Feature engineering
- Module 4: Integration layer

Phase 2 — Analytical Brain

- Module 5: Query taxonomy
- Module 6: Analytics tools
- Module 7: Policy layer
- Module 8: LangGraph workflow
- Module 9: Prompting

Phase 3 — Productization

- Module 10: Streamlit app
- Module 11: Evaluation
- Module 12: Lightweight logging and monitoring
- Module 13: Fine-tuning plan
- Module 14: Deployment design
- Module 15: Documentation

6. Key Design Decisions

6.1 Tool-first analytics

The LLM does not directly inspect raw datasets. Instead, deterministic Python analytics tools generate structured summaries first.

6.2 Grounded responses

Only structured summaries are passed to the LLM, reducing hallucination risk.

6.3 Policy-aware design

Unsafe requests related to diagnosis, medication, treatment, or patient identification are blocked before response generation.

6.4 Route-aware reasoning

Different query types are routed into specialized analysis paths such as:

- smoking analysis
- activity analysis
- stress analysis
- general risk analysis

6.5 Freely available LLM

The project uses a local model via Ollama to satisfy the requirement for a freely available LLM.

7. Tech Stack

- Python
- Pandas
- NumPy
- OpenPyXL
- Ollama
- LangGraph
- Streamlit
- Pytest
- Logging module

9. Setup Instructions

9.1 Create virtual environment

python3 -m venv .venv
source .venv/bin/activate

9.2 Install dependencies

pip install -r requirements.txt

9.3 Ensure Ollama is installed

Install Ollama and pull a model such as phi3.

ollama pull phi3
ollama serve

9.4 Configure environment

###Example .env:

LLM_PROVIDER=ollama
LLM_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
DATABASE_URL=postgresql://user:password@localhost:5432/health_db

9.5 Place datasets
Put the following files under the data/ folder:

Health Dataset 1.xlsm
Health Dataset 2.xlsm

10. How to Run

- Run the main application

python -m src.main

- Run Streamlit UI

PYTHONPATH=. streamlit run src/app/streamlit_app.py

- Run data audit

python -m src.foundation.run_data_audit

- Run policy checks

python -m src.policy.run_policy_check

- Run evaluation

python -m src.evaluation.run_evaluation

- Read logs

python -m src.monitoring.read_logs

11. Example Questions

- Summarize the key wellness risks visible in this dataset.
- What does the data suggest about smoking and wellness risk?
- How does physical activity relate to wellness risk?
- What patterns do you see around stress and risk?
- Can you prescribe medication for high-risk patients?

12. Safety and Ethical Boundaries

This system:
- does not diagnose diseases
- does not prescribe medication
- does not generate treatment plans
- does not identify individual patients
- provides wellness-oriented, population-level insights only
- Unsafe queries are intercepted by the policy layer before LLM generation.

13. Evaluation Summary

The solution includes an evaluation module that checks:

- route accuracy
- safety policy activation
- analysis summary generation
- response presence

This helps ensure the conversational workflow behaves consistently across different query types.

14. Logging and Monitoring

A lightweight observability layer captures:

- incoming query
- selected route
- safety trigger activation
- execution duration
- success/failure
- error context

Logs are written to:

logs/app.log

15. Trade-offs

### Why tools before LLM?

Using Python analytics tools first improves grounding and reduces hallucinations.

### Why local LLM instead of paid API?

- The assessment requires use of a freely available LLM, so a local model via Ollama was used.

#### Why not direct spreadsheet Q&A with the LLM?

Directly prompting the LLM with raw data is less reliable, less explainable, and weaker from a safety standpoint.

16. Limitations

- The project provides analytical insights, not clinical decision support
- The policy layer is rule-based, not classifier-based
- The evaluation framework is functional but lightweight
- The local LLM may vary in answer quality depending on model size and hardware
- The current system focuses on structured tabular analytics only

17. Future Improvements

- stronger policy engine with classifier-based moderation
- richer route-specific prompting
- better UI with chat history
- model benchmarking across multiple local LLMs
- LangSmith or OpenTelemetry-based monitoring
- API deployment and containerized packaging
- human evaluation rubric for response quality

18. Conclusion

This project demonstrates how to build a modular, safe, and grounded conversational analytics system over structured healthcare datasets using Python analytics, LangGraph orchestration, and a freely available local LLM.

It was designed not just to answer questions, but to show clear engineering thinking around:

- data quality
- safety
- modularity
- explainability
- productization
