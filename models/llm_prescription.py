import os
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

class LLMPrescriptionEngine:
    """LLM-powered prescription generation"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = os.getenv('MODEL_NAME', 'gpt-4-turbo-preview')
    
    def generate_prescription(self, diagnosis_result, patient_data):
        """Generate personalized prescription using LLM"""
        
        prompt = self._create_prescription_prompt(diagnosis_result, patient_data)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert physician specializing in diabetes management.
                        Generate comprehensive, personalized treatment plans including:
                        - Appropriate medications with dosages
                        - Lifestyle modifications
                        - Monitoring requirements
                        - Follow-up schedule
                        - Important warnings and precautions
                        
                        Base recommendations on current medical guidelines and patient-specific factors.
                        Provide output in JSON format."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                response_format={"type": "json_object"}
            )
            
            prescription = json.loads(response.choices[0].message.content)
            return prescription
            
        except Exception as e:
            print(f"LLM Prescription Error: {e}")
            return self._fallback_prescription(diagnosis_result, patient_data)
    
    def _create_prescription_prompt(self, diagnosis_result, patient_data):
        """Create detailed prompt for prescription generation"""
        
        # Check if this is questionnaire-only mode
        is_questionnaire_only = patient_data.get('mode') == 'questionnaire_only'
        
        prompt = f"""
Generate a comprehensive medical prescription for the following patient:

Diagnosis Information:
- Assessment: {diagnosis_result['diagnosis']}
- Risk Level: {diagnosis_result['risk_level']}
- Confidence: {diagnosis_result['confidence']}%
- Reasoning: {diagnosis_result.get('reasoning', 'N/A')}
"""
        
        if is_questionnaire_only:
            # Questionnaire-only mode - no lab data
            prompt += f"""
Patient Details:
- Name: {patient_data.get('name', 'Patient')}
- Assessment Mode: Questionnaire-based screening (NO lab tests available)

"""
            # Add questionnaire data if available
            if 'questionnaire' in patient_data:
                q_data = patient_data['questionnaire']
                prompt += f"""Questionnaire Risk Score: {q_data['risk_score']['risk_percentage']}%

"""
                # Add key questionnaire responses
                for section in q_data['formatted_answers']:
                    prompt += f"{section['section']}:\n"
                    for response in section['responses'][:3]:  # First 3 responses per section
                        prompt += f"  - {response['question']}: {response['answer']}\n"
                    prompt += "\n"
            
            prompt += """
IMPORTANT: Since this is a screening assessment WITHOUT lab tests:
- Emphasize the need for laboratory testing (fasting glucose, HbA1c)
- Provide preventive lifestyle recommendations
- Focus on risk reduction strategies
- Include when to seek medical attention
"""
        else:
            # Standard mode with lab data
            prompt += f"""
Patient Details:
- Age: {patient_data.get('age', 'N/A')} years
- BMI: {patient_data.get('bmi', 'N/A')}
- Glucose Level: {patient_data.get('glucose_level', 'N/A')} mg/dL
- Family History: {patient_data.get('family_history', 'no')}
- Physical Activity: {patient_data.get('physical_activity', 'moderate')}
"""
        
        prompt += """
Please provide a detailed prescription in the following JSON format:
{
    "medications": ["medication 1 with dosage", "medication 2 with dosage"],
    "lifestyle": ["lifestyle recommendation 1", "lifestyle recommendation 2"],
    "diet": ["dietary recommendation 1", "dietary recommendation 2"],
    "exercise": ["exercise recommendation 1", "exercise recommendation 2"],
    "monitoring": ["monitoring requirement 1", "monitoring requirement 2"],
    "follow_up": "Follow-up schedule",
    "warnings": ["warning 1", "warning 2"],
    "emergency_signs": ["sign 1", "sign 2"],
    "additional_notes": "Any additional important information"
}

Ensure all recommendations are evidence-based and appropriate for the patient's condition.
"""
        
        return prompt
    
    def _fallback_prescription(self, diagnosis_result, patient_data):
        """Fallback prescription if LLM fails"""
        diagnosis = diagnosis_result['diagnosis']
        is_questionnaire_only = patient_data.get('mode') == 'questionnaire_only'
        
        prescription = {
            'medications': [],
            'lifestyle': [],
            'diet': [],
            'exercise': [],
            'monitoring': [],
            'follow_up': '',
            'warnings': [],
            'emergency_signs': [],
            'additional_notes': ''
        }
        
        if is_questionnaire_only:
            # Questionnaire-only mode - focus on screening and prevention
            prescription['medications'] = [
                'No medications prescribed - lab tests required first'
            ]
            prescription['lifestyle'] = [
                'Schedule appointment with healthcare provider',
                'Get fasting glucose and HbA1c tests',
                'Maintain healthy weight',
                'Reduce stress through relaxation techniques'
            ]
            prescription['diet'] = [
                'Reduce sugar and refined carbohydrates',
                'Eat more vegetables, fruits, and whole grains',
                'Control portion sizes',
                'Limit processed foods and sugary drinks'
            ]
            prescription['exercise'] = [
                'Aim for 150 minutes of moderate activity per week',
                'Include both cardio and strength training',
                'Start slowly if currently inactive'
            ]
            prescription['monitoring'] = [
                'Get fasting blood glucose test',
                'Get HbA1c test',
                'Monitor symptoms and track changes',
                'Regular blood pressure checks'
            ]
            prescription['follow_up'] = 'Schedule doctor appointment within 2-4 weeks for lab tests'
            prescription['warnings'] = [
                'This is a screening assessment, not a diagnosis',
                'Lab tests are essential for definitive diagnosis',
                'Do not start medications without doctor consultation'
            ]
            prescription['emergency_signs'] = [
                'Extreme thirst or frequent urination',
                'Unexplained rapid weight loss',
                'Severe fatigue or confusion',
                'Blurred vision or dizziness'
            ]
            prescription['additional_notes'] = 'This assessment is based on symptoms and risk factors. Laboratory testing is required for accurate diagnosis and treatment planning.'
            
        elif 'Diabetes' in diagnosis:
            prescription['medications'] = [
                'Metformin 500mg - Take twice daily with meals',
                'Consider insulin therapy if glucose remains uncontrolled'
            ]
            prescription['diet'] = [
                'Limit carbohydrates to 45-60g per meal',
                'Avoid sugary drinks and processed foods',
                'Increase fiber intake (vegetables, whole grains)'
            ]
            prescription['exercise'] = [
                'Walk 30 minutes daily after meals',
                'Resistance training 2-3 times per week'
            ]
            prescription['monitoring'] = [
                'Check fasting glucose daily',
                'HbA1c test every 3 months',
                'Annual kidney and eye exams'
            ]
            prescription['follow_up'] = 'Schedule appointment in 2 weeks'
            prescription['warnings'] = [
                'Watch for hypoglycemia symptoms (shakiness, sweating)',
                'Never skip meals when on medication'
            ]
            prescription['emergency_signs'] = [
                'Blood glucose > 300 mg/dL',
                'Severe confusion or loss of consciousness'
            ]
            
        elif 'Pre-diabetes' in diagnosis:
            prescription['medications'] = [
                'Metformin 500mg may be considered (consult physician)'
            ]
            prescription['diet'] = [
                'Reduce sugar and refined carbs',
                'Eat more vegetables and lean proteins',
                'Control portion sizes'
            ]
            prescription['exercise'] = [
                '150 minutes moderate activity per week',
                'Include both cardio and strength training'
            ]
            prescription['monitoring'] = [
                'HbA1c test every 6 months',
                'Monthly fasting glucose checks'
            ]
            prescription['follow_up'] = 'Schedule appointment in 3 months'
            prescription['warnings'] = [
                'Pre-diabetes is reversible with lifestyle changes'
            ]
        
        else:  # Normal or Low Risk
            prescription['lifestyle'] = [
                'Maintain balanced diet',
                'Regular physical activity',
                'Annual health checkups'
            ]
            prescription['monitoring'] = [
                'Annual fasting glucose test'
            ]
            prescription['follow_up'] = 'Annual checkup recommended'
        
        return prescription
