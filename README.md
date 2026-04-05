---
title: AI Hospital Triage System
emoji: 🏥
colorFrom: blue
colorTo: red
sdk: gradio
sdk_version: 4.36.1
app_file: app.py
pinned: false
---

# 🏥 AI Hospital Triage System

An AI-powered patient triage assessment system designed for emergency medical care prioritization. Built for the Meta PyTorch OpenEnv Hackathon.

## 🚀 Features

- **AI-Powered Assessment**: Intelligent triage scoring algorithm
- **Real-time Analysis**: Instant patient priority evaluation
- **Professional UI**: Clean, intuitive Gradio interface
- **Evidence-Based**: Medical triage principles implementation
- **Mobile Responsive**: Works on all devices

## 📋 How It Works

### Scoring Algorithm
The system uses a weighted scoring formula to determine patient priority:

```
score = (heart_rate/10) + (100 - oxygen) + (pain*2)
```

### Decision Thresholds
- **Score ≥ 25**: 🚨 **TREAT NOW** (Critical Priority)
- **Score ≥ 15**: ⚠️ **MONITOR** (Moderate Priority)  
- **Score < 15**: 🟢 **WAIT** (Low Priority)

## 🎯 Use Case

### Emergency Department Triage
This AI system helps emergency medical staff quickly assess patient priority based on vital signs and pain levels. The algorithm considers:

- **Heart Rate**: Elevated rates indicate potential distress
- **Oxygen Saturation**: Lower levels suggest respiratory compromise
- **Pain Level**: Patient-reported discomfort assessment

### Example Assessments
| Patient | Heart Rate | Oxygen | Pain | Score | Decision |
|---------|-------------|---------|-------|-------|----------|
| Critical | 120 bpm | 85% | 8/10 | 39.0 | 🚨 TREAT NOW |
| Moderate | 85 bpm | 95% | 4/10 | 21.5 | ⚠️ MONITOR |
| Stable | 70 bpm | 98% | 2/10 | 13.0 | 🟢 WAIT |

## 🏗️ Tech Stack

- **Frontend**: Gradio 4.36.1
- **Backend**: Python 3.10+
- **Deployment**: Hugging Face Spaces
- **Algorithm**: Custom triage scoring system

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/Dhanyashri-tr/Hospital_Triage_System.git
cd Hospital_Triage_System

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Hugging Face Spaces
The application is automatically deployed and available at:
https://dhanyashri-tr-hospital-triege-system.hf.space

## 📊 Algorithm Details

### Input Parameters
- **Heart Rate**: 40-180 bpm (Normal: 60-100 bpm)
- **Oxygen Level**: 70-100% (Normal: 95-100%)
- **Pain Level**: 0-10 scale (0=no pain, 10=severe pain)

### Scoring Components
1. **Heart Rate Component**: `heart_rate/10`
   - Higher rates increase urgency score
   
2. **Oxygen Component**: `(100 - oxygen)`
   - Lower oxygen levels significantly increase score
   
3. **Pain Component**: `pain*2`
   - Higher pain levels weighted more heavily

### Medical Rationale
The scoring algorithm prioritizes:
- **Respiratory compromise** (oxygen saturation)
- **Cardiovascular distress** (heart rate)
- **Patient discomfort** (pain level)

## ⚠️ Medical Disclaimer

**IMPORTANT**: This AI-powered triage system is designed for **educational demonstration purposes only** as part of the Meta PyTorch OpenEnv Hackathon.

- ❌ **Do not use** this tool for actual medical decision-making
- ❌ **Do not rely** on this system for real patient assessment
- ✅ **Always consult** qualified healthcare professionals
- ✅ **Use only** for educational and demonstration purposes

## 🏆 Hackathon Information

- **Event**: Meta PyTorch OpenEnv Hackathon
- **Category**: Healthcare AI Applications
- **Purpose**: Demonstrate AI in medical triage systems
- **Status**: Educational Prototype
- **Technology**: Python, Gradio, Machine Learning

## 📱 Interface Features

- **Professional Design**: Clean, medical-grade interface
- **Interactive Sliders**: Easy parameter adjustment
- **Real-time Feedback**: Instant assessment results
- **Detailed Reporting**: Comprehensive triage analysis
- **Mobile Responsive**: Works on smartphones and tablets

## 🔬 Future Enhancements

- [ ] Integration with real medical devices
- [ ] Machine learning model training
- [ ] Multi-parameter vital sign analysis
- [ ] Historical patient data tracking
- [ ] Hospital system integration

## 📞 Contact & Support

For questions about this hackathon project or AI implementation:

- **GitHub**: https://github.com/Dhanyashri-tr/Hospital_Triage_System
- **Hugging Face**: https://huggingface.co/spaces/dhanyashri-tr/Hospital_Triage_System

---

**🏆 Built with passion for healthcare innovation at the Meta PyTorch OpenEnv Hackathon**
