import os
import joblib
import numpy as np
from .preprocessing import preprocess_text

class SpamPredictor:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "models", "spam_classifier.joblib")
        vectorizer_path = os.path.join(base_dir, "models", "tfidf_vectorizer.joblib")
        
        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            raise RuntimeError(f"Model or vectorizer not found in {base_dir}/models. Please train models first.")
            
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        
    def predict(self, body: str, subject: str = "") -> dict:
        clean_text = preprocess_text(body=body, subject=subject)
        
        if not clean_text.strip():
            raise ValueError("Input contains no usable text after preprocessing.")
            
        features = self.vectorizer.transform([clean_text])
        
        # We check if model has predict_proba, if not we use decision_function
        if hasattr(self.model, "predict_proba"):
            probs = self.model.predict_proba(features)[0]
            prediction_val = self.model.predict(features)[0]
            # Probabilities for class 0 (ham) and class 1 (spam)
            prob_spam = probs[1]
        else:
            decision = self.model.decision_function(features)[0]
            prediction_val = self.model.predict(features)[0]
            # Sigmoid conversion
            prob_spam = 1.0 / (1.0 + np.exp(-decision))
            
        if prediction_val == 1:
            prediction_label = "spam"
            confidence = float(prob_spam)
            message = "This email is likely spam."
        else:
            prediction_label = "not_spam"
            confidence = float(1.0 - prob_spam)
            message = "This email looks legitimate."
            
        return {
            "prediction": prediction_label,
            "confidence": round(confidence, 4),
            "message": message
        }
