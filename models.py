"""
Typed models for Hospital Triage Environment
Defines Action, Observation, and State according to OpenEnv standards
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class ActionType(str, Enum):
    """Action types for triage decisions"""
    TREAT_NOW = "TREAT_NOW"
    MONITOR = "MONITOR"
    WAIT = "WAIT"


class Action(BaseModel):
    """Action model for OpenEnv compliance"""
    action: ActionType = Field(description="Triage action to take")


class SymptomType(str, Enum):
    """Patient symptom types"""
    CHEST_PAIN = "chest_pain"
    CONFUSION = "confusion"
    SHORTNESS_BREATH = "shortness_breath"
    ABDOMINAL_PAIN = "abdominal_pain"
    HEADACHE = "headache"
    BLEEDING = "bleeding"
    FAINTING = "fainting"


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
    symptoms: List[SymptomType]
    severity_score: float = Field(ge=0, le=100, description="Severity score 0-100")
    triage_level: str = Field(description="Triage level: RED/YELLOW/GREEN")
    waiting_time: int = Field(ge=0, description="Minutes waiting")


class Observation(BaseModel):
    """Environment observation for agent"""
    patient: PatientData
    available_resources: Dict[str, int] = Field(description="Available hospital resources")
    queue_length: int = Field(ge=0, description="Number of patients waiting")
    step_count: int = Field(ge=0, description="Current step in episode")


class EnvironmentState(BaseModel):
    """Complete environment state"""
    episode_id: str
    step_count: int
    total_reward: float
    is_done: bool
    current_patient: Optional[PatientData]
    resource_status: Dict[str, Any]
    performance_metrics: Dict[str, float]


class StepResult(BaseModel):
    """Result of step() call"""
    observation: Observation
    reward: float = Field(ge=0, le=1, description="Reward for action")
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)


class ResetResult(BaseModel):
    """Result of reset() call"""
    observation: Observation
    state: EnvironmentState
