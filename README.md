# DiabetesAI

🤖 **AI-Powered** diabetes diagnosis system with intelligent test report parsing and medical assessment.

## Features

### 🔬 Professional Test Upload
- **Drag & Drop Interface** - Upload lab reports easily
- **AI-Powered OCR** - Automatically extract test values from images/PDFs
- **Smart Validation** - Verify extracted data accuracy
- **Multi-Format Support** - JPG, PNG, PDF files

### 🧠 LLM-Powered Diagnosis
- **GPT-4 Vision** - Reads and interprets lab reports
- **Clinical Reasoning** - Detailed explanation of diagnosis
- **Personalized Prescriptions** - AI-generated treatment plans
- **Risk Assessment** - Comprehensive risk factor analysis

### 📊 Manual Entry Option
- Traditional form-based data entry
- Comprehensive patient information collection
- Flexible for various use cases

## Installation

1. Install Python dependencies:
```bash
cd diabetes-diagnosis-system
pip install -r requirements.txt
```

2. Configure LLM (OpenAI):
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. Run the application:
```bash
python app.py
```

4. Open browser to: `http://localhost:5000`

## Usage

### Option 1: Upload Lab Report
1. Click "Upload Lab Report" tab
2. Drag & drop or select your test report image
3. Click "Extract Data from Report"
4. Review extracted information
5. Click "Use This Data for Diagnosis"
6. Fill in any missing details
7. Get AI-powered diagnosis and prescription

### Option 2: Manual Entry
1. Click "Manual Entry" tab
2. Fill in patient information
3. Submit for diagnosis

## Design Inspiration

Based on US healthcare portal best practices:
- Clean, professional interface
- HIPAA-compliant design patterns
- Patient-centered information display
- Accessible color schemes and typography
- Mobile-responsive layout

## Medical Guidelines

- **Normal**: Fasting glucose < 100 mg/dL
- **Pre-diabetes**: Fasting glucose 100-125 mg/dL
- **Diabetes**: Fasting glucose ≥ 126 mg/dL

## Technology Stack

- **Backend**: Flask (Python)
- **AI/ML**: OpenAI GPT-4 with Vision
- **OCR**: GPT-4 Vision for medical document parsing
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript

## Security & Privacy

- 10MB file size limit
- Secure file handling
- No permanent storage of uploaded images
- HIPAA-aware design patterns

## About DiabetesAI

DiabetesAI is an intelligent medical assistant that combines advanced AI technology with clinical guidelines to provide comprehensive diabetes assessment and personalized treatment recommendations.

## Disclaimer

DiabetesAI is for educational and demonstration purposes. Always consult qualified healthcare professionals for medical diagnosis and treatment.
