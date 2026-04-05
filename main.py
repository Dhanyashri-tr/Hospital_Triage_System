"""
Hospital Triage System - Production Ready FastAPI App
Clean, modular, and Hugging Face compatible
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn

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

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str

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

# API Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(
        status="ok",
        message="Hospital Triage System API is running"
    )

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        message="Service is healthy"
    )

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
    return {"error": "Endpoint not found", "message": f"The path {request.url.path} was not found"}

@app.exception_handler(500)
async def internal_error(request, exc):
    """Handle 500 errors"""
    return {"error": "Internal server error", "message": "An unexpected error occurred"}

# Run the app
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=7860,
        log_level="info"
    )
