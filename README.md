# 🏥 Medical Symptom Checker

An intelligent symptom diagnosis system built with Flask that analyzes symptoms and provides potential diagnoses with confidence scores and personalized recommendations.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
![Status](https://img.shields.io/badge/Status-Educational%20Project-yellow.svg)
![Not Perfect](https://img.shields.io/badge/Note-Not%20Perfect-orange.svg)

> **⚠️ DISCLAIMER**: This is an educational project created for academic purposes. It is **NOT perfect** and should **NOT** be used as a substitute for professional medical advice, diagnosis, or treatment. The diagnostic algorithm is rule-based and limited in scope. Always consult qualified healthcare professionals for any medical concerns.

> **📚 Academic Project**: This was developed as part of a Y3S1 Expert Systems course. While functional, it has limitations and is intended for learning purposes only.

## 🚀 Features

### Advanced Diagnostic Engine
- **Multi-Disease Detection**: Analyzes 9+ medical conditions including COVID-19, Influenza, Pneumonia, Strep Throat, Sinusitis, Bronchitis, Allergies, Migraines, and Common Cold
- **Weighted Symptom Analysis**: Each symptom has a disease-specific weight for accurate matching
- **Confidence Scoring**: Provides percentage-based confidence levels for each possible diagnosis
- **Temperature Correlation**: Cross-references body temperature with disease profiles
- **Critical Symptom Detection**: Automatically flags life-threatening symptoms requiring immediate care

### Comprehensive Symptom Assessment
Track 22+ different symptoms across multiple categories:
- **General**: Fever, Fatigue, Body Aches, Chills
- **Respiratory**: Cough, Difficulty Breathing, Chest Pain, Stuffy/Runny Nose, Sneezing
- **Head & Throat**: Headache, Sore Throat, Difficulty Swallowing, Facial Pain, Swollen Lymph Nodes
- **Sensory**: Loss of Taste/Smell, Watery/Itchy Eyes, Light/Sound Sensitivity
- **Other**: Nausea, Confusion

### Intelligent Recommendations
- **Immediate Actions**: Emergency care alerts for critical conditions
- **Medical Guidance**: Specific testing and consultation recommendations
- **Home Care**: Symptom-specific self-care instructions
- **Prevention**: Hygiene and preventive measures

### Professional UI/UX
- Modern, responsive design works on all devices
- Color-coded severity indicators
- Interactive sliders with real-time feedback
- Ranked diagnosis display (🥇🥈🥉)
- Animated visual cues for critical warnings
- Comprehensive result summaries

## 📋 Requirements

- Python 3.7+
- Flask 3.0+

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/medical-symptom-checker.git
   cd medical-symptom-checker
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

1. **Start the application:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Enter your symptoms:**
   - Input your current body temperature in Celsius
   - Rate each symptom from 0 (none) to 10 (severe)
   - Click "Analyze Symptoms"

4. **Review results:**
   - Overall severity score
   - Ranked list of possible conditions with confidence levels
   - Matched symptoms for each diagnosis
   - Personalized recommendations

## 🏗️ Project Structure

```
medical-symptom-checker/
├── app.py                 # Flask application with diagnostic logic
├── requirements.txt       # Python dependencies
├── LICENSE               # GPL v3 License
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
├── templates/
│   └── index.html        # Main UI template
└── static/
    ├── style.css         # Styling and animations
    └── script.js         # Client-side logic
```

## 🧠 How It Works

### 1. Symptom Collection
User inputs are collected via interactive sliders and temperature input.

### 2. Disease Matching Algorithm
```python
For each disease:
    - Calculate weighted symptom match score
    - Check temperature range correlation
    - Apply confidence adjustments
    - Filter diseases with >20% probability
```

### 3. Severity Assessment
Evaluates:
- Temperature elevation
- Critical symptom presence
- Overall symptom intensity
- Disease urgency level

### 4. Recommendation Generation
Based on:
- Top diagnosis confidence
- Critical symptom flags
- Symptom-specific care needs
- Disease-specific actions

## 🎨 Key Components

### Backend (app.py)
- **DISEASE_DATABASE**: Medical knowledge base with 9 diseases
- **calculate_disease_probability()**: Core matching algorithm
- **check_critical_symptoms()**: Emergency detection
- **generate_recommendations()**: Personalized advice
- **assess_overall_severity()**: Condition grading

### Frontend
- **Interactive Forms**: 22 symptom sliders + temperature input
- **Real-time Feedback**: Color-coded severity indicators
- **Results Dashboard**: Multiple diagnosis cards, severity metrics
- **Responsive Design**: Mobile-friendly interface

## ⚠️ Medical Disclaimer

**IMPORTANT**: This tool is for educational and informational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

- Always consult qualified healthcare professionals for medical concerns
- In emergencies, call emergency services immediately
- Do not delay seeking medical care based on this tool's output
- This system does not replace clinical examination or laboratory tests

### Known Limitations

This is an **educational project** with the following limitations:

- ❌ **Limited disease database** - Only covers 9 common conditions
- ❌ **Rule-based logic** - Not powered by machine learning or AI
- ❌ **No personalization** - Doesn't account for age, gender, medical history, or pre-existing conditions
- ❌ **Symptom overlap** - Many diseases share similar symptoms, which may lead to multiple possible diagnoses
- ❌ **Self-reported data** - Accuracy depends entirely on user input
- ❌ **No medical validation** - Not tested or approved by medical professionals
- ❌ **Educational purpose only** - Created for academic learning, not clinical use

**Use at your own risk. This is a student project, not a medical tool.**

## 🔒 Privacy & Security

- No data is stored or transmitted to external servers
- All processing happens locally
- No personal health information is retained
- Session data is cleared on page refresh

## 🚀 Production Deployment Considerations

Before deploying to production:

1. **Security**:
   - Disable Flask debug mode
   - Implement HTTPS
   - Add input validation and sanitization
   - Implement rate limiting

2. **Scalability**:
   - Use production WSGI server (Gunicorn, uWSGI)
   - Implement caching
   - Add database for analytics (optional)

3. **Legal**:
   - Consult healthcare regulations in your jurisdiction
   - Add comprehensive terms of service
   - Include proper medical disclaimers
   - Consider HIPAA compliance if storing data

4. **Monitoring**:
   - Implement error logging
   - Add usage analytics
   - Monitor system performance

## 📈 Future Enhancements

- [ ] Machine learning model integration
- [ ] Symptom duration tracking
- [ ] Patient history support
- [ ] Multi-language support
- [ ] PDF report generation
- [ ] Integration with telehealth services
- [ ] Age and gender-specific adjustments
- [ ] Drug interaction warnings

## 📸 Screenshots

![Medical Symptom Checker Interface](docs/screenshot.png)
*Interactive symptom assessment interface with real-time feedback*

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

Contributions are welcome! This is an educational project.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please ensure:
- Code is well-documented
- Medical information is accurate
- Tests are included for new features
- README is updated as needed

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

- Built as part of Y3S1 Expert Systems coursework at Norton University
- Medical symptom data compiled from reputable medical sources
- Icon and UI design inspired by modern healthcare applications

---

**Remember**: This is an educational tool and **not perfect**. Always seek professional medical advice for health concerns.

⚠️ **This project has limitations and is for learning purposes only. Use real medical services for actual health issues.**
3. Follow medical best practices
4. Cite sources for medical information

## 📞 Support

For issues or questions about the implementation, refer to the Flask documentation or Python resources.

---

**Version**: 2.0  
**Last Updated**: November 2025  
**Educational Project** - Norton University Expert Systems Course

