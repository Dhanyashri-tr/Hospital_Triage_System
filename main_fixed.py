"""
FastAPI Main Application
Hospital OpenEnv API with /reset, /step, and /state endpoints
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import uuid
from contextlib import asynccontextmanager

from env import HospitalEnv
from severity import generate_random_patient


# Global environment instance
env: Optional[HospitalEnv] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup the environment"""
    global env
    env = HospitalEnv()
    yield
    # Cleanup can be added here if needed


# Initialize FastAPI app
app = FastAPI(
    title="Hospital OpenEnv API",
    description="AI Hospital Triage System with Resource Management",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Pydantic models for API requests/responses
class ResetRequest(BaseModel):
    task: Optional[str] = "medium"
    max_steps: Optional[int] = 100


class StepRequest(BaseModel):
    action: str  # "TREAT_NOW", "MONITOR", or "WAIT"


class StateResponse(BaseModel):
    current_step: int
    current_patient: Optional[Dict[str, Any]]
    queue_length: int
    treated_count: int
    total_reward: float
    resources: Dict[str, int]
    max_resources: Dict[str, int]
    done: bool
    termination_reason: Optional[str]


class StepResponse(BaseModel):
    state: StateResponse
    reward: float
    done: bool
    info: Dict[str, Any]


class MetricsResponse(BaseModel):
    average_reward: float
    total_reward: float
    efficiency: float
    steps_completed: int
    patients_treated: int
    termination_reason: Optional[str]


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Hospital OpenEnv API v1.1.0",
        "description": "AI Hospital Triage System with Resource Management",
        "endpoints": {
            "/reset": "POST - Reset environment with optional task difficulty",
            "/step": "POST - Execute one action step",
            "/state": "GET - Get current environment state",
            "/metrics": "GET - Get performance metrics",
            "/docs": "GET - Interactive API documentation"
        },
        "actions": ["TREAT_NOW", "MONITOR", "WAIT"],
        "difficulty_levels": ["easy", "medium", "hard"]
    }


@app.post("/reset", response_model=StateResponse)
async def reset_environment(request: ResetRequest):
    """
    Reset the environment to initial state
    
    - **task**: Difficulty level ("easy", "medium", "hard")
    - **max_steps**: Maximum number of steps before termination
    """
    global env
    
    try:
        # Create new environment instance
        env = HospitalEnv(max_steps=request.max_steps, difficulty=request.task)
        
        # Reset environment
        state = env.reset(task=request.task)
        
        return StateResponse(**state)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")


@app.post("/step", response_model=StepResponse)
async def step_environment(request: StepRequest):
    """
    Execute one action step in the environment
    
    - **action**: Action to take ("TREAT_NOW", "MONITOR", "WAIT")
    
    Returns:
    - **state**: Updated environment state
    - **reward**: Reward for the action (-1.0 to 1.0)
    - **done**: Whether environment is finished
    - **info**: Additional information including reward breakdown
    """
    global env
    
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    if env.done:
        raise HTTPException(status_code=400, detail="Environment is done. Call /reset to start new episode.")
    
    try:
        # Validate action
        valid_actions = ["TREAT_NOW", "MONITOR", "WAIT"]
        if request.action not in valid_actions:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid action. Must be one of: {valid_actions}"
            )
        
        # Execute step
        state, reward, done, info = env.step(request.action)
        
        # Enhance response with additional fields
        if state.get("current_patient"):
            info.update({
                "severity_score": state["current_patient"].get("severity_score"),
                "triage_level": state["current_patient"].get("triage_level"),
                "decision_reason": info.get("decision_reason", ""),
                "reward_breakdown": info.get("reward_breakdown", {}),
                "resource_status_message": info.get("resource_status_message", ""),
                "resource_blocked": info.get("resource_blocked", False),
                "no_bed_available": info.get("no_bed_available", False),
                "no_doctor_available": info.get("no_doctor_available", False)
            })
        
        return StepResponse(
            state=StateResponse(**state),
            reward=reward,
            done=done,
            info=info
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step failed: {str(e)}")


@app.get("/state", response_model=StateResponse)
async def get_state():
    """
    Get current environment state without taking a step
    
    Returns the complete current state including patient information,
    resource availability, and environment status.
    """
    global env
    
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    try:
        state = env.state()
        return StateResponse(**state)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get state failed: {str(e)}")


@app.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """
    Get performance metrics for the current episode
    
    Returns:
    - **average_reward**: Average reward per step
    - **total_reward**: Cumulative reward for the episode
    - **efficiency**: Ratio of positive to total decisions
    - **steps_completed**: Number of steps taken
    - **patients_treated**: Number of patients successfully treated
    - **termination_reason**: Reason for episode termination
    """
    global env
    
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    try:
        metrics = env.get_metrics()
        return MetricsResponse(**metrics)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get metrics failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global env
    
    return {
        "status": "healthy",
        "environment_initialized": env is not None,
        "environment_done": env.done if env else None,
        "version": "1.1.0"
    }


@app.get("/demo/patient")
async def generate_demo_patient():
    """
    Generate a demo patient for testing
    
    Returns a randomly generated patient with calculated severity score
    and triage level for demonstration purposes.
    """
    try:
        patient = generate_random_patient()
        return {
            "patient": patient,
            "interpretation": {
                "severity_level": "CRITICAL" if patient["severity_score"] >= 50 else 
                               "MODERATE" if patient["severity_score"] >= 20 else "LOW",
                "recommended_action": "TREAT_NOW" if patient["triage_level"] == "RED" else
                                    "MONITOR" if patient["triage_level"] == "YELLOW" else "WAIT",
                "urgency": "IMMEDIATE" if patient["triage_level"] == "RED" else
                          "OBSERVE" if patient["triage_level"] == "YELLOW" else "ROUTINE"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo patient generation failed: {str(e)}")


@app.get("/demo/scenario")
async def generate_demo_scenario():
    """
    Generate a complete demo scenario
    
    Returns a sample environment state with multiple patients
    for testing and demonstration purposes.
    """
    global env
    
    try:
        # Create a temporary environment for demo
        demo_env = HospitalEnv(max_steps=50, difficulty="medium")
        demo_env.reset()
        
        # Get current state
        state = demo_env.state()
        
        # Add sample next patients
        sample_patients = []
        for i in range(min(3, len(demo_env.patient_queue) - 1)):
            sample_patients.append(demo_env.patient_queue[i + 1])
        
        return {
            "current_state": StateResponse(**state),
            "queue_preview": sample_patients,
            "resource_status": {
                "icu_utilization": f"{(demo_env.max_resources['icu_beds'] - demo_env.current_resources.icu_beds)}/{demo_env.max_resources['icu_beds']}",
                "general_utilization": f"{(demo_env.max_resources['general_beds'] - demo_env.current_resources.general_beds)}/{demo_env.max_resources['general_beds']}",
                "doctor_utilization": f"{(demo_env.max_resources['doctors'] - demo_env.current_resources.doctors)}/{demo_env.max_resources['doctors']}"
            },
            "recommendations": {
                "if_red": "TREAT_NOW immediately - ICU bed required",
                "if_yellow": "MONITOR - general bed may be needed", 
                "if_green": "WAIT - can be deferred if resources constrained"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo scenario generation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
