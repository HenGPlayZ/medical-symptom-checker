# 🚀 Quick Start Guide

Get the Medical Symptom Checker running in under 5 minutes!

> **Note**: This is an educational project with limitations. Not for real medical diagnosis.

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/medical-symptom-checker.git
cd medical-symptom-checker
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

## How to Use

### 1. Enter Your Temperature
Input your body temperature in Celsius (e.g., 37.5)

### 2. Rate Your Symptoms
Use the interactive sliders to rate each symptom (0-10):
- **0** = No symptom
- **1-3** = Mild
- **4-6** = Moderate  
- **7-9** = Severe
- **10** = Extremely severe

### 3. Click "Analyze Symptoms"
The system processes your input using the diagnostic algorithm

### 4. Review Your Results
- **Overall Severity**: 0-10 scale
- **Possible Conditions**: Ranked with confidence %
- **Matched Symptoms**: What symptoms led to each diagnosis
- **Recommendations**: Medical guidance and home care

## Example Test Cases

### Test 1: Common Cold
```
Temperature: 37.2°C
Stuffy Nose: 7
Runny Nose: 6
Sneezing: 7
Sore Throat: 5
Cough: 4
```
**Expected Result**: Common Cold (high confidence)

### Test 2: Influenza
```
Temperature: 38.8°C
Fever: 9
Body Aches: 8
Fatigue: 8
Headache: 7
Cough: 6
Chills: 8
```
**Expected Result**: Influenza (high confidence)

### Test 3: COVID-19
```
Temperature: 38.2°C
Fever: 7
Cough: 8
Fatigue: 7
Loss of Taste: 9
Body Ache: 6
Difficulty Breathing: 5
```
**Expected Result**: COVID-19 (high confidence)

### Test 4: Seasonal Allergies
```
Temperature: 36.8°C
Sneezing: 8
Runny Nose: 8
Itchy Eyes: 9
Watery Eyes: 8
Stuffy Nose: 6
```
**Expected Result**: Allergies (high confidence)

## Understanding Results

### Confidence Levels
- **70-100%** = High confidence (🥇 red badge)
- **40-69%** = Medium confidence (🥈 yellow badge)
- **20-39%** = Low confidence (🥉 green badge)

### Urgency Levels
- 🔴 **Urgent** = Seek immediate medical care
- 🟡 **Warning** = Schedule doctor visit within 24-48 hours
- 🟢 **Normal** = Monitor and use home care

### Severity Score (0-10)
- **8-10**: Critical - Emergency care needed
- **5-7**: Moderate - Medical consultation recommended
- **2-4**: Mild - Monitor symptoms
- **0-1**: Very mild - Home care sufficient

## ⚠️ Important Notes

- This is an **educational tool only** - it's **not perfect** and has many limitations
- **NOT** a replacement for professional medical advice
- The system only knows 9 diseases and uses simple rule-based matching
- Accuracy depends on honest self-reporting of symptoms
- In emergencies, call emergency services immediately
- Always consult healthcare professionals for medical concerns

**This is a student project for learning - don't use it for real medical decisions!**

## Troubleshooting

**Port already in use?**
```bash
# Use a different port
flask run --port 5001
```

**Module not found?**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Explore the code in `app.py` to understand the diagnostic logic
- Check `static/script.js` for frontend implementation
- Review `templates/index.html` for UI structure

---

**Need help?** Open an issue on GitHub!

**Severity Score:**
- 0-3: Mild condition
- 4-6: Moderate condition
- 7-10: Severe condition (medical attention recommended)

### Important Notes

⚠️ **This is NOT a replacement for professional medical advice!**

- Always consult a healthcare provider for medical concerns
- Call emergency services for life-threatening symptoms
- The tool provides preliminary assessment only
- Results should not delay seeking proper medical care

### Troubleshooting

**Port Already in Use:**
```bash
# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Then run app.py again
python app.py
```

**Flask Not Found:**
```bash
pip install --upgrade flask
```

**Page Not Loading:**
- Check that app.py is running without errors
- Verify you're using http://localhost:5000 (not https)
- Try http://127.0.0.1:5000 as alternative

### Features Overview

✅ 22+ symptoms tracked across multiple categories
✅ 9 disease conditions in knowledge base
✅ Weighted symptom matching algorithm
✅ Temperature correlation analysis
✅ Critical symptom detection
✅ Multiple diagnosis ranking
✅ Personalized recommendations
✅ Mobile-responsive design
✅ Real-time severity indicators
✅ No data storage (privacy-first)

### System Requirements

- Python 3.7 or higher
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection NOT required (runs locally)
- ~50MB disk space

---

Enjoy using the Advanced Medical Symptom Checker! 🏥

