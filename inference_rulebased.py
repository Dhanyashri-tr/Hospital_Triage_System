"""
Simple Rule-Based Agent for Hospital Triage
Fallback for OpenEnv inference when LLM is not available
"""

import asyncio
import os
import textwrap
from typing import List, Optional

from models import ActionType
from env_new import HospitalTriageEnv

# Environment configuration
TASK_NAME = os.getenv("HOSPITAL_TRIAGE_TASK", "triage")
BENCHMARK = os.getenv("HOSPITAL_TRIAGE_BENCHMARK", "hospital_triage")
MAX_STEPS = 5
SUCCESS_SCORE_THRESHOLD = 0.6  # normalized score in [0, 1]

# Max possible reward: 1.0 per step
MAX_TOTAL_REWARD = MAX_STEPS * 1.0


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model=rule_based", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


def get_rule_based_action(patient_data: dict) -> str:
    """Simple rule-based triage decision"""
    triage_level = patient_data["triage_level"]
    severity_score = patient_data["severity_score"]
    waiting_time = patient_data["waiting_time"]
    
    # Critical cases
    if triage_level == "RED" or severity_score >= 60:
        return "TREAT_NOW"
    
    # Moderate cases
    elif triage_level == "YELLOW" or 30 <= severity_score < 60:
        # Consider waiting time for moderate cases
        if waiting_time > 20:
            return "TREAT_NOW"  # Been waiting too long
        else:
            return "MONITOR"
    
    # Low priority cases
    else:
        return "WAIT"


async def main() -> None:
    """Main inference loop with rule-based agent"""
    # Initialize environment
    env = HospitalTriageEnv(difficulty="medium")
    
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False
    
    log_start(task=TASK_NAME, env=BENCHMARK, model="rule_based")
    
    try:
        # Reset environment
        reset_result = env.reset()
        observation = reset_result.observation
        state = reset_result.state
        
        last_reward = 0.0
        
        print(f"[DEBUG] Episode {state.episode_id} started", flush=True)
        
        for step in range(1, MAX_STEPS + 1):
            if state.is_done:
                break
            
            # Extract patient data
            patient_data = {
                "patient_id": observation.patient.patient_id,
                "triage_level": observation.patient.triage_level,
                "severity_score": observation.patient.severity_score,
                "waiting_time": observation.patient.waiting_time,
                "vitals": {
                    "heart_rate": observation.patient.vitals.heart_rate,
                    "oxygen_saturation": observation.patient.vitals.oxygen_saturation,
                    "temperature": observation.patient.vitals.temperature,
                    "systolic_bp": observation.patient.vitals.systolic_bp,
                    "age": observation.patient.vitals.age
                },
                "symptoms": [s.value for s in observation.patient.symptoms]
            }
            
            # Get action from rule-based agent
            action_str = get_rule_based_action(patient_data)
            
            # Execute action
            from models import Action
            step_result = env.step(Action(action=ActionType(action_str)))
            
            reward = step_result.reward
            done = step_result.done
            error = None
            
            rewards.append(reward)
            steps_taken = step
            last_reward = reward
            
            # Log step
            log_step(step=step, action=action_str, reward=reward, done=done, error=error)
            
            print(f"[DEBUG] Patient {patient_data['patient_id']} - Action: {action_str}, Reward: {reward:.2f}", flush=True)
            
            # Update state
            state = env.state()
            
            if done:
                break
        
        # Calculate final score
        score = sum(rewards) / MAX_TOTAL_REWARD if MAX_TOTAL_REWARD > 0 else 0.0
        score = min(max(score, 0.0), 1.0)  # clamp to [0, 1]
        success = score >= SUCCESS_SCORE_THRESHOLD
        
        print(f"[DEBUG] Final score: {score:.3f}, Success: {success}", flush=True)
        
    except Exception as e:
        print(f"[DEBUG] Main loop error: {e}", flush=True)
        log_step(step=steps_taken+1, action="ERROR", reward=0.0, done=True, error=str(e))
        
    finally:
        # Environment cleanup (if needed)
        try:
            # No explicit close() method for our environment
            pass
        except Exception as e:
            print(f"[DEBUG] Cleanup error: {e}", flush=True)
        
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())
