# ASCRO Architecture

ASCRO relies on a multi-agent orchestration framework (LangGraph) integrated with an ML Predictor and RAG.

## Component Flow

```mermaid
graph TD
    User([User Query]) --> Supervisor[Supervisor Agent]
    
    subgraph "Agentic Core (LangGraph on vLLM)"
        Supervisor --> Researcher[Researcher Agent]
        Researcher --> Predictor[Predictor Agent]
        Predictor --> Executor[Executor Agent]
        Executor --> Critic[Critic Agent]
        Critic -- Reject (Max 2) --> Executor
    end
    
    subgraph "RAG Pipeline"
        Researcher -.-> FAISS[(FAISS Vector DB)]
        Docs[TCS Playbooks / Contracts] --> FAISS
    end
    
    subgraph "ML Predictor"
        Predictor -.-> XGBoost[XGBoost Classifier]
        CSV[Tabular History Data] --> XGBoost
    end
    
    Critic -- Approve --> Output([Mitigation Plan & Report])
```

## Agent Roles
1. **Supervisor Agent**: Extracts parameters and routes.
2. **Researcher Agent**: Performs similarity search against `data/docs` to find relevant supplier contracts, geographical risk profiles, and internal TCS mitigation playbooks.
3. **Predictor Agent**: Translates text parameters into numerical features. Queries the XGBoost model to get a real-time risk score and probability of supply chain failure.
4. **Executor Agent**: Combines context from the Researcher and the numeric risk assessment from the Predictor to formulate an exact step-by-step mitigation plan.
5. **Critic Agent**: Reviews the Executor's plan for feasibility and hallucinations. Sends it back if it does not address the risk adequately.
