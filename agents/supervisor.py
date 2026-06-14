from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm_provider import get_llm
from utils.metrics import tracker

SUPERVISOR_PROMPT = """You are the Supervisor Agent for ASCRO (Agentic Supply Chain Resilience Orchestrator).
Your job is to read the user's query about a supply chain disruption and decide the next steps.
Extract any relevant entities: Supplier IDs, Regions, Materials.
Your output MUST be exactly one of the following next nodes: "Researcher" or "Predictor".
Always start with "Researcher" to gather context, unless the user explicitly bypasses research.
Do not output anything else.
"""

def supervisor_agent(state: dict):
    tracker.start_timer()
    llm = get_llm(role="supervisor")
    
    query = state.get("query", "")
    messages = [
        SystemMessage(content=SUPERVISOR_PROMPT),
        HumanMessage(content=query)
    ]
    
    response = llm.invoke(messages)
    tracker.stop_timer()
    
    # We always route to Researcher first for simplicity in this prototype.
    return {"current_agent": "supervisor", "next_node": "Researcher"}
