class PrescriptionEngine:
    """Generate medical prescriptions based on diagnosis"""
    
    def generate_prescription(self, diagnosis, patient_data):
        """Generate personalized prescription recommendations"""
        
        prescription = {
            'medications': [],
            'lifestyle': [],
            'monitoring': [],
            'follow_up': '',
            'warnings': []
        }
        
        if 'Diabetes' in diagnosis:
            prescription['medications'] = [
                'Metformin 500mg - Take twice daily with meals',
                'Consider insulin therapy if glucose remains uncontrolled'
            ]
            prescription['lifestyle'] = [
                'Follow a low-carb, high-fiber diet',
                'Exercise 30 minutes daily (walking, swimming)',
                'Monitor blood glucose 3-4 times daily',
                'Maintain healthy weight (target BMI < 25)'
            ]
            prescription['monitoring'] = [
                'HbA1c test every 3 months',
                'Fasting glucose daily',
                'Regular kidney function tests',
                'Annual eye examination'
            ]
            prescription['follow_up'] = 'Schedule appointment in 2 weeks'
            prescription['warnings'] = [
                'Watch for hypoglycemia symptoms',
                'Seek immediate care if glucose > 300 mg/dL'
            ]
            
        elif 'Pre-diabetes' in diagnosis:
            prescription['medications'] = [
                'Metformin 500mg may be considered (consult physician)',
                'Vitamin D supplement if deficient'
            ]
            prescription['lifestyle'] = [
                'Reduce sugar and refined carbohydrate intake',
                'Exercise 150 minutes per week',
                'Lose 5-7% of body weight if overweight',
                'Increase fiber intake (vegetables, whole grains)'
            ]
            prescription['monitoring'] = [
                'HbA1c test every 6 months',
                'Fasting glucose monthly',
                'Weight tracking weekly'
            ]
            prescription['follow_up'] = 'Schedule appointment in 3 months'
            prescription['warnings'] = [
                'Pre-diabetes is reversible with lifestyle changes',
                'Monitor for symptoms: increased thirst, frequent urination'
            ]
            
        else:  # Normal
            prescription['lifestyle'] = [
                'Maintain balanced diet',
                'Regular physical activity',
                'Annual health checkups'
            ]
            prescription['monitoring'] = [
                'Annual fasting glucose test',
                'Maintain healthy weight'
            ]
            prescription['follow_up'] = 'Annual checkup recommended'
        
        # Add BMI-specific recommendations
        if patient_data['bmi'] >= 30:
            prescription['lifestyle'].insert(0, 'Weight loss program recommended (consult nutritionist)')
        
        return prescription
