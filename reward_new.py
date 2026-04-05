"""
Reward calculation system for hospital triage
Implements meaningful reward function with progress-based scoring
"""

from typing import Dict, Any
from models import ActionType, PatientData


class RewardCalculator:
    """Calculate rewards for triage decisions"""
    
    def __init__(self):
        # Reward values for different outcomes
        self.rewards = {
            'correct_critical': 1.0,      # Correctly identified critical patient
            'correct_moderate': 0.8,      # Correctly identified moderate patient
            'correct_low': 0.6,           # Correctly identified low priority patient
            'slightly_incorrect': 0.5,    # Close but not optimal
            'dangerous_wrong': 0.0,       # Dangerous incorrect decision
            'resource_penalty': -0.2,     # Resource constraint penalty
            'waiting_penalty': -0.1       # Waiting time penalty
        }
    
    def calculate_reward(self, action: ActionType, patient: PatientData, 
                        resources_available: Dict[str, int]) -> float:
        """Calculate reward for given action and patient state"""
        
        triage_level = patient.triage_level
        severity_score = patient.severity_score
        waiting_time = patient.waiting_time
        
        # Base reward based on action appropriateness
        if triage_level == "RED":
            if action == ActionType.TREAT_NOW:
                base_reward = self.rewards['correct_critical']
            elif action == ActionType.MONITOR:
                base_reward = self.rewards['dangerous_wrong']
            else:  # WAIT
                base_reward = self.rewards['dangerous_wrong']
        
        elif triage_level == "YELLOW":
            if action == ActionType.MONITOR:
                base_reward = self.rewards['correct_moderate']
            elif action == ActionType.TREAT_NOW:
                base_reward = self.rewards['slightly_incorrect']
            else:  # WAIT
                base_reward = self.rewards['slightly_incorrect']
        
        else:  # GREEN
            if action == ActionType.WAIT:
                base_reward = self.rewards['correct_low']
            elif action == ActionType.MONITOR:
                base_reward = self.rewards['slightly_incorrect']
            else:  # TREAT_NOW
                base_reward = self.rewards['slightly_incorrect']
        
        # Apply resource penalties
        resource_penalty = 0
        if action == ActionType.TREAT_NOW:
            if triage_level == "RED":
                if resources_available.get('icu_beds', 0) <= 0:
                    resource_penalty = self.rewards['resource_penalty']
            else:
                if resources_available.get('general_beds', 0) <= 0:
                    resource_penalty = self.rewards['resource_penalty']
            
            if resources_available.get('doctors', 0) <= 0:
                resource_penalty += self.rewards['resource_penalty']
        
        # Apply waiting penalties for critical patients
        waiting_penalty = 0
        if triage_level == "RED" and waiting_time > 10:
            waiting_penalty = self.rewards['waiting_penalty'] * (waiting_time / 30)
        elif triage_level == "YELLOW" and waiting_time > 30:
            waiting_penalty = self.rewards['waiting_penalty'] * ((waiting_time - 30) / 60)
        
        # Calculate final reward
        final_reward = base_reward + resource_penalty + waiting_penalty
        
        # Ensure reward is in valid range [0, 1]
        final_reward = max(0, min(1, final_reward))
        
        return round(final_reward, 2)
    
    def get_reward_explanation(self, action: ActionType, patient: PatientData, 
                              reward: float) -> str:
        """Generate explanation for reward calculation"""
        
        triage_level = patient.triage_level
        
        if triage_level == "RED" and action == ActionType.TREAT_NOW:
            return "Correctly identified critical patient requiring immediate treatment"
        elif triage_level == "RED" and action != ActionType.TREAT_NOW:
            return "Dangerous: Critical patient delayed - requires immediate treatment"
        elif triage_level == "YELLOW" and action == ActionType.MONITOR:
            return "Correctly identified moderate patient requiring observation"
        elif triage_level == "GREEN" and action == ActionType.WAIT:
            return "Correctly identified low priority patient - can wait"
        elif triage_level == "YELLOW" and action == ActionType.TREAT_NOW:
            return "Slightly incorrect: Moderate patient doesn't need immediate treatment"
        elif triage_level == "GREEN" and action == ActionType.TREAT_NOW:
            return "Slightly incorrect: Low priority patient doesn't need immediate treatment"
        else:
            return f"Action {action} for {triage_level} patient"
