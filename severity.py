"""
Severity Score Calculation Module
Handles patient severity scoring with 0-100 normalization and weighted formula
"""

import random
from enum import Enum
from typing import Dict, List, Tuple


class SymptomType(Enum):
    CHEST_PAIN = "chest_pain"
    CONFUSION = "confusion"
    SHORTNESS_BREATH = "shortness_breath"
    ABDOMINAL_PAIN = "abdominal_pain"
    HEADACHE = "headache"
    BLEEDING = "bleeding"
    FAINTING = "fainting"


class SeverityCalculator:
    """Calculate and normalize patient severity scores (0-100)"""
    
    def __init__(self):
        # Weight factors for different vital signs
        self.weights = {
            'spo2': 25,      # Oxygen saturation - most critical
            'systolic_bp': 20, # Blood pressure
            'heart_rate': 15,  # Heart rate
            'age': 10,         # Age risk factor
            'symptoms': 30     # Symptom severity
        }
    
    def calculate_vital_score(self, spo2: float, systolic_bp: int, heart_rate: int, age: int) -> float:
        """Calculate vital signs component of severity score"""
        score = 0
        
        # SPO2 scoring (critical if <90)
        if spo2 < 85:
            score += self.weights['spo2'] * 1.0  # Maximum weight
        elif spo2 < 90:
            score += self.weights['spo2'] * 0.8
        elif spo2 < 95:
            score += self.weights['spo2'] * 0.4
        else:
            score += self.weights['spo2'] * 0.1
        
        # Systolic BP scoring (<90 critical, >180 also critical)
        if systolic_bp < 80:
            score += self.weights['systolic_bp'] * 1.0
        elif systolic_bp < 90:
            score += self.weights['systolic_bp'] * 0.7
        elif systolic_bp > 180:
            score += self.weights['systolic_bp'] * 0.6
        elif systolic_bp > 160:
            score += self.weights['systolic_bp'] * 0.3
        else:
            score += self.weights['systolic_bp'] * 0.1
        
        # Heart rate scoring (>120 critical, <50 also critical)
        if heart_rate < 40:
            score += self.weights['heart_rate'] * 1.0
        elif heart_rate < 50:
            score += self.weights['heart_rate'] * 0.6
        elif heart_rate > 130:
            score += self.weights['heart_rate'] * 0.8
        elif heart_rate > 120:
            score += self.weights['heart_rate'] * 0.7
        elif heart_rate > 100:
            score += self.weights['heart_rate'] * 0.3
        else:
            score += self.weights['heart_rate'] * 0.1
        
        # Age scoring (>65 increased risk)
        if age > 80:
            score += self.weights['age'] * 0.8
        elif age > 65:
            score += self.weights['age'] * 0.6
        elif age > 50:
            score += self.weights['age'] * 0.3
        else:
            score += self.weights['age'] * 0.1
        
        return score
    
    def calculate_symptom_score(self, symptoms: List[SymptomType]) -> float:
        """Calculate symptom component of severity score"""
        symptom_weights = {
            SymptomType.CHEST_PAIN: 0.9,
            SymptomType.CONFUSION: 0.8,
            SymptomType.SHORTNESS_BREATH: 0.7,
            SymptomType.BLEEDING: 0.8,
            SymptomType.FAINTING: 0.9,
            SymptomType.ABDOMINAL_PAIN: 0.5,
            SymptomType.HEADACHE: 0.3
        }
        
        if not symptoms:
            return self.weights['symptoms'] * 0.1  # Minimal score for no symptoms
        
        total_score = 0
        for symptom in symptoms:
            weight = symptom_weights.get(symptom, 0.3)
            total_score += self.weights['symptoms'] * weight / len(symptoms)
        
        return min(total_score, self.weights['symptoms'])
    
    def calculate_severity_score(self, spo2: float, systolic_bp: int, heart_rate: int, 
                                age: int, symptoms: List[SymptomType]) -> Dict:
        """Calculate comprehensive severity score (0-100)"""
        vital_score = self.calculate_vital_score(spo2, systolic_bp, heart_rate, age)
        symptom_score = self.calculate_symptom_score(symptoms)
        
        # Combine scores and normalize to 0-100
        raw_score = vital_score + symptom_score
        normalized_score = min(100, max(0, raw_score))
        
        # Determine triage level
        if normalized_score >= 50:
            triage_level = "RED"
        elif normalized_score >= 20:
            triage_level = "YELLOW"
        else:
            triage_level = "GREEN"
        
        return {
            "severity_score": round(normalized_score, 1),
            "triage_level": triage_level,
            "vital_component": round(vital_score, 1),
            "symptom_component": round(symptom_score, 1),
            "breakdown": {
                "spo2_score": round(self._get_spo2_score(spo2), 1),
                "bp_score": round(self._get_bp_score(systolic_bp), 1),
                "hr_score": round(self._get_hr_score(heart_rate), 1),
                "age_score": round(self._get_age_score(age), 1),
                "symptom_score_total": round(symptom_score, 1)
            }
        }
    
    def _get_spo2_score(self, spo2: float) -> float:
        if spo2 < 85:
            return self.weights['spo2'] * 1.0
        elif spo2 < 90:
            return self.weights['spo2'] * 0.8
        elif spo2 < 95:
            return self.weights['spo2'] * 0.4
        else:
            return self.weights['spo2'] * 0.1
    
    def _get_bp_score(self, systolic_bp: int) -> float:
        if systolic_bp < 80:
            return self.weights['systolic_bp'] * 1.0
        elif systolic_bp < 90:
            return self.weights['systolic_bp'] * 0.7
        elif systolic_bp > 180:
            return self.weights['systolic_bp'] * 0.6
        elif systolic_bp > 160:
            return self.weights['systolic_bp'] * 0.3
        else:
            return self.weights['systolic_bp'] * 0.1
    
    def _get_hr_score(self, heart_rate: int) -> float:
        if heart_rate < 40:
            return self.weights['heart_rate'] * 1.0
        elif heart_rate < 50:
            return self.weights['heart_rate'] * 0.6
        elif heart_rate > 130:
            return self.weights['heart_rate'] * 0.8
        elif heart_rate > 120:
            return self.weights['heart_rate'] * 0.7
        elif heart_rate > 100:
            return self.weights['heart_rate'] * 0.3
        else:
            return self.weights['heart_rate'] * 0.1
    
    def _get_age_score(self, age: int) -> float:
        if age > 80:
            return self.weights['age'] * 0.8
        elif age > 65:
            return self.weights['age'] * 0.6
        elif age > 50:
            return self.weights['age'] * 0.3
        else:
            return self.weights['age'] * 0.1


def generate_random_patient() -> Dict:
    """Generate a random patient for testing"""
    calc = SeverityCalculator()
    
    # Generate random vitals
    spo2 = random.uniform(85, 100)
    systolic_bp = random.randint(70, 180)
    heart_rate = random.randint(40, 130)
    age = random.randint(18, 90)
    
    # Generate random symptoms (more severe for higher scores)
    symptom_options = list(SymptomType)
    num_symptoms = random.choices([0, 1, 2, 3], weights=[0.3, 0.4, 0.2, 0.1])[0]
    symptoms = random.sample(symptom_options, num_symptoms)
    
    # Calculate severity
    severity_data = calc.calculate_severity_score(spo2, systolic_bp, heart_rate, age, symptoms)
    
    return {
        "patient_id": f"P{random.randint(1000, 9999)}",
        "vitals": {
            "spo2": round(spo2, 1),
            "systolic_bp": systolic_bp,
            "heart_rate": heart_rate,
            "age": age
        },
        "symptoms": [s.value for s in symptoms],
        **severity_data
    }
