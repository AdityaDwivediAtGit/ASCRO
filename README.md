# ASCRO: Agentic Supply Chain Resilience Orchestrator 🏭

> **TCS & AMD AI Hackathon - Track 1 (Agents) Winner Candidate**

ASCRO is an end-to-end multi-agent orchestration system designed to proactively detect, analyze, and mitigate supply chain disruptions. Built on **LangGraph**, it coordinates a team of specialized agents (Supervisor, Researcher, Predictor, Executor, Critic) to provide real-time risk assessment.

## 🚀 Key Innovation: AMD & ROCm Optimization
ASCRO is architected from the ground up for high-performance inference on **AMD MI300X** accelerators:
- **vLLM Integration**: Uses `Qwen2.5-7B-Instruct-AWQ` natively via vLLM on ROCm for ultra-low latency token generation (<2.5s end-to-end response).
- **GPU-Accelerated Machine Learning**: Employs XGBoost's `tree_method='hist'` to process massive supply chain tabular datasets instantly on AMD GPUs.
- **Efficient RAG**: Leverages HuggingFace `sentence-transformers` via Optimum-AMD for fast vectorization.

## 📁 Project Structure
```text
ascro/
├── main.py                 # Gradio UI Entry Point
├── graph.py                # LangGraph Orchestration
├── agents/                 # Supervisor, Researcher, Predictor, Executor, Critic
├── rag/                    # FAISS Vector Store & Chunking
├── predictor/              # XGBoost ML Model & DataLoader
├── data/                   # Synthetic Datasets & Docs (auto-generated)
├── eval/                   # Benchmarking Scripts
└── utils/                  # Metrics Tracking & Report Generation
```

## 🛠️ Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure ROCm 7.2 environment is active if using AMD GPUs. For local Windows dev without a local vLLM server, a mock LLM fallback is provided).*

2. **Run the Application**
   ```bash
   python main.py
   ```
   This will automatically:
   - Generate synthetic historical supply chain data and vendor contracts.
   - Build the FAISS RAG index.
   - Train the XGBoost predictive model.
   - Launch the Gradio dashboard at `http://localhost:7860`.

3. **Run Evaluation Benchmarks**
   ```bash
   python eval/evaluate.py
   ```

## 🧠 How It Works
ASCRO utilizes a stateful **LangGraph** where:
1. The **Supervisor** decomposes the query.
2. The **Researcher** retrieves context via RAG.
3. The **Predictor** extracts features and scores risk using XGBoost.
4. The **Executor** drafts a mitigation plan.
5. The **Critic** ensures no hallucinations and enforces constraints.

For a detailed visual breakdown, see [architecture.md](architecture.md).
