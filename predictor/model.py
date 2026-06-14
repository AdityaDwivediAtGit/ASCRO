import os
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
import pandas as pd

from predictor.data_loader import load_data

DATA_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(DATA_DIR, "data", "xgboost_model.json")

class SupplyChainPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = None
        self._load_or_train_model()

    def _load_or_train_model(self):
        X, y, df = load_data()
        self.feature_names = list(X.columns)
        
        self.model = xgb.XGBClassifier(
            objective='binary:logistic',
            eval_metric='logloss',
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            tree_method='hist', # Uses GPU if available, else fast CPU
            random_state=42
        )
        
        if os.path.exists(MODEL_PATH):
            self.model.load_model(MODEL_PATH)
        else:
            print("Training XGBoost model from scratch...")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model.fit(X_train, y_train)
            
            y_pred = self.model.predict(X_test)
            f1 = f1_score(y_test, y_pred)
            acc = accuracy_score(y_test, y_pred)
            print(f"Model trained. Test F1: {f1:.3f}, Accuracy: {acc:.3f}")
            
            self.model.save_model(MODEL_PATH)
            print(f"Model saved to {MODEL_PATH}")

    def predict_risk(self, feature_dict: dict):
        """
        Predicts disruption probability given a dictionary of features.
        Missing features from the training set are filled with 0.
        """
        if not self.model:
            return {"error": "Model not loaded."}
            
        # Create a dataframe with a single row of zeros for all known features
        df_input = pd.DataFrame(0, index=[0], columns=self.feature_names)
        
        # Populate the known features
        for key, val in feature_dict.items():
            if key in df_input.columns:
                df_input.at[0, key] = val
            # Handle categorical translation if someone passed raw supplier_id
            elif f"supplier_id_{val}" in df_input.columns:
                df_input.at[0, f"supplier_id_{val}"] = 1
            elif f"region_{val}" in df_input.columns:
                df_input.at[0, f"region_{val}"] = 1
            elif f"material_{val}" in df_input.columns:
                df_input.at[0, f"material_{val}"] = 1
                
        # Predict
        prob = self.model.predict_proba(df_input)[0][1]
        
        # Determine risk score category
        if prob > 0.7:
            risk_level = "HIGH"
        elif prob > 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        return {
            "probability": round(float(prob), 3),
            "risk_score": risk_level,
            "explanation": f"Based on XGBoost analysis, the disruption probability is {prob*100:.1f}%. High risk drivers typically include elevated weather/geo risk indexes or low vendor reliability."
        }

# Singleton instance
predictor_instance = None

def get_predictor():
    global predictor_instance
    if predictor_instance is None:
        try:
            predictor_instance = SupplyChainPredictor()
        except Exception as e:
            print(f"Failed to load predictor: {e}")
    return predictor_instance
