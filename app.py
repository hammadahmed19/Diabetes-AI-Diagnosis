from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Import LLM-powered models
from models.llm_diagnosis import LLMDiagnosisModel
from models.llm_prescription import LLMPrescriptionEngine
from models.test_parser import TestReportParser
from models.questionnaire import (
    DIABETES_QUESTIONNAIRE, 
    calculate_questionnaire_risk_score,
    format_questionnaire_for_llm
)

# Fallback to rule-based models if LLM not configured
try:
    from models.diagnosis_model import DiagnosisModel
    from models.prescription import PrescriptionEngine
except ImportError:
    pass

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize models based on configuration
USE_LLM = os.getenv('OPENAI_API_KEY') is not None

if USE_LLM:
    print("🤖 DiabetesAI: Using LLM-powered diagnosis and prescription")
    diagnosis_model = LLMDiagnosisModel()
    prescription_engine = LLMPrescriptionEngine()
    test_parser = TestReportParser()
else:
    print("⚙️ DiabetesAI: Using rule-based diagnosis (set OPENAI_API_KEY to use LLM)")
    diagnosis_model = DiagnosisModel()
    prescription_engine = PrescriptionEngine()
    test_parser = None

def init_db():
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  age INTEGER,
                  glucose_level REAL,
                  bmi REAL,
                  diagnosis TEXT,
                  prescription TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-questionnaire', methods=['GET'])
def get_questionnaire():
    """Return the diabetes questionnaire"""
    return jsonify(DIABETES_QUESTIONNAIRE)

@app.route('/diagnose-questionnaire', methods=['POST'])
def diagnose_questionnaire():
    """Diagnose based on questionnaire only (no lab tests required)"""
    data = request.json
    
    # Extract questionnaire answers
    questionnaire_answers = data.get('questionnaire_answers', {})
    
    if not questionnaire_answers:
        return jsonify({
            'success': False,
            'message': 'Please answer the questionnaire questions'
        }), 400
    
    # Calculate risk score from questionnaire
    questionnaire_data = {
        'risk_score': calculate_questionnaire_risk_score(questionnaire_answers),
        'formatted_answers': format_questionnaire_for_llm(questionnaire_answers)
    }
    
    # Prepare patient data for LLM (questionnaire-only mode)
    patient_data = {
        'name': data.get('name', 'Patient'),
        'questionnaire': questionnaire_data,
        'mode': 'questionnaire_only'
    }
    
    # Get diagnosis from LLM
    diagnosis_result = diagnosis_model.predict(patient_data)
    
    # Get prescription
    if USE_LLM:
        prescription = prescription_engine.generate_prescription(
            diagnosis_result,
            patient_data
        )
    else:
        prescription = prescription_engine.generate_prescription(
            diagnosis_result['diagnosis'],
            patient_data
        )
    
    response = {
        'diagnosis': diagnosis_result['diagnosis'],
        'confidence': diagnosis_result['confidence'],
        'risk_level': diagnosis_result['risk_level'],
        'reasoning': diagnosis_result.get('reasoning', ''),
        'key_factors': diagnosis_result.get('key_factors', []),
        'prescription': prescription,
        'questionnaire_risk': questionnaire_data['risk_score'],
        'llm_powered': USE_LLM,
        'mode': 'questionnaire_only'
    }
    
    return jsonify(response)

@app.route('/diagnose', methods=['POST'])
def diagnose():
    data = request.json
    
    # Extract patient data
    patient_data = {
        'name': data.get('name'),
        'age': int(data.get('age')),
        'glucose_level': float(data.get('glucose_level')),
        'bmi': float(data.get('bmi')),
        'family_history': data.get('family_history', 'no'),
        'physical_activity': data.get('physical_activity', 'moderate')
    }
    
    # Process questionnaire if provided
    questionnaire_data = None
    if 'questionnaire_answers' in data:
        questionnaire_answers = data['questionnaire_answers']
        questionnaire_data = {
            'risk_score': calculate_questionnaire_risk_score(questionnaire_answers),
            'formatted_answers': format_questionnaire_for_llm(questionnaire_answers)
        }
        patient_data['questionnaire'] = questionnaire_data
    
    # Get diagnosis
    diagnosis_result = diagnosis_model.predict(patient_data)
    
    # Get prescription
    if USE_LLM:
        prescription = prescription_engine.generate_prescription(
            diagnosis_result,
            patient_data
        )
    else:
        prescription = prescription_engine.generate_prescription(
            diagnosis_result['diagnosis'],
            patient_data
        )
    
    # Save to database
    save_patient_record(patient_data, diagnosis_result, prescription)
    
    response = {
        'diagnosis': diagnosis_result['diagnosis'],
        'confidence': diagnosis_result['confidence'],
        'risk_level': diagnosis_result['risk_level'],
        'reasoning': diagnosis_result.get('reasoning', ''),
        'key_factors': diagnosis_result.get('key_factors', []),
        'prescription': prescription,
        'llm_powered': USE_LLM
    }
    
    # Include questionnaire risk score if available
    if questionnaire_data:
        response['questionnaire_risk'] = questionnaire_data['risk_score']
    
    return jsonify(response)

def save_patient_record(patient_data, diagnosis_result, prescription):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    c.execute('''INSERT INTO patients (name, age, glucose_level, bmi, diagnosis, prescription)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (patient_data['name'], patient_data['age'], patient_data['glucose_level'],
               patient_data['bmi'], diagnosis_result['diagnosis'], str(prescription)))
    conn.commit()
    conn.close()

@app.route('/parse-test-report', methods=['POST'])
def parse_test_report():
    """Parse uploaded medical test report"""
    if not USE_LLM or test_parser is None:
        return jsonify({
            'success': False,
            'message': 'LLM features not available. Please configure OPENAI_API_KEY.'
        })
    
    if 'test_report' not in request.files:
        return jsonify({
            'success': False,
            'message': 'No file uploaded'
        })
    
    file = request.files['test_report']
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'message': 'No file selected'
        })
    
    try:
        print(f"Processing file: {file.filename}")
        
        # Parse the test report
        result = test_parser.parse_test_report(file)
        
        print(f"Parse result: {result}")
        
        if result['success']:
            # Validate extracted data
            warnings = test_parser.validate_extracted_data(result['data'])
            if warnings:
                result['warnings'] = warnings
            
            # Auto-diagnose if we have enough data
            data = result['data']
            if data.get('glucose_level') and data.get('age'):
                try:
                    # Calculate BMI if we have weight and height
                    bmi = None
                    if data.get('weight') and data.get('height'):
                        weight_kg = float(data['weight'])
                        height_m = float(data['height']) / 100  # convert cm to m
                        bmi = round(weight_kg / (height_m ** 2), 1)
                        data['bmi'] = bmi
                    
                    # Use extracted BMI or default
                    if not bmi and data.get('bmi'):
                        bmi = float(data['bmi'])
                    if not bmi:
                        bmi = 25  # default if not available
                    
                    # Prepare patient data for diagnosis
                    patient_data = {
                        'name': data.get('patient_name', 'Patient'),
                        'age': int(float(data['age'])),
                        'glucose_level': float(data['glucose_level']),
                        'bmi': float(bmi),
                        'family_history': 'no',  # default
                        'physical_activity': 'moderate'  # default
                    }
                    
                    print(f"Auto-diagnosing with data: {patient_data}")
                    
                    # Get diagnosis
                    diagnosis_result = diagnosis_model.predict(patient_data)
                    
                    # Get prescription
                    if USE_LLM:
                        prescription = prescription_engine.generate_prescription(
                            diagnosis_result,
                            patient_data
                        )
                    else:
                        prescription = prescription_engine.generate_prescription(
                            diagnosis_result['diagnosis'],
                            patient_data
                        )
                    
                    # Add diagnosis to result
                    result['auto_diagnosis'] = {
                        'diagnosis': diagnosis_result['diagnosis'],
                        'confidence': diagnosis_result['confidence'],
                        'risk_level': diagnosis_result['risk_level'],
                        'reasoning': diagnosis_result.get('reasoning', ''),
                        'key_factors': diagnosis_result.get('key_factors', []),
                        'prescription': prescription
                    }
                    
                    # Save to database
                    save_patient_record(patient_data, diagnosis_result, prescription)
                    
                except Exception as diag_error:
                    print(f"Auto-diagnosis error: {diag_error}")
                    # Continue without auto-diagnosis
                    result['auto_diagnosis_error'] = str(diag_error)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in parse_test_report endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error processing file: {str(e)}'
        })

if __name__ == '__main__':
    init_db()
    
    # Get configuration from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Starting DiabetesAI on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
