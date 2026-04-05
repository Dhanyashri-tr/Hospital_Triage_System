"""
Hospital Triage Environment - OpenEnv Inference Script
Meta PyTorch Hackathon Compliant
"""

import asyncio
import os
import textwrap
from typing import List, Optional

from openai import OpenAI

from models import ActionType
from env_new import HospitalTriageEnv

# Environment configuration
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
TASK_NAME = os.getenv("HOSPITAL_TRIAGE_TASK", "triage")
BENCHMARK = os.getenv("HOSPITAL_TRIAGE_BENCHMARK", "hospital_triage")
MAX_STEPS = 5
TEMPERATURE = 0.3
MAX_TOKENS = 100
SUCCESS_SCORE_THRESHOLD = 0.6  # normalized score in [0, 1]

# Max possible reward: 1.0 per step
MAX_TOTAL_REWARD = MAX_STEPS * 1.0

SYSTEM_PROMPT = textwrap.dedent(
    """
    You are an AI hospital triage assistant. You must prioritize patients based on their medical condition.
    
    Available actions:
    - TREAT_NOW: Immediate medical attention for critical patients
    - MONITOR: Observation and monitoring for moderate cases  
    - WAIT: Can be deferred for low priority patients
    
    Patient assessment factors:
    - RED triage (severity >= 60): Critical - needs immediate treatment
    - YELLOW triage (30 <= severity < 60): Moderate - needs monitoring
    - GREEN triage (severity < 30): Low priority - can wait
    
    Analyze the patient's vitals, symptoms, and severity score, then choose the most appropriate action.
    Reply with exactly one action: TREAT_NOW, MONITOR, or WAIT
    """
).strip()


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


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


def build_user_prompt(step: int, patient_data: dict, last_reward: float, history: List[str]) -> str:
    """Build user prompt with patient information"""
    vitals = patient_data["vitals"]
    symptoms = [s.replace("_", " ").title() for s in patient_data["symptoms"]]
    
    return textwrap.dedent(
        f"""
        Step: {step}
        
        Patient Information:
        - Patient ID: {patient_data['patient_id']}
        - Triage Level: {patient_data['triage_level']}
        - Severity Score: {patient_data['severity_score']}/100
        - Waiting Time: {patient_data['waiting_time']} minutes
        
        Vital Signs:
        - Heart Rate: {vitals['heart_rate']} bpm
        - Oxygen Saturation: {vitals['oxygen_saturation']}%
        - Temperature: {vitals['temperature']}°C
        - Blood Pressure: {vitals['systolic_bp']} mmHg
        - Age: {vitals['age']} years
        
        Symptoms: {', '.join(symptoms) if symptoms else 'None'}
        
        Last Action Reward: {last_reward:.2f}
        
        Choose your action: TREAT_NOW, MONITOR, or WAIT
        """
    ).strip()


def get_model_action(client: OpenAI, step: int, patient_data: dict, last_reward: float, history: List[str]) -> str:
    """Get action from LLM model"""
    user_prompt = build_user_prompt(step, patient_data, last_reward, history)
    
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        
        text = (completion.choices[0].message.content or "").strip().upper()
        
        # Validate action
        valid_actions = ["TREAT_NOW", "MONITOR", "WAIT"]
        for action in valid_actions:
            if action in text:
                return action
        
        # Default to WAIT if no valid action found
        return "WAIT"
        
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return "WAIT"


async def main() -> None:
    """Main inference loop"""
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    
    # Initialize environment
    env = HospitalTriageEnv(difficulty="medium")
    
    history: List[str] = []
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False
    
    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)
    
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
            
            # Get action from model
            action_str = get_model_action(client, step, patient_data, last_reward, history)
            
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
            
            # Add to history
            history.append(f"Step {step}: {action_str} -> reward {reward:+.2f} (triage: {patient_data['triage_level']})")
            
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
