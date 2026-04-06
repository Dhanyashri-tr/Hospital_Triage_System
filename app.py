import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="AI Hospital Triage System",
    page_icon="🏥",
    layout="centered"
)

# Main title and description
st.title("🏥 AI Hospital Triage System")
st.markdown("**Meta PyTorch OpenEnv Hackathon Project**")
st.markdown("*AI-Powered Patient Priority Assessment for Emergency Medical Care*")

st.divider()

# Input section
st.header("📋 Patient Information")
st.markdown("Enter patient vitals to receive triage assessment.")

# Input sliders
col1, col2, col3 = st.columns(3)

with col1:
    heart_rate = st.slider(
        "💓 Heart Rate (bpm)",
        min_value=40,
        max_value=180,
        value=80,
        step=1,
        help="Normal range: 60-100 bpm"
    )

with col2:
    oxygen_level = st.slider(
        "🫁 Oxygen Level (%)",
        min_value=70,
        max_value=100,
        value=95,
        step=1,
        help="Normal range: 95-100%"
    )

with col3:
    pain_level = st.slider(
        "😫 Pain Level",
        min_value=0,
        max_value=10,
        value=3,
        step=1,
        help="Rate pain from 0 (no pain) to 10 (severe pain)"
    )

st.divider()

# Assessment button
if st.button("🚀 Run Triage Assessment", type="primary", use_container_width=True):
    # Calculate triage score using exact formula
    score = heart_rate/10 + (100 - oxygen_level) + (pain_level * 2)
    
    # Determine triage decision based on score
    if score >= 25:
        decision = "🚨 TREAT NOW"
        priority = "CRITICAL"
        color = "red"
    elif score >= 15:
        decision = "⚠️ MONITOR"
        priority = "MODERATE"
        color = "orange"
    else:
        decision = "🟢 WAIT"
        priority = "LOW"
        color = "green"
    
    # Display results
    st.success("## 🏥 Triage Assessment Complete")
    
    # Decision display
    if color == "red":
        st.error(f"### **Decision: {decision}**")
    elif color == "orange":
        st.warning(f"### **Decision: {decision}**")
    else:
        st.info(f"### **Decision: {decision}**")
    
    # Score and priority
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Triage Score", f"{score:.2f}/100")
    with col2:
        st.metric("Priority Level", priority)
    
    # Assessment details
    with st.expander("📊 Assessment Details"):
        st.write(f"**Heart Rate:** {heart_rate} bpm")
        st.write(f"**Oxygen Level:** {oxygen_level}%")
        st.write(f"**Pain Level:** {pain_level}/10")
        st.write(f"**Scoring Formula:** score = (heart_rate/10) + (100 - oxygen) + (pain*2)")
    
    # Medical recommendation with FIXED string replacement
    clean_decision = decision.replace('🚨', '').replace('⚠️', '').replace('🟢', '').strip()
    st.info(f"**Medical Recommendation:** {clean_decision} - {priority.lower()} priority case requiring immediate attention.")

st.divider()

# Information section
with st.expander("📖 How It Works"):
    st.markdown("""
    ### 🎯 Scoring Algorithm
    
    The AI system uses a weighted scoring formula to determine patient priority:
    
    **Formula:** `score = (heart_rate/10) + (100 - oxygen) + (pain*2)`
    
    ### 🚨 Decision Thresholds
    
    | Score Range | Decision | Priority | Action |
    |-------------|----------|----------|--------|
    | **≥ 25** | 🚨 TREAT NOW | Critical | Immediate medical attention required |
    | **≥ 15** | ⚠️ MONITOR | Moderate | Close monitoring, may need treatment |
    | **< 15** | 🟢 WAIT | Low | Can wait for treatment |
    
    ### 🧪 Example Cases
    
    - **Critical Case**: HR=120, O2=85, Pain=8 → Score=39 → 🚨 TREAT NOW
    - **Moderate Case**: HR=85, O2=95, Pain=4 → Score=21.5 → ⚠️ MONITOR  
    - **Stable Case**: HR=70, O2=98, Pain=2 → Score=13 → 🟢 WAIT
    """)

# Footer
st.divider()
st.markdown("""
---
### ⚠️ Medical Disclaimer
This AI-powered triage system is designed for **educational demonstration purposes only** as part of Meta PyTorch OpenEnv Hackathon.

**Do not use this tool for actual medical decision-making.** Always consult qualified healthcare professionals for real patient assessment and treatment.

### 🏆 Project Information
- **Hackathon**: Meta PyTorch OpenEnv Hackathon
- **Technology**: Python, Streamlit, AI/ML
- **Purpose**: Demonstrate AI applications in healthcare triage
- **Status**: Educational Prototype
""")
