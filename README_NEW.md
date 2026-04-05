# 🏥 Hospital OpenEnv API v1.1.0

## Overview
A comprehensive AI Hospital Triage System implementing OpenEnv interface with FastAPI. This system provides realistic patient prioritization using severity scoring, resource management, and reward-based learning.

## ✨ Key Features

### 🔬 **Severity Score Normalization (0-100)**
- Weighted formula based on vital signs and symptoms
- Consistent distribution: LOW (0-20), MODERATE (21-50), CRITICAL (51-100)
- Factors: SPO2, systolic BP, heart rate, age, symptoms

### 🚦 **Triage Categories**
- **RED** (≥50): Critical - Immediate treatment required
- **YELLOW** (20-49): Moderate - Monitoring needed  
- **GREEN** (<20): Low - Can wait

### 🏗️ **Resource Management**
- ICU beds, general beds, doctors, nurses
- Strict resource constraints with blocking logic
- Resource allocation and release tracking

### ⚖️ **Balanced Reward System**
- Moderate rewards (0.4-0.7) for correct decisions
- Strong penalties (-0.5 or lower) for incorrect actions
- Resource violation penalties
- Waiting time penalties

### 🔄 **Queue Simulation**
- Stochastic patient arrivals
- Emergency case injection (10% probability)
- Dynamic waiting time tracking

### 📊 **Explainability**
- Decision reasoning for each action
- Reward breakdown components
- Resource status messages
- Termination reason tracking

## 🚀 Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run Server (3 Options)

#### Option 1: Simple (Recommended)
```bash
python main.py
```

#### Option 2: Using startup scripts
```bash
# Windows
start_server.bat

# Linux/Mac  
./start_server.sh
```

#### Option 3: Using uvicorn directly
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Server starts on `http://localhost:8000`**

### API Documentation
- Interactive docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📡 API Endpoints

### Core OpenEnv Interface

#### `POST /reset`
Reset environment with optional difficulty.
```json
{
  "task": "medium",
  "max_steps": 100
}
```

#### `POST /step`
Execute one action step.
```json
{
  "action": "TREAT_NOW"
}
```
**Actions**: `TREAT_NOW`, `MONITOR`, `WAIT`

#### `GET /state`
Get current environment state.

### Additional Endpoints

#### `GET /metrics`
Performance metrics for current episode.

#### `GET /health`
System health check.

#### `GET /demo/patient`
Generate demo patient for testing.

#### `GET /demo/scenario`
Generate complete demo scenario.

## 🏗️ Architecture

```
Hospital_Triage_System/
├── main.py              # FastAPI application
├── env.py               # Main environment logic
├── severity.py          # Severity calculation
├── reward.py            # Reward system
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## 🎯 Difficulty Levels

| Level | ICU Beds | General Beds | Doctors | Arrival Rate |
|-------|-----------|--------------|---------|--------------|
| Easy  | 5         | 20           | 8       | Low (30%)    |
| Medium| 3         | 15           | 5       | Medium (50%) |
| Hard  | 2         | 10           | 3       | High (70%)   |

## 📊 Response Format

### Step Response
```json
{
  "state": {
    "current_step": 5,
    "current_patient": {...},
    "queue_length": 3,
    "treated_count": 2,
    "total_reward": 1.2,
    "resources": {...},
    "done": false
  },
  "reward": 0.6,
  "done": false,
  "info": {
    "severity_score": 75.3,
    "triage_level": "RED",
    "decision_reason": "Correctly identified critical patient...",
    "reward_breakdown": {...},
    "resource_status_message": "Resources available...",
    "resource_blocked": false
  }
}
```

## 🧪 Testing Examples

### Basic Workflow
```bash
# 1. Reset environment
curl -X POST "http://localhost:8000/reset" \
  -H "Content-Type: application/json" \
  -d '{"task": "medium"}'

# 2. Take action
curl -X POST "http://localhost:8000/step" \
  -H "Content-Type: application/json" \
  -d '{"action": "TREAT_NOW"}'

# 3. Check state
curl "http://localhost:8000/state"
```

### Demo Patient
```bash
curl "http://localhost:8000/demo/patient"
```

## 🎮 Usage Scenarios

### Scenario 1: Critical Patient
- High severity score (≥50)
- RED triage level
- Requires ICU bed + doctor
- High reward for TREAT_NOW

### Scenario 2: Resource Constraint
- Action blocked if resources unavailable
- Strong penalty applied
- Patient remains in queue

### Scenario 3: Emergency Arrival
- Random emergency patients
- High severity vitals forced
- Tests system under pressure

## 📈 Performance Metrics

- **Average Reward**: Mean reward per step
- **Total Reward**: Cumulative episode reward  
- **Efficiency**: Positive decision ratio
- **Patients Treated**: Successfully processed
- **Termination Reason**: Episode end cause

## 🔧 Configuration

### Environment Variables
```python
# In main.py
MAX_STEPS = 100          # Default max steps
DEFAULT_DIFFICULTY = "medium"
EMERGENCY_PROB = 0.1     # 10% emergency chance
```

### Reward Calibration
```python
# In reward.py
BASE_REWARDS = {
    "correct_critical": 0.6,
    "correct_moderate": 0.5,
    "resource_penalty": -0.8,
    # ... more weights
}
```

## 🚨 Termination Conditions

1. **MAX_STEPS_REACHED**: Step limit exceeded
2. **NO_PATIENTS_REMAINING**: Queue empty
3. **SUCCESS**: 20+ patients treated
4. **CRITICAL_FAILURE**: System error

## 🧠 AI Integration

### Reinforcement Learning
- Compatible with RL frameworks
- State representation for ML models
- Reward signal for training

### Decision Support
- Explainable reasoning
- Resource constraint awareness
- Priority recommendations

## 🔍 Monitoring

### Health Checks
```bash
curl "http://localhost:8000/health"
```

### Performance Metrics
```bash
curl "http://localhost:8000/metrics"
```

## 🐛 Troubleshooting

### Common Issues
1. **Resource blocked**: Check available resources
2. **Invalid action**: Use TREAT_NOW/MONITOR/WAIT
3. **Environment done**: Call /reset first

### Debug Mode
Enable verbose logging in `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Submit pull request

## 📞 Support

For issues and questions:
- Check API docs at `/docs`
- Review health endpoint
- Validate request formats

---

**Version**: 1.1.0  
**Last Updated**: 2026-04-04  
**Status**: Production Ready ✅
