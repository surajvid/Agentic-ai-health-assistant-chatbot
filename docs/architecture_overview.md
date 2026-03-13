
# Architecture Overview

## End-to-End Flow

```text
User Query
   ↓
Query Taxonomy
   ↓
Policy Layer
   ↓
LangGraph Workflow
      ├── Route Query Node
      ├── Safety Check Node
      ├── Build Analysis Node
      └── Generate Response Node
   ↓
Local LLM (Ollama)
   ↓
Final Answer

###Data Flow

Health Dataset 1 (.xlsm)      Health Dataset 2 (.xlsm)
        ↓                             ↓
   Data Audit                    Data Audit
        ↓                             ↓
   Preprocessing                Preprocessing
        ↓                             ↓
                              Activity Aggregation
                                      ↓
                        Patient-Level Integration Layer
                                      ↓
                           Feature Engineering
                                      ↓
                           Analytical DataFrame
                                      ↓
                              Analytics Tools
                                      ↓
                            Structured Summary
                                      ↓
                                 Prompt Layer
                                      ↓
                                 Local LLM


                                 
                                 
# Architectural Principles

1. Separation of concerns

Each layer handles a specific responsibility.

2. Tool-first reasoning

Deterministic analytics precede language generation.

3. Safety-first design

Unsafe medical or privacy-sensitive questions are blocked before LLM invocation.

4. Route-aware processing

Different query categories trigger different analysis pathways.

5. Local execution

The LLM runs via Ollama to satisfy the freely available model requirement.

# Why LangGraph?

LangGraph was used because it provides:

- explicit workflow structure
- stateful multi-step orchestration
- conditional branching
- easier debugging and explainability than an opaque monolithic chain