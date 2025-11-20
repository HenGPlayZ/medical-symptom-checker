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
- JSON-based configuration
- Modular architecture

Author: Norton University - Y3S1 Expert Systems
License: GPL v3
Version: 2.0 (Production Ready)
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from config import config, DATA_DIR
from utils import DataLoader, DiagnosisEngine, RecommendationEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize data loader and engines
try:
    data_loader = DataLoader(DATA_DIR)
    disease_database = data_loader.get_diseases()
    recommendations_config = data_loader.get_recommendations_config()

    diagnosis_engine = DiagnosisEngine(disease_database)
    recommendation_engine = RecommendationEngine(recommendations_config)

    logger.info(f"Application initialized successfully in {env} mode")
    logger.info(f"Loaded {len(disease_database)} diseases from database")
except Exception as e:
    logger.error(f"Failed to initialize application: {e}")
    raise


def validate_symptom_input(data: dict) -> tuple:
    """
    Validate and extract symptom data from request

    Args:
        data: Request JSON data

    Returns:
        Tuple of (temperature, symptoms_data) or raises ValueError
    """
    try:
        temperature = float(data.get('temperature', 36.6))

        # Validate temperature range
        if not (app.config['MIN_TEMPERATURE'] <= temperature <= app.config['MAX_TEMPERATURE']):
            raise ValueError(f"Temperature must be between {app.config['MIN_TEMPERATURE']}°C and {app.config['MAX_TEMPERATURE']}°C")

        # Extract all symptoms
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

        # Validate symptom ranges (0-10)
        for symptom, value in symptoms_data.items():
            if not (0 <= value <= 10):
                raise ValueError(f"Symptom '{symptom}' must be between 0 and 10")

        return temperature, symptoms_data

    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid input data: {str(e)}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/diagnose', methods=['POST'])
def get_diagnosis():
    """
    Process symptom data and return diagnosis with recommendations

    Returns:
        JSON response with diagnoses and recommendations
    """
    try:
        # Validate and extract input data
        temperature, symptoms_data = validate_symptom_input(request.json)

        # Perform diagnosis
        diagnoses = diagnosis_engine.analyze_symptoms(
            symptoms_data,
            temperature,
            min_confidence=app.config['MIN_CONFIDENCE_THRESHOLD']
        )

        # Limit to max results
        diagnoses = diagnoses[:app.config['MAX_RESULTS']]

        # Assess overall severity
        overall_severity = diagnosis_engine.assess_overall_severity(
            diagnoses, symptoms_data, temperature
        )

        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(
            diagnoses, symptoms_data, temperature
        )

        # Calculate symptom summary
        active_symptoms = {k: v for k, v in symptoms_data.items() if v > 0}
        symptom_avg = sum(active_symptoms.values()) / len(active_symptoms) if active_symptoms else 0

        response = {
            'diagnoses': diagnoses,
            'overall_severity': overall_severity,
            'symptom_average': round(symptom_avg, 1),
            'temperature': temperature,
            'active_symptom_count': len(active_symptoms),
            'recommendations': recommendations,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'critical_warning': len(recommendations.get('immediate', [])) > 0
        }

        logger.info(f"Diagnosis completed: {len(diagnoses)} matches, severity: {overall_severity}")
        return jsonify(response)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        return jsonify({'error': 'Internal server error. Please try again.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

