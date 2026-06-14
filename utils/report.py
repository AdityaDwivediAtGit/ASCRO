import os
from fpdf import FPDF

def generate_markdown_report(state, output_path="final_report.md"):
    """Generates a markdown report from the agent state."""
    report_content = f"# ASCRO Risk Assessment Report\n\n"
    
    report_content += f"## Original Query\n{state.get('query', 'N/A')}\n\n"
    
    if "research_summary" in state:
        report_content += f"## Research Findings\n{state['research_summary']}\n\n"
        
    if "prediction_result" in state:
        pred = state['prediction_result']
        report_content += f"## Predictive Analysis\n"
        report_content += f"- Risk Score: {pred.get('risk_score', 'N/A')}\n"
        report_content += f"- Disruption Probability: {pred.get('probability', 'N/A')}\n"
        report_content += f"- Explanation: {pred.get('explanation', 'N/A')}\n\n"
        
    if "mitigation_plan" in state:
        report_content += f"## Recommended Mitigation Plan\n{state['mitigation_plan']}\n\n"
        
    with open(output_path, "w") as f:
        f.write(report_content)
    
    return output_path

def generate_pdf_report(state, output_path="final_report.pdf"):
    """Generates a simple PDF report from the state."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="ASCRO Risk Assessment Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=12)
    
    sections = [
        ("Original Query", state.get('query', 'N/A')),
        ("Research Findings", state.get('research_summary', 'N/A')),
        ("Predictive Analysis", str(state.get('prediction_result', 'N/A'))),
        ("Mitigation Plan", state.get('mitigation_plan', 'N/A'))
    ]
    
    for title, content in sections:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=title, ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, txt=str(content).encode('latin-1', 'replace').decode('latin-1'))
        pdf.ln(5)
        
    pdf.output(output_path)
    return output_path
