"""
FastAPI server for Hospital Triage Environment
Exposes OpenEnv-compatible API endpoints
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
from contextlib import asynccontextmanager

from models import Action, ActionType, EnvironmentState, StepResult, ResetResult
from env_new import HospitalTriageEnv


# Global environment instance
env: Optional[HospitalTriageEnv] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup the environment"""
    global env
    env = HospitalTriageEnv()
    yield
    # Cleanup can be added here if needed


# Initialize FastAPI app
app = FastAPI(
    title="Hospital Triage OpenEnv API",
    description="OpenEnv-compatible hospital triage environment",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# Request models
class ResetRequest(BaseModel):
    difficulty: Optional[str] = "medium"


class StepRequest(BaseModel):
    action: ActionType


class HealthResponse(BaseModel):
    status: str


@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="ok")


@app.post("/reset", response_model=ResetResult)
async def reset_environment(request: ResetRequest):
    """Reset environment and return initial observation"""
    global env
    
    if env is None:
        env = HospitalTriageEnv()
    
    try:
        result = env.reset(difficulty=request.difficulty)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")


@app.post("/step", response_model=StepResult)
async def step_environment(request: StepRequest):
    """Execute action and return observation, reward, and done flag"""
    global env
    
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    try:
        action = Action(action=request.action)
        result = env.step(action)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step failed: {str(e)}")


@app.get("/state", response_model=EnvironmentState)
async def get_state():
    """Get current environment state"""
    global env
    
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    try:
        return env.state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get state failed: {str(e)}")


@app.get("/performance")
async def get_performance():
    """Get performance summary for current episode"""
    global env
    
    if env is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")
    
    try:
        return env.get_performance_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get performance failed: {str(e)}")


@app.get("/info")
async def get_info():
    """Get environment information"""
    return {
        "name": "Hospital Triage Environment",
        "version": "1.0.0",
        "description": "OpenEnv-compatible hospital triage decision-making environment",
        "actions": [action.value for action in ActionType],
        "difficulty_levels": ["easy", "medium", "hard"],
        "observation_space": "PatientData with vitals, symptoms, and resources",
        "reward_range": [0.0, 1.0],
        "max_episode_steps": 1
    }


# Add CORS middleware for web interface
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
