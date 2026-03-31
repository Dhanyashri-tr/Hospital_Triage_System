import gradio as gr
from env import HospitalEnv
from datetime import datetime

env = HospitalEnv()

def simulate(name, severity, waiting_time, age, resources, condition):
    state = env.reset()

    # override values
    state["severity"] = severity
    state["waiting_time"] = waiting_time
    state["age"] = age
    state["resources_available"] = resources
    state["condition"] = condition
    priority_score = (
    state["severity"] * 2 +
    state["waiting_time"] * 0.5 +
    (10 if state["condition"] in ["cardiac", "stroke"] else 0)
    )
    priority_score = round(priority_score, 2)
    if priority_score >= 25:
        level = "🔴 Critical"
    elif priority_score >= 15:
        level = "🟡 Moderate"
    else:
        level = "🟢 Safe"
    condition = state["condition"].lower().strip()

    if condition == "cardiac":
        emoji = "❤️"
    elif condition == "stroke":
        emoji = "🧠"
    elif condition == "injury":
        emoji = "🦴"
    else:
        emoji = "🩺"

    # Alert Message
    if level == "🔴 Critical":
        alert = "🚨 Immediate ICU attention required!"
    elif level == "🟡 Moderate":
        alert = "⚠️ Needs attention soon"
    else:
        alert = "✅ Safe to wait"

    #  Risk Factors
    risk_factors = []

    if state["age"] > 60:
        risk_factors.append("Elderly")

    if state["severity"] > 7:
        risk_factors.append("High Severity")

    if state["waiting_time"] > 30:
        risk_factors.append("Long Wait Time")

    risk_text = ", ".join(risk_factors) if risk_factors else "None"

    # Department Suggestion
    if state["condition"] == "cardiac":
        dept = "❤️ Cardiology"
    elif state["condition"] == "stroke":
        dept = "🧠 Neurology"
    elif state["condition"] == "injury":
        dept = "🦴 Orthopedics"
    else:
        dept = "🩺 General Medicine"

    # Estimated Wait Time
    if level == "🔴 Critical":
        wait_msg = "Immediate"
    elif level == "🟡 Moderate":
        wait_msg = "Within 15 minutes"
    else:
        wait_msg = "30+ minutes"
        if state["condition"] == "cardiac":
            emoji = "❤️"
        elif state["condition"] == "stroke":
            emoji = "🧠"
        else:
            emoji = "🩺"

    # Patient ID 
    patient_id = f"P{int(state['severity']*100 + state['age'])}"

    # Timestamp
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # priority meter
    meter_width = min(priority_score * 3, 100)

    action = smart_agent(state)
    next_state, reward, done = env.step(action)

    return f"""
    <h2>👤 Patient: {name}</h2>

    <p><b>  Patient ID:</b> {patient_id}</p>
    <p><b>  Time:</b> {timestamp}</p>

    <h3>  Patient Summary</h3>

    <ul>
    <li><b>Severity:</b> {state["severity"]}</li>
    <li><b>Waiting Time:</b> {state["waiting_time"]} minutes</li>
    <li><b>Age:</b> {state["age"]}</li>
    <li><b>Condition:</b>Condition: {emoji} {state["condition"]}</li>
    </ul>

    <h3 style="color:purple;">🔥 Priority Score: {priority_score}</h3>
    <h3>📊 Priority Level: {level}</h3>

    <h3 style="color:red;">{alert}</h3>

    <p><b>⚠️ Risk Factors:</b> {risk_text}</p>
    <p><b>   Department:</b> {dept}</p>
    <p><b>⏳ Estimated Wait:</b> {wait_msg}</p>
    

    <h3 style="color:{'red' if action=='treat_now' else 'green'};">
       Decision: {action.upper()}
    </h3>

    <p><b>Reward:</b> {reward}</p>

    <p><b>Reason:</b> {explain_decision(state)}</p>
    <h3>Priority Meter</h3>
    <div style="width:100%;background:#ddd;">
    <div style="background-color:#333; border-radius:10px; overflow:hidden;">
        <div style="
            width:{meter_width}%;
            background-color:red;
            padding:8px;
            text-align:center;
            color:white;">
            {priority_score}
        </div>
    </div>
    </div>
    """

def smart_agent(state):
    if state["severity"] >= 9:
        return "treat_now"
    elif state["condition"] in ["cardiac", "stroke", "accident"]:
        return "treat_now"
    elif state["waiting_time"] > 30:
        return "monitor"
    else:
        return "wait"

def explain_decision(state):
    if state["severity"] >= 9:
        return "Critical severity → immediate treatment required"
    
    elif state["condition"] in ["cardiac", "stroke", "accident"]:
        return "Life-threatening condition → prioritized treatment"
    
    elif state["age"] > 65 and state["severity"] > 5:
        return "Elderly patient with moderate risk → prioritized"
    
    elif state["resources_available"] == 0:
        return "No resources available → patient must wait"
    
    elif state["waiting_time"] > 30:
        return "Patient waited too long → prioritized"
    
    else:
        return "Stable condition → safe to wait"

interface = gr.Interface(
    fn=simulate,
    inputs=[
        gr.Textbox(label="Patient Name"),
        gr.Slider(0, 10, label="Severity"),
        gr.Slider(0, 60, label="Waiting Time (minutes)"),
        gr.Slider(0, 100, label="Age"),
        gr.Slider(0, 5, label="Resources Available"),
        gr.Textbox(label="Condition (fever/injury/etc)")
    ],
    outputs=gr.HTML(),
    title="🏥 Hospital Triage AI System",
    description="AI-powered patient prioritization system with explainable decisions"
)

interface.launch()