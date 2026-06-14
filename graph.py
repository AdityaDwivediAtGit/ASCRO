from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from agents.supervisor import supervisor_agent
from agents.researcher import researcher_agent
from agents.predictor import predictor_agent
from agents.executor import executor_agent
from agents.critic import critic_agent

class AgentState(TypedDict):
    query: str
    current_agent: str
    next_node: Optional[str]
    research_summary: Optional[str]
    prediction_result: Optional[dict]
    mitigation_plan: Optional[str]
    is_approved: Optional[bool]
    critic_feedback: Optional[str]
    revision_count: Optional[int]

def router_node(state: AgentState):
    """A dummy node if needed for conditional edges, though we can route directly."""
    pass

def create_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("Supervisor", supervisor_agent)
    workflow.add_node("Researcher", researcher_agent)
    workflow.add_node("Predictor", predictor_agent)
    workflow.add_node("Executor", executor_agent)
    workflow.add_node("Critic", critic_agent)
    
    # Define edges
    # Standard flow: Supervisor -> Researcher -> Predictor -> Executor -> Critic
    workflow.set_entry_point("Supervisor")
    
    # For prototype simplicity, force linear flow for the first three nodes.
    # In a fully autonomous setting, Supervisor would use conditional edges.
    workflow.add_edge("Supervisor", "Researcher")
    workflow.add_edge("Researcher", "Predictor")
    workflow.add_edge("Predictor", "Executor")
    workflow.add_edge("Executor", "Critic")
    
    # Critic loop
    def critic_router(state: AgentState):
        if state.get("is_approved", False):
            return "END"
        else:
            return "Executor"
            
    workflow.add_conditional_edges(
        "Critic",
        critic_router,
        {"END": END, "Executor": "Executor"}
    )
    
    # Compile
    app = workflow.compile()
    return app

# Initialize the graph
ascro_app = create_graph()

def run_workflow(query: str):
    accumulated_state = {
        "query": query, 
        "revision_count": 0,
        "research_summary": "",
        "prediction_result": {},
        "mitigation_plan": "",
        "is_approved": False,
        "critic_feedback": "",
        "current_agent": ""
    }
    
    # To track the trace, we will stream the events
    events = []
    for event in ascro_app.stream(accumulated_state):
        for node_name, state_update in event.items():
            events.append((node_name, state_update))
            accumulated_state.update(state_update)
            
    return events, accumulated_state
