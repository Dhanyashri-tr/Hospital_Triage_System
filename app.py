import streamlit as st

st.title("🏥 AI Hospital Triage System")

heart_rate = st.slider("Heart Rate", 40, 180, 80)
oxygen = st.slider("Oxygen Level", 70, 100, 95)
pain = st.slider("Pain Level", 0, 10, 5)

if st.button("Analyze"):
    score = heart_rate/10 + (100 - oxygen) + pain*2

    if score >= 25:
        st.error(f"🚨 TREAT NOW | Score: {score:.2f}")
    elif score >= 15:
        st.warning(f"⚠️ MONITOR | Score: {score:.2f}")
    else:
        st.success(f"🟢 WAIT | Score: {score:.2f}")