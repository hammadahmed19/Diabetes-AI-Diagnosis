import numpy as np

class DiagnosisModel:
    """AI-based diagnosis model for diabetes and pre-diabetes"""
    
    def __init__(self):
        # Clinical thresholds based on medical guidelines
        self.thresholds = {
            'normal': {'fasting': 100, 'random': 140},
            'prediabetes': {'fasting': 125, 'random': 200},
            'diabetes': {'fasting': 126, 'random': 200}
        }
    
    def predict(self, patient_data):
        """
        Predict diabetes status based on patient data
        Returns: dict with diagnosis, confidence, and risk_level
        """
        glucose = patient_data['glucose_level']
        bmi = patient_data['bmi']
        age = patient_data['age']
        family_history = patient_data.get('family_history', 'no')
        
        # Calculate risk score
        risk_score = 0
        
        # Glucose level assessment
        if glucose >= 200:
            diagnosis = 'Diabetes'
            risk_score += 40
        elif glucose >= 126:
            diagnosis = 'Pre-diabetes (High Risk)'
            risk_score += 30
        elif glucose >= 100:
            diagnosis = 'Pre-diabetes (Moderate Risk)'
            risk_score += 20
        else:
            diagnosis = 'Normal'
            risk_score += 5
        
        # BMI factor
        if bmi >= 30:
            risk_score += 20
        elif bmi >= 25:
            risk_score += 10
        
        # Age factor
        if age >= 45:
            risk_score += 15
        
        # Family history
        if family_history == 'yes':
            risk_score += 15
        
        # Calculate confidence
        confidence = min(risk_score / 100 * 100, 95)
        
        # Determine risk level
        if risk_score >= 60:
            risk_level = 'High'
        elif risk_score >= 35:
            risk_level = 'Moderate'
        else:
            risk_level = 'Low'
        
        return {
            'diagnosis': diagnosis,
            'confidence': round(confidence, 2),
            'risk_level': risk_level,
            'risk_score': risk_score
        }
