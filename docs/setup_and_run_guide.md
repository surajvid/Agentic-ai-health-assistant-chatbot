
---
# Setup and Run Guide

## 1. Clone the repository

```bash
git clone <your_repo_url>
cd agentic-ai-health-assistant

## 2. Create and activate virtual environment

python3 -m venv .venv
source .venv/bin/activate

## 3. Install Python dependencies

pip install -r requirements.txt

## 4. Install and run Ollama

ollama pull phi3
ollama serve

## 5. Configure .env
Create a .env file in the project root:

LLM_PROVIDER=ollama
LLM_MODEL=phi3
OLLAMA_BASE_URL=http://localhost:11434
DATABASE_URL=postgresql://user:password@localhost:5432/health_db

## 6. Add dataset files

Place these files under the data/ directory:

Health Dataset 1.xlsm

Health Dataset 2.xlsm

## 7. Run the application

Main runner

python -m src.main

Streamlit UI

PYTHONPATH=. streamlit run src/app/streamlit_app.py

Evaluation

python -m src.evaluation.run_evaluation

## 8. Common issues

Import errors

Always run module-based commands from the project root.

Ollama connection failure

Ensure:
ollama serve is running in the background.

Streamlit import issue

Use:
PYTHONPATH=. streamlit run src/app/streamlit_app.py

Excel loading issue

Make sure openpyxl is installed and the loader uses sheet_name=0.
