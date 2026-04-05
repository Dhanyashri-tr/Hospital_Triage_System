---
title: Hospital Triage System
emoji: 🏥
colorFrom: red
colorTo: blue
sdk: gradio
python_version: 3.10
app_file: app.py
pinned: true
license: mit
tags:
- healthcare
- triage
- gradio
- medical
- ai
- demo
short_description: AI-powered hospital triage priority assessment
---

# 🏥 Hospital Triage System

An AI-powered hospital triage system that assesses patient priority and recommends medical actions using a simple Gradio interface.

## 🚀 Features

- **AI-Powered Triage**: Analyzes patient vitals and pain levels
- **Simple Interface**: Easy-to-use Gradio web UI
- **Real-time Assessment**: Instant triage decisions
- **Color-Coded Results**: Visual triage level indicators
- **Mobile Friendly**: Responsive design for all devices

## 📡 How to Use

### Input Parameters
- **Heart Rate**: Patient's pulse in beats per minute (30-200 bpm)
- **Oxygen Saturation**: Blood oxygen level (70-100%)
- **Pain Level**: Patient's self-reported pain (0-10 scale)

### Triage Logic
- **Score ≥ 25**: 🚨 **TREAT_NOW** (Critical - RED)
- **Score ≥ 15**: 👁️ **MONITOR** (Moderate - YELLOW)
- **Score < 15**: ⏰ **WAIT** (Stable - GREEN)

## 🎮 Demo

Visit the deployed Space to try the interactive triage assessment:
- Enter patient vitals
- Click "Assess Patient Priority"
- Get instant triage recommendation

## 🏗️ Technology Stack

- **Gradio**: Modern web interface framework
- **Python**: Core triage logic
- **NumPy**: Numerical computations
- **Hugging Face Spaces**: Instant deployment

## 📋 Example Cases

| Scenario | Heart Rate | Oxygen | Pain | Result |
|----------|-------------|---------|--------|---------|
| Critical Case | 110 | 88 | 8 | 🚨 TREAT_NOW |
| Moderate Case | 85 | 95 | 4 | 👁️ MONITOR |
| Stable Case | 70 | 98 | 2 | ⏰ WAIT |

## ⚠️ Medical Disclaimer

This is an AI demonstration tool for educational purposes only. Always consult qualified healthcare professionals for actual medical decisions and patient care.

---

**🏆 Built for Meta PyTorch OpenEnv Hackathon**

### API Endpoints

- **Interactive Docs**: Visit `/docs` for interactive API documentation
- **Reset Environment**: `POST /reset`
- **Execute Action**: `POST /step` 
- **Get State**: `GET /state`
- **View Metrics**: `GET /metrics`

### Test the System

```python
import requests

# Reset environment
response = requests.post("/reset", json={"task": "medium"})
state = response.json()

# Take action
response = requests.post("/step", json={"action": "TREAT_NOW"})
result = response.json()

print(f"Reward: {result['reward']}")
print(f"Done: {result['done']}")
```

## Features

- **Severity Score Normalization** (0-100)
-  **Triage Categories** (RED/YELLOW/GREEN)
- **Resource Management** (ICU/general beds, doctors)
- **Balanced Reward System**
- **Queue Simulation**
- **Explainable AI**

## Live Demo

Visit the Space URL to interact with the live API and explore the comprehensive documentation.

## Key Features

### Severity Scoring
- Weighted formula: SPO2 (25%), systolic BP (20%), heart rate (15%), age (10%), symptoms (30%)
- Consistent distribution: LOW (0-20), MODERATE (21-50), CRITICAL (51-100)
- Proper triage mapping: RED/YELLOW/GREEN

### Resource Management
- ICU beds, general beds, doctors, nurses tracking
- Strict resource constraints with blocking logic
- Resource allocation and release management

### Reward System
- Moderate rewards (0.4-0.7) for correct decisions
- Strong penalties (-0.5 or lower) for incorrect actions
- Resource violation penalties and waiting time penalties

## Architecture

```
Hospital_Triage_System/
├── main.py              # FastAPI application
├── env.py               # Environment logic
├── severity.py          # Severity calculation
├── reward.py            # Reward system
├── test_system.py       # Test suite
├── requirements.txt     # Dependencies
└── Dockerfile          # Deployment config
```

## Demo Usage

1. Visit the live Space
2. Try the interactive API documentation
3. Reset environment with different difficulty levels
4. Test TREAT_NOW, MONITOR, and WAIT actions
5. View performance metrics

## AI Integration

- Compatible with RL frameworks
- Standard OpenEnv interface
- Structured state representation
- Calibrated reward signals

## Technologies Used

- **FastAPI**: Web framework and API
- **OpenEnv**: Environment interface standard
- **Pydantic**: Data validation
- **Python**: Core programming language
- **Uvicorn**: ASGI server
- **Docker**: Containerization

## Performance Metrics

- Average reward per step
- Total cumulative reward
- Decision efficiency ratio
- Patients treated count
- Termination analysis
## OpenEnv Environment Details

### Observation Space
The environment state includes:
- severity (1–10)
- waiting_time (minutes)
- age
- resources_available
- condition (cardiac, injury, fever)

### Action Space
The agent can take one of the following actions:
- TREAT_NOW
- MONITOR
- WAIT

### Reward Function
- Correct critical decision → +10
- Correct moderate decision → +5
- Correct low priority decision → +2
- Incorrect decision → -5
- Penalty for long waiting time → -3

### Episode Design
Each episode represents a single triage decision, making it a one-step decision environment.

## Hackathon Highlights

- **Realistic Simulation**: Hospital resource management
- **Explainable AI**: Clear decision reasoning
- **Professional API**: Production-ready interface
- **Comprehensive Testing**: Full verification suite
- **OpenEnv Compatible**: Standard RL interface

## License

MIT License

---

**Built for Meta PyTorch Hackathon 2026**  
**Category: AI/ML with OpenEnv Framework**  
**Live Demo**: https://dhanyashri-tr-hospital-triege-system.hf.space
