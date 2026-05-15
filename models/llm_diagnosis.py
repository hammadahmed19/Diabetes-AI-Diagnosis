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
        
        # Check if this is questionnaire-only mode
        is_questionnaire_only = patient_data.get('mode') == 'questionnaire_only'
        
        if is_questionnaire_only:
            # Questionnaire-only diagnosis (no lab tests)
            prompt = f"""
You are an expert endocrinologist performing an initial diabetes risk assessment based on patient symptoms, lifestyle, and medical history WITHOUT laboratory test results.

Patient Name: {patient_data['name']}

"""
            # Add questionnaire data
            if 'questionnaire' in patient_data:
                q_data = patient_data['questionnaire']
                prompt += f"""Questionnaire Risk Assessment:
- Risk Score: {q_data['risk_score']['total_score']}/{q_data['risk_score']['max_score']}
- Risk Percentage: {q_data['risk_score']['risk_percentage']}%
- Risk Level: {q_data['risk_score']['risk_level']}

Detailed Patient Assessment:
"""
                for section in q_data['formatted_answers']:
                    prompt += f"\n{section['section']}:\n"
                    for response in section['responses']:
                        prompt += f"  - {response['question']}: {response['answer']}\n"
            
            prompt += """
Based on this clinical assessment WITHOUT lab test results, provide your professional evaluation:

IMPORTANT: Since we don't have glucose levels or other lab tests, your diagnosis should be:
- "High Risk for Diabetes" - if multiple severe symptoms and risk factors present
- "Moderate Risk for Pre-diabetes" - if some symptoms and risk factors present
- "Low Risk" - if minimal symptoms and risk factors
- Always recommend laboratory testing for confirmation

Please provide your analysis in the following JSON format:
{
    "diagnosis": "High Risk for Diabetes/Moderate Risk for Pre-diabetes/Low Risk",
    "confidence": 75.5,
    "risk_level": "Low/Moderate/High",
    "reasoning": "Detailed explanation based on symptoms, lifestyle, and medical history. Emphasize that lab tests are needed for definitive diagnosis.",
    "key_factors": ["factor1", "factor2", "factor3"],
    "risk_score": 45,
    "recommendations": ["Recommend fasting glucose test", "Recommend HbA1c test", "Other recommendations"]
}

Consider all symptoms, lifestyle factors, and medical history in your assessment. Remember this is a screening assessment, not a definitive diagnosis.
"""
        else:
            # Standard diagnosis with lab tests
            prompt = f"""
Analyze the following patient data and provide a diabetes diagnosis:

Patient Information:
- Name: {patient_data['name']}
- Age: {patient_data['age']} years
- Blood Glucose Level: {patient_data['glucose_level']} mg/dL
- BMI: {patient_data['bmi']}
- Family History of Diabetes: {patient_data.get('family_history', 'no')}
- Physical Activity Level: {patient_data.get('physical_activity', 'moderate')}
"""
            
            # Add questionnaire data if available
            if 'questionnaire' in patient_data:
                q_data = patient_data['questionnaire']
                prompt += f"""

Questionnaire Risk Assessment:
- Risk Score: {q_data['risk_score']['total_score']}/{q_data['risk_score']['max_score']}
- Risk Percentage: {q_data['risk_score']['risk_percentage']}%
- Risk Level: {q_data['risk_score']['risk_level']}

Detailed Questionnaire Responses:
"""
                for section in q_data['formatted_answers']:
                    prompt += f"\n{section['section']}:\n"
                    for response in section['responses']:
                        prompt += f"  - {response['question']}: {response['answer']}\n"
            
            prompt += """
Please provide your analysis in the following JSON format:
{
    "diagnosis": "Normal/Pre-diabetes/Diabetes",
    "confidence": 85.5,
    "risk_level": "Low/Moderate/High",
    "reasoning": "Detailed explanation of the diagnosis",
    "key_factors": ["factor1", "factor2"],
    "risk_score": 45
}

Consider all clinical guidelines, questionnaire responses, and risk factors in your assessment.
"""
        
        return prompt
    
    def _fallback_diagnosis(self, patient_data):
        """Fallback rule-based diagnosis if LLM fails"""
        
        # Check if questionnaire-only mode
        is_questionnaire_only = patient_data.get('mode') == 'questionnaire_only'
        
        if is_questionnaire_only:
            # Use questionnaire risk score for diagnosis
            if 'questionnaire' in patient_data:
                risk_data = patient_data['questionnaire']['risk_score']
                risk_percentage = risk_data['risk_percentage']
                
                if risk_percentage >= 70:
                    diagnosis = 'High Risk for Diabetes - Lab Tests Recommended'
                    confidence = min(risk_percentage, 85)
                    risk_level = 'High'
                elif risk_percentage >= 40:
                    diagnosis = 'Moderate Risk for Pre-diabetes - Lab Tests Recommended'
                    confidence = min(risk_percentage, 75)
                    risk_level = 'Moderate'
                else:
                    diagnosis = 'Low Risk - Routine Screening Recommended'
                    confidence = 70
                    risk_level = 'Low'
                
                return {
                    'diagnosis': diagnosis,
                    'confidence': round(confidence, 2),
                    'risk_level': risk_level,
                    'risk_score': risk_data['total_score'],
                    'reasoning': f"Based on questionnaire assessment with {risk_percentage}% risk score. Laboratory testing is required for definitive diagnosis.",
                    'key_factors': ['Questionnaire-based screening', 'Lab tests needed for confirmation'],
                    'recommendations': ['Fasting glucose test', 'HbA1c test', 'Consult healthcare provider']
                }
        
        # Standard fallback with lab values
        glucose = patient_data.get('glucose_level', 0)
        bmi = patient_data.get('bmi', 25)
        age = patient_data.get('age', 30)
        
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
