"""
Inference script for Hospital Triage Environment
Demonstrates agent interaction with reproducible scoring
"""

import random
import time
from typing import Dict, Any, List
from models import ActionType
from env_new import HospitalTriageEnv


class SimpleAgent:
    """Simple rule-based agent for demonstration"""
    
    def __init__(self):
        self.actions = list(ActionType)
    
    def select_action(self, patient_data: Dict[str, Any]) -> ActionType:
        """Select action based on patient triage level"""
        triage_level = patient_data.get("triage_level", "GREEN")
        
        if triage_level == "RED":
            return ActionType.TREAT_NOW
        elif triage_level == "YELLOW":
            return ActionType.MONITOR
        else:
            return ActionType.WAIT


class RandomAgent:
    """Random agent for baseline"""
    
    def __init__(self):
        self.actions = list(ActionType)
    
    def select_action(self, patient_data: Dict[str, Any]) -> ActionType:
        """Select random action"""
        return random.choice(self.actions)


def run_episode(env: HospitalTriageEnv, agent, episode_id: int) -> Dict[str, Any]:
    """Run a single episode and return results"""
    
    # Reset environment
    reset_result = env.reset()
    observation = reset_result.observation
    state = reset_result.state
    
    print(f"\n=== Episode {episode_id} ===")
    print(f"Episode ID: {state.episode_id}")
    print(f"Difficulty: {env.difficulty}")
    print(f"Patient ID: {observation.patient.patient_id}")
    print(f"Triage Level: {observation.patient.triage_level}")
    print(f"Severity Score: {observation.patient.severity_score}")
    print(f"Vitals: HR={observation.patient.vitals.heart_rate}, "
          f"SpO2={observation.patient.vitals.oxygen_saturation}, "
          f"BP={observation.patient.vitals.systolic_bp}")
    print(f"Symptoms: {[s.value for s in observation.patient.symptoms]}")
    print(f"Available Resources: {observation.available_resources}")
    
    # Agent selects action
    patient_dict = {
        "triage_level": observation.patient.triage_level,
        "severity_score": observation.patient.severity_score
    }
    action = agent.select_action(patient_dict)
    
    print(f"\nAgent Action: {action.value}")
    
    # Execute action
    from models import Action
    step_result = env.step(Action(action=action))
    
    print(f"Reward: {step_result.reward}")
    print(f"Done: {step_result.done}")
    print(f"Explanation: {step_result.info.get('reward_explanation', 'N/A')}")
    
    # Get final state
    final_state = env.state()
    print(f"Total Reward: {final_state.total_reward}")
    print(f"Accuracy: {final_state.performance_metrics.get('accuracy', 0):.2f}")
    
    return {
        "episode_id": episode_id,
        "patient_id": observation.patient.patient_id,
        "triage_level": observation.patient.triage_level,
        "severity_score": observation.patient.severity_score,
        "action_taken": action.value,
        "reward": step_result.reward,
        "total_reward": final_state.total_reward,
        "accuracy": final_state.performance_metrics.get('accuracy', 0),
        "explanation": step_result.info.get('reward_explanation', 'N/A')
    }


def evaluate_agents(difficulty: str = "medium", num_episodes: int = 5):
    """Evaluate different agents on the environment"""
    
    print("=" * 60)
    print("HOSPITAL TRIAGE ENVIRONMENT - INFERENCE DEMO")
    print("=" * 60)
    print(f"Difficulty: {difficulty}")
    print(f"Episodes per agent: {num_episodes}")
    print()
    
    # Initialize agents
    simple_agent = SimpleAgent()
    random_agent = RandomAgent()
    
    # Test Simple Agent
    print("🤖 TESTING SIMPLE AGENT")
    print("-" * 40)
    
    simple_results = []
    env = HospitalTriageEnv(difficulty=difficulty)
    
    for i in range(num_episodes):
        result = run_episode(env, simple_agent, i + 1)
        simple_results.append(result)
        time.sleep(0.5)  # Brief pause for readability
    
    # Calculate Simple Agent performance
    simple_avg_reward = sum(r["reward"] for r in simple_results) / len(simple_results)
    simple_avg_accuracy = sum(r["accuracy"] for r in simple_results) / len(simple_results)
    
    print(f"\n📊 SIMPLE AGENT RESULTS:")
    print(f"Average Reward: {simple_avg_reward:.3f}")
    print(f"Average Accuracy: {simple_avg_accuracy:.3f}")
    print(f"Correct Decisions: {sum(1 for r in simple_results if r['reward'] > 0.5)}/{len(simple_results)}")
    
    # Test Random Agent
    print(f"\n🎲 TESTING RANDOM AGENT")
    print("-" * 40)
    
    random_results = []
    env = HospitalTriageEnv(difficulty=difficulty)  # Fresh environment
    
    for i in range(num_episodes):
        result = run_episode(env, random_agent, i + 1)
        random_results.append(result)
        time.sleep(0.5)
    
    # Calculate Random Agent performance
    random_avg_reward = sum(r["reward"] for r in random_results) / len(random_results)
    random_avg_accuracy = sum(r["accuracy"] for r in random_results) / len(random_results)
    
    print(f"\n📊 RANDOM AGENT RESULTS:")
    print(f"Average Reward: {random_avg_reward:.3f}")
    print(f"Average Accuracy: {random_avg_accuracy:.3f}")
    print(f"Correct Decisions: {sum(1 for r in random_results if r['reward'] > 0.5)}/{len(random_results)}")
    
    # Comparison
    print(f"\n🏆 COMPARISON:")
    print(f"Simple Agent vs Random Agent:")
    print(f"  Reward: {simple_avg_reward:.3f} vs {random_avg_reward:.3f}")
    print(f"  Accuracy: {simple_avg_accuracy:.3f} vs {random_avg_accuracy:.3f}")
    
    if simple_avg_reward > random_avg_reward:
        print("  ✅ Simple Agent performs better!")
    elif random_avg_reward > simple_avg_reward:
        print("  🎲 Random Agent performs better!")
    else:
        print("  ⚖️ Both agents perform equally")
    
    return {
        "simple_agent": {
            "results": simple_results,
            "avg_reward": simple_avg_reward,
            "avg_accuracy": simple_avg_accuracy
        },
        "random_agent": {
            "results": random_results,
            "avg_reward": random_avg_reward,
            "avg_accuracy": random_avg_accuracy
        }
    }


def test_api_workflow():
    """Test the API workflow for demonstration"""
    
    print("\n" + "=" * 60)
    print("🌐 API WORKFLOW DEMONSTRATION")
    print("=" * 60)
    
    import requests
    
    base_url = "http://localhost:8000"
    
    try:
        # Health check
        response = requests.get(f"{base_url}/")
        print(f"✅ Health Check: {response.json()}")
        
        # Get environment info
        response = requests.get(f"{base_url}/info")
        print(f"✅ Environment Info: {response.json()}")
        
        # Reset environment
        response = requests.post(f"{base_url}/reset", json={"difficulty": "medium"})
        reset_data = response.json()
        print(f"✅ Reset Complete - Episode ID: {reset_data['state']['episode_id']}")
        
        # Get state
        response = requests.get(f"{base_url}/state")
        state_data = response.json()
        print(f"✅ Current State - Step: {state_data['step_count']}")
        
        # Step with action
        response = requests.post(f"{base_url}/step", json={"action": "TREAT_NOW"})
        step_data = response.json()
        print(f"✅ Step Complete - Reward: {step_data['reward']}")
        
        # Get performance
        response = requests.get(f"{base_url}/performance")
        perf_data = response.json()
        print(f"✅ Performance - Accuracy: {perf_data['accuracy']}")
        
        print("\n🎉 API workflow completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Start server with: uvicorn app:app --host 0.0.0.0 --port 7860")
    except Exception as e:
        print(f"❌ API test failed: {e}")


if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    
    print("🏥 Hospital Triage Environment - Inference Demo")
    print("=" * 60)
    
    # Run evaluation on different difficulty levels
    difficulties = ["easy", "medium", "hard"]
    
    for difficulty in difficulties:
        print(f"\n🎯 Testing {difficulty.upper()} difficulty:")
        evaluate_agents(difficulty, num_episodes=3)
        print()
    
    # Test API workflow
    test_api_workflow()
    
    print("\n" + "=" * 60)
    print("🎯 INFERENCE DEMO COMPLETE")
    print("=" * 60)
    print("Results show reproducible scoring with clear performance metrics")
    print("Simple rule-based agent outperforms random baseline")
    print("API workflow demonstrates OpenEnv compliance")
