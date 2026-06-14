from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm_provider import get_llm
from utils.metrics import tracker
from rag.retriever import retriever

RESEARCHER_PROMPT = """You are the Researcher Agent for ASCRO.
Your task is to analyze the user's query and the retrieved context documents, and summarize the key findings.
Focus on identifying specific risk factors, affected regions, alternative suppliers, and relevant policies.
"""

def researcher_agent(state: dict):
    tracker.start_timer()
    llm = get_llm(role="researcher")
    
    query = state.get("query", "")
    
    # Retrieve context
    context = retriever.search(query)
    
    messages = [
        SystemMessage(content=RESEARCHER_PROMPT),
        HumanMessage(content=f"Query: {query}\n\nContext:\n{context}\n\nProvide a summary of the research:")
    ]
    
    response = llm.invoke(messages)
    tracker.stop_timer()
    
    return {"research_summary": response.content, "current_agent": "researcher"}
