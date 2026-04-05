
sdk: gradio
---
title: 🏥 Hospital Triage OpenEnv
emoji: 🏥
colorFrom: red
colorTo: blue
sdk: docker
python_version: 3.10
app_file: app.py
pinned: true
license: mit
tags:
- healthcare
- triage
- openenv
- fastapi
- rl
- hospital
- ai
- pytorch
- hackathon
short_description: OpenEnv-compatible hospital triage environment
---

# 🏥 Hospital Triage OpenEnv Environment

A production-ready OpenEnv-compatible environment for hospital triage decision-making where AI agents can learn to prioritize patients effectively.

## 🎯 Problem

Simulates a hospital emergency triage system where agents must decide between:
- **TREAT_NOW** - Immediate medical attention
- **MONITOR** - Observation and monitoring
- **WAIT** - Can be deferred

## 🚀 OpenEnv Compliance

Fully implements OpenEnv standards with typed models:

```python
# Gym-style RL loop
env = HospitalTriageEnv()
observation = env.reset()
action = agent.select_action(observation)
observation, reward, done, info = env.step(action)
```

## 📡 API Endpoints

### Core OpenEnv Interface
- `POST /reset` - Initialize new episode
- `POST /step` - Execute action decision  
- `GET /state` - Get environment state

### Additional Endpoints
- `GET /` - Health check
- `GET /info` - Environment information
- `GET /performance` - Performance metrics

## 🎮 Usage Examples

### Python API
```python
import requests

# Reset environment
response = requests.post("/reset", json={"difficulty": "medium"})
episode = response.json()

# Take action
response = requests.post("/step", json={"action": "TREAT_NOW"})
result = response.json()

print(f"Reward: {result['reward']}")
print(f"Done: {result['done']}")
```

### Agent Interaction
```python
from env_new import HospitalTriageEnv
from models import Action, ActionType

env = HospitalTriageEnv(difficulty="medium")
observation = env.reset()

action = Action(action=ActionType.TREAT_NOW)
result = env.step(action)
```

## 📊 Sample Input/Output

### Reset Response
```json
{
  "observation": {
    "patient": {
      "patient_id": "P1234",
      "vitals": {"heart_rate": 85, "oxygen_saturation": 92},
      "symptoms": ["chest_pain"],
      "severity_score": 75.3,
      "triage_level": "RED"
    },
    "available_resources": {"icu_beds": 3, "doctors": 5},
    "step_count": 0
  },
  "state": {
    "episode_id": "uuid-string",
    "step_count": 0,
    "total_reward": 0.0,
    "is_done": false
  }
}
```

### Step Response
```json
{
  "observation": {...},
  "reward": 1.0,
  "done": true,
  "info": {
    "reward_explanation": "Correctly identified critical patient",
    "performance": {"accuracy": 1.0}
  }
}
```

## 🏗️ Environment Design

### Difficulty Levels
- **EASY** - Clear symptoms, obvious vitals
- **MEDIUM** - Mixed signals, moderate complexity  
- **HARD** - Ambiguous critical cases

### Reward System
- **Correct critical decision** → +1.0
- **Correct moderate decision** → +0.8
- **Correct low priority** → +0.6
- **Slightly incorrect** → +0.5
- **Dangerous wrong decision** → +0.0

## 🧪 Testing

Run the inference script to test agent performance:

```bash
python inference.py
```

This demonstrates:
- Simple rule-based agent vs random baseline
- Reproducible scoring with fixed seeds
- Performance metrics and comparisons
- API workflow testing

## 📁 Project Structure

```
hospital_triage_env/
├── models.py          # Action, Observation, State models
├── env.py             # Environment logic
├── app.py             # FastAPI server
├── inference.py       # Demo script
├── reward.py          # Reward calculation
├── severity.py        # Severity scoring
├── requirements.txt
└── README.md
```

## 🔧 Technologies

- **FastAPI** - Web framework and API
- **OpenEnv** - Environment interface standard
- **Pydantic** - Data validation and models
- **Python 3.10** - Core language

## 🌐 Live Demo

Interactive API documentation available at `/docs` endpoint when running.

## 📝 License

MIT License

---

**Built for Meta PyTorch OpenEnv Hackathon**  
**Category: AI/ML with OpenEnv Framework**
