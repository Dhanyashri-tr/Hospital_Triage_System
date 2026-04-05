"""
Hospital Environment Module
Main OpenEnv environment with resource constraints and queue simulation
"""

import random
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from severity import SeverityCalculator, SymptomType, generate_random_patient
from reward import RewardCalculator, ActionType


class TerminationReason(Enum):
    MAX_STEPS_REACHED = "max_steps_reached"
    NO_PATIENTS_REMAINING = "no_patients_remaining"
    CRITICAL_FAILURE = "critical_failure"
    SUCCESS = "success"


@dataclass
class ResourceState:
    """Track hospital resource availability"""
    icu_beds: int
    general_beds: int
    doctors: int
    nurses: int
    
    def to_dict(self) -> Dict:
        return {
            "icu_beds": self.icu_beds,
            "general_beds": self.general_beds,
            "doctors": self.doctors,
            "nurses": self.nurses
        }


class HospitalEnv:
    """Main Hospital Triage Environment implementing OpenEnv interface"""
    
    def __init__(self, max_steps: int = 100, difficulty: str = "medium"):
        self.max_steps = max_steps
        self.difficulty = difficulty
        self.current_step = 0
        
        # Initialize components
        self.severity_calc = SeverityCalculator()
        self.reward_calc = RewardCalculator()
        
        # Environment state
        self.state_data = {}
        self.patient_queue = []
        self.treated_patients = []
        self.total_reward = 0.0
        self.reward_history = []
        
        # Resource management
        self.max_resources = self._get_initial_resources(difficulty)
        self.current_resources = ResourceState(**self.max_resources)
        
        # Termination tracking
        self.termination_reason = None
        self.done = False
        
        # Queue simulation parameters
        self.arrival_prob = self._get_arrival_probability(difficulty)
        self.emergency_prob = 0.1  # 10% chance of emergency arrival
    
    def _get_initial_resources(self, difficulty: str) -> Dict:
        """Get initial resource allocation based on difficulty"""
        if difficulty == "easy":
            return {"icu_beds": 5, "general_beds": 20, "doctors": 8, "nurses": 15}
        elif difficulty == "medium":
            return {"icu_beds": 3, "general_beds": 15, "doctors": 5, "nurses": 10}
        else:  # hard
            return {"icu_beds": 2, "general_beds": 10, "doctors": 3, "nurses": 6}
    
    def _get_arrival_probability(self, difficulty: str) -> float:
        """Get patient arrival probability based on difficulty"""
        if difficulty == "easy":
            return 0.3  # Lower arrival rate
        elif difficulty == "medium":
            return 0.5  # Medium arrival rate
        else:  # hard
            return 0.7  # High arrival rate
    
    def reset(self, task: Optional[str] = None) -> Dict:
        """Reset environment to initial state"""
        self.current_step = 0
        self.difficulty = task or self.difficulty
        self.patient_queue = []
        self.treated_patients = []
        self.total_reward = 0.0
        self.reward_history = []
        self.done = False
        self.termination_reason = None
        
        # Reset resources
        self.max_resources = self._get_initial_resources(self.difficulty)
        self.current_resources = ResourceState(**self.max_resources)
        
        # Generate initial patients
        self._generate_initial_patients()
        
        # Update state
        self._update_state()
        
        return self.state()
    
    def _generate_initial_patients(self):
        """Generate initial patient queue"""
        num_patients = random.randint(3, 7)
        for _ in range(num_patients):
            patient = generate_random_patient()
            patient["waiting_time"] = random.randint(0, 30)
            self.patient_queue.append(patient)
    
    def _simulate_patient_arrivals(self):
        """Simulate stochastic patient arrivals"""
        if random.random() < self.arrival_prob:
            # Determine number of new patients
            num_new = random.choices([1, 2, 3], weights=[0.7, 0.25, 0.05])[0]
            
            for _ in range(num_new):
                # Emergency case injection
                if random.random() < self.emergency_prob:
                    patient = self._generate_emergency_patient()
                else:
                    patient = generate_random_patient()
                
                patient["waiting_time"] = 0
                self.patient_queue.append(patient)
    
    def _generate_emergency_patient(self) -> Dict:
        """Generate high-severity emergency patient"""
        # Force high severity vitals
        patient = generate_random_patient()
        
        # Override with emergency vitals
        patient["vitals"]["spo2"] = random.uniform(85, 92)
        patient["vitals"]["systolic_bp"] = random.randint(80, 100)
        patient["vitals"]["heart_rate"] = random.randint(110, 140)
        
        # Add severe symptoms
        emergency_symptoms = [SymptomType.CHEST_PAIN, SymptomType.SHORTNESS_BREATH, 
                             SymptomType.CONFUSION, SymptomType.BLEEDING]
        patient["symptoms"] = random.sample(emergency_symptoms, random.randint(1, 3))
        
        # Recalculate severity
        severity_data = self.severity_calc.calculate_severity_score(
            patient["vitals"]["spo2"],
            patient["vitals"]["systolic_bp"], 
            patient["vitals"]["heart_rate"],
            patient["vitals"]["age"],
            [SymptomType(s) for s in patient["symptoms"]]
        )
        
        patient.update(severity_data)
        return patient
    
    def _check_resource_availability(self, action: ActionType, patient: Dict) -> Tuple[bool, Dict]:
        """Check if required resources are available"""
        resource_blocked = False
        block_reasons = []
        
        if action == ActionType.TREAT_NOW:
            triage_level = patient.get("triage_level", "GREEN")
            
            # ICU bed requirement for critical patients
            if triage_level == "RED":
                if self.current_resources.icu_beds <= 0:
                    resource_blocked = True
                    block_reasons.append("no_icu_bed")
            else:
                if self.current_resources.general_beds <= 0:
                    resource_blocked = True
                    block_reasons.append("no_general_bed")
            
            # Doctor requirement
            if self.current_resources.doctors <= 0:
                resource_blocked = True
                block_reasons.append("no_doctor")
        
        return resource_blocked, {"blocked": resource_blocked, "reasons": block_reasons}
    
    def _allocate_resources(self, action: ActionType, patient: Dict):
        """Allocate resources for treatment"""
        if action == ActionType.TREAT_NOW:
            triage_level = patient.get("triage_level", "GREEN")
            
            # Allocate bed
            if triage_level == "RED":
                self.current_resources.icu_beds -= 1
            else:
                self.current_resources.general_beds -= 1
            
            # Allocate doctor
            self.current_resources.doctors -= 1
    
    def _release_resources(self, patient: Dict):
        """Release resources when patient is discharged"""
        triage_level = patient.get("triage_level", "GREEN")
        
        # Release bed
        if triage_level == "RED":
            self.current_resources.icu_beds += 1
        else:
            self.current_resources.general_beds += 1
        
        # Release doctor
        self.current_resources.doctors += 1
    
    def _update_waiting_times(self):
        """Increment waiting times for all patients in queue"""
        for patient in self.patient_queue:
            patient["waiting_time"] += 1
    
    def _update_state(self):
        """Update current environment state"""
        current_patient = self.patient_queue[0] if self.patient_queue else None
        
        self.state_data = {
            "current_step": self.current_step,
            "current_patient": current_patient,
            "queue_length": len(self.patient_queue),
            "treated_count": len(self.treated_patients),
            "total_reward": round(self.total_reward, 3),
            "resources": self.current_resources.to_dict(),
            "max_resources": self.max_resources,
            "done": self.done,
            "termination_reason": self.termination_reason.value if self.termination_reason else None
        }
    
    def step(self, action: str) -> Tuple[Dict, float, bool, Dict]:
        """Execute one step in the environment"""
        if self.done:
            return self.state(), 0.0, True, {"error": "Environment is done"}
        
        if not self.patient_queue:
            self.done = True
            self.termination_reason = TerminationReason.NO_PATIENTS_REMAINING
            self._update_state()
            return self.state(), 0.0, True, {}
        
        # Convert action string to enum
        try:
            action_enum = ActionType(action.upper())
        except ValueError:
            return self.state(), -0.1, False, {"error": f"Invalid action: {action}"}
        
        current_patient = self.patient_queue[0]
        
        # Check resource availability
        resource_blocked, resource_info = self._check_resource_availability(action_enum, current_patient)
        
        # Calculate reward
        reward_data = self.reward_calc.calculate_total_reward(
            action_enum,
            current_patient["severity_score"],
            current_patient["triage_level"],
            current_patient["waiting_time"],
            self.current_resources.to_dict(),
            resource_blocked
        )
        
        reward = reward_data["total_reward"]
        self.total_reward += reward
        self.reward_history.append(reward)
        
        # Process action if not blocked
        if not resource_blocked and action_enum == ActionType.TREAT_NOW:
            self._allocate_resources(action_enum, current_patient)
            self.treated_patients.append(current_patient)
            self.patient_queue.pop(0)
            self._release_resources(current_patient)  # Immediate discharge for simplicity
        elif action_enum in [ActionType.MONITOR, ActionType.WAIT]:
            # Patient stays in queue
            pass
        elif resource_blocked:
            # Action blocked - patient stays in queue with penalty already applied
            pass
        
        # Update waiting times and simulate arrivals
        self._update_waiting_times()
        self._simulate_patient_arrivals()
        
        # Increment step
        self.current_step += 1
        
        # Check termination conditions
        if self.current_step >= self.max_steps:
            self.done = True
            self.termination_reason = TerminationReason.MAX_STEPS_REACHED
        elif len(self.treated_patients) >= 20:  # Success condition
            self.done = True
            self.termination_reason = TerminationReason.SUCCESS
        
        # Update state
        self._update_state()
        
        # Prepare info dict
        info = {
            "reward_breakdown": reward_data["reward_breakdown"],
            "decision_reason": reward_data["decision_reason"],
            "resource_blocked": resource_blocked,
            "no_bed_available": "no_icu_bed" in resource_info["reasons"] or "no_general_bed" in resource_info["reasons"],
            "no_doctor_available": "no_doctor" in resource_info["reasons"],
            "resource_status_message": self._get_resource_status_message(resource_blocked, resource_info),
            "patient_info": current_patient
        }
        
        return self.state(), reward, self.done, info
    
    def _get_resource_status_message(self, resource_blocked: bool, resource_info: Dict) -> str:
        """Generate resource status message"""
        if resource_blocked:
            reasons = resource_info["reasons"]
            if "no_icu_bed" in reasons:
                return "Action blocked: No ICU beds available"
            elif "no_general_bed" in reasons:
                return "Action blocked: No general beds available"
            elif "no_doctor" in reasons:
                return "Action blocked: No doctors available"
            else:
                return "Action blocked: Resource constraints"
        else:
            return f"Resources available - ICU: {self.current_resources.icu_beds}, General: {self.current_resources.general_beds}, Doctors: {self.current_resources.doctors}"
    
    def state(self) -> Dict:
        """Get current environment state"""
        return self.state_data
    
    def get_metrics(self) -> Dict:
        """Get performance metrics"""
        if not self.reward_history:
            return {"average_reward": 0, "total_reward": 0, "efficiency": 0}
        
        avg_reward = sum(self.reward_history) / len(self.reward_history)
        positive_rewards = [r for r in self.reward_history if r > 0]
        efficiency = len(positive_rewards) / len(self.reward_history) if self.reward_history else 0
        
        return {
            "average_reward": round(avg_reward, 3),
            "total_reward": round(self.total_reward, 3),
            "efficiency": round(efficiency, 3),
            "steps_completed": self.current_step,
            "patients_treated": len(self.treated_patients),
            "termination_reason": self.termination_reason.value if self.termination_reason else None
        }