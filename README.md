---
title: AI Hospital Triage System
emoji: 🏥
colorFrom: blue
colorTo: red
sdk: gradio
app_file: app.py
---

# 🏥 AI-Powered Hospital Triage System

## Overview
This project simulates an intelligent hospital triage system that prioritizes patients based on urgency.

It uses a rule-based AI approach inspired by real-world emergency triage systems to decide whether a patient should be treated immediately, monitored, or can safely wait.

## Features

-  Smart severity mapping (symptoms → score)
-  Priority score calculation
-  Priority levels (Critical / Moderate / Safe)
-  Decision system (Treat / Monitor / Wait)
-  Reward-based evaluation (RL-inspired)
-  Dynamic priority meter (with colors & animation)
-  Risk factor detection
-  Department recommendation
-  Patient summary with ID & timestamp
-  Explainable AI decisions

##  How It Works

1. User inputs patient details:
   - Name
   - Severity (via symptoms)
   - Waiting time
   - Age
   - Condition
   - Resources available

2. System calculates a **priority score**:
    Priority Score = (Severity × 2) + (Waiting Time × 0.5) + Condition Bonus

3. Based on score:
   - 🔴 Critical → Immediate treatment
   - 🟡 Moderate → Monitor
   - 🟢 Safe → Wait

4. The system outputs:
   - Decision
   - Reward
   - Reason (Explainable AI)
   - Visual priority meter

---

## Real-World Relevance

This system simulates real hospital triage workflows:
- Emergency severity prioritization
- Resource allocation
- Risk-based decision making

## Limitations

- Rule-based (not trained ML model)
- Uses simulated data
- No real hospital integration

## Future Improvements

- Integrate Machine Learning model
- Use real patient datasets
- Add database support
- Live hospital integration
- Emergency alert system

## Tech Stack

- Python 🐍
- Gradio (UI)
- FastAPI (initial backend)
- Custom Environment (RL-inspired)

## Conclusion

This project demonstrates how AI can assist in **critical healthcare decision-making**, improving efficiency, accuracy, and patient prioritization.

## Author

Dhanyashri T R
Vinayaka T


