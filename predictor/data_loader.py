import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CSV_FILE = os.path.join(DATA_DIR, "supply_chain_history.csv")

def load_data():
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(f"{CSV_FILE} not found. Run generate_synthetic_data.py first.")
    
    df = pd.read_csv(CSV_FILE)
    
    # Feature engineering for ML
    df_encoded = pd.get_dummies(df, columns=['supplier_id', 'region', 'material'])
    
    # Separate features and target
    X = df_encoded.drop(['disrupted', 'historical_risk_score'], axis=1)
    y = df['disrupted']
    
    return X, y, df

def get_feature_names():
    X, _, _ = load_data()
    return list(X.columns)
