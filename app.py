"""
Medical Symptom Checker - Flask Application
=============================================

An intelligent symptom diagnosis system that analyzes patient symptoms and provides
potential diagnoses with confidence scores and personalized recommendations.

Features:
- Multi-disease detection (9 diseases)
- Weighted symptom analysis
- Temperature correlation
- Critical symptom detection
- Personalized recommendations

Author: Norton University - Y3S1 Expert Systems
License: GPL v3
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Disease knowledge base with weighted symptoms
DISEASE_DATABASE = {
    'COVID-19': {
        'symptoms': {
            'fever': 0.9, 'cough': 0.8, 'fatigue': 0.85, 'body_ache': 0.7,
            'sore_throat': 0.6, 'headache': 0.65, 'loss_of_taste': 0.95,
            'difficulty_breathing': 0.85, 'chest_pain': 0.7
        },
        'temp_range': (37.5, 40.0),
        'severity': 'high',
        'urgency': 'urgent',
        'description': 'COVID-19 (Coronavirus Disease)',
        'incubation': '2-14 days'
    },
    'Influenza': {
        'symptoms': {
            'fever': 0.95, 'body_ache': 0.9, 'fatigue': 0.85, 'headache': 0.8,
            'cough': 0.75, 'sore_throat': 0.6, 'chills': 0.85
        },
        'temp_range': (38.0, 40.0),
        'severity': 'high',
        'urgency': 'warning',
        'description': 'Seasonal Influenza (Flu)',
        'incubation': '1-4 days'
    },
    'Common Cold': {
        'symptoms': {
            'stuffy_nose': 0.9, 'runny_nose': 0.9, 'sore_throat': 0.7,
            'sneezing': 0.85, 'cough': 0.6, 'headache': 0.5
        },
        'temp_range': (36.5, 38.0),
        'severity': 'low',
        'urgency': 'normal',
        'description': 'Common Cold (Viral)',
        'incubation': '1-3 days'
    },
    'Strep Throat': {
        'symptoms': {
            'sore_throat': 0.95, 'fever': 0.8, 'headache': 0.7,
            'difficulty_swallowing': 0.9, 'swollen_lymph': 0.8
        },
        'temp_range': (37.8, 39.5),
        'severity': 'medium',
        'urgency': 'warning',
        'description': 'Streptococcal Pharyngitis',
        'incubation': '2-5 days'
    },
    'Sinusitis': {
        'symptoms': {
            'stuffy_nose': 0.9, 'facial_pain': 0.85, 'headache': 0.8,
            'runny_nose': 0.75, 'cough': 0.6, 'fatigue': 0.6
        },
        'temp_range': (36.5, 38.5),
        'severity': 'medium',
        'urgency': 'normal',
        'description': 'Sinus Infection',
        'incubation': '3-7 days'
    },
    'Bronchitis': {
        'symptoms': {
            'cough': 0.95, 'chest_pain': 0.7, 'fatigue': 0.75,
            'difficulty_breathing': 0.7, 'fever': 0.6, 'body_ache': 0.6
        },
        'temp_range': (37.0, 38.5),
        'severity': 'medium',
        'urgency': 'warning',
        'description': 'Acute Bronchitis',
        'incubation': '3-7 days'
    },
    'Allergies': {
        'symptoms': {
            'sneezing': 0.9, 'runny_nose': 0.9, 'itchy_eyes': 0.85,
            'stuffy_nose': 0.8, 'watery_eyes': 0.8
        },
        'temp_range': (36.0, 37.2),
        'severity': 'low',
        'urgency': 'normal',
        'description': 'Seasonal Allergies',
        'incubation': 'immediate'
    },
    'Pneumonia': {
        'symptoms': {
            'cough': 0.9, 'difficulty_breathing': 0.9, 'chest_pain': 0.85,
            'fever': 0.9, 'fatigue': 0.8, 'chills': 0.8
        },
        'temp_range': (38.5, 40.5),
        'severity': 'high',
        'urgency': 'urgent',
        'description': 'Pneumonia (Bacterial/Viral)',
        'incubation': '1-3 weeks'
    },
    'Migraine': {
        'symptoms': {
            'headache': 0.95, 'nausea': 0.8, 'sensitivity_light': 0.85,
            'sensitivity_sound': 0.8
        },
        'temp_range': (36.0, 37.5),
        'severity': 'medium',
        'urgency': 'normal',
        'description': 'Migraine Headache',
        'incubation': 'episodic'
    }
}

def calculate_disease_probability(symptoms_data, disease_info):
    """Calculate probability of disease based on symptom matching"""
    matched_score = 0
    total_possible = 0
    matched_symptoms = []

    for symptom, weight in disease_info['symptoms'].items():
        total_possible += weight * 10
        if symptom in symptoms_data and symptoms_data[symptom] > 0:
            symptom_value = symptoms_data[symptom]
            matched_score += (symptom_value * weight)
            if symptom_value >= 5:
                matched_symptoms.append(symptom.replace('_', ' ').title())

    probability = (matched_score / total_possible) * 100 if total_possible > 0 else 0
    return probability, matched_symptoms

def check_critical_symptoms(symptoms_data, temperature):
    """Check for symptoms requiring immediate medical attention"""
    critical_flags = []

    if temperature >= 40.0:
        critical_flags.append("Very high fever (≥40°C)")
    if symptoms_data.get('difficulty_breathing', 0) >= 7:
        critical_flags.append("Severe difficulty breathing")
    if symptoms_data.get('chest_pain', 0) >= 7:
        critical_flags.append("Severe chest pain")
    if temperature >= 39.4 and symptoms_data.get('headache', 0) >= 8:
        critical_flags.append("High fever with severe headache")
    if symptoms_data.get('confusion', 0) >= 5:
        critical_flags.append("Mental confusion")

    return critical_flags

def generate_recommendations(diagnoses, symptoms_data, temperature):
    """Generate personalized recommendations based on diagnosis"""
    recommendations = {
        'immediate': [],
        'medical': [],
        'home_care': [],
        'prevention': []
    }

    # Check critical symptoms first
    critical = check_critical_symptoms(symptoms_data, temperature)
    if critical:
        recommendations['immediate'].append("🚨 SEEK EMERGENCY MEDICAL CARE IMMEDIATELY")
        recommendations['immediate'].extend(critical)
        return recommendations

    # Medical recommendations
    if diagnoses and diagnoses[0]['confidence'] >= 60:
        top_disease = diagnoses[0]
        if top_disease['urgency'] == 'urgent':
            recommendations['medical'].append("Visit emergency room or urgent care within 2-4 hours")
        elif top_disease['urgency'] == 'warning':
            recommendations['medical'].append("Schedule a doctor's appointment within 24-48 hours")
            recommendations['medical'].append("Consider telehealth consultation")

        if 'COVID-19' in top_disease['disease']:
            recommendations['medical'].append("Get tested for COVID-19")
            recommendations['medical'].append("Self-isolate until results are available")
        elif 'Strep' in top_disease['disease']:
            recommendations['medical'].append("Throat culture or rapid strep test recommended")
        elif 'Pneumonia' in top_disease['disease']:
            recommendations['medical'].append("Chest X-ray may be required")

    # Temperature-based care
    if temperature >= 38.5:
        recommendations['home_care'].append(f"Take acetaminophen or ibuprofen for fever (Current: {temperature}°C)")
        recommendations['home_care'].append("Monitor temperature every 2-3 hours")
        recommendations['home_care'].append("Use cool compress on forehead")
    elif temperature >= 37.8:
        recommendations['home_care'].append("Monitor temperature regularly")

    # Symptom-specific care
    if symptoms_data.get('cough', 0) >= 6:
        recommendations['home_care'].append("Use cough suppressant or expectorant as appropriate")
        recommendations['home_care'].append("Use honey and warm liquids to soothe cough")

    if symptoms_data.get('sore_throat', 0) >= 6:
        recommendations['home_care'].append("Gargle with warm salt water 3-4 times daily")
        recommendations['home_care'].append("Use throat lozenges or sprays")

    if symptoms_data.get('stuffy_nose', 0) >= 6 or symptoms_data.get('runny_nose', 0) >= 6:
        recommendations['home_care'].append("Use saline nasal spray or rinse")
        recommendations['home_care'].append("Run a cool-mist humidifier")
        recommendations['home_care'].append("Stay well-hydrated")

    if symptoms_data.get('headache', 0) >= 6:
        recommendations['home_care'].append("Rest in a quiet, dark room")
        recommendations['home_care'].append("Apply cold/warm compress to head or neck")

    # General care
    if any(symptoms_data.get(s, 0) >= 5 for s in ['fatigue', 'body_ache', 'fever']):
        recommendations['home_care'].append("Get plenty of rest (7-9 hours)")
        recommendations['home_care'].append("Stay hydrated (8-10 glasses of water daily)")
        recommendations['home_care'].append("Eat nutritious, easily digestible foods")

    # Prevention
    recommendations['prevention'].append("Wash hands frequently for 20+ seconds")
    recommendations['prevention'].append("Avoid close contact with others if symptoms persist")
    recommendations['prevention'].append("Cover coughs and sneezes with elbow")
    recommendations['prevention'].append("Disinfect frequently touched surfaces")

    return recommendations

def assess_overall_severity(diagnoses, symptoms_data, temperature):
    """Assess overall patient condition severity"""
    severity_score = 0

    # Temperature contribution
    if temperature >= 40.0:
        severity_score += 4
    elif temperature >= 39.0:
        severity_score += 3
    elif temperature >= 38.0:
        severity_score += 2
    elif temperature >= 37.5:
        severity_score += 1

    # Symptom severity contribution
    high_severity_symptoms = ['difficulty_breathing', 'chest_pain', 'confusion']
    for symptom in high_severity_symptoms:
        if symptoms_data.get(symptom, 0) >= 7:
            severity_score += 3
        elif symptoms_data.get(symptom, 0) >= 5:
            severity_score += 2

    # General symptoms
    symptom_avg = sum(symptoms_data.values()) / len(symptoms_data) if symptoms_data else 0
    if symptom_avg >= 7:
        severity_score += 3
    elif symptom_avg >= 5:
        severity_score += 2
    elif symptom_avg >= 3:
        severity_score += 1

    # Disease confidence
    if diagnoses and diagnoses[0]['confidence'] >= 80:
        if diagnoses[0]['urgency'] == 'urgent':
            severity_score += 2
        elif diagnoses[0]['urgency'] == 'warning':
            severity_score += 1

    return min(severity_score, 10)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/diagnose', methods=['POST'])
def get_diagnosis():
    data = request.json

    try:
        # Extract and validate input
        temperature = float(data.get('temperature', 36.6))

        symptoms_data = {
            'fever': int(data.get('fever', 0)),
            'body_ache': int(data.get('body_ache', 0)),
            'headache': int(data.get('headache', 0)),
            'stuffy_nose': int(data.get('stuffy_nose', 0)),
            'runny_nose': int(data.get('runny_nose', 0)),
            'cough': int(data.get('cough', 0)),
            'fatigue': int(data.get('fatigue', 0)),
            'sore_throat': int(data.get('sore_throat', 0)),
            'difficulty_breathing': int(data.get('difficulty_breathing', 0)),
            'chest_pain': int(data.get('chest_pain', 0)),
            'loss_of_taste': int(data.get('loss_of_taste', 0)),
            'nausea': int(data.get('nausea', 0)),
            'chills': int(data.get('chills', 0)),
            'sneezing': int(data.get('sneezing', 0)),
            'watery_eyes': int(data.get('watery_eyes', 0)),
            'itchy_eyes': int(data.get('itchy_eyes', 0)),
            'facial_pain': int(data.get('facial_pain', 0)),
            'difficulty_swallowing': int(data.get('difficulty_swallowing', 0)),
            'swollen_lymph': int(data.get('swollen_lymph', 0)),
            'sensitivity_light': int(data.get('sensitivity_light', 0)),
            'sensitivity_sound': int(data.get('sensitivity_sound', 0)),
            'confusion': int(data.get('confusion', 0))
        }

        # Calculate probabilities for all diseases
        disease_matches = []
        for disease_name, disease_info in DISEASE_DATABASE.items():
            probability, matched_symptoms = calculate_disease_probability(symptoms_data, disease_info)

            # Temperature range check
            temp_match = disease_info['temp_range'][0] <= temperature <= disease_info['temp_range'][1]

            # Adjust probability based on temperature match
            if temp_match:
                probability *= 1.2
            elif abs(temperature - disease_info['temp_range'][1]) <= 1.0:
                probability *= 1.1

            probability = min(probability, 100)

            if probability >= 20:  # Only include diseases with >20% probability
                disease_matches.append({
                    'disease': disease_name,
                    'description': disease_info['description'],
                    'confidence': round(probability, 1),
                    'urgency': disease_info['urgency'],
                    'severity': disease_info['severity'],
                    'matched_symptoms': matched_symptoms,
                    'incubation': disease_info['incubation']
                })

        # Sort by confidence
        disease_matches.sort(key=lambda x: x['confidence'], reverse=True)

        # Assess overall severity
        overall_severity = assess_overall_severity(disease_matches, symptoms_data, temperature)

        # Generate recommendations
        recommendations = generate_recommendations(disease_matches, symptoms_data, temperature)

        # Calculate symptom summary
        active_symptoms = {k: v for k, v in symptoms_data.items() if v > 0}
        symptom_avg = sum(active_symptoms.values()) / len(active_symptoms) if active_symptoms else 0

        return jsonify({
            'diagnoses': disease_matches[:5],  # Top 5 matches
            'overall_severity': overall_severity,
            'symptom_average': round(symptom_avg, 1),
            'temperature': temperature,
            'active_symptom_count': len(active_symptoms),
            'recommendations': recommendations,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'critical_warning': len(recommendations.get('immediate', [])) > 0
        })

    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)

