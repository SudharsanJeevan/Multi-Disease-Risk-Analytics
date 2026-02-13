"""
Prediction Engine Module
Loads trained ML models and makes predictions
"""

import pickle
import numpy as np
import pandas as pd
from pathlib import Path
import config

class DiseasePredictor:
    """Handles disease prediction using trained ML models"""
    
    def __init__(self, disease_type):
        """
        Initialize predictor for specific disease
        
        Args:
            disease_type: One of 'diabetes', 'heart', 'kidney', 'liver', 'breast_cancer'
        """
        self.disease_type = disease_type
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load trained model and scaler"""
        try:
            model_path = config.MODEL_PATHS[self.disease_type]["model"]
            scaler_path = config.MODEL_PATHS[self.disease_type]["scaler"]
            
            if model_path.exists() and scaler_path.exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                return True
            else:
                print(f"Model files not found for {self.disease_type}")
                return False
                
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def is_model_available(self):
        """Check if model is loaded and ready"""
        return self.model is not None and self.scaler is not None
    
    def predict(self, input_data):
        """
        Make prediction
        
        Args:
            input_data: Dictionary or list/array of input features
        
        Returns:
            dict with keys: 'prediction', 'probability', 'risk_level'
        """
        if not self.is_model_available():
            return {
                'error': 'Model not available',
                'prediction': None,
                'probability': None,
                'risk_level': None
            }
        
        try:
            # Convert input to array
            if isinstance(input_data, dict):
                input_array = np.array(list(input_data.values())).reshape(1, -1)
            elif isinstance(input_data, (list, np.ndarray)):
                input_array = np.array(input_data).reshape(1, -1)
            else:
                return {'error': 'Invalid input format'}
            
            # Scale features
            input_scaled = self.scaler.transform(input_array)
            
            # Make prediction
            prediction = self.model.predict(input_scaled)[0]
            
            # Get probability if available
            if hasattr(self.model, 'predict_proba'):
                probability = self.model.predict_proba(input_scaled)[0]
                # Probability of positive class (disease present)
                risk_prob = probability[1] if len(probability) > 1 else probability[0]
            else:
                # For models without predict_proba, use decision function
                if hasattr(self.model, 'decision_function'):
                    decision = self.model.decision_function(input_scaled)[0]
                    # Convert to probability-like score (0-1 range)
                    risk_prob = 1 / (1 + np.exp(-decision))
                else:
                    risk_prob = float(prediction)
            
            # Determine risk level
            risk_level = self.get_risk_level(risk_prob)
            
            return {
                'prediction': int(prediction),
                'probability': float(risk_prob),
                'risk_level': risk_level,
                'error': None
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'prediction': None,
                'probability': None,
                'risk_level': None
            }
    
    def get_risk_level(self, probability):
        """
        Determine risk level based on probability
        
        Args:
            probability: Risk probability (0-1)
        
        Returns:
            str: 'Low', 'Moderate', or 'High'
        """
        if probability < config.RISK_THRESHOLDS['low']:
            return 'Low'
        elif probability > config.RISK_THRESHOLDS['high']:
            return 'High'
        else:
            return 'Moderate'
    
    def get_risk_color(self, risk_level):
        """Get color code for risk level"""
        color_map = {
            'Low': config.COLORS['low_risk'],
            'Moderate': config.COLORS['moderate_risk'],
            'High': config.COLORS['high_risk']
        }
        return color_map.get(risk_level, config.COLORS['secondary'])
    
    def get_recommendations(self, risk_level, disease_type):
        """
        Get health recommendations based on risk level and disease
        
        Args:
            risk_level: str ('Low', 'Moderate', 'High')
            disease_type: str
        
        Returns:
            list of recommendation strings
        """
        recommendations = {
            'diabetes': {
                'Low': [
                    "✅ Maintain a healthy diet with balanced carbohydrates",
                    "✅ Regular physical activity (30 minutes daily)",
                    "✅ Monitor blood sugar levels periodically",
                    "✅ Maintain healthy body weight"
                ],
                'Moderate': [
                    "⚠️ Consult a doctor for detailed evaluation",
                    "⚠️ Monitor blood sugar levels regularly",
                    "⚠️ Follow a strict diet plan",
                    "⚠️ Increase physical activity",
                    "⚠️ Reduce sugar and processed food intake"
                ],
                'High': [
                    "🚨 Immediate medical consultation recommended",
                    "🚨 Regular blood sugar monitoring essential",
                    "🚨 Follow prescribed medication strictly",
                    "🚨 Strict diet control required",
                    "🚨 Daily exercise routine necessary"
                ]
            },
            'heart': {
                'Low': [
                    "✅ Maintain healthy cholesterol levels",
                    "✅ Regular cardiovascular exercise",
                    "✅ Heart-healthy diet (low sodium, healthy fats)",
                    "✅ Avoid smoking and excessive alcohol"
                ],
                'Moderate': [
                    "⚠️ Consult a cardiologist",
                    "⚠️ Monitor blood pressure regularly",
                    "⚠️ Reduce sodium intake",
                    "⚠️ Manage stress levels",
                    "⚠️ Regular ECG checkups"
                ],
                'High': [
                    "🚨 Urgent cardiology consultation required",
                    "🚨 Daily blood pressure monitoring",
                    "🚨 Strict medication adherence",
                    "🚨 Avoid strenuous activities",
                    "🚨 Emergency contact readily available"
                ]
            },
            'kidney': {
                'Low': [
                    "✅ Stay well hydrated",
                    "✅ Maintain healthy blood pressure",
                    "✅ Limit salt intake",
                    "✅ Regular kidney function tests"
                ],
                'Moderate': [
                    "⚠️ Consult a nephrologist",
                    "⚠️ Monitor kidney function regularly",
                    "⚠️ Control blood pressure and sugar",
                    "⚠️ Limit protein intake if advised",
                    "⚠️ Avoid nephrotoxic medications"
                ],
                'High': [
                    "🚨 Immediate nephrology consultation",
                    "🚨 Regular dialysis may be needed",
                    "🚨 Strict dietary restrictions",
                    "🚨 Close monitoring of fluid intake",
                    "🚨 Regular lab tests essential"
                ]
            },
            'liver': {
                'Low': [
                    "✅ Limit alcohol consumption",
                    "✅ Maintain healthy body weight",
                    "✅ Avoid hepatotoxic substances",
                    "✅ Regular liver function tests"
                ],
                'Moderate': [
                    "⚠️ Consult a hepatologist",
                    "⚠️ Complete abstinence from alcohol",
                    "⚠️ Monitor liver enzymes regularly",
                    "⚠️ Avoid fatty foods",
                    "⚠️ Medication review with doctor"
                ],
                'High': [
                    "🚨 Urgent hepatology consultation",
                    "🚨 Complete alcohol cessation",
                    "🚨 Regular liver function monitoring",
                    "🚨 Strict dietary control",
                    "🚨 Watch for warning signs (jaundice, etc.)"
                ]
            },
            'breast_cancer': {
                'Low': [
                    "✅ Regular self-examinations",
                    "✅ Annual mammography screening",
                    "✅ Maintain healthy lifestyle",
                    "✅ Know your family history"
                ],
                'Moderate': [
                    "⚠️ Consult an oncologist",
                    "⚠️ Additional screening tests recommended",
                    "⚠️ More frequent self-examinations",
                    "⚠️ Discuss preventive options with doctor",
                    "⚠️ Monitor for any changes"
                ],
                'High': [
                    "🚨 Immediate oncology consultation",
                    "🚨 Comprehensive diagnostic workup needed",
                    "🚨 Biopsy may be required",
                    "🚨 Discuss treatment options",
                    "🚨 Seek second opinion if needed"
                ]
            }
        }
        
        return recommendations.get(disease_type, {}).get(risk_level, [
            "Consult healthcare professional for personalized advice"
        ])


def get_predictor(disease_type):
    """
    Factory function to get predictor instance
    
    Args:
        disease_type: One of 'diabetes', 'heart', 'kidney', 'liver', 'breast_cancer'
    
    Returns:
        DiseasePredictor instance
    """
    return DiseasePredictor(disease_type)
