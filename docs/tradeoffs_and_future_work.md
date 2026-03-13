# Trade-offs and Future Work

## Key Trade-offs

### 1. Rule-based safety instead of model-based safety
The policy layer uses explicit rules for simplicity, transparency, and predictability.

**Trade-off:**  
Easy to understand and debug, but less flexible than classifier-based moderation.

### 2. Local LLM via Ollama instead of hosted API
A local LLM was chosen to satisfy the requirement of using a freely available LLM.

**Trade-off:**  
No API cost and better privacy, but output quality may be lower than frontier hosted models.

### 3. Structured summaries before LLM
The system passes structured analysis summaries to the LLM rather than raw tabular data.

**Trade-off:**  
Better grounding and safety, but less flexible for very open-ended exploratory questions.

### 4. Lightweight logging instead of enterprise tracing
The monitoring approach uses standard logging and runtime metrics.

**Trade-off:**  
Simple and portable, but less feature-rich than LangSmith or enterprise observability tools.

## Future Work

- classifier-based policy and moderation layer
- richer prompt templates by query subtype
- UI with chat history and saved sessions
- API packaging and containerization
- enhanced evaluation with answer quality rubric
- benchmark multiple local LLMs
- stronger deployment monitoring
- optional predictive modeling extensions