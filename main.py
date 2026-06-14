import os
import gradio as gr
from graph import run_workflow
from utils.metrics import tracker
from utils.report import generate_markdown_report

# Ensure synthetic data exists on first run
if not os.path.exists(os.path.join("data", "supply_chain_history.csv")):
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from data.generate_synthetic_data import generate_tabular_data, generate_rag_documents
    generate_tabular_data()
    generate_rag_documents()

# Initialize everything
from rag.indexer import build_index
if not os.path.exists(os.path.join("data", "faiss_index")):
    build_index()

def process_query(query: str):
    # Reset metrics
    tracker.total_tokens = 0
    tracker.latency_ms = 0
    
    events, final_state = run_workflow(query)
    
    # Format Trace
    trace_text = "### Agent Execution Trace\n\n"
    for node_name, state_update in events:
        trace_text += f"**[{node_name}]**\n"
        if "research_summary" in state_update:
            trace_text += f"Research Findings Extracted.\n"
        if "prediction_result" in state_update:
            trace_text += f"Prediction: {state_update['prediction_result'].get('risk_score', 'N/A')}\n"
        if "mitigation_plan" in state_update:
            trace_text += f"Plan Drafted (Revision {state_update.get('revision_count', 0)}).\n"
        if "critic_feedback" in state_update:
            trace_text += f"Critic: {state_update['critic_feedback']}\n"
        trace_text += "\n"
        
    # Format Final Output
    final_output = final_state.get("mitigation_plan", "No plan generated.")
    
    # Get Metrics
    metrics = tracker.get_metrics()
    metrics_text = f"**Latency:** {metrics['Latency (ms)']} ms | **Tokens:** {metrics['Total Tokens']} | **GPU Mem:** {metrics['GPU Mem Used (MB)']} MB"
    
    # Generate Report File
    report_path = generate_markdown_report(final_state)
    
    return final_output, trace_text, metrics_text, report_path

with gr.Blocks(title="ASCRO - Agentic Supply Chain Resilience Orchestrator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏭 ASCRO: Agentic Supply Chain Resilience Orchestrator")
    gr.Markdown("TCS & AMD AI Hackathon Prototype | Powered by LangGraph, XGBoost, and vLLM (ROCm)")
    
    with gr.Tabs():
        with gr.TabItem("Chat & Orchestration"):
            with gr.Row():
                with gr.Column(scale=2):
                    query_input = gr.Textbox(
                        label="Describe the scenario or disruption", 
                        placeholder="e.g. Assess semiconductor shortage risk for Q3 auto client due to APAC storms.",
                        lines=3
                    )
                    submit_btn = gr.Button("Assess & Mitigate", variant="primary")
                    
                    gr.Examples(
                        examples=[
                            "Assess semiconductor shortage risk for Q3 auto client due to APAC storms.",
                            "Supplier_A is delayed by 30 days in NA. What's the impact and mitigation?",
                            "Geopolitical tensions rising in EMEA. Evaluate Supplier_C steel delivery risk."
                        ],
                        inputs=query_input
                    )
                with gr.Column(scale=1):
                    metrics_output = gr.Markdown("### Real-time Metrics\n*Run a query to see performance stats.*")
                    report_file = gr.File(label="Export Final Report")

            with gr.Row():
                with gr.Column(scale=1):
                    trace_output = gr.Markdown("### Agent Trace\n*Waiting for input...*")
                with gr.Column(scale=2):
                    final_plan_output = gr.Markdown("### Mitigation Plan\n*Waiting for input...*")

            submit_btn.click(
                fn=process_query,
                inputs=query_input,
                outputs=[final_plan_output, trace_output, metrics_output, report_file]
            )
            
        with gr.TabItem("System Architecture"):
            gr.Markdown("""
            ## ASCRO Multi-Agent Architecture
            
            This system runs on **AMD MI300X** instances using ROCm optimizations:
            - **vLLM**: Qwen2.5-7B-Instruct-AWQ for low-latency agent reasoning.
            - **Embeddings**: Sentence-Transformers via Optimum-AMD.
            - **Predictor**: XGBoost GPU tree method.
            
            **Agent Flow**:
            1. **Supervisor**: Analyzes the query and routes tasks.
            2. **Researcher**: Retrieves supply chain data using FAISS RAG.
            3. **Predictor**: ML model outputs probability of disruption.
            4. **Executor**: Drafts a comprehensive mitigation strategy.
            5. **Critic**: Self-reflects and rejects poor plans back to the Executor.
            """)

if __name__ == "__main__":
    # Launch on 0.0.0.0 and enable share=True for notebooks.amd.com proxy access
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
