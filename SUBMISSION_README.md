# 🏥 Hospital OpenEnv API - Meta PyTorch Hackathon Submission

## 📋 Project Overview
A comprehensive AI Hospital Triage System implementing OpenEnv interface with FastAPI. Features realistic patient prioritization using severity scoring (0-100), resource management, and reward-based learning.

## ✨ Key Features Implemented

### 🔬 **Severity Score Normalization (0-100)**
- Weighted formula: SPO2 (25%), systolic BP (20%), heart rate (15%), age (10%), symptoms (30%)
- Consistent distribution: LOW (0-20), MODERATE (21-50), CRITICAL (51-100)
- Proper triage mapping: RED/YELLOW/GREEN

### 🏗️ **Resource Management**
- ICU beds, general beds, doctors, nurses tracking
- Strict resource constraints with blocking logic
- Resource allocation and release management

### ⚖️ **Balanced Reward System**
- Moderate rewards (0.4-0.7) for correct decisions
- Strong penalties (-0.5 or lower) for incorrect actions
- Resource violation penalties and waiting time penalties

### 🔄 **Queue Simulation**
- Stochastic patient arrivals with probability-based rates
- Emergency case injection (10% probability)
- Dynamic waiting time tracking

### 📊 **Explainability**
- Decision reasoning for each action
- Reward breakdown components
- Resource status messages
- Termination reason tracking

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- OpenEnv Core
- FastAPI

### Installation
```bash
pip install -r requirements.txt
pip install openenv-core
```

### Run Server
```bash
python main.py
```

### Test System
```bash
python test_system.py
```

## 📡 API Endpoints

### Core OpenEnv Interface
- `POST /reset` - Reset environment with difficulty
- `POST /step` - Execute action (TREAT_NOW/MONITOR/WAIT)
- `GET /state` - Get current environment state

### Additional Features
- `GET /metrics` - Performance metrics
- `GET /demo/patient` - Generate sample patient
- `GET /demo/scenario` - Complete demo scenario
- `GET /docs` - Interactive API documentation

## 🏗️ Architecture
```
Hospital_Triage_System/
├── main.py              # FastAPI application
├── env.py               # Main environment logic
├── severity.py          # Severity calculation
├── reward.py            # Reward system
├── test_system.py       # Test suite
├── requirements.txt     # Dependencies
└── README.md           # Documentation
```

## 🎯 Difficulty Levels
- **Easy**: 5 ICU beds, 20 general beds, 8 doctors
- **Medium**: 3 ICU beds, 15 general beds, 5 doctors  
- **Hard**: 2 ICU beds, 10 general beds, 3 doctors

## 📈 Performance Metrics
- Average reward per step
- Total cumulative reward
- Decision efficiency ratio
- Patients treated count
- Termination analysis

## 🧠 AI Integration
- Compatible with RL frameworks
- Standard OpenEnv interface
- Structured state representation
- Calibrated reward signals

## 🔧 Technologies Used
- **FastAPI**: Web framework and API
- **OpenEnv**: Environment interface standard
- **Pydantic**: Data validation
- **Python**: Core programming language
- **Uvicorn**: ASGI server

## 📊 Verification Results
- ✅ Severity normalization: 0-100 range verified
- ✅ Triage mapping: RED/YELLOW/GREEN correct
- ✅ Resource constraints: Proper blocking logic
- ✅ Reward balance: Moderate positives, strong negatives
- ✅ API compliance: Full OpenEnv interface

## 🎮 Demo Usage
1. Start server: `python main.py`
2. Visit: http://localhost:8000/docs
3. Reset environment: POST `/reset`
4. Take actions: POST `/step`
5. View metrics: GET `/metrics`

## 🏆 Hackathon Highlights
- **Realistic Simulation**: Hospital resource management
- **Explainable AI**: Clear decision reasoning
- **Professional API**: Production-ready interface
- **Comprehensive Testing**: Full verification suite
- **OpenEnv Compatible**: Standard RL interface

## 📝 License
MIT License

## 👥 Team
Single developer project

---

**Submission for Meta PyTorch Hackathon 2026**  
**Category: AI/ML with OpenEnv Framework**  
**Deadline: April 8th, 11:59 PM**
