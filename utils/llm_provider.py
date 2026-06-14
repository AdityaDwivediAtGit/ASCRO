import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from utils.metrics import tracker

# We use ChatOpenAI pointing to a local vLLM server by default.
# vLLM provides an OpenAI compatible API.

VLLM_API_BASE = os.environ.get("VLLM_API_BASE", "http://localhost:8000/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct-AWQ")
USE_MOCK_LLM = os.environ.get("USE_MOCK_LLM", "1") == "1"

class MockLLM:
    """A mock LLM fallback to ensure the hackathon demo runs even without an active GPU server."""
    def __init__(self, role="agent"):
        self.role = role
        
    def invoke(self, messages):
        tracker.add_tokens(150)
        # Simple heuristics to return fake responses based on the last message
        last_msg = str(messages[-1].content).lower()
        if "plan" in last_msg or "mitigation" in last_msg:
            resp = "1. Immediate Action: Source from alternative vendors.\n2. Mid-term: Buffer inventory."
        elif "research" in last_msg or "context" in last_msg:
            resp = "Research shows severe delays expected in APAC due to weather. Vendor A is highly reliable."
        elif "predict" in last_msg or "score" in last_msg:
            resp = "Risk score is elevated. Disruption probability is 85%."
        elif "critic" in last_msg or "review" in last_msg:
            resp = "The plan looks solid and addresses all constraints. APPROVE."
        else:
            resp = "I have processed the request and updated the state accordingly."
        return AIMessage(content=resp)

def get_llm(role="agent"):
    if USE_MOCK_LLM:
        return MockLLM(role=role)
    else:
        # Real vLLM endpoint
        return ChatOpenAI(
            base_url=VLLM_API_BASE,
            api_key="EMPTY", # vllm doesn't need a real key
            model=MODEL_NAME,
            temperature=0.1,
            max_tokens=1024
        )
