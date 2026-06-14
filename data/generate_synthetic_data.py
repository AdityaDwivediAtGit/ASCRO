import os
import pandas as pd
import numpy as np
import random

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def generate_tabular_data(n_samples=1000):
    print("Generating synthetic tabular data...")
    np.random.seed(42)
    random.seed(42)
    
    # Features
    suppliers = [f"Supplier_{chr(65+i)}" for i in range(10)]
    regions = ["APAC", "NA", "EMEA", "LATAM"]
    materials = ["Semiconductors", "Steel", "Plastics", "Lithium", "Packaging"]
    
    data = []
    for _ in range(n_samples):
        supplier = random.choice(suppliers)
        region = random.choice(regions)
        material = random.choice(materials)
        
        # Risk factors
        lead_time_days = int(np.random.normal(30, 10))
        weather_risk_index = np.random.uniform(0, 1)
        geopolitical_risk_index = np.random.uniform(0, 1)
        vendor_reliability_score = np.random.uniform(0.5, 1.0)
        
        # Target variable (probability of disruption > 0.7 = disruption)
        # Higher weather, higher geo, lower vendor reliability -> higher risk
        risk_score = (0.3 * weather_risk_index + 
                      0.4 * geopolitical_risk_index + 
                      0.3 * (1 - vendor_reliability_score) + 
                      0.1 * (lead_time_days / 60))
        
        # Add some noise
        risk_score += np.random.normal(0, 0.1)
        risk_score = max(0.0, min(1.0, risk_score))
        
        disrupted = 1 if risk_score > 0.65 else 0
        
        data.append({
            "supplier_id": supplier,
            "region": region,
            "material": material,
            "lead_time_days": lead_time_days,
            "weather_risk_index": round(weather_risk_index, 3),
            "geopolitical_risk_index": round(geopolitical_risk_index, 3),
            "vendor_reliability_score": round(vendor_reliability_score, 3),
            "historical_risk_score": round(risk_score, 3),
            "disrupted": disrupted
        })
        
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(DATA_DIR, "supply_chain_history.csv"), index=False)
    print(f"Saved tabular data to supply_chain_history.csv ({n_samples} rows)")

def generate_rag_documents():
    print("Generating synthetic documents for RAG...")
    docs_dir = os.path.join(DATA_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    doc_1 = """# TCS Supply Chain Resilience Playbook
## Semiconductor Shortage Mitigation
When assessing semiconductor shortages, specifically for Q3 auto clients, the immediate actions are:
1. Identify dual-sourcing options in NA or EMEA regions to offset APAC dependency.
2. Review vendor reliability scores. Any vendor below 0.75 should be flagged for immediate audit.
3. Leverage strategic buffer inventory for critical lithium and semiconductor components.
4. Implement rapid re-routing protocols if geopolitical risk index exceeds 0.60.
"""

    doc_2 = """# Supplier Contract: Supplier_C
**Material:** Semiconductors
**Region:** APAC
**Terms:** 
Supplier_C agrees to a standard lead time of 45 days. In the event of force majeure (including extreme weather events with risk index > 0.8), Supplier_C is exempt from SLA penalties.
Current vendor reliability score as of Q2 is 0.68 due to recent logistical bottlenecks at major ports.
"""

    doc_3 = """# Global Supply Chain News - Q3 2026
**Alert:** Increasing tensions in major trade routes are causing a spike in geopolitical risk indexes, currently averaging 0.72 in affected zones. 
Auto manufacturers relying heavily on APAC semiconductor imports are advised to activate contingency plans.
A major storm is also brewing, elevating weather risks in key manufacturing hubs.
"""

    doc_4 = """# Supplier Contract: Supplier_A
**Material:** Semiconductors
**Region:** NA
**Terms:**
Supplier_A offers premium expedited shipping with a standard lead time of 20 days.
Vendor reliability score is stellar at 0.95. No geopolitical risk exemptions.
Cost is 20% higher than standard market rate, but guaranteed delivery makes it suitable for critical mitigation plans.
"""

    with open(os.path.join(docs_dir, "tcs_playbook.md"), "w") as f:
        f.write(doc_1)
        
    with open(os.path.join(docs_dir, "contract_supplier_c.md"), "w") as f:
        f.write(doc_2)
        
    with open(os.path.join(docs_dir, "news_q3.md"), "w") as f:
        f.write(doc_3)
        
    with open(os.path.join(docs_dir, "contract_supplier_a.md"), "w") as f:
        f.write(doc_4)
        
    print("Saved synthetic documents to docs/ directory.")

if __name__ == "__main__":
    generate_tabular_data()
    generate_rag_documents()
    print("Data generation complete.")
