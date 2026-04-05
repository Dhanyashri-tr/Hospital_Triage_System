---
title: 🏥 Hospital OpenEnv API
emoji: 🏥
colorFrom: red
colorTo: blue
sdk: docker
python_version: 3.10
app_file: main.py
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
short_description: AI Hospital Triage System with OpenEnv interface
---

# 🏥 Hospital OpenEnv API

A comprehensive AI Hospital Triage System implementing OpenEnv interface with FastAPI. Features realistic patient prioritization using severity scoring, resource management, and reward-based learning.

## 🚀 Quick Start

The API is automatically deployed and available at the Space URL.

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

## ✨ Features

- 🔬 **Severity Score Normalization** (0-100)
- 🚦 **Triage Categories** (RED/YELLOW/GREEN)
- 🏗️ **Resource Management** (ICU/general beds, doctors)
- ⚖️ **Balanced Reward System**
- 🔄 **Queue Simulation**
- 📊 **Explainable AI**

## 📊 Live Demo

Visit the Space URL to interact with the live API and explore the comprehensive documentation.

---

**Built for Meta PyTorch Hackathon 2026**
