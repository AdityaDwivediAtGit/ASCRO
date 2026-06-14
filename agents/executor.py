from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm_provider import get_llm
from utils.metrics import tracker

EXECUTOR_PROMPT = """You are the Executor Agent for ASCRO.
Your task is to draft a comprehensive supply chain mitigation plan based on the research findings and predictive risk score.
Format the plan clearly with actionable steps, timelines, and alternatives.
Do not hallucinate facts; rely only on the provided context.
"""

def executor_agent(state: dict):
    tracker.start_timer()
    llm = get_llm(role="executor")
    
    query = state.get("query", "")
    research = state.get("research_summary", "")
    pred = state.get("prediction_result", {})
    
    context = f"Query: {query}\n\nResearch:\n{research}\n\nPrediction Risk Score: {pred.get('risk_score', 'N/A')} (Prob: {pred.get('probability', 'N/A')})"
    
    messages = [
        SystemMessage(content=EXECUTOR_PROMPT),
        HumanMessage(content=f"{context}\n\nDraft the mitigation plan:")
    ]
    
    response = llm.invoke(messages)
    tracker.stop_timer()
    
    return {"mitigation_plan": response.content, "current_agent": "executor", "revision_count": state.get("revision_count", 0) + 1}
