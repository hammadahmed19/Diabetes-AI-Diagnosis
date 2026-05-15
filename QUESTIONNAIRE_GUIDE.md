# 📋 Diabetes Questionnaire Guide

## Overview
The comprehensive diabetes questionnaire is a **screening tool that works WITHOUT lab tests**. It's designed like a doctor's initial assessment, gathering information about symptoms, lifestyle, and medical history to evaluate diabetes risk before any laboratory testing.

## 🎯 Key Features
- ✅ **No lab tests required** - Works with symptoms and risk factors alone
- ✅ **Clinical screening approach** - Mimics doctor's initial assessment
- ✅ **AI-powered analysis** - LLM evaluates all responses comprehensively
- ✅ **Risk stratification** - Provides risk percentage and level
- ✅ **Actionable recommendations** - Suggests next steps including lab tests

## Questionnaire Sections

### 1. Basic Information (3 Questions)
Collects fundamental demographic and physical data:

**Age Range**
- Under 25 years: 0 points
- 25-34 years: 1 point
- 35-44 years: 2 points
- 45-54 years: 3 points
- 55-64 years: 4 points
- 65+ years: 5 points

**Weight Status**
- Underweight: 0 points
- Normal weight: 0 points
- Overweight: 3 points
- Obese: 5 points

**Waist Circumference**
- Male: < 40 inches (102 cm): 0 points
- Male: ≥ 40 inches (102 cm): 3 points
- Female: < 35 inches (88 cm): 0 points
- Female: ≥ 35 inches (88 cm): 3 points

### 2. Symptoms Assessment (10 Questions)
Evaluates common diabetes symptoms with weighted scoring:

| Symptom | Weight | Description |
|---------|--------|-------------|
| Frequent urination | 3 | Especially at night (nocturia) |
| Excessive thirst | 3 | Polydipsia - constant thirst |
| Unexplained weight loss | 4 | Significant weight loss without trying |
| Increased hunger | 2 | Polyphagia - eating more but still hungry |
| Fatigue | 2 | Persistent tiredness and low energy |
| Blurred vision | 3 | Vision problems or changes |
| Slow healing | 3 | Cuts and wounds take longer to heal |
| Tingling/numbness | 3 | In hands or feet (neuropathy) |
| Frequent infections | 2 | Skin, gum, or urinary infections |
| Darkened skin patches | 3 | Especially neck, armpits (acanthosis nigricans) |

### 3. Lifestyle Factors (5 Questions)
Assesses lifestyle risk factors with scored options:

**Diet Quality**
- Healthy (fruits, vegetables, whole grains): 0 points
- Moderate (mix of healthy and processed): 2 points
- Poor (mostly processed, high sugar/fat): 4 points

**Sugar Intake**
- Rarely (< once/week): 0 points
- Sometimes (2-3 times/week): 2 points
- Often (daily or multiple times): 4 points

**Exercise Frequency**
- Regular (4+ times/week): 0 points
- Moderate (2-3 times/week): 1 point
- Occasional (once/week): 2 points
- Sedentary (rarely/never): 4 points

**Sleep Quality**
- Adequate (7-9 hours): 0 points
- Insufficient (< 6 hours): 2 points
- Excessive (> 10 hours): 1 point

**Stress Level**
- Low: 0 points
- Moderate: 1 point
- High: 3 points

### 4. Medical History (6 Questions)
Evaluates medical background and risk factors:

**Family History of Diabetes**
- No family history: 0 points
- Distant relatives: 2 points
- Immediate family: 4 points

**Gestational Diabetes** (Weight: 4)
- Yes/No/Not Applicable

**High Blood Pressure** (Weight: 2)
- Yes/No

**High Cholesterol** (Weight: 2)
- Yes/No

**PCOS** (Weight: 3)
- Yes/No/Not Applicable

**Previous Pre-diabetes** (Weight: 5)
- Yes/No

## How It Works Without Lab Tests

### Traditional Approach (Requires Lab Tests)
1. Patient gets blood work done
2. Doctor reviews glucose levels, HbA1c
3. Diagnosis based on lab values

### Questionnaire Approach (No Lab Tests)
1. Patient answers comprehensive questions
2. AI analyzes symptoms + lifestyle + medical history
3. **Risk assessment** provided (not definitive diagnosis)
4. **Lab tests recommended** for confirmation

### Assessment Categories
- **High Risk for Diabetes** - Multiple severe symptoms and risk factors
- **Moderate Risk for Pre-diabetes** - Some symptoms and risk factors
- **Low Risk** - Minimal symptoms and risk factors

**Important:** All assessments recommend laboratory testing for definitive diagnosis.

## Risk Scoring System

### Calculation
- Total Score: Sum of all weighted answers
- Max Score: Maximum possible score from all questions
- Risk Percentage: (Total Score / Max Score) × 100

### Risk Levels
- **Low Risk**: < 35%
- **Moderate Risk**: 35-59%
- **High Risk**: ≥ 60%

## How the LLM Uses Questionnaire Data

The questionnaire responses are formatted and sent to the LLM along with:
1. Basic patient information (age, glucose level, BMI)
2. Calculated risk score and percentage
3. Detailed responses for each section

The LLM analyzes:
- Pattern recognition across symptoms
- Lifestyle risk factor combinations
- Medical history correlations
- Overall risk profile

This comprehensive analysis results in:
- More accurate diagnosis
- Higher confidence scores
- Better personalized recommendations
- Detailed clinical reasoning

## Benefits of Questionnaire-Only Screening

1. **Accessible**: No need for lab appointment first
2. **Immediate**: Get risk assessment instantly
3. **Comprehensive**: 23+ data points analyzed
4. **Educational**: Learn about diabetes risk factors
5. **Actionable**: Clear next steps provided
6. **Cost-effective**: Free initial screening
7. **Privacy**: No medical records needed initially

## When to Use Each Mode

### Use Questionnaire Mode When:
- ✅ No recent lab tests available
- ✅ Initial screening/self-assessment
- ✅ Checking if lab tests are warranted
- ✅ Monitoring risk factors over time
- ✅ Educational purposes

### Use Manual Entry/Upload Mode When:
- ✅ Lab test results available
- ✅ Need definitive diagnosis
- ✅ Following up on previous screening
- ✅ Doctor requested specific analysis

## Benefits Over Manual Entry

1. **Comprehensive Assessment**: 19 data points vs 6 in manual entry
2. **Symptom Tracking**: Identifies early warning signs
3. **Risk Stratification**: Quantified risk percentage
4. **Better AI Analysis**: More context for LLM reasoning
5. **Personalized Care**: Tailored recommendations based on lifestyle

## Usage Tips

1. **Be Honest**: Accurate answers lead to better diagnosis
2. **Complete All Sections**: More data = better analysis
3. **Recent Information**: Use current symptoms and habits
4. **Medical Records**: Have glucose levels and BMI ready
5. **Consult Doctor**: Use results to inform medical consultation

## API Integration

### Endpoint: `/diagnose-questionnaire`
**New endpoint specifically for questionnaire-only screening**

```json
{
  "name": "Patient Name",
  "questionnaire_answers": {
    "age_range": "45_54",
    "weight_status": "overweight",
    "waist_size": "high_male",
    "frequent_urination": "yes",
    "excessive_thirst": "yes",
    "diet_quality": "moderate",
    "exercise_frequency": "occasional",
    "family_diabetes": "immediate",
    ...
  }
}
```

### Response Includes:
```json
{
  "diagnosis": "Moderate Risk for Pre-diabetes - Lab Tests Recommended",
  "confidence": 75.5,
  "risk_level": "Moderate",
  "mode": "questionnaire_only",
  "questionnaire_risk": {
    "total_score": 45,
    "max_score": 100,
    "risk_percentage": 45.0,
    "risk_level": "Moderate"
  },
  "reasoning": "Detailed AI analysis emphasizing need for lab confirmation...",
  "recommendations": [
    "Fasting glucose test",
    "HbA1c test",
    "Consult healthcare provider"
  ],
  "prescription": {...}
}
```

### Original Endpoint: `/diagnose`
**Still available for lab test-based diagnosis**
```json
{
  "name": "Patient Name",
  "age": 45,
  "glucose_level": 130,
  "bmi": 28.5,
  "questionnaire_answers": {
    "frequent_urination": "yes",
    "excessive_thirst": "yes",
    "diet_quality": "moderate",
    "exercise_frequency": "occasional",
    "family_diabetes": "immediate",
    ...
  }
}
```

### Response Includes:
```json
{
  "diagnosis": "Pre-diabetes",
  "confidence": 87.5,
  "risk_level": "Moderate",
  "questionnaire_risk": {
    "total_score": 45,
    "max_score": 100,
    "risk_percentage": 45.0,
    "risk_level": "Moderate"
  },
  "reasoning": "Detailed AI analysis...",
  "prescription": {...}
}
```

## Medical Disclaimer

This questionnaire is a screening tool and does not replace professional medical diagnosis. Always consult with qualified healthcare providers for:
- Definitive diagnosis
- Treatment plans
- Medication management
- Ongoing care

## Future Enhancements

- [ ] Multi-language support
- [ ] Progress tracking over time
- [ ] Family history tree visualization
- [ ] Integration with wearable devices
- [ ] Dietary habit detailed analysis
- [ ] Mental health assessment
- [ ] Medication interaction checker
