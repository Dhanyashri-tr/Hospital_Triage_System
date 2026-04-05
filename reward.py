"""
Reward Calculation Module
Handles balanced reward calculation with proper penalties and resource constraints
"""

from typing import Dict, List, Tuple
from enum import Enum


class ActionType(Enum):
    TREAT_NOW = "TREAT_NOW"
    MONITOR = "MONITOR"
    WAIT = "WAIT"


class RewardCalculator:
    """Calculate balanced rewards for triage decisions"""
    
    def __init__(self):
        # Base reward ranges (kept moderate to avoid inflation)
        self.base_rewards = {
            "correct_critical": 0.6,    # Correct TREAT_NOW for high severity
            "correct_moderate": 0.5,    # Correct MONITOR for moderate severity
            "correct_low": 0.3,         # Correct WAIT for low severity
            "incorrect_critical": -0.7,  # Wrong action for critical cases
            "incorrect_moderate": -0.5, # Wrong action for moderate cases
            "incorrect_low": -0.3,      # Wrong action for low cases
            "resource_penalty": -0.8,    # Penalty for resource constraint violations
            "waiting_penalty": -0.2,     # Penalty for excessive waiting
            "overtreatment_penalty": -0.4 # Penalty for unnecessary treatment
        }
    
    def calculate_action_reward(self, action: ActionType, severity_score: float, 
                              triage_level: str) -> float:
        """Calculate base reward for action-severity match"""
        
        if triage_level == "RED":  # severity >= 50
            if action == ActionType.TREAT_NOW:
                return self.base_rewards["correct_critical"]
            elif action == ActionType.MONITOR:
                return self.base_rewards["incorrect_critical"]
            else:  # WAIT
                return self.base_rewards["incorrect_critical"]
        
        elif triage_level == "YELLOW":  # severity 20-49
            if action == ActionType.MONITOR:
                return self.base_rewards["correct_moderate"]
            elif action == ActionType.TREAT_NOW:
                # Slight penalty for overtreatment but not as severe
                return self.base_rewards["overtreatment_penalty"]
            else:  # WAIT
                return self.base_rewards["incorrect_moderate"]
        
        else:  # GREEN - severity < 20
            if action == ActionType.WAIT:
                return self.base_rewards["correct_low"]
            elif action == ActionType.TREAT_NOW:
                return self.base_rewards["overtreatment_penalty"]
            else:  # MONITOR
                return self.base_rewards["incorrect_low"]
    
    def calculate_resource_penalty(self, action: ActionType, resources_available: Dict,
                                  resource_blocked: bool) -> float:
        """Calculate penalty for resource constraint violations"""
        
        if resource_blocked:
            return self.base_rewards["resource_penalty"]
        
        # Small bonus for efficient resource use
        if action == ActionType.TREAT_NOW:
            if resources_available.get("icu_beds", 0) > 0 and resources_available.get("doctors", 0) > 0:
                return 0.1  # Small efficiency bonus
        
        return 0.0
    
    def calculate_waiting_penalty(self, waiting_time: int, triage_level: str) -> float:
        """Calculate penalty for excessive waiting time"""
        
        penalty = 0.0
        
        if triage_level == "RED" and waiting_time > 10:
            penalty = self.base_rewards["waiting_penalty"] * (waiting_time / 30)
        elif triage_level == "YELLOW" and waiting_time > 30:
            penalty = self.base_rewards["waiting_penalty"] * ((waiting_time - 30) / 60)
        elif triage_level == "GREEN" and waiting_time > 60:
            penalty = self.base_rewards["waiting_penalty"] * ((waiting_time - 60) / 120)
        
        return min(penalty, -0.6)  # Cap the penalty
    
    def calculate_total_reward(self, action: ActionType, severity_score: float,
                             triage_level: str, waiting_time: int,
                             resources_available: Dict, resource_blocked: bool) -> Dict:
        """Calculate comprehensive reward with breakdown"""
        
        # Base action reward
        action_reward = self.calculate_action_reward(action, severity_score, triage_level)
        
        # Resource penalty
        resource_penalty = self.calculate_resource_penalty(action, resources_available, resource_blocked)
        
        # Waiting penalty
        waiting_penalty = self.calculate_waiting_penalty(waiting_time, triage_level)
        
        # Total reward
        total_reward = action_reward + resource_penalty + waiting_penalty
        
        # Ensure reward is bounded
        total_reward = max(-1.0, min(1.0, total_reward))
        
        return {
            "total_reward": round(total_reward, 3),
            "reward_breakdown": {
                "action_reward": round(action_reward, 3),
                "resource_penalty": round(resource_penalty, 3),
                "waiting_penalty": round(waiting_penalty, 3)
            },
            "decision_reason": self._get_decision_reason(action, severity_score, triage_level, 
                                                       resource_blocked, total_reward)
        }
    
    def _get_decision_reason(self, action: ActionType, severity_score: float, triage_level: str,
                           resource_blocked: bool, reward: float) -> str:
        """Generate explainable decision reasoning"""
        
        reasons = []
        
        # Action appropriateness
        if triage_level == "RED" and action == ActionType.TREAT_NOW:
            reasons.append("Correctly identified critical patient needing immediate treatment")
        elif triage_level == "RED" and action != ActionType.TREAT_NOW:
            reasons.append("Critical patient delayed - suboptimal decision")
        elif triage_level == "YELLOW" and action == ActionType.MONITOR:
            reasons.append("Appropriate monitoring for moderate severity")
        elif triage_level == "GREEN" and action == ActionType.WAIT:
            reasons.append("Appropriate waiting for low severity")
        elif action == ActionType.TREAT_NOW and triage_level in ["YELLOW", "GREEN"]:
            reasons.append("Potential overtreatment - resources may be wasted")
        
        # Resource constraints
        if resource_blocked:
            reasons.append("Action blocked by resource constraints")
        
        # Reward explanation
        if reward > 0.5:
            reasons.append("Excellent decision with positive outcome")
        elif reward > 0:
            reasons.append("Acceptable decision with minor issues")
        elif reward > -0.3:
            reasons.append("Poor decision with negative consequences")
        else:
            reasons.append("Bad decision with significant negative impact")
        
        return "; ".join(reasons) if reasons else "Standard decision process"


def calculate_reward_efficiency_score(rewards: List[float]) -> Dict:
    """Calculate efficiency metrics for a sequence of rewards"""
    
    if not rewards:
        return {"average_reward": 0, "total_reward": 0, "efficiency_score": 0}
    
    total_reward = sum(rewards)
    average_reward = total_reward / len(rewards)
    
    # Efficiency score: positive rewards vs negative rewards ratio
    positive_rewards = [r for r in rewards if r > 0]
    negative_rewards = [r for r in rewards if r < 0]
    
    if negative_rewards:
        efficiency = sum(positive_rewards) / abs(sum(negative_rewards)) if negative_rewards else 1.0
    else:
        efficiency = 1.0 if positive_rewards else 0.0
    
    return {
        "average_reward": round(average_reward, 3),
        "total_reward": round(total_reward, 3),
        "efficiency_score": round(efficiency, 3),
        "positive_decisions": len(positive_rewards),
        "negative_decisions": len(negative_rewards)
    }
