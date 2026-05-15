import os
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

class LLMDiagnosisModel:
    """LLM-powered diagnosis model for diabetes and pre-diabetes"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('MODEL_NAME', 'gpt-4-turbo-preview')
        
    def predict(self, patient_data):
        """
        Use LLM to analyze patient data and provide diagnosis
        Returns: dict with diagnosis, confidence, risk_level, and reasoning
        """
        
        # Create detailed prompt for the LLM
        prompt = self._create_diagnosis_prompt(patient_data)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert endocrinologist AI assistant specializing in diabetes diagnosis. 
                        Analyze patient data and provide accurate diagnosis based on medical guidelines:
                        - Normal: Fasting glucose < 100 mg/dL
                        - Pre-diabetes: Fasting glucose 100-125 mg/dL
                        - Diabetes: Fasting glucose ≥ 126 mg/dL or Random glucose ≥ 200 mg/dL
                        
                        Consider all risk factors including BMI, age, family history, and lifestyle.
                        Provide diagnosis in JSON format with diagnosis, confidence, risk_level, and detailed reasoning."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"LLM Error: {e}")
            # Fallback to rule-based diagnosis
            return self._fallback_diagnosis(patient_data)
    
    def _create_diagnosis_prompt(self, patient_data):
        """Create detailed prompt for LLM analysis"""
        return f"""
Analyze the following patient data and provide a diabetes diagnosis:

Patient Information:
- Name: {patient_data['name']}
- Age: {patient_data['age']} years
- Blood Glucose Level: {patient_data['glucose_level']} mg/dL
- BMI: {patient_data['bmi']}
- Family History of Diabetes: {patient_data.get('family_history', 'no')}
- Physical Activity Level: {patient_data.get('physical_activity', 'moderate')}

Please provide your analysis in the following JSON format:
{{
    "diagnosis": "Normal/Pre-diabetes/Diabetes",
    "confidence": 85.5,
    "risk_level": "Low/Moderate/High",
    "reasoning": "Detailed explanation of the diagnosis",
    "key_factors": ["factor1", "factor2"],
    "risk_score": 45
}}

Consider all clinical guidelines and risk factors in your assessment.
"""
    
    def _fallback_diagnosis(self, patient_data):
        """Fallback rule-based diagnosis if LLM fails"""
        glucose = patient_data['glucose_level']
        bmi = patient_data['bmi']
        age = patient_data['age']
        
        risk_score = 0
        key_factors = []
        
        if glucose >= 200:
            diagnosis = 'Diabetes'
            risk_score += 40
            key_factors.append('Very high glucose level')
        elif glucose >= 126:
            diagnosis = 'Pre-diabetes (High Risk)'
            risk_score += 30
            key_factors.append('Elevated glucose level')
        elif glucose >= 100:
            diagnosis = 'Pre-diabetes (Moderate Risk)'
            risk_score += 20
            key_factors.append('Borderline glucose level')
        else:
            diagnosis = 'Normal'
            risk_score += 5
            key_factors.append('Normal glucose level')
        
        if bmi >= 30:
            risk_score += 20
            key_factors.append('Obesity (BMI ≥ 30)')
        elif bmi >= 25:
            risk_score += 10
            key_factors.append('Overweight (BMI ≥ 25)')
        
        if age >= 45:
            risk_score += 15
            key_factors.append('Age over 45')
        
        if patient_data.get('family_history') == 'yes':
            risk_score += 15
            key_factors.append('Family history of diabetes')
        
        risk_level = 'High' if risk_score >= 60 else 'Moderate' if risk_score >= 35 else 'Low'
        confidence = min(risk_score / 100 * 100, 95)
        
        return {
            'diagnosis': diagnosis,
            'confidence': round(confidence, 2),
            'risk_level': risk_level,
            'risk_score': risk_score,
            'reasoning': f"Based on clinical analysis: {', '.join(key_factors)}",
            'key_factors': key_factors
        }
