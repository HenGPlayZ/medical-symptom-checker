"""
Recommendation Engine Module
=============================

Generates personalized medical recommendations based on diagnosis and symptoms.
"""

from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """Generates personalized recommendations"""

    def __init__(self, recommendations_config: Dict[str, Any]):
        self.config = recommendations_config

    def check_critical_symptoms(
        self,
        symptoms_data: Dict[str, int],
        temperature: float
    ) -> List[str]:
        """
        Check for symptoms requiring immediate medical attention

        Args:
            symptoms_data: Dictionary of symptom severities
            temperature: Patient's temperature

        Returns:
            List of critical warning messages
        """
        critical_flags = []
        critical_config = self.config.get('critical_symptoms', {})

        # Check high fever
        if 'high_fever' in critical_config:
            threshold = critical_config['high_fever'].get('threshold', 40.0)
            if temperature >= threshold:
                critical_flags.append(critical_config['high_fever']['message'])

        # Check other critical symptoms
        for key, config in critical_config.items():
            if key == 'high_fever':
                continue

            if 'symptom' in config:
                symptom = config['symptom']
                threshold = config.get('threshold', 7)

                # Special case for fever with headache
                if key == 'fever_with_headache':
                    temp_threshold = config.get('temp_threshold', 39.4)
                    symptom_threshold = config.get('symptom_threshold', 8)
                    if (temperature >= temp_threshold and
                        symptoms_data.get(symptom, 0) >= symptom_threshold):
                        critical_flags.append(config['message'])
                else:
                    if symptoms_data.get(symptom, 0) >= threshold:
                        critical_flags.append(config['message'])

        return critical_flags

    def generate_recommendations(
        self,
        diagnoses: List[Dict[str, Any]],
        symptoms_data: Dict[str, int],
        temperature: float
    ) -> Dict[str, List[str]]:
        """
        Generate personalized recommendations

        Args:
            diagnoses: List of potential diagnoses
            symptoms_data: Symptom severity data
            temperature: Patient's temperature

        Returns:
            Dictionary with recommendation categories
        """
        recommendations = {
            'immediate': [],
            'medical': [],
            'home_care': [],
            'prevention': []
        }

        # Check for critical symptoms first
        critical = self.check_critical_symptoms(symptoms_data, temperature)
        if critical:
            recommendations['immediate'].append("🚨 SEEK EMERGENCY MEDICAL CARE IMMEDIATELY")
            recommendations['immediate'].extend(critical)
            return recommendations

        # Medical recommendations based on diagnosis
        self._add_medical_recommendations(recommendations, diagnoses)

        # Temperature-based care
        self._add_temperature_care(recommendations, temperature)

        # Symptom-specific care
        self._add_symptom_care(recommendations, symptoms_data)

        # General care recommendations
        self._add_general_care(recommendations, symptoms_data)

        # Prevention measures
        recommendations['prevention'] = self.config.get('prevention', [])

        logger.info(f"Generated {sum(len(v) for v in recommendations.values())} recommendations")
        return recommendations

    def _add_medical_recommendations(
        self,
        recommendations: Dict[str, List[str]],
        diagnoses: List[Dict[str, Any]]
    ):
        """Add medical recommendations based on diagnosis"""
        if not diagnoses or diagnoses[0]['confidence'] < 60:
            return

        top_disease = diagnoses[0]
        urgency_config = self.config.get('urgency_levels', {})

        # Add urgency-based recommendations
        if top_disease['urgency'] in urgency_config:
            urgency_info = urgency_config[top_disease['urgency']]
            if 'message' in urgency_info:
                recommendations['medical'].append(urgency_info['message'])
            elif 'messages' in urgency_info:
                recommendations['medical'].extend(urgency_info['messages'])

        # Add disease-specific recommendations
        disease_specific = self.config.get('disease_specific', {})
        disease_name = top_disease['disease']

        if disease_name in disease_specific:
            recommendations['medical'].extend(
                disease_specific[disease_name].get('medical', [])
            )

    def _add_temperature_care(
        self,
        recommendations: Dict[str, List[str]],
        temperature: float
    ):
        """Add temperature-based care recommendations"""
        temp_care = self.config.get('temperature_care', {})

        for level, config in temp_care.items():
            threshold = config.get('threshold', 100)
            if temperature >= threshold:
                for rec in config.get('recommendations', []):
                    # Replace temperature placeholder
                    rec = rec.replace('{temp}', str(temperature))
                    recommendations['home_care'].append(rec)
                break

    def _add_symptom_care(
        self,
        recommendations: Dict[str, List[str]],
        symptoms_data: Dict[str, int]
    ):
        """Add symptom-specific care recommendations"""
        symptom_care = self.config.get('symptom_care', {})

        for symptom, config in symptom_care.items():
            threshold = config.get('threshold', 6)
            if symptoms_data.get(symptom, 0) >= threshold:
                recommendations['home_care'].extend(
                    config.get('recommendations', [])
                )

    def _add_general_care(
        self,
        recommendations: Dict[str, List[str]],
        symptoms_data: Dict[str, int]
    ):
        """Add general care recommendations"""
        general_config = self.config.get('general_care', {})
        threshold = general_config.get('threshold', 5)
        check_symptoms = general_config.get('symptoms', [])

        # Check if any general symptoms are above threshold
        if any(symptoms_data.get(s, 0) >= threshold for s in check_symptoms):
            recommendations['home_care'].extend(
                general_config.get('recommendations', [])
            )

