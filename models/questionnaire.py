# Diabetes Risk Assessment Questionnaire
# Comprehensive questions for diabetes diagnosis

DIABETES_QUESTIONNAIRE = {
    "sections": [
        {
            "id": "basic_info",
            "title": "Basic Information",
            "questions": [
                {
                    "id": "age_range",
                    "text": "What is your age range?",
                    "type": "multiple_choice",
                    "options": [
                        {"value": "under_25", "label": "Under 25 years", "score": 0},
                        {"value": "25_34", "label": "25-34 years", "score": 1},
                        {"value": "35_44", "label": "35-44 years", "score": 2},
                        {"value": "45_54", "label": "45-54 years", "score": 3},
                        {"value": "55_64", "label": "55-64 years", "score": 4},
                        {"value": "65_plus", "label": "65+ years", "score": 5}
                    ]
                },
                {
                    "id": "weight_status",
                    "text": "How would you describe your weight status?",
                    "type": "multiple_choice",
                    "options": [
                        {"value": "underweight", "label": "Underweight", "score": 0},
                        {"value": "normal", "label": "Normal weight", "score": 0},
                        {"value": "overweight", "label": "Overweight", "score": 3},
                        {"value": "obese", "label": "Obese", "score": 5}
                    ]
                },
                {
                    "id": "waist_size",
                    "text": "What is your waist circumference?",
                    "type": "multiple_choice",
                    "options": [
                        {"value": "normal_male", "label": "Male: Less than 40 inches (102 cm)", "score": 0},
                        {"value": "high_male", "label": "Male: 40 inches (102 cm) or more", "score": 3},
                        {"value": "normal_female", "label": "Female: Less than 35 inches (88 cm)", "score": 0},
                        {"value": "high_female", "label": "Female: 35 inches (88 cm) or more", "score": 3}
                    ]
                }
            ]
        },
        {
            "id": "symptoms",
            "title": "Symptoms Assessment",
            "questions": [
                {
                    "id": "frequent_urination",
                    "text": "Do you experience frequent urination (especially at night)?",
                    "type": "yes_no",
                    "weight": 3
                },
                {
                    "id": "excessive_thirst",
                    "text": "Do you feel excessively thirsty?",
                    "type": "yes_no",
                    "weight": 3
                },
                {
                    "id": "unexplained_weight_loss",
                    "text": "Have you experienced unexplained weight loss recently?",
                    "type": "yes_no",
                    "weight": 4
                },
                {
                    "id": "increased_hunger",
                    "text": "Do you feel hungry even after eating?",
                    "type": "yes_no",
                    "weight": 2
                },
                {
                    "id": "fatigue",
                    "text": "Do you feel tired or fatigued frequently?",
                    "type": "yes_no",
                    "weight": 2
                },
                {
                    "id": "blurred_vision",
                    "text": "Have you experienced blurred vision?",
                    "type": "yes_no",
                    "weight": 3
                },
                {
                    "id": "slow_healing",
                    "text": "Do cuts or wounds take longer to heal?",
                    "type": "yes_no",
                    "weight": 3
                },
                {
                    "id": "tingling_numbness",
                    "text": "Do you experience tingling or numbness in hands or feet?",
                    "type": "yes_no",
                    "weight": 3
                },
                {
                    "id": "frequent_infections",
                    "text": "Do you get frequent infections (skin, gum, or urinary)?",
                    "type": "yes_no",
                    "weight": 2
                },
                {
                    "id": "darkened_skin",
                    "text": "Do you have darkened skin patches (especially neck, armpits)?",
                    "type": "yes_no",
                    "weight": 3
                }
            ]
        },
        {
            "id": "lifestyle",
            "title": "Lifestyle Factors",
            "questions": [
                {
                    "id": "diet_quality",
                    "text": "How would you describe your diet?",
                    "type": "multiple_choice",
                    "options": [
                        {"value": "healthy", "label": "Mostly healthy (fruits, vegetables, whole grains)", "score": 0},
                        {"value": "moderate", "label": "Moderate (mix of healthy and processed foods)", "score": 2},
                        {"value": "poor", "label": "Poor (mostly processed, high sugar/fat foods)", "score": 4}
                    ]
                },
                {
                    "id": "sugar_intake",
                    "text": "How often do you consume sugary drinks or foods?",
                    "type": "multiple_choice",
                    "options": [
                        {"value": "rarely", "label": "Rarely (less than once a week)", "score": 0},
                        {"value": "sometimes", "label": "Sometimes (2-3 times a week)", "score": 2},
                        {"value": "often", "label": "Often (daily or multiple times daily)", "score": 4}
                    ]
                },
                {
                    "id": "exercise_frequency",
                    "text": "How often do you exercise?",
                    "type": "multiple_choice",
                    "options": [
                        {"value": "regular", "label": "Regularly (4+ times per week)", "score": 0},
                        {"value": "moderate", "label": "Moderately (2-3 times per week)", "score": 1},
                        {"value": "occasional", "label": "Occasionally (once a week)", "score": 2},
                        {"value": "sedentary", "label": "Rarely or never", "score": 4}
                    ]
                },
                {
                    "id": "sleep_quality",
                    "text": "How many hours do you sleep per night on average?",
                    "type": "multiple_choice",
                    "options": [
                        {"value": "adequate", "label": "7-9 hours", "score": 0},
                        {"value": "insufficient", "label": "Less than 6 hours", "score": 2},
                        {"value": "excessive", "label": "More than 10 hours", "score": 1}
                    ]
                },
                {
                    "id": "stress_level",
                    "text": "How would you rate your stress level?",
                    "type": "multiple_choice",
                    "options": [
                        {"value": "low", "label": "Low", "score": 0},
                        {"value": "moderate", "label": "Moderate", "score": 1},
                        {"value": "high", "label": "High", "score": 3}
                    ]
                }
            ]
        },
        {
            "id": "medical_history",
            "title": "Medical History",
            "questions": [
                {
                    "id": "family_diabetes",
                    "text": "Do you have a family history of diabetes?",
                    "type": "multiple_choice",
                    "options": [
                        {"value": "none", "label": "No family history", "score": 0},
                        {"value": "distant", "label": "Distant relatives (grandparents, aunts, uncles)", "score": 2},
                        {"value": "immediate", "label": "Immediate family (parents, siblings)", "score": 4}
                    ]
                },
                {
                    "id": "gestational_diabetes",
                    "text": "Have you ever had gestational diabetes (diabetes during pregnancy)?",
                    "type": "yes_no_na",
                    "weight": 4
                },
                {
                    "id": "high_blood_pressure",
                    "text": "Do you have high blood pressure?",
                    "type": "yes_no",
                    "weight": 2
                },
                {
                    "id": "high_cholesterol",
                    "text": "Do you have high cholesterol?",
                    "type": "yes_no",
                    "weight": 2
                },
                
                {
                    "id": "previous_prediabetes",
                    "text": "Have you been previously diagnosed with pre-diabetes?",
                    "type": "yes_no",
                    "weight": 5
                }
            ]
        }
    ]
}

def calculate_questionnaire_risk_score(answers):
    """Calculate risk score from questionnaire answers"""
    total_score = 0
    max_score = 0
    
    for section in DIABETES_QUESTIONNAIRE["sections"]:
        for question in section["questions"]:
            q_id = question["id"]
            if q_id not in answers:
                continue
                
            answer = answers[q_id]
            
            if question["type"] == "yes_no":
                if answer == "yes":
                    total_score += question["weight"]
                max_score += question["weight"]
            
            elif question["type"] == "yes_no_na":
                if answer == "yes":
                    total_score += question["weight"]
                if answer != "na":
                    max_score += question["weight"]
            
            elif question["type"] == "multiple_choice":
                for option in question["options"]:
                    if option["value"] == answer:
                        total_score += option["score"]
                max_score += max([opt["score"] for opt in question["options"]])
    
    # Calculate percentage
    risk_percentage = (total_score / max_score * 100) if max_score > 0 else 0
    
    return {
        "total_score": total_score,
        "max_score": max_score,
        "risk_percentage": round(risk_percentage, 1),
        "risk_level": "High" if risk_percentage >= 60 else "Moderate" if risk_percentage >= 35 else "Low"
    }

def format_questionnaire_for_llm(answers):
    """Format questionnaire answers for LLM analysis"""
    formatted = []
    
    for section in DIABETES_QUESTIONNAIRE["sections"]:
        section_data = {
            "section": section["title"],
            "responses": []
        }
        
        for question in section["questions"]:
            q_id = question["id"]
            if q_id in answers:
                answer = answers[q_id]
                
                # Format the answer based on type
                if question["type"] == "multiple_choice":
                    for option in question["options"]:
                        if option["value"] == answer:
                            answer_text = option["label"]
                            break
                else:
                    answer_text = answer
                
                section_data["responses"].append({
                    "question": question["text"],
                    "answer": answer_text
                })
        
        if section_data["responses"]:
            formatted.append(section_data)
    
    return formatted
