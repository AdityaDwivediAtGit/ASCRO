import time
import os
import sys

# Ensure we can import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from graph import run_workflow
from utils.metrics import tracker

def evaluate_system():
    print("Starting ASCRO Evaluation...")
    
    test_queries = [
        "Assess semiconductor shortage risk for Q3 auto client due to APAC storms.",
        "Supplier_A is delayed by 30 days in NA. What's the impact?",
        "Geopolitical tensions rising in EMEA. Evaluate Supplier_C steel delivery risk."
    ]
    
    results = []
    
    for i, query in enumerate(test_queries):
        print(f"\n--- Running Test {i+1} ---")
        print(f"Query: {query}")
        
        # Reset tracking
        tracker.total_tokens = 0
        tracker.latency_ms = 0
        
        start = time.time()
        events, final_state = run_workflow(query)
        end = time.time()
        
        metrics = tracker.get_metrics()
        
        prediction = final_state.get('prediction_result', {})
        
        results.append({
            "query": query,
            "latency_ms": metrics["Latency (ms)"],
            "tokens": metrics["Total Tokens"],
            "risk_score": prediction.get('risk_score', 'N/A'),
            "revisions": final_state.get("revision_count", 0)
        })
        
        print(f"Latency: {metrics['Latency (ms)']} ms")
        print(f"Tokens: {metrics['Total Tokens']}")
        print(f"Risk Score: {prediction.get('risk_score', 'N/A')}")
        
    print("\n=== Evaluation Summary ===")
    avg_latency = sum(r["latency_ms"] for r in results) / len(results)
    avg_tokens = sum(r["tokens"] for r in results) / len(results)
    
    print(f"Average Latency: {avg_latency:.2f} ms")
    print(f"Average Tokens per Request: {avg_tokens:.2f}")
    
    # Check if meets hackathon goals (< 2.5s simulated / target latency)
    if avg_latency < 2500:
        print("✅ Latency Goal Met (< 2.5s)")
    else:
        print("⚠️ Latency Goal Not Met (Requires vLLM / AMD optimization)")
        
if __name__ == "__main__":
    evaluate_system()
