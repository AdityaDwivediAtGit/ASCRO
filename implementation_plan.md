# Goal Description

Develop the Agentic Supply Chain Resilience Orchestrator (ASCRO) from scratch. This is an end-to-end multi-agent prototype for the TCS & AMD AI Hackathon Track 1. The system uses LangGraph to orchestrate multiple specialized agents (Supervisor, Researcher, Predictor, Executor, Critic) that collaborate to assess and mitigate supply chain disruptions. The solution is heavily optimized for AMD MI300X/ROCm utilizing vLLM for inference, sentence-transformers for RAG, and XGBoost for predictive analysis. The frontend will be a robust Gradio application showcasing a trace dashboard, metrics, and chat interface.

## User Review Required

> [!WARNING]
> **Environment & Hardware Assumptions**
> The target environment for the hackathon is Linux with ROCm 7.2 (e.g., notebooks.amd.com). However, the current workspace is a Windows machine. The application will be written to explicitly use `vllm` and other AMD-optimized libraries, but testing these natively on Windows may cause import errors or require fallback implementations (like standard `transformers` or a mock LLM) during local development.
> I will implement a graceful fallback to standard `transformers` or a dummy LLM locally if `vllm` fails to load, so that the UI and agent logic can be tested on Windows without crashing. Is this approach acceptable?

> [!IMPORTANT]
> **Open Source Models**
> I will default the code to use `Qwen/Qwen2.5-7B-Instruct-AWQ` or `meta-llama/Meta-Llama-3-8B-Instruct` as the local vLLM target. Please ensure you have the Hugging Face token setup or the models downloaded in your hackathon environment.

## Open Questions

1. Do you have a specific Hugging Face Hub token to use for model downloads in this environment, or should I write the code to assume public models?
2. For the RAG documents and tabular data, I plan to write Python scripts that automatically generate realistic synthetic CSVs and PDFs in the `data/` folder upon first run. Does that sound good?

## Proposed Changes

---

### Project Structure & Setup

Create the foundational files and dependencies.

#### [NEW] [requirements.txt](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/requirements.txt)
Will contain all required packages: `langgraph`, `langchain`, `llama-index`, `vllm`, `gradio`, `xgboost`, `pandas`, `scikit-learn`, `faiss-cpu`, `sentence-transformers`, `optimum-amd`, etc.

#### [NEW] [main.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/main.py)
Entry point of the application launching the Gradio interface, handling interactions with the LangGraph state.

---

### Core Architecture (LangGraph & Agents)

Implement the multi-agent graph and agent specific behaviors.

#### [NEW] [graph.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/graph.py)
Defines the `StateGraph`, the nodes (agents), and the conditional edges (Critic loop).

#### [NEW] [agents/__init__.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/agents/__init__.py)
#### [NEW] [agents/supervisor.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/agents/supervisor.py)
Breaks down the query and plans the execution flow.
#### [NEW] [agents/researcher.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/agents/researcher.py)
Connects to the RAG retriever to fetch context.
#### [NEW] [agents/predictor.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/agents/predictor.py)
Invokes the XGBoost model to get disruption probabilities and risk scores.
#### [NEW] [agents/executor.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/agents/executor.py)
Drafts the mitigation plan using research and predictions.
#### [NEW] [agents/critic.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/agents/critic.py)
Reviews the executor's output against the user's constraints and either approves or sends it back for revision.

---

### RAG & ML Capabilities

#### [NEW] [rag/indexer.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/rag/indexer.py)
Reads PDFs/txts from `data/`, chunks them, and builds a FAISS vector store.
#### [NEW] [rag/retriever.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/rag/retriever.py)
Loads the index and provides a retrieval tool for the Researcher.
#### [NEW] [predictor/model.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/predictor/model.py)
XGBoost implementation. Includes training logic on synthetic tabular data.
#### [NEW] [predictor/data_loader.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/predictor/data_loader.py)
Generates or loads tabular supply chain datasets.

---

### Tools & Utils

#### [NEW] [tools/__init__.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/tools/__init__.py)
#### [NEW] [tools/repl.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/tools/repl.py)
Provides a restricted Python REPL for math/calculations.
#### [NEW] [utils/metrics.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/utils/metrics.py)
Tracks latency, token usage, and simulated GPU stats (or real `rocm-smi` if available).
#### [NEW] [utils/report.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/utils/report.py)
Formats the agent trace and final output into a polished markdown/PDF document.
#### [NEW] [utils/llm_provider.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/utils/llm_provider.py)
A wrapper to initialize `vllm` locally and provide an interface compatible with LangChain.

---

### Evaluation & Documentation

#### [NEW] [eval/evaluate.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/eval/evaluate.py)
Runs batch queries and calculates F1 score for prediction, latency, and simulated RAG recall.
#### [NEW] [README.md](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/README.md)
Hackathon specific README with architecture diagrams (Mermaid), installation instructions, and AMD Mi300X specific notes.
#### [NEW] [data/generate_synthetic_data.py](file:///c:/Users/dwive/OneDrive/Documents/Git%20Cloned/ASCRO/data/generate_synthetic_data.py)
Script to populate mock data so the app runs out-of-the-box.

## Verification Plan

### Automated Tests
- The app will automatically run `data/generate_synthetic_data.py` on startup if data is missing.
- `python eval/evaluate.py` will be executed to generate the baseline metrics.

### Manual Verification
- Launch the Gradio UI using `python main.py`.
- Interact with the Chat UI to trigger a risk assessment (e.g., "Assess semiconductor shortage risk for Q3 auto client").
- Verify that the Trace tab correctly visualizes the LangGraph flow: Supervisor -> Researcher -> Predictor -> Executor -> Critic.
- Check the Metrics tab to confirm latency and token counts are being recorded.
