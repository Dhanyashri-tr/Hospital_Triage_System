"""
Hospital Triage System - Production Ready FastAPI App
Clean, working, and Hugging Face compatible with UI
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
import json

# Initialize FastAPI app
app = FastAPI(
    title="Hospital Triage System",
    description="AI-powered patient triage priority prediction",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Pydantic models for data validation
class PatientVitals(BaseModel):
    """Patient vital signs"""
    heart_rate: int = Field(ge=30, le=200, description="Heart rate in bpm")
    oxygen_saturation: float = Field(ge=70, le=100, description="Oxygen saturation %")
    temperature: float = Field(ge=35.0, le=42.0, description="Temperature in Celsius")
    systolic_bp: int = Field(ge=60, le=200, description="Systolic blood pressure")
    age: int = Field(ge=1, le=120, description="Patient age")

class PatientData(BaseModel):
    """Complete patient information"""
    patient_id: str
    vitals: PatientVitals
    symptoms: List[str] = Field(default_factory=list)
    waiting_time: int = Field(ge=0, description="Minutes waiting")

class TriageRequest(BaseModel):
    """Request for triage prediction"""
    patient: PatientData

class TriageResponse(BaseModel):
    """Response with triage decision"""
    patient_id: str
    triage_level: str = Field(description="RED, YELLOW, or GREEN")
    severity_score: float = Field(ge=0, le=100, description="Severity score 0-100")
    recommended_action: str = Field(description="TREAT_NOW, MONITOR, or WAIT")
    priority_score: float = Field(ge=0, le=1, description="Priority score 0-1")
    explanation: str = Field(description="Reason for decision")

# Core triage logic
def calculate_severity_score(vitals: PatientVitals, symptoms: List[str]) -> float:
    """Calculate severity score from vitals and symptoms"""
    score = 0
    
    # Oxygen saturation (most critical)
    if vitals.oxygen_saturation < 85:
        score += 30
    elif vitals.oxygen_saturation < 90:
        score += 20
    elif vitals.oxygen_saturation < 95:
        score += 10
    
    # Heart rate
    if vitals.heart_rate < 40 or vitals.heart_rate > 130:
        score += 20
    elif vitals.heart_rate < 50 or vitals.heart_rate > 120:
        score += 15
    elif vitals.heart_rate > 100:
        score += 10
    
    # Blood pressure
    if vitals.systolic_bp < 80 or vitals.systolic_bp > 180:
        score += 15
    elif vitals.systolic_bp < 90 or vitals.systolic_bp > 160:
        score += 10
    
    # Temperature
    if vitals.temperature > 39.5:
        score += 10
    elif vitals.temperature > 38.5:
        score += 5
    
    # Age
    if vitals.age > 80:
        score += 10
    elif vitals.age > 65:
        score += 7
    elif vitals.age > 50:
        score += 5
    
    # Symptoms
    critical_symptoms = ['chest_pain', 'confusion', 'shortness_breath', 'bleeding', 'fainting']
    moderate_symptoms = ['abdominal_pain', 'headache']
    
    for symptom in symptoms:
        if symptom in critical_symptoms:
            score += 8
        elif symptom in moderate_symptoms:
            score += 4
    
    return min(100, max(0, score))

def determine_triage_level(severity_score: float) -> str:
    """Determine triage level from severity score"""
    if severity_score >= 60:
        return "RED"
    elif severity_score >= 30:
        return "YELLOW"
    else:
        return "GREEN"

def recommend_action(triage_level: str, waiting_time: int) -> str:
    """Recommend action based on triage level and waiting time"""
    if triage_level == "RED":
        return "TREAT_NOW"
    elif triage_level == "YELLOW":
        if waiting_time > 30:
            return "TREAT_NOW"
        else:
            return "MONITOR"
    else:  # GREEN
        return "WAIT"

def calculate_priority_score(severity_score: float) -> float:
    """Calculate priority score 0-1 from severity score"""
    return min(1.0, max(0.0, severity_score / 100))

def generate_explanation(triage_level: str, severity_score: float, symptoms: List[str]) -> str:
    """Generate explanation for triage decision"""
    if triage_level == "RED":
        return f"Critical condition detected (severity: {severity_score:.1f}). Immediate treatment required due to life-threatening symptoms."
    elif triage_level == "YELLOW":
        return f"Moderate condition (severity: {severity_score:.1f}). Close monitoring required, may need treatment if condition worsens."
    else:
        return f"Stable condition (severity: {severity_score:.1f}). Can wait, low priority for treatment."

# HTML UI Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏥 Hospital Triage System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .form-container {
            padding: 40px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .form-group input, .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: #3498db;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
        }
        
        .symptoms-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }
        
        .symptom-checkbox {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .symptom-checkbox input {
            width: auto;
            margin-right: 8px;
        }
        
        .submit-btn {
            width: 100%;
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
            color: white;
            border: none;
            padding: 15px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
        }
        
        .submit-btn:disabled {
            background: #95a5a6;
            cursor: not-allowed;
            transform: none;
        }
        
        .result-container {
            margin-top: 30px;
            padding: 25px;
            border-radius: 10px;
            display: none;
        }
        
        .result-red {
            background: #ffebee;
            border-left: 5px solid #e74c3c;
        }
        
        .result-yellow {
            background: #fff8e1;
            border-left: 5px solid #f39c12;
        }
        
        .result-green {
            background: #e8f5e8;
            border-left: 5px solid #27ae60;
        }
        
        .result-title {
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        .result-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .result-item {
            padding: 10px;
            background: rgba(255,255,255,0.7);
            border-radius: 5px;
        }
        
        .result-item strong {
            color: #2c3e50;
        }
        
        .explanation {
            padding: 15px;
            background: rgba(255,255,255,0.9);
            border-radius: 5px;
            line-height: 1.6;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            font-size: 18px;
            color: #3498db;
        }
        
        .error {
            background: #ffebee;
            color: #e74c3c;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 Hospital Triage System</h1>
            <p>AI-Powered Patient Priority Assessment</p>
        </div>
        
        <div class="form-container">
            <form id="triageForm">
                <div class="form-group">
                    <label for="patientId">Patient ID</label>
                    <input type="text" id="patientId" value="P1001" required>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="age">Age</label>
                        <input type="number" id="age" min="1" max="120" value="45" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="heartRate">Heart Rate (bpm)</label>
                        <input type="number" id="heartRate" min="30" max="200" value="85" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="oxygen">Oxygen Saturation (%)</label>
                        <input type="number" id="oxygen" min="70" max="100" step="0.1" value="92" required>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="temperature">Temperature (°C)</label>
                        <input type="number" id="temperature" min="35" max="42" step="0.1" value="37.5" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="bloodPressure">Systolic BP</label>
                        <input type="number" id="bloodPressure" min="60" max="200" value="120" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="waitingTime">Waiting Time (min)</label>
                        <input type="number" id="waitingTime" min="0" value="5" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Symptoms</label>
                    <div class="symptoms-container">
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="chestPain" value="chest_pain">
                            <label for="chestPain">Chest Pain</label>
                        </div>
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="confusion" value="confusion">
                            <label for="confusion">Confusion</label>
                        </div>
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="shortnessBreath" value="shortness_breath">
                            <label for="shortnessBreath">Shortness of Breath</label>
                        </div>
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="bleeding" value="bleeding">
                            <label for="bleeding">Bleeding</label>
                        </div>
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="fainting" value="fainting">
                            <label for="fainting">Fainting</label>
                        </div>
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="abdominalPain" value="abdominal_pain">
                            <label for="abdominalPain">Abdominal Pain</label>
                        </div>
                        <div class="symptom-checkbox">
                            <input type="checkbox" id="headache" value="headache">
                            <label for="headache">Headache</label>
                        </div>
                    </div>
                </div>
                
                <button type="submit" class="submit-btn" id="submitBtn">
                    🚀 Assess Patient Priority
                </button>
            </form>
            
            <div id="loading" class="loading" style="display: none;">
                ⏳ Analyzing patient data...
            </div>
            
            <div id="error" class="error" style="display: none;"></div>
            
            <div id="result" class="result-container">
                <div class="result-title" id="resultTitle"></div>
                <div class="result-details">
                    <div class="result-item">
                        <strong>Triage Level:</strong> <span id="triageLevel"></span>
                    </div>
                    <div class="result-item">
                        <strong>Severity Score:</strong> <span id="severityScore"></span>/100
                    </div>
                    <div class="result-item">
                        <strong>Recommended Action:</strong> <span id="recommendedAction"></span>
                    </div>
                    <div class="result-item">
                        <strong>Priority Score:</strong> <span id="priorityScore"></span>
                    </div>
                </div>
                <div class="explanation" id="explanation"></div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('triageForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error').style.display = 'none';
            document.getElementById('result').style.display = 'none';
            document.getElementById('submitBtn').disabled = true;
            
            // Collect symptoms
            const symptoms = [];
            const symptomCheckboxes = document.querySelectorAll('.symptom-checkbox input:checked');
            symptomCheckboxes.forEach(checkbox => {
                symptoms.push(checkbox.value);
            });
            
            // Prepare data
            const patientData = {
                patient: {
                    patient_id: document.getElementById('patientId').value,
                    vitals: {
                        age: parseInt(document.getElementById('age').value),
                        heart_rate: parseInt(document.getElementById('heartRate').value),
                        oxygen_saturation: parseFloat(document.getElementById('oxygen').value),
                        temperature: parseFloat(document.getElementById('temperature').value),
                        systolic_bp: parseInt(document.getElementById('bloodPressure').value)
                    },
                    symptoms: symptoms,
                    waiting_time: parseInt(document.getElementById('waitingTime').value)
                }
            };
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(patientData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    // Hide loading
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('submitBtn').disabled = false;
                    
                    // Show results
                    const resultDiv = document.getElementById('result');
                    resultDiv.style.display = 'block';
                    
                    // Set result class based on triage level
                    resultDiv.className = 'result-container result-' + result.triage_level.toLowerCase();
                    
                    // Fill result data
                    document.getElementById('resultTitle').textContent = '🏥 Triage Assessment Complete';
                    document.getElementById('triageLevel').textContent = result.triage_level;
                    document.getElementById('severityScore').textContent = result.severity_score;
                    document.getElementById('recommendedAction').textContent = result.recommended_action;
                    document.getElementById('priorityScore').textContent = result.priority_score;
                    document.getElementById('explanation').textContent = result.explanation;
                } else {
                    throw new Error(result.detail || 'Prediction failed');
                }
            } catch (error) {
                // Hide loading
                document.getElementById('loading').style.display = 'none';
                document.getElementById('submitBtn').disabled = false;
                
                // Show error
                document.getElementById('error').textContent = '❌ Error: ' + error.message;
                document.getElementById('error').style.display = 'block';
            }
        });
    </script>
</body>
</html>
"""

# API Endpoints
@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with HTML UI"""
    return HTMLResponse(content=HTML_TEMPLATE)

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok", "message": "Hospital Triage System is running"}

@app.post("/predict", response_model=TriageResponse)
async def predict_triage(request: TriageRequest):
    """Predict triage priority for patient"""
    try:
        # Calculate severity score
        severity_score = calculate_severity_score(request.patient.vitals, request.patient.symptoms)
        
        # Determine triage level
        triage_level = determine_triage_level(severity_score)
        
        # Recommend action
        recommended_action = recommend_action(triage_level, request.patient.waiting_time)
        
        # Calculate priority score
        priority_score = calculate_priority_score(severity_score)
        
        # Generate explanation
        explanation = generate_explanation(triage_level, severity_score, request.patient.symptoms)
        
        return TriageResponse(
            patient_id=request.patient.patient_id,
            triage_level=triage_level,
            severity_score=round(severity_score, 1),
            recommended_action=recommended_action,
            priority_score=round(priority_score, 3),
            explanation=explanation
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/info")
async def get_info():
    """Get API information"""
    return {
        "name": "Hospital Triage System",
        "version": "1.0.0",
        "description": "AI-powered patient triage priority prediction",
        "endpoints": {
            "predict": "POST /predict - Get triage prediction",
            "health": "GET /health - Health check",
            "docs": "/docs - API documentation"
        },
        "triage_levels": ["RED", "YELLOW", "GREEN"],
        "actions": ["TREAT_NOW", "MONITOR", "WAIT"],
        "severity_range": [0, 100],
        "priority_range": [0, 1]
    }

# Error handlers
@app.exception_handler(404)
async def not_found(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "message": f"The path {request.url.path} was not found"}
    )

@app.exception_handler(500)
async def internal_error(request, exc):
    """Handle 500 errors"""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": "An unexpected error occurred"}
    )

# Run app
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7860,
        log_level="info"
    )
