import re
from predictor.model import get_predictor
from utils.metrics import tracker

def predictor_agent(state: dict):
    tracker.start_timer()
    predictor = get_predictor()
    
    query = state.get("query", "")
    summary = state.get("research_summary", "")
    
    # Simple entity extraction heuristic since we want it to run fast on local hardware
    # We look for keywords matching our tabular data.
    features = {}
    
    text_to_search = (query + " " + summary).lower()
    
    if "apac" in text_to_search: features["region_APAC"] = 1
    elif "emea" in text_to_search: features["region_EMEA"] = 1
    elif "na " in text_to_search: features["region_NA"] = 1
    
    if "semiconductor" in text_to_search: features["material_Semiconductors"] = 1
    
    match = re.search(r"supplier_([a-z])", text_to_search)
    if match:
        features[f"supplier_id_Supplier_{match.group(1).upper()}"] = 1
        
    if "weather" in text_to_search or "storm" in text_to_search:
        features["weather_risk_index"] = 0.8
    if "geopolitic" in text_to_search or "tension" in text_to_search:
        features["geopolitical_risk_index"] = 0.75
        
    # Get ML prediction
    prediction_result = predictor.predict_risk(features)
    
    tracker.stop_timer()
    
    return {"prediction_result": prediction_result, "current_agent": "predictor"}
