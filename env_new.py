"""
Hospital Triage Environment - OpenEnv Compliant
Implements full OpenEnv structure with reset(), step(), and state() APIs
"""

import uuid
import random
from typing import Dict, Any, Optional, Tuple
from models import (
    Action, ActionType, Observation, EnvironmentState, 
    StepResult, ResetResult, PatientData, PatientVitals, SymptomType
)
from severity import SeverityCalculator
from reward_new import RewardCalculator


class HospitalTriageEnv:
    """OpenEnv-compliant hospital triage environment"""
    
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.severity_calc = SeverityCalculator()
        self.reward_calc = RewardCalculator()
        
        # Environment state
        self.episode_id: str = ""
        self.step_count: int = 0
        self.total_reward: float = 0.0
        self.is_done: bool = False
        
        # Current patient
        self.current_patient: Optional[PatientData] = None
        
        # Resources
        self.max_resources = self._get_max_resources(difficulty)
        self.current_resources = self.max_resources.copy()
        
        # Performance tracking
        self.decisions_made = 0
        self.correct_decisions = 0
    
    def _get_max_resources(self, difficulty: str) -> Dict[str, int]:
        """Get maximum resources based on difficulty"""
        if difficulty == "easy":
            return {"icu_beds": 5, "general_beds": 20, "doctors": 8, "nurses": 15}
        elif difficulty == "medium":
            return {"icu_beds": 3, "general_beds": 15, "doctors": 5, "nurses": 10}
        else:  # hard
            return {"icu_beds": 2, "general_beds": 10, "doctors": 3, "nurses": 6}
    
    def reset(self, difficulty: Optional[str] = None) -> ResetResult:
        """Reset environment for new episode"""
        if difficulty:
            self.difficulty = difficulty
            self.max_resources = self._get_max_resources(difficulty)
        
        # Reset episode state
        self.episode_id = str(uuid.uuid4())
        self.step_count = 0
        self.total_reward = 0.0
        self.is_done = False
        self.decisions_made = 0
        self.correct_decisions = 0
        
        # Reset resources
        self.current_resources = self.max_resources.copy()
        
        # Generate new patient
        patient_data = self.severity_calc.generate_patient(self.difficulty)
        self.current_patient = PatientData(**patient_data)
        
        # Create observation
        observation = Observation(
            patient=self.current_patient,
            available_resources=self.current_resources.copy(),
            queue_length=random.randint(0, 5),
            step_count=self.step_count
        )
        
        # Create environment state
        state = EnvironmentState(
            episode_id=self.episode_id,
            step_count=self.step_count,
            total_reward=self.total_reward,
            is_done=self.is_done,
            current_patient=self.current_patient,
            resource_status={
                "available": self.current_resources,
                "max": self.max_resources,
                "utilization": {
                    k: self.max_resources[k] - v 
                    for k, v in self.current_resources.items()
                }
            },
            performance_metrics={
                "accuracy": 0.0,
                "total_decisions": 0,
                "avg_reward": 0.0
            }
        )
        
        return ResetResult(observation=observation, state=state)
    
    def step(self, action: Action) -> StepResult:
        """Execute one step in the environment"""
        if self.is_done:
            raise ValueError("Episode is done. Call reset() to start new episode.")
        
        if not self.current_patient:
            raise ValueError("No current patient. Call reset() first.")
        
        self.step_count += 1
        self.decisions_made += 1
        
        # Calculate reward
        reward = self.reward_calc.calculate_reward(
            action.action, self.current_patient, self.current_resources
        )
        
        # Check if decision was correct (for tracking)
        triage_level = self.current_patient.triage_level
        if (triage_level == "RED" and action.action == ActionType.TREAT_NOW) or \
           (triage_level == "YELLOW" and action.action == ActionType.MONITOR) or \
           (triage_level == "GREEN" and action.action == ActionType.WAIT):
            self.correct_decisions += 1
        
        self.total_reward += reward
        
        # Update resources if action was TREAT_NOW
        if action.action == ActionType.TREAT_NOW:
            if triage_level == "RED":
                if self.current_resources.get('icu_beds', 0) > 0:
                    self.current_resources['icu_beds'] -= 1
            else:
                if self.current_resources.get('general_beds', 0) > 0:
                    self.current_resources['general_beds'] -= 1
            
            if self.current_resources.get('doctors', 0) > 0:
                self.current_resources['doctors'] -= 1
        
        # Create new observation
        observation = Observation(
            patient=self.current_patient,
            available_resources=self.current_resources.copy(),
            queue_length=max(0, random.randint(0, 5) - 1),  # Simulate queue movement
            step_count=self.step_count
        )
        
        # Episode ends after one decision for simplicity
        self.is_done = True
        
        # Create info
        info = {
            "episode_id": self.episode_id,
            "step": self.step_count,
            "action_taken": action.action,
            "patient_triage": triage_level,
            "patient_severity": self.current_patient.severity_score,
            "reward_explanation": self.reward_calc.get_reward_explanation(
                action.action, self.current_patient, reward
            ),
            "resources_used": action.action == ActionType.TREAT_NOW,
            "performance": {
                "accuracy": self.correct_decisions / self.decisions_made if self.decisions_made > 0 else 0,
                "total_decisions": self.decisions_made,
                "correct_decisions": self.correct_decisions
            }
        }
        
        return StepResult(
            observation=observation,
            reward=reward,
            done=self.is_done,
            info=info
        )
    
    def state(self) -> EnvironmentState:
        """Get current environment state"""
        accuracy = self.correct_decisions / self.decisions_made if self.decisions_made > 0 else 0
        avg_reward = self.total_reward / self.step_count if self.step_count > 0 else 0
        
        return EnvironmentState(
            episode_id=self.episode_id,
            step_count=self.step_count,
            total_reward=self.total_reward,
            is_done=self.is_done,
            current_patient=self.current_patient,
            resource_status={
                "available": self.current_resources,
                "max": self.max_resources,
                "utilization": {
                    k: self.max_resources[k] - v 
                    for k, v in self.current_resources.items()
                }
            },
            performance_metrics={
                "accuracy": round(accuracy, 3),
                "total_decisions": self.decisions_made,
                "avg_reward": round(avg_reward, 3)
            }
        )
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for current episode"""
        accuracy = self.correct_decisions / self.decisions_made if self.decisions_made > 0 else 0
        avg_reward = self.total_reward / self.step_count if self.step_count > 0 else 0
        
        return {
            "episode_id": self.episode_id,
            "difficulty": self.difficulty,
            "steps": self.step_count,
            "total_reward": round(self.total_reward, 3),
            "accuracy": round(accuracy, 3),
            "decisions_made": self.decisions_made,
            "correct_decisions": self.correct_decisions,
            "avg_reward": round(avg_reward, 3)
        }
