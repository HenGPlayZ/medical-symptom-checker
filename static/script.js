// All symptoms to track
const symptoms = [
    'fever', 'body_ache', 'headache', 'stuffy_nose', 'runny_nose', 'cough', 
    'fatigue', 'sore_throat', 'difficulty_breathing', 'chest_pain', 'loss_of_taste',
    'nausea', 'chills', 'sneezing', 'watery_eyes', 'itchy_eyes', 'facial_pain',
    'difficulty_swallowing', 'swollen_lymph', 'sensitivity_light', 'sensitivity_sound', 
    'confusion'
];

// Update slider values dynamically
symptoms.forEach(symptom => {
    const slider = document.getElementById(symptom);
    const valueDisplay = document.getElementById(`${symptom}-value`);
    
    if (slider && valueDisplay) {
        slider.addEventListener('input', function() {
            valueDisplay.textContent = this.value;
            updateValueColor(valueDisplay, this.value);
        });
    }
});

function updateValueColor(element, value) {
    const val = parseInt(value);
    if (val >= 7) {
        element.style.color = '#ef4444';
    } else if (val >= 4) {
        element.style.color = '#f59e0b';
    } else {
        element.style.color = '#2563eb';
    }
}

// Handle form submission
document.getElementById('symptomForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        temperature: parseFloat(document.getElementById('temperature').value)
    };
    
    // Collect all symptom values
    symptoms.forEach(symptom => {
        const element = document.getElementById(symptom);
        formData[symptom] = element ? parseInt(element.value) : 0;
    });
    
    // Show loading state
    const submitBtn = e.target.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = '🔍 Analyzing...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/diagnose', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResults(result);
        } else {
            alert('Error: ' + (result.error || 'Something went wrong'));
        }
    } catch (error) {
        alert('Error connecting to server: ' + error.message);
    } finally {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
});

// Display comprehensive results
function displayResults(result) {
    const resultsDiv = document.getElementById('results');
    
    // Show results section
    resultsDiv.classList.remove('hidden');
    
    // Update timestamp
    document.getElementById('timestamp').textContent = result.timestamp;
    
    // Handle critical warning
    const criticalWarning = document.getElementById('critical-warning');
    const criticalList = document.getElementById('critical-list');
    
    if (result.critical_warning && result.recommendations.immediate) {
        criticalWarning.classList.remove('hidden');
        criticalList.innerHTML = '';
        result.recommendations.immediate.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            criticalList.appendChild(li);
        });
    } else {
        criticalWarning.classList.add('hidden');
    }
    
    // Update summary cards
    updateSummaryCards(result);
    
    // Display diagnoses
    displayDiagnoses(result.diagnoses);
    
    // Display recommendations
    displayRecommendations(result.recommendations);
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function updateSummaryCards(result) {
    // Severity score
    const severityScore = document.getElementById('severity-score');
    const severityFill = document.getElementById('severity-fill');
    
    severityScore.textContent = `${result.overall_severity}/10`;
    severityFill.style.width = `${result.overall_severity * 10}%`;
    
    if (result.overall_severity >= 7) {
        severityFill.style.background = '#ef4444';
        severityScore.style.color = '#ef4444';
    } else if (result.overall_severity >= 4) {
        severityFill.style.background = '#f59e0b';
        severityScore.style.color = '#f59e0b';
    } else {
        severityFill.style.background = '#10b981';
        severityScore.style.color = '#10b981';
    }
    
    // Active symptoms count
    document.getElementById('symptom-count').textContent = result.active_symptom_count;
    
    // Temperature
    const tempDisplay = document.getElementById('temp-display');
    tempDisplay.textContent = `${result.temperature}°C`;
    if (result.temperature >= 38.5) {
        tempDisplay.style.color = '#ef4444';
    } else if (result.temperature >= 37.5) {
        tempDisplay.style.color = '#f59e0b';
    } else {
        tempDisplay.style.color = '#10b981';
    }
}

function displayDiagnoses(diagnoses) {
    const diagnosisList = document.getElementById('diagnosis-list');
    diagnosisList.innerHTML = '';
    
    if (!diagnoses || diagnoses.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'diagnosis-card normal';
        noResults.innerHTML = `
            <div class="diagnosis-header">
                <div class="diagnosis-name">No specific condition detected</div>
            </div>
            <p class="diagnosis-description">Symptoms are minimal. Continue to monitor your condition.</p>
        `;
        diagnosisList.appendChild(noResults);
        return;
    }
    
    diagnoses.forEach((diagnosis, index) => {
        const card = document.createElement('div');
        card.className = `diagnosis-card ${diagnosis.urgency}`;
        
        const confidenceClass = diagnosis.confidence >= 70 ? 'high' : 
                               diagnosis.confidence >= 40 ? 'medium' : 'low';
        
        let matchedSymptomsHtml = '';
        if (diagnosis.matched_symptoms && diagnosis.matched_symptoms.length > 0) {
            matchedSymptomsHtml = `
                <div class="matched-symptoms">
                    <strong>Matched Symptoms:</strong><br>
                    ${diagnosis.matched_symptoms.map(s => `<span class="symptom-tag">${s}</span>`).join('')}
                </div>
            `;
        }
        
        const rankBadge = index === 0 ? '🥇 ' : index === 1 ? '🥈 ' : index === 2 ? '🥉 ' : '';
        
        card.innerHTML = `
            <div class="diagnosis-header">
                <div class="diagnosis-name">${rankBadge}${diagnosis.disease}</div>
                <span class="confidence-badge ${confidenceClass}">${diagnosis.confidence}% Match</span>
            </div>
            <p class="diagnosis-description">
                ${diagnosis.description} • Incubation: ${diagnosis.incubation}
            </p>
            ${matchedSymptomsHtml}
        `;
        
        diagnosisList.appendChild(card);
    });
}

function displayRecommendations(recommendations) {
    // Medical recommendations
    const medicalRec = document.getElementById('medical-rec');
    const medicalList = document.getElementById('medical-list');
    
    if (recommendations.medical && recommendations.medical.length > 0) {
        medicalRec.classList.remove('hidden');
        medicalList.innerHTML = '';
        recommendations.medical.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            medicalList.appendChild(li);
        });
    } else {
        medicalRec.classList.add('hidden');
    }
    
    // Home care recommendations
    const homecareRec = document.getElementById('homecare-rec');
    const homecareList = document.getElementById('homecare-list');
    
    if (recommendations.home_care && recommendations.home_care.length > 0) {
        homecareRec.classList.remove('hidden');
        homecareList.innerHTML = '';
        recommendations.home_care.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            homecareList.appendChild(li);
        });
    } else {
        homecareRec.classList.add('hidden');
    }
    
    // Prevention recommendations
    const preventionRec = document.getElementById('prevention-rec');
    const preventionList = document.getElementById('prevention-list');
    
    if (recommendations.prevention && recommendations.prevention.length > 0) {
        preventionRec.classList.remove('hidden');
        preventionList.innerHTML = '';
        recommendations.prevention.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            preventionList.appendChild(li);
        });
    } else {
        preventionRec.classList.add('hidden');
    }
}

// Reset form
document.getElementById('reset-btn').addEventListener('click', function() {
    document.getElementById('symptomForm').reset();
    document.getElementById('results').classList.add('hidden');
    
    // Reset temperature to default
    document.getElementById('temperature').value = '36.6';
    
    // Reset all slider value displays
    symptoms.forEach(symptom => {
        const element = document.getElementById(symptom);
        const valueDisplay = document.getElementById(`${symptom}-value`);
        if (element && valueDisplay) {
            element.value = '0';
            valueDisplay.textContent = '0';
            valueDisplay.style.color = '#2563eb';
        }
    });
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

