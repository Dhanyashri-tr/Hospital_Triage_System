import streamlit as st

st.set_page_config(page_title="AI Hospital Triage System")

st.title("🏥 AI Hospital Triage System")
st.write("Enter patient details to determine priority level")

heart_rate = st.slider("Heart Rate (bpm)", 40, 180, 80)
oxygen = st.slider("Oxygen Level (%)", 70, 100, 95)
pain = st.slider("Pain Level", 0, 10, 5)

if st.button("Analyze Patient"):
    score = heart_rate/10 + (100 - oxygen) + pain*2

    if score >= 25:
        decision = "🚨 TREAT NOW"
        priority = "HIGH"
    elif score >= 15:
        decision = "⚠️ MONITOR"
        priority = "MEDIUM"
    else:
        decision = "🟢 WAIT"
        priority = "LOW"

    st.success(f"""
    Score: {score:.2f}
    Priority: {priority}
    Decision: {decision}
    """)