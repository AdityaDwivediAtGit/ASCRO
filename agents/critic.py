from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm_provider import get_llm
from utils.metrics import tracker

CRITIC_PROMPT = """You are the Critic Agent for ASCRO.
Review the proposed mitigation plan against the initial query and the identified risks.
Check for hallucinations, feasibility, and whether it addresses the core issue.
If the plan is acceptable, output "APPROVE".
If the plan is flawed, output "REJECT: [Reason]".
Your output should ONLY begin with APPROVE or REJECT.
"""

def critic_agent(state: dict):
    tracker.start_timer()
    llm = get_llm(role="critic")
    
    query = state.get("query", "")
    plan = state.get("mitigation_plan", "")
    
    messages = [
        SystemMessage(content=CRITIC_PROMPT),
        HumanMessage(content=f"Query: {query}\n\nPlan:\n{plan}\n\nReview the plan:")
    ]
    
    response = llm.invoke(messages)
    tracker.stop_timer()
    
    content = response.content.strip().upper()
    is_approved = content.startswith("APPROVE")
    
    # Cap revisions to prevent infinite loops
    if not is_approved and state.get("revision_count", 0) >= 2:
        is_approved = True
        
    return {"is_approved": is_approved, "critic_feedback": response.content, "current_agent": "critic"}
